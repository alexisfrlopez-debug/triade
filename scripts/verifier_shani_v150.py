#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""scripts/verifier_shani_v150.py — LE VÉRIFICATEUR DU PAQUET 6/6 (la variante
SHA-NI, l'instruction lfh49a1xf, D205) : les SIX contrôles de l'instruction
plus la mesure avant/après, TOUT sur pièces.

  V1 — LA NOTATION : round-trip 100 % (keystone → capstone → keystone,
       octet-identique), le contrôle structurel TEMPS CONSTANT du nouveau
       chemin (shani-02 : ZÉRO saut, AUCUN opérande mémoire indexé — les
       64 tours s'exécutent toujours ; shani-03 : chaque saut nommé sur sa
       condition PUBLIQUE), la concordance au plan (chaque déplacement RIP
       et chaque appel direct == le symbole de shani/layout.py), l'héritage
       byte-identique (les octets scellés de loupe.exe @0xC000-0xC3C0 ==
       les notations tls13-01..04 ré-assemblées) ;
  V2 — L'ÉMULATION, LA DIRECTION SCALAIRE : la composition tls13-01 (scellé)
       → shani-03 (variante) → tls13-04 (scellé) sous Unicorn — la sonde
       NATURELLE rend 0 (le modèle qemu64 n'a pas SHA — le repli vécu SANS
       intervention), les vecteurs FIPS au fichier virtuel de la mémoire,
       le corpus, l'invariance de découpage, ET LE ROUTAGE NOMMÉ : le
       compteur d'instructions PROUVE que le verdict 0 exécute LE SCELLÉ
       (0xC080) et JAMAIS la variante ; le verdict 1 forcé (sonde
       neutralisée en copie de laboratoire) ROUTE à 0xD080 — l'émulateur
       y meurt sur sha256rnds2 (invalide sous qemu64) : LA PREUVE du
       routage dans les DEUX sens ;
  V3 — LE NATIF, LES DEUX DIRECTIONS : sur le CPU SHA-NI du laboratoire —
       la sonde réelle (rax = 1, recroisé aux drapeaux /proc/cpuinfo), les
       QUATRE vecteurs dorés FIPS 180-4 aux TROIS compositions (scellée ;
       variante dispatch réel → chemin SHA-NI ; variante dispatch FORCÉ
       scalaire — la sonde neutralisée `xor eax,eax; ret` en copie de
       laboratoire : le repli exercé sur machine SHA-NI), l'égalité
       scalaire/SHA-NI sur corpus aléatoire (1 000 tampons aux bords), le
       point zéro N=0, l'invariance de découpage ;
  V4 — LA MESURE AVANT/APRÈS (l'entrée OPT-01) : compositions COMPLÈTES
       init+absorb+final sur 8 Mio, la MÊME entrée, la MÊME machine, le
       condensé VÉRIFIÉ à hashlib AVANT comptage (chaque répétition — une
       répétition au condensé faux ABORTE la mesure), 15 répétitions par
       bras, la médiane et l'IQR des cycles RDTSC, le rapport cycles/octet
       et le facteur du gain ;
  V5 — LES SCELLÉS INTACTS : sha256 des QUATRE pièces avant == après ; le
       garde sceau-I 14/14 arbres VERTS ;
  V6 — LE REFUS R11 (la règle à l'envers) : le dossier du hot path
       CONSIGNED AVANT la notation — mesure_hotpath.txt existe, porte les
       empreintes des scellés, la part 98,11 % de tls13-02, et son
       horodatage précède celui de la première notation shani (le constat
       d'ORDRE sur les heures des fichiers).

LA PIÈCE CONSIGNÉE : preuves_v150/shani/rapport_verification.txt + les CSV
(verdicts, mesures). Aucun scellé touché — la variante vit en copies de
laboratoire ; la cérémonie et le run terrain appartiennent au développeur.

Usage : python3 scripts/verifier_shani_v150.py
"""

from __future__ import annotations

import csv
import datetime as _dt
import ctypes
import hashlib
import importlib.util
import mmap
import os
import random
import struct
import subprocess
import sys
import time

TRIADE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PREUVES = os.path.join(TRIADE, "scripts", "preuves_v150", "shani")
SHANI = os.path.join(TRIADE, "shani")

from keystone import Ks, KS_ARCH_X86, KS_MODE_64  # noqa: E402
import capstone  # noqa: E402
from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE  # noqa: E402
from unicorn.x86_const import (UC_X86_REG_RAX, UC_X86_REG_RBX,  # noqa: E402
                               UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8,
                               UC_X86_REG_RIP, UC_X86_REG_RSP)

KS = Ks(KS_ARCH_X86, KS_MODE_64)
CS = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

# les plans par chemin nominatif (D158 : jamais d'import anonyme)
_spec_l = importlib.util.spec_from_file_location(
    "layout_shani", os.path.join(SHANI, "layout.py"))
LSH = importlib.util.module_from_spec(_spec_l)
_spec_l.loader.exec_module(LSH)
_spec_lt = importlib.util.spec_from_file_location(
    "layout_tls13", os.path.join(TRIADE, "tls13", "layout.py"))
LT = importlib.util.module_from_spec(_spec_lt)
_spec_lt.loader.exec_module(LT)

GRAINE = 20261112
TAILLE_MESURE = 8 * 1024 * 1024      # 8 Mio — la même entrée aux deux bras
REPETITIONS = 15

SCELLES = [
    ("loupe.exe", os.path.join(TRIADE, "loupe", "loupe.exe"),
     "c111510535767a40b0122d4e42261c9d8e1ec10d94d95ef666fd76ceb93e61d1"),
    ("proxy.exe", os.path.join(TRIADE, "tls13", "proxy.exe"),
     "446279f3ab356900870cc3b3e1700654a4216ec0b264172340e453db3b00d93d"),
    ("demo.exe", os.path.join(TRIADE, "demo", "demo.exe"),
     "df8f2e50949b14c072f139013a6166a041e573e49b6872d826958f522495e4af"),
    ("selftest.exe", os.path.join(TRIADE, "m1", "selftest.exe"),
     "8038585b7af83c9fe5e6fdccd197e67888b9e5fb09d8d6c84cb998c684bff3c0"),
]

VECTEURS_FIPS = [
    ("le vide", b"",
     "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    ("« abc »", b"abc",
     "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"),
    ("les 448 bits",
     b"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq",
     "248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1"),
    ("les 896 bits",
     b"abcdefghbcdefghicdefghijdefghijkefghijklfghijklmghijklmnhijklmno"
     b"ijklmnopjklmnopqklmnopqrlmnopqrsmnopqrstnopqrstu",
     "cf5b16a778af8380036ce59e7b0492370b249b11e8f07a51afac45037afee9d1"),
]

REUSSITES: list[tuple[str, str]] = []
ECHECS: list[tuple[str, str]] = []


def controle(nom: str, ok: bool, detail: str) -> None:
    marque = "VERT" if ok else "ÉCHEC"
    print(f"  [{marque}] {nom} — {detail}")
    (REUSSITES if ok else ECHECS).append((nom, detail))


def section(titre: str) -> None:
    print(f"\n--- {titre} ---")


# --- la lecture des notations (le lecteur canonique — keystone, rien d'autre) -----

def lire_notation(chemin: str):
    """La notation explicite : lignes d'instructions aux adresses courantes,
    l'en-tête documenté (les cibles RIP, les appels) — rend (octets, lignes,
    métadonnées de l'en-tête, rva). Le code EST PADDÉ au slot (NOP 0x90 —
    la convention D8 : le scellé vit au slot complet, jamais au code nu)."""
    lignes_doc, corps = [], []
    with open(chemin, encoding="utf-8") as f:
        for brut in f.read().splitlines():
            if brut.startswith(";"):
                lignes_doc.append(brut)
                continue
            ligne = brut.split(";")[0].strip()
            if ligne:
                corps.append(ligne)
    rva, slot = None, None
    for l in lignes_doc:
        if "slot RVA" in l:
            bout = l.split("slot RVA ")[1].split(",")[0]
            rva = int(bout, 16)
        if "taille" in l and "octets" in l and "slot RVA" in l:
            slot = int(l.split("taille ")[1].split(" octets")[0])
    adresse = rva
    octets = b""
    for ligne in corps:
        enc, _ = KS.asm(ligne, adresse)
        octets += bytes(enc)
        adresse += len(enc)
    if slot is not None and len(octets) < slot:
        octets += b"\x90" * (slot - len(octets))
    return octets, corps, lignes_doc, rva


def roundtrip(octets: bytes, rva: int) -> tuple[bool, int, int]:
    """keystone → capstone → keystone : chaque instruction ré-assemblée de
    SA transcription capstone doit rendre SES octets (K1 du rejeu)."""
    ok, n, adresse = True, 0, rva
    for ins in CS.disasm(octets, rva):
        texte = f"{ins.mnemonic} {ins.op_str}".strip()
        enc, _ = KS.asm(texte, ins.address)
        if bytes(enc) != ins.bytes:
            ok = False
        n += 1
        adresse += len(ins.bytes)
    return ok, n, adresse - rva


# --- l'extraction des octets scellés (le miroir du harnais) -----------------------

def extraire_section(donnees: bytes, rva: int, taille: int) -> bytes:
    e = struct.unpack_from("<I", donnees, 0x3C)[0]
    nb = struct.unpack_from("<H", donnees, e + 6)[0]
    opt = struct.unpack_from("<H", donnees, e + 20)[0]
    for i in range(nb):
        o = e + 24 + opt + i * 40
        va, = struct.unpack_from("<I", donnees, o + 12)
        vs, = struct.unpack_from("<I", donnees, o + 8)
        ra, = struct.unpack_from("<I", donnees, o + 20)
        if va <= rva < va + vs:
            raw = ra + (rva - va)
            return donnees[raw:raw + taille]
    raise ValueError(f"RVA {rva:#x} introuvable")


# --- l'exécutif natif (mmap exécutable + trampolines SysV→msx64) ------------------

class Natif:
    """L'image posée aux RVA du plan dans une page exécutable : l'héritage
    scellé (extrait de loupe.exe), les notations shani assemblées, la table
    K du scellé, le masque — les blocs appelés par trampoline msx64."""

    # LE TRAMPOLINE SysV→msx64, ASSEMBLÉ PAR KEYSTONE à l'import (jamais un
    # octet gravé de tête — la leçon du paquet : « 4C 89 D0 » hand-derivé
    # était « mov rax, r10 », un octet de REX et la carte segfaultait) :
    # mov r8,rdx ; mov rdx,rsi ; mov rcx,rdi ; mov rax,imm64 (patché) ;
    # jmp rax — l'imm64 vit à l'offset 11 du gabarit
    _enc, _ = KS.asm("mov r8, rdx\nmov rdx, rsi\nmov rcx, rdi\n"
                     "mov rax, 0x1122334455667788\njmp rax")
    TAMPON_SYSV = bytes(_enc)
    _enc2, _ = KS.asm("lfence\nrdtsc\nshl rdx, 32\nor rax, rdx\nret")
    RDTSC = bytes(_enc2)
    IMM64_OFFSET = 11           # la position de l'imm64 dans TAMPON_SYSV

    def __init__(self, base_img: int = 0x1000, taille_img: int = 0x1F000):
        # la carte : base_img d'alignement de page PUIS l'espace RVA — tout
        # accès vit en OFFSET (base_img + rva) de la carte, sans exception
        self.base_img = base_img
        self.mem = mmap.mmap(-1, base_img + taille_img + 0x1000,
                             prot=mmap.PROT_READ | mmap.PROT_WRITE
                             | mmap.PROT_EXEC)
        self.base = ctypes.addressof(ctypes.c_char.from_buffer(self.mem))
        self.img = self.base + base_img
        self.cur_trampo = 0x1F100       # les trampolines au sommet de la carte
        self._cache_trampo: dict[int, int] = {}
        self.fn3 = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.c_void_p,
                                    ctypes.c_void_p, ctypes.c_void_p)

    def pose(self, rva: int, donnees: bytes) -> None:
        """Pose les octets À LEUR RVA dans l'image (l'offset de la carte =
        base_img + rva — la convention UNIQUE, jamais d'accès décalé)."""
        o = self.base_img + rva
        self.mem[o:o + len(donnees)] = donnees

    def trampoline(self, cible_rva: int) -> int:
        """UN trampoline PAR CIBLE, CACHÉ (jamais un par appel — la carte
        n'est pas infinie et le lecteur rdtsc vit au sommet) : au plus
        SEPT trampolines vivent, un par bloc appelé."""
        if cible_rva in self._cache_trampo:
            return self._cache_trampo[cible_rva]
        gabarit = bytearray(self.TAMPON_SYSV)
        struct.pack_into("<Q", gabarit, self.IMM64_OFFSET,
                         self.img + cible_rva)
        o = self.base_img + self.cur_trampo
        adr = self.base + o
        self.mem[o:o + len(gabarit)] = gabarit
        # le gabarit mesure 21 o — le pas de 32 évite TOUT chevauchement
        # (un pas de 16 laissait le trampoline suivant ÉCRASER l'imm64 du
        # précédent : la cache servait alors une cible corrompue)
        self.cur_trampo += 32
        self._cache_trampo[cible_rva] = adr
        return adr

    def appeler3(self, cible_rva: int, a1, a2, a3):
        return ctypes.cast(self.trampoline(cible_rva), self.fn3)(a1, a2, a3)


# --- les compositions (les opérations COMPLÈTES init+absorb+final) ---------------

class Compositions:
    """Trois compositions : scellée (tls13-01/03/04 — L'AVANT), variante
    (tls13-01 + shani-03 + tls13-04 — L'APRÈS tel que dispatché), et la
    variante à sonde neutralisée (le repli FORCÉ sur machine SHA-NI).
    Les données d'entrée vivent dans LEUR PROPRE carte (les blocs prennent
    des POINTEURS — aucune contrainte d'image : le corpus aux bords comme
    le tampon de mesure de 8 Mio)."""

    TAILLE_DONNEES = 16 * 1024 * 1024   # le corpus (65 537) et la mesure (8 Mio)

    def __init__(self, natif: Natif, heritages: dict, shani: dict):
        self.n = natif
        self.TLS01, self.TLS03, self.TLS04 = (LSH.R_TLS01, LSH.R_TLS03,
                                              LSH.R_TLS04)
        self.SHANI03 = LSH.SHANI03_VA
        self.SHANI01 = LSH.SHANI01_VA
        self.ctx = natif.img + 0x18000          # un contexte de 112 o
        self.sortie = natif.img + 0x18100       # 32 o
        self.donnees_mem = mmap.mmap(-1, self.TAILLE_DONNEES,
                                     prot=mmap.PROT_READ | mmap.PROT_WRITE)
        self.donnees_adr = ctypes.addressof(
            ctypes.c_char.from_buffer(self.donnees_mem))

    def _init(self):
        self.n.appeler3(self.TLS01, self.ctx, 0, 0)

    def _absorbe(self, ptr, n, variante: bool):
        cible = self.SHANI03 if variante else self.TLS03
        return self.n.appeler3(cible, self.ctx, ptr, n)

    def _finalise(self):
        return self.n.appeler3(self.TLS04, self.ctx, self.sortie, 0)

    def _lire_sortie(self) -> bytes:
        o = self.n.base_img + 0x18100
        return bytes(self.n.mem[o:o + 32])

    def condense(self, donnees: bytes, variante: bool) -> bytes:
        self.donnees_mem[0:len(donnees)] = donnees
        self._init()
        r = self._absorbe(self.donnees_adr, len(donnees), variante)
        assert r == 0, f"absorption rax={r}"
        r = self._finalise()
        assert r == 0, f"finalisation rax={r}"
        return self._lire_sortie()

    def condense_morcele(self, donnees: bytes, morceaux, variante: bool) -> bytes:
        self.donnees_mem[0:len(donnees)] = donnees
        self._init()
        pos = 0
        for m in morceaux:
            r = self._absorbe(self.donnees_adr + pos, m, variante)
            assert r == 0
            pos += m
        assert pos == len(donnees)
        r = self._finalise()
        assert r == 0
        return self._lire_sortie()


# --- V2 : l'émulation Unicorn (la direction scalaire naturelle) -------------------

class EmulationScalaire:
    """La composition variante sous Unicorn : la sonde NATURELLE (le modèle
    qemu64 sans SHA rend 0 — le repli vécu), le compteur d'instructions
    PROUVANT quel bloc s'exécute, et le routage forcé dans les deux sens."""

    RET_MAGIQUE = 0x13E00
    PILE = 0x7F000000

    def __init__(self, heritages: dict, shani: dict):
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        self.uc.mem_map(0x1000, 0x1F000)
        self.uc.mem_map(self.PILE, 0x10000)
        self.uc.mem_write(LSH.R_K, heritages["K"])
        self.uc.mem_write(LSH.R_MASQUE, LSH.MASQUE_BE)
        for nom, rva in (("tls13-01", LSH.R_TLS01), ("tls13-02", LSH.R_TLS02),
                         ("tls13-03", LSH.R_TLS03), ("tls13-04", LSH.R_TLS04)):
            self.uc.mem_write(rva, heritages[nom])
        self.uc.mem_write(LSH.SHANI01_VA, shani["shani-01-sonde"])
        self.uc.mem_write(LSH.SHANI02_VA, shani["shani-02-comprimer"])
        self.uc.mem_write(LSH.SHANI03_VA, shani["shani-03-absorber"])
        self.compte = {"scelle": 0, "variante": 0, "sonde": 0}
        self.uc.hook_add(UC_HOOK_CODE, self._compter)

    def _compter(self, uc, adresse, taille, donnees):
        if LSH.R_TLS02 <= adresse < LSH.R_TLS02 + 0x1C0:
            if adresse == LSH.R_TLS02:
                self.compte["scelle"] += 1
        elif LSH.SHANI02_VA <= adresse < LSH.SHANI02_VA + 0x380:
            if adresse == LSH.SHANI02_VA:
                self.compte["variante"] += 1
        elif adresse == LSH.SHANI01_VA:
            self.compte["sonde"] += 1

    def appeler(self, va, rcx=0, rdx=0, r8=0):
        uc = self.uc
        uc.reg_write(UC_X86_REG_RAX, 0)
        uc.reg_write(UC_X86_REG_RCX, rcx)
        uc.reg_write(UC_X86_REG_RDX, rdx)
        uc.reg_write(UC_X86_REG_R8, r8)
        uc.reg_write(UC_X86_REG_RSP, 0x7F008000)
        uc.mem_write(0x7F008000, struct.pack("<Q", self.RET_MAGIQUE))
        uc.emu_start(va, self.RET_MAGIQUE, count=500_000_000)
        return uc.reg_read(UC_X86_REG_RAX)


# --- LE PROGRAMME -----------------------------------------------------------------

def main() -> int:
    os.makedirs(PREUVES, exist_ok=True)
    horodatage = _dt.datetime.now(_dt.timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%SZ")
    print("=== scripts/verifier_shani_v150.py — LE VÉRIFICATEUR DU PAQUET 6/6 "
          f"(graine {GRAINE}) ===")
    print(f"horodatage : {horodatage}")

    empreintes = {}
    for nom, chemin, attendu in SCELLES:
        donnees = open(chemin, "rb").read()
        empreintes[nom] = hashlib.sha256(donnees).hexdigest()
        assert empreintes[nom] == attendu, f"{nom} a divergé AVANT le paquet !"

    donnees_loupe = open(os.path.join(TRIADE, "loupe", "loupe.exe"), "rb").read()

    # L'HÉRITAGE : les octets scellés extraits de loupe.exe (la source —
    # jamais les notations seules : les octets DÉPLOYÉS)
    heritages = {
        "tls13-01": extraire_section(donnees_loupe, LSH.R_TLS01, 0x80),
        "tls13-02": extraire_section(donnees_loupe, LSH.R_TLS02, 0x1C0),
        "tls13-03": extraire_section(donnees_loupe, LSH.R_TLS03, 0xC0),
        "tls13-04": extraire_section(donnees_loupe, LSH.R_TLS04, 0xC0),
        "K": extraire_section(donnees_loupe, LSH.R_K, 256),
    }
    assert struct.unpack("<64I", heritages["K"]) == tuple(LT.K), \
        "la table K du scellé ≠ les constantes du plan tls13"

    # LES NOTATIONS SHANI assemblées
    shani = {}
    for nom in ("shani-01-sonde", "shani-02-comprimer", "shani-03-absorber"):
        chemin = os.path.join(SHANI, "notation", nom + ".asm")
        octets, corps, doc, rva = lire_notation(chemin)
        shani[nom] = octets

    # ============================== V1 — LA NOTATION ==========================
    section("V1 — la notation : round-trip, temps constant structurel, "
            "concordance au plan, héritage")

    ok_rt, total_ins = True, 0
    for nom, rva, slot in (("shani-01-sonde", LSH.SHANI01_VA, 0x40),
                           ("shani-02-comprimer", LSH.SHANI02_VA, 0x380),
                           ("shani-03-absorber", LSH.SHANI03_VA, 0xC0)):
        octets = shani[nom]
        ok, n, taille = roundtrip(octets, rva)
        ok_rt &= ok and (rva + taille <= rva + slot)
        total_ins += n
        print(f"    {nom:22} {n:3} instructions · {taille} o / slot "
              f"{slot:#x} · round-trip {'OK' if ok else 'ÉCHEC'}")
    controle("V1.a:round-trip-100-pourcent", ok_rt,
             f"{total_ins} instructions ré-assemblées de leur transcription "
             "capstone — octet pour octet (K1 du rejeu)")

    # LE TEMPS CONSTANT STRUCTUREL : shani-02 — ZÉRO saut, AUCUN opérande
    # mémoire indexé ; shani-03 — chaque saut conditionnel précédé d'un
    # test/compare sur un registre PUBLIC (la longueur, le complément, le
    # verdict CPU — jamais une donnée absorbée)
    ins02 = list(CS.disasm(shani["shani-02-comprimer"], LSH.SHANI02_VA))
    sauts02 = [i for i in ins02 if i.mnemonic.startswith("j")
               or i.mnemonic.startswith("loop") or i.mnemonic == "call"]
    ok_mem = True
    for i in ins02:
        if "[" not in i.op_str:
            continue
        for operande in i.op_str.split("[")[1:]:
            # le registre de BASE : le premier jeton du contenu du crochet
            base = operande.split("]")[0].strip().split()[0].rstrip("+").rstrip("-")
            if base not in ("rcx", "rdx", "rip", "rsp"):
                ok_mem = False
    controle("V1.b:temps-constant-shani-02",
             len(sauts02) == 0 and ok_mem,
             f"zéro saut et zéro appel dans le corps ({len(ins02)} "
             "instructions) ; tout accès mémoire à déplacement fixe "
             "(rcx le contexte, rdx le bloc, rip les constantes du plan, "
             "rsp la crémaillère) — les 64 tours s'exécutent TOUJOURS, "
             "aucune adresse ne lit les données")
    ins03 = list(CS.disasm(shani["shani-03-absorber"], LSH.SHANI03_VA))
    # chaque saut CONDITIONNEL : l'instruction test/cmp qui le précède ne
    # cite QUE des registres publics (r13 N, rbp complément, r15 verdict)
    ok_j03, detail_j03 = True, []
    for k, i in enumerate(ins03):
        if not (i.mnemonic.startswith("j") and i.mnemonic != "jmp"):
            continue
        prev = ins03[k - 1]
        if prev.mnemonic not in ("test", "cmp"):
            ok_j03 = False
            detail_j03.append(f"{i.mnemonic} sans test/cmp")
            continue
        registres = {t for t in prev.op_str.replace(",", " ").split()
                     if t.startswith("r")}
        publics = {"r13", "rbp", "r15", "rsp"}
        if not registres <= publics:
            ok_j03 = False
            detail_j03.append(f"{i.mnemonic} ← {prev.mnemonic} {prev.op_str} "
                              "(registres non publics)")
        else:
            detail_j03.append(f"{i.mnemonic} ← {prev.mnemonic} {prev.op_str}")
    n_cond = sum(1 for i in ins03 if i.mnemonic.startswith("j")
                 and i.mnemonic != "jmp")
    controle("V1.c:sauts-publics-shani-03", ok_j03 and n_cond == 3,
             f"les {n_cond} sauts conditionnels, chacun précédé de son test "
             "sur registre PUBLIC (r13 la longueur N, rbp le complément au "
             "tampon, r15 le verdict CPU — jamais une donnée absorbée) : "
             + " ; ".join(detail_j03))

    # LA CONCORDANCE AU PLAN : chaque appel direct == le symbole du plan
    appels = [f"{i.mnemonic} {i.op_str}" for i in ins03
              if i.mnemonic == "call"]
    attendus = [f"call {LSH.SHANI01_VA:#x}", f"call {LSH.SHANI02_VA:#x}",
                f"call {LSH.R_TLS02:#x}"]
    controle("V1.d:concordance-appels-au-plan",
             sorted(appels) == sorted(attendus),
             f"les TROIS appels directs == le plan (la sonde 0x"
             f"{LSH.SHANI01_VA:x}, la variante 0x{LSH.SHANI02_VA:x}, LE "
             f"SCELLÉ 0x{LSH.R_TLS02:x} — R7) ; trouvés : "
             + ", ".join(sorted(appels)))
    # les déplacements RIP de shani-02 == le masque et les 16 groupes K
    rips = []
    for i in ins02:
        if "rip" in i.op_str:
            for m in (f"[rip + 0x", f"[rip - 0x"):
                if m in i.op_str:
                    bout = i.op_str.split(m)[1].split("]")[0]
                    disp = int(bout, 16) * (1 if "+" in m else -1)
                    rips.append(i.address + i.size + disp)
    ok_rip = (sorted(set(rips)) == sorted([LSH.R_MASQUE]
                                          + LSH.K_GROUPES))
    controle("V1.e:concordance-rip-au-plan", ok_rip,
             f"les {len(rips)} déplacements RIP visent le masque @0x"
             f"{LSH.R_MASQUE:x} (×4) et les SEIZE groupes de la table K du "
             f"scellé @0x{LSH.R_K:x}+16·g — la source unique, jamais "
             "re-déclarée")

    # L'HÉRITAGE BYTE-IDENTIQUE : les notations tls13 ré-assemblées ==
    # les octets scellés extraits (R7 — la double preuve du harnais, ici
    # re-constatée pour le dossier du paquet)
    ok_h = True
    for nom, rva, slot in (("tls13-01", LT.TLS01_VA, 0x80),
                           ("tls13-02", LT.TLS02_VA, 0x1C0),
                           ("tls13-03", LT.TLS03_VA, 0xC0),
                           ("tls13-04", LT.TLS04_VA, 0xC0)):
        chemin = os.path.join(TRIADE, "tls13", "notation", nom
                              + ("-sha256-init" if nom == "tls13-01"
                                 else "-sha256-comprimer" if nom == "tls13-02"
                                 else "-sha256-absorber" if nom == "tls13-03"
                                 else "-sha256-finaliser") + ".asm")
        octets, _, _, _ = lire_notation(chemin)
        ok_h &= octets == heritages[nom]
    controle("V1.f:heritage-byte-identique", ok_h,
             "tls13-01..04 : les notations ré-assemblées == les octets "
             "extraits du scellé loupe.exe @0xC000-0xC3C0 (R7) — le repli "
             "de la variante appellera CES octets-là")

    # ====================== V2 — L'ÉMULATION (scalaire) =======================
    section("V2 — l'émulation : la direction scalaire NATURELLE + le routage")

    emul = EmulationScalaire(heritages, shani)
    CTX, DONNEES, SORTIE = 0x15000, 0x16000, 0x17000

    def condense_emul(donnees: bytes) -> bytes:
        emul.appeler(LSH.R_TLS01, rcx=CTX)                    # le scellé
        emul.uc.mem_write(DONNEES, donnees)
        r = emul.appeler(LSH.SHANI03_VA, rcx=CTX, rdx=DONNEES,
                         r8=len(donnees))                     # la variante
        assert r == 0
        r = emul.appeler(LSH.R_TLS04, rcx=CTX, rdx=SORTIE)    # le scellé
        assert r == 0
        return bytes(emul.uc.mem_read(SORTIE, 32))

    # la sonde NATURELLE sous qemu64 : le verdict 0
    verdict_emul = emul.appeler(LSH.SHANI01_VA)
    controle("V2.a:la-sonde-naturelle-rend-zero", verdict_emul == 0,
             f"la sonde sous Unicorn (modèle qemu64, sans SHA) rend rax = "
             f"{verdict_emul} — le repli scalaire est le chemin NATUREL de "
             "l'émulation, aucun forçage")

    ok_fips = True
    for nom, message, attendu in VECTEURS_FIPS:
        eu = condense_emul(message)
        ok_fips &= eu.hex() == attendu == hashlib.sha256(message).hexdigest()
    controle("V2.b:fips-au-chemin-scalaire-emule", ok_fips,
             "les QUATRE vecteurs dorés par la composition scellé→variante"
             "(dispatch naturel 0)→scellé == hashlib")

    rng = random.Random(f"{GRAINE}:emul")
    ok_corpus, n_corpus = True, 0
    for i in range(120):
        taille = rng.choice([0, 1, 55, 56, 63, 64, 65, 127, 128, 129,
                             255, 1000, 4096])
        donnees = rng.randbytes(taille)
        ok_corpus &= condense_emul(donnees) == hashlib.sha256(donnees).digest()
        n_corpus += 1
    controle("V2.c:corpus-scalaire-emule", ok_corpus,
             f"{n_corpus} tampons aux bords — la variante AU CHEMIN SCELLÉ "
             "== hashlib octet pour octet")

    # l'invariance de découpage (le miroir de la preuve M9) : 1 000 o =
    # 333 morceaux de 3 + 1 octet — le découpage N'EST JAMAIS une entrée
    rngd = random.Random(f"{GRAINE}:decoupage")
    temoin = rngd.randbytes(1000)
    entiers = condense_emul(temoin)
    emul.appeler(LSH.R_TLS01, rcx=CTX)               # ré-init explicite
    emul.uc.mem_write(DONNEES, temoin)
    for i in range(0, 999, 3):                        # 333 × 3 o = 999
        r = emul.appeler(LSH.SHANI03_VA, rcx=CTX, rdx=DONNEES + i, r8=3)
        assert r == 0
    r = emul.appeler(LSH.SHANI03_VA, rcx=CTX, rdx=DONNEES + 999, r8=1)
    assert r == 0
    r = emul.appeler(LSH.R_TLS04, rcx=CTX, rdx=SORTIE)
    assert r == 0
    dec3 = bytes(emul.uc.mem_read(SORTIE, 32))
    controle("V2.d:invariance-decoupage", entiers == dec3,
             "le témoin de 1 000 o en un appel == par 333 morceaux de 3 "
             "+ 1 octet — l'invariance au chemin variante-scalaire")

    # LE ROUTAGE NOMMÉ : le compteur prouve QUEL bloc s'exécute — le
    # message de 200 o FORCE la compression DANS L'ABSORBEUR (3 blocs
    # pleins : le chemin dispatché, pas le bourrage du finaliseur)
    emul.compte = {"scelle": 0, "variante": 0, "sonde": 0}
    condense_emul(rng.randbytes(200))
    compte0 = dict(emul.compte)
    ok_routage0 = (compte0["scelle"] == 4   # 3 blocs pleins + le bourrage
                   and compte0["variante"] == 0
                   and compte0["sonde"] == 1)
    # le verdict 1 FORCÉ (la sonde neutralisée en copie de labo) : le
    # dispatch ROUTE à la variante — l'émulateur y meurt sur sha256rnds2
    # (invalide sous qemu64), LA MORT NOMMÉE DANS LE SLOT de la variante
    sonde_neutralisee, _ = KS.asm("mov eax, 1\nret", LSH.SHANI01_VA)
    emul.uc.mem_write(LSH.SHANI01_VA, bytes(sonde_neutralisee))
    # LA LEÇON D'INSTRUMENT DE L'ENTRÉE 157 rejouée : unicorn NE RE-TRADUIT
    # PAS un bloc déjà exécuté après mem_write — le cache de traduction est
    # PURGÉ à chaque re-pose (sans cela, la sonde ORIGINALE sert depuis le
    # cache et le verdict forcé n'a JAMAIS lieu)
    emul.uc.ctl_remove_cache(LSH.SHANI01_VA, LSH.SHANI01_VA + 0x40)
    emul.compte = {"scelle": 0, "variante": 0, "sonde": 0}
    mort_dans_la_variante = False
    try:
        condense_emul(rng.randbytes(200))       # ≥ 64 o : la compression
        # DISPATCHÉE vit dans l'absorbeur — si l'on arrive ici, le routage
        # n'a PAS eu lieu (un échec nommé)
    except UcError:
        rip = emul.uc.reg_read(UC_X86_REG_RIP)
        mort_dans_la_variante = (LSH.SHANI02_VA <= rip
                                 < LSH.SHANI02_VA + 0x380)
    controle("V2.e:le-routage-nomme-aux-deux-sens",
             ok_routage0 and mort_dans_la_variante,
             f"verdict 0 (naturel) : {compte0['scelle']} compressions AU "
             f"SCELLÉ (0xC080), 0 à la variante, la sonde appelée UNE fois ; "
             "verdict 1 (forcé, la sonde neutralisée en copie de "
             "laboratoire) : le dispatch ROUTE à la variante — l'émulateur "
             "meurt DANS LE SLOT de shani-02 sur sha256rnds2 (invalide sous "
             "qemu64) : LA PREUVE du routage aux deux sens")

    # ======================= V3 — LE NATIF (deux sens) ========================
    section("V3 — le natif : les deux directions sur le CPU SHA-NI du labo")

    natif = Natif()
    natif.pose(LSH.R_K, heritages["K"])
    natif.pose(LSH.R_MASQUE, LSH.MASQUE_BE)
    for nom, rva in (("tls13-01", LSH.R_TLS01), ("tls13-02", LSH.R_TLS02),
                     ("tls13-03", LSH.R_TLS03), ("tls13-04", LSH.R_TLS04)):
        natif.pose(rva, heritages[nom])
    natif.pose(LSH.SHANI01_VA, shani["shani-01-sonde"])
    natif.pose(LSH.SHANI02_VA, shani["shani-02-comprimer"])
    natif.pose(LSH.SHANI03_VA, shani["shani-03-absorber"])
    natif.pose(0x1F200, Natif.RDTSC)        # le lecteur rdtsc+lfence

    comps = Compositions(natif, heritages, shani)

    # la sonde réelle : rax = 1 (ce CPU a SHA-NI ∧ SSSE3), recroisé aux
    # drapeaux /proc/cpuinfo (le juge indépendant du labo)
    verdict_natif = natif.appeler3(LSH.SHANI01_VA, 0, 0, 0)
    drapeaux = open("/proc/cpuinfo").read()
    ok_drapeaux = (" sha_ni" in drapeaux.split("\n")[0].replace(
        "flags", "", 1) or "sha_ni" in drapeaux) and "ssse3" in drapeaux
    controle("V3.a:la-sonde-reelle-recroisee",
             verdict_natif == 1 and ok_drapeaux,
             f"la sonde native rend rax = {verdict_natif} ; /proc/cpuinfo "
             "porte sha_ni ET ssse3 — le verdict RECROISÉ au système, le "
             "dispatch vivra le chemin SHA-NI sur cette machine")

    # LES FIPS aux TROIS compositions (scellée ; variante réelle → SHA-NI ;
    # variante à sonde neutralisée → repli FORCÉ)
    ok_fips3 = True
    details_fips = []
    for nom, message, attendu in VECTEURS_FIPS:
        eu_scellee = comps.condense(message, variante=False)
        eu_variante = comps.condense(message, variante=True)
        # la sonde neutralisée (copie de labo) : xor eax,eax; ret → verdict 0
        neutre, _ = KS.asm("xor eax, eax\nret", LSH.SHANI01_VA)
        natif.pose(LSH.SHANI01_VA, bytes(neutre))
        eu_forcee = comps.condense(message, variante=True)
        natif.pose(LSH.SHANI01_VA, shani["shani-01-sonde"])
        bon = (eu_scellee == eu_variante == eu_forcee
               == bytes.fromhex(attendu)
               == hashlib.sha256(message).digest())
        ok_fips3 &= bon
        details_fips.append(f"{nom}={'VERT' if bon else 'ÉCHEC'}")
    controle("V3.b:fips-dorés-aux-trois-compositions", ok_fips3,
             "les QUATRE vecteurs × TROIS compositions (scellée ; variante "
             "dispatch réel → SHA-NI ; variante dispatch FORCÉ scalaire — "
             "la sonde neutralisée en copie de laboratoire) == l'attendu "
             "FIPS == hashlib — « dispatch forcé dans les deux sens » : "
             + " · ".join(details_fips))

    # L'ÉGALITÉ scalaire/SHA-NI sur corpus aléatoire (l'exigence)
    rng = random.Random(f"{GRAINE}:corpus")
    bords = [0, 1, 54, 55, 56, 57, 63, 64, 65, 111, 112, 119, 120, 127,
             128, 129, 255, 256, 1000, 4096, 65537]
    ok_eq, n_eq = True, 0
    for i in range(1000):
        taille = bords[i % len(bords)] if i < 2 * len(bords) \
            else rng.randrange(0, 8192)
        donnees = rng.randbytes(taille)
        eu_scellee = comps.condense(donnees, variante=False)
        eu_variante = comps.condense(donnees, variante=True)
        neutre, _ = KS.asm("xor eax, eax\nret", LSH.SHANI01_VA)
        natif.pose(LSH.SHANI01_VA, bytes(neutre))
        eu_forcee = comps.condense(donnees, variante=True)
        natif.pose(LSH.SHANI01_VA, shani["shani-01-sonde"])
        attendu = hashlib.sha256(donnees).digest()
        if not (eu_scellee == eu_variante == eu_forcee == attendu):
            ok_eq = False
            break
        n_eq += 1
    controle("V3.c:egalite-scalaire-shani-corpus", ok_eq,
             f"{n_eq} tampons aléatoires (graine {GRAINE}:corpus, les "
             "longueurs aux bords 0..65 537) : scellée == variante-SHA-NI "
             "== variante-forcée-scalaire == hashlib — l'égalité exigée")

    # l'invariance de découpage au chemin SHA-NI (V3 de la spec shani-03)
    rngd = random.Random(f"{GRAINE}:decoupage-natif")
    temoin = rngd.randbytes(300)
    entiers = comps.condense(temoin, variante=True)
    m3 = comps.condense_morcele(temoin, [3] * 100, variante=True)
    m6364 = comps.condense_morcele(temoin, [63, 64, 65, 63, 45],
                                   variante=True)
    controle("V3.d:invariance-decoupage-shani", entiers == m3 == m6364,
             "le témoin de 300 o : en un appel == par 100 morceaux de 3 == "
             "par 63/64/65/63/45 — au chemin SHA-NI")

    # ================== V4 — LA MESURE AVANT/APRÈS (OPT-01) ===================
    section(f"V4 — la mesure avant/après : {TAILLE_MESURE // 1024 // 1024} Mio, "
            f"{REPETITIONS} répétitions, condensé vérifié avant comptage")

    rng_m = random.Random(f"{GRAINE}:mesure")
    tampon = rng_m.randbytes(TAILLE_MESURE)
    attendu = hashlib.sha256(tampon).digest()
    fn_rdtsc = ctypes.CFUNCTYPE(ctypes.c_uint64)(
        natif.img + 0x1F200)

    # LA VÉRIFICATION AVANT COMPTAGE : chaque bras rend le condensé attendu
    # AVANT la première mesure chronométrée — et CHAQUE répétition
    # re-vérifie (une répétition fausse ABORTE la mesure)
    mesures = {"scellée (l'avant)": [], "variante SHA-NI (l'après)": [],
               "variante forcée scalaire": []}

    def mesurer(variante: bool, cle: str) -> None:
        assert comps.condense(tampon, variante) == attendu, \
            "le condensé du bras ne vérifie PAS — la mesure est refusée"
        for _ in range(REPETITIONS):
            t0 = fn_rdtsc()
            eu = comps.condense(tampon, variante)
            t1 = fn_rdtsc()
            if eu != attendu:
                raise AssertionError("une répétition au condensé faux — "
                                     "la mesure est ABORTÉE (aucun chiffre)")
            mesures[cle].append(t1 - t0)

    mesurer(False, "scellée (l'avant)")
    mesurer(True, "variante SHA-NI (l'après)")
    neutre, _ = KS.asm("xor eax, eax\nret", LSH.SHANI01_VA)
    natif.pose(LSH.SHANI01_VA, bytes(neutre))
    mesurer(True, "variante forcée scalaire")
    natif.pose(LSH.SHANI01_VA, shani["shani-01-sonde"])

    def stats(valeurs):
        s = sorted(valeurs)
        med = s[len(s) // 2]
        q1, q3 = s[len(s) // 4], s[3 * len(s) // 4]
        return med, q1, q3

    lignes_mesures = []
    rapport = {}
    for cle, vals in mesures.items():
        med, q1, q3 = stats(vals)
        cpo = med / TAILLE_MESURE
        rapport[cle] = (med, q1, q3, cpo)
        lignes_mesures.append({"bras": cle, "median_cycles": med,
                               "q1_cycles": q1, "q3_cycles": q3,
                               "cycles_par_octet": round(cpo, 4),
                               "repetitions": len(vals)})
        print(f"    {cle:28} médiane {med:>13,} cycles "
              f"[IQR {q1:,}..{q3:,}] · {cpo:.3f} cycles/o")
    facteur = rapport["scellée (l'avant)"][0] / \
        rapport["variante SHA-NI (l'après)"][0]
    surcharge = rapport["variante forcée scalaire"][0] / \
        rapport["scellée (l'avant)"][0]
    print(f"    → le facteur du gain : {facteur:.2f}× · la surcharge du "
          f"dispatch (sonde+branche) : {surcharge * 100 - 100:+.2f} %")
    med_avant = rapport["scellée (l'avant)"][0]
    med_apres = rapport["variante SHA-NI (l'après)"][0]
    controle("V4.a:mesure-avant-apres",
             facteur > 1.0 and all(len(v) == REPETITIONS
                                   for v in mesures.values()),
             f"l'avant (composition scellée) {med_avant:,} "
             f"cycles médiane ; l'après (variante, dispatch réel SHA-NI) "
             f"{med_apres:,} ; le gain "
             f"{facteur:.2f}× ; la surcharge du dispatch "
             f"{surcharge * 100 - 100:+.2f} % — {REPETITIONS} répétitions "
             "par bras, CHAQUE condensé vérifié à hashlib avant et pendant "
             "le comptage, les opérations COMPLÈTES init+absorb+final")

    chemin_mes = os.path.join(PREUVES, "mesures_avant_apres.csv")
    with open(chemin_mes, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(lignes_mesures[0].keys()))
        w.writeheader()
        w.writerows(lignes_mesures)
    emp_mes = hashlib.sha256(open(chemin_mes, "rb").read()).hexdigest()

    # les valeurs du rapport (extraites AVANT — jamais d'imbrication
    # délicate dans les f-strings)
    (r_av_med, r_av_q1, r_av_q3, r_av_cpo) = rapport["scellée (l'avant)"]
    (r_ap_med, r_ap_q1, r_ap_q3, r_ap_cpo) = rapport["variante SHA-NI (l'après)"]
    (r_fs_med, r_fs_q1, r_fs_q3, r_fs_cpo) = rapport["variante forcée scalaire"]

    # ========================= V5 — LES SCELLÉS INTACTS =======================
    section("V5 — les scellés intacts + le garde sceau-I")
    ok_sc = True
    for nom, chemin, attendu in SCELLES:
        donnees = open(chemin, "rb").read()
        eu = hashlib.sha256(donnees).hexdigest()
        ok_sc &= eu == attendu == empreintes[nom]
    controle("V5.a:les-quatre-scellés-intacts", ok_sc,
             "loupe.exe c1115105… · proxy.exe 446279f3… · demo.exe "
             "df8f2e50… · selftest.exe 8038585b… — identiques AVANT et "
             "APRÈS le paquet (la variante vit en copies de laboratoire)")
    garde = subprocess.run(
        [sys.executable, os.path.join(TRIADE, "v06", "sceau_I.py"),
         "verifier"], capture_output=True, text=True)
    ok_garde = ("14 arbres VERTS" in garde.stdout)
    controle("V5.b:le-garde-sceau-I", ok_garde,
             "les 14 arbres signés VERTS — l'arbre signé n'est pas touché "
             "(aucune cérémonie : elle appartient au développeur)")

    # ======================= V6 — LE DOSSIER R11 (l'ordre) ====================
    section("V6 — le dossier R11 : la mesure consignée AVANT la notation")
    chemin_hot = os.path.join(TRIADE, "scripts", "preuves_v150",
                              "hotpath_shani", "mesure_hotpath.txt")
    hot_existe = os.path.exists(chemin_hot)
    hot_texte = open(chemin_hot).read() if hot_existe else ""
    hot_ok = ("98.11 %" in hot_texte and "tls13-02" in hot_texte
              and "AVANT" in hot_texte)
    hot_mtime = os.path.getmtime(chemin_hot)
    premiere_notation = min(
        os.path.getmtime(os.path.join(SHANI, "notation", n + ".asm"))
        for n in ("shani-01-sonde", "shani-02-comprimer",
                  "shani-03-absorber"))
    controle("V6.a:la-mesure-avant-la-notation",
             hot_ok and hot_mtime < premiere_notation,
             "mesure_hotpath.txt (tls13-02 = 98,11 %, consignée AVANT "
             "l'optimisation) existait et fut écrite AVANT la première "
             "notation shani — l'ordre de R11 constaté sur les heures des "
             "fichiers ; le hot path était MESURÉ avant que le premier "
             "octet de la variante n'existe : l'optimisation n'est PAS "
             "refusée, elle est FONDÉE")

    # ============================ LE RAPPORT ===================================
    total = len(REUSSITES) + len(ECHECS)
    rapport_lignes = [
        "VÉRIFICATION DU PAQUET 6/6 — LA VARIANTE SHA-NI (lfh49a1xf, D205)",
        "==================================================================",
        "",
        f"Horodatage : {horodatage} · graine {GRAINE}",
        f"Instrument : keystone/capstone (round-trip), Unicorn 2.1.4 (la "
        "direction scalaire), le CPU SHA-NI natif du laboratoire (les deux "
        "directions), mmap exécutable + ctypes (l'exécutif natif)",
        "",
        "LES CONTRÔLES :",
    ]
    for nom, detail in REUSSITES:
        rapport_lignes.append(f"  [VERT]   {nom} — {detail}")
    for nom, detail in ECHECS:
        rapport_lignes.append(f"  [ÉCHEC]  {nom} — {detail}")
    rapport_lignes += [
        "",
        "LA MESURE AVANT/APRÈS (l'entrée OPT-01 — les nombres de CE rapport) :",
        f"  l'avant  (composition scellée tls13-01/03/04) : "
        f"{r_av_med:,} cycles médiane ({r_av_cpo:.3f} cycles/o, IQR "
        f"{r_av_q1:,}..{r_av_q3:,})",
        f"  l'après  (variante, dispatch réel SHA-NI)     : "
        f"{r_ap_med:,} cycles médiane ({r_ap_cpo:.3f} cycles/o)",
        f"  la variante à dispatch FORCÉ scalaire         : "
        f"{r_fs_med:,} cycles médiane ({r_fs_cpo:.3f} cycles/o — le repli "
        "exercé sur machine SHA-NI)",
        f"  LE GAIN : {facteur:.2f}× · la surcharge du dispatch : "
        f"{surcharge * 100 - 100:+.2f} %",
        f"  Conditions : {TAILLE_MESURE // 1024 // 1024} Mio de PRNG "
        f"déterministe (graine {GRAINE}:mesure), la MÊME entrée aux deux "
        "bras, la MÊME machine, les opérations COMPLÈTES init+absorb+final, "
        "le condensé VÉRIFIÉ à hashlib avant ET pendant le comptage",
        "",
        f"PIÈCES : mesures_avant_apres.csv (sha256 {emp_mes})",
        "",
        "FRONTIÈRES : les QUATRE pièces scellées INTACTES (sha256 "
        "identiques avant/après) ; le garde sceau-I 14/14 VERT ; la "
        "variante vit en COPIES DE LABORATOIRE aux adresses du plan — "
        "AUCUN scellement, la cérémonie d'ère et le run terrain "
        "appartiennent au développeur ; aucun chiffre fabriqué — tout "
        "nombre est LU d'une pièce ou mesuré devant témoin.",
        "",
        f"BILAN : {total} contrôles — {len(REUSSITES)} VERTS, "
        f"{len(ECHECS)} ÉCHECS",
    ]
    chemin_rap = os.path.join(PREUVES, "rapport_verification.txt")
    with open(chemin_rap, "w") as f:
        f.write("\n".join(rapport_lignes) + "\n")
    emp_rap = hashlib.sha256(open(chemin_rap, "rb").read()).hexdigest()
    print(f"\nPIÈCES : rapport_verification.txt (sha256 {emp_rap[:16]}…)")
    print(f"         mesures_avant_apres.csv (sha256 {emp_mes[:16]}…)")
    if ECHECS:
        for nom, detail in ECHECS:
            print(f"  [ÉCHEC] {nom} — {detail}")
        print("VERDICT : ÉCHEC — le paquet n'est pas prouvé")
        return 1
    print("VERDICT : VERT — la variante SHA-Ni est NOTÉE-PROUVÉE-MESURÉE "
          "sur pièces (les deux directions du dispatch, l'égalité au "
          "corpus, le gain mesuré — l'entrée OPT-01 fondée)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
