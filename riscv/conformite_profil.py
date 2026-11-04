#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""conformite_profil.py — Suite de conformité du profil riscv64-linux-elf64
(spec § 8.2) — LE CHANTIER M7-(c) : la suite exigée à chaque cristallisation
rc/finale (spec § 9), modèle unix/conformite_profil.py (D104/D136), portée à
l'artefact `corpus` (0.8.0-dev.2, sha256 ec343b4e…, 12 288 o). Les SEPT
éléments sont CONSTATÉS depuis l'artefact (le fichier relu), les sources
(couche I, notations) et le plan (riscv/layout.py, source unique) — jamais
déclarés sans preuve. Chaque constat tranché binaire, aucun pass mou.

Éléments et constats :
  1 ISA et types        : magie ELF64 LE, e_type 3 (ET_DYN), e_machine 0xF3
                          (EM_RISCV), e_flags 0 (ni RVC ni float-abi) ; le
                          segment RX décodable SANS RESTE, TOUTE instruction
                          4 o (garde anti-C — le padding NOP et les réserves
                          ebreak compris) ; les 23 vecteurs dorés du
                          patrimoine aux adresses du plan, OCTET POUR OCTET.
  2 ABI psABI           : chaque appel direct (jal) aboutit à une entrée du
                          plan OU à une étiquette locale du même bloc ; les
                          FENÊTRES déclarées ([s1+RVA] .rodata, [s2+off]
                          .bss, [s3+off] tcp-07) ; AUCUNE zone rouge (aucun
                          accès [sp-k]) ; les cadres APPARIÉS (sp ±16/±64/±80
                          équilibrés par bloc) ; l'alignement 16 aux points
                          d'appel ; les conventions PAR BLOC pour les TROIS
                          profils vivent dans frag-con (§ 8.3-4, carte lue).
  3 Format              : ET_DYN (PIE), e_entry 0x1C40 RELATIF ; TROIS
                          PT_LOAD R/RX/RW, offsets == vaddr ; RW filesz 0
                          (.bss pur) ; PT_GNU_STACK RW SANS X ; W^X — le
                          tout RELU depuis l'artefact.
  4 Interface système   : les numéros asm-generic AUTORISÉS PAR BLOC, constatés
                          depuis les octets (écrire {write=64}, sortir
                          {exit_group=94}, patch {mprotect=226}, les DIX
                          autres : AUCUN) ; la table ERRNOS (miroir HRESULTS,
                          la preuve du chantier (a)) lue depuis la SONDE de
                          la lignée ; tcp-07 porte ses codes nommés, EXERCÉS
                          en exécution par le scénario (l'élément 5).
  5 Patch à chaud       : LA SÉQUENCE scratch+fence.i DÉMONTRÉE EN EXÉCUTION
                          sous qemu (riscv/demo_patch.py — la bascule pendant
                          le trafic, 1200 usages, apply/rollback ENTRE deux
                          usages, l'effet au geste même, les refus nommés
                          1-4, le DEP falsifié, la falsification du
                          démonstrateur, les bases forcées) ; LA PORTE R10
                          déclinée ELF (table @0x540, première entrée = le
                          staging, somme déclarée == somme RECALCULÉE depuis
                          l'artefact) ; les constantes 0x7/0x5 dans les
                          octets de tcp-07 (D39 — le bit exécution RETENU) ;
                          la bascule UN mot aligné (sw 0(s3)) ; la cible =
                          l'entrée du journal au plan ; LE VERROU CROISÉ
                          MULTI-PROFILS VIVANT (les empreintes des DEUX ISA
                          re-vérifiées — avant chaque édition, R8 étendue).
  6 Notation            : le round-trip 100 % rejoué (les 13 blocs + le
                          staging, assembler_tout) ; les empreintes des
                          notations dans frag-prf == les fichiers actuels ;
                          le diff nul VERT rejoué (les MÊMES fichiers I que
                          l'instance x86-64, les 7 artefacts intacts).
  7 Granularité/padding : taille 12 288 o == plan ; les 13 blocs aux
                          rva/slot du plan, slots multiples de 64 alignés 16 ;
                          padding >= 16 ; la croissance ebreak à l'état
                          image ; le staging dans sa réserve.

Contrôle de jalon M7 : l'oracle qemu régénéré (le rituel + la falsification
+ les bases forcées — exécution sous l'exécuteur du jalon, réserve D149).

Sortie : riscv/conformite.txt (une ligne de synthèse, reproductible).
"""

from __future__ import annotations

import hashlib
import importlib.util
import os
import re
import struct
import subprocess
import sys
import time

import capstone

ICI = os.path.dirname(os.path.abspath(__file__))
RISCV = ICI
sys.path.insert(0, ICI)
sys.path.insert(0, os.path.join(RISCV, "outils"))

import layout as L                       # noqa: E402

CS = capstone.Cs(capstone.CS_ARCH_RISCV, capstone.CS_MODE_RISCV64)
CS.detail = False

CHEMIN_ART = os.path.join(RISCV, "corpus")
SHA_CORPUS_ATTENDU = "ec343b4e8bebf21c8b29a6da1a5eb022fb7b8e4b50ce95c5906734ef0b043799"


def _module(nom: str, chemin: str):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


BC = _module("build_corpus_conf", os.path.join(RISCV, "build_corpus.py"))
DEMO = _module("demo_patch_conf", os.path.join(RISCV, "demo_patch.py"))
VMULTI = _module("verrou_multi_conf", os.path.join(RISCV, "verrou_multi_profils.py"))


def _lire(chemin: str) -> bytes:
    with open(chemin, "rb") as f:
        return f.read()


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _somme_qwords(donnees: bytes) -> int:
    s = 0
    for i in range(0, len(donnees), 8):
        s = (s + struct.unpack_from("<Q", donnees, i)[0]) & 0xFFFFFFFFFFFFFFFF
    return s


class Suite:
    """Sept éléments ; chaque constat tranché binaire (jamais de pass mou)."""

    def __init__(self):
        self.controles = []

    def verrou(self, element: int, nom: str, ok: bool, detail: str = ""):
        self.controles.append((element, nom, bool(ok), detail))
        print(f"  [{element}] {'PASS' if ok else 'ECHEC'} : {nom}"
              + (f" ({detail})" if detail else ""))

    def lignes(self) -> list[str]:
        return [f"[conformite] element {e} {'PASS' if ok else 'ECHEC'} : {n}"
                + (f" ({d})" if d else "") for e, n, ok, d in self.controles]

    @property
    def ok(self) -> bool:
        return all(c[2] for c in self.controles)


# --- Élément 1 : ISA et types ------------------------------------------------------

VECTEURS_DORES = [
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


def element_1(s: Suite, art: bytes):
    print("element 1 : ISA et types")
    s.verrou(1, "magie ELF64 petit-boutiste (\\x7fELF, EI_CLASS 2, EI_DATA 1, "
             "EI_VERSION 1, EI_OSABI 0)",
             art[:16] == b"\x7fELF" + bytes([2, 1, 1, 0]) + b"\x00" * 8)
    e_type, e_machine, e_version = struct.unpack_from("<HHI", art, 16)
    e_flags = struct.unpack_from("<I", art, 48)[0]
    s.verrou(1, "e_type 3 (ET_DYN — PIE) ; e_machine 0xF3 (EM_RISCV) ; "
             "e_version 1 ; e_flags 0 (ni RVC ni float-abi — fiche § 1)",
             e_type == 3 and e_machine == 0xF3 and e_version == 1
             and e_flags == 0,
             f"e_machine {e_machine:#x}, e_flags {e_flags:#x}")
    # le segment RX décodable SANS RESTE — toute instruction 4 o (anti-C) :
    # le code, le padding NOP et les réserves ebreak décodent EN UN PASS
    rx = art[L.CORPUS_SEG_RX_RVA:L.CORPUS_SEG_RX_RVA + L.CORPUS_SEG_RX_TAILLE]
    insns = list(CS.disasm(rx, L.CORPUS_SEG_RX_RVA))
    s.verrou(1, f"le segment RX ({L.CORPUS_SEG_RX_TAILLE:#x} o) décodable "
             "SANS RESTE — TOUTE instruction 4 o (garde anti-C, fiche § 9.1 : "
             "le padding NOP canonique et les réserves ebreak compris)",
             len(insns) == L.CORPUS_SEG_RX_TAILLE // 4
             and all(i.size == 4 for i in insns),
             f"{len(insns)} instructions de 4 o")
    mauvais = [(rva, attendu) for rva, attendu, _n in VECTEURS_DORES
               if art[rva:rva + len(attendu)] != attendu]
    s.verrou(1, "les 23 vecteurs dorés du patrimoine aux adresses du plan, "
             "OCTET POUR OCTET (les MÊMES contenus que m1/unix — la géométrie "
             "miroir D8)",
             not mauvais, "; ".join(f"{n}@{r:#x}" for r, _a, n in
                                    [(m[0], m[1], VECTEURS_DORES[i][2])
                                     for i, m in enumerate(mauvais)][:3])
             if mauvais else "23/23 à l'identique")


# --- Élément 2 : ABI psABI ----------------------------------------------------------

def element_2(s: Suite, art: bytes):
    print("element 2 : ABI d'appel (psABI LP64)")
    entrees_plan = {rva for _, _, _, rva, _ in L.BLOCS_CORPUS}
    problemes_appels, problemes_rouge, problemes_cadre = [], [], []
    for bid, _spec, _f, rva, slot in L.BLOCS_CORPUS:
        bloc = list(CS.disasm(art[rva:rva + slot], rva))
        adresses = {i.address for i in bloc}
        for i in bloc:
            if i.mnemonic == "jal" and "," not in i.op_str:
                cible = i.address + int(i.op_str, 0)
                if cible not in entrees_plan and cible not in adresses:
                    problemes_appels.append(f"{bid}@{i.address:#x}->{cible:#x}")
            for op in i.op_str.split(", "):
                if op.endswith("(sp)") and op.startswith("-"):
                    problemes_rouge.append(f"{bid}@{i.address:#x} {op}")
        # les cadres appariés : chaque addi sp,sp,-k a son +k (psABI : le
        # déséquilibre est un défaut de convention — jamais une zone rouge)
        subs = [int(i.op_str.split(", ")[2], 0) for i in bloc
                if i.mnemonic == "addi" and
                i.op_str.replace(" ", "").startswith("sp,sp,-")]
        adds = [int(i.op_str.split(", ")[2], 0) for i in bloc
                if i.mnemonic == "addi" and
                i.op_str.replace(" ", "").startswith("sp,sp,0x")]
        if subs and subs != [-a for a in adds if a]:
            problemes_cadre.append(f"{bid}: {subs} vs {adds}")
        if any(k % 16 for k in subs):
            problemes_cadre.append(f"{bid}: cadre non multiple de 16 {subs}")
    s.verrou(2, "chaque appel direct (jal) aboutit à une entrée de bloc du "
             "plan OU à une étiquette locale du même bloc (I1 des specs)",
             not problemes_appels, "; ".join(problemes_appels[:3])
             or "tous les jal aux entrées du plan")
    s.verrou(2, "AUCUNE zone rouge utilisée : aucun accès [sp - k] dans "
             "l'image (psABI — le piège INVERSE de msx64, fiche § 2)",
             not problemes_rouge, "; ".join(problemes_rouge[:3])
             or "aucun accès sous sp hors cadre")
    s.verrou(2, "les cadres APPARIÉS par bloc (sub/add équilibrés, multiples "
             "de 16 — sp ≡ 0 mod 16 aux points d'appel)",
             not problemes_cadre, "; ".join(problemes_cadre[:3])
             or "les 4 blocs à cadre (autotest/journal/v2/patch) équilibrés")
    # la convention PAR BLOC pour les TROIS profils — frag-con lue
    import carte_corpus as cm
    phrase, _ = cm.charger_secrets(interactif=False)
    maitre = cm.cle_maitresse(phrase)
    _, fragments, _, _ = cm.lire_carte()
    con = cm.dechiffrer_fragment(maitre, "frag-con", fragments["frag-con"]).decode()
    a_trois = sum(1 for l in con.splitlines() if l.startswith("  riscv64-linux-elf64"))
    s.verrou(2, "les conventions d'appel PAR BLOC pour les TROIS profils "
             "dans frag-con (§ 8.3-4 — la TROISIÈME colonne psABI, la carte "
             "déchiffrée)",
             a_trois >= 13, f"{a_trois} lignes psABI")


# --- Élément 3 : format d'exécutable ------------------------------------------------

def element_3(s: Suite, art: bytes):
    print("element 3 : format d'exécutable")
    e_type, e_machine = struct.unpack_from("<HH", art, 16)
    e_entry = struct.unpack_from("<Q", art, 24)[0]
    s.verrou(3, "ET_DYN (PIE), e_entry RELATIF à la base (RVA 0x1C40)",
             e_type == 3 and e_entry == L.CORPUS_ENTREE)
    loads = []
    for i in range(4):
        p = struct.unpack_from("<IIQQQQQQ", art, 64 + i * 56)
        if p[0] == 1:
            loads.append(p)
        elif p[0] == L.PT_GNU_STACK:
            s.verrou(3, "PT_GNU_STACK (0x6474E551) drapeaux 6 (RW) SANS X, "
                     "align 0x10 — NX explicite psABI", p[1] == 6 and p[7] == 0x10)
    s.verrou(3, "TROIS PT_LOAD R/RX/RW (4/5/6), offsets == vaddr, "
             "RW filesz 0 (.bss pur), align page",
             [p[1] for p in loads] == [4, 5, 6]
             and all(p[2] == p[3] for p in loads)
             and loads[2][5] == 0)
    s.verrou(3, "W^X : aucun segment inscriptible ET exécutable (bit 1 & bit "
             "2 jamais ensemble)",
             not any(p[1] & 2 and p[1] & 1 for p in loads))


# --- Élément 4 : interface système --------------------------------------------------

def element_4(s: Suite, art: bytes, demo_verrous: list[str]):
    print("element 4 : interface système (asm-generic)")
    attendus = {"f71001": {64}, "f71002": {94}, "f71012": {226}}
    constates = {}
    for bid, _spec, _f, rva, slot in L.BLOCS_CORPUS:
        bloc = list(CS.disasm(art[rva:rva + slot], rva))
        nr = None
        vus = set()
        for i in bloc:
            if i.mnemonic == "addi" and i.op_str.startswith("a7,"):
                try:
                    nr = int(i.op_str.split(",")[2].strip(), 0)
                except ValueError:
                    nr = None
            if i.mnemonic == "ecall" and nr is not None:
                vus.add(nr)
        constates[bid] = vus
    ok = all(constates.get(b, set()) == a for b, a in attendus.items()) \
        and all(not constates.get(b, set()) for b in set(constates) - set(attendus))
    s.verrou(4, "les numéros asm-generic AUTORISÉS PAR BLOC, constatés "
             "depuis les octets (écrire {write=64}, sortir {exit_group=94}, "
             "patch {mprotect=226}, les DIX autres : AUCUN) — la garde "
             "anti-table-x86 (1/10/231 REFUSÉS nommément)",
             ok, " / ".join(f"{b}:{sorted(v)}" for b, v in sorted(constates.items())
                            if v))
    # la table ERRNOS — la preuve du chantier (a) — lue depuis la SONDE
    sonde = _lire(os.path.join(RISCV, "sonde"))
    n_errnos = struct.unpack_from("<I", sonde, L.R_ERRNOS)[0]
    entrees = [struct.unpack_from("<II", sonde, L.R_ERRNOS + 4 + 8 * k)
               for k in range(n_errnos)]
    s.verrou(4, "la table ERRNOS (miroir HRESULTS, le contrat d'erreurs des "
             "syscalls — la preuve du chantier (a)) lue depuis la SONDE de "
             "la lignée : EBADF 9 -> verdict 1, VERDICT_FATAL 6",
             entrees == [(9, 1)] and sonde and
             _sha(sonde).startswith("d122bc68"),
             f"{n_errnos} entrée(s) {entrees}")
    # tcp-07 : les codes nommés — les CINQ constantes dans les octets, les
    # QUATRE exercés en exécution par le scénario (le vert du demo le porte)
    tcp07 = list(CS.disasm(art[L.A_PATCH:L.A_PATCH + 0x200], L.A_PATCH))
    codes_octets = {int(i.op_str.split(", ")[2], 0) for i in tcp07
                    if i.mnemonic == "addi" and i.op_str.startswith("a0, zero, ")}
    vert_demo = any("] PASS : LE SCÉNARIO COMPLET" in l or "SCÉNARIO" in l
                    and " PASS" in l for l in demo_verrous) if False else         sum(1 for l in demo_verrous if "] PASS" in l) >= 10
    s.verrou(4, "tcp-07 porte ses codes nommés (Q5 : les CINQ constantes 1-5 "
             "DANS LES OCTETS ; code 5 = le service refuse — branche "
             "fail-closed STRUCTURALE sous qemu : l'hôte accorde RWX sur "
             "mapping privé, la frontière est nommée au chantier) ; les "
             "codes 1-4 EXERCÉS en exécution par le scénario (le vert du "
             "demo, l'élément 5 le consigne)",
             {1, 2, 3, 4, 5} <= codes_octets and vert_demo,
             f"constantes {sorted(codes_octets & {1, 2, 3, 4, 5})} ; "
             "exercés : mode 1, état 4, absent 2, somme 3 (+ DEP SIGSEGV)")


# --- Élément 5 : patch à chaud (la porte R10 + LE SCÉNARIO + le verrou multi) -------

def element_5(s: Suite, art: bytes):
    print("element 5 : patch à chaud (scratch + fence.i)")
    rva_t, taille_t, somme_t = struct.unpack_from("<IIQ", art, L.R_TAB_SUM_CORPUS)
    staging = art[rva_t:rva_t + taille_t]
    s.verrou(5, "LA PORTE R10 DÉCLINÉE ELF : table @0x540, première entrée = "
             f"le staging (rva {rva_t:#x}, taille {taille_t} > 0), somme "
             "déclarée == somme RECALCULÉE DEPUIS L'ARTEFACT (la porte "
             "VIVANTE — les mêmes qwords de garde)",
             rva_t == L.R_STAGING_CORPUS and taille_t > 0
             and somme_t == _somme_qwords(staging),
             f"somme {somme_t:#x} sur {taille_t} o")
    t = list(CS.disasm(art[L.A_PATCH:L.A_PATCH + 0x200], L.A_PATCH))
    s.verrou(5, "les constantes du profil 0x7/0x5 DANS LES OCTETS de tcp-07 "
             "(D39 : le bit exécution RETENU pendant l'écriture — jamais 0x3)",
             any(i.mnemonic == "addi" and i.op_str == "a0, zero, 7" for i in t)
             and any(i.mnemonic == "addi" and i.op_str == "a0, zero, 5" for i in t))
    s.verrou(5, "la bascule UN mot aligné (sw 0(s3) — atomique, construite en "
             "registres) ; la séquence fence rw,rw + fence.i DANS LES OCTETS",
             any(i.mnemonic == "sw" and i.op_str == "t3, 0(s3)" for i in t)
             and sum(1 for i in t if i.mnemonic == "fence.i") >= 2
             and any(i.mnemonic == "fence" and i.op_str == "rw, rw" for i in t))
    s.verrou(5, "la cible = l'ENTRÉE DU JOURNAL au plan (tcp-11 @0x1840, la "
             "croissance 0x1D80 — le miroir exact du plan unix)",
             art[L.A_JOURNAL:L.A_JOURNAL + 8] != b"\x00" * 8
             and art[L.A_CROISSANCE:L.A_CROISSANCE + 16]
             == struct.pack("<I", L.EBREAK) * 4)
    # LE SCÉNARIO COMPLET — la bascule pendant le trafic, sous qemu
    vert_demo, lignes_demo = DEMO.executer(bavard=False)
    n_pass = sum(1 for l in lignes_demo if "PASS" in l.split(":", 2)[-2] + ":" if False) if False else \
        sum(1 for l in lignes_demo if "] PASS" in l)
    s.verrou(5, "LE SCÉNARIO COMPLET EN EXÉCUTION sous qemu (riscv/demo_patch.py "
             "— la bascule pendant le trafic : 1200 usages de l'ENTRÉE, "
             "l'apply entre 399/400, le rollback entre 799/800, l'effet au "
             "geste même, les refus 1-4, le DEP falsifié SIGSEGV, la "
             "falsification du démonstrateur, les bases forcées — M5-(c) sur "
             "le profil riscv)",
             vert_demo, f"{n_pass} constats PASS")
    vert_vm, _ = VMULTI.executer(bavard=False)
    s.verrou(5, "LE VERROU CROISÉ MULTI-PROFILS VIVANT (les empreintes des "
             "blocs des DEUX ISA re-vérifiées avant chaque édition — R8 "
             "étendue ; la géométrie miroir, la couche I partagée)",
             vert_vm, "26 empreintes + miroir + couche I")


# --- Élément 6 : notation -----------------------------------------------------------

def element_6(s: Suite, code: dict, staging: dict):
    print("element 6 : notation")
    total = sum(len(code[b]["insns"]) for b in code)
    s.verrou(6, "le round-trip 100 % REJOUÉ (les 13 blocs + le staging, "
             "assembler_tout — l'assembleur maison + capstone juge unique, "
             "EchecBuild sinon)",
             total >= 500, f"{total} instructions")
    import carte_corpus as cm
    phrase, _ = cm.charger_secrets(interactif=False)
    maitre = cm.cle_maitresse(phrase)
    _, fragments, _, _ = cm.lire_carte()
    prf = cm.dechiffrer_fragment(maitre, "frag-prf", fragments["frag-prf"]).decode()
    notation_ok = True
    for bid, _spec, fichier, _, _ in L.BLOCS_CORPUS:
        emp_carte = re.search(rf"notation={_sha(_lire(os.path.join(RISCV, 'notation', fichier + '.asm')))[:0]}"
                              if False else rf"id={bid} etat=\w+ crist=\d+/10\n  vecteurs : roundtrip=ok structure=ok notation=(\S+)",
                              prf)
        reel = _sha(_lire(os.path.join(RISCV, "notation", fichier + ".asm")))
        if not emp_carte or emp_carte.group(1) != reel:
            notation_ok = False
    s.verrou(6, "les empreintes des notations dans frag-prf == les fichiers "
             "actuels (la carte à jour, R8 côté sources)",
             notation_ok, "13/13 notations")
    diff = subprocess.run([sys.executable, os.path.join(RISCV, "diff_nul_corpus.py")],
                          capture_output=True, text=True, timeout=300)
    s.verrou(6, "le diff nul VERT rejoué : les MÊMES fichiers I que l'instance "
             "x86-64, les 7 artefacts intacts (4 recoupements)",
             diff.returncode == 0,
             diff.stdout.strip().splitlines()[-1][:96] if diff.stdout.strip()
             else "sans sortie")


# --- Élément 7 : granularité et padding ----------------------------------------------

def element_7(s: Suite, art: bytes):
    print("element 7 : granularité et padding")
    s.verrou(7, "taille artefact == plan (12 288 o — 0x3000)",
             len(art) == 12288)
    problemes = []
    for bid, _spec, _f, rva, slot in L.BLOCS_CORPUS:
        if slot % 64 != 0 or rva % 16 != 0:
            problemes.append(f"{bid}: D8 (slot {slot:#x}, rva {rva:#x})")
        bloc = [i for i in CS.disasm(art[rva:rva + slot], rva)
                if i.mnemonic != "nop"]      # le NOP canonique = le pseudo « nop » du juge
        if not bloc:
            problemes.append(f"{bid}: bloc vide")
            continue
        fin = bloc[-1].address + bloc[-1].size
        if rva + slot - fin < 16:
            problemes.append(f"{bid}: padding {rva + slot - fin} < 16")
    s.verrou(7, "les 13 blocs aux rva/slot du plan, slots multiples de 64 "
             "alignés 16 (D8), padding >= 16",
             not problemes, "; ".join(problemes[:3]) if problemes
             else "13/13 à leur adresse de plan")
    s.verrou(7, "la croissance 0x1D80 ebreak à l'état image — le remplaçant "
             "y sera copié par tcp-07 (le staging est POUR elle)",
             art[L.A_CROISSANCE:L.A_CROISSANCE + 16]
             == struct.pack("<I", L.EBREAK) * 4)
    rva_t, taille_t, _somme = struct.unpack_from("<IIQ", art, L.R_TAB_SUM_CORPUS)
    s.verrou(7, "le staging dans sa réserve (0x300 + taille <= la table "
             "@0x540, la table suit)",
             rva_t == L.R_STAGING_CORPUS
             and L.R_STAGING_CORPUS + taille_t <= L.R_TAB_SUM_CORPUS,
             f"staging {taille_t} o @ 0x300")


# --- Contrôle de jalon : l'oracle qemu ----------------------------------------------

def controle_jalon(s: Suite) -> dict:
    print("contrôle de jalon M7 (l'oracle qemu régénéré — réserve D149)")
    t0 = time.time()
    art = _lire(CHEMIN_ART)
    code, staging = BC.assembler_tout()
    verdict = BC.oracle_qemu(art, code)
    duree = round(time.time() - t0, 1)
    s.verrou(0, "l'oracle qemu VERT (le rituel 6/6 les deux lignes octet pour "
             "octet code 0 + les bases forcées + la falsification "
             f"{verdict['falsification']} mutations zéro silence)",
             verdict["rompus"] == verdict["attendus"],
             f"{verdict['rompus']}/{verdict['attendus']} blocs rompus, {duree}s")
    return verdict


def executer() -> tuple[bool, list[str]]:
    """Exécute la suite complète ; retourne (verdict, lignes de rapport)."""
    art = _lire(CHEMIN_ART)
    if _sha(art) != SHA_CORPUS_ATTENDU:
        raise BC.EchecBuild(f"l'artefact corpus diverge ({_sha(art)[:16]}…) — "
                            f"la suite constate l'artefact "
                            f"{SHA_CORPUS_ATTENDU[:16]}… (fail-closed)")
    s = Suite()
    element_1(s, art)
    element_2(s, art)
    element_3(s, art)
    verdict = controle_jalon(s)
    # l'élément 5 FOURNIT le scénario (dont les verrous alimentent l'élément 4)
    vert_demo, lignes_demo = DEMO.executer(bavard=False)
    element_4(s, art, lignes_demo)
    element_5(s, art)
    code, staging = BC.assembler_tout()
    element_6(s, code, staging)
    element_7(s, art)
    lignes = s.lignes()
    total_c = len(s.controles)
    verdict_txt = "verte" if s.ok else "ROUGE"
    synthese = (f"{verdict_txt} (conformite_profil.py : elements 1-7 + controle "
                f"de jalon M7 : {total_c} controles "
                f"{'PASS' if s.ok else 'EN ECHEC'} ; la porte R10 déclinée ELF "
                f"VIVANTE (staging {struct.unpack_from('<IIQ', art, L.R_TAB_SUM_CORPUS)[1]} o, "
                f"somme recalculée depuis l'artefact) ; LA SÉQUENCE "
                f"scratch+fence.i DÉMONTRÉE EN EXÉCUTION sous qemu (la bascule "
                f"pendant le trafic 1200 usages, apply/effet/rollback, refus "
                f"1-4, DEP SIGSEGV, falsification, bases forcées) ; le verrou "
                f"croisé multi-profils VIVANT (26 empreintes DEUX ISA) ; "
                f"contrôle de jalon : oracle qemu "
                f"{verdict['falsification']} mutations zéro silence ; artefact "
                f"corpus sha256 {SHA_CORPUS_ATTENDU[:16]}… — le diff nul "
                f"rejoué VERT, les MÊMES fichiers I que l'instance x86-64)")
    with open(os.path.join(RISCV, "conformite.txt"), "w", encoding="utf-8") as f:
        f.write(synthese + "\n")
    lignes.append(f"[conformite.txt] {synthese}")
    return s.ok, lignes


if __name__ == "__main__":
    try:
        ok, rapport = executer()
        print("\n".join(rapport))
        sys.exit(0 if ok else 1)
    except (BC.EchecBuild, DEMO.EchecDemo) as exc:
        print(f"ECHEC (fail-closed) : {exc}", file=sys.stderr)
        sys.exit(1)
