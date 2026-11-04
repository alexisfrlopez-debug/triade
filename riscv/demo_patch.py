#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""demo_patch.py — LA BASCULE PENDANT LE TRAFIC, INSTANCE RV64 (chantier M7-(c)).

Le portage du modèle unix/demo_patch.py (M5-(c) refermé sur le profil Linux)
à l'instance riscv : SOUS QEMU le scénario vit DANS l'invité — le
démonstrateur `demo-patch` (f72001, notation/demo-patch.asm, 184
instructions) est _start d'un artefact qui réutilise LES MÊMES blocs du
corpus (la même notation, les mêmes slots, le même staging, la même table
R10, les mêmes fixtures) ; la transcription intégrale EST la pièce (il n'y
a AUCUN détournement de canal — la narration et les émissions vivent sur le
MÊME flux, D153 ne s'applique pas ; l'oracle host-side compare OCTET POUR
OCTET la transcription attendue, construite depuis le plan).

Les pièces du verdict (fail-closed, chacune tranchée binaire) :
  (a) LE TRAFIC EN SESSION, LA BASCULE ENTRE DEUX USAGES : 1 200 usages de
      l'ENTRÉE du journal (0x1840 — la CIBLE du patch) ; l'apply entre les
      usages 399 et 400, le rollback entre 799 et 800 ; chaque usage rend
      son verdict exact (contrôlé SUR PLACE par le démonstrateur : la
      longueur rendue == 8 + len(itoa(i)) + la marque) et la transcription
      est OCTET POUR OCTET l'attendu — 800 lignes v1, 400 lignes v2 (marque
      « j2: »), aucune déchirée, aucune perdue, aucun mélange de formats ;
  (b) L'EFFET AU GESTE MÊME : sous v2 l'entrée appelée rend « j2: verdict »
      (12 o — LE PATCH EST EFFECTIF), au retour « verdict » sans marque
      (8 o) ; le mot d'entrée a basculé (≠ l'original sauvegardé) puis est
      revenu à l'octet près (== ENTREE_SAUVEE) ; le remplaçant DORMANT
      (la croissance habitée, ≠ la réserve ebreak) ; le verrou rendu ;
  (c) LES REFUS NOMMÉS EXERCÉS : mode invalide 1 (2 et -1), états
      incohérents 4 (apply x2, rollback x2), staging absent 2 et somme
      divergente 3 — les deux derniers par mutation IN-GUEST de la table
      R10 (mprotect par le démonstrateur, restaurée après chacun) ;
  (d) LE DEP FALSIFIÉ (0x7→0x3) : le mutant du FICHIER, un run séparé —
      l'exécution FAUTE au retour du mprotect (page sans X) : SIGSEGV ;
  (e) LA FALSIFICATION DU DÉMONSTRATEUR (D154 : l'instrument est
      soupçonnable) : un octet d'opcode corrompu par instruction, jusqu'à
      la déviation — si TOUTES passent silencieusement, l'oracle est VACUE
      et refuse ;
  (f) L'INDIFFÉRENCE À LA BASE : les bases forcées du CHARGEUR (-R/-B+-R),
      la transcription identique à toute base ;
  (g) ZÉRO RÉGRESSION SUR PIÈCES : le FICHIER corpus n'a pas bougé d'un
      octet (sha relu) et son rituel rejoué rend exactement ses deux lignes
      au code 0 — le demo est un INSTRUMENT, le corpus l'artefact.

FRONTIÈRES NOMMÉES : code 5 (le service refuse) n'est pas productible sous
qemu-user de façon naturelle (l'hôte accorde RWX sur mapping privé) — la
branche vit fail-closed dans tcp-07 (bltz → refus5) ; la concurrence réelle
est HORS périmètre (fiche § 5 : le corpus M7 est mono-fil — portée de
fence.i : le cœur courant ; la bascule PENDANT le trafic se démontre EN
SESSION, entre deux usages) ; le demo n'est PAS un artefact de la lignée
(pas de carte — le modèle unix/demo_patch.py).

Usage : python3 riscv/demo_patch.py [--bavard]
Retour : executer() -> (vert, lignes) — appelé par conformite_profil.py.
"""

from __future__ import annotations

import hashlib
import importlib.util
import os
import re
import struct
import subprocess
import sys
import tempfile

ICI = os.path.dirname(os.path.abspath(__file__))
RISCV = ICI
sys.path.insert(0, ICI)
sys.path.insert(0, os.path.join(ICI, "outils"))
sys.path.insert(0, os.path.join(ICI, "notation"))

import layout as L                       # noqa: E402

import capstone                          # noqa: E402
from as_rv64 import EchecAssemblage, assembler  # noqa: E402

CS = capstone.Cs(capstone.CS_ARCH_RISCV, capstone.CS_MODE_RISCV64)
CS.detail = False

_BRANCHES = {"beq", "bne", "blt", "bge", "bltu", "bgeu",
             "beqz", "bnez", "bgez", "bltz", "bgtz", "blez", "j"}

CHEMIN_DEMO = os.path.join(RISCV, "demo")
CHEMIN_CORPUS = os.path.join(RISCV, "corpus")
SHA_CORPUS_ATTENDU = "ec343b4e8bebf21c8b29a6da1a5eb022fb7b8e4b50ce95c5906734ef0b043799"
RITUEL = (b"TRIADE M1 : minilibc 21/21 OK\n"
          b"corpus : autotest 21 vecteurs\n")

N_TRAFIC, K_APPLY, M_ROLLBACK = 1200, 400, 800


class EchecDemo(Exception):
    """Tout refus nommé (fail-closed : jamais un faux vert)."""


def _charger_module(nom: str, chemin: str):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


BC = _charger_module("build_corpus_demo", os.path.join(RISCV, "build_corpus.py"))


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# ---------------------------------------------------------------------------
# L'oracle structurel du démonstrateur (les déclarations PAR BLOC, f72001)
# ---------------------------------------------------------------------------

APPELS_DEMO = {L.A_ECRIRE_CORPUS, L.A_SORTIR, L.A_STRLEN, L.A_ITOA,
               L.A_JOURNAL, L.A_PATCH}       # … + les étiquettes locales
SYSCALLS_DEMO = {L.SYS_MPROTECT}            # .protger_page (l'instrument nommé)
DONNEES_S1_DEMO = {L.R_D_TRAFIC, L.R_D_NL, L.R_D_VERDICT, L.R_D_APPLY,
                   L.R_D_TRAMP, L.R_D_EFFET, L.R_D_ROLLB, L.R_D_V1,
                   L.R_D_PTRAFIC, L.R_D_REST, L.R_D_DORM, L.R_D_VERROU,
                   L.R_D_REFMODE, L.R_D_REFETAT, L.R_D_REFABS, L.R_D_REFSOM,
                   L.R_D_FIN, L.R_D_ECHEC,
                   L.R_TAB_SUM_CORPUS + 4, L.R_TAB_SUM_CORPUS + 8}
DONNEES_S2_DEMO = {L.VERROU_REL, L.ETAT_REL, L.ENTREE_SAUVEE_REL,
                   L.DEMO_SCRATCH_REL}
DONNEES_S9_DEMO = {0, L.CROISSANCE_REL}

_RE_MEM = re.compile(r"^(-?(?:0x[0-9a-f]+|\d+))\((\w+)\)$")


def _nombre(s: str) -> int:
    return int(s, 0)


def _cible_relative(insn) -> int | None:
    if insn.mnemonic in _BRANCHES or insn.mnemonic == "jal":
        return insn.address + _nombre(insn.op_str.split(",")[-1].strip())
    return None


def oracle_demo(drv: dict) -> list[str]:
    """Le contrat du démonstrateur sur le code désassemblé (le modèle de
    l'oracle du corpus — les déclarations PAR BLOC, la garde anti-table-x86,
    l'anti-C, les fenêtres, t1/s3 jamais touchés)."""
    verrous = []

    def verrou(nom, condition, detail=""):
        if not condition:
            raise EchecDemo(f"oracle demo : {nom} {detail}")
        verrous.append(nom)

    insns = drv["insns"]
    labels = drv["labels"]
    adresses = {i.address for i in insns}
    locaux = set(labels.values())
    nr = None
    for i in insns:
        verrou(f"taille-4@{i.address:#x}", i.size == 4, f"taille {i.size} (anti-C)")
        if i.mnemonic in _BRANCHES:
            cible = _cible_relative(i)
            verrou(f"saut-interne@{i.address:#x}", cible in adresses,
                   f"cible {cible:#x} hors frontière du bloc")
        if i.mnemonic == "jal":
            if "," in i.op_str:
                raise EchecDemo(f"appel@{i.address:#x} : jal hors forme d'appel "
                                f"({i.op_str!r} — le lien vit dans ra)")
            cible = _cible_relative(i)
            verrou(f"appel-autorise@{i.address:#x}",
                   cible in APPELS_DEMO | locaux, f"cible {cible:#x} hors blocs déclarés")
        if i.mnemonic.startswith("jalr"):
            verrou(f"ret-seul@{i.address:#x}", i.mnemonic == "ret",
                   f"jalr indirect : {i.mnemonic} {i.op_str}")
        if i.mnemonic == "addi" and i.op_str.startswith("a7,"):
            try:
                nr = _nombre(i.op_str.split(",")[2].strip())
            except (ValueError, IndexError):
                nr = None
        if i.mnemonic == "ecall":
            if nr in L.TABLE_X86_REFUSEE:
                raise EchecDemo(
                    f"syscall-x86@{i.address:#x} : a7={nr} est le numéro x86-64 "
                    f"de « {L.TABLE_X86_REFUSEE[nr]} » — REFUS NOMMÉ (garde "
                    f"anti-table-x86)")
            verrou(f"syscall-autorise@{i.address:#x}",
                   nr in SYSCALLS_DEMO, f"a7={nr} non déclaré (226 seul — "
                   "l'ouverture des pages de la table)")
        ops = [o.strip() for o in i.op_str.split(",")] if i.op_str else []
        for o in ops:
            m = _RE_MEM.match(o)
            if m:
                imm, base = _nombre(m.group(1)), m.group(2)
                if base == "s1":
                    verrou(f"s1-declaree@{i.address:#x}", imm in DONNEES_S1_DEMO,
                           f"s1+{imm:#x} hors données déclarées")
                elif base == "s2":
                    verrou(f"s2-declaree@{i.address:#x}", imm in DONNEES_S2_DEMO,
                           f"s2+{imm:#x} hors .bss déclarée")
                elif base == "s9":
                    verrou(f"s9-declaree@{i.address:#x}", imm in DONNEES_S9_DEMO,
                           f"s9+{imm:#x} hors fenêtre inspection déclarée")
    # t1 (fiche § 2 : le registre de travail du projet — la discipline de la
    # lignée) et s3 (D156 : la fenêtre PRIVÉE de tcp-07) : JAMAIS touchés
    for i in insns:
        ops = i.op_str.replace("(", ", ").replace(")", "").split(", ")
        verrou(f"t1-s3-respectes@{i.address:#x}",
               "t1" not in [o.strip() for o in ops]
               and "s3" not in [o.strip() for o in ops],
               f"t1/s3 touché : {i.mnemonic} {i.op_str}")
    # les paires d'ancres re-vérifiées DEPUIS LE CODE
    attendues = [(insns[0], "s1", L.ANCRE_D_RODATA, L.CIBLE_D_RODATA),
                 (insns[2], "s2", L.ANCRE_D_BSS, L.CIBLE_D_BSS),
                 (insns[4], "s9", L.ANCRE_D_ENTREE, L.CIBLE_D_ENTREE)]
    for insn_a, reg, site, cible in attendues:
        verrou(f"ancre-{reg}-site", insn_a.address == site,
               f"l'auipc {reg} à {insn_a.address:#x}, le plan déclare {site:#x}")
        hi = (insn_a.op_str.split(", ")[1])
        hi = _nombre(hi) - 0x100000 if _nombre(hi) >= 0x80000 else _nombre(hi)
        idx = insns.index(insn_a)
        insn_i = insns[idx + 1]
        # le LO==0 se canonicalise en « mv reg, reg » (la graphie du juge —
        # l'encodage est le MÊME addi-0 ; le LO se lit alors 0)
        if insn_i.mnemonic == "mv" and insn_i.op_str == f"{reg}, {reg}":
            lo = 0
            forme = True
        else:
            forme = (insn_i.mnemonic == "addi" and
                     insn_i.op_str.startswith(f"{reg}, {reg}, "))
            lo = _nombre(insn_i.op_str.split(", ")[2]) if forme else None
        verrou(f"ancre-{reg}-paire", forme,
               "l'addi de la paire n'est pas adjacent à son auipc "
               "(ou mv si LO==0 — la graphie du juge)")
        verrou(f"ancre-{reg}-arithmetique",
               site + hi * 4096 + lo == cible,
               f"{site:#x} + {hi:#x}*4096 + {lo} != {cible:#x}")
    # _start : le corps ne touche JAMAIS sp — la SEULE écriture de pile vit
    # dans le cadre de .dire (la leçon sr-04 : jal écrase le lien — .dire
    # appelle écrire, il SAUVE ra ; apparié -16/+16, ordonné, dans SA zone)
    zone_dire = (labels.get("dire", 0),
                 labels.get("protger_page", 1 << 60))
    ecritures_sp = [i for i in insns if i.mnemonic == "addi" and
                    i.op_str.replace(" ", "").startswith("sp,sp,")]
    verrou("corps-sans-pile",
           all(zone_dire[0] <= i.address < zone_dire[1] for i in ecritures_sp),
           "les écritures de sp vivent DANS .dire (le corps ne touche jamais sp)")
    imm_sp = sorted(_nombre(i.op_str.split(",")[2]) for i in ecritures_sp)
    verrou("cadre-dire-apparieé",
           imm_sp == [-16, 16] and len(ecritures_sp) == 2,
           f"écritures sp : {[i.op_str for i in ecritures_sp]}")
    seq = [i.mnemonic + "|" + i.op_str for i in insns
           if zone_dire[0] <= i.address < zone_dire[1]]
    try:
        i_sub = next(k for k, s in enumerate(seq)
                     if s.startswith("addi|sp, sp, -"))
        i_sd = next(k for k, s in enumerate(seq) if s.startswith("sd|ra, 0(sp)"))
        i_ld = next(k for k, s in enumerate(seq) if s.startswith("ld|ra, 0(sp)"))
        i_add = next(k for k, s in enumerate(seq)
                     if s.startswith("addi|sp, sp, 0x"))
        i_ret = seq.index("ret|")
        verrou("cadre-dire-ordonne", i_sub < i_sd < i_ld < i_add < i_ret,
               f"cadre : -16@{i_sub} sd@{i_sd} ld@{i_ld} +16@{i_add} ret@{i_ret}")
    except StopIteration:
        verrou("cadre-dire-ordonne", False, "le cadre de .dire incomplet")
    verrou("sans-cadre-hors-dire",
           not any(i.mnemonic in ("sd", "ld", "lw", "lwu", "sw")
                   and "(sp)" in i.op_str.replace(" ", "")
                   and not (zone_dire[0] <= i.address < zone_dire[1])
                   for i in insns),
           "aucun accès mémoire en base sp hors du cadre de .dire "
           "(les ld de données via s2/s9 sont légitimes)")
    # padding D8
    fin_code = insns[-1].address + insns[-1].size
    verrou("padding-16", 0x2000 + L.BLOC_DEMO[4] - fin_code >= 16)
    return verrous


# ---------------------------------------------------------------------------
# La construction de l'image du demo (le corpus + le démonstrateur)
# ---------------------------------------------------------------------------

def assembler_demo() -> dict:
    """La notation du démonstrateur -> octets + insns + labels (R5 intégré)."""
    return BC.assembler_bloc(L.BLOC_DEMO[2], L.BLOC_DEMO[3], L.BLOC_DEMO[4])


def composer_demo(code: dict, staging: dict, drv: dict) -> bytes:
    """L'image du demo : le corpus INTÉGRAL (mêmes blocs, même staging, même
    table, mêmes fixtures) + les chaînes du démonstrateur (0x580-0x7BC) +
    le démonstrateur à 0x2000 (la réserve RX y cède la place) + e_entry."""
    seg_r = bytearray(b"\x00" * L.CORPUS_SEG_R_TAILLE)
    seg_rx = bytearray(struct.pack("<I", L.EBREAK) * (L.CORPUS_SEG_RX_TAILLE // 4))
    poses = []

    def poser(seg, base, rva, donnees, nom=""):
        poses.append((rva, rva + len(donnees), nom or hex(rva)))
        if rva + len(donnees) > base + len(seg):
            raise EchecDemo(f"segment débordant à {rva:#x} ({nom})")
        seg[rva - base: rva - base + len(donnees)] = donnees

    # — le segment R : le corpus (fixtures + staging + table) + les chaînes
    fixtures = [
        (L.R_SA, b"TRIADE\0", "SA"), (L.R_SB, b"TRIADE\0", "SB"),
        (L.R_SC, b"TRIADF\0", "SC"), (L.R_SD, b"TRI\0", "SD"),
        (L.R_MOTIF16, bytes(range(16)), "MOTIF16"),
        (L.R_SENT16, b"\xaa" * 16, "SENT16"),
        (L.R_MOTIF33, L.CORPUS_MOTIF33, "MOTIF33"),
        (L.R_ZERO16, b"\x00" * 16, "ZERO16"),
        (L.R_FF33, b"\xff" * 33, "FF33"),
        (L.R_S_VIDE, b"\0", "S_VIDE"),
        (L.R_S_TRIADE, b"TRIADE\0", "S_TRIADE"),
        (L.R_S_33, L.CORPUS_S_33 + b"\0", "S_33"),
        (L.R_I0, b"0\0", "I0"), (L.R_IMAX, b"4294967295\0", "IMAX"),
        (L.R_I123, b"1234567890\0", "I123"), (L.R_I7, b"7\0", "I7"),
        (L.R_SLASH, b"/", "SLASH"),
        (L.R_PREFIXE_M1, L.CORPUS_PREFIXE_M1, "PREFIXE_M1"),
        (L.R_OK, b" OK\n", "OK"), (L.R_KO, b" KO\n", "KO"),
        (L.R_J_PREF, L.CORPUS_J_PREF, "J_PREF"),
        (L.R_J_SUFF, L.CORPUS_J_SUFF, "J_SUFF"),
        (L.R_J2_MARK, L.CORPUS_J2_MARK, "J2_MARK"),
    ]
    for rva, donnees, nom in fixtures:
        poser(seg_r, L.CORPUS_SEG_R_RVA, rva, donnees, nom)
    st_octets, st_taille, st_somme = BC.octets_staging(staging)
    poser(seg_r, L.CORPUS_SEG_R_RVA, L.R_STAGING_CORPUS, st_octets, "STAGING")
    poser(seg_r, L.CORPUS_SEG_R_RVA, L.R_TAB_SUM_CORPUS,
          struct.pack("<IIQIQQ", L.R_STAGING_CORPUS, st_taille,
                      st_somme, 0, 0, 0), "TAB_SUM")
    # les chaînes du démonstrateur (0x580-0x7BC — SOUS la portée s1+imm12)
    chaines = [
        (L.R_D_TRAFIC, L.D_TRAFIC), (L.R_D_NL, L.D_NL),
        (L.R_D_VERDICT, L.D_VERDICT), (L.R_D_APPLY, L.D_APPLY),
        (L.R_D_TRAMP, L.D_TRAMP), (L.R_D_EFFET, L.D_EFFET),
        (L.R_D_ROLLB, L.D_ROLLB), (L.R_D_V1, L.D_V1),
        (L.R_D_PTRAFIC, L.D_PTRAFIC), (L.R_D_REST, L.D_REST),
        (L.R_D_DORM, L.D_DORM), (L.R_D_VERROU, L.D_VERROU),
        (L.R_D_REFMODE, L.D_REFMODE), (L.R_D_REFETAT, L.D_REFETAT),
        (L.R_D_REFABS, L.D_REFABS), (L.R_D_REFSOM, L.D_REFSOM),
        (L.R_D_FIN, L.D_FIN), (L.R_D_ECHEC, L.D_ECHEC),
    ]
    for rva, donnees in chaines:
        poser(seg_r, L.CORPUS_SEG_R_RVA, rva, donnees, f"chaine@{rva:#x}")
    # — le segment RX : les 13 slots du corpus, la croissance DEMEURE ebreak,
    #     le démonstrateur à 0x2000
    for bid, _, _, rva, slot in L.BLOCS_CORPUS:
        poser(seg_rx, L.CORPUS_SEG_RX_RVA, rva, code[bid]["slot"], bid)
    poser(seg_rx, L.CORPUS_SEG_RX_RVA, L.BLOC_DEMO[3], drv["slot"], "f72001")
    # — anti-chevauchement (C1)
    for (d1, f1, n1), (d2, f2, n2) in zip(poses, poses[1:]):
        if d1 < f2 and d2 < f1:
            raise EchecDemo(f"chevauchement : {n1} [{d1:#x},{f1:#x}) / "
                            f"{n2} [{d2:#x},{f2:#x})")
    # — ehdr (ET_DYN, EM_RISCV) + 4 phdr — SEULE e_entry change du corpus
    e_ident = b"\x7fELF" + bytes([2, 1, 1, 0]) + b"\x00" * 8
    ehdr = struct.pack("<16sHHIQQQIHHHHHH", e_ident,
                       3, L.E_MACHINE, 1, L.DEMO_ENTREE,
                       64, 0, L.E_FLAGS,
                       64, 56, 4, 0, 0, 0)
    ph_r = struct.pack("<IIQQQQQQ", 1, 4, L.CORPUS_SEG_R_RVA, L.CORPUS_SEG_R_RVA,
                       L.CORPUS_SEG_R_RVA, L.CORPUS_SEG_R_TAILLE,
                       L.CORPUS_SEG_R_TAILLE, L.TAILLE_PAGE)
    ph_rx = struct.pack("<IIQQQQQQ", 1, 5, L.CORPUS_SEG_RX_RVA, L.CORPUS_SEG_RX_RVA,
                        L.CORPUS_SEG_RX_RVA, L.CORPUS_SEG_RX_TAILLE,
                        L.CORPUS_SEG_RX_TAILLE, L.TAILLE_PAGE)
    ph_rw = struct.pack("<IIQQQQQQ", 1, 6, L.CORPUS_SEG_RW_RVA, L.CORPUS_SEG_RW_RVA,
                        L.CORPUS_SEG_RW_RVA, 0, L.CORPUS_SEG_RW_TAILLE,
                        L.TAILLE_PAGE)
    ph_stack = struct.pack("<IIQQQQQQ", L.PT_GNU_STACK, 6, 0, 0, 0, 0, 0, 0x10)
    seg_r[0:64] = ehdr
    seg_r[64:120] = ph_r
    seg_r[120:176] = ph_rx
    seg_r[176:232] = ph_rw
    seg_r[232:288] = ph_stack
    return bytes(seg_r) + bytes(seg_rx)


def valider_demo(img: bytes, staging: dict, drv: dict) -> list[str]:
    """Relit l'image du demo (le modèle valider_elf du corpus — la même
    discipline, e_entry 0x2000 à la place)."""
    lignes = []
    if len(img) != L.CORPUS_TAILLE_FICHIER:
        raise EchecDemo(f"taille {len(img):#x} != {L.CORPUS_TAILLE_FICHIER:#x}")
    if img[:4] != b"\x7fELF" or img[4] != 2 or img[5] != 1:
        raise EchecDemo("magie ELF64 LE absente")
    e_type, e_machine = struct.unpack_from("<HH", img, 16)
    e_entry = struct.unpack_from("<Q", img, 24)[0]
    if e_type != 3 or e_machine != L.E_MACHINE or e_entry != L.DEMO_ENTREE:
        raise EchecDemo(f"e_type/e_machine/e_entry {e_type}/{e_machine:#x}/"
                        f"{e_entry:#x} != 3/{L.E_MACHINE:#x}/{L.DEMO_ENTREE:#x}")
    loads = []
    for i in range(4):
        p = struct.unpack_from("<IIQQQQQQ", img, 64 + i * 56)
        if p[0] == 1:
            loads.append(p)
        elif p[0] == L.PT_GNU_STACK:
            if p[1] != 6 or p[7] != 0x10:
                raise EchecDemo("PT_GNU_STACK != RW sans X (NX psABI)")
        else:
            raise EchecDemo(f"p_type inattendu {p[0]:#x}")
    if [p[1] for p in loads] != [4, 5, 6]:
        raise EchecDemo(f"PT_LOAD {[p[1] for p in loads]} != R/RX/RW")
    for p in loads:
        if p[1] & 2 and p[1] & 1:
            raise EchecDemo(f"PT_LOAD {p[1]:#x} : W^X rompu")
    if img[L.R_D_TRAFIC:L.R_D_TRAFIC + 7] != L.D_TRAFIC:
        raise EchecDemo("la chaîne TRAFIC divergente du plan")
    for rva, s in ((L.R_D_EFFET, L.D_EFFET), (L.R_D_FIN, L.D_FIN),
                   (L.R_D_ECHEC, L.D_ECHEC)):
        if img[rva:rva + len(s)] != s:
            raise EchecDemo(f"chaîne @ {rva:#x} divergente")
    if img[L.A_CROISSANCE:L.A_CROISSANCE + 16] != struct.pack("<I", L.EBREAK) * 4:
        raise EchecDemo("la croissance n'est pas ebreak à l'état image")
    if img[L.BLOC_DEMO[3]:L.BLOC_DEMO[3] + 8] == struct.pack("<I", L.EBREAK) * 2:
        raise EchecDemo("le démonstrateur absent de son slot")
    lignes.append(f"[demo-elf] {len(img)} o, ET_DYN EM_RISCV, entrée "
                  f"{L.DEMO_ENTREE:#x} RVA, 13 blocs + le démonstrateur "
                  f"({len(drv['octets'])} o), la croissance ebreak, les "
                  f"chaînes 0x580-0x7BC sous la portée s1")
    return lignes


# ---------------------------------------------------------------------------
# L'exécution sous qemu (réserve instrumentale D149 — TCG, syscalls réels)
# ---------------------------------------------------------------------------

def chemin_qemu() -> str:
    return BC.chemin_qemu()


class Terrain:
    def __init__(self, img: bytes, extra: list[str] | None = None):
        self.qemu = chemin_qemu()
        self.extra = extra or []
        self.dossier = tempfile.mkdtemp(prefix="demo-rv-",
                                        dir=os.path.join(RISCV, ".tmp"))
        os.makedirs(self.dossier, exist_ok=True)
        self.chemin = os.path.join(self.dossier, "demo")
        with open(self.chemin, "wb") as f:
            f.write(img)
        os.chmod(self.chemin, 0o755)

    def lancer(self) -> tuple[bytes, bytes, int]:
        try:
            r = subprocess.run([self.qemu] + self.extra + [self.chemin],
                               capture_output=True, timeout=60)
            return r.stdout, r.stderr, r.returncode
        except subprocess.TimeoutExpired:
            return b"", b"<timeout>", -99

    def nettoyer(self):
        import shutil
        shutil.rmtree(self.dossier, ignore_errors=True)


def transcription_attendue() -> bytes:
    """La transcription intégrale, construite depuis le plan (le même
    générateur que le démonstrateur suit — l'attendu est DÉTERMINISTE)."""
    att = bytearray()
    for i in range(N_TRAFIC):
        if i == K_APPLY:
            att += L.D_APPLY + L.D_TRAMP + b"j2: verdict\n" + L.D_EFFET
        if i == M_ROLLBACK:
            att += L.D_ROLLB + b"verdict\n" + L.D_V1
        ligne = b"trafic " + str(i).encode() + b"\n"
        att += (b"j2: " + ligne) if K_APPLY <= i < M_ROLLBACK else ligne
    att += (L.D_PTRAFIC + L.D_REST + L.D_DORM + L.D_VERROU
            + L.D_REFMODE + L.D_REFETAT + L.D_REFABS + L.D_REFSOM
            + L.D_FIN)
    return bytes(att)


def executer(bavard: bool = True) -> tuple[bool, list[str]]:
    lignes: list[str] = []
    vert = True

    def constat(message: str, ok: bool, detail: str = "") -> None:
        nonlocal vert
        vert = vert and ok
        l = f"[demo] {'PASS' if ok else 'ECHEC'} : {message}"
        if detail:
            l += f" ({detail})"
        lignes.append(l)

    # — (0) la construction : le corpus + le démonstrateur, DÉTERMINISTE ----
    code, staging = BC.assembler_tout()
    drv = assembler_demo()
    verrous = oracle_demo(drv)
    img = composer_demo(code, staging, drv)
    for l in valider_demo(img, staging, drv):
        lignes.append(l)
    code_b, staging_b = BC.assembler_tout()
    img_b = composer_demo(code_b, staging_b, assembler_demo())
    if sha(img) != sha(img_b):
        raise EchecDemo("le demo n'est pas DÉTERMINISTE au rebuild")
    with open(CHEMIN_DEMO, "wb") as f:
        f.write(img)
    os.chmod(CHEMIN_DEMO, 0o755)
    constat(f"le demo construit : sha256 {sha(img)[:16]}…, {len(img)} o, "
            f"{len(verrous)} verrous structurels, DÉTERMINISTE au rebuild "
            f"({len(drv['insns'])} instructions, round-trip 100 %)", True,
            f"sha {sha(img)[:16]}…, {len(drv['octets'])} o de code")

    attendu = transcription_attendue()

    # — (a) LE TRAFIC EN SESSION — la transcription OCTET POUR OCTET --------
    t = Terrain(img)
    try:
        sortie, err, code_sortie = t.lancer()
        constat("le trafic en session : la transcription est OCTET POUR "
                f"OCTET l'attendu — {N_TRAFIC} usages, l'apply entre "
                f"{K_APPLY - 1} et {K_APPLY}, le retour entre {M_ROLLBACK - 1} "
                f"et {M_ROLLBACK}, code 0",
                code_sortie == 0 and not err and sortie == attendu,
                f"code={code_sortie}, {len(sortie)} o rendus / "
                f"{len(attendu)} attendus"
                + (f", err={err[:80]!r}" if err else ""))
        # la cohérence du flux : les lignes du trafic, aucune perdue/déchirée
        motif = re.compile(rb"^(j2: )?trafic (\d+)$")
        vues: dict[int, bool] = {}
        duplique = fragment = melange = None
        corpus_lignes = sortie.split(b"\n")
        emissions = {b"j2: verdict", b"verdict"}   # les lignes de l'épreuve
        for l in corpus_lignes[:-1]:
            m = motif.match(l)
            if not m:
                if l.startswith(b"demo: ") or l in emissions:
                    continue    # la narration + les émissions de l'épreuve
                fragment = fragment or l
                continue
            num = int(m.group(2))
            if num in vues:
                duplique = duplique or num
            vues[num] = m.group(1) is not None
        n_v1 = sum(1 for i in range(N_TRAFIC) if not (K_APPLY <= i < M_ROLLBACK))
        indices_ok = set(vues) == set(range(N_TRAFIC)) and duplique is None
        for i, est_v2 in vues.items():
            if est_v2 != (K_APPLY <= i < M_ROLLBACK):
                melange = melange or i
        constat(f"le journal est COHÉRENT : {N_TRAFIC} lignes ENTIÈRES, "
                f"indices 0..{N_TRAFIC - 1} chacun EXACTEMENT une fois — "
                f"{n_v1} lignes v1, {M_ROLLBACK - K_APPLY} lignes v2 (marque "
                "j2:), aucun mélange de formats dans une même ligne",
                indices_ok and melange is None and fragment is None,
                (f"fragment {fragment!r}") if fragment is not None
                else (f"dupliqué {duplique}") if duplique is not None
                else (f"mélange @{melange}") if melange is not None
                else f"{N_TRAFIC}/{N_TRAFIC} indices, "
                     f"{sum(1 for v in vues.values() if v)} v2")
    finally:
        t.nettoyer()

    # — (d) LE DEP FALSIFIÉ : 0x7 → 0x3, le fetch faute (page sans X) -------
    mutant = bytearray(img)
    cible = None
    for insn in CS.disasm(bytes(img[L.A_PATCH:L.A_PATCH + 0x200]), L.A_PATCH):
        # la DERNIÈRE occurrence = le site de L'APPLY (le rollback précède
        # .applique dans le code — viser l'apply : le mutard meurt au
        # PREMIER apply, la transcription s'arrête aux 400 lignes v1)
        if insn.mnemonic == "addi" and insn.op_str == "a0, zero, 7":
            cible = insn.address
    if cible is None:
        raise EchecDemo("le DEP : l'immédiat 0x7 de tcp-07 introuvable")
    if img[cible + 2] != 0x70:
        raise EchecDemo(f"le DEP : l'octet immédiat inattendu {img[cible + 2]:#04x}")
    mutant[cible + 2] = 0x30            # 0x7 → 0x3 (imm12 bits 15:12 → 0x3)
    verif = list(CS.disasm(bytes(mutant[cible:cible + 4]), cible))
    if not verif or verif[0].mnemonic != "addi" or verif[0].op_str != "a0, zero, 3":
        raise EchecDemo("le DEP : le mutant ne relit pas addi a0, zero, 3")
    # l'attendu du mutant : les 400 lignes v1 EXACTEMENT (le premier apply
    # est le point de mort — tcp-07 mprotect la page SANS bit X, le fetch
    # suivant faute : ACCERR) — un attente PRÉCISE, pas un « != attendu »
    attendu_dep = b"".join(b"trafic " + str(i).encode() + b"\n"
                           for i in range(K_APPLY))
    tm = Terrain(bytes(mutant))
    try:
        sortie_m, err_m, code_m = tm.lancer()
        constat("LE DEP FALSIFIÉ (0x7→0x3) : l'exécution FAUTE au retour du "
                "premier mprotect (page sans X — le fetch suivant : ACCERR) — "
                "SIGSEGV, zéro silence (D39 : le bit exécution RETENU pendant "
                "l'écriture, la falsification le retire)",
                code_m == -11 and sortie_m == attendu_dep,
                f"code={code_m}, {len(sortie_m)} o == {len(attendu_dep)} attendus")
    finally:
        tm.nettoyer()

    # — (e) LA FALSIFICATION DU DÉMONSTRATEUR (D154) -------------------------
    rompu, essais = None, 0
    for insn in drv["insns"]:
        mutant_f = bytearray(img)
        mutant_f[insn.address] ^= 0xFF
        essais += 1
        tf = Terrain(bytes(mutant_f))
        try:
            sortie_f, err_f, code_f = tf.lancer()
            if (code_f, sortie_f) != (0, attendu):
                rompu = insn.address
                break
        finally:
            tf.nettoyer()
    constat("la falsification du démonstrateur : un octet d'opcode corrompu "
            "fait dévier la transcription ou le code (zéro silence — non-vacuité)",
            rompu is not None,
            f"rompu à {rompu:#x} (essai n°{essais})" if rompu is not None
            else f"{essais} mutations TOUTES silencieuses — VACUE")

    # — (f) L'INDIFFÉRENCE À LA BASE (bases forcées du CHARGEUR) -------------
    for nom_cfg, extra in (("-R 1G", ["-R", "1G"]),
                           ("-R 4G", ["-R", "4G"]),
                           ("-B 0x100000000 -R 2G", ["-B", "0x100000000", "-R", "2G"])):
        tb = Terrain(img, extra=extra)
        try:
            sortie_b, err_b, code_b2 = tb.lancer()
            constat(f"base forcée {nom_cfg} : la transcription identique "
                    "(l'indifférence à la base — jamais un ASLR émulé)",
                    code_b2 == 0 and sortie_b == attendu,
                    f"code={code_b2}")
        finally:
            tb.nettoyer()

    # — (g) ZÉRO RÉGRESSION SUR PIÈCES ---------------------------------------
    with open(CHEMIN_CORPUS, "rb") as f:
        sha_apres = sha(f.read())
    constat("le FICHIER corpus n'a pas bougé d'un octet (le patch est un "
            "fait de la session invitée, jamais du fichier — relu après la "
            "démonstration)", sha_apres == SHA_CORPUS_ATTENDU,
            f"sha256 {sha_apres[:16]}…")
    tc = Terrain(open(CHEMIN_CORPUS, "rb").read())
    try:
        sortie_c, err_c, code_c = tc.lancer()
        constat("le rituel du corpus REJOUÉ : exactement ses deux lignes au "
                "code 0 (l'artefact intègre après la démonstration)",
                code_c == 0 and sortie_c == RITUEL and not err_c,
                f"code={code_c}")
    finally:
        tc.nettoyer()

    lignes.append(f"[demo] VERDICT : {'VERT' if vert else 'KO'} — la bascule "
                  "pendant le trafic, la séquence scratch+fence.i (mprotect → "
                  "copie → fence rw,rw → la bascule UN mot → fence.i → RX), "
                  "l'effet au geste même, le rollback, les refus nommés "
                  "(1/2/3/4), le DEP falsifié et la falsification du "
                  "démonstrateur — démontrés sur pièces sous qemu (réserve "
                  "instrumentale D149 : TCG, noyau et syscalls réels)")
    if bavard:
        print("\n".join(lignes))
    return vert, lignes


if __name__ == "__main__":
    try:
        ok, _ = executer(bavard=True)
        sys.exit(0 if ok else 1)
    except (EchecDemo, BC.EchecBuild) as exc:
        print(f"ECHEC (fail-closed) : {exc}", file=sys.stderr)
        sys.exit(1)
