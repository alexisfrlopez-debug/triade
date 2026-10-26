#!/usr/bin/env python3
"""oracle_differentiel.py — Oracle éphémère du jalon M1 (D1, D29).

Implémentation de référence DÉRIVÉE DE LA COUCHE I (m1/I/*.md) — jamais de la
notation — exécutée sur un substrat d'émulation Unicorn :

  1. tests par bloc : chaque bloc reçoit des entrées aléatoires contraintes par
     les pré-conditions de son contrat, la sortie (valeur de retour, mémoire,
     curseur, registres non volatils, RSP, intégrité de l'image hors régions
     autorisées) est comparée à la référence. Volume de référence : 12 000 cas
     par bloc critique (spécification § 8) ;
  2. émulation du binaire entier avec shims IAT (GetStdHandle/WriteFile/
     ExitProcess) : la sortie doit être exactement la ligne de verdict attendue
     et le code de sortie 0 ;
  3. falsification : la corruption d'un octet de code d'un bloc doit être
     détectée (aucune vacuité de l'oracle).

L'oracle est régénéré/exécuté à chaque session (D1) : seuls ses verdicts hachés
survivent dans frag-prf. Les graines différencient les exécutions — dix
vérifications cristallisent un bloc (R6) sans jamais répéter les mêmes entrées.

Usage (depuis build_m1.py) : executer(exe, graine=N, volume="complet"|"reduit")
"""

from __future__ import annotations

import hashlib
import random
import struct
import sys

import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import layout as L

import unicorn as _uc
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE
from unicorn.x86_const import (
    UC_X86_REG_RSP, UC_X86_REG_RIP, UC_X86_REG_RAX, UC_X86_REG_RCX,
    UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9, UC_X86_REG_RBX,
    UC_X86_REG_RBP, UC_X86_REG_RDI, UC_X86_REG_RSI, UC_X86_REG_R12,
    UC_X86_REG_R13, UC_X86_REG_R14, UC_X86_REG_R15,
)

IMAGE = L.IMAGE_BASE
PILE_BASE = 0x500000000          # pile d'émulation
PILE_TAILLE = 0x100000
PILE_SOMMET = PILE_BASE + PILE_TAILLE - 0x1000
SENTINELLE = 0xDEADBEEFCAFE      # adresse de retour factice
PAGE_SENTINELLE = SENTINELLE & ~0xFFF
SRC = 0x150000000                # grattage : source
DST = 0x150100000                # grattage : destination
TMP = 0x150200000                # grattage : tampon
TRAMPOLINE = 0x140100000         # fausses adresses d'API (page RX)
FAKE_GSH, FAKE_WF, FAKE_EP = TRAMPOLINE, TRAMPOLINE + 0x10, TRAMPOLINE + 0x20
FAKE_HANDLE = 0x0000BEEF

NON_VOLATILS = [UC_X86_REG_RBX, UC_X86_REG_RBP, UC_X86_REG_RDI, UC_X86_REG_RSI,
                UC_X86_REG_R12, UC_X86_REG_R13, UC_X86_REG_R14, UC_X86_REG_R15]
MAGIE = 0x5A5A5A5A5A5A5A5A


class EchecOracle(Exception):
    """Tout écart entre le bloc émulé et la référence dérivée de I."""


# --- Emulateur -----------------------------------------------------------------

class Emulateur:
    """Une instance = un binaire mappé. Les cas réutilisent le même moteur."""

    def __init__(self, exe: bytes):
        exe = bytes(exe)
        self.exe = exe
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        uc = self.uc
        uc.mem_map(IMAGE, L.SIZE_OF_IMAGE)                       # image
        uc.mem_map(PILE_BASE, PILE_TAILLE)                       # pile
        uc.mem_map(PAGE_SENTINELLE, 0x1000)                      # retour factice
        uc.mem_map(SRC, 0x300000)                                # grattage 3 Mo
        uc.mem_write(IMAGE + L.TEXT_RVA, exe[L.TEXT_FILE:L.TEXT_FILE + L.TEXT_VSIZE])
        uc.mem_write(IMAGE + L.RDATA_RVA, exe[L.RDATA_FILE:L.RDATA_FILE + L.RDATA_VSIZE])
        uc.mem_write(IMAGE + L.DATA_RVA, exe[L.DATA_FILE:L.DATA_FILE + L.DATA_RAW])
        # État .data de référence : la queue BSS est nulle (chargeur)
        self.donnees_vierges = bytes(uc.mem_read(IMAGE + L.DATA_RVA, L.DATA_VSIZE))
        self.reinitialiser_donnees()
        # L'intégrité de l'image se mesure APRÈS résolution de l'IAT par le
        # chargeur (les shim remplacent les hint/name — comportement légitime).
        self.image_code = bytes(uc.mem_read(IMAGE + L.TEXT_RVA, L.TEXT_VSIZE)) \
            + bytes(uc.mem_read(IMAGE + L.RDATA_RVA, L.RDATA_VSIZE))
        self.sortie = bytearray()
        self.code_sortie = None

    def reinitialiser_donnees(self):
        """Remet .data à l'état chargeur (curseur nul) et l'IAT aux shim."""
        self.uc.mem_write(IMAGE + L.DATA_RVA, b"\x00" * L.DATA_VSIZE)
        for nom, fake in (("GetStdHandle", FAKE_GSH), ("WriteFile", FAKE_WF),
                          ("ExitProcess", FAKE_EP)):
            self.uc.mem_write(IMAGE + L.IAT_SLOTS[nom], struct.pack("<Q", fake))
        self.sortie = bytearray()
        self.code_sortie = None

    def installer_shims(self):
        """Interception des trois API : effet émulé, retour par pile (idempotent)."""
        if getattr(self, "_shims_poses", False):
            return
        uc = self.uc

        def crochet(uc_, adresse, taille, _):
            if adresse == FAKE_GSH:
                uc_.reg_write(UC_X86_REG_RAX, FAKE_HANDLE)
            elif adresse == FAKE_WF:
                tampon = uc_.reg_read(UC_X86_REG_RDX)
                n = uc_.reg_read(UC_X86_REG_R8)
                if uc_.reg_read(UC_X86_REG_RCX) != FAKE_HANDLE:
                    raise EchecOracle("WriteFile : handle inattendu (P1 de hello-02)")
                self.sortie += bytes(uc_.mem_read(tampon, n))
                uc_.reg_write(UC_X86_REG_RAX, 1)
            elif adresse == FAKE_EP:
                self.code_sortie = uc_.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF
                uc_.emu_stop()
                return
            else:
                return
            rsp = uc_.reg_read(UC_X86_REG_RSP)
            retour = struct.unpack("<Q", uc_.mem_read(rsp, 8))[0]
            uc_.reg_write(UC_X86_REG_RSP, rsp + 8)
            uc_.reg_write(UC_X86_REG_RIP, retour)

        uc.mem_map(TRAMPOLINE, 0x1000)
        uc.mem_write(TRAMPOLINE, b"\xc3" * 0x1000)
        self.hook = uc.hook_add(UC_HOOK_CODE, crochet)
        self._shims_poses = True

    def appeler(self, rva: int, args: tuple = (0, 0, 0, 0), limite: int = 2_000_000):
        """Appelle un bloc : pile alignée, sentinel de retour, non-volatiles magiques."""
        uc = self.uc
        uc.reg_write(UC_X86_REG_RSP, PILE_SOMMET - 8)
        uc.mem_write(PILE_SOMMET - 8, struct.pack("<Q", SENTINELLE))
        for reg, val in zip((UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9), args):
            uc.reg_write(reg, val)
        for reg in NON_VOLATILS:
            uc.reg_write(reg, MAGIE)
        uc.reg_write(UC_X86_REG_RAX, 0)
        # canari de pile : profondeur légitime < 0x400
        uc.mem_write(PILE_SOMMET - 0x1000, b"\xaa" * 0xC00)
        uc.emu_start(IMAGE + rva, SENTINELLE, count=limite)

    def verifier_enveloppe(self, rax_attendu=None):
        """RSP restauré, sentinel consommé, non volatils intacts, canari intact."""
        uc = self.uc
        if uc.reg_read(UC_X86_REG_RSP) != PILE_SOMMET:
            raise EchecOracle(f"RSP non restaure : {uc.reg_read(UC_X86_REG_RSP):#x}")
        for reg in NON_VOLATILS:
            if uc.reg_read(reg) != MAGIE:
                raise EchecOracle(f"registre non volatil modifie (I2/I3) : {reg}")
        if bytes(uc.mem_read(PILE_SOMMET - 0x1000, 0xC00)) != b"\xaa" * 0xC00:
            raise EchecOracle("ecriture sauvage sous la pile (profondeur > legitime)")
        if bytes(uc.mem_read(IMAGE + L.TEXT_RVA, L.TEXT_VSIZE)) + \
           bytes(uc.mem_read(IMAGE + L.RDATA_RVA, L.RDATA_VSIZE)) != self.image_code:
            raise EchecOracle("image .text/.rdata modifiee pendant l'execution")
        rax = uc.reg_read(UC_X86_REG_RAX)
        if rax_attendu is not None and rax != rax_attendu:
            raise EchecOracle(f"rax = {rax:#x}, attendu {rax_attendu:#x}")
        return rax

    def donnees(self) -> bytes:
        return bytes(self.uc.mem_read(IMAGE + L.DATA_RVA, L.DATA_VSIZE))


# --- Références dérivées de la couche I ------------------------------------------
# Chaque fonction relie sa ligne à la clause du contrat (libc-0N) qu'elle incarne.

def ref_memcpy(src: bytes, n: int) -> bytes:
    """libc-01 Q1 : les n octets de dst sont egaux a ceux de src."""
    return src[:n]


def ref_memcmp(a: bytes, b: bytes, n: int) -> int:
    """libc-02 Q1-Q4 : verdict normalise -1/0/+1 au premier octet divergent."""
    for i in range(n):
        if a[i] != b[i]:
            return -1 if a[i] < b[i] else 1
    return 0


def ref_strlen(s: bytes) -> int:
    """libc-03 Q1 : offset du premier octet nul."""
    return s.index(0)


def ref_itoa(v: int) -> bytes:
    """libc-04 Q1/Q2 : decimale compacte, NUL final."""
    return str(v).encode("ascii") + b"\x00"


def ref_zone_alloc(curseur: int, taille: int, align: int):
    """libc-05 Q1-Q4 : modele du curseur. Retour (pointeur_absolu|0, nouveau_curseur)."""
    if taille > L.ARENE_TAILLE:
        return 0, curseur                                     # Q3 : taille > arene
    if align == 0 or (align & (align - 1)) != 0 or align > 64:
        return 0, curseur                                     # Q3 : alignement invalide
    offset = (curseur + align - 1) & ~(align - 1)
    if offset + taille > L.ARENE_TAILLE:
        return 0, curseur                                     # Q3 : arene epuisee
    return IMAGE + L.ARENE_BASE + offset, offset + taille


def ref_memset(n: int, octet: int) -> bytes:
    """libc-07 Q1 : n octets egaux a l'octet de remplissage."""
    return bytes([octet]) * n


# --- Suites par bloc ---------------------------------------------------------------

VOLUMES = {
    "complet": {"b20001": 12000, "b20002": 12000, "b20003": 12000, "b20004": 12000,
                "b20005": 12000, "b20006": 3000, "b20007": 12000, "a10002": 1000,
                "a10003": 10},
    "reduit": {"b20001": 300, "b20002": 300, "b20003": 300, "b20004": 300,
               "b20005": 300, "b20006": 100, "b20007": 300, "a10002": 50,
               "a10003": 3},
}


def _alea(graine: int, bid: str) -> random.Random:
    return random.Random(f"M1:{graine}:{bid}")


def suite_memcpy(em: Emulateur, rng: random.Random, cas: int):
    """libc-01 : V2 — dst, src, rax, non volatils, bornes, src inchange."""
    for _ in range(cas):
        n = rng.choice((0, 1, 2, 3, 7, 15, 16, 17, 31, 33, 64, rng.randrange(0, 128),
                        rng.randrange(0, 1024)))
        src = bytes(rng.randrange(256) for _ in range(1024))
        attendu = ref_memcpy(src, n)
        em.reinitialiser_donnees()
        em.uc.mem_write(SRC, src)
        em.uc.mem_write(DST, b"\x5c" * 1024)
        em.appeler(0x1100, (DST, SRC, n, 0))
        rax = em.verifier_enveloppe(DST)
        obtenu = bytes(em.uc.mem_read(DST, 1024))
        if obtenu[:n] != attendu:
            raise EchecOracle(f"memcpy : dst diverge (n={n})")
        if obtenu[n:] != b"\x5c" * (1024 - n):
            raise EchecOracle(f"memcpy : ecriture au-dela de dst+n (Q3/I4, n={n})")
        if bytes(em.uc.mem_read(SRC, 1024)) != src:
            raise EchecOracle("memcpy : src modifie (Q3)")
        if em.donnees() != em.donnees_vierges:
            raise EchecOracle("memcpy : .data modifiee")


def suite_memcmp(em: Emulateur, rng: random.Random, cas: int):
    """libc-02 : V2 — verdict exact -1/0/+1, regions intactes."""
    for _ in range(cas):
        n = rng.choice((0, 1, 2, 3, 6, 16, 33, 64, rng.randrange(0, 256)))
        longueur = n + rng.randrange(0, 64)
        a = bytearray(rng.randrange(256) for _ in range(longueur))
        b = bytearray(a)
        relation = rng.choice(("egal", "inferieur", "superieur"))
        if relation != "egal" and n > 0:
            pos = rng.randrange(n)
            if relation == "inferieur":
                a[pos], b[pos] = 0x25, 0x42
            else:
                a[pos], b[pos] = 0x42, 0x25
        attendu = ref_memcmp(bytes(a), bytes(b), n)
        em.reinitialiser_donnees()
        em.uc.mem_write(SRC, bytes(a))
        em.uc.mem_write(DST, bytes(b))
        em.appeler(0x1180, (SRC, DST, n, 0))
        rax = em.verifier_enveloppe()
        if (rax & 0xFFFFFFFF) != (attendu & 0xFFFFFFFF):
            raise EchecOracle(f"memcmp : verdict {rax & 0xFFFFFFFF:#x} != {attendu} (n={n}, {relation})")
        if bytes(em.uc.mem_read(SRC, longueur)) != bytes(a) or \
           bytes(em.uc.mem_read(DST, longueur)) != bytes(b):
            raise EchecOracle("memcmp : region comparee modifiee (I4)")


def suite_strlen(em: Emulateur, rng: random.Random, cas: int):
    """libc-03 : V2 — longueur exacte, chaine intacte, arret au premier nul (I4)."""
    for _ in range(cas):
        lg = rng.choice((0, 1, 2, 6, 33, 100, rng.randrange(0, 200)))
        chaine = bytes(rng.randrange(1, 256) for _ in range(lg)) + b"\x00"
        apres = bytes(rng.randrange(1, 256) for _ in range(64))
        attendu = ref_strlen(chaine)
        em.reinitialiser_donnees()
        em.uc.mem_write(SRC, chaine + apres)
        em.appeler(0x1200, (SRC, 0, 0, 0))
        rax = em.verifier_enveloppe()
        if rax != attendu:
            raise EchecOracle(f"strlen : {rax} != {attendu} (I4 : arret au premier NUL)")


def suite_itoa(em: Emulateur, rng: random.Random, cas: int):
    """libc-04:R2 : V2 — préfixe compact, NUL, rien hors du tampon 12 octets, rax."""
    bornes = [0, 1, 9, 10, 99, 100, 999, 1000, 999999999, 2147483647, 2147483648,
              4294967294, 4294967295]
    for i in range(cas):
        v = bornes[i % len(bornes)] if i < len(bornes) else rng.randrange(1 << 32)
        attendu = ref_itoa(v)
        em.reinitialiser_donnees()
        em.uc.mem_write(TMP, b"\x77" * 16)
        em.appeler(0x1280, (v, TMP, 0, 0))
        rax = em.verifier_enveloppe(TMP)
        obtenu = bytes(em.uc.mem_read(TMP, 16))
        if obtenu[:len(attendu)] != attendu:
            raise EchecOracle(f"itoa : {obtenu[:12]!r} != {attendu!r} pour {v}")
        if obtenu[12:] != b"\x77" * 4:
            raise EchecOracle(f"itoa : ecriture hors du tampon de 12 octets (Q4) pour {v}")


def suite_zone(em: Emulateur, rng: random.Random, cas: int, avec_reset: bool):
    """libc-05/06 : V2 — sequences allocations/reinitialisations contre le modele."""
    aligns_valides = [1, 2, 4, 8, 16, 32, 64]
    aligns_invalides = [0, 3, 5, 63, 65, 128]
    for _ in range(cas):
        em.reinitialiser_donnees()
        curseur = 0
        dernier_ptr, dernier_taille = None, 0
        for _etape in range(rng.randrange(2, 6)):
            if avec_reset and rng.random() < 0.25:
                em.appeler(0x1380)
                em.verifier_enveloppe()
                curseur = 0
                dernier_ptr = None
                continue
            if rng.random() < 0.2:
                taille = rng.choice((L.ARENE_TAILLE + 1, 0x7D0, 0x800, 0x1000, 1 << 40))
                align = rng.choice(aligns_valides)
            elif rng.random() < 0.15:
                taille = rng.randrange(0, 64)
                align = rng.choice(aligns_invalides)
            else:
                taille = rng.choice((0, 1, 2, 3, 8, 15, 16, 17, 33, 64,
                                     rng.randrange(0, 200)))
                align = rng.choice(aligns_valides)
            attendu, curseur_apres = ref_zone_alloc(curseur, taille, align)
            em.appeler(0x1300, (taille, align, 0, 0))
            rax = em.verifier_enveloppe()
            if rax != attendu:
                raise EchecOracle(
                    f"zone_alloc : {rax:#x} != {attendu:#x} (taille={taille}, align={align})")
            if attendu and align > 1 and attendu % align != 0:
                raise EchecOracle(f"zone_alloc : pointeur non aligne ({attendu:#x} % {align})")
            if attendu and dernier_ptr is not None and \
               attendu < dernier_ptr + dernier_taille:
                raise EchecOracle("zone_alloc : chevauchement de bornes (Q1)")
            curseur = curseur_apres
            if attendu:
                dernier_ptr, dernier_taille = attendu, taille
            octets_curseur = struct.unpack("<Q", em.uc.mem_read(IMAGE + L.R_CURSEUR, 8))[0]
            if octets_curseur != curseur:
                raise EchecOracle(f"zone : curseur {octets_curseur} != modele {curseur}")
            if em.donnees()[8:] != em.donnees_vierges[8:]:
                raise EchecOracle("zone : ecriture hors du qword curseur (I3/I4 — arene incluse)")
        if avec_reset:
            em.appeler(0x1380)
            em.verifier_enveloppe()
            if struct.unpack("<Q", em.uc.mem_read(IMAGE + L.R_CURSEUR, 8))[0] != 0:
                raise EchecOracle("zone_reset : curseur non nul (Q1)")
            em.appeler(0x1300, (16, 8, 0, 0))
            rax = em.verifier_enveloppe()
            if rax != IMAGE + L.ARENE_BASE:
                raise EchecOracle("zone_reset : reallocation != base (determinisme)")


def suite_memset(em: Emulateur, rng: random.Random, cas: int):
    """libc-07 : V2 — remplissage exact, bornes intactes, rax = dst."""
    for _ in range(cas):
        n = rng.choice((0, 1, 2, 3, 7, 15, 16, 17, 31, 33, 64, rng.randrange(0, 128),
                        rng.randrange(0, 1024)))
        octet = rng.randrange(256)
        attendu = ref_memset(n, octet)
        em.reinitialiser_donnees()
        em.uc.mem_write(DST, b"\x5c" * 1024)
        em.appeler(0x13C0, (DST, octet, n, 0))
        rax = em.verifier_enveloppe(DST)
        obtenu = bytes(em.uc.mem_read(DST, 1024))
        if obtenu[:n] != attendu:
            raise EchecOracle(f"memset : contenu diverge (n={n})")
        if obtenu[n:] != b"\x5c" * (1024 - n):
            raise EchecOracle(f"memset : ecriture au-dela de dst+n (Q3, n={n})")
        if em.donnees() != em.donnees_vierges:
            raise EchecOracle("memset : .data modifiee")


def suite_write(em: Emulateur, rng: random.Random, cas: int):
    """hello-02 reutilisé : octets exacts transmis a WriteFile, BOOL brut (Q1/Q3)."""
    em.installer_shims()
    for _ in range(cas):
        n = rng.choice((1, 2, 16, 33, 64, rng.randrange(1, 256)))
        tampon = bytes(rng.randrange(256) for _ in range(256))
        em.reinitialiser_donnees()
        for nom, fake in (("GetStdHandle", FAKE_GSH), ("WriteFile", FAKE_WF),
                          ("ExitProcess", FAKE_EP)):
            em.uc.mem_write(IMAGE + L.IAT_SLOTS[nom], struct.pack("<Q", fake))
        em.uc.mem_write(SRC, tampon)
        em.sortie = bytearray()
        em.appeler(0x1040, (FAKE_HANDLE, SRC, n, 0))
        rax = em.verifier_enveloppe()
        if em.sortie != tampon[:n]:
            raise EchecOracle(f"write : sortie diverge ({len(em.sortie)} o != {n})")
        if rax != 1:
            raise EchecOracle(f"write : BOOL = {rax}, attendu 1")


def suite_exit(em: Emulateur, rng: random.Random, cas: int):
    """hello-03 réutilisé : code propagé à ExitProcess, pas de retour (Q1)."""
    em.installer_shims()
    for i in range(cas):
        code = (i * 37) & 0xFFFFFFFF
        em.reinitialiser_donnees()
        for nom, fake in (("GetStdHandle", FAKE_GSH), ("WriteFile", FAKE_WF),
                          ("ExitProcess", FAKE_EP)):
            em.uc.mem_write(IMAGE + L.IAT_SLOTS[nom], struct.pack("<Q", fake))
        em.appeler(0x1080, (code, 0, 0, 0), limite=1000)
        if em.code_sortie != code:
            raise EchecOracle(f"exit : code {em.code_sortie} != {code}")


# --- Émulation du binaire entier ----------------------------------------------------

def emuler_binaire(exe: bytes, phase: int):
    """libc-08 V2 : sortie exacte de la ligne de verdict, code de sortie 0."""
    em = Emulateur(exe)
    em.installer_shims()
    em.appeler(0x1800, limite=10_000_000)
    n = L.NB_TESTS_DEV1 if phase == 1 else L.NB_TESTS_DEV2
    attendu = b"TRIADE M1 : minilibc %d/%d OK\r\n" % (n, n)
    if em.sortie != attendu:
        raise EchecOracle(f"binaire : sortie {bytes(em.sortie)!r} != {attendu!r}")
    if em.code_sortie != 0:
        raise EchecOracle(f"binaire : code de sortie {em.code_sortie} != 0")
    if bytes(em.uc.mem_read(IMAGE + L.TEXT_RVA, L.TEXT_VSIZE)) + \
       bytes(em.uc.mem_read(IMAGE + L.RDATA_RVA, L.RDATA_VSIZE)) != em.image_code:
        raise EchecOracle("binaire : image .text/.rdata modifiee pendant l'execution")
    return bytes(em.sortie), em.code_sortie


# --- Falsification : aucune vacuité de l'oracle --------------------------------------

SUITES = {
    "b20001": lambda em, rng, n: suite_memcpy(em, rng, n),
    "b20002": lambda em, rng, n: suite_memcmp(em, rng, n),
    "b20003": lambda em, rng, n: suite_strlen(em, rng, n),
    "b20004": lambda em, rng, n: suite_itoa(em, rng, n),
    "b20005": lambda em, rng, n: suite_zone(em, rng, n, avec_reset=False),
    "b20006": lambda em, rng, n: suite_zone(em, rng, n, avec_reset=True),
    "b20007": lambda em, rng, n: suite_memset(em, rng, n),
    "a10002": lambda em, rng, n: suite_write(em, rng, n),
    "a10003": lambda em, rng, n: suite_exit(em, rng, n),
}

RVAS = {"b20001": 0x1100, "b20002": 0x1180, "b20003": 0x1200, "b20004": 0x1280,
        "b20005": 0x1300, "b20006": 0x1380, "b20007": 0x13C0,
        "a10002": 0x1040, "a10003": 0x1080, "b20008": 0x1800}


def _binaire_seul(exe: bytes, phase: int):
    sortie, code = emuler_binaire(exe, phase)
    return sortie, code


def falsifier(exe: bytes, phase: int) -> str:
    """Un octet de code corrompu => l'oracle DOIT le détecter (zéro silence)."""
    cibles = ["b20001", "b20002", "b20003", "b20004", "b20005", "b20006", "b20007",
              "a10002", "a10003", "b20008"]
    if phase == 1:
        cibles.remove("b20007")
    detectees = 0
    for bid in cibles:
        rva = RVAS[bid]
        vu = False
        for offset in (0, 5, 10):
            mutant = bytearray(exe)
            mutant[L.TEXT_FILE + (rva - L.TEXT_RVA) + offset] ^= 0xFF
            try:
                if bid == "b20008":
                    _binaire_seul(bytes(mutant), phase)
                else:
                    em = Emulateur(bytes(mutant))
                    SUITES[bid](em, random.Random(f"falsif:{bid}:{offset}"), 200)
                vu = False  # aucune detection : l'oracle serait vide pour cet octet
            except (EchecOracle, _uc.UcError):
                vu = True   # detection : deviation ou arret propre de l'emulation
                break
        if not vu:
            raise EchecOracle(f"falsification : corruption de {bid} non détectée — oracle vide")
        detectees += 1
    return f"{detectees}/{len(cibles)} corruptions détectées"


# --- Point d'entrée -------------------------------------------------------------------

def executer(exe: bytes, graine: int = 1, volume: str = "complet") -> dict:
    if volume not in VOLUMES:
        raise EchecOracle(f"volume inconnu : {volume}")
    phase = 2 if exe[L.TEXT_FILE + (0x13C0 - L.TEXT_RVA)] != 0xCC else 1
    vol = VOLUMES[volume]
    em = Emulateur(exe)
    verdicts, total = {}, 0

    ordre = ["b20005", "b20006", "b20002", "b20001", "b20003", "b20004",
             "a10002", "a10003"]
    if phase >= 2:
        ordre.insert(6, "b20007")
    for bid in ordre:
        n = vol[bid]
        SUITES[bid](em, _alea(graine, bid), n)
        total += n
        verdicts[bid] = {"cas": n, "detail": f"ok({n})"}

    sortie, code = emuler_binaire(exe, phase)
    verdicts["b20008"] = {"cas": 1, "detail": f"emulation complete ok : {sortie!r}, code {code}"}
    falsification = falsifier(exe, phase)

    empreinte = hashlib.sha256(
        json_stable(verdicts).encode("ascii") + f"|graine={graine}|volume={volume}".encode("ascii")
    ).hexdigest()
    return {
        "total_cas": total,
        "blocs": verdicts,
        "binaire": f"sortie exacte, code 0 (phase {phase})",
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
    graine = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[1] == "--graine" else 1
    volume = sys.argv[3] if len(sys.argv) > 3 else "complet"
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "selftest.exe"), "rb") as f:
        exe = f.read()
    v = executer(exe, graine=graine, volume=volume)
    print(f"[oracle] {v['total_cas']} cas verts (volume {v['volume']}, graine {v['graine']})")
    print(f"[oracle] binaire : {v['binaire']}")
    print(f"[oracle] falsification : {v['falsification']}")
    print(f"[oracle] empreinte des verdicts : {v['empreinte']}")
