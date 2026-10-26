#!/usr/bin/env python3
"""oracle_m2.py — Oracle éphémère du jalon M2 (D1, D29).

Implémentation de référence DÉRIVÉE DE LA COUCHE I (m2/I/*.md) — jamais de
la notation — exécutée sur le substrat Unicorn. Six familles de tests :

  1. blocs unitaires : entrées aléatoires contraintes par les pré-conditions,
     sorties comparées à la référence (echo v1/v2, journal, libc-09,
     wrappers net/thr) ;
  2. MOTEUR DE PATCH (tcp-07) : application réelle en émulation — copie du
     staging en croissance, bascule par qword aligné unique, appel de
     l'entrée basculée (comportement v2), rollback (entrée restaurée
     octet pour octet, comportement v1), refus fail-closed (staging
     corrompu, absent, état incohérent, protection refusée) ;
  3. PATCH EN SESSION (tcp-09) : bascule entre deux recv d'une MÊME session
     émulée — le moteur réel s'exécute pendant la connexion (pile
     secondaire, registres du thread sauvegardés/restaurés), la réponse
     suivante change, la connexion continue (critère de sortie M2) ;
  4. console (tcp-10) : commandes patch/rollback/quit/inconnu, refus,
     fin de flux ;
  5. binaire entier (tcp-12) : porte R10 (corruption → arrêt code 1 AVANT
     tout appel réseau), chemin nominal (bannière, écoute, connexion,
     arrêt code 0), erreurs structurelles (code 2) ;
  6. falsification : la corruption d'un octet de chaque bloc embarqué doit
     être détectée (zéro silence).

L'oracle est régénéré/exécuté à chaque session (D1) : seuls ses verdicts
hachés survivent dans frag-prf. Les graines différencient les exécutions.

Usage (depuis build_m2.py) : executer(exe, graine=N, volume="complet"|"reduit")
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
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE
from unicorn.x86_const import (
    UC_X86_REG_RSP, UC_X86_REG_RIP, UC_X86_REG_RAX, UC_X86_REG_RCX,
    UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9, UC_X86_REG_RBX,
    UC_X86_REG_RBP, UC_X86_REG_RDI, UC_X86_REG_RSI, UC_X86_REG_R10,
    UC_X86_REG_R11, UC_X86_REG_R12, UC_X86_REG_R13, UC_X86_REG_R14,
    UC_X86_REG_R15, UC_X86_REG_EFLAGS,
)

from keystone import Ks, KS_ARCH_X86, KS_MODE_64

ICI = os.path.dirname(os.path.abspath(__file__))
M1_DIR = os.path.join(os.path.dirname(ICI), "m1")
IMAGE = L.IMAGE_BASE
PILE_BASE = 0x500000000
PILE_TAILLE = 0x100000
PILE_SOMMET = PILE_BASE + PILE_TAILLE - 0x1000
ALT_SOMMET = PILE_SOMMET - 0x2000          # pile secondaire (patch en session)
SENTINELLE = 0xDEADBEEFCAFE
PAGE_SENTINELLE = SENTINELLE & ~0xFFF
CANARI_BASE = PILE_SOMMET - 0x3000     # sous les cadres légitimes (conn : -0x490 ; pile
                                       # secondaire du patch : -0x20A0) — profondeur > 0xC00
SRC = 0x150000000                          # grattage : source
DST = 0x150100000                          # grattage : destination
TMP = 0x150200000                          # grattage : tampon
TRAMPOLINE = 0x140100000                   # fausses adresses d'API (page RX)
FAKE_STDOUT = 0x0000BEE1
FAKE_STDIN = 0x0000BEE2
FAKE_SOCK = 0x2001

NON_VOLATILS = [UC_X86_REG_RBX, UC_X86_REG_RBP, UC_X86_REG_RDI, UC_X86_REG_RSI,
                UC_X86_REG_R12, UC_X86_REG_R13, UC_X86_REG_R14, UC_X86_REG_R15]
TOUS_REGISTRES = [UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_RBX,
                  UC_X86_REG_RSP, UC_X86_REG_RBP, UC_X86_REG_RSI, UC_X86_REG_RDI,
                  UC_X86_REG_R8, UC_X86_REG_R9, UC_X86_REG_R10, UC_X86_REG_R11,
                  UC_X86_REG_R12, UC_X86_REG_R13, UC_X86_REG_R14, UC_X86_REG_R15,
                  UC_X86_REG_EFLAGS]
MAGIE = 0x5A5A5A5A5A5A5A5A

TOUTES_API = list(L.KERNEL32_IMPORTS) + list(L.WS2_IMPORTS)
FAUX = {nom: TRAMPOLINE + i * 0x10 for i, nom in enumerate(TOUTES_API)}
FAUX_REV = {v: k for k, v in FAUX.items()}


class EchecOracle(Exception):
    """Tout écart entre le bloc émulé et la référence dérivée de I."""


# --- Assemblage local (notations explicites, pour images synthétiques) ---------

def assembler_notation(chemin: str, rva: int) -> bytes:
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    with open(chemin, encoding="utf-8") as f:
        lignes = [l.strip() for l in f.read().splitlines()
                  if l.strip() and not l.strip().startswith(";")]
    octets, adresse = b"", rva
    for ligne in lignes:
        enc, _ = ks.asm(ligne, adresse)
        if not enc:
            raise EchecOracle(f"{chemin} : ligne inassemblable : {ligne!r}")
        octets += bytes(enc)
        adresse += len(enc)
    return octets


def image_libc09() -> bytes:
    """Image synthétique : libc-05 @0x1300 + libc-09 @0x1440.

    libc-09 n'est pas embarqué dans echo.exe (aucun appelant à M2) : le
    verrou croisé le vérifie contre sa notation, l'oracle l'exécute ici en
    compagnie de sa dépendance, aux adresses du plan d'adressage.
    """
    exe = bytearray(b"\x00" * L.TAILLE_FICHIER)
    for chemin, rva in (
            (os.path.join(M1_DIR, "notation", "libc-05-zone-alloc.asm"), 0x1300),
            (os.path.join(ICI, "notation", "libc-09-zone-alloc-ts.asm"), 0x1440)):
        octets = assembler_notation(chemin, rva)
        exe[L.TEXT_FILE + (rva - L.TEXT_RVA): L.TEXT_FILE + (rva - L.TEXT_RVA) + len(octets)] = octets
    return bytes(exe)


# --- Références dérivées de la couche I -----------------------------------------

def _alea(graine: int, bid: str) -> random.Random:
    return random.Random(f"M2:{graine}:{bid}")


def ref_echo_v1(tampon: bytes) -> bytes:
    """tcp-08 Q2 (R1) : transformation identité."""
    return tampon


def ref_echo_v2(tampon: bytes) -> bytes:
    """tcp-08 Q2 (R2) : majuscules ASCII a-z, autres octets intacts."""
    return bytes((b - 0x20) if 0x61 <= b <= 0x7A else b for b in tampon)


def ref_zone_alloc(curseur: int, taille: int, align: int):
    """libc-05 (héritage M1, modèle du curseur) : (pointeur|0, nouveau_curseur)."""
    if taille > L.ARENE_TAILLE:
        return 0, curseur
    if align == 0 or (align & (align - 1)) != 0 or align > 64:
        return 0, curseur
    offset = (curseur + align - 1) & ~(align - 1)
    if offset + taille > L.ARENE_TAILLE:
        return 0, curseur
    return IMAGE + L.ARENE_BASE + offset, offset + taille


def ref_itoa(v: int) -> bytes:
    return str(v).encode("ascii")


# --- Émulateur -------------------------------------------------------------------

class Emulateur:
    """Une instance = un binaire mappé. Shims IAT kernel32 + ws2_32 scriptés."""

    def __init__(self, exe: bytes):
        exe = bytes(exe)
        self.exe = exe
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        uc = self.uc
        uc.mem_map(IMAGE, L.SIZE_OF_IMAGE)
        uc.mem_map(PILE_BASE, PILE_TAILLE)
        uc.mem_map(PAGE_SENTINELLE, 0x1000)
        uc.mem_map(SRC, 0x300000)
        self._ecrire_image(exe)
        self.regions_patchables: list[tuple[int, int]] = []
        self.reinitialiser_donnees()
        # L'intégrité de l'image se mesure APRÈS résolution de l'IAT par le
        # chargeur (les shims remplacent les hint/names — comportement légitime).
        self.image_reference = self.image_courante()
        self._shims_poses = False

    def _ecrire_image(self, exe: bytes):
        uc = self.uc
        uc.mem_write(IMAGE + L.TEXT_RVA, exe[L.TEXT_FILE:L.TEXT_FILE + L.TEXT_VSIZE])
        uc.mem_write(IMAGE + L.RDATA_RVA, exe[L.RDATA_FILE:L.RDATA_FILE + L.RDATA_VSIZE])
        uc.mem_write(IMAGE + L.DATA_RVA, exe[L.DATA_FILE:L.DATA_FILE + L.DATA_RAW])
        uc.mem_write(IMAGE + L.TEXT2_RVA, exe[L.TEXT2_FILE:L.TEXT2_FILE + L.TEXT2_VSIZE])

    def image_courante(self) -> bytes:
        uc = self.uc
        return (bytes(uc.mem_read(IMAGE + L.TEXT_RVA, L.TEXT_VSIZE))
                + bytes(uc.mem_read(IMAGE + L.RDATA_RVA, L.RDATA_VSIZE))
                + bytes(uc.mem_read(IMAGE + L.TEXT2_RVA, L.TEXT2_VSIZE)))

    def reinitialiser_donnees(self):
        """Image restaurée depuis l'exe, .data vierge, IAT sur les shims,
        journaux et scripts remis à zéro."""
        self._ecrire_image(self.exe)
        self.uc.mem_write(IMAGE + L.DATA_RVA, b"\x00" * L.DATA_VSIZE)
        for nom, faux in FAUX.items():
            self.uc.mem_write(IMAGE + L.IAT_SLOTS[nom], struct.pack("<Q", faux))
        self.sortie = bytearray()          # stdout (WriteFile)
        self.envois: list[bytes] = []      # socket (send)
        self.code_sortie = None
        self.appels_ws2: list[tuple] = []
        self.appels_vp: list[tuple] = []
        self.threads_crees: list[tuple] = []
        self.fermetures: list[int] = []
        self.handles_fermes: list[int] = []
        self.cs_entrees = 0
        self.cs_sorties = 0
        self.file_recv: deque = deque()
        self.file_send: deque = deque()
        self.file_accept: deque = deque()
        self.file_stdin: deque = deque()
        self.retour_wsastartup = 0
        self.retour_socket = FAKE_SOCK
        self.retour_bind = 0
        self.retour_listen = 0
        self.retour_vp = 1
        self.attente = None

    def poser_etat(self, stdout=FAKE_STDOUT, stdin=FAKE_STDIN, listen=0):
        """Pré-conditions P5 : handles et socket cachés en .data par tcp-12."""
        if stdout:
            self.uc.mem_write(IMAGE + L.R_STDOUT, struct.pack("<Q", stdout))
        if stdin:
            self.uc.mem_write(IMAGE + L.R_STDIN, struct.pack("<Q", stdin))
        if listen:
            self.uc.mem_write(IMAGE + L.R_LISTEN, struct.pack("<Q", listen))

    def lire_qword(self, rva: int) -> int:
        return struct.unpack("<Q", self.uc.mem_read(IMAGE + rva, 8))[0]

    def installer_shims(self):
        if self._shims_poses:
            return
        uc = self.uc
        uc.mem_map(TRAMPOLINE, 0x1000)
        uc.mem_write(TRAMPOLINE, b"\xc3" * 0x1000)

        def retour(uc_):
            rsp = uc_.reg_read(UC_X86_REG_RSP)
            adr = struct.unpack("<Q", uc_.mem_read(rsp, 8))[0]
            uc_.reg_write(UC_X86_REG_RSP, rsp + 8)
            uc_.reg_write(UC_X86_REG_RIP, adr)

        def crochet(uc_, adresse, taille, _):
            nom = FAUX_REV.get(adresse)
            if nom is None:
                return
            rcx = uc_.reg_read(UC_X86_REG_RCX)
            rdx = uc_.reg_read(UC_X86_REG_RDX)
            r8 = uc_.reg_read(UC_X86_REG_R8)
            r9 = uc_.reg_read(UC_X86_REG_R9)
            if nom == "GetStdHandle":
                c = rcx & 0xFFFFFFFF
                uc_.reg_write(UC_X86_REG_RAX, FAKE_STDOUT if c == 0xFFFFFFF5
                              else FAKE_STDIN if c == 0xFFFFFFF6 else 0)
            elif nom == "WriteFile":
                self.sortie += bytes(uc_.mem_read(rdx, r8))
                uc_.reg_write(UC_X86_REG_RAX, 1)
            elif nom == "ExitProcess":
                self.code_sortie = rcx & 0xFFFFFFFF
                uc_.emu_stop()
                return
            elif nom == "CreateThread":
                self.threads_crees.append((r8, r9))
                uc_.reg_write(UC_X86_REG_RAX, 0x100 + 8 * len(self.threads_crees))
            elif nom == "VirtualProtect":
                self.appels_vp.append((rcx, rdx, r8 & 0xFFFFFFFF))
                uc_.reg_write(UC_X86_REG_RAX, self.retour_vp)
            elif nom == "InitializeCriticalSection":
                pass
            elif nom == "EnterCriticalSection":
                self.cs_entrees += 1
            elif nom == "LeaveCriticalSection":
                self.cs_sorties += 1
            elif nom == "ReadFile":
                if not self.file_stdin:
                    uc_.reg_write(UC_X86_REG_RAX, 0)
                else:
                    item = self.file_stdin.popleft()
                    if item is False:
                        uc_.reg_write(UC_X86_REG_RAX, 0)
                    else:
                        uc_.mem_write(rdx, item)
                        uc_.mem_write(r9, struct.pack("<Q", len(item)))
                        uc_.reg_write(UC_X86_REG_RAX, 1)
            elif nom == "CloseHandle":
                self.handles_fermes.append(rcx)
                uc_.reg_write(UC_X86_REG_RAX, 1)
            elif nom == "WSAStartup":
                self.appels_ws2.append(("WSAStartup", rcx & 0xFFFFFFFF, rdx))
                uc_.reg_write(UC_X86_REG_RAX, self.retour_wsastartup & 0xFFFFFFFF)
            elif nom == "socket":
                self.appels_ws2.append(("socket", rcx, rdx, r8))
                uc_.reg_write(UC_X86_REG_RAX,
                              self.retour_socket if self.retour_socket != -1
                              else 0xFFFFFFFFFFFFFFFF)
            elif nom == "bind":
                addr = bytes(uc_.mem_read(rdx, 16))
                self.appels_ws2.append(("bind", rcx, addr, r8))
                uc_.reg_write(UC_X86_REG_RAX, self.retour_bind & 0xFFFFFFFF)
            elif nom == "listen":
                self.appels_ws2.append(("listen", rcx, rdx))
                uc_.reg_write(UC_X86_REG_RAX, self.retour_listen & 0xFFFFFFFF)
            elif nom == "accept":
                self.appels_ws2.append(("accept", rcx, rdx, r8))
                if not self.file_accept:
                    uc_.reg_write(UC_X86_REG_RAX, 0xFFFFFFFFFFFFFFFF)
                else:
                    item = self.file_accept.popleft()
                    if item == "quit":
                        # Simule l'effet du thread console : drapeau posé,
                        # socket d'écoute fermée, acceptation débloquée.
                        uc_.mem_write(IMAGE + L.R_QUIT, struct.pack("<Q", 1))
                        uc_.reg_write(UC_X86_REG_RAX, 0xFFFFFFFFFFFFFFFF)
                    else:
                        uc_.reg_write(UC_X86_REG_RAX, item)
            elif nom == "recv":
                if not self.file_recv:
                    uc_.reg_write(UC_X86_REG_RAX, 0xFFFFFFFFFFFFFFFF)
                else:
                    item = self.file_recv.popleft()
                    if isinstance(item, tuple) and item[0] == "stop":
                        # Arrêt orchestré : le moteur de patch s'exécutera
                        # PENDANT la connexion, la charge utile servie à la
                        # reprise (critère M2).
                        self.attente = {"rdx": rdx, "r8": r8, "payload": item[1]}
                        uc_.emu_stop()
                        return
                    if isinstance(item, int):
                        uc_.reg_write(UC_X86_REG_RAX,
                                      item if item >= 0 else 0xFFFFFFFFFFFFFFFF)
                    else:
                        uc_.mem_write(rdx, item)
                        uc_.reg_write(UC_X86_REG_RAX, len(item))
            elif nom == "send":
                n = r8
                self.envois.append(bytes(uc_.mem_read(rdx, n)))
                if not self.file_send:
                    uc_.reg_write(UC_X86_REG_RAX, n)
                else:
                    k = self.file_send.popleft()
                    uc_.reg_write(UC_X86_REG_RAX,
                                  k if k >= 0 else 0xFFFFFFFFFFFFFFFF)
            elif nom == "closesocket":
                self.appels_ws2.append(("closesocket", rcx))
                self.fermetures.append(rcx)
                uc_.reg_write(UC_X86_REG_RAX, 0)
            elif nom == "WSAGetLastError":
                uc_.reg_write(UC_X86_REG_RAX, 10054)
            elif nom == "WSACleanup":
                self.appels_ws2.append(("WSACleanup",))
                uc_.reg_write(UC_X86_REG_RAX, 0)
            else:
                raise EchecOracle(f"shim non implémenté : {nom}")
            retour(uc_)

        self.hook = uc.hook_add(UC_HOOK_CODE, crochet)
        self._shims_poses = True

    def appeler(self, rva: int, args: tuple = (0, 0, 0, 0), arg5: int | None = None,
                limite: int = 2_000_000, pile: int | None = None):
        """Appelle un bloc : pile alignée, sentinel, non-volatiles magiques.

        `arg5` : cinquième argument posé à [rsp+0x28] (loge conventionnelle).
        `pile` : sommet alternatif (patch en session — pile secondaire).
        """
        uc = self.uc
        sommet = pile if pile is not None else PILE_SOMMET
        uc.reg_write(UC_X86_REG_RSP, sommet - 8)
        uc.mem_write(sommet - 8, struct.pack("<Q", SENTINELLE))
        if arg5 is not None:
            uc.mem_write(sommet - 8 + 0x28, struct.pack("<Q", arg5))
        for reg, val in zip((UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9), args):
            uc.reg_write(reg, val)
        for reg in NON_VOLATILS:
            uc.reg_write(reg, MAGIE)
        uc.reg_write(UC_X86_REG_RAX, 0)
        uc.mem_write(CANARI_BASE, b"\xaa" * 0xC00)
        uc.emu_start(IMAGE + rva, SENTINELLE, count=limite)

    def reprendre(self, limite: int = 2_000_000):
        """Reprend le bloc arrêté par un shim orchestré (recv « stop ») :
        sert la charge utile attendue, rend la main après l'appel recv,
        poursuit l'exécution jusqu'au sentinel."""
        uc = self.uc
        att = self.attente
        if att is None:
            raise EchecOracle("reprendre() sans arrêt orchestré")
        uc.mem_write(att["rdx"], att["payload"])
        rsp = uc.reg_read(UC_X86_REG_RSP)
        adr = struct.unpack("<Q", uc.mem_read(rsp, 8))[0]
        uc.reg_write(UC_X86_REG_RSP, rsp + 8)
        uc.reg_write(UC_X86_REG_RAX, len(att["payload"]))
        self.attente = None
        uc.emu_start(adr, SENTINELLE, count=limite)

    def instantane(self) -> dict:
        return {reg: self.uc.reg_read(reg) for reg in TOUS_REGISTRES}

    def restaurer(self, snap: dict):
        for reg, val in snap.items():
            self.uc.reg_write(reg, val)

    def verifier_enveloppe(self, rax_attendu=None, image=True):
        """RSP restauré, sentinel consommé, non volatils intacts, canari
        intact, image inchangée hors régions patchables."""
        uc = self.uc
        if uc.reg_read(UC_X86_REG_RSP) != PILE_SOMMET:
            raise EchecOracle(f"RSP non restauré : {uc.reg_read(UC_X86_REG_RSP):#x}")
        for reg in NON_VOLATILS:
            if uc.reg_read(reg) != MAGIE:
                raise EchecOracle("registre non volatil modifié (I2/I3)")
        if bytes(uc.mem_read(CANARI_BASE, 0xC00)) != b"\xaa" * 0xC00:
            raise EchecOracle("écriture sauvage sous la pile")
        if image:
            self._comparer_image()
        rax = uc.reg_read(UC_X86_REG_RAX)
        if rax_attendu is not None and rax != rax_attendu:
            raise EchecOracle(f"rax = {rax:#x}, attendu {rax_attendu:#x}")
        return rax

    def _comparer_image(self):
        cur, ref = self.image_courante(), self.image_reference
        if cur == ref:
            return
        tranches = [(L.TEXT_RVA, L.TEXT_VSIZE), (L.RDATA_RVA, L.RDATA_VSIZE),
                    (L.TEXT2_RVA, L.TEXT2_VSIZE)]
        offset = 0
        for base, taille in tranches:
            for i in range(taille):
                if cur[offset + i] != ref[offset + i]:
                    rva = base + i
                    if not any(debut <= rva < fin for debut, fin in self.regions_patchables):
                        raise EchecOracle(f"image modifiée hors régions patchables : RVA {rva:#x}")
            offset += taille

    def donnees(self) -> bytes:
        return bytes(self.uc.mem_read(IMAGE + L.DATA_RVA, L.DATA_VSIZE))


# --- Suites unitaires ------------------------------------------------------------

def _base_fichier(rva: int) -> int:
    """Offset fichier d'un RVA (sections .text/.rdata/.text2)."""
    if rva >= L.TEXT2_RVA:
        return L.TEXT2_FILE + (rva - L.TEXT2_RVA)
    if rva >= L.RDATA_RVA:
        return L.RDATA_FILE + (rva - L.RDATA_RVA)
    return L.TEXT_FILE + (rva - L.TEXT_RVA)


def _octets_fichier(exe: bytes, rva: int, n: int) -> bytes:
    return exe[_base_fichier(rva): _base_fichier(rva) + n]


def _somme_qwords(octets: bytes) -> int:
    return sum(struct.unpack(f"<{len(octets) // 8}Q", octets)) & 0xFFFFFFFFFFFFFFFF


def suite_echo_v1(em: Emulateur, rng: random.Random, cas: int):
    """tcp-08:R1 — identité exacte, bornes, sur place et séparées, n = 0."""
    for _ in range(cas):
        n = rng.choice((0, 1, 2, 3, 7, 15, 16, 17, 33, 64, 255, 1024,
                        rng.randrange(0, 1024)))
        src = bytes(rng.randrange(256) for _ in range(1024))
        sur_place = rng.random() < 0.5
        em.reinitialiser_donnees()
        em.uc.mem_write(SRC, src)
        em.uc.mem_write(DST, b"\x5c" * 1024)
        dst = SRC if sur_place else DST
        em.appeler(L.ECHO_ENTREE, (dst, SRC, n))
        rax = em.verifier_enveloppe(n)
        obtenu = bytes(em.uc.mem_read(dst if not sur_place else SRC, 1024))
        if obtenu[:n] != ref_echo_v1(src[:n]):
            raise EchecOracle(f"echo v1 : dst diverge (n={n})")
        if not sur_place and obtenu[n:] != b"\x5c" * (1024 - n):
            raise EchecOracle(f"echo v1 : écriture au-delà de dst+n (Q3, n={n})")
        if not sur_place and bytes(em.uc.mem_read(SRC, 1024)) != src:
            raise EchecOracle("echo v1 : source modifiée (Q3)")


def suite_echo_v2(em: Emulateur, rng: random.Random, cas: int, exe: bytes):
    """tcp-08:R2 — le staging EST la notation v2 ; installé en croissance,
    l'appel de la croissance produit les majuscules (bornes, sur place)."""
    attendu_notation = assembler_notation(
        os.path.join(ICI, "notation", "tcp-08-echo-v2.asm"), L.ECHO_CROISSANCE)
    staging = _octets_fichier(exe, L.R_STAGING, 128, "rdata")
    if staging != attendu_notation + b"\x90" * (128 - len(attendu_notation)):
        raise EchecOracle("staging .rdata != notation tcp-08-echo-v2 (R5)")
    em.regions_patchables = [(L.ECHO_CROISSANCE, L.ECHO_CROISSANCE + 0x80)]
    for _ in range(cas):
        n = rng.choice((0, 1, 2, 3, 7, 15, 16, 17, 33, 64, 255, 1024,
                        rng.randrange(0, 1024)))
        src = bytes(rng.choice((0x41, 0x61, 0x7A, 0x20, 0x00, 0xFF, rng.randrange(256)))
                    for _ in range(1024))
        sur_place = rng.random() < 0.5
        em.reinitialiser_donnees()
        em.uc.mem_write(IMAGE + L.ECHO_CROISSANCE, staging)
        em.uc.mem_write(SRC, src)
        em.uc.mem_write(DST, b"\x5c" * 1024)
        dst = SRC if sur_place else DST
        em.appeler(L.ECHO_CROISSANCE, (dst, SRC, n))
        rax = em.verifier_enveloppe(n)
        obtenu = bytes(em.uc.mem_read(dst if not sur_place else SRC, 1024))
        if obtenu[:n] != ref_echo_v2(src[:n]):
            raise EchecOracle(f"echo v2 : majuscules divergent (n={n})")
        if not sur_place and obtenu[n:] != b"\x5c" * (1024 - n):
            raise EchecOracle(f"echo v2 : écriture au-delà de dst+n (Q3, n={n})")


def suite_patch(em: Emulateur, exe: bytes, phase: int) -> int:
    """tcp-07 — le cœur de M2 : application réelle, effet, rollback, refus."""
    em.installer_shims()
    entree_orig = _octets_fichier(exe, L.ECHO_ENTREE, 8)
    em.regions_patchables = [(L.ECHO_ENTREE, L.ECHO_ENTREE + 8),
                             (L.ECHO_CROISSANCE, L.ECHO_CROISSANCE + 0x80)]
    cas = 0

    # a. mode invalide -> 1, aucun effet
    em.reinitialiser_donnees()
    em.poser_etat()
    em.appeler(0x4400, (9,))
    em.verifier_enveloppe(1)
    cas += 1

    if phase < 2:
        # dev.1 : staging absent -> 2 ; rollback à vide -> 4 ; entrée intacte
        em.appeler(0x4400, (0,))
        em.verifier_enveloppe(2)
        em.appeler(0x4400, (1,))
        em.verifier_enveloppe(4)
        if bytes(em.uc.mem_read(IMAGE + L.ECHO_ENTREE, 8)) != entree_orig:
            raise EchecOracle("dev.1 : entrée echo modifiée sans staging (Q5)")
        return cas + 2

    staging = _octets_fichier(exe, L.R_STAGING, 128, "rdata")

    # b. application : copie, bascule, protection appariée, état
    em.reinitialiser_donnees()
    em.poser_etat()
    em.appeler(0x4400, (0,))
    em.verifier_enveloppe(0)
    if len(em.appels_vp) != 2 or em.appels_vp[0][2] != 4 or em.appels_vp[1][2] != 0x20:
        raise EchecOracle(f"patch : VirtualProtect non appariés RW/RX : {em.appels_vp}")
    if (em.appels_vp[0][0] != IMAGE + 0x4000 or em.appels_vp[0][1] != 0x700):
        raise EchecOracle("patch : page/étendue de protection inattendues (Q4)")
    if bytes(em.uc.mem_read(IMAGE + L.ECHO_CROISSANCE, 128)) != staging:
        raise EchecOracle("patch : croissance != staging octet pour octet (Q1)")
    rel = L.ECHO_CROISSANCE - (L.ECHO_ENTREE + 5)
    bascule = bytes([0xE9]) + struct.pack("<i", rel) + b"\x90\x90\x90"
    if bytes(em.uc.mem_read(IMAGE + L.ECHO_ENTREE, 8)) != bascule:
        raise EchecOracle("patch : entrée != E9 rel32 + NOP x3 (Q1/Q3)")
    if em.lire_qword(L.R_ENTREE_SAUVEE) != struct.unpack("<Q", entree_orig)[0]:
        raise EchecOracle("patch : entrée originale non sauvegardée (Q1)")
    if em.lire_qword(L.R_ETAT_PATCH) != 1:
        raise EchecOracle("patch : état != 1 (Q1)")
    cas += 1

    # c. LE PATCH EST EFFECTIF : l'entrée basculée sert les majuscules
    echantillon = b"Triade m2 : serveur echo!"
    em.uc.mem_write(SRC, echantillon)
    em.appeler(L.ECHO_ENTREE, (DST, SRC, len(echantillon)))
    em.verifier_enveloppe(len(echantillon))
    if bytes(em.uc.mem_read(DST, len(echantillon))) != ref_echo_v2(echantillon):
        raise EchecOracle("patch : l'entrée basculée ne sert pas v2 (Q1)")
    cas += 1

    # d. double application -> 4 sans effet
    em.appeler(0x4400, (0,))
    em.verifier_enveloppe(4)
    cas += 1

    # e. rollback : entrée restaurée octet pour octet, comportement v1
    em.appeler(0x4400, (1,))
    em.verifier_enveloppe(0)
    if bytes(em.uc.mem_read(IMAGE + L.ECHO_ENTREE, 8)) != entree_orig:
        raise EchecOracle("rollback : entrée non restaurée (Q2)")
    if em.lire_qword(L.R_ETAT_PATCH) != 0:
        raise EchecOracle("rollback : état != 0 (Q2)")
    em.appeler(L.ECHO_ENTREE, (DST, SRC, len(echantillon)))
    em.verifier_enveloppe(len(echantillon))
    if bytes(em.uc.mem_read(DST, len(echantillon))) != echantillon:
        raise EchecOracle("rollback : comportement v1 non retrouvé (Q2)")
    cas += 2

    # f. rollback à vide -> 4
    em.appeler(0x4400, (1,))
    em.verifier_enveloppe(4)
    cas += 1

    # g. staging corrompu -> refus 3 AVANT toute écriture, service v1 préservé
    em.reinitialiser_donnees()
    em.poser_etat()
    em.uc.mem_write(IMAGE + L.R_STAGING + 7, bytes([staging[7] ^ 0xFF]))
    em.appeler(0x4400, (0,))
    em.verifier_enveloppe(3)
    if bytes(em.uc.mem_read(IMAGE + L.ECHO_ENTREE, 8)) != entree_orig:
        raise EchecOracle("falsification staging : entrée modifiée malgré le refus (Q5)")
    if em.appels_vp:
        raise EchecOracle("falsification staging : protection touchée avant refus (Q5)")
    em.uc.mem_write(SRC, echantillon)
    em.appeler(L.ECHO_ENTREE, (DST, SRC, len(echantillon)))
    em.verifier_enveloppe(len(echantillon))
    if bytes(em.uc.mem_read(DST, len(echantillon))) != echantillon:
        raise EchecOracle("falsification staging : service v1 non préservé (E1)")
    cas += 2

    # h. protection refusée -> 5, aucun effet
    em.reinitialiser_donnees()
    em.poser_etat()
    em.retour_vp = 0
    em.appeler(0x4400, (0,))
    em.verifier_enveloppe(5)
    if bytes(em.uc.mem_read(IMAGE + L.ECHO_ENTREE, 8)) != entree_orig:
        raise EchecOracle("protection refusée : entrée modifiée (Q5)")
    if em.lire_qword(L.R_ETAT_PATCH) != 0:
        raise EchecOracle("protection refusée : état changé (Q5)")
    cas += 1
    return cas


def suite_libc09(rng: random.Random, cas: int) -> int:
    """libc-09 — image synthétique (libc-05 + libc-09) : modèle du curseur
    hérité + appariement exact Enter/Leave sur tous les chemins."""
    em = Emulateur(image_libc09())
    em.installer_shims()
    aligns_valides = [1, 2, 4, 8, 16, 32, 64]
    aligns_invalides = [0, 3, 5, 63, 65, 128]
    for _ in range(cas):
        em.reinitialiser_donnees()
        curseur = 0
        for _etape in range(rng.randrange(2, 6)):
            if rng.random() < 0.2:
                taille = rng.choice((L.ARENE_TAILLE + 1, 0x7D0, 0x800, 1 << 40))
                align = rng.choice(aligns_valides)
            elif rng.random() < 0.15:
                taille = rng.randrange(0, 64)
                align = rng.choice(aligns_invalides)
            else:
                taille = rng.choice((0, 1, 2, 3, 8, 15, 16, 17, 33, 64,
                                     rng.randrange(0, 200)))
                align = rng.choice(aligns_valides)
            attendu, curseur_apres = ref_zone_alloc(curseur, taille, align)
            ecs, lcs = em.cs_entrees, em.cs_sorties
            em.appeler(0x1440, (taille, align))
            rax = em.verifier_enveloppe(attendu)
            if em.cs_entrees != ecs + 1 or em.cs_sorties != lcs + 1:
                raise EchecOracle("libc-09 : Enter/Leave non appariés (Q3)")
            if struct.unpack("<Q", em.uc.mem_read(IMAGE + L.R_CURSEUR, 8))[0] != curseur_apres:
                raise EchecOracle("libc-09 : curseur != modèle libc-05 (Q1/Q2)")
            curseur = curseur_apres
    return cas


def suite_net(em: Emulateur, rng: random.Random, cas: int) -> int:
    """tcp-01..05 — arguments exacts, nettoyage par chemin d'échec, passages."""
    em.installer_shims()
    addr_attendu = b"\x02\x00\x61\xa8\x00\x00\x00\x00" + b"\x00" * 8
    for i in range(cas):
        em.reinitialiser_donnees()
        mode = i % 6
        if mode == 1:
            em.retour_wsastartup = 1
        elif mode == 2:
            em.retour_socket = -1
        elif mode == 3:
            em.retour_bind = 1
        elif mode == 4:
            em.retour_listen = 1
        em.appeler(0x4000)
        rax = em.verifier_enveloppe(0 if 1 <= mode <= 4 else FAKE_SOCK)
        noms = [a[0] for a in em.appels_ws2]
        attendus = {1: ["WSAStartup"], 2: ["WSAStartup", "socket", "WSACleanup"],
                    3: ["WSAStartup", "socket", "bind", "closesocket", "WSACleanup"],
                    4: ["WSAStartup", "socket", "bind", "listen", "closesocket", "WSACleanup"]}
        attendu = attendus.get(mode, ["WSAStartup", "socket", "bind", "listen"])
        if noms != attendu:
            raise EchecOracle(f"tcp-01 mode {mode} : appels {noms}")
        if mode not in attendus:
            wsa, sock, bind, listen_ = em.appels_ws2
            if wsa[1] != 0x202:
                raise EchecOracle("tcp-01 : WSAStartup != 0x0202 (Q2)")
            if not (PILE_SOMMET - 0x400 < wsa[2] < PILE_SOMMET):
                raise EchecOracle("tcp-01 : WSADATA hors du cadre (Q4/I3)")
            if (sock[1], sock[2], sock[3]) != (2, 1, 6):
                raise EchecOracle("tcp-01 : socket != AF_INET/SOCK_STREAM/TCP (Q2)")
            if bind[2] != addr_attendu or bind[3] != 16:
                raise EchecOracle(f"tcp-01 : sockaddr inattendu : {bind[2].hex()}")
            if listen_[1] != FAKE_SOCK or listen_[2] != 8:
                raise EchecOracle("tcp-01 : listen != (socket, 8) (Q2)")
        # passages : accept / recv / send / close
        em.file_accept.append(0x777)
        em.appeler(0x4100, (FAKE_SOCK,))
        em.verifier_enveloppe(0x777)
        em.file_recv.append(b"abc")
        em.appeler(0x4140, (FAKE_SOCK, DST, 16))
        em.verifier_enveloppe(3)
        if bytes(em.uc.mem_read(DST, 3)) != b"abc":
            raise EchecOracle("tcp-03 : octets reçus divergents (Q1)")
        em.file_send.append(-1)
        em.appeler(0x4180, (FAKE_SOCK, DST, 3))
        em.verifier_enveloppe(0xFFFFFFFFFFFFFFFF)
        em.appeler(0x41C0, (FAKE_SOCK,))
        em.verifier_enveloppe(0)
        if not em.fermetures or em.fermetures[-1] != FAKE_SOCK:
            raise EchecOracle("tcp-05 : closesocket non appelé (Q1)")
    return cas * 6


def suite_spawn(em: Emulateur, rng: random.Random, cas: int) -> int:
    """tcp-06 — (proc, arg) transmis intacts, handle/0 propagés."""
    em.installer_shims()
    for _ in range(cas):
        proc = rng.choice((0x4800, 0x4980, 0x4000, IMAGE + 0x1234))
        arg = rng.randrange(0, 1 << 32)
        em.reinitialiser_donnees()
        em.appeler(0x4300, (proc, arg))
        handle = em.verifier_enveloppe()
        if em.threads_crees != [(proc, arg)]:
            raise EchecOracle(f"tcp-06 : threads {em.threads_crees} != ({proc:#x}, {arg})")
        if handle != 0x108:
            raise EchecOracle("tcp-06 : handle inattendu (Q1)")
    return cas


def suite_journal(em: Emulateur, rng: random.Random, cas: int) -> int:
    """tcp-11 — composition exacte, BOOL, Enter/Leave appariés, sentinel."""
    em.installer_shims()
    for _ in range(cas):
        sans_champ = rng.random() < 0.3
        valeur = 0xFFFFFFFF if sans_champ else rng.randrange(0, 4294967295)
        pre = bytes(rng.randrange(65, 91) for _ in range(rng.randrange(0, 21)))
        suf = bytes(rng.randrange(97, 123) for _ in range(rng.randrange(0, 17)))
        if len(pre) + 12 + len(suf) > 64:
            suf = suf[:64 - 12 - len(pre)]
        em.reinitialiser_donnees()
        em.poser_etat()
        em.uc.mem_write(TMP, pre)
        em.uc.mem_write(TMP + 64, suf)
        ecs, lcs = em.cs_entrees, em.cs_sorties
        em.appeler(0x4B00, (TMP, len(pre), valeur, TMP + 64), arg5=len(suf))
        rax = em.verifier_enveloppe(1)
        attendu = pre + (b"" if sans_champ else ref_itoa(valeur)) + suf
        if bytes(em.sortie) != attendu:
            raise EchecOracle(f"tcp-11 : ligne {bytes(em.sortie)!r} != {attendu!r}")
        if em.cs_entrees != ecs + 1 or em.cs_sorties != lcs + 1:
            raise EchecOracle("tcp-11 : Enter/Leave non appariés (Q3)")
    return cas


def suite_conn(em: Emulateur, exe: bytes, phase: int) -> int:
    """tcp-09 — sessions scriptées ; le scénario final applique le moteur de
    patch RÉEL pendant une session ouverte (critère de sortie M2)."""
    em.installer_shims()
    em.regions_patchables = [(L.ECHO_ENTREE, L.ECHO_ENTREE + 8),
                             (L.ECHO_CROISSANCE, L.ECHO_CROISSANCE + 0x80)]
    cas = 0

    # S1 : échanges multiples puis fermeture du pair
    em.reinitialiser_donnees()
    em.poser_etat()
    em.file_recv += [b"abc", b"Hello, Triade!", 0]
    em.appeler(0x4800, (FAKE_SOCK,))
    em.verifier_enveloppe()
    if em.envois != [b"abc", b"Hello, Triade!"]:
        raise EchecOracle(f"tcp-09 S1 : échos {em.envois}")
    if bytes(em.sortie) != b"echo 3\r\necho 14\r\nfin connexion\r\n":
        raise EchecOracle(f"tcp-09 S1 : journal {bytes(em.sortie)!r}")
    if em.fermetures != [FAKE_SOCK]:
        raise EchecOracle("tcp-09 S1 : socket non fermée une fois (Q2)")
    cas += 1

    # S2 : émission partielle (3 puis 2) complétée sans perte ni doublement
    em.reinitialiser_donnees()
    em.poser_etat()
    em.file_recv.append(b"abcde")
    em.file_send += [3, 2]
    em.appeler(0x4800, (FAKE_SOCK,))
    em.verifier_enveloppe()
    if em.envois != [b"abcde", b"de"]:
        raise EchecOracle(f"tcp-09 S2 : envois partiels {em.envois}")
    if bytes(em.sortie) != b"echo 5\r\nfin connexion\r\n":
        raise EchecOracle("tcp-09 S2 : journal partial-send inattendu")
    cas += 1

    # S3 : erreur de réception -> fin propre
    em.reinitialiser_donnees()
    em.poser_etat()
    em.file_recv.append(-1)
    em.appeler(0x4800, (FAKE_SOCK,))
    em.verifier_enveloppe()
    if em.envois or bytes(em.sortie) != b"fin connexion\r\n":
        raise EchecOracle("tcp-09 S3 : erreur recv mal gérée (Q2/E1)")
    cas += 1

    # S4 : erreur d'émission en cours de boucle -> fin propre
    em.reinitialiser_donnees()
    em.poser_etat()
    em.file_recv.append(b"abc")
    em.file_send.append(-1)
    em.appeler(0x4800, (FAKE_SOCK,))
    em.verifier_enveloppe()
    if bytes(em.sortie) != b"echo 3\r\nfin connexion\r\n":
        raise EchecOracle("tcp-09 S4 : erreur send mal gérée (Q2/E1)")
    cas += 1

    # S5 : PATCH PENDANT LA SESSION (dev.2) — sans interruption de service
    if phase >= 2:
        em.reinitialiser_donnees()
        em.poser_etat()
        em.file_recv += [b"avant le patch\n", ("stop", b"apres le patch\n"), 0]
        em.appeler(0x4800, (FAKE_SOCK,))          # s'arrête au 2e recv
        if em.attente is None:
            raise EchecOracle("S5 : arrêt orchestré attendu au 2e recv")
        if em.envois != [b"avant le patch\n"]:
            raise EchecOracle("S5 : premier écho diverge")
        instantane = em.instantane()
        em.appeler(0x4400, (0,), pile=ALT_SOMMET)  # moteur RÉEL, pile secondaire
        em.restaurer(instantane)                   # contexte du thread restauré
        em.reprendre()                             # le pair est servi : v2 active
        em.verifier_enveloppe()
        if em.envois != [b"avant le patch\n", b"APRES LE PATCH\n"]:
            raise EchecOracle(f"S5 : continuité rompue — échos {em.envois}")
        if bytes(em.sortie) != b"echo 15\r\necho 15\r\nfin connexion\r\n":
            raise EchecOracle(f"S5 : journal {bytes(em.sortie)!r}")
        cas += 1

        # S6 : CYCLE COMPLET EN SESSION — identité, patch, majuscules,
        # rollback, retour identité — sur la MÊME connexion
        em.reinitialiser_donnees()
        em.poser_etat()
        em.file_recv += [b"un\n", ("stop", b"deux\n"), ("stop", b"trois\n"), 0]
        em.appeler(0x4800, (FAKE_SOCK,))          # s'arrête au 2e recv
        if em.envois != [b"un\n"]:
            raise EchecOracle(f"S6 : premier écho {em.envois}")
        instantane = em.instantane()
        em.appeler(0x4400, (0,), pile=ALT_SOMMET)  # PATCH pendant la session
        em.restaurer(instantane)
        em.reprendre()                             # "deux\n" -> majuscules
        if em.attente is None:
            raise EchecOracle("S6 : second arrêt orchestré attendu")
        instantane = em.instantane()
        em.appeler(0x4400, (1,), pile=ALT_SOMMET)  # ROLLBACK pendant la session
        em.restaurer(instantane)
        em.reprendre()                             # "trois\n" -> identité
        em.verifier_enveloppe()
        if em.envois != [b"un\n", b"DEUX\n", b"trois\n"]:
            raise EchecOracle(f"S6 : cycle patch/rollback en session {em.envois}")
        if bytes(em.sortie) != b"echo 3\r\necho 4\r\necho 5\r\nfin connexion\r\n":
            raise EchecOracle(f"S6 : journal {bytes(em.sortie)!r}")
        cas += 1
    else:
        # dev.1 : patch refusé en session (staging absent) -> service identité
        em.reinitialiser_donnees()
        em.poser_etat()
        em.file_recv += [("stop", b"x\n"), 0]
        em.appeler(0x4800, (FAKE_SOCK,))
        instantane = em.instantane()
        em.appeler(0x4400, (0,), pile=ALT_SOMMET)
        code = em.uc.reg_read(UC_X86_REG_RAX)
        em.restaurer(instantane)
        em.reprendre()
        em.verifier_enveloppe()
        if code != 2:
            raise EchecOracle(f"dev.1 : patch en session devait être refusé (2), code {code}")
        if em.envois != [b"x\n"]:
            raise EchecOracle("dev.1 : le refus devait préserver l'identité")
        cas += 1
    return cas


def suite_console(em: Emulateur, exe: bytes, phase: int) -> int:
    """tcp-10 — commandes, refus, approximations, quit, fin de flux."""
    em.installer_shims()
    cas = 0

    # C1 : séquence nominale
    em.reinitialiser_donnees()
    em.poser_etat(listen=0x3001)
    em.file_stdin += [b"patch\r\n", b"rollback\r\n", b"status\r\n", b"quit\r\n"]
    em.appeler(0x4980)
    em.verifier_enveloppe()
    if phase >= 2:
        attendu = (b"patch applique (majuscules)\r\n"
                   + b"retour arriere (identite)\r\n"
                   + b"commande inconnue\r\n")
        if bytes(em.sortie) != attendu:
            raise EchecOracle(f"C1 : journal {bytes(em.sortie)!r}")
        if em.lire_qword(L.R_ETAT_PATCH) != 0:
            raise EchecOracle("C1 : état final != v1 après rollback")
    else:
        attendu = b"commande refusee\r\n" * 2 + b"commande inconnue\r\n"
        if bytes(em.sortie) != attendu:
            raise EchecOracle(f"C1 dev.1 : journal {bytes(em.sortie)!r}")
    if em.lire_qword(L.R_QUIT) != 1:
        raise EchecOracle("C1 : drapeau quit non posé (Q1)")
    if em.fermetures != [0x3001]:
        raise EchecOracle("C1 : socket d'écoute non fermée au quit (Q1)")
    cas += 1

    # C2 : approximations — jamais confondues avec les commandes
    em.reinitialiser_donnees()
    em.poser_etat(listen=0x3001)
    em.file_stdin += [b"patchx\r\n", b"patc\r\n", b"rollbackX\r\n", b"qui\r\n"]
    em.appeler(0x4980)
    em.verifier_enveloppe()
    if bytes(em.sortie) != b"commande inconnue\r\n" * 4:
        raise EchecOracle(f"C2 : approximations {bytes(em.sortie)!r} (Q3)")
    if em.lire_qword(L.R_QUIT) != 0:
        raise EchecOracle("C2 : qui != quit ne doit pas arrêter (Q3)")
    cas += 1

    # C3 : double patch -> refus idempotent ; fin de flux -> retour propre
    em.reinitialiser_donnees()
    em.poser_etat(listen=0x3001)
    em.file_stdin += [b"patch\r\n", b"patch\r\n", False]
    em.appeler(0x4980)
    em.verifier_enveloppe()
    if phase >= 2:
        attendu = b"patch applique (majuscules)\r\ncommande refusee\r\n"
        if bytes(em.sortie) != attendu:
            raise EchecOracle(f"C3 : {bytes(em.sortie)!r}")
        if em.lire_qword(L.R_ETAT_PATCH) != 1:
            raise EchecOracle("C3 : le second patch ne doit rien casser (E2)")
    else:
        if bytes(em.sortie) != b"commande refusee\r\n" * 2:
            raise EchecOracle(f"C3 dev.1 : {bytes(em.sortie)!r}")
    cas += 1

    # C4 : rollback à vide -> refus
    em.reinitialiser_donnees()
    em.poser_etat(listen=0x3001)
    em.file_stdin += [b"rollback\r\n", False]
    em.appeler(0x4980)
    em.verifier_enveloppe()
    if not bytes(em.sortie).endswith(b"commande refusee\r\n"):
        raise EchecOracle("C4 : rollback à vide non refusé (E2)")
    cas += 1
    return cas


# --- Binaire entier (tcp-12) et porte R10 ----------------------------------------

def emuler_binaire(exe: bytes, phase: int, scenario: str = "nominal"):
    """tcp-12 — bannière, écoute, connexion, arrêt ; codes 0/1/2."""
    em = Emulateur(exe)
    em.installer_shims()
    if scenario == "nominal":
        em.file_accept += [0x777, "quit"]
        em.appeler(0x1800, limite=10_000_000)
        attendu = L.BANNIERE + b"connexion entrante\r\narret\r\n"
        if bytes(em.sortie) != attendu:
            raise EchecOracle(f"binaire : sortie {bytes(em.sortie)!r} != {attendu!r}")
        if em.code_sortie != 0:
            raise EchecOracle(f"binaire : code {em.code_sortie} != 0 (Q4)")
        # tcp-12 passe des adresses ABSOLUES (lea rip + bloc, position-indépendant
        # D33) : CreateThread reçoit VA réelles (image mappée à IMAGE), pas des RVA
        # — erratum oracle journal 18 (l'attente était écrite en RVA).
        if em.threads_crees != [(IMAGE + 0x4980, 0), (IMAGE + 0x4800, 0x777)]:
            raise EchecOracle(f"binaire : threads {em.threads_crees}")
        if len(em.handles_fermes) != 2:
            raise EchecOracle("binaire : handles de threads non fermés (Q2)")
        noms = [a[0] for a in em.appels_ws2]
        if noms != ["WSAStartup", "socket", "bind", "listen", "accept", "accept"]:
            raise EchecOracle(f"binaire : séquence ws2 {noms}")
    elif scenario == "erreur_wsa":
        em.retour_wsastartup = 1
        em.appeler(0x1800, limite=10_000_000)
        attendu = L.BANNIERE + b"erreur reseau, arret\r\n"
        if bytes(em.sortie) != attendu or em.code_sortie != 2:
            raise EchecOracle(f"binaire erreur_wsa : {bytes(em.sortie)!r} code {em.code_sortie}")
    elif scenario == "accept_sans_quit":
        em.file_accept += [0x777, -1]
        em.appeler(0x1800, limite=10_000_000)
        attendu = L.BANNIERE + b"connexion entrante\r\nerreur reseau, arret\r\n"
        if bytes(em.sortie) != attendu or em.code_sortie != 2:
            raise EchecOracle(f"binaire accept_sans_quit : {bytes(em.sortie)!r} code {em.code_sortie}")
    else:
        raise EchecOracle(f"scénario inconnu : {scenario}")
    return bytes(em.sortie), em.code_sortie


def porte_r10(exe: bytes, phase: int) -> int:
    """R10 — corruption d'un octet : arrêt code 1 AVANT tout appel réseau."""
    cibles = [L.ECHO_ENTREE, 0x4400, 0x4800, 0x4980, 0x4B00, 0x1800]
    if phase >= 2:
        cibles.append(L.R_STAGING)
    cas = 0
    for rva in cibles:
        mutant = bytearray(exe)
        mutant[_base_fichier(rva) + 11] ^= 0xFF
        em = Emulateur(bytes(mutant))
        em.installer_shims()
        crash = None
        try:
            em.appeler(0x1800, limite=10_000_000)
        except _uc.UcError as e:
            crash = e
        if rva == L.ENTREE and crash is not None:
            # Erratum V3 (journal 18) : la porte ne peut pas témoigner de sa
            # propre corruption — un défaut dans SON code peut la briser avant
            # son verdict. Le garant testable pour son propre slot : morte
            # AVANT tout effet (aucun réseau, aucun journal, aucun service).
            if em.appels_ws2 or bytes(em.sortie):
                raise EchecOracle(
                    f"R10 {rva:#x} : effet avant la mort ({bytes(em.sortie)!r})")
        else:
            if crash is not None:
                raise EchecOracle(f"R10 {rva:#x} : crash {crash}")
            if bytes(em.sortie) != b"TRIADE M2 : integrite KO, arret\r\n":
                raise EchecOracle(f"R10 {rva:#x} : sortie {bytes(em.sortie)!r}")
            if em.code_sortie != 1:
                raise EchecOracle(f"R10 {rva:#x} : code {em.code_sortie} != 1 (Q1)")
        if em.appels_ws2:
            raise EchecOracle(f"R10 {rva:#x} : appel réseau avant la porte (I2)")
        cas += 1
    # version antérieure au plancher -> refus (monotonie, anti-rollback)
    mutant = bytearray(exe)
    base = L.RDATA_FILE + (L.R_VERSION - L.RDATA_RVA)
    struct.pack_into("<Q", mutant, base, 0x00020000)
    em = Emulateur(bytes(mutant))
    em.installer_shims()
    em.appeler(0x1800, limite=10_000_000)
    if em.code_sortie != 1 or em.appels_ws2:
        raise EchecOracle("R10 : version < plancher non refusée (Q1)")
    return cas + 1


# --- Falsification : zéro silence -------------------------------------------------

def _detecteur_rapide(exe: bytes, bid: str, phase: int):
    """Déterministe : réussit sur l'artefact sain — toute déviation trahit la
    corruption (l'exception propage = corruption détectée)."""
    em = Emulateur(exe)
    em.installer_shims()
    if bid == "a10002":
        em.uc.mem_write(SRC, b"octets!")
        em.appeler(0x1040, (FAKE_STDOUT, SRC, 7))
        em.verifier_enveloppe(1)
        if bytes(em.sortie) != b"octets!":
            raise EchecOracle("write : octets divergents")
    elif bid == "a10003":
        em.appeler(0x1080, (0x25, 0, 0, 0), limite=1000)
        if em.code_sortie != 0x25:
            raise EchecOracle("exit : code non propagé")
    elif bid == "b20001":
        em.uc.mem_write(SRC, L.MOTIF33 if hasattr(L, "MOTIF33") else b"m" * 33)
        em.appeler(0x1100, (DST, SRC, 33))
        em.verifier_enveloppe(DST)
        if bytes(em.uc.mem_read(DST, 33)) != bytes(em.uc.mem_read(SRC, 33)):
            raise EchecOracle("memcpy : copie divergente")
    elif bid == "b20002":
        em.uc.mem_write(SRC, b"TRIADE\x00")
        em.uc.mem_write(DST, b"TRIADE\x00")
        em.appeler(0x1180, (SRC, DST, 6))
        em.verifier_enveloppe(0)
    elif bid == "b20003":
        em.uc.mem_write(SRC, b"TRIADE\x00")
        em.appeler(0x1200, (SRC, 0, 0, 0))
        em.verifier_enveloppe(6)
    elif bid == "b20004":
        em.appeler(0x1280, (1234567890, TMP))
        em.verifier_enveloppe(TMP)
        if bytes(em.uc.mem_read(TMP, 11)) != b"1234567890\x00":
            raise EchecOracle("itoa : décimale divergente")
    elif bid == "c30001":
        em.appeler(0x4000)
        em.verifier_enveloppe(FAKE_SOCK)
        if [a[0] for a in em.appels_ws2] != ["WSAStartup", "socket", "bind", "listen"]:
            raise EchecOracle("init : séquence divergente")
    elif bid == "c30002":
        em.file_accept.append(0x777)
        em.appeler(0x4100, (FAKE_SOCK,))
        em.verifier_enveloppe(0x777)
    elif bid == "c30003":
        em.file_recv.append(b"abc")
        em.appeler(0x4140, (FAKE_SOCK, DST, 8))
        em.verifier_enveloppe(3)
    elif bid == "c30004":
        em.uc.mem_write(DST, b"xyz")
        em.appeler(0x4180, (FAKE_SOCK, DST, 3))
        em.verifier_enveloppe(3)
    elif bid == "c30005":
        em.appeler(0x41C0, (FAKE_SOCK,))
        em.verifier_enveloppe(0)
        if em.fermetures != [FAKE_SOCK]:
            raise EchecOracle("close : fermeture absente")
    elif bid == "c30006":
        em.appeler(0x4300, (0x4800, 7))
        em.verifier_enveloppe(0x108)
        if em.threads_crees != [(0x4800, 7)]:
            raise EchecOracle("spawn : arguments divergents")
    elif bid == "c30007":
        if phase < 2:
            em.appeler(0x4400, (0,))
            em.verifier_enveloppe(2)
        else:
            em.regions_patchables = [(L.ECHO_ENTREE, L.ECHO_ENTREE + 8),
                                     (L.ECHO_CROISSANCE, L.ECHO_CROISSANCE + 0x80)]
            em.appeler(0x4400, (0,))
            em.verifier_enveloppe(0)
            if em.lire_qword(L.R_ETAT_PATCH) != 1:
                raise EchecOracle("patch : état divergent")
    elif bid == "c30008":
        em.uc.mem_write(SRC, b"Triade!")
        em.appeler(L.ECHO_ENTREE, (DST, SRC, 7))
        em.verifier_enveloppe(7)
        if bytes(em.uc.mem_read(DST, 7)) != b"Triade!":
            raise EchecOracle("echo v1 : identité rompue")
    elif bid == "c30009":
        em.poser_etat()
        em.file_recv += [b"ab", 0]
        em.appeler(0x4800, (FAKE_SOCK,))
        em.verifier_enveloppe()
        if em.envois != [b"ab"]:
            raise EchecOracle("conn : écho divergent")
    elif bid == "c30010":
        em.poser_etat(listen=0x3001)
        em.file_stdin.append(b"quit\r\n")
        em.appeler(0x4980)
        em.verifier_enveloppe()
        if em.lire_qword(L.R_QUIT) != 1:
            raise EchecOracle("console : quit non traité")
    elif bid == "c30011":
        em.poser_etat()
        em.uc.mem_write(TMP, b"echo ")
        em.uc.mem_write(TMP + 64, b"\r\n")
        em.appeler(0x4B00, (TMP, 5, 42, TMP + 64), arg5=2)
        em.verifier_enveloppe(1)
        if bytes(em.sortie) != b"echo 42\r\n":
            raise EchecOracle("journal : ligne divergente")
    elif bid == "c30013":
        em.file_accept += [0x777, "quit"]
        em.appeler(0x1800, limite=10_000_000)
        if em.code_sortie != 0 or bytes(em.sortie) != L.BANNIERE + b"connexion entrante\r\narret\r\n":
            raise EchecOracle("main : chemin nominal divergent")
    else:
        raise EchecOracle(f"détecteur manquant pour {bid}")


def falsifier(exe: bytes, phase: int) -> str:
    cibles = {"a10002": 0x1040, "a10003": 0x1080, "b20001": 0x1100, "b20002": 0x1180,
              "b20003": 0x1200, "b20004": 0x1280, "c30001": 0x4000, "c30002": 0x4100,
              "c30003": 0x4140, "c30004": 0x4180, "c30005": 0x41C0, "c30006": 0x4300,
              "c30007": 0x4400, "c30008": 0x4600, "c30009": 0x4800, "c30010": 0x4980,
              "c30011": 0x4B00, "c30013": 0x1800}
    detectees = 0
    for bid, rva in cibles.items():
        vu = False
        for offset in (0, 5, 10):
            mutant = bytearray(exe)
            mutant[_base_fichier(rva) + offset] ^= 0xFF
            try:
                _detecteur_rapide(bytes(mutant), bid, phase)
                vu = False
            except (EchecOracle, _uc.UcError):
                vu = True
                break
        if not vu:
            raise EchecOracle(f"falsification : corruption de {bid} non détectée — oracle vide")
        detectees += 1
    return f"{detectees}/{len(cibles)} corruptions détectées"


# --- Point d'entrée -----------------------------------------------------------------

VOLUMES = {
    "complet": {"echo_v1": 12000, "echo_v2": 12000, "libc09": 12000,
                "net": 1500, "spawn": 1500, "journal": 4000},
    "reduit": {"echo_v1": 300, "echo_v2": 300, "libc09": 300,
               "net": 120, "spawn": 100, "journal": 250},
}


def executer(exe: bytes, graine: int = 1, volume: str = "complet") -> dict:
    if volume not in VOLUMES:
        raise EchecOracle(f"volume inconnu : {volume}")
    phase = 2 if exe[L.RDATA_FILE + (L.R_STAGING - L.RDATA_RVA)] != 0xCC else 1
    vol = VOLUMES[volume]
    verdicts, total = {}, 0

    em = Emulateur(exe)
    em.installer_shims()
    em.appeler(L.ECHO_ENTREE, (DST, SRC, 1))        # échauffement / mapping

    em = Emulateur(exe)
    suite_echo_v1(em, _alea(graine, "c30008"), vol["echo_v1"])
    total += vol["echo_v1"]
    verdicts["c30008"] = {"cas": vol["echo_v1"], "detail": f"identité ok({vol['echo_v1']})"}

    if phase >= 2:
        em = Emulateur(exe)
        suite_echo_v2(em, _alea(graine, "c30014"), vol["echo_v2"], exe)
        total += vol["echo_v2"]
        verdicts["c30014"] = {"cas": vol["echo_v2"],
                              "detail": f"majuscules ok({vol['echo_v2']}), staging = notation"}
    else:
        verdicts["c30014"] = {"cas": 0, "detail": "staging absent (dev.1)"}

    n = suite_libc09(_alea(graine, "c30012"), vol["libc09"])
    total += n
    verdicts["c30012"] = {"cas": n, "detail": f"modèle curseur + verrous ok({n})"}

    em = Emulateur(exe)
    n = suite_net(em, _alea(graine, "net"), vol["net"])
    total += n
    verdicts["net"] = {"cas": n, "detail": f"tcp-01..05 ok({n} contrôles)"}

    em = Emulateur(exe)
    n = suite_spawn(em, _alea(graine, "c30006"), vol["spawn"])
    total += n
    verdicts["c30006"] = {"cas": n, "detail": f"spawn ok({n})"}

    em = Emulateur(exe)
    n = suite_journal(em, _alea(graine, "c30011"), vol["journal"])
    total += n
    verdicts["c30011"] = {"cas": n, "detail": f"lignes exactes ok({n})"}

    em = Emulateur(exe)
    n = suite_patch(em, exe, phase)
    total += n
    verdicts["c30007"] = {"cas": n, "detail": (
        f"bascule+effet+rollback+refus ok({n} scénarios)" if phase >= 2
        else f"mécanique+refus ok({n} scénarios, staging absent)")}

    em = Emulateur(exe)
    n = suite_conn(em, exe, phase)
    total += n
    verdicts["c30009"] = {"cas": n, "detail": (
        "sessions + PATCH EN SESSION ok (continuité)" if phase >= 2
        else f"sessions ok({n}), patch refusé (dev.1)")}

    em = Emulateur(exe)
    n = suite_console(em, exe, phase)
    total += n
    verdicts["c30010"] = {"cas": n, "detail": f"commandes+refus+quit ok({n})"}

    for scenario in ("nominal", "erreur_wsa", "accept_sans_quit"):
        emuler_binaire(exe, phase, scenario)
        total += 1
    verdicts["c30013"] = {"cas": 3, "detail": "binaire : nominal/erreur_wsa/accept_sans_quit, codes 0/2/2"}

    n = porte_r10(exe, phase)
    total += n
    verdicts["r10"] = {"cas": n, "detail": "corruptions -> KO code 1 avant réseau"}

    falsification = falsifier(exe, phase)

    empreinte = hashlib.sha256(
        json_stable(verdicts).encode("ascii")
        + f"|graine={graine}|volume={volume}|phase={phase}".encode("ascii")).hexdigest()
    return {
        "total_cas": total,
        "blocs": verdicts,
        "binaire": f"sortie exacte, code 0 (phase {phase})",
        "patch": ("bascule atomique + rollback EFFECTIFS en émulation (sessions continues)"
                  if phase >= 2 else "mécanique vérifiée, remplaçant en attente (dev.1)"),
        "falsification": falsification,
        "empreinte": "sha256:" + empreinte,
        "graine": graine,
        "volume": volume,
        "phase": phase,
    }


def json_stable(d: dict) -> str:
    import json
    return json.dumps(d, sort_keys=True, ensure_ascii=True)


if __name__ == "__main__":
    graine = 1
    volume = "reduit"
    args = sys.argv[1:]
    if "--graine" in args:
        graine = int(args[args.index("--graine") + 1])
    if "--volume" in args:
        volume = args[args.index("--volume") + 1]
    chemin = os.path.join(ICI, "echo.exe")
    if "--exe" in args:
        chemin = args[args.index("--exe") + 1]
    with open(chemin, "rb") as f:
        artefact = f.read()
    v = executer(artefact, graine=graine, volume=volume)
    print(f"[oracle] {v['total_cas']} cas verts (volume {v['volume']}, graine {v['graine']}, phase {v['phase']})")
    print(f"[oracle] patch : {v['patch']}")
    print(f"[oracle] falsification : {v['falsification']}")
    print(f"[oracle] empreinte des verdicts : {v['empreinte']}")
