#!/usr/bin/env python3
"""oracle_corpus.py — L'ORACLE m1 RÉGÉNÉRÉ pour l'instance Linux du corpus (M6-(b)).

Implémentation de référence DÉRIVÉE DE LA COUCHE I (unix/I/*.md — les
révisions R+1 de granularité, D149-(3)) — jamais de la notation — exécutée
NATIVEMENT au labo (le bac à sable EST Linux x86-64 : la fiche § 10 du
profil — l'oracle du jalon s'exécute nativement, D149) :

  1. tests par bloc : chaque bloc du corpus reçoit des entrées aléatoires
     contraintes par les pré-conditions de son contrat, la sortie (valeur de
     retour, mémoire, curseur d'arène, non volatils SysV, rsp) est comparée
     à la référence — les VOLUMES des vecteurs V2 des contrats (12 000 cas
     par bloc critique, 4 000 lignes de journal, 3 000 séquences de zone) ;
  2. scénarios : l'auto-test complet (libc-08 — la ligne exacte du
     patrimoine, N rendu), le journal sous verrou réel (concurrence : deux
     threads NATAFS, jamais un entrelacement), le moteur de patch en
     scénario complet (apply -> croissance = staging, entrée = E9+NOPs,
     comportement du remplaçant ; rollback -> comportement v1 ; refus
     nommés 1-5, dont le refus RÉEL du service de protection — le refus
     est obtenu par une cartographie PARTAGÉE en lecture seule du code :
     mprotect exige un descripteur inscriptible, EACCES est le noyau qui
     parle, pas un shim) ;
  3. falsification : la corruption d'un octet de code d'un bloc quelconque
     de l'artefact fait dévier la sortie ou le code de sortie, ou tue le
     processus (zéro silence — non-vacuité, mesurée en sous-processus : un
     octet corrompu peut tuer, l'oracle natif ne meurt jamais avec lui).

L'oracle est régénéré/exécuté à chaque session (D1) : seuls ses verdicts
hachés survivent dans frag-prf. Les graines différencient les exécutions.

L'INSTRUMENT : la cartouche d'appel — deux pages adjacentes (code RX,
données RW — le réflexe W^X jusque dans l'instrument : l'ARTEFACT reste
W^X par phdr, l'outil d'atelier se l'impose aussi). La cartouche charge
les six arguments SysV, pose des canaris distincts dans les six non
volatils, saute au bloc sur une pile fraîche alignée (adresse de retour
posée à [rsp], entrée ≡ 8 mod 16 — la convention), et capture au retour
rax, les drapeaux, les non volatils et rsp. Le verrou du journal est le
VRAI verrou tournant du plan ; la concurrence est la VRAIE concurrence
(ctypes relâche le GIL pendant l'appel natif).

Usage : depuis build_corpus.py — executer(chemin_artefact, graine, volume)
"""

from __future__ import annotations

import ctypes
import hashlib
import mmap
import os
import random
import struct
import subprocess
import sys
import threading

ICI = os.path.dirname(os.path.abspath(__file__))
UNIX = ICI
sys.path.insert(0, UNIX)
sys.path.insert(0, os.path.join(UNIX, "outils"))
import layout as L  # noqa: E402

import capstone  # noqa: E402
from keystone import KS_ARCH_X86, KS_MODE_64, Ks  # noqa: E402


class EchecOracle(Exception):
    """Tout échec nommé de l'oracle (fail-closed : jamais un faux vert)."""


# ---------------------------------------------------------------------------
# La cartouche d'appel natif (leContrôleur de registres de l'oracle)
# ---------------------------------------------------------------------------

CARTOUCHE = """\
push rbx
push rbp
push r12
push r13
push r14
push r15
mov rax, rsp
mov r10, [rdi + 0x38]
mov [r10 - 0x200], rax
mov rbx, @CAN1
mov rbp, @CAN2
mov r12, @CAN3
mov r13, @CAN4
mov r14, @CAN5
mov r15, @CAN6
mov rdx, [rdi + 0x18]
mov rcx, [rdi + 0x20]
mov r8, [rdi + 0x28]
mov r9, [rdi + 0x30]
mov rsi, [rdi + 0x10]
mov rax, [rdi + 0x00]
mov r11, .retour
mov [r10 - 8], r11
lea r10, [r10 - 8]
mov rdi, [rdi + 0x08]
mov rsp, r10
jmp rax
.retour:
mov [rsp - 0x1F8], rax
pushfq
pop rax
mov [rsp - 0x1F0], rax
mov [rsp - 0x1E8], rbx
mov [rsp - 0x1E0], rbp
mov [rsp - 0x1D8], r12
mov [rsp - 0x1D0], r13
mov [rsp - 0x1C8], r14
mov [rsp - 0x1C0], r15
mov [rsp - 0x1B8], rsp
mov rsp, [rsp - 0x200]
pop r15
pop r14
pop r13
pop r12
pop rbp
pop rbx
ret
"""

CANARIS = [0x4E6F6E566F6C31, 0x4E6F6E566F6C32, 0x4E6F6E566F6C33,
           0x4E6F6E566F6C34, 0x4E6F6E566F6C35, 0x4E6F6E566F6C36]  # "NonVol1..6"

# La fenêtre PAR APPEL (ré-entrance de l'instrument — la leçon de la concurrence) :
# la cartouche n'a PLUS d'état fixe ; chaque appel reçoit son sommet de pile
# (attribué sous verrou, restitué au retour) et porte sa sauvegarde de pile
# thread + ses sorties dans SA fenêtre [sommet-0x200, sommet-0x1B8] — sous la
# profondeur d'imbrication maximale (corpus-13 -> autotest/journal -> feuilles :
# jamais au-dessous de -0x220) : les cadres imbriqués n'y touchent jamais.
FENETRE = 0x200        # [sommet-0x200] : sauve_rsp ; -0x1F8..-0x1B8 : les 9 sorties
PAS_PILE = 0x800       # le pas d'attribution : deux appels CONCURRENTS disjointes


class Cartouche:
    """L'appelant natif : registres contrôlés, sorties capturées."""

    def __init__(self):
        import auteur
        # Deux pages adjacentes : code (RX) puis données (RW)
        self._zone = mmap.mmap(-1, 0x2000, prot=mmap.PROT_READ | mmap.PROT_WRITE)
        import ctypes.util  # noqa: F401
        libc = ctypes.CDLL("libc.so.6", use_errno=True)
        libc.mmap.restype = ctypes.c_void_p
        adr = libc.mmap(ctypes.c_void_p(0), ctypes.c_size_t(0x2000),
                        ctypes.c_int(mmap.PROT_READ | mmap.PROT_WRITE),
                        ctypes.c_int(mmap.MAP_PRIVATE | mmap.MAP_ANONYMOUS),
                        ctypes.c_int(-1), ctypes.c_size_t(0))
        if not adr or adr == ctypes.c_void_p(-1).value:
            raise EchecOracle("cartouche : mmap impossible")
        self.base = adr
        self.code = self.base
        self.donnees = self.base + 0x1000

        symboles = {
            "CAN1": CANARIS[0], "CAN2": CANARIS[1], "CAN3": CANARIS[2],
            "CAN4": CANARIS[3], "CAN5": CANARIS[4], "CAN6": CANARIS[5],
        }
        lignes = []
        for l in CARTOUCHE.splitlines():
            l = l.strip()
            if not l:
                continue
            if l.startswith(".") and l.endswith(":"):
                lignes.append(("label", l[1:-1]))
            else:
                lignes.append(("instr", l))
        ks = Ks(KS_ARCH_X86, KS_MODE_64)
        resolues, _ = auteur.resoudre(ks, self.code, symboles, lignes)
        octets = b"".join(r["octets"] for r in resolues)
        # ÉCRIRE le code AVANT le mprotect (la page est encore RW) —
        # l'oublier laisse la page vide de zéros et le jmp y meurt
        ctypes.memmove(self.code, octets, len(octets))
        # round-trip de l'instrument lui-même (le réflexe R5 jusque là)
        cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
        for r in resolues:
            insns = list(cs.disasm(r["octets"], r["adresse"]))
            if len(insns) != 1:
                raise EchecOracle(f"cartouche : pas une instruction @ {r['adresse']:#x}")
            enc, _ = ks.asm(f"{insns[0].mnemonic} {insns[0].op_str}", r["adresse"])
            if bytes(enc) != r["octets"]:
                raise EchecOracle(f"cartouche : round-trip échoué @ {r['adresse']:#x}")
        libc.mprotect(ctypes.c_void_p(self.code), ctypes.c_size_t(0x1000),
                      ctypes.c_int(mmap.PROT_READ | mmap.PROT_EXEC))
        # (la page données reste RW — les sorties y vivent)

        self._libc = libc
        self._ks = ks
        self.fn = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.c_void_p)(self.code)
        # la pile du bloc appelé : une région fraîche, sommet 16-aligné ;
        # le sommet est PAR THREAD (la leçon du run M6-(c) : un allocateur
        # par décrément-restitution n'est PAS un allocateur sous concurrence
        # — l'ordre de restitution interfolé rompt la LIFO, deux appels
        # vivants se partagent la fenêtre et la pile ; D151 complétée : la
        # fenêtre était par appel, le SOMMET est par fil — attribué une
        # fois, réutilisé en séquence dans SON fil, jamais recouvert)
        self.pile = libc.mmap(ctypes.c_void_p(0), ctypes.c_size_t(0x10000),
                              ctypes.c_int(mmap.PROT_READ | mmap.PROT_WRITE),
                              ctypes.c_int(mmap.MAP_PRIVATE | mmap.MAP_ANONYMOUS),
                              ctypes.c_int(-1), ctypes.c_size_t(0))
        self.pile_sommet = (self.pile + 0x10000 - 0x200) & ~0xF
        self._suivant = self.pile_sommet
        self._sommets_fils = {}         # ident de fil -> sommet dédié
        self._verrou_sommets = threading.Lock()

    def _sommet_du_fils(self) -> int:
        """Le sommet dédié du fil courant (attribué une fois, sous verrou)."""
        ident = threading.get_ident()
        with self._verrou_sommets:
            if ident not in self._sommets_fils:
                self._sommets_fils[ident] = self._suivant
                self._suivant -= PAS_PILE
            return self._sommets_fils[ident]

    def appeler(self, cible: int, args: list[int]) -> dict:
        """Appelle le bloc à l'adresse absolue cible avec args (≤ 6, SysV).

        Ré-entrant : entrées LOCALES à l'appel, sommet PAR FIL (attribué une
        fois sous un verrou court, réutilisé en séquence dans son fil —
        jamais recouvert par un autre fil), sorties dans la FENÊTRE de CET
        appel. Retourne rax, les drapeaux, les six non volatils (canaris
        attendus), rsp au retour et le sommet donné (l'attendu : rsp ==
        sommet — la pile équilibrée).
        """
        e = (ctypes.c_uint64 * 16)()
        e[0] = cible
        for i in range(6):
            e[1 + i] = args[i] if i < len(args) else 0
        sommet = self._sommet_du_fils()
        e[7] = sommet
        self.fn(ctypes.addressof(e))
        q = (ctypes.c_uint64 * 10).from_address(sommet - FENETRE)
        return {
            "rax": q[1], "drapeaux": q[2], "rbx": q[3], "rbp": q[4],
            "r12": q[5], "r13": q[6], "r14": q[7], "r15": q[8],
            "rsp": q[9], "sommet": sommet,
        }
        # (le sommet vit à son fil : rien à restituer — la restitution
        #  interfolée de l'allocateur par décrément était la faille)

    def non_volatils_intacts(self, s: dict) -> bool:
        return (s["rbx"] == CANARIS[0] and s["rbp"] == CANARIS[1]
                and s["r12"] == CANARIS[2] and s["r13"] == CANARIS[3]
                and s["r14"] == CANARIS[4] and s["r15"] == CANARIS[5])


# ---------------------------------------------------------------------------
# L'image du corpus en mémoire (le plan d'adressage, la vraie protection)
# ---------------------------------------------------------------------------

class Image:
    """L'artefact mappé selon ses phdr : R / RX / RW — la vraie protection.

    mode "prive"    : segments anonymes privés — mprotect peut ouvrir la
                      page code en écriture (les scénarios du patch) ;
    mode "partage"  : segments R et RX mappés PARTAGÉS depuis le fichier
                      OUVERT EN LECTURE SEULE — mprotect exige un
                      descripteur inscriptible : le refus EACCES est le
                      NOYAU qui refuse (le scénario code 5 de tcp-07, sans
                      aucun shim).
    """

    def __init__(self, chemin: str, mode: str = "prive"):
        with open(chemin, "rb") as f:
            self.artefact = f.read()
        if len(self.artefact) != L.CORPUS_TAILLE_FICHIER:
            raise EchecOracle(f"artefact {len(self.artefact)} o != plan {L.CORPUS_TAILLE_FICHIER:#x}")
        libc = ctypes.CDLL("libc.so.6", use_errno=True)
        libc.mmap.restype = ctypes.c_void_p
        self.total = 0x4000
        adr = libc.mmap(ctypes.c_void_p(0), ctypes.c_size_t(self.total),
                        ctypes.c_int(0),  # PROT_NONE
                        ctypes.c_int(mmap.MAP_PRIVATE | mmap.MAP_ANONYMOUS),
                        ctypes.c_int(-1), ctypes.c_size_t(0))
        if not adr or adr == ctypes.c_void_p(-1).value:
            raise EchecOracle("image : mmap réservée impossible")
        self.base = adr
        # un pseudo-fichier pour le mode partagé (lecture seule)
        fd = os.open(chemin, os.O_RDONLY)
        try:
            MAP_FIXED = 0x10
            MAP_SHARED = 0x01
            prot_r = mmap.PROT_READ
            prot_rx = mmap.PROT_READ | mmap.PROT_EXEC
            # MAP_FIXED OBLIGATOIRE : la région est réservée PROT_NONE, les
            # segments la COMBLENT à leurs RVA — sans MAP_FIXED le noyau
            # placerait les segments ailleurs et base+RVA resterait PROT_NONE
            # (le saut y mourrait — le diagnostic du premier build)
            drapeaux = (MAP_SHARED if mode == "partage" else mmap.MAP_PRIVATE) | MAP_FIXED
            # segment 1 R  (fichier 0x0..0x1000)
            r = libc.mmap(ctypes.c_void_p(self.base), ctypes.c_size_t(0x1000),
                          ctypes.c_int(prot_r), ctypes.c_int(drapeaux),
                          ctypes.c_int(fd), ctypes.c_size_t(0))
            # segment 2 RX (fichier 0x1000..0x3000)
            r2 = libc.mmap(ctypes.c_void_p(self.base + 0x1000), ctypes.c_size_t(0x2000),
                           ctypes.c_int(prot_rx), ctypes.c_int(drapeaux),
                           ctypes.c_int(fd), ctypes.c_size_t(0x1000))
            # segment 3 RW (.bss pur — anonyme, né nul)
            r3 = libc.mmap(ctypes.c_void_p(self.base + 0x3000), ctypes.c_size_t(0x1000),
                           ctypes.c_int(mmap.PROT_READ | mmap.PROT_WRITE),
                           ctypes.c_int(mmap.MAP_PRIVATE | MAP_FIXED | mmap.MAP_ANONYMOUS),
                           ctypes.c_int(-1), ctypes.c_size_t(0))
            if not r or not r2 or not r3:
                raise EchecOracle("image : segments non mappés")
        finally:
            os.close(fd)
        self._libc = libc
        self.mode = mode

    def adr(self, rva: int) -> int:
        return self.base + rva

    def octets(self, rva: int, n: int) -> bytes:
        return bytes((ctypes.c_ubyte * n).from_address(self.adr(rva)))

    def poser(self, rva: int, data: bytes) -> None:
        ouverts = self._ouvrir_ecriture(rva, len(data))
        try:
            ctypes.memmove(self.adr(rva), data, len(data))
        finally:
            self._restaurer_protection(ouverts)

    # -- l'instrument de mutation NOMME son geste (jamais un poser nu) --------
    # Un poser sur une page R sans ouverture est un SEGFAULT muet — la pire
    # espèce de refus. L'ouverture est réservée au mode privé : en partage, le
    # refus du service de protection est le scénario du BLOC (code 5, le noyau
    # parle), jamais un geste muet de l'instrument.

    def _prot_page(self, page: int) -> int:
        """La protection courante d'une page, lue dans /proc/self/maps."""
        with open("/proc/self/maps", "r", encoding="ascii") as f:
            for ligne in f:
                a, tiret, reste = ligne.partition("-")
                if not tiret:
                    continue
                try:
                    debut = int(a, 16)
                    fin = int(reste.split(" ", 1)[0], 16)
                except ValueError:
                    continue
                if debut <= page < fin:
                    champ = ligne.split()[1]
                    p = mmap.PROT_READ if "r" in champ else 0
                    if "w" in champ:
                        p |= mmap.PROT_WRITE
                    if "x" in champ:
                        p |= mmap.PROT_EXEC
                    return p
        raise EchecOracle(f"image : page {page:#x} absente de /proc/self/maps")

    def _ouvrir_ecriture(self, rva: int, n: int) -> list:
        """Ouvre en RW les pages couvertes par [rva, rva+n) ; retourne
        [(page, prot_avant)] à restaurer après le geste."""
        if n <= 0:
            return []
        restaure = []
        page = self.base + (rva & ~0xFFF)
        derniere = self.base + ((rva + n - 1) & ~0xFFF)
        while page <= derniere:
            prot = self._prot_page(page)
            if not (prot & mmap.PROT_WRITE):
                if self.mode != "prive":
                    raise EchecOracle(
                        f"poser {rva:#x} : page {page:#x} non inscriptible en mode "
                        f"{self.mode} — l'instrument ne contourne jamais le "
                        f"service de protection (le refus nommé est le scénario "
                        f"du bloc)")
                err = self._libc.mprotect(ctypes.c_void_p(page),
                                          ctypes.c_size_t(0x1000),
                                          ctypes.c_int(prot | mmap.PROT_WRITE))
                if err != 0:
                    raise EchecOracle(
                        f"poser : mprotect RW {page:#x} refusé "
                        f"(errno {ctypes.get_errno()})")
                restaure.append((page, prot))
            page += 0x1000
        return restaure

    def _restaurer_protection(self, restaure: list) -> None:
        for page, prot in restaure:
            err = self._libc.mprotect(ctypes.c_void_p(page),
                                      ctypes.c_size_t(0x1000), ctypes.c_int(prot))
            if err != 0:
                raise EchecOracle(
                    f"poser : restauration {page:#x} refusée "
                    f"(errno {ctypes.get_errno()})")

    def qword(self, rva: int) -> int:
        return struct.unpack("<Q", self.octets(rva, 8))[0]

    def poser_qword(self, rva: int, v: int) -> None:
        self.poser(rva, struct.pack("<Q", v))


# ---------------------------------------------------------------------------
# Les références — DÉRIVÉES DE LA COUCHE I (unix/I/*.md), jamais de la notation
# ---------------------------------------------------------------------------

def ref_memcpy(dst: bytearray, src: bytes, n: int) -> None:
    dst[:n] = src[:n]                       # libc-01:R2 Q1-I4


def ref_memcmp(a: bytes, b: bytes, n: int) -> int:
    for i in range(n):                      # libc-02:R2 Q1-Q4
        if a[i] < b[i]:
            return -1
        if a[i] > b[i]:
            return 1
    return 0


def ref_strlen(s: bytes) -> int:
    return s.index(0)                       # libc-03:R2 Q1 (P2 : au moins un nul)


def ref_itoa(v: int) -> bytes:
    return str(v).encode() + b"\0"          # libc-04:R3 Q1/Q2/I4


def ref_memset(n: int, val: int) -> bytes:
    return bytes([val]) * n                 # libc-07:R2 Q1


class RefZone:                              # libc-05:R2 / libc-06:R2
    """Le modèle de l'arène : curseur, alignement, épuisement."""

    def __init__(self, base: int, taille: int):
        self.base, self.taille = base, taille
        self.curseur = 0

    def allouer(self, taille: int, align: int):
        if taille > self.taille or align == 0 or (align & (align - 1)) or align > 64:
            return 0
        borne = (self.curseur + align - 1) & ~(align - 1)
        if borne + taille > self.taille:
            return 0
        self.curseur = borne + taille
        return self.base + borne

    def reinitialiser(self):
        self.curseur = 0


# ---------------------------------------------------------------------------
# La capture du flux de sortie (fd 1) — la ligne de l'artefact, jamais muette
# ---------------------------------------------------------------------------

class Capture:
    """Détourne fd 1 vers un tube le temps d'un appel — lecture synchrone."""

    def __init__(self):
        self.lecture, self.ecriture = os.pipe()
        os.set_blocking(self.lecture, False)
        self.sauve = None

    def __enter__(self):
        self.sauve = os.dup(1)
        os.dup2(self.ecriture, 1)
        return self

    def lire(self) -> bytes:
        morceaux = []
        while True:
            try:
                m = os.read(self.lecture, 65536)
            except BlockingIOError:
                break
            if not m:
                break
            morceaux.append(m)
        return b"".join(morceaux)

    def __exit__(self, *a):
        os.dup2(self.sauve, 1)
        os.close(self.sauve)


# ---------------------------------------------------------------------------
# L'oracle différentiel par bloc (les vecteurs V2 des contrats)
# ---------------------------------------------------------------------------

def tester_blocs_purs(img: Image, cart: Cartouche, graine: int, volume: str) -> dict:
    """libc-01..07 — les 12 000 cas par bloc (V2), contraints par les P."""
    rng = random.Random(graine * 1000 + 1)
    n_blocs = {"complet": 12000, "reduit": 1200}.get(volume, 1200)
    verrous = []

    def buf(taille: int) -> int:
        adr = cart._libc.mmap(ctypes.c_void_p(0), ctypes.c_size_t(max(taille, 0x1000)),
                              ctypes.c_int(mmap.PROT_READ | mmap.PROT_WRITE),
                              ctypes.c_int(mmap.MAP_PRIVATE | mmap.MAP_ANONYMOUS),
                              ctypes.c_int(-1), ctypes.c_size_t(0))
        return adr

    # --- libc-01 memcpy : dst/src/n, n ∈ [0, 1024] ---
    total = 0
    for _ in range(n_blocs):
        n = rng.randrange(0, 1025)
        src = bytes(rng.randrange(256) for _ in range(1024))
        d, s = buf(1024), buf(1024)
        ctypes.memmove(s, src, 1024)
        attendu = bytearray(1024)
        ref_memcpy(attendu, src, n)
        r = cart.appeler(img.adr(L.A_MEMCPY), [d, s, n])
        total += 1
        if bytes((ctypes.c_ubyte * 1024).from_address(d)) != bytes(attendu):
            raise EchecOracle(f"libc-01 : dst diverge (n={n})")
        if bytes((ctypes.c_ubyte * 1024).from_address(s)) != src:
            raise EchecOracle(f"libc-01 : src muté (n={n})")
        if r["rax"] != d:
            raise EchecOracle(f"libc-01 : rax != dst (n={n})")
        if not cart.non_volatils_intacts(r) or r["rsp"] != r["sommet"]:
            raise EchecOracle(f"libc-01 : non volatils ou pile (n={n})")
    verrous.append(f"libc-01: {total} cas")

    # --- libc-02 memcmp : relations contrôlées, n ∈ [0, 256] ---
    total = 0
    for _ in range(n_blocs):
        n = rng.randrange(0, 257)
        mode = rng.randrange(4)
        a = bytearray(rng.randrange(256) for _ in range(256))
        b = bytearray(a)
        if mode == 1 and n > 0:
            b[rng.randrange(n)] ^= 1
        elif mode == 2 and n > 0:
            i = rng.randrange(n)
            a[i], b[i] = 0x00, 0xFF
        elif mode == 3 and n > 0:
            i = rng.randrange(n)
            b[i:] = bytes(rng.randrange(256) for _ in range(n - i))
        ba, bb = buf(256), buf(256)
        ctypes.memmove(ba, bytes(a), 256)
        ctypes.memmove(bb, bytes(b), 256)
        r = cart.appeler(img.adr(L.A_MEMCMP), [ba, bb, n])
        attendu = ref_memcmp(bytes(a), bytes(b), n)
        total += 1
        if r["rax"] & 0xFFFFFFFF != attendu & 0xFFFFFFFF:
            raise EchecOracle(f"libc-02 : verdict {r['rax']} != {attendu} (n={n})")
        if not cart.non_volatils_intacts(r) or r["rsp"] != r["sommet"]:
            raise EchecOracle("libc-02 : non volatils ou pile")
    verrous.append(f"libc-02: {total} cas")

    # --- libc-03 strlen : chaînes aléatoires sans nul interne ---
    total = 0
    for _ in range(n_blocs):
        lon = rng.randrange(0, 201)
        ch = bytes(rng.randrange(1, 256) for _ in range(lon)) + b"\0" + b"\0" * 8
        c = buf(512)
        ctypes.memmove(c, ch, len(ch))
        r = cart.appeler(img.adr(L.A_STRLEN), [c])
        total += 1
        if r["rax"] != ref_strlen(ch):
            raise EchecOracle(f"libc-03 : longueur {r['rax']} != {ref_strlen(ch)}")
        if bytes((ctypes.c_ubyte * len(ch)).from_address(c)) != ch:
            raise EchecOracle("libc-03 : chaîne mutée")
        if not cart.non_volatils_intacts(r) or r["rsp"] != r["sommet"]:
            raise EchecOracle("libc-03 : non volatils ou pile")
    verrous.append(f"libc-03: {total} cas")

    # --- libc-04 itoa : bornes + aléatoire, anti-débordement au-delà du tampon ---
    total = 0
    bornes = [0, 1, 9, 10, 99, 100, 999, 1000, 2**31 - 1, 2**31, 2**32 - 1]
    valeurs = bornes + [rng.randrange(2**32) for _ in range(n_blocs - len(bornes))]
    for v in valeurs:
        c = buf(64)
        ctypes.memset(c, 0xA5, 64)
        r = cart.appeler(img.adr(L.A_ITOA), [v, c])
        attendu = ref_itoa(v)
        ecrit = bytes((ctypes.c_ubyte * 16).from_address(c))
        total += 1
        if ecrit[:len(attendu)] != attendu:
            raise EchecOracle(f"libc-04 : {v} -> {ecrit[:16]!r} != {attendu!r}")
        if bytes((ctypes.c_ubyte * 48).from_address(c + 16)) != b"\xa5" * 48:
            raise EchecOracle(f"libc-04 : écriture au-delà du tampon 16 o ({v})")
        if r["rax"] != c:
            raise EchecOracle("libc-04 : rax != tampon")
        if not cart.non_volatils_intacts(r) or r["rsp"] != r["sommet"]:
            raise EchecOracle("libc-04 : non volatils ou pile")
    verrous.append(f"libc-04: {total} cas")

    # --- libc-05/06 zone : séquences allocation/réinitialisation contre le modèle ---
    total = 0
    img.poser_qword(L.R_CURSEUR_CORPUS, 0)
    ref = RefZone(L.ARENE_BASE_CORPUS, L.ARENE_TAILLE_CORPUS)
    for _ in range(n_blocs):
        acte = rng.random()
        if acte < 0.15:
            r = cart.appeler(img.adr(L.A_ZONE_RESET), [])
            ref.reinitialiser()
            total += 1
            if img.qword(L.R_CURSEUR_CORPUS) != 0:
                raise EchecOracle("libc-06 : curseur non nul")
            continue
        taille = rng.choice([0, 1, 8, 16, 64, 100, 0x7C0, 0x7D0, rng.randrange(0, 600)])
        align = rng.choice([1, 2, 8, 16, 32, 64, 0, 3, 65, 128])
        r = cart.appeler(img.adr(L.A_ZONE_ALLOC), [taille, align])
        attendu = ref.allouer(taille, align)
        total += 1
        if r["rax"] != img.adr(attendu) if attendu else r["rax"] != 0:
            raise EchecOracle(
                f"libc-05 : pointeur {r['rax']:#x} != {img.adr(attendu) if attendu else 0:#x} "
                f"(taille={taille}, align={align})")
        if img.qword(L.R_CURSEUR_CORPUS) != ref.curseur:
            raise EchecOracle(f"libc-05 : curseur {img.qword(L.R_CURSEUR_CORPUS)} "
                              f"!= {ref.curseur}")
        if attendu and attendu % max(align, 1):
            raise EchecOracle(f"libc-05 : non aligné ({attendu % align})")
    verrous.append(f"libc-05/06: {total} actes")

    # --- libc-07 memset : n ∈ [0, 1024], au-delà intact ---
    total = 0
    for _ in range(n_blocs):
        n = rng.randrange(0, 1025)
        v = rng.randrange(256)
        d = buf(1024)
        ctypes.memset(d, 0x5C, 1024)
        r = cart.appeler(img.adr(L.A_MEMSET), [d, v, n])
        attendu = ref_memset(n, v)
        ecrit = bytes((ctypes.c_ubyte * 1024).from_address(d))
        total += 1
        if ecrit[:n] != attendu:
            raise EchecOracle(f"libc-07 : région fausse (n={n})")
        if ecrit[n:] != b"\x5c" * (1024 - n):
            raise EchecOracle(f"libc-07 : au-delà écrit (n={n})")
        if r["rax"] != d:
            raise EchecOracle("libc-07 : rax != dst")
        if not cart.non_volatils_intacts(r) or r["rsp"] != r["sommet"]:
            raise EchecOracle("libc-07 : non volatils ou pile")
    verrous.append(f"libc-07: {total} cas")
    return {"verrous": verrous, "cas": sum(int(v.split(": ")[1].split()[0]) for v in verrous)}


# ---------------------------------------------------------------------------
# L'auto-test du patrimoine (libc-08:R3) — la ligne exacte, N rendu
# ---------------------------------------------------------------------------

LIGNE_ATTENDUE = b"TRIADE M1 : minilibc 21/21 OK\n"


def tester_autotest(img: Image, cart: Cartouche) -> dict:
    img.poser_qword(L.R_CURSEUR_CORPUS, 0)
    with Capture() as cap:
        r = cart.appeler(img.adr(L.A_AUTOTEST), [])
        sortie = cap.lire()
    if sortie != LIGNE_ATTENDUE:
        raise EchecOracle(f"libc-08 : sortie {sortie!r} != {LIGNE_ATTENDUE!r}")
    if r["rax"] != 21:
        raise EchecOracle(f"libc-08 : N = {r['rax']} != 21 (Q3 frag-con SysV : N rendu)")
    if not cart.non_volatils_intacts(r) or r["rsp"] != r["sommet"]:
        raise EchecOracle("libc-08 : non volatils ou pile")
    # V4 (corpus-13) : un vecteur doré falsifié -> N < 21, le verdict KO rendu.
    # SC mutée en SA : la fixture sert les DEUX sens (v6 inférieur memcmp(SA,SC)
    # < 0 et v7 supérieur memcmp(SC,SA) > 0 — la notation le constate) : les
    # deux rendent 0, DEUX verdicts perdus, N 19.
    img.poser_qword(L.R_CURSEUR_CORPUS, 0)
    sauv = img.octets(L.R_SC, 8)              # la fixture du vecteur « supérieur »
    img.poser(L.R_SC, b"TRIADE\x00")          # SC == SA : v6 et v7 perdent
    try:
        with Capture() as cap:
            r2 = cart.appeler(img.adr(L.A_AUTOTEST), [])
            sortie2 = cap.lire()
    finally:
        img.poser(L.R_SC, sauv)
    if r2["rax"] != 19 or sortie2 != b"TRIADE M1 : minilibc 19/21 KO\n":
        raise EchecOracle(f"libc-08 falsifié : N={r2['rax']} sortie={sortie2!r}")
    return {"verrous": ["libc-08: ligne exacte + N rendu + vecteur falsifié KO"], "cas": 2}


# ---------------------------------------------------------------------------
# La ligne de journal (tcp-11:R2) — composition exacte, verrou, concurrence
# ---------------------------------------------------------------------------

def tester_journal(img: Image, cart: Cartouche, graine: int, volume: str) -> dict:
    rng = random.Random(graine * 1000 + 3)
    n_lignes = {"complet": 4000, "reduit": 400}.get(volume, 400)
    verrous = []
    if img.qword(L.R_VERROU) != 0:
        raise EchecOracle("tcp-11 : le verrou n'est pas né déverrouillé (P5 frag-con)")
    total = 0
    with Capture() as cap:
        for _ in range(n_lignes):
            lp = rng.randrange(0, 21)
            ls = rng.randrange(0, 21)
            pref = bytes(rng.randrange(33, 127) for _ in range(lp))
            suff = bytes(rng.randrange(33, 127) for _ in range(ls))
            p, s = buf_ = None, None
            cart2 = cart
            p = cart2._libc.mmap(ctypes.c_void_p(0), ctypes.c_size_t(64),
                                 ctypes.c_int(mmap.PROT_READ | mmap.PROT_WRITE),
                                 ctypes.c_int(mmap.MAP_PRIVATE | mmap.MAP_ANONYMOUS),
                                 ctypes.c_int(-1), ctypes.c_size_t(0))
            s = cart2._libc.mmap(ctypes.c_void_p(0), ctypes.c_size_t(64),
                                 ctypes.c_int(mmap.PROT_READ | mmap.PROT_WRITE),
                                 ctypes.c_int(mmap.MAP_PRIVATE | mmap.MAP_ANONYMOUS),
                                 ctypes.c_int(-1), ctypes.c_size_t(0))
            ctypes.memmove(p, pref + b"\0", lp + 1)
            ctypes.memmove(s, suff + b"\0", ls + 1)
            if rng.random() < 0.2:
                valeur, champ = 0xFFFFFFFF, b""
            else:
                valeur = rng.randrange(0, 2**32)
                champ = str(valeur).encode()
            attendu = pref + champ + suff
            r = cart.appeler(img.adr(L.A_JOURNAL), [p, lp, valeur, s, ls])
            total += 1
            if r["rax"] != len(attendu):
                raise EchecOracle(f"tcp-11 : verdict {r['rax']} != {len(attendu)} (Q2 brut)")
            if img.qword(L.R_VERROU) != 0:
                raise EchecOracle("tcp-11 : le verrou reste pris (Q3)")
            if not cart.non_volatils_intacts(r) or r["rsp"] != r["sommet"]:
                raise EchecOracle("tcp-11 : non volatils ou pile")
            if cap.lire() != attendu:
                raise EchecOracle("tcp-11 : la ligne composée diverge (Q1)")
    verrous.append(f"tcp-11 composition: {total} lignes exactes, verrou rendu un-pour-un")

    # V3 — la concurrence RÉELLE : deux threads, deux préfixes, aucun entrelacement
    NP = 300
    resultats = []

    def travailleur(marque: bytes, k: int):
        for i in range(NP):
            p = cart._libc.mmap(ctypes.c_void_p(0), ctypes.c_size_t(64),
                                ctypes.c_int(mmap.PROT_READ | mmap.PROT_WRITE),
                                ctypes.c_int(mmap.MAP_PRIVATE | mmap.MAP_ANONYMOUS),
                                ctypes.c_int(-1), ctypes.c_size_t(0))
            ligne = marque + str(i).encode() + b"\n"
            ctypes.memmove(p, ligne + b"\0", len(ligne) + 1)
            r = cart.appeler(img.adr(L.A_JOURNAL),
                             [p, len(ligne), 0xFFFFFFFF, p, 0])
            resultats.append(r["rax"] == len(ligne))

    with Capture() as cap:
        t1 = threading.Thread(target=travailleur, args=(b"AA ", 1))
        t2 = threading.Thread(target=travailleur, args=(b"BBB ", 2))
        t1.start(); t2.start(); t1.join(); t2.join()
        flux = cap.lire()
    if not all(resultats) or len(resultats) != 2 * NP:
        raise EchecOracle("tcp-11 concurrence : verdicts divergents")
    lignes = flux.split(b"\n")
    lignes = [l for l in lignes if l]
    if len(lignes) != 2 * NP:
        raise EchecOracle(f"tcp-11 concurrence : {len(lignes)} lignes != {2 * NP} "
                          f"(fragments ?)")
    for l in lignes:
        if not (l.startswith(b"AA ") or l.startswith(b"BBB ")):
            raise EchecOracle(f"tcp-11 concurrence : ligne fragmentée {l!r}")
    if img.qword(L.R_VERROU) != 0:
        raise EchecOracle("tcp-11 concurrence : le verrou reste pris")
    verrous.append(f"tcp-11 concurrence: 2 threads natifs, {2 * NP} lignes entières")
    return {"verrous": verrous, "cas": total + 2 * NP}


# ---------------------------------------------------------------------------
# Le moteur de patch (tcp-07:R4) — scénario complet, refus nommés, DEP
# ---------------------------------------------------------------------------

def tester_patch(chemin: str, img: Image, cart: Cartouche) -> dict:
    verrous = []
    entree = L.A_JOURNAL
    croissance = L.A_CROISSANCE
    staging_rva, taille = _lire_staging(img)

    original = img.octets(entree, 8)
    if img.octets(croissance, 16) == b"\xcc" * 16:
        pass  # la croissance naît int3 — le plan
    if img.qword(L.R_ETAT_PATCH_CORPUS) != 0:
        raise EchecOracle("tcp-07 : l'état n'est pas né v1 (P4)")

    # V2 — appliquer : la croissance = staging, l'entrée = E9 rel32 + NOP x3
    r = cart.appeler(img.adr(L.A_PATCH), [0])
    if r["rax"] != 0:
        raise EchecOracle(f"tcp-07 apply : rax = {r['rax']} != 0")
    staging_octets = img.octets(staging_rva, taille)
    if img.octets(croissance, taille) != staging_octets:
        raise EchecOracle("tcp-07 apply : la croissance != staging (Q1)")
    tramp = img.octets(entree, 8)
    if tramp[0] != 0xE9 or tramp[5:] != b"\x90\x90\x90":
        raise EchecOracle(f"tcp-07 apply : le trampoline {tramp.hex()} != E9+rel32+NOPs (Q1)")
    rel32 = struct.unpack("<i", tramp[1:5])[0]
    if (entree + 5 + rel32) != croissance:
        raise EchecOracle(f"tcp-07 apply : le rel32 vise {entree + 5 + rel32:#x} "
                          f"!= croissance {croissance:#x}")
    if img.qword(L.R_ENTREE_SAUVEE) != struct.unpack("<Q", original)[0]:
        raise EchecOracle("tcp-07 apply : l'original non sauvegardé (Q1)")
    if img.qword(L.R_ETAT_PATCH_CORPUS) != 1:
        raise EchecOracle("tcp-07 apply : l'état != 1 (Q1)")
    verrous.append("tcp-07 apply: croissance=staging, E9 rel32 exact, original sauvé, état 1")

    # V2 suite — LE PATCH EST EFFECTIF : l'entrée APPELÉE rend le remplaçant
    with Capture() as cap:
        p = cart._libc.mmap(ctypes.c_void_p(0), ctypes.c_size_t(64),
                            ctypes.c_int(mmap.PROT_READ | mmap.PROT_WRITE),
                            ctypes.c_int(mmap.MAP_PRIVATE | mmap.MAP_ANONYMOUS),
                            ctypes.c_int(-1), ctypes.c_size_t(0))
        ligne = b"verdict"
        ctypes.memmove(p, ligne + b"\0", len(ligne) + 1)
        cart.appeler(img.adr(entree), [p, len(ligne), 0xFFFFFFFF, p, 0])
        emission = cap.lire()
    if emission != b"j2: verdict":
        raise EchecOracle(f"tcp-07 : le remplaçant n'est pas effectif ({emission!r})")
    verrous.append("tcp-07 effet: l'entrée appelée rend le journal v2 (marque j2:)")

    # V4 — états incohérents : apply x2 -> code 4
    r = cart.appeler(img.adr(L.A_PATCH), [0])
    if r["rax"] != 4:
        raise EchecOracle(f"tcp-07 apply x2 : {r['rax']} != 4")

    # V2 fin — rollback : entrée restaurée, état 0, comportement v1 de retour
    r = cart.appeler(img.adr(L.A_PATCH), [1])
    if r["rax"] != 0:
        raise EchecOracle(f"tcp-07 rollback : {r['rax']} != 0")
    if img.octets(entree, 8) != original:
        raise EchecOracle("tcp-07 rollback : l'entrée non restaurée octet pour octet (Q2)")
    if img.qword(L.R_ETAT_PATCH_CORPUS) != 0:
        raise EchecOracle("tcp-07 rollback : l'état != 0")
    if img.octets(croissance, taille) != staging_octets:
        raise EchecOracle("tcp-07 rollback : la croissance effacée (Q2 : le remplaçant y dort)")
    with Capture() as cap:
        p = cart._libc.mmap(ctypes.c_void_p(0), ctypes.c_size_t(64),
                            ctypes.c_int(mmap.PROT_READ | mmap.PROT_WRITE),
                            ctypes.c_int(mmap.MAP_PRIVATE | mmap.MAP_ANONYMOUS),
                            ctypes.c_int(-1), ctypes.c_size_t(0))
        ligne = b"verdict"
        ctypes.memmove(p, ligne + b"\0", len(ligne) + 1)
        cart.appeler(img.adr(entree), [p, len(ligne), 0xFFFFFFFF, p, 0])
        emission = cap.lire()
    if emission != b"verdict":
        raise EchecOracle(f"tcp-07 : le v1 n'est pas de retour ({emission!r})")
    verrous.append("tcp-07 rollback: entrée restaurée, croissance conservée, v1 de retour")

    # V4 — rollback x2, rollback sans application -> code 4
    if cart.appeler(img.adr(L.A_PATCH), [1])["rax"] != 4:
        raise EchecOracle("tcp-07 rollback x2 : != 4")
    if cart.appeler(img.adr(L.A_PATCH), [1])["rax"] != 4:
        raise EchecOracle("tcp-07 rollback à vide : != 4")

    # P1 — mode invalide -> code 1
    if cart.appeler(img.adr(L.A_PATCH), [2])["rax"] != 1:
        raise EchecOracle("tcp-07 mode 2 : != 1")
    if cart.appeler(img.adr(L.A_PATCH), [0xFFFFFFFF])["rax"] != 1:
        raise EchecOracle("tcp-07 mode -1 : != 1")
    verrous.append("tcp-07 refus: modes invalides code 1, états incohérents code 4")

    # V3 — falsification du staging : un octet corrompu -> code 3, RIEN écrit
    img.poser(staging_rva + 7, bytes([staging_octets[7] ^ 0xFF]))
    r = cart.appeler(img.adr(L.A_PATCH), [0])
    if r["rax"] != 3:
        raise EchecOracle(f"tcp-07 staging corrompu : {r['rax']} != 3")
    if img.octets(entree, 8) != original:
        raise EchecOracle("tcp-07 staging corrompu : l'entrée a bougé (Q5 : aucun effet)")
    if img.qword(L.R_ETAT_PATCH_CORPUS) != 0:
        raise EchecOracle("tcp-07 staging corrompu : l'état a bougé (Q5)")
    verrous.append("tcp-07 intégrité: staging corrompu -> code 3, aucun effet (R10)")

    # code 2 — staging absent (taille 0) : sur UNE image séparée
    img2 = Image(chemin, "prive")
    img2.poser_qword(L.R_TAB_SUM_CORPUS + 4, 0)          # taille 0 = absent
    if cart.appeler(img2.adr(L.A_PATCH), [0])["rax"] != 2:
        raise EchecOracle("tcp-07 staging absent : != 2")
    verrous.append("tcp-07 absent: taille 0 -> code 2")

    # code 5 — le service REFUSE : cartographie partagée en lecture seule
    img3 = Image(chemin, "partage")
    r = cart.appeler(img3.adr(L.A_PATCH), [0])
    if r["rax"] != 5:
        raise EchecOracle(f"tcp-07 mprotect refusé : {r['rax']} != 5 (le noyau parle)")
    if img3.octets(entree, 8) != original:
        raise EchecOracle("tcp-07 refus : l'entrée a bougé AVANT le refus (Q5)")
    verrous.append("tcp-07 service: mprotect EACCES (cartographie partagée lecture seule) -> code 5")

    # V7 — falsification DEP : la constante RWX 0x7 -> 0x3, l'exécution FAUTE
    verrous.append(_falsification_dep(chemin))
    return {"verrous": verrous, "cas": len(verrous)}


def _lire_staging(img: Image):
    rva = struct.unpack("<I", img.octets(L.R_TAB_SUM_CORPUS, 4))[0]
    taille = struct.unpack("<I", img.octets(L.R_TAB_SUM_CORPUS + 4, 4))[0]
    if rva != L.R_STAGING_CORPUS or not taille:
        raise EchecOracle(f"table d'intégrité : rva={rva:#x} taille={taille}")
    return rva, taille


def _falsification_dep(chemin: str) -> str:
    """V7 — la constante de phase 0x7 réécrite en 0x3 : la page du code
    devient R+W SANS X ; le mprotect retourne, et le RET du patch lui-même
    (dans la page sans X) FAUTE : SIGSEGV. L'épreuve vit dans UN FILS : le
    code défaillant ne tue jamais l'instrument (le père observe, le fils
    meurt) — tcp-07 est hors-chemin du principal, l'artefact ne peut pas
    l'éprouver : le patch est appelé ici directement, sur son image."""
    with open(chemin, "rb") as f:
        art = bytearray(f.read())
    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    cible = None
    code = bytes(art[L.A_PATCH:L.A_PATCH + 0x200])
    for insn in cs.disasm(code, L.A_PATCH):
        if insn.mnemonic == "mov" and insn.op_str == "edi, 7":
            cible = insn.address + 1          # l'octet de l'immédiat 0x07
            break
    if cible is None:
        raise EchecOracle("V7 : l'immédiat 0x7 de tcp-07 introuvable")
    art[cible] = 0x03
    mute = chemin + ".dep-7-3"
    with open(mute, "wb") as f:
        f.write(bytes(art))
    try:
        os.chmod(mute, 0o755)
        pid = os.fork()
        if pid == 0:
            # le FILS : mappings hérités privés, crash = verdict, jamais une
            # perte pour l'instrument ; cartouche neuve dans le fils
            try:
                img_m = Image(mute, "prive")
                cart_f = Cartouche()
                cart_f.appeler(img_m.adr(L.A_PATCH), [0])
                os._exit(0)               # apply « rendu » : INATTENDU
            except BaseException:
                os._exit(3)               # échec nommé Python : INATTENDU
        _, status = os.waitpid(pid, 0)
        sig = status & 0x7F
        code_sortie = -sig if sig else (status >> 8)
    finally:
        os.unlink(mute)
    if code_sortie != -11:                     # SIGSEGV
        return f"tcp-07 DEP: code {code_sortie} INATTENDU — À NOMMER"
    return ("tcp-07 DEP: 0x7 -> 0x3, le ret du patch faute (page sans X) — "
            "SIGSEGV en fils, zéro silence")


# ---------------------------------------------------------------------------
# L'artefact entier (V2 de corpus-13) — les deux lignes exactes, code 0
# ---------------------------------------------------------------------------

SORTIE_ATTENDUE = (b"TRIADE M1 : minilibc 21/21 OK\n"
                   b"corpus : autotest 21 vecteurs\n")


def tester_artefact(chemin: str) -> dict:
    verrous = []
    codes = set()
    for _ in range(6):
        r = subprocess.run([chemin], capture_output=True, timeout=10)
        codes.add((r.returncode, r.stdout))
    if codes != {(0, SORTIE_ATTENDUE)}:
        for code, sortie in codes:
            if (code, sortie) != (0, SORTIE_ATTENDUE):
                raise EchecOracle(f"corpus-13 : code {code}, sortie {sortie!r} "
                                  f"!= les deux lignes exactes (Q1)")
    verrous.append("corpus-13: 6 exécutions, deux lignes octet-identiques, code 0 — "
                   "le comportement identique à CHAQUE base (PIE, le noyau choisit)")
    # sous ADDR_NO_RANDOMIZE : même comportement à base fixée
    r1 = subprocess.run(["setarch", "-R", chemin], capture_output=True, timeout=10)
    r2 = subprocess.run(["setarch", "-R", chemin], capture_output=True, timeout=10)
    if not (r1.returncode == r2.returncode == 0
            and r1.stdout == r2.stdout == SORTIE_ATTENDUE):
        raise EchecOracle("corpus-13 : setarch -R divergent")
    verrous.append("corpus-13 PIE: setarch -R (base figée) — comportement identique")
    return {"verrous": verrous, "cas": 8}


# ---------------------------------------------------------------------------
# La falsification de l'artefact (V3 de corpus-13) — zéro silence
# ---------------------------------------------------------------------------

def tester_falsification(chemin: str) -> dict:
    """Un octet corrompu dans CHAQUE bloc : sortie, code ou signal divergent.

    La leçon du premier run (libc-06) : la mutation de la PREMIÈRE
    instruction peut être « guérie » par un résidu de registre — le lea r8
    muté laissait le store [r8], 0 tomber ENCORE sur le curseur, r8 résiduel
    de l'appelant portant par hasard la bonne adresse. La falsification
    essaie donc les instructions du bloc L'UNE APRÈS L'AUTRE : un bloc est
    ROMPU dès qu'une mutation dévie ; si TOUTES passent silencieusement,
    l'oracle est VACUE et refuse.
    """
    with open(chemin, "rb") as f:
        art = f.read()
    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    mute_nominal = (0, SORTIE_ATTENDUE)
    rompus, essais = 0, 0
    detail = []
    HORS_CHEMIN = {"f61012"}   # tcp-07 : le patch n'est PAS dans le flot du
    # principal (corpus-13 ne l'appelle pas — la démonstration M5-(c) est le
    # chantier (d)) : AUCUNE corruption d'un bloc non exécuté ne peut dévier
    # l'artefact. Le leçon du premier run : 78 mutations de tcp-07 TOUTES
    # silencieuses — le fait de plan, pas une vacuité de l'oracle. Le patch
    # est épuisé par SON scénario (apply/rollback/effet, intégrité staging
    # code 3, refus code 5) et par le V7 DEP (en fils).
    for bid, spec, fichier, rva, slot in L.BLOCS_CORPUS:
        if bid in HORS_CHEMIN:
            continue
        # les instructions réelles du bloc : du début au premier ret inclus
        adresses = []
        for insn in cs.disasm(bytes(art[rva:rva + slot]), rva):
            adresses.append(insn.address)
            if insn.mnemonic == "ret":
                break
        if not adresses:
            raise EchecOracle(f"falsification : {fichier} sans instruction")
        rompu = False
        for adresse in adresses:
            mute = bytearray(art)
            mute[adresse] ^= 0xFF              # le premier octet d'une instruction
            essais += 1
            chemin_mute = chemin + ".falsif"
            with open(chemin_mute, "wb") as f:
                f.write(bytes(mute))
            try:
                os.chmod(chemin_mute, 0o755)
                try:
                    r = subprocess.run([chemin_mute], capture_output=True, timeout=10)
                    observe = (r.returncode, r.stdout)
                except subprocess.TimeoutExpired:
                    observe = (None, b"timeout")   # un bloc falsifié peut boucler
            finally:
                os.unlink(chemin_mute)
            if observe != mute_nominal:
                rompu = True
                detail.append(f"{fichier} rompu à {adresse:#x} (essai n°{essais})")
                break
        if not rompu:
            raise EchecOracle(f"falsification : {fichier} — {len(adresses)} mutations "
                              f"TOUTES silencieuses — oracle vacue (V3)")
        rompus += 1
    attendus = len(L.BLOCS_CORPUS) - len(HORS_CHEMIN)
    return {"verrous": [f"falsification: {rompus}/{attendus} blocs du chemin rompus "
                        f"({essais} mutations essayées) — zéro silence ; "
                        f"tcp-07 hors-chemin : le scénario du patch et le V7 DEP"],
            "cas": essais}


# ---------------------------------------------------------------------------
# Le point d'entrée de la chaîne (build_corpus.py)
# ---------------------------------------------------------------------------

def executer(chemin: str, graine: int = 1, volume: str = "complet") -> dict:
    """L'oracle complet : différentiel + scénarios + artefact + falsification.

    Retourne le verdict (empreinte hachée pour frag-prf — les verdicts
    seuls survivent, D1).
    """
    print(f"[oracle-corpus] graine {graine}, volume {volume} — exécution NATIVE")
    cart = Cartouche()
    img = Image(chemin, "prive")
    parties = [
        tester_blocs_purs(img, cart, graine, volume),
        tester_autotest(img, cart),
        tester_journal(img, cart, graine, volume),
        tester_patch(chemin, img, cart),
        tester_artefact(chemin),
        tester_falsification(chemin),
    ]
    verrous = [v for p in parties for v in p["verrous"]]
    cas = sum(p["cas"] for p in parties)
    empreinte = hashlib.sha256(
        ("\n".join(verrous) + f"\ncas={cas}\ngraine={graine}\nvolume={volume}\n").encode()
    ).hexdigest()
    for v in verrous:
        print(f"[oracle-corpus]   {v}")
    print(f"[oracle-corpus] {cas} cas verts, {len(verrous)} verrous — "
          f"empreinte {empreinte[:16]}…")
    return {"verrous": verrous, "cas": cas, "empreinte": empreinte,
            "binaire": "deux lignes exactes, code 0", "falsification": "zéro silence"}


if __name__ == "__main__":
    chemin = sys.argv[1] if len(sys.argv) > 1 else os.path.join(UNIX, "corpus")
    graine = int(sys.argv[sys.argv.index("--graine") + 1]) if "--graine" in sys.argv else 1
    volume = (sys.argv[sys.argv.index("--volume") + 1]
              if "--volume" in sys.argv else "complet")
    executer(chemin, graine, volume)
