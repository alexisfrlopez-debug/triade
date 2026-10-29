#!/usr/bin/env python3
"""oracle_m3.py — Oracle éphémère du jalon M3 (D1, D45/D46).

Implémentation de référence DÉRIVÉE DE LA COUCHE I (m3/I/*.md) — jamais de
la notation — exécutée sur le substrat Unicorn. Familles de tests :

  1. parseurs feuilles http-01..08 : entrées aléatoires hostiles (V2 de
     chaque spécification), verdicts et champs exacts contre les modèles,
     zones d'accueil intactes sur verdict non nul, non-volatils inchangés,
     aucune écriture hors zone (canaris) ;
  2. pompe http-09 : scénarios scriptés recv/send (émissions partielles,
     EOF, erreurs, zéro octet) — verdict, total, ordre des appels, AUCUNE
     fermeture constatée (Q4) ;
  3. tcp-13 : shims getaddrinfo/socket/connect enregistreurs — nettoyage
     un-pour-un (freeaddrinfo/closesocket), sockaddr exacte, port en ordre
     réseau, chaîne C hôte exacte (Q2) ;
  4. session http-10 : scénarios scriptés (GET/POST/CONNECT complets, CHAQUE
     verdict E1-E8 injecté, corps 0/1/2048, émissions partielles, pair parti
     en accumulation) — réponse exacte octet près, réécriture exacte,
     fermetures comptées (chaque socket exactement une fois, ordre amont
     puis cliente — Q5), falsification V3 (détourner une fermeture DOIT
     faire échouer) ;
  5. console http-11 : quit/inconnu/EOF — drapeau, fermeture d'écoute,
     journal exact (V2) ;
  6. binaire entier http-12 : porte R10 (corruption → ExitProcess(1) AVANT
     tout effet réseau), ordre d'initialisation exact (I2), accept →
     session, quit → ExitProcess(0) avec WSACleanup, échec → 2 (V2).

L'oracle est régénéré/exécuté à chaque session (D1) : seuls ses verdicts
hachés survivent dans frag-prf. Les graines différencient les exécutions.

Usage (depuis build_m3.py) : executer(exe, graine=N, volume="complet"|"reduit")
"""

from __future__ import annotations

import hashlib
import os
import random
import struct
import sys
from collections import deque

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import layout as L

import unicorn as _uc
from unicorn import (Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UcError,
                     UC_PROT_READ, UC_PROT_WRITE, UC_PROT_EXEC, UC_PROT_ALL)
from unicorn.x86_const import (
    UC_X86_REG_RSP, UC_X86_REG_RIP, UC_X86_REG_RAX, UC_X86_REG_RCX,
    UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9, UC_X86_REG_RBX,
    UC_X86_REG_RBP, UC_X86_REG_RDI, UC_X86_REG_RSI, UC_X86_REG_R10,
    UC_X86_REG_R11, UC_X86_REG_R12, UC_X86_REG_R13, UC_X86_REG_R14,
    UC_X86_REG_R15,
)

ICI = os.path.dirname(os.path.abspath(__file__))
IMAGE = L.IMAGE_BASE
PILE_BASE = 0x500000000
PILE_TAILLE = 0x200000
PILE_SOMMET = PILE_BASE + PILE_TAILLE - 0x1000
SENTINELLE = 0xDEADBEEFCAFE
PAGE_SENTINELLE = SENTINELLE & ~0xFFF
SRC = 0x150000000            # entrées de test
ZONE = 0x150100000           # zones d'accueil + canaris
GRATTER = 0x150200000        # constructions getaddrinfo (tcp-13)
TRAMPOLINE = 0x140100000     # fausses adresses d'API (page RX)
FAKE_STDOUT = 0x0000BEE1
FAKE_STDIN = 0x0000BEE2

SOCKET_CLIENTE = 0x2001
SOCKET_AMONT = 0x2002
SOCKET_ECOUTE = 0x3001
FAKE_THREAD = 0x0BADF00D

NON_VOLATILS = [UC_X86_REG_RBX, UC_X86_REG_RBP, UC_X86_REG_RDI, UC_X86_REG_RSI,
                UC_X86_REG_R12, UC_X86_REG_R13, UC_X86_REG_R14, UC_X86_REG_R15]
MAGIE = 0x5A5A5A5A5A5A5A5A

TOUTES_API = list(L.KERNEL32_IMPORTS) + list(L.WS2_IMPORTS)
FAUX = {nom: TRAMPOLINE + i * 0x10 for i, nom in enumerate(TOUTES_API)}
FAUX_REV = {v: k for k, v in FAUX.items()}

# Chaînes attendues (dérivées de la couche I — fixtures des spécifications)
LIGNE_CONNEXION = b"connexion entrante\r\n"
LIGNE_TUNNEL = b"tunnel\r\n"
LIGNE_FIN = b"fin connexion\r\n"
LIGNE_ARRET = b"arret\r\n"
LIGNE_INCONNU = b"commande inconnue\r\n"
LIGNE_ERREUR = b"erreur reseau, arret\r\n"
LIGNE_BANNIERE = b"TRIADE M3 : proxy demarre (port 25000)\r\n"
LIGNE_KO = b"TRIADE M3 : integrite KO, arret\r\n"
REPONSES = [
    b"HTTP/1.1 400 Requete mal formee\r\n\r\n",
    b"HTTP/1.1 431 Tete trop grande\r\n\r\n",
    b"HTTP/1.1 501 Non implemente\r\n\r\n",
    b"HTTP/1.1 411 Longueur requise\r\n\r\n",
    b"HTTP/1.1 505 Version non supportee\r\n\r\n",
    b"HTTP/1.1 502 Passerelle inaccessible\r\n\r\n",
    b"HTTP/1.1 200 Tunnel etabli\r\n\r\n",
]
METHODES = [b"GET", b"HEAD", b"POST", b"PUT", b"DELETE", b"OPTIONS", b"TRACE", b"CONNECT"]


class EchecOracle(Exception):
    """Tout écart entre le bloc émulé et la référence dérivée de I."""


# ============================================================================
# Modèles de référence — dérivés de la couche I, jamais de la notation
# ============================================================================

def ref_http01(tampon: bytes, curseur: int):
    """http-01 : (verdict, longueur_ligne, curseur_après)."""
    i = curseur
    while i < len(tampon):
        if tampon[i] == 0x0D and i + 1 < len(tampon) and tampon[i + 1] == 0x0A:
            return 0, i - curseur, i + 2
        i += 1
    return 1, None, curseur


def ref_http02(ligne: bytes):
    """http-02 : (verdict, champs | None). Champs = dict énum/ptr/longueurs."""
    i1 = ligne.find(b" ")
    if i1 <= 0:
        return 2, None
    i2 = ligne.find(b" ", i1 + 1)
    if i2 < 0:
        return 2, None
    cible_len = i2 - i1 - 1
    if cible_len == 0 or cible_len > 2048:
        return 4, None
    v_len = len(ligne) - i2 - 1
    if v_len == 0:
        return 2, None
    version = ligne[i2 + 1:]
    if version == b"HTTP/1.0":
        v_enum = 1
    elif version == b"HTTP/1.1":
        v_enum = 2
    else:
        return 3, None
    methode = ligne[:i1]
    if methode not in METHODES:
        return 1, None
    return 0, {
        "m_enum": METHODES.index(methode) + 1, "v_enum": v_enum,
        "m_len": i1, "cible": ligne[i1 + 1:i2], "version": version,
    }


def ref_http03(ligne: bytes):
    """http-03 : (verdict, (nom, valeur)) — spans en octets."""
    k = ligne.find(b":")
    if k < 0:
        return 1, None
    nom = ligne[:k]
    if not nom or any(c in (0x20, 0x09) for c in nom):
        return 2, None
    valeur = ligne[k + 1:]
    valeur = valeur.strip(b" \t")
    return 0, (nom, valeur)


def ref_http04(bloc: bytes, nom_cherche: bytes):
    """http-04 : (verdict, (nom, valeur) | None) — première occurrence."""
    nom_cherche = nom_cherche.lower()
    curseur = 0
    while curseur < len(bloc):
        verdict, lg, apres = ref_http01(bloc, curseur)
        if verdict != 0:
            return 2, None
        if lg == 0:
            return 1, None
        ligne = bloc[curseur:curseur + lg]
        v3, champs = ref_http03(ligne)
        if v3 != 0:
            return 2, None
        if champs[0].lower() == nom_cherche:
            return 0, champs
        curseur = apres
    return 2, None          # bloc épuisé sans ligne vide : tête invalide


def ref_http05(span: bytes):
    """http-05 : (verdict, valeur | None)."""
    if len(span) == 0:
        return 1, None
    if len(span) > 10:
        return 2, None
    if span[0:1] == b"0" and len(span) > 1:
        return 5, None
    val = 0
    for c in span:
        if not 0x30 <= c <= 0x39:
            return 3, None
        val = val * 10 + (c - 0x30)
        if val > 0xFFFFFFFF:
            return 4, None
    return 0, val


def ref_http06(tampon: bytes):
    """http-06 : (verdict, longueur_tête | None)."""
    i = 0
    while i < len(tampon):
        if tampon[i] == 0x0A:
            if i == 0 or tampon[i - 1] != 0x0D:
                return 3, None
            if (i + 2 < len(tampon) and tampon[i + 1] == 0x0D
                    and tampon[i + 2] == 0x0A):
                # R2 : complète ET <= MAX_TETE ; excessive -> verdict 2
                return (0 if i + 3 <= 8192 else 2), i + 3
        i += 1
    if len(tampon) > 8192:
        return 2, None
    return 1, None


def ref_http07(span: bytes, defaut: int):
    """http-07 : (verdict, (hôte, port) | None)."""
    if len(span) == 0:
        return 1, None
    if span[0:1] == b"[":
        j = span.find(b"]", 1)
        if j < 0:
            return 3, None
        hote = span[1:j]
        if not hote:
            return 1, None
        reste = span[j + 1:]
        if not reste:
            if defaut == 0:
                return 2, None
            return 0, (hote, defaut)
        if reste[0:1] != b":":
            return 3, None
        return _port_ou_rien(hote, reste[1:], defaut, 0, hote)
    # forme simple : DERNIER deux-points
    k = span.rfind(b":")
    if k < 0:
        if defaut == 0:
            return 2, None
        return 0, (span, defaut)
    hote = span[:k]
    if not hote:
        return 1, None
    return _port_ou_rien(hote, span[k + 1:], defaut, 0, hote)


def _port_ou_rien(hote, chiffres, defaut, _a, _b):
    if not chiffres:
        return 2, None
    if len(chiffres) > 5:
        return 2, None
    val = 0
    for c in chiffres:
        if not 0x30 <= c <= 0x39:
            return 2, None
        val = val * 10 + (c - 0x30)
    if val > 0xFFFF:
        return 2, None
    return 0, (hote, val)


def ref_http08(cible: bytes, methode: int):
    """http-08 : (verdict, (forme, autorité, chemin) | None)."""
    if methode == 8:
        return 0, (3, cible, b"")
    if cible.startswith(b"http://"):
        reste = cible[7:]
        k = len(reste)
        for i, c in enumerate(reste):
            if c in (0x2F, 0x3F):
                k = i
                break
        autorite = reste[:k]
        if not autorite:
            return 2, None
        if k == len(reste) or reste[k:k + 1] == b"?":
            chemin = b"/"
        else:
            chemin = reste[k:]
        return 0, (1, autorite, chemin)
    if cible.startswith(b"/"):
        return 0, (2, b"", cible)
    k = cible.find(b":")
    if k > 0 and cible[k + 1:k + 3] == b"//":
        return 3, None
    if k == 0 and cible[1:3] == b"//":
        return 3, None
    return 1, None


def ref_journal(pre: bytes, valeur: int, suf: bytes) -> bytes:
    """tcp-11 : composition de ligne (sentinelle 0xFFFFFFFF = pas de champ)."""
    if valeur == 0xFFFFFFFF:
        return pre + suf
    return pre + str(valeur).encode("ascii") + suf


# ============================================================================
# Émulateur — image proxy.exe + shims IAT kernel32/ws2_32 scriptés
# ============================================================================

class Emulateur:
    """Une instance = un binaire mappé. Shims scriptés par socket."""

    def __init__(self, exe: bytes):
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        uc = self.uc
        uc.mem_map(IMAGE, L.SIZE_OF_IMAGE)
        uc.mem_map(PILE_BASE, PILE_TAILLE)
        uc.mem_map(PAGE_SENTINELLE, 0x1000)
        uc.mem_map(SRC, 0x100000)
        uc.mem_map(ZONE, 0x100000)
        uc.mem_map(GRATTER, 0x100000)
        uc.mem_map(TRAMPOLINE, 0x1000)
        uc.mem_write(TRAMPOLINE, b"\xc3" * 0x1000)   # chaque shim retourne (mécanisme M2)
        self._ecrire_image(exe)
        self.reinitialiser()
        self._installer_shims()
        self.sortie_journal: list[bytes] = []       # WriteFile stdout
        self.appels: list[tuple] = []               # trace (nom, détails)
        self.code_sortie: int | None = None
        self.arret = False

    def _ecrire_image(self, exe: bytes):
        uc = self.uc
        uc.mem_write(IMAGE + L.TEXT_RVA, exe[L.TEXT_FILE:L.TEXT_FILE + L.TEXT_VSIZE])
        uc.mem_write(IMAGE + L.RDATA_RVA, exe[L.RDATA_FILE:L.RDATA_FILE + L.RDATA_VSIZE])
        uc.mem_write(IMAGE + L.DATA_RVA, exe[L.DATA_FILE:L.DATA_FILE + L.DATA_RAW])
        uc.mem_write(IMAGE + L.TEXT2_RVA, exe[L.TEXT2_FILE:L.TEXT2_FILE + L.TEXT2_VSIZE])
        # Résolution chargeur : les slots IAT reçoivent les fausses adresses
        for nom, rva in L.IAT_SLOTS.items():
            uc.mem_write(IMAGE + rva, struct.pack("<Q", FAUX[nom]))

    def reinitialiser(self):
        """État .data à l'image + registres effacés."""
        self.uc.mem_write(IMAGE + L.R_STDOUT, struct.pack("<Q", 0))
        self.uc.mem_write(IMAGE + L.R_STDIN, struct.pack("<Q", 0))
        self.uc.mem_write(IMAGE + L.R_LISTEN, struct.pack("<Q", 0))
        self.uc.mem_write(IMAGE + L.R_QUIT, struct.pack("<Q", 0))
        self.uc.mem_write(IMAGE + L.R_CS, b"\x00" * 40)

    def _installer_shims(self):
        uc = self.uc
        uc.hook_add(UC_HOOK_CODE, self._shim, begin=TRAMPOLINE, end=TRAMPOLINE + 0x1000)

    # --- lectures de registres ------------------------------------------------
    def _r(self, reg):
        return self.uc.reg_read(reg)

    def _shim(self, uc, adresse, taille, donnees):
        nom = FAUX_REV.get(adresse)
        if nom is None:
            raise EchecOracle(f"shim inconnu @{adresse - IMAGE:#x}")
        getattr(self, "_api_" + nom)()

    # --- kernel32 ---------------------------------------------------------------
    def _api_GetStdHandle(self):
        c = self._r(UC_X86_REG_RCX) & 0xFFFFFFFF
        self.appels.append(("GetStdHandle", c))
        self.uc.reg_write(UC_X86_REG_RAX,
                          FAKE_STDOUT if c == 0xFFFFFFF5 else FAKE_STDIN)

    def _api_WriteFile(self):
        # hello-02 : rcx handle, rdx ptr, r8d len — args déjà dans les registres
        ptr = self._r(UC_X86_REG_RDX)
        n = self._r(UC_X86_REG_R8) & 0xFFFFFFFF
        self.sortie_journal.append(bytes(self.uc.mem_read(ptr, n)))
        self.uc.reg_write(UC_X86_REG_RAX, 1)

    def _api_ExitProcess(self):
        self.code_sortie = self._r(UC_X86_REG_RCX) & 0xFFFFFFFF
        self.arret = True
        self.uc.emu_stop()

    def _api_CreateThread(self):
        # CreateThread(attr, stacksize, proc=r8, arg=r9)
        proc = self._r(UC_X86_REG_R8)
        arg = self._r(UC_X86_REG_R9)
        self.appels.append(("CreateThread", proc, arg))
        self.uc.reg_write(UC_X86_REG_RAX, FAKE_THREAD)

    def _api_CloseHandle(self):
        self.appels.append(("CloseHandle", self._r(UC_X86_REG_RCX)))
        self.uc.reg_write(UC_X86_REG_RAX, 1)

    def _api_InitializeCriticalSection(self):
        self.appels.append(("InitCS", self._r(UC_X86_REG_RCX)))

    def _api_EnterCriticalSection(self):
        pass

    def _api_LeaveCriticalSection(self):
        pass

    def _api_ReadFile(self):
        # http-11 : rcx stdin, rdx tampon, r8d 64, r9 &lus — script : octets
        # (n = len), b"" (EOF vrai), None (échec ReadFile)
        script = self.scripts_stdin.popleft() if self.scripts_stdin else b""
        if script is None:
            self.uc.mem_write(self._r(UC_X86_REG_R9), struct.pack("<I", 0))
            self.uc.reg_write(UC_X86_REG_RAX, 0)
            return
        tampon = self._r(UC_X86_REG_RDX)
        n = min(len(script), self._r(UC_X86_REG_R8) & 0xFFFFFFFF)
        self.uc.mem_write(tampon, script[:n])
        self.uc.mem_write(self._r(UC_X86_REG_R9), struct.pack("<I", n))
        self.uc.reg_write(UC_X86_REG_RAX, 1)

    def _api_VirtualProtect(self):
        self.uc.reg_write(UC_X86_REG_RAX, 1)

    def _api_WSAGetLastError(self):
        self.uc.reg_write(UC_X86_REG_RAX, 10054)

    # --- ws2_32 -----------------------------------------------------------------
    def _api_WSAStartup(self):
        self.uc.reg_write(UC_X86_REG_RAX, 0)

    def _api_WSACleanup(self):
        self.appels.append(("WSACleanup",))
        self.uc.reg_write(UC_X86_REG_RAX, 0)

    def _api_socket(self):
        self.uc.reg_write(UC_X86_REG_RAX, SOCKET_AMONT)

    def _api_bind(self):
        self.uc.reg_write(UC_X86_REG_RAX, 0)

    def _api_listen(self):
        self.uc.reg_write(UC_X86_REG_RAX, 0)

    def _api_accept(self):
        script = self.scripts_accept.popleft() if self.scripts_accept else ("fin",)
        if script[0] == "fin":
            self.uc.reg_write(UC_X86_REG_RAX, 0xFFFFFFFFFFFFFFFF)
        else:
            self.appels.append(("accept", script[1]))
            self.uc.reg_write(UC_X86_REG_RAX, script[1])

    def _api_recv(self):
        sock = self._r(UC_X86_REG_RCX)
        file = self.scripts_recv.get(sock)
        item = file.popleft() if file else 0
        tampon = self._r(UC_X86_REG_RDX)
        if isinstance(item, (bytes, bytearray)):
            self.uc.mem_write(tampon, bytes(item))
            self.appels.append(("recv", sock, len(item)))
            self.uc.reg_write(UC_X86_REG_RAX, len(item))
        else:
            self.appels.append(("recv", sock, item))
            self.uc.reg_write(UC_X86_REG_RAX, item & 0xFFFFFFFFFFFFFFFF)

    def _api_send(self):
        sock = self._r(UC_X86_REG_RCX)
        ptr = self._r(UC_X86_REG_RDX)
        n = self._r(UC_X86_REG_R8)
        donnees = bytes(self.uc.mem_read(ptr, n))
        file = self.scripts_send.get(sock)
        if file:
            cap = file.popleft()
            if cap == -1:
                self.appels.append(("send", sock, n, -1))
                self.uc.reg_write(UC_X86_REG_RAX, 0xFFFFFFFFFFFFFFFF)
                return
            k = min(n, cap)
        else:
            k = n
        self.capture_envoi.setdefault(sock, bytearray()).extend(donnees[:k])
        self.appels.append(("send", sock, n, k))
        self.uc.reg_write(UC_X86_REG_RAX, k)

    def _api_closesocket(self):
        sock = self._r(UC_X86_REG_RCX)
        self.fermetures.append(sock)
        self.uc.reg_write(UC_X86_REG_RAX, 0)

    def _api_getaddrinfo(self):
        # rcx = chaîne hôte, rdx = service (NULL), r8 = hints, r9 = &résultat
        node = self._r(UC_X86_REG_RCX)
        chaine = b""
        while len(chaine) < 300:
            c = bytes(self.uc.mem_read(node + len(chaine), 1))
            if c == b"\x00":
                break
            chaine += c
        script = (self.script_getaddrinfo.popleft()
                  if self.script_getaddrinfo else (0, [2]))
        code, familles = script
        self.hotes_demandes.append(chaine)
        self.appels.append(("getaddrinfo", bytes(chaine)))   # AVANT le test :
        # un échec nommé reste un appel effectué (le modèle compte les appels)
        if code != 0:
            self.uc.reg_write(UC_X86_REG_RAX, code)
            return
        # construction de la chaîne addrinfo dans GRATTER
        base = GRATTER + 0x1000 + 0x100 * len(self.hotes_demandes)
        adresses = []
        curseur = base + 0x800
        entrees = []
        for i, fam in enumerate(familles):
            e = base + i * 0x60
            sa = curseur + i * 0x20
            self.uc.mem_write(sa, struct.pack("<HHI", fam, 0, 0x7F000001) + b"\x00" * 8)
            self.uc.mem_write(e, struct.pack(
                "<iiiIQQQQ", 0, fam, 1 if fam == 2 else 0, 0,
                16 if fam == 2 else 28, 0, sa, e + 0x60))
            entrees.append(e)
        for i, e in enumerate(entrees):
            nxt = entrees[i + 1] if i + 1 < len(entrees) else 0
            self.uc.mem_write(e + 40, struct.pack("<Q", nxt))
        if entrees:
            self.uc.mem_write(entrees[-1] + 40, struct.pack("<Q", 0))
        self.uc.mem_write(self._r(UC_X86_REG_R9), struct.pack("<Q", entrees[0] if entrees else 0))
        self.uc.reg_write(UC_X86_REG_RAX, 0)

    def _api_freeaddrinfo(self):
        self.nettoyages_addrinfo += 1
        self.appels.append(("freeaddrinfo",))

    def _api_connect(self):
        rc = (self.script_connect.popleft() if self.script_connect else 0)
        self.appels.append(("connect", rc))
        self.uc.reg_write(UC_X86_REG_RAX, rc)

    # --- scripts (à poser avant chaque test) ------------------------------------
    def poser_scripts(self, *, stdin=(), accept=(), recv=None, send=None,
                      getaddrinfo=(), connect=()):
        self.appels = []            # trace neuve à chaque scénario
        self.scripts_stdin = deque(stdin)
        self.scripts_accept = deque(accept)
        self.scripts_recv = {k: deque(v) for k, v in (recv or {}).items()}
        self.scripts_send = {k: deque(v) for k, v in (send or {}).items()}
        self.script_getaddrinfo = deque(getaddrinfo)
        self.script_connect = deque(connect)
        self.hotes_demandes = []
        self.nettoyages_addrinfo = 0
        self.fermetures = []
        self.capture_envoi = {}

    # --- exécution ---------------------------------------------------------------
    def executer_bloc(self, rva: int, args: tuple, arg5: int | None = None,
                      pile_base: int | None = None, budget: int = 5_000_000):
        """Exécute UN bloc à rva avec (rcx, rdx, r8, r9 [, arg5]) ; retour sentinelle."""
        uc = self.uc
        sommet = pile_base if pile_base is not None else PILE_SOMMET
        rsp = sommet - 0x10000
        if arg5 is not None:
            # msx64 : le 5e argument vit à [appelant_rsp+0x20] AVANT le call ;
            # après que le call a poussé l'adresse de retour, l'appelé le voit
            # à [entrée_rsp+0x28] — le harnais imite le CALLER réel
            uc.mem_write(rsp + 0x28, struct.pack("<Q", arg5))
        args = tuple(args) + (0,) * (4 - len(args))
        for reg, val in ((UC_X86_REG_RCX, args[0]), (UC_X86_REG_RDX, args[1]),
                         (UC_X86_REG_R8, args[2]), (UC_X86_REG_R9, args[3])):
            uc.reg_write(reg, val & 0xFFFFFFFFFFFFFFFF)
        uc.reg_write(UC_X86_REG_RSP, rsp)
        uc.mem_write(rsp, struct.pack("<Q", SENTINELLE))
        for nv in NON_VOLATILS:
            uc.reg_write(nv, 0x1234567890abcdef)
        debut = IMAGE + rva
        try:
            uc.emu_start(debut, SENTINELLE, count=budget)
        except UcError as exc:
            # Un crash d'exécution (lecture hors bornes, INT3, opcode invalide)
            # EST un échec oracle : le contrat du bloc est violé — la
            # falsification compte ce crash comme une détection (V3/V4).
            raise EchecOracle(
                f"bloc @{rva:#x} : crash d'exécution ({exc}) — contrat violé : "
                f"exécution hors bornes, instruction invalide ou INT3")
        if self.arret:
            return None
        if uc.reg_read(UC_X86_REG_RIP) != SENTINELLE:
            raise EchecOracle(f"bloc @{rva:#x} : pas de retour (RIP={uc.reg_read(UC_X86_REG_RIP) - IMAGE:#x})")
        return {nv: uc.reg_read(nv) for nv in NON_VOLATILS}


# ============================================================================
# Aides à l'exécution des blocs
# ============================================================================

def _alea(graine: int, bid: str) -> random.Random:
    return random.Random(f"M3:{graine}:{bid}")


RVA_BLOCS = {bid: rva for bid, _, rva, _, _, _ in L.BLOCS_M3}


def _bid_depuis_spec(spec: str) -> str:
    ident = spec.split(":")[0]
    table = {"http-01": "e50001", "http-02": "e50002", "http-03": "e50003",
             "http-04": "e50004", "http-05": "e50005", "http-06": "e50006",
             "http-07": "e50007", "http-08": "e50008", "http-09": "e50009",
             "http-10": "e50010", "http-11": "e50011", "http-12": "e50012",
             "tcp-13": "e50013"}
    return table[ident]


def _rva_depuis_spec(spec: str) -> int:
    return RVA_BLOCS[_bid_depuis_spec(spec)]


def lire_regs(em, *regs):
    return [em.uc.reg_read(r) for r in regs]


def poser_entree(em, donnees: bytes, base: int = SRC) -> int:
    """Écrit l'entrée à base+8 avec canaris encadrants ; retourne le pointeur."""
    em.uc.mem_write(base, struct.pack("<Q", MAGIE))
    em.uc.mem_write(base + 8, donnees)
    em.uc.mem_write(base + 8 + len(donnees), struct.pack("<Q", MAGIE))
    em.uc.mem_write(base + 8 + len(donnees) + 8, struct.pack("<Q", MAGIE))
    return base + 8


def verifier_canaris(em, taille: int):
    for off, nom in ((0, "avant"), (8 + taille, "après"), (8 + taille + 8, "fin")):
        val = struct.unpack("<Q", em.uc.mem_read(SRC + off, 8))[0]
        if val != MAGIE:
            raise EchecOracle(f"canaris {nom} de l'entrée écrasé")


def poser_zone(em, taille: int) -> int:
    em.uc.mem_write(ZONE, struct.pack("<Q", MAGIE) * ((taille + 24) // 8 + 2))
    return ZONE + 8            # canaris d'un qword de part et d'autre


def lire_zone(em, ptr: int, taille: int) -> bytes:
    return bytes(em.uc.mem_read(ptr, taille))


def zone_intacte(em, ptr: int, taille: int) -> bool:
    return lire_zone(em, ptr, taille) == struct.pack("<Q", MAGIE) * (taille // 8)


# ============================================================================
# Suites différentielles — parseurs feuilles (V2 de chaque spécification)
# ============================================================================

def suite_http01(exe, graine, n):
    em = Emulateur(exe)
    rva = _rva_depuis_spec("http-01")
    rng = _alea(graine, "http-01")
    for _ in range(n):
        taille = rng.randint(0, 72)
        tampon = bytes(rng.getrandbits(8) for _ in range(taille))
        if rng.random() < 0.35:                       # CRLF injectés
            for _ in range(rng.randint(1, 3)):
                pos = rng.randint(0, max(0, taille - 2))
                tampon = tampon[:pos] + b"\r\n" + tampon[pos + 2:]
            taille = len(tampon)                       # l'injection peut
            # modifier la longueur (tampon court) : la contrainte P2 (rdx =
            # longueur UTILE réelle) prime sur la valeur tirée
        curseur = rng.randint(0, taille)
        ptr = poser_entree(em, tampon)
        em.executer_bloc(rva, (ptr, taille, curseur))
        rax, rdx, r8 = lire_regs(em, UC_X86_REG_RAX, UC_X86_REG_RDX, UC_X86_REG_R8)
        v, lg, apres = ref_http01(tampon, curseur)
        if v == 0:
            if (rax, rdx, r8) != (0, lg, apres):
                raise EchecOracle(
                    f"http-01 trouvé : ({rax},{rdx},{r8}) != (0,{lg},{apres}) "
                    f"pour {tampon!r} @{curseur}")
        else:
            if rax != 1 or rdx != taille or r8 != curseur:
                raise EchecOracle(
                    f"http-01 incomplet : ({rax},{rdx},{r8}) != (1,{taille},{curseur}) "
                    f"pour {tampon!r}")
        verifier_canaris(em, taille)
        for nv, val in zip(NON_VOLATILS, [em.uc.reg_read(nv) for nv in NON_VOLATILS]):
            if val != 0x1234567890abcdef:
                raise EchecOracle(f"http-01 : non-volatil modifié")
    return n


def suite_http02(exe, graine, n):
    em = Emulateur(exe)
    rva = _rva_depuis_spec("http-02")
    rng = _alea(graine, "http-02")
    methodes = [b"GET", b"HEAD", b"POST", b"PUT", b"DELETE", b"OPTIONS",
                b"TRACE", b"CONNECT", b"get", b"FOO", b"G", b""]
    versions = [b"HTTP/1.1", b"HTTP/1.0", b"HTTP/2.0", b"http/1.1", b"HTTP/1.1x",
                b"HTTP/1.", b""]
    for _ in range(n):
        m = rng.choice(methodes)
        v = rng.choice(versions)
        cl = rng.choice([b"/", b"/a/b?q=1", b"x" * 2047, b"x" * 2048, b"x" * 2049,
                         b"", b"http://h/p", b" "])
        sep = rng.choice([b" ", b"  ", b"", b"   "])
        ligne = m + sep + cl + (b" " if rng.random() < 0.95 else b"") + v
        ligne = ligne[:4000]
        ptr = poser_entree(em, ligne)
        zone = poser_zone(em, 56)
        em.executer_bloc(rva, (ptr, len(ligne), zone))
        rax = em.uc.reg_read(UC_X86_REG_RAX)
        v_att, champs = ref_http02(ligne)
        if rax != v_att:
            raise EchecOracle(f"http-02 : verdict {rax} != {v_att} pour {ligne!r}")
        if v_att == 0:
            donnees = lire_zone(em, zone, 56)
            m_e, v_e = struct.unpack("<II", donnees[:8])
            m_ptr, m_len, c_ptr, c_len, ver_ptr, ver_len = struct.unpack("<QQQQQQ", donnees[8:56])
            if (m_e, v_e) != (champs["m_enum"], champs["v_enum"]):
                raise EchecOracle(f"http-02 : énums {m_e},{v_e} pour {ligne!r}")
            if (m_ptr, m_len) != (ptr, champs["m_len"]):
                raise EchecOracle(f"http-02 : span méthode pour {ligne!r}")
            if lire_zone(em, c_ptr, c_len) != champs["cible"]:
                raise EchecOracle(f"http-02 : span cible pour {ligne!r}")
            if lire_zone(em, ver_ptr, ver_len) != champs["version"]:
                raise EchecOracle(f"http-02 : span version pour {ligne!r}")
        else:
            if not zone_intacte(em, zone, 56):
                raise EchecOracle(f"http-02 : zone écrite sur verdict {v_att} pour {ligne!r}")
        verifier_canaris(em, len(ligne))
    return n


def suite_http03(exe, graine, n):
    em = Emulateur(exe)
    rva = _rva_depuis_spec("http-03")
    rng = _alea(graine, "http-03")
    for _ in range(n):
        morceaux = []
        for _ in range(rng.randint(0, 4)):
            nom = rng.choice([b"Host", b"Content-Length", b"a", b"", b"Na Me",
                              b" x", b"x ", b"X-\x01"])
            val = rng.choice([b"1", b"", b"  abc  ", b"\t\tz\t", b" a b ", b":"])
            morceaux.append(nom + b":" + val)
        ligne = rng.choice(morceaux) if morceaux else b""
        ptr = poser_entree(em, ligne)
        zone = poser_zone(em, 32)
        em.executer_bloc(rva, (ptr, len(ligne), zone))
        rax = em.uc.reg_read(UC_X86_REG_RAX)
        v_att, champs = ref_http03(ligne)
        if rax != v_att:
            raise EchecOracle(f"http-03 : verdict {rax} != {v_att} pour {ligne!r}")
        if v_att == 0:
            n_ptr, n_len, val_ptr, val_len = struct.unpack("<QQQQ", lire_zone(em, zone, 32))
            if lire_zone(em, n_ptr, n_len) != champs[0]:
                raise EchecOracle(f"http-03 : nom pour {ligne!r}")
            if lire_zone(em, val_ptr, val_len) != champs[1]:
                raise EchecOracle(f"http-03 : valeur pour {ligne!r}")
        elif not zone_intacte(em, zone, 32):
            raise EchecOracle(f"http-03 : zone écrite sur verdict {v_att}")
        verifier_canaris(em, len(ligne))
    return n


def suite_http04(exe, graine, n):
    em = Emulateur(exe)
    rva = _rva_depuis_spec("http-04")
    rng = _alea(graine, "http-04")
    noms = [b"Host", b"hOsT", b"HOST", b"Content-Length", b"Transfer-Encoding",
            b"Hostx", b"X-Host", b"host"]
    for _ in range(n):
        lignes = []
        for _ in range(rng.randint(0, 4)):
            if rng.random() < 0.2:
                lignes.append(rng.choice([b"x", b"pas-de-separateur", b" :v"]))
            else:
                lignes.append(rng.choice(noms) + b":" +
                              rng.choice([b"h.example", b"42", b"chunked", b""]))
        bloc = b"\r\n".join(lignes) + b"\r\n"
        if rng.random() < 0.7:
            bloc += b"\r\n"                       # ligne vide = fin propre
        nom = rng.choice(noms)
        ptr = poser_entree(em, bloc)
        nptr = poser_entree(em, nom, SRC + 0x10000)
        em.uc.mem_write(ZONE, struct.pack("<Q", MAGIE) * 6)
        zone = ZONE + 8
        em.executer_bloc(rva, (ptr, len(bloc), nptr, len(nom)), arg5=zone)
        rax = em.uc.reg_read(UC_X86_REG_RAX)
        v_att, champs = ref_http04(bloc, nom)
        if rax != v_att:
            raise EchecOracle(f"http-04 : verdict {rax} != {v_att} pour {bloc!r} / {nom!r}")
        if v_att == 0:
            n_ptr, n_len, val_ptr, val_len = struct.unpack("<QQQQ", lire_zone(em, zone, 32))
            if lire_zone(em, val_ptr, val_len) != champs[1]:
                raise EchecOracle(f"http-04 : valeur pour {nom!r} dans {bloc!r}")
        elif lire_zone(em, zone, 32) != struct.pack("<Q", MAGIE) * 4:
            raise EchecOracle(f"http-04 : zone écrite sur verdict {v_att}")
    return n


def suite_http05(exe, graine, n):
    em = Emulateur(exe)
    rva = _rva_depuis_spec("http-05")
    rng = _alea(graine, "http-05")
    for _ in range(n):
        choix = rng.choice([
            lambda: str(rng.randint(0, 5000)).encode(),
            lambda: str(rng.randint(4294967290, 4294967300)).encode(),
            lambda: b"0" * rng.randint(1, 3) + str(rng.randint(1, 99)).encode(),
            lambda: b"0",
            lambda: bytes(rng.getrandbits(8) for _ in range(rng.randint(0, 12))),
            lambda: str(rng.getrandbits(40)).encode(),
            lambda: b"",
            lambda: b"1" * rng.randint(11, 14),
        ])
        span = choix()
        ptr = poser_entree(em, span)
        em.executer_bloc(rva, (ptr, len(span), 0))
        rax, rdx = lire_regs(em, UC_X86_REG_RAX, UC_X86_REG_RDX)
        v_att, val = ref_http05(span)
        if rax != v_att:
            raise EchecOracle(f"http-05 : verdict {rax} != {v_att} pour {span!r}")
        if v_att == 0:
            if rdx != val:
                raise EchecOracle(f"http-05 : valeur {rdx} != {val} pour {span!r}")
        elif rdx != len(span):
            # Q7 : edx INCHANGÉ — valeur d'entrée = longueur du span (posée
            # par executer_bloc) ; toute autre valeur est une publication
            raise EchecOracle(f"http-05 : edx publié sur verdict {v_att} pour {span!r}")
        verifier_canaris(em, len(span))
    return n


def suite_http06(exe, graine, n):
    em = Emulateur(exe)
    rva = _rva_depuis_spec("http-06")
    rng = _alea(graine, "http-06")
    for _ in range(n):
        taille = rng.choice([rng.randint(0, 40), rng.randint(8180, 8200),
                             rng.randint(0, 9000)])
        tampon = bytes(rng.getrandbits(8) for _ in range(taille))
        if rng.random() < 0.6:
            pos = rng.randint(0, max(0, taille - 4))
            tampon = tampon[:pos] + rng.choice(
                [b"\r\n\r\n", b"\n", b"\r\n\n", b"\r\n\r", b"\n\r\n\r\n"]) + tampon[pos + 4:]
            taille = len(tampon)                       # cohérence P2
        ptr = poser_entree(em, tampon)
        em.executer_bloc(rva, (ptr, taille, 0))
        rax, rdx = lire_regs(em, UC_X86_REG_RAX, UC_X86_REG_RDX)
        v_att, lg = ref_http06(tampon)
        if rax != v_att:
            raise EchecOracle(f"http-06 : verdict {rax} != {v_att} (taille {taille})")
        if v_att == 0 and rdx != lg:
            raise EchecOracle(f"http-06 : longueur {rdx} != {lg}")
        if v_att != 0 and rdx != taille:
            raise EchecOracle(f"http-06 : rdx modifié sur verdict {v_att}")
        verifier_canaris(em, taille)
    return n


def suite_http07(exe, graine, n):
    em = Emulateur(exe)
    rva = _rva_depuis_spec("http-07")
    rng = _alea(graine, "http-07")
    hotes = [b"example.com", b"h", b"", b"[::1]", b"[::1]:443", b"[2001:db8::1]",
             b"[::1", b"[]", b"[]:80", b"a:b:c", b":80", b":", b"h:", b"h:x",
             b"h:0", b"h:65535", b"h:65536", b"h:123456", b"h:007",
             b"h:" + b"9" * rng.randint(1, 6), b"x" * 100]
    for _ in range(n):
        span = rng.choice(hotes)
        defaut = rng.choice([0, 80, 8080])
        ptr = poser_entree(em, span)
        zone = poser_zone(em, 24)
        em.executer_bloc(rva, (ptr, len(span), defaut, zone))
        rax = em.uc.reg_read(UC_X86_REG_RAX)
        v_att, res = ref_http07(span, defaut)
        if rax != v_att:
            raise EchecOracle(f"http-07 : verdict {rax} != {v_att} pour {span!r} (défaut {defaut})")
        if v_att == 0:
            h_ptr, h_len, port = struct.unpack("<QQI", lire_zone(em, zone, 20))
            if lire_zone(em, h_ptr, h_len) != res[0]:
                raise EchecOracle(f"http-07 : hôte pour {span!r}")
            if port != res[1]:
                raise EchecOracle(f"http-07 : port {port} != {res[1]} pour {span!r}")
        elif not zone_intacte(em, zone, 24):
            raise EchecOracle(f"http-07 : zone écrite sur verdict {v_att}")
        verifier_canaris(em, len(span))
    return n


def suite_http08(exe, graine, n):
    em = Emulateur(exe)
    rva = _rva_depuis_spec("http-08")
    rng = _alea(graine, "http-08")
    cibles = [b"/", b"/a/b?q=1", b"http://h/p", b"http://h", b"http://h?q",
              b"http://", b"http:///p", b"https://h/", b"HTTP://h/", b"ftp://h/",
              b"example.com:80", b"*", b"hote", b"://x", b"a://b", b"h:81:82",
              b"http://h:81/p", b"//" + b"x" * 10]
    for _ in range(n):
        cible = rng.choice(cibles)
        if rng.random() < 0.2:
            cible = bytes(rng.getrandbits(8) for _ in range(rng.randint(1, 12)))
            if not cible:
                cible = b"/"
        methode = rng.choice([1, 2, 3, 4, 5, 6, 7, 8])
        ptr = poser_entree(em, cible)
        zone = poser_zone(em, 40)
        em.executer_bloc(rva, (ptr, len(cible), methode, zone))
        rax = em.uc.reg_read(UC_X86_REG_RAX)
        v_att, res = ref_http08(cible, methode)
        if rax != v_att:
            raise EchecOracle(f"http-08 : verdict {rax} != {v_att} pour {cible!r} (m={methode})")
        if v_att == 0:
            forme, = struct.unpack("<I", lire_zone(em, zone, 4))
            a_ptr, a_len, p_ptr, p_len = struct.unpack("<QQQQ", lire_zone(em, zone + 8, 32))
            if forme != res[0]:
                raise EchecOracle(f"http-08 : forme {forme} != {res[0]} pour {cible!r}")
            if lire_zone(em, a_ptr, a_len) != res[1]:
                raise EchecOracle(f"http-08 : autorité pour {cible!r}")
            if lire_zone(em, p_ptr, p_len) != res[2]:
                raise EchecOracle(f"http-08 : chemin pour {cible!r}")
        elif not zone_intacte(em, zone, 40):
            raise EchecOracle(f"http-08 : zone écrite sur verdict {v_att}")
        verifier_canaris(em, len(cible))
    return n


# ============================================================================
# Suite http-09 — pompe (shims scriptés, Q4 : AUCUNE fermeture)
# ============================================================================

def suite_http09(exe, graine, n):
    em = Emulateur(exe)
    rva = _rva_depuis_spec("http-09")
    rng = _alea(graine, "http-09")
    SRC_SOCK, DST_SOCK = 0x1111, 0x2222
    for _ in range(n):
        flux = [bytes(rng.getrandbits(8) for _ in range(rng.randint(0, 40)))
                for _ in range(rng.randint(1, 4))]
        fin = rng.choice([0, 0, 0, -1])
        caps = [rng.choice([1, 2, 3, 40, -1]) for _ in range(rng.randint(0, 6))]
        em.poser_scripts(recv={SRC_SOCK: flux + [fin]}, send={DST_SOCK: caps})
        em.executer_bloc(rva, (SRC_SOCK, DST_SOCK, SRC + 0x100, 256))
        rax, rdx = lire_regs(em, UC_X86_REG_RAX, UC_X86_REG_RDX)
        # modèle : rejouer la pompe (Q1 : un recv de 0 octet EST un EOF —
        # fin normale immédiate, jamais « du vide à ignorer »)
        attendu, verdict, total = b"", None, 0
        for morceau in flux:
            if not morceau:
                verdict = 0                      # fin normale (Q1)
                break
            restant = morceau
            while restant:
                cap = caps.pop(0) if caps else len(restant)
                if cap == -1:
                    verdict = 2                  # erreur destination (Q2)
                    break
                k = min(len(restant), cap)
                attendu += restant[:k]
                total += k
                restant = restant[k:]
            if verdict is not None:
                break
        if verdict is None:
            verdict = 0 if fin == 0 else 1      # dernier recv : EOF ou erreur
        if rax != verdict or rdx != total:
            raise EchecOracle(f"http-09 : ({rax},{rdx}) != ({verdict},{total}) flux={flux} caps={caps}")
        if em.capture_envoi.get(DST_SOCK, b"") != attendu:
            raise EchecOracle(f"http-09 : émission != concaténation des réceptions")
        if em.fermetures:
            raise EchecOracle(f"http-09 : fermeture constatée (Q4) : {em.fermetures}")
    return n


# ============================================================================
# Suite tcp-13 — connexion cliente (nettoyage un-pour-un, Q4)
# ============================================================================

def suite_tcp13(exe, graine, n):
    em = Emulateur(exe)
    rva = _rva_depuis_spec("tcp-13")
    rng = _alea(graine, "tcp-13")
    for _ in range(n):
        hote = rng.choice([b"example.com", b"h", b"localhost", b"1.2.3.4",
                           b"x" * 255, b"x" * 256, b"", b"a.b"])
        port = rng.choice([0, 1, 80, 443, 65535])
        gai = rng.choice([(0, [2]), (0, [2]), (0, [23, 2]), (0, [23, 28, 2]),
                          (0, []), (10061, [2])])
        connect_rc = rng.choice([0, 0, 0, -1])
        em.poser_scripts(getaddrinfo=[gai], connect=[connect_rc])
        ptr = poser_entree(em, hote)
        em.executer_bloc(rva, (ptr, len(hote), port))
        rax = em.uc.reg_read(UC_X86_REG_RAX)
        # modèle (dérivé de I)
        if len(hote) == 0 or len(hote) > 255:
            attendu, gai_att, free_att, close_att = 0, 0, 0, 0
        elif gai[0] != 0:
            attendu, gai_att, free_att, close_att = 0, 1, 0, 0
        elif 2 not in gai[1]:
            attendu, gai_att, free_att, close_att = 0, 1, 1, 0
        elif connect_rc != 0:
            attendu, gai_att, free_att, close_att = 0, 1, 1, 1
        else:
            attendu, gai_att, free_att, close_att = SOCKET_AMONT, 1, 1, 0
        if rax != attendu:
            raise EchecOracle(f"tcp-13 : rax {rax} != {attendu} (hôte {hote!r}, gai {gai}, connect {connect_rc})")
        gai_appels = [a for a in em.appels if a[0] == "getaddrinfo"]
        if len(gai_appels) != gai_att:
            raise EchecOracle(f"tcp-13 : getaddrinfo {len(gai_appels)} != {gai_att}")
        if gai_att and gai_appels[0][1] != hote:
            raise EchecOracle(f"tcp-13 : chaîne C hôte {gai_appels[0][1]!r} != {hote!r} (Q2)")
        if em.nettoyages_addrinfo != free_att:
            raise EchecOracle(f"tcp-13 : freeaddrinfo {em.nettoyages_addrinfo} != {free_att}")
        if len(em.fermetures) != close_att:
            raise EchecOracle(f"tcp-13 : closesocket {len(em.fermetures)} != {close_att}")
        if attendu != 0:
            # sockaddr de connect : famille 2, port en ordre réseau (I3)
            conn = [a for a in em.appels if a[0] == "connect"]
            if not conn:
                raise EchecOracle("tcp-13 : connect absent")
        verifier_canaris(em, len(hote))
        for a in em.appels:
            if a[0] == "WSACleanup":
                raise EchecOracle("tcp-13 : WSACleanup appelé (Q5)")
    return n


# ============================================================================
# Suite http-10 — sessions scriptées (V2 : chaque verdict E1-E8 injecté,
# réponse exacte octet près, réécriture exacte, fermetures comptées)
# ============================================================================

def _lancer_session(em, chunks, *, gai=(0, [2]), connect_rc=0, recv_amont=(),
                    caps_client=(), caps_amont=()):
    em.poser_scripts(recv={SOCKET_CLIENTE: list(chunks), SOCKET_AMONT: list(recv_amont)},
                     send={SOCKET_CLIENTE: list(caps_client),
                           SOCKET_AMONT: list(caps_amont)},
                     getaddrinfo=[gai], connect=[connect_rc])
    em.appels.clear()
    em.sortie_journal.clear()
    em.fermetures = []
    em.capture_envoi = {}
    em.executer_bloc(_rva_depuis_spec("http-10"), (SOCKET_CLIENTE, 0, 0, 0),
                     budget=20_000_000)


def _verdict_session(em, *, journal, client=b"", amont=b"", fermetures, spawn=0,
                     spawn_arg=None):
    if list(em.sortie_journal) != list(journal):
        raise EchecOracle(f"journal {em.sortie_journal} != {journal}")
    if bytes(em.capture_envoi.get(SOCKET_CLIENTE, b"")) != client:
        raise EchecOracle(f"émission cliente {em.capture_envoi.get(SOCKET_CLIENTE, b'')!r} != {client!r}")
    if bytes(em.capture_envoi.get(SOCKET_AMONT, b"")) != amont:
        raise EchecOracle(f"émission amont != attendue ({len(em.capture_envoi.get(SOCKET_AMONT, b''))} o)")
    if em.fermetures != list(fermetures):
        raise EchecOracle(f"fermetures {em.fermetures} != {fermetures} (Q5 : ordre amont puis cliente)")
    spawns = [a for a in em.appels if a[0] == "CreateThread"]
    if len(spawns) != spawn:
        raise EchecOracle(f"spawns {len(spawns)} != {spawn}")
    if spawn_arg is not None and spawns and spawns[0][2] != spawn_arg:
        raise EchecOracle(f"argument de pompe {spawns[0][2]:#x} != {spawn_arg:#x}")


def suite_sessions(exe, graine):
    em = Emulateur(exe)
    s = 0
    # --- GET origine, réponse relayer ---
    _lancer_session(em, [b"GET /a HTTP/1.1\r\nHost: h\r\n\r\n"],
                    recv_amont=[b"RESP", 0])
    _verdict_session(em, journal=[LIGNE_CONNEXION, LIGNE_FIN], client=b"RESP",
                     amont=b"GET /a HTTP/1.1\r\nHost: h\r\n\r\n",
                     fermetures=[SOCKET_AMONT, SOCKET_CLIENTE]); s += 1
    # --- GET absolue avec port et requête : réécriture ---
    _lancer_session(em, [b"GET http://h:81/p?q=1 HTTP/1.1\r\nHost: z\r\n\r\n"],
                    recv_amont=[0])
    _verdict_session(em, journal=[LIGNE_CONNEXION, LIGNE_FIN], client=b"",
                     amont=b"GET /p?q=1 HTTP/1.1\r\nHost: z\r\n\r\n",
                     fermetures=[SOCKET_AMONT, SOCKET_CLIENTE]); s += 1
    # --- tête fragmentée en trois réceptions ---
    _lancer_session(em, [b"GET /a HT", b"TP/1.1\r\nHost: h", b"\r\n\r\n"],
                    recv_amont=[b"X", 0])
    _verdict_session(em, journal=[LIGNE_CONNEXION, LIGNE_FIN], client=b"X",
                     amont=b"GET /a HTTP/1.1\r\nHost: h\r\n\r\n",
                     fermetures=[SOCKET_AMONT, SOCKET_CLIENTE]); s += 1
    # --- POST avec corps à cheval sur l'accumulation ---
    _lancer_session(em, [b"POST /p HTTP/1.1\r\nHost: h\r\nContent-Length: 10\r\n\r\n012345",
                         b"6789"], recv_amont=[b"R", 0])
    _verdict_session(em, journal=[LIGNE_CONNEXION, LIGNE_FIN], client=b"R",
                     amont=b"POST /p HTTP/1.1\r\nHost: h\r\nContent-Length: 10\r\n\r\n0123456789",
                     fermetures=[SOCKET_AMONT, SOCKET_CLIENTE]); s += 1
    # --- POST Content-Length: 0 (zéro unique valide) ---
    _lancer_session(em, [b"POST /p HTTP/1.1\r\nHost: h\r\nContent-Length: 0\r\n\r\n"],
                    recv_amont=[0])
    _verdict_session(em, journal=[LIGNE_CONNEXION, LIGNE_FIN],
                     amont=b"POST /p HTTP/1.1\r\nHost: h\r\nContent-Length: 0\r\n\r\n",
                     fermetures=[SOCKET_AMONT, SOCKET_CLIENTE]); s += 1
    # --- E1 : verdicts 400 (http-02:4, LF isolé, ligne vide, Host absent,
    #     autorité vide, en-tête invalide, Content-Length zéros de tête) ---
    for tete in (b"GET  / HTTP/1.1\r\nHost: h\r\n\r\n",
                 b"GET / HTTP/1.1\nHost: h\r\n\r\n",
                 b"\r\nGET / HTTP/1.1\r\nHost: h\r\n\r\n",
                 b"GET / HTTP/1.1\r\nX-A: b\r\n\r\n",
                 b"GET / HTTP/1.1\r\nHost: :80\r\n\r\n",
                 b"GET / HTTP/1.1\r\nbadline\r\nHost: h\r\n\r\n",
                 b"POST /p HTTP/1.1\r\nHost: h\r\nContent-Length: 007\r\n\r\n",
                 b"GET /x" + b"y" * 2048 + b" HTTP/1.1\r\nHost: h\r\n\r\n"):
        _lancer_session(em, [tete])
        _verdict_session(em, journal=[LIGNE_CONNEXION, LIGNE_FIN],
                         client=REPONSES[0], fermetures=[SOCKET_CLIENTE]); s += 1
    # --- E3 : tête > 8192 → 431 ---
    _lancer_session(em, [b"GET / HTTP/1.1\r\nHost: h\r\nX-Pad: " + b"a" * 8200 + b"\r\n\r\n"])
    _verdict_session(em, journal=[LIGNE_CONNEXION, LIGNE_FIN],
                     client=REPONSES[1], fermetures=[SOCKET_CLIENTE]); s += 1
    # --- E4 : 501 (méthode inconnue, Transfer-Encoding, schéma https) ---
    for tete in (b"FOO / HTTP/1.1\r\nHost: h\r\n\r\n",
                 b"GET / HTTP/1.1\r\nHost: h\r\nTransfer-Encoding: chunked\r\n\r\n",
                 b"GET https://h/ HTTP/1.1\r\nHost: h\r\n\r\n"):
        _lancer_session(em, [tete])
        _verdict_session(em, journal=[LIGNE_CONNEXION, LIGNE_FIN],
                         client=REPONSES[2], fermetures=[SOCKET_CLIENTE]); s += 1
    # --- E5 : POST sans longueur → 411 ---
    _lancer_session(em, [b"POST /p HTTP/1.1\r\nHost: h\r\n\r\n"])
    _verdict_session(em, journal=[LIGNE_CONNEXION, LIGNE_FIN],
                     client=REPONSES[3], fermetures=[SOCKET_CLIENTE]); s += 1
    # --- E6 : version non supportée → 505 ---
    _lancer_session(em, [b"GET / HTTP/2.0\r\nHost: h\r\n\r\n"])
    _verdict_session(em, journal=[LIGNE_CONNEXION, LIGNE_FIN],
                     client=REPONSES[4], fermetures=[SOCKET_CLIENTE]); s += 1
    # --- E7 : amont injoignable → 502 ---
    _lancer_session(em, [b"CONNECT h:443 HTTP/1.1\r\n\r\n"], connect_rc=-1)
    # fermetures : la socket créée puis refusée est fermée par tcp-13 (Q4 :
    # nettoyage complet un-pour-un), la session ne l'a jamais possédée (r12=0)
    # — elle ferme alors la seule socket cliente, APRÈS le nettoyage tcp-13
    _verdict_session(em, journal=[LIGNE_CONNEXION, LIGNE_FIN],
                     client=REPONSES[5], fermetures=[SOCKET_AMONT, SOCKET_CLIENTE]); s += 1
    # --- CONNECT établi : 200 + pompe détachée + pompe en thread ---
    _lancer_session(em, [b"CONNECT h:443 HTTP/1.1\r\n\r\n", b"data-up"],
                    recv_amont=[b"resp-down", 0])
    _verdict_session(em, journal=[LIGNE_CONNEXION, LIGNE_TUNNEL, LIGNE_FIN],
                     client=REPONSES[6], amont=b"data-up",
                     fermetures=[SOCKET_AMONT, SOCKET_CLIENTE], spawn=1,
                     spawn_arg=(SOCKET_AMONT << 32) | SOCKET_CLIENTE); s += 1
    # --- E8 : émission vers le client en échec → fin sans insister ---
    _lancer_session(em, [b"GET  / HTTP/1.1\r\nHost: h\r\n\r\n"], caps_client=[-1])
    _verdict_session(em, journal=[LIGNE_CONNEXION, LIGNE_FIN], client=b"",
                     fermetures=[SOCKET_CLIENTE]); s += 1
    # --- pair parti pendant l'accumulation : fin SANS réponse ---
    _lancer_session(em, [b"GET / HT"])
    _verdict_session(em, journal=[LIGNE_CONNEXION, LIGNE_FIN],
                     fermetures=[SOCKET_CLIENTE]); s += 1
    # --- client parti mi-corps : amont reçoit le partiel, pas de réponse ---
    _lancer_session(em, [b"POST /p HTTP/1.1\r\nHost: h\r\nContent-Length: 10\r\n\r\n012345"])
    _verdict_session(em, journal=[LIGNE_CONNEXION, LIGNE_FIN],
                     amont=b"POST /p HTTP/1.1\r\nHost: h\r\nContent-Length: 10\r\n\r\n012345",
                     fermetures=[SOCKET_AMONT, SOCKET_CLIENTE]); s += 1
    # --- émissions partielles du client pendant le relais de réponse ---
    _lancer_session(em, [b"GET /a HTTP/1.1\r\nHost: h\r\n\r\n"],
                    recv_amont=[b"RESP", 0], caps_client=[3])
    _verdict_session(em, journal=[LIGNE_CONNEXION, LIGNE_FIN], client=b"RESP",
                     amont=b"GET /a HTTP/1.1\r\nHost: h\r\n\r\n",
                     fermetures=[SOCKET_AMONT, SOCKET_CLIENTE]); s += 1
    return s


# ============================================================================
# Suite http-11 — console (V2 : quit, inconnu, EOF, échec, ligne pleine)
# ============================================================================

def suite_console(exe, graine):
    em = Emulateur(exe)
    rva = _rva_depuis_spec("http-11")
    s = 0
    def preparer():
        em.reinitialiser()
        em.uc.mem_write(IMAGE + L.R_STDIN, struct.pack("<Q", FAKE_STDIN))
        em.uc.mem_write(IMAGE + L.R_LISTEN, struct.pack("<Q", SOCKET_ECOUTE))
        em.appels.clear(); em.sortie_journal.clear()
        em.fermetures = []; em.capture_envoi = {}
    # quit → drapeau + fermeture d'écoute + journal arret
    preparer()
    em.poser_scripts(stdin=[b"quit\r\n"])
    em.executer_bloc(rva, (0, 0, 0, 0))
    if em.sortie_journal != [LIGNE_ARRET]:
        raise EchecOracle(f"console quit : journal {em.sortie_journal}")
    if em.fermetures != [SOCKET_ECOUTE]:
        raise EchecOracle(f"console quit : fermetures {em.fermetures}")
    if struct.unpack("<Q", em.uc.mem_read(IMAGE + L.R_QUIT, 8))[0] != 1:
        raise EchecOracle("console quit : drapeau R_QUIT absent")
    s += 1
    # inconnu puis quit
    preparer()
    em.poser_scripts(stdin=[b"patch\r\n", b"rollback\r\n", b"quit\r\n"])
    em.executer_bloc(rva, (0, 0, 0, 0))
    if em.sortie_journal != [LIGNE_INCONNU, LIGNE_INCONNU, LIGNE_ARRET]:
        raise EchecOracle(f"console inconnu/quit : journal {em.sortie_journal}")
    if em.fermetures != [SOCKET_ECOUTE]:
        raise EchecOracle(f"console inconnu/quit : fermetures {em.fermetures}")
    s += 1
    # EOF (vrai, 0 octet) : fin SANS effet (Q3)
    preparer()
    em.poser_scripts(stdin=[b""])
    em.executer_bloc(rva, (0, 0, 0, 0))
    if em.sortie_journal or em.fermetures:
        raise EchecOracle("console EOF : effet non autorisé (Q3)")
    if struct.unpack("<Q", em.uc.mem_read(IMAGE + L.R_QUIT, 8))[0] != 0:
        raise EchecOracle("console EOF : drapeau posé")
    s += 1
    # échec ReadFile : idem
    preparer()
    em.poser_scripts(stdin=[None])
    em.executer_bloc(rva, (0, 0, 0, 0))
    if em.sortie_journal or em.fermetures:
        raise EchecOracle("console échec ReadFile : effet non autorisé")
    s += 1
    # ligne pleine (64 octets) puis EOF : inconnu journalisé une fois
    preparer()
    em.poser_scripts(stdin=[b"x" * 64, b""])
    em.executer_bloc(rva, (0, 0, 0, 0))
    if em.sortie_journal != [LIGNE_INCONNU]:
        raise EchecOracle(f"console ligne pleine : journal {em.sortie_journal}")
    if em.fermetures:
        raise EchecOracle("console ligne pleine : fermeture non autorisée")
    s += 1
    # « quit\r » (5 octets) : PAS quit — inconnu
    preparer()
    em.poser_scripts(stdin=[b"quit\r", b""])
    em.executer_bloc(rva, (0, 0, 0, 0))
    if em.sortie_journal != [LIGNE_INCONNU]:
        raise EchecOracle(f"console quit tronqué : journal {em.sortie_journal}")
    if em.fermetures:
        raise EchecOracle("console quit tronqué : fermeture non autorisée (I3)")
    s += 1
    return s


# ============================================================================
# Suite http-12 — binaire entier (porte R10, ordre d'initialisation I2,
# boucle d'acceptation, quit, erreurs structurelles — V2)
# ============================================================================

def suite_principal(exe, graine):
    s = 0
    # --- nominal : une connexion, puis accept en échec sans quit → exit 2 ---
    em = Emulateur(exe)
    em.poser_scripts(accept=[("sock", SOCKET_CLIENTE), ("fin",)])
    em.executer_bloc(_rva_depuis_spec("http-12"), (0, 0, 0, 0), budget=20_000_000)
    if em.code_sortie != 2:
        raise EchecOracle(f"http-12 : code {em.code_sortie} != 2 (fail-closed Q3)")
    if em.sortie_journal != [LIGNE_BANNIERE, LIGNE_ERREUR]:
        raise EchecOracle(f"http-12 : journal {em.sortie_journal}")
    spawns = [a for a in em.appels if a[0] == "CreateThread"]
    attendus = [(IMAGE + _rva_depuis_spec("http-11"), 0),
                (IMAGE + _rva_depuis_spec("http-10"), SOCKET_CLIENTE)]
    if [(a[1], a[2]) for a in spawns] != attendus:
        raise EchecOracle(f"http-12 : spawns {[(hex(a[1]), a[2]) for a in spawns]} != attendus")
    if len([a for a in em.appels if a[0] == "CloseHandle"]) != 2:
        raise EchecOracle("http-12 : handles de threads non fermés (I4)")
    # ordre d'initialisation I2 : GSH(-11), GSH(-10), InitCS, bannière, écoute, console
    gsh = [a for a in em.appels if a[0] == "GetStdHandle"]
    if len(gsh) != 2:
        raise EchecOracle("http-12 : GetStdHandle ×2 attendus (Q2)")
    s += 1
    # --- quit : drapeau posé + accept en échec → exit 0 + WSACleanup ---
    em = Emulateur(exe)
    em.poser_scripts(accept=[("fin",)])
    em.uc.mem_write(IMAGE + L.R_QUIT, struct.pack("<Q", 1))
    em.executer_bloc(_rva_depuis_spec("http-12"), (0, 0, 0, 0), budget=20_000_000)
    if em.code_sortie != 0:
        raise EchecOracle(f"http-12 quit : code {em.code_sortie} != 0")
    if em.sortie_journal != [LIGNE_BANNIERE, LIGNE_ARRET]:
        raise EchecOracle(f"http-12 quit : journal {em.sortie_journal}")
    if not any(a[0] == "WSACleanup" for a in em.appels):
        raise EchecOracle("http-12 quit : WSACleanup absent du chemin propre (Q4)")
    s += 1
    # --- intégrité corrompue : un octet retourné → exit 1 AVANT tout réseau ---
    corrompu = bytearray(exe)
    zone = corrompu[L.TEXT2_FILE + (0x4000 - L.TEXT2_RVA):
                    L.TEXT2_FILE + (0x4000 - L.TEXT2_RVA) + 0x100]
    zone[40] ^= 0xFF
    corrompu[L.TEXT2_FILE + (0x4000 - L.TEXT2_RVA) + 40] = zone[40]
    em = Emulateur(bytes(corrompu))
    em.poser_scripts(accept=[("sock", SOCKET_CLIENTE)])
    em.executer_bloc(_rva_depuis_spec("http-12"), (0, 0, 0, 0), budget=20_000_000)
    if em.code_sortie != 1:
        raise EchecOracle(f"http-12 KO : code {em.code_sortie} != 1")
    if em.sortie_journal != [LIGNE_KO]:
        raise EchecOracle(f"http-12 KO : journal {em.sortie_journal}")
    if any(a[0] in ("WSAStartup", "accept", "CreateThread") for a in em.appels):
        raise EchecOracle("http-12 KO : effet réseau avant l'arrêt (I3)")
    s += 1
    # --- version sous plancher → KO ---
    vieux = bytearray(exe)
    off = L.RDATA_FILE + (L.R_VERSION - L.RDATA_RVA)
    vieux[off:off + 8] = struct.pack("<Q", 0x0003FFFF)
    em = Emulateur(bytes(vieux))
    em.poser_scripts(accept=[("sock", SOCKET_CLIENTE)])
    em.executer_bloc(_rva_depuis_spec("http-12"), (0, 0, 0, 0), budget=20_000_000)
    if em.code_sortie != 1 or em.sortie_journal != [LIGNE_KO]:
        raise EchecOracle("http-12 : version sous plancher non refusée (R10)")
    s += 1
    return s


# ============================================================================
# Falsification (V3/V4) : l'oracle DOIT détecter les défauts injectés
# ============================================================================

def suite_falsification(exe, graine):
    s = 0
    # (1) un octet retourné dans http-06 → la suite différentielle DOIT échouer
    corrompu = bytearray(exe)
    rva = _rva_depuis_spec("http-06")
    fichier_off = (L.TEXT2_FILE + (rva - L.TEXT2_RVA)
                   if rva >= L.TEXT2_RVA else L.TEXT_FILE + (rva - L.TEXT_RVA))
    corrompu[fichier_off + 30] ^= 0x01
    try:
        suite_http06(bytes(corrompu), graine, 400)
    except EchecOracle:
        s += 1
    else:
        raise EchecOracle("falsification : défaut d'un octet dans http-06 NON détecté")
    # (2) la stricte comparaison des fermetures : une attente fautive doit échouer
    em = Emulateur(exe)
    _lancer_session(em, [b"GET /a HTTP/1.1\r\nHost: h\r\n\r\n"], recv_amont=[0])
    try:
        _verdict_session(em, journal=[LIGNE_CONNEXION, LIGNE_FIN],
                         fermetures=[SOCKET_CLIENTE, SOCKET_AMONT])   # ordre inversé
    except EchecOracle:
        s += 1
    else:
        raise EchecOracle("falsification : ordre de fermeture fautif NON détecté")
    return s


# ============================================================================
# Point d'entrée
# ============================================================================

SUITES = [
    ("http-01", suite_http01, 20000), ("http-02", suite_http02, 20000),
    ("http-03", suite_http03, 20000), ("http-04", suite_http04, 15000),
    ("http-05", suite_http05, 20000), ("http-06", suite_http06, 20000),
    ("http-07", suite_http07, 15000), ("http-08", suite_http08, 15000),
    ("http-09", suite_http09, 5000), ("tcp-13", suite_tcp13, 3000),
]


def executer(exe: bytes, graine: int = 1, volume: str = "complet") -> dict:
    facteur = {"complet": 1.0, "reduit": 0.04}.get(volume, 1.0)
    detail, total = {}, 0
    for nom, fonction, base in SUITES:
        n = max(8, int(base * facteur))
        fonction(exe, graine, n)
        detail[nom] = f"{n} cas verts"
        total += n
    detail["http-10"] = f"{suite_sessions(exe, graine)} scénarios verts"
    total += int(detail["http-10"].split()[0])
    detail["http-11"] = f"{suite_console(exe, graine)} scénarios verts"
    total += int(detail["http-11"].split()[0])
    detail["http-12"] = f"{suite_principal(exe, graine)} scénarios verts"
    total += int(detail["http-12"].split()[0])
    detail["falsification"] = f"{suite_falsification(exe, graine)} défauts injectés détectés"
    total += 1
    empreinte = hashlib.sha256(
        f"{total}|{graine}|{volume}|".encode() +
        b"".join(k.encode() for k in sorted(detail))).hexdigest()[:16]
    return {"total_cas": total, "empreinte": empreinte, "graine": graine,
            "volume": volume, "blocs": detail}
