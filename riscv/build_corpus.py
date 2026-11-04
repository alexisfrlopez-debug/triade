#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_corpus.py — LA CHAÎNE INTÉGRALE de l'artefact `corpus` de la lignée
du jalon M7 (riscv/, chantier M7-(b) : la TROISIÈME instanciation de la même
couche I — D149-(7), le diff nul par script).

Le corpus paritaire RV64 : les DOUZE blocs du patrimoine (les révisions R+1
de la couche I — LES MÊMES FICHIERS CANONIQUES de unix/I/, chargés, jamais
copiés ; ancêtres scellés INTACTS dans m0/m1/m2) et le principal propre au
jalon (corpus-13, modèle ah-09). La GÉOMÉTRIE MIROIR du plan unix (D8) :
les MÊMES RVA, les MÊMES fixtures — seul le demi-octet ISA change.

La chaîne (le modèle build_m7.py, la discipline de la lignée) :
  1. couche I : lecture et audit des fichiers CANONIQUES de unix/I/
     (l'instance CHARGE — la garde absent ≠ illisible, D151) ;
  2. diff nul : diff_nul_corpus.py — les quatre recoupements (canoniques,
     observables R1↔R+1 par la chaîne M6, invariance des scellés, parité
     § 8.3 par exécution) ;
  3. assemblage : la notation (auteur.py) -> octets, round-trip PAR
     INSTRUCTION (R5, capstone juge unique, graphie canonique) ;
  4. oracle structurel : les contrats I sur le code désassemblé — appels
     déclarés PAR BLOC, syscalls asm-generic PAR BLOC avec LA GARDE
     ANTI-TABLE-X86 (a7 = 1/10/231 est un REFUS NOMMÉ — la parité est
     SÉMANTIQUE, jamais lexicale), données déclarées PAR FENÊTRE ([s1+RVA]
     .rodata, [s2+off] .bss — LA LEÇON imm12 : la fenêtre centrale, s3 la
     fenêtre de tcp-07), paires d'ancres re-vérifiées DEPUIS le code
     désassemblé, anti-C (taille 4), _start sans cadre, sortir sans ret,
     le verrou amoswap.d posé puis rendu, les cadres appariés et ordonnés,
     t1 JAMAIS touché (fiche § 2) ;
  5. composition : ELF64 durci (ET_DYN/PIE, 3 segments R/RX/RW, .bss pur,
     PT_GNU_STACK sans X — le durcissement M7-(a) hérité), fixtures dorées
     du patrimoine (les MÊMES contenus), staging du remplaçant + table
     d'intégrité R10, la croissance en réserve ebreak ;
  6. validation : l'image RELUE — W^X depuis les phdr, tables conformes au
     layout (source unique), e_entry relatif ;
  7. oracle d'exécution : qemu-riscv64 (réserve instrumentale D149 — TCG,
     noyau et syscalls RÉELS, nommée dans chaque verdict) — le rituel de
     parité en exécution (les DEUX lignes exactes + code 0, la parité § 8.3
     PAR EXÉCUTION), l'indifférence à la base par bases forcées du
     CHARGEUR (jamais un ASLR émulé feint), la falsification (un octet par
     instruction, zéro silence) ;
  8. la carte : génération 1 du corpus (fragments chiffrés, signature
     Ed25519 clés projet D27, verrou croisé R8, frag-con documenté PAR
     BLOC pour les TROIS profils — § 8.3-4).

Le scellage rc/final est la porte du chantier (c) (le contrôle D146 adapté
à l'exécuteur du jalon) — le présent build pose la balise 0.8.0-dev.2.

Usage : python3 riscv/build_corpus.py [--verifier] [--graine N]
Code de sortie : 0 = chaîne verte ; 1 = refus nommé (fail-closed).
"""

from __future__ import annotations

import hashlib
import os
import re
import struct
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone

ICI = os.path.dirname(os.path.abspath(__file__))
RISCV = ICI
UNIX = os.path.join(os.path.dirname(ICI), "unix")
sys.path.insert(0, ICI)
sys.path.insert(0, os.path.join(ICI, "outils"))
sys.path.insert(0, os.path.join(ICI, "notation"))

import layout as L                       # noqa: E402

import capstone                          # noqa: E402
import carte_corpus as cm                # noqa: E402
from as_rv64 import EchecAssemblage, assembler  # noqa: E402
from porte_roundtrip import franchir as franchir_porte  # noqa: E402

sys.path.insert(0, os.path.join(os.path.dirname(ICI), "m2"))
from carte_m2 import empreinte_racine    # noqa: E402  (mécanique commune D27)

CS = capstone.Cs(capstone.CS_ARCH_RISCV, capstone.CS_MODE_RISCV64)
CS.detail = False

_BRANCHES = {"beq", "bne", "blt", "bge", "bltu", "bgeu",
             "beqz", "bnez", "bgez", "bltz", "bgtz", "blez", "j"}


class EchecBuild(Exception):
    """Tout refus nommé de la chaîne (fail-closed : jamais un faux vert)."""


# --- Couche I : les fichiers CANONIQUES de unix/I/ (chargés, jamais copiés) --------

def lire_spec(chemin: str) -> dict:
    if not os.path.exists(chemin):
        raise EchecBuild(f"spécification ABSENTE : {chemin} (le corpus vit à "
                         f"unix/I/ — l'instance le CHARGE, écrite-avant-code)")
    try:
        with open(chemin, encoding="utf-8") as f:
            texte = f.read()
    except OSError as e:
        raise EchecBuild(f"spécification ILLISIBLE : {chemin} ({e}) — un fichier "
                         f"présent et illisible est un REFUS, jamais une permission "
                         f"(l'incident de l'état zéro, D151)") from e
    m = re.match(r"(\S+) · (.+?) · révision (\d+)", texte)
    if not m:
        raise EchecBuild(f"{chemin} : première ligne hors gabarit § 2.2")
    spec = {"id": m.group(1), "nom": m.group(2), "rev": int(m.group(3)),
            "texte": texte, "chemin": chemin}
    for bloc in ("Intention", "Contrat", "Échecs", "Vecteurs", "Fixtures",
                 "Provenance", "Décisions"):
        if bloc not in texte:
            raise EchecBuild(f"{chemin} : bloc de gabarit manquant : {bloc}")
    if "écrite-avant-code" not in texte:
        raise EchecBuild(f"{chemin} : provenance inattendue (écrite-avant-code)")
    return spec


def charger_couche_I() -> dict[str, dict]:
    """Les specs du corpus : LES MÊMES FICHIERS CANONIQUES que l'instance
    x86-64-linux charge (unix/I/) — la troisième instanciation, D149-(7)."""
    specs = {}
    for bid, sid, fichier, _, _ in L.BLOCS_CORPUS:
        chemin = os.path.join(UNIX, "I", fichier + ".md")
        spec = lire_spec(chemin)
        if f"{spec['id']}:R{spec['rev']}" != sid:
            raise EchecBuild(f"{chemin} : identifiant/révision "
                             f"{spec['id']}:R{spec['rev']} != plan {sid} "
                             f"(l'épinglage du plan — la leçon de l'incident)")
        specs[bid] = spec
    return specs


def _empreintes_I() -> dict:
    """Les empreintes des fichiers canoniques (frag-prf — la même couche
    que l'instance x86-64, empreintes identiques)."""
    emps = {}
    for _, _, fichier, _, _ in L.BLOCS_CORPUS:
        with open(os.path.join(UNIX, "I", fichier + ".md"), "rb") as f:
            emps[fichier] = sha(f.read())
    return emps


# --- Assemblage : notation -> octets (R5, l'assembleur maison + le juge) ----------

def assembler_bloc(fichier: str, rva: int, slot: int) -> dict:
    """Notation explicite -> octets + instructions + round-trip intégral.

    Les étiquettes résolues de l'en-tête (auteur) sont conservées : elles
    sont les cibles d'appel LOCALES déclarées (l'oracle les autorise).
    """
    chemin = os.path.join(ICI, "notation", fichier + ".asm")
    with open(chemin, encoding="utf-8") as f:
        lignes = [l.strip() for l in f.read().splitlines()]
    instrs = [l for l in lignes if l and not l.startswith(";")]
    labels: dict[str, int] = {}
    for l in lignes:
        m = re.match(r"; Étiquettes résolues : (.+)$", l)
        if m:
            for champ in m.group(1).split(", "):
                nom, _, val = champ.partition("=")
                labels[nom.lstrip(".")] = int(val, 16)
    code, insns = bytearray(), []
    pos = rva
    for texte in instrs:
        try:
            octets = assembler(texte, pos)
        except EchecAssemblage as exc:
            raise EchecBuild(f"{fichier} @ {pos:#x} : inassemblable : {exc}") from None
        if len(octets) != 4:
            raise EchecBuild(f"{fichier} @ {pos:#x} : {len(octets)} o != 4 (garde anti-C)")
        des = list(CS.disasm(octets, pos))
        if len(des) != 1 or des[0].size != 4:
            raise EchecBuild(f"{fichier} @ {pos:#x} : le juge ne décode pas UNE "
                             f"instruction de 4 o : {texte!r}")
        texte_cs = f"{des[0].mnemonic} {des[0].op_str}".strip()
        if assembler(texte_cs, pos) != octets:
            raise EchecBuild(f"{fichier} @ {pos:#x} : round-trip R5 rompu : {texte!r}")
        insns.append(des[0])
        code += octets
        pos += 4
    if len(code) > slot:
        raise EchecBuild(f"{fichier} : {len(code)} o > slot {slot:#x} (D8)")
    if slot - len(code) < 16:
        raise EchecBuild(f"{fichier} : padding {slot - len(code)} < 16 (D8)")
    n_nop = (slot - len(code)) // 4
    slot_plein = bytes(code) + struct.pack("<I", L.NOP_CANONIQUE) * n_nop
    if len(slot_plein) != slot:
        raise EchecBuild(f"{fichier} : le slot n'est pas multiple de 4 (garde anti-C)")
    return {"octets": bytes(code), "slot": slot_plein, "insns": insns,
            "texte": instrs, "labels": labels, "rva": rva, "slot_taille": slot}


def assembler_tout() -> tuple[dict, dict]:
    code, staging = {}, None
    for bid, _, fichier, rva, slot in L.BLOCS_CORPUS:
        code[bid] = assembler_bloc(fichier, rva, slot)
        print(f"[R5] {bid} ({fichier}) : {len(code[bid]['octets'])} o, "
              f"round-trip {len(code[bid]['insns'])}/{len(code[bid]['insns'])} = 100 %")
    bid, _, fichier, rva, slot = L.BLOC_STAGING
    staging = assembler_bloc(fichier, rva, slot)
    print(f"[R5] {bid} (staging {fichier}, POUR {rva:#x}) : "
          f"{len(staging['octets'])} o")
    return code, staging


# --- Oracle structurel : les contrats I sur le code désassemblé --------------------

# Les appels directs (jal — le lien vit dans ra) PAR BLOC (I1 des specs)
APPELS_AUTORISES = {
    "f71010": {L.A_ZONE_ALLOC, L.A_ZONE_RESET, L.A_MEMCMP, L.A_MEMCPY,
               L.A_STRLEN, L.A_ITOA, L.A_MEMSET, L.A_ECRIRE_CORPUS},   # libc-08 I1
    "f71011": {L.A_MEMCPY, L.A_ITOA, L.A_STRLEN, L.A_ECRIRE_CORPUS},   # tcp-11 I1
    "f71991": {L.A_MEMCPY, L.A_ITOA, L.A_STRLEN, L.A_ECRIRE_CORPUS},   # le remplaçant
    "f71012": {L.A_MEMCPY},                                            # tcp-07 I1 (+ .protger local)
    "f71013": {L.A_AUTOTEST, L.A_JOURNAL, L.A_SORTIR},                 # corpus-13 I1
}
SYSCALLS_AUTORISES = {        # I1/I2 : numéros ASM-GENERIC par bloc
    "f71001": {L.SYS_WRITE},        # écrire I4 : UN appel au service (write 64)
    "f71002": {L.SYS_EXIT_GROUP},   # sortir I1 (exit_group 94)
    "f71012": {L.SYS_MPROTECT},     # tcp-07 I1 (mprotect 226, dans .protger)
}
# Les fenêtres : [s1 + RVA] .rodata, [s2 + déplacement] .bss, [s3 + off]
# l'entrée (tcp-07) — I3 des specs, le plan source unique
R_TAB_SUM_TAILLE = L.R_TAB_SUM_CORPUS + 4       # u32 : la taille du staging
R_TAB_SUM_SOMME = L.R_TAB_SUM_CORPUS + 8        # u64 : la somme attendue
DONNEES_S1 = {
    "f71010": {L.R_SA, L.R_SB, L.R_SC, L.R_SD, L.R_MOTIF16, L.R_SENT16,
               L.R_MOTIF33, L.R_ZERO16, L.R_FF33, L.R_S_VIDE, L.R_S_TRIADE,
               L.R_S_33, L.R_I0, L.R_IMAX, L.R_I123, L.R_I7,
               L.R_PREFIXE_M1, L.R_SLASH, L.R_OK, L.R_KO},              # libc-08
    "f71991": {L.R_J2_MARK},                                          # tcp-11 v2 (la marque)
    "f71012": {L.R_STAGING_CORPUS, R_TAB_SUM_TAILLE, R_TAB_SUM_SOMME},  # tcp-07
    "f71013": {L.R_J_PREF, L.R_J_SUFF},                               # corpus-13
}
DONNEES_S2 = {
    "f71007": {L.CURSEUR_REL, L.ARENE_REL},      # libc-05 (le curseur + l'arène)
    "f71008": {L.CURSEUR_REL},                   # libc-06
    "f71011": {L.VERROU_REL},                    # tcp-11 (le verrou tournant)
    "f71991": {L.VERROU_REL},                    # le remplaçant (le même verrou)
    "f71012": {L.ETAT_REL, L.ENTREE_SAUVEE_REL},  # tcp-07
}
DONNEES_S3 = {
    "f71012": {0, L.CROISSANCE_REL},             # tcp-07 (l'entrée 0, la croissance +0x540)
}
# Les LO d'ancre (addi sN, sN, LO) — leurs adresses exactes : ils échappent
# au contrôle des formations (leurs PROPRES verrous d'ancre tranchent)
LO_ANCRES = {L.ANCRE_RODATA + 4, L.ANCRE_BSS_CORPUS + 4, L.ANCRE_ENTREE + 4}

# Les feuilles pures (libc-01..07 : I1 aucun appel, aucun accès système)
FEUILLES_PURES = {"f71003", "f71004", "f71005", "f71006", "f71007",
                  "f71008", "f71009"}

_RE_MEM = re.compile(r"^(-?(?:0x[0-9a-f]+|\d+))\((\w+)\)$")


def _nombre(s: str) -> int:
    return int(s, 0)


def _cible_relative(insn) -> int | None:
    """Cible d'un branchement/saut relatif (le texte porte le décalage)."""
    if insn.mnemonic in _BRANCHES or insn.mnemonic == "jal":
        return insn.address + _nombre(insn.op_str.split(",")[-1].strip())
    return None


def _imm20_signe(v: int) -> int:
    return v - 0x100000 if v >= 0x80000 else v


def oracle_structurel(code: dict, staging: dict) -> list[str]:
    verrous = []

    def verrou(nom, condition, detail=""):
        if not condition:
            raise EchecBuild(f"oracle structurel : {nom} {detail}")
        verrous.append(nom)

    tout = dict(code)
    tout["f71991"] = staging            # le remplaçant est vérifié AUSSI
    adresses = {bid: {i.address for i in tout[bid]["insns"]} for bid in tout}
    for bid, bloc in tout.items():
        insns = bloc["insns"]
        rva, slot = bloc["rva"], bloc["slot_taille"]
        labels = bloc.get("labels", {})
        # anti-C : TOUTE instruction fait 4 o (fiche § 9.1)
        for i in insns:
            verrou(f"{bid}:taille-4@{i.address:#x}", i.size == 4,
                   f"taille {i.size} != 4 (extension C ?)")
        # sauts internes : frontière d'instruction du même bloc
        for i in insns:
            if i.mnemonic in _BRANCHES:
                cible = _cible_relative(i)
                verrou(f"{bid}:saut-interne@{i.address:#x}",
                       cible in adresses[bid], f"cible {cible:#x} hors frontière")
        # appels directs (jal — le lien vit dans ra, JAMAIS ailleurs)
        locaux = set(labels.values())
        for i in insns:
            if i.mnemonic == "jal":
                if "," in i.op_str:
                    raise EchecBuild(
                        f"{bid}:appel@{i.address:#x} : jal hors forme d'appel du "
                        f"jalon ({i.op_str!r} — le lien vit dans ra, jamais ailleurs)")
                cible = _cible_relative(i)
                verrou(f"{bid}:appel-autorise@{i.address:#x}",
                       cible in APPELS_AUTORISES.get(bid, set()) | locaux,
                       f"cible {cible:#x} hors blocs déclarés (I1)")
        # jalr : uniquement ret (le retour canonique) — aucun appel indirect
        # au corpus (le scratch t1 du patch vit au chantier (c), fiche § 5)
        for i in insns:
            if i.mnemonic.startswith("jalr"):
                verrou(f"{bid}:ret-seul@{i.address:#x}", i.mnemonic == "ret",
                       f"jalr indirect hors contrat : {i.mnemonic} {i.op_str}")
        # syscalls : a7 posé juste avant (addi a7, zero, imm) ; numéros
        # asm-generic autorisés PAR BLOC — ET LA GARDE ANTI-TABLE-X86
        nr = None
        for i in insns:
            if i.mnemonic == "addi" and i.op_str.startswith("a7,"):
                try:
                    nr = _nombre(i.op_str.split(",")[2].strip())
                except (ValueError, IndexError):
                    nr = None
            if i.mnemonic == "ecall":
                if nr in L.TABLE_X86_REFUSEE:
                    raise EchecBuild(
                        f"oracle structurel : {bid}:syscall-x86@{i.address:#x} "
                        f"a7 = {nr} est le numéro x86-64 de "
                        f"« {L.TABLE_X86_REFUSEE[nr]} » — REFUS NOMMÉ (garde "
                        f"anti-table-x86, fiche § 4 : la parité est SÉMANTIQUE, "
                        f"jamais lexicale ; la table du jalon est asm-generic)")
                verrou(f"{bid}:syscall-autorise@{i.address:#x}",
                       nr in SYSCALLS_AUTORISES.get(bid, set()),
                       f"a7={nr} non déclaré (I1 — table asm-generic)")
        # données : les accès [fenêtre + déplacement] DÉCLARÉS (I3 — le plan)
        for i in insns:
            ops = [o.strip() for o in i.op_str.split(",")] if i.op_str else []
            for o in ops:
                m = _RE_MEM.match(o)
                if m:
                    imm, base = _nombre(m.group(1)), m.group(2)
                    if base == "s1":
                        verrou(f"{bid}:s1-rva-declaree@{i.address:#x}",
                               imm in DONNEES_S1.get(bid, set()),
                               f"s1+{imm:#x} hors .rodata déclarée (I3)")
                    elif base == "s2":
                        verrou(f"{bid}:s2-off-declaree@{i.address:#x}",
                               imm in DONNEES_S2.get(bid, set()),
                               f"s2+{imm:#x} hors .bss déclarée (I3)")
                    elif base == "s3":
                        verrou(f"{bid}:s3-off-declaree@{i.address:#x}",
                               imm in DONNEES_S3.get(bid, set()),
                               f"s3+{imm:#x} hors fenêtre entrée déclarée (I3)")
                    # base sp : la pile (traitée ci-dessous) ; base quelconque
                    # (t2 l'adresse du verrou, t5 le qword du staging) :
                    # POINTEUR CALCULÉ — formé depuis les déclarations
                    # ci-dessous (formation addi), jamais une adresse constante
            # formation de pointeur : addi rd, s1/s2/s3, imm (imm != 0 —
            # l'idiome imm=0 est rendu mv par le juge) ; les addi d'ancre
            # (LO des paires, à leurs sites exacts) échappent à ce contrôle :
            # leurs PROPRES verrous d'ancre tranchent (le layout fait foi)
            if i.mnemonic == "addi" and len(ops) == 3 and ops[1] in ("s1", "s2", "s3"):
                if i.address not in LO_ANCRES and _nombre(ops[2]) != 0:
                    jeu = {"s1": DONNEES_S1, "s2": DONNEES_S2,
                           "s3": DONNEES_S3}[ops[1]]
                    verrou(f"{bid}:{ops[1]}-formation@{i.address:#x}",
                           _nombre(ops[2]) in jeu.get(bid, set()),
                           f"{ops[1]}+{ops[2]} hors données déclarées (I3)")
        # t1 : le registre de travail du projet (fiche § 2) — JAMAIS touché
        # par un bloc du corpus (l'instrument de la sonde ; le portage de
        # R10/R11 x86-64 : le corpus n'en a pas besoin, il le respecte)
        for i in insns:
            ops = i.op_str.replace("(", ", ").replace(")", "").split(", ")
            verrou(f"{bid}:t1-respecte@{i.address:#x}",
                   "t1" not in [o.strip() for o in ops],
                   f"t1 touché : {i.mnemonic} {i.op_str} (fiche § 2)")
        # les paires d'ancres re-vérifiées DEPUIS LE CODE DÉSASSEMBLÉ
        ancres = []
        if bid == "f71013":
            ancres = [(insns[0], "s1", L.ANCRE_RODATA, L.CIBLE_RODATA),
                      (insns[2], "s2", L.ANCRE_BSS_CORPUS, L.CIBLE_BSS_CORPUS)]
        elif bid == "f71012":
            for i in insns:
                if i.mnemonic == "auipc" and i.op_str.startswith("s3, "):
                    ancres = [(i, "s3", L.ANCRE_ENTREE, L.CIBLE_ENTREE)]
                    break
        for insn_a, reg, site, cible in ancres:
            verrou(f"{bid}:ancre-{reg}-site", insn_a.address == site,
                   f"l'auipc {reg} vit à {insn_a.address:#x}, le layout déclare "
                   f"{site:#x} — la paire n'est pas au site (leçon C1)")
            hi = _imm20_signe(_nombre(insn_a.op_str.split(", ")[1]))
            idx = insns.index(insn_a)
            insn_i = insns[idx + 1]
            verrou(f"{bid}:ancre-{reg}-paire",
                   insn_i.mnemonic == "addi" and
                   insn_i.op_str.startswith(f"{reg}, {reg}, "),
                   "l'addi de la paire n'est pas adjacent à son auipc")
            lo = _nombre(insn_i.op_str.split(", ")[2])
            verrou(f"{bid}:ancre-{reg}-arithmetique@{insn_a.address:#x}",
                   site + hi * 4096 + lo == cible,
                   f"{site:#x} + {hi:#x}*4096 + {lo} != {cible:#x}")
        # padding/alignement (D8/D28/D33)
        fin_code = insns[-1].address + insns[-1].size
        verrou(f"{bid}:padding-16", rva + slot - fin_code >= 16)
        verrou(f"{bid}:slot-aligne-16", rva % 16 == 0)
        verrou(f"{bid}:slot-multiple-64", slot % 64 == 0)
        # la pile psABI : AUCUNE zone rouge — les feuilles ne touchent JAMAIS
        # sp ; les blocs à cadre : appariés et ordonnés ; _start : jamais
        ecritures_sp = [i for i in insns if i.mnemonic == "addi" and
                        i.op_str.replace(" ", "").startswith("sp,sp,")]
        if bid == "f71013":
            verrou(f"{bid}:start-sans-pile", not ecritures_sp,
                   "_start ne touche jamais sp (I4 — ABI de démarrage)")
            verrou(f"{bid}:start-sans-ecall",
                   not any(i.mnemonic == "ecall" for i in insns),
                   "aucun syscall direct — tout service passe par les blocs (I2)")
            verrou(f"{bid}:start-sans-cadre",
                   not any(i.mnemonic in ("sd", "ld") for i in insns),
                   "_start n'a pas de cadre à sauvegarder (le rituel ne revient pas)")
        elif bid in ("f71010", "f71011", "f71991", "f71012"):
            imm_sp = sorted(_nombre(i.op_str.split(",")[2]) for i in ecritures_sp)
            verrou(f"{bid}:pile-appairee",
                   len(ecritures_sp) == 2 and imm_sp[0] == -imm_sp[1],
                   f"écritures sp : {[i.op_str for i in ecritures_sp]}")
            seq = [i.mnemonic + "|" + i.op_str for i in insns]
            i_sub = next(k for k, s in enumerate(seq)
                         if s.startswith("addi|sp, sp, -"))
            i_add = next(k for k, s in enumerate(seq)
                         if s.startswith("addi|sp, sp, 0x"))
            i_sd = next(k for k, s in enumerate(seq) if s.startswith("sd|ra, 0(sp)"))
            i_ld = next(k for k, s in enumerate(seq) if s.startswith("ld|ra, 0(sp)"))
            i_ret = seq.index("ret|")
            verrou(f"{bid}:cadre-ordonne",
                   i_sub < i_sd < i_ld < i_add < i_ret,
                   f"cadre : -{imm_sp[1]:#x}@{i_sub} sd@{i_sd} ld@{i_ld} "
                   f"+{imm_sp[1]:#x}@{i_add} ret@{i_ret}")
        else:
            verrou(f"{bid}:feuille-sans-pile", not ecritures_sp,
                   "une feuille ne touche jamais sp (I2/psABI : AUCUNE zone rouge)")
            if bid in FEUILLES_PURES:
                verrou(f"{bid}:feuille-pure",
                       not any(i.mnemonic in ("jal", "ecall") for i in insns),
                       "un bloc PUR n'appelle ni bloc ni système (I1)")
                # I3 psABI : aucun registre non volatil MODIFIÉ — le registre
                # de destination n'est jamais un sN (les stores n'écrivent
                # AUCUN registre : sd zero, -0x400(s2) est une écriture de
                # DONNÉE, le curseur — jamais une sauvegarde de pile) ; les
                # bases s1/s2/s3 sont LUES, jamais écrites
                sregs = {f"s{n}" for n in range(12)}
                for i in insns:
                    if i.mnemonic in ("sd", "sw", "sh", "sb"):
                        continue          # un store n'écrit aucun registre
                    ops0 = i.op_str.split(",")[0].strip() if i.op_str else ""
                    verrou(f"{bid}:feuille-sans-non-volatil@{i.address:#x}",
                           ops0 not in sregs,
                           f"{ops0} écrit (I3 — psABI : aucun non volatil modifié)")
    # sortir : aucun ret, ebreak défensif (hello-03:R2 Q1/I1)
    s = code["f71002"]["insns"]
    verrou("f71002:jamais-ret", not any(i.mnemonic == "ret" for i in s))
    verrou("f71002:ebreak-defensif", any(i.mnemonic == "ebreak" for i in s))
    # écrire : UN seul ecall (I4)
    verrou("f71001:appel-unique",
           sum(1 for i in code["f71001"]["insns"] if i.mnemonic == "ecall") == 1)
    # tcp-11 : le verrou amoswap.d posé puis rendu (I1/Q3) — la restitution
    # est un sd simple (le portage du mov simple x86-64 ; le corpus est
    # mono-fil, fiche § 5 — le chantier (c) porte le verrou multi-profils)
    for bid in ("f71011", "f71991"):
        j = tout[bid]["insns"]
        verrou(f"{bid}:verrou-amoswap",
               any(i.mnemonic == "amoswap.d" for i in j),
               "l'atomique du profil (l'extension A — le portage du lock xchg)")
        verrou(f"{bid}:verrou-rendu",
               any(i.mnemonic == "sd" and i.op_str.endswith("(s2)") and
                   i.op_str.startswith("zero,") for i in j),
               "la restitution est un sd zero simple (Q3 : sur tout chemin)")
    # tcp-07 : la séquence du profil (fiche § 5) — mprotect 0x7/0x5 (D39 :
    # le bit exécution RETENU), fence rw,rw entre la copie et la bascule,
    # fence.i après chaque écriture de code, LA BASCULE en UNE écriture
    # alignée (un mot — jamais deux écritures partielles), le .protger local
    t = code["f71012"]["insns"]
    verrou("f71012:bit-execute-retenu",
           any(i.mnemonic == "addi" and i.op_str == "a0, zero, 7" for i in t)
           and any(i.mnemonic == "addi" and i.op_str == "a0, zero, 5" for i in t),
           "les constantes du profil 0x7/0x5 (I6, D39 — jamais 0x3)")
    verrou("f71012:fence-rw-rw",
           any(i.mnemonic == "fence" and "rw" == i.op_str.split(", ")[0]
               and i.op_str.split(", ")[1] == "rw" for i in t),
           "fence rw, rw entre la copie et la bascule (fiche § 5 (3))")
    verrou("f71012:fence-i",
           sum(1 for i in t if i.mnemonic == "fence.i") >= 2,
           "fence.i après chaque écriture de code (fiche § 5 (5))")
    verrou("f71012:protger-local",
           any(i.mnemonic == "jal" and "protger" in str(tout["f71012"].get("labels", {}))
               for i in t) or "protger" in tout["f71012"]["labels"],
           "le sous-programme local .protger est déclaré (I1)")
    verrou("f71012:bascule-un-mot",
           any(i.mnemonic == "sw" and i.op_str == "t3, 0(s3)" for i in t),
           "la bascule est UNE écriture alignée de mot (Q3 — atomique)")
    # le staging : assemblé POUR la croissance (le plan, la raison du v2)
    verrou("staging:pour-croissance",
           staging["rva"] == L.A_CROISSANCE,
           f"le remplaçant doit être assemblé pour {L.A_CROISSANCE:#x}")
    return verrous


# --- Symboles des notations confrontés au layout (leçon C1) ------------------------

SYMBOLES_LAYOUT = {
    # adresses d'appel (I1) + fixtures (le plan du corpus)
    "A_ECRIRE": L.A_ECRIRE_CORPUS, "A_SORTIR": L.A_SORTIR,
    "A_MEMCPY": L.A_MEMCPY, "A_MEMCMP": L.A_MEMCMP, "A_STRLEN": L.A_STRLEN,
    "A_ITOA": L.A_ITOA, "A_ZONE_ALLOC": L.A_ZONE_ALLOC,
    "A_ZONE_RESET": L.A_ZONE_RESET, "A_MEMSET": L.A_MEMSET,
    "A_AUTOTEST": L.A_AUTOTEST, "A_JOURNAL": L.A_JOURNAL,
    "A_PATCH": L.A_PATCH,
    "SA": L.R_SA, "SB": L.R_SB, "SC": L.R_SC, "SD": L.R_SD,
    "MOTIF16": L.R_MOTIF16, "SENT16": L.R_SENT16, "MOTIF33": L.R_MOTIF33,
    "ZERO16": L.R_ZERO16, "FF33": L.R_FF33, "S_VIDE": L.R_S_VIDE,
    "S_TRIADE": L.R_S_TRIADE, "S_33": L.R_S_33, "I0": L.R_I0,
    "IMAX": L.R_IMAX, "I123": L.R_I123, "I7": L.R_I7, "SLASH": L.R_SLASH,
    "PREFIXE": L.R_PREFIXE_M1, "OK": L.R_OK, "KO": L.R_KO,
    "J_PREF": L.R_J_PREF, "J_SUFF": L.R_J_SUFF, "J2_MARK": L.R_J2_MARK,
    "L_PREF": 18, "L_SUFF": 10,
    # les fenêtres (I3 — les déplacements relatifs aux ancres)
    "CURSEUR_REL": L.CURSEUR_REL, "ARENE_REL": L.ARENE_REL,
    "VERROU_REL": L.VERROU_REL, "ETAT_REL": L.ETAT_REL,
    "ENTREE_SAUVEE_REL": L.ENTREE_SAUVEE_REL, "CROISSANCE_REL": L.CROISSANCE_REL,
    # le staging et la porte R10
    "STAGING": L.R_STAGING_CORPUS, "TAILLE_SUM": R_TAB_SUM_TAILLE,
    "SOMME_SUM": R_TAB_SUM_SOMME, "ARENE_TAILLE": L.ARENE_TAILLE_CORPUS,
    # les tables et constantes du profil (asm-generic — la garde anti-x86)
    "SYS_WRITE": L.SYS_WRITE, "SYS_EXIT_GROUP": L.SYS_EXIT_GROUP,
    "SYS_MPROTECT": L.SYS_MPROTECT, "PROT_RWX": L.PROT_RWX,
    "PROT_RX": L.PROT_RX, "SENTINELLE": 0xFFFFFFFF,
    # les ancres (les sites — le layout tranche)
    "ANCRE_RODATA": L.ANCRE_RODATA, "ANCRE_BSS_CORPUS": L.ANCRE_BSS_CORPUS,
    "ANCRE_ENTREE": L.ANCRE_ENTREE,
}


def verifier_symboles() -> int:
    """Chaque @symbole des notations doit être celui du layout (source unique)."""
    n = 0
    for _, _, fichier, _, _ in list(L.BLOCS_CORPUS) + [L.BLOC_STAGING]:
        chemin = os.path.join(ICI, "notation", fichier + ".asm")
        for ligne in open(chemin, encoding="utf-8"):
            m = re.search(r"; Symboles .*: (.*)$", ligne)
            if m:
                for paire in m.group(1).split(", "):
                    nom, _, val = paire.partition("=")
                    nom = nom.lstrip("@")
                    if nom in SYMBOLES_LAYOUT:
                        attendu = SYMBOLES_LAYOUT[nom]
                        if int(val, 16) != attendu:
                            raise EchecBuild(
                                f"{fichier} : @{nom}={val} != layout {attendu:#x} "
                                f"(C1 : l'arithmétique de l'auteur est vérifiée, "
                                f"jamais crue)")
                        if nom.startswith("SYS_") and attendu in L.TABLE_X86_REFUSEE:
                            raise EchecBuild(
                                f"{fichier} : @{nom}={attendu} est un numéro x86-64 "
                                f"(« {L.TABLE_X86_REFUSEE[attendu]} ») — REFUS NOMMÉ "
                                f"(garde anti-table-x86, fiche § 4)")
                        n += 1
                break
    return n


# --- Composition ELF64 durci du corpus ----------------------------------------------

def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def somme_qwords(donnees: bytes) -> int:
    """La somme additive 64 bits des qwords (R10 — la porte d'intégrité)."""
    s = 0
    for i in range(0, len(donnees), 8):
        s = (s + struct.unpack_from("<Q", donnees, i)[0]) & 0xFFFFFFFFFFFFFFFF
    return s


def octets_staging(staging: dict) -> tuple[bytes, int, int]:
    """Le staging qword-paddé (réserve ebreak), sa taille et sa somme (R10)."""
    code = staging["octets"]
    taille = (len(code) + 7) & ~7              # multiple de qword (la somme)
    reste = taille - len(code)                # multiple de 4 (garde anti-C)
    paddage = (struct.pack("<I", L.EBREAK) * (reste // 4 + 1))[:reste]
    return code + paddage, taille, somme_qwords(code + paddage)


def composer_elf(code: dict, staging: dict) -> bytes:
    """Image durcie : segment R (en-têtes + fixtures + staging + table R10),
    segment RX (les treize slots, NOP intra-slot, la croissance ebreak),
    .bss pur (le chargeur le naît nul)."""
    seg_r = bytearray(b"\x00" * L.CORPUS_SEG_R_TAILLE)
    seg_rx = bytearray(struct.pack("<I", L.EBREAK) * (L.CORPUS_SEG_RX_TAILLE // 4))
    poses: list[tuple[int, int, str]] = []

    def poser(seg: bytearray, base: int, rva: int, donnees: bytes, nom: str = ""):
        poses.append((rva, rva + len(donnees), nom or hex(rva)))
        if rva + len(donnees) > base + len(seg):
            raise EchecBuild(f"segment débordant à {rva:#x} ({nom})")
        seg[rva - base: rva - base + len(donnees)] = donnees

    # — segment R : les vecteurs dorés du patrimoine (MÊMES contenus que
    #   m1/unix — la géométrie miroir : les MÊMES RVA)
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
    # — le staging + la table d'intégrité R10 (première entrée = le staging)
    staging_octets, staging_taille, staging_somme = octets_staging(staging)
    if staging_taille > L.STAGING_TAILLE_MAX:
        raise EchecBuild(f"staging {staging_taille} o > max {L.STAGING_TAILLE_MAX:#x}")
    poser(seg_r, L.CORPUS_SEG_R_RVA, L.R_STAGING_CORPUS, staging_octets, "STAGING")
    table = struct.pack("<IIQIQQ", L.R_STAGING_CORPUS, staging_taille,
                        staging_somme, 0, 0, 0)
    poser(seg_r, L.CORPUS_SEG_R_RVA, L.R_TAB_SUM_CORPUS, table, "TAB_SUM")
    # — segment RX : les treize slots (NOP intra-slot) ; la croissance
    #   demeure ebreak (le remplaçant y sera copié par tcp-07, chantier (c))
    for bid, _, _, rva, slot in L.BLOCS_CORPUS:
        poser(seg_rx, L.CORPUS_SEG_RX_RVA, rva, code[bid]["slot"], bid)
    # — anti-chevauchement (C1)
    for (d1, f1, n1), (d2, f2, n2) in zip(poses, poses[1:]):
        if d1 < f2 and d2 < f1:
            raise EchecBuild(f"chevauchement : {n1} [{d1:#x},{f1:#x}) / "
                             f"{n2} [{d2:#x},{f2:#x})")
    # — ehdr (ET_DYN, la moitié ISA RISC-V) + 4 phdr par-dessus les zéros
    e_ident = b"\x7fELF" + bytes([2, 1, 1, 0]) + b"\x00" * 8
    ehdr = struct.pack("<16sHHIQQQIHHHHHH", e_ident,
                       3, L.E_MACHINE, 1,           # ET_DYN (PIE), EM_RISCV, v1
                       L.CORPUS_ENTREE,             # e_entry = RVA (relatif)
                       64, 0, L.E_FLAGS,            # phoff, shoff, flags = 0
                       64, 56, 4, 0, 0, 0)         # ehsize, phentsize, phnum = 4
    ph_r = struct.pack("<IIQQQQQQ", 1, 4,          # LOAD, R (lecture seule)
                        L.CORPUS_SEG_R_RVA, L.CORPUS_SEG_R_RVA, L.CORPUS_SEG_R_RVA,
                        L.CORPUS_SEG_R_TAILLE, L.CORPUS_SEG_R_TAILLE, L.TAILLE_PAGE)
    ph_rx = struct.pack("<IIQQQQQQ", 1, 5,         # LOAD, R+X
                         L.CORPUS_SEG_RX_RVA, L.CORPUS_SEG_RX_RVA, L.CORPUS_SEG_RX_RVA,
                         L.CORPUS_SEG_RX_TAILLE, L.CORPUS_SEG_RX_TAILLE, L.TAILLE_PAGE)
    ph_rw = struct.pack("<IIQQQQQQ", 1, 6,         # LOAD, R+W (.bss pur)
                         L.CORPUS_SEG_RW_RVA, L.CORPUS_SEG_RW_RVA, L.CORPUS_SEG_RW_RVA,
                         0, L.CORPUS_SEG_RW_TAILLE, L.TAILLE_PAGE)
    ph_stack = struct.pack("<IIQQQQQQ", L.PT_GNU_STACK, 6,   # RW SANS X (NX)
                            0, 0, 0, 0, 0, 0x10)
    seg_r[0:64] = ehdr
    seg_r[64:120] = ph_r
    seg_r[120:176] = ph_rx
    seg_r[176:232] = ph_rw
    seg_r[232:288] = ph_stack
    return bytes(seg_r) + bytes(seg_rx)


def valider_elf(img: bytes, staging: dict) -> list[str]:
    """Relit l'image composée : le durcissement, le plan, la source unique."""
    lignes = []
    if len(img) != L.CORPUS_TAILLE_FICHIER:
        raise EchecBuild(f"taille {len(img):#x} != {L.CORPUS_TAILLE_FICHIER:#x}")
    if img[:4] != b"\x7fELF" or img[4] != 2 or img[5] != 1:
        raise EchecBuild("magie ELF64 LE absente")
    e_type, e_machine = struct.unpack_from("<HH", img, 16)
    e_entry = struct.unpack_from("<Q", img, 24)[0]
    e_flags = struct.unpack_from("<I", img, 48)[0]
    if e_type != 3:
        raise EchecBuild(f"e_type {e_type} != 3 (ET_DYN — le durcissement hérité)")
    if e_machine != L.E_MACHINE:
        raise EchecBuild(f"e_machine {e_machine:#x} != {L.E_MACHINE:#x} (EM_RISCV)")
    if e_flags != L.E_FLAGS:
        raise EchecBuild(f"e_flags {e_flags:#x} != {L.E_FLAGS:#x} (ni RVC ni float-abi)")
    if e_entry != L.CORPUS_ENTREE:
        raise EchecBuild(f"e_entry {e_entry:#x} != {L.CORPUS_ENTREE:#x} (RVA relatif)")
    phoff, phentsize, phnum = struct.unpack_from("<Q", img, 32)[0], \
        struct.unpack_from("<H", img, 54)[0], struct.unpack_from("<H", img, 56)[0]
    if (phoff, phentsize, phnum) != (64, 56, 4):
        raise EchecBuild(f"phdr ({phoff},{phentsize},{phnum}) != (64,56,4)")
    loads = []
    for i in range(phnum):
        p = struct.unpack_from("<IIQQQQQQ", img, phoff + i * 56)
        if p[0] == 1:
            loads.append(p)
        elif p[0] == L.PT_GNU_STACK:
            if p[1] != 6 or p[7] != 0x10:
                raise EchecBuild("PT_GNU_STACK != RW sans X, align 0x10 "
                                 "(NX exigé psABI)")
            lignes.append("[phdr] PT_GNU_STACK RW SANS X — NX explicite psABI")
        else:
            raise EchecBuild(f"p_type inattendu {p[0]:#x}")
    if len(loads) != 3 or [p[1] for p in loads] != [4, 5, 6]:
        raise EchecBuild(f"PT_LOAD {[p[1] for p in loads]} != R/RX/RW")
    for p in loads:
        if p[1] & 2 and p[1] & 1:
            raise EchecBuild(f"PT_LOAD {p[1]:#x} : inscriptible ET exécutable (W^X rompu)")
        if p[2] != p[3] or p[7] != L.TAILLE_PAGE:
            raise EchecBuild(f"PT_LOAD {p[1]:#x} : offset != vaddr ou align != page")
    attendus = {4: (L.CORPUS_SEG_R_RVA, L.CORPUS_SEG_R_TAILLE, L.CORPUS_SEG_R_TAILLE),
                5: (L.CORPUS_SEG_RX_RVA, L.CORPUS_SEG_RX_TAILLE, L.CORPUS_SEG_RX_TAILLE),
                6: (L.CORPUS_SEG_RW_RVA, 0, L.CORPUS_SEG_RW_TAILLE)}
    for p in loads:
        if (p[3], p[5], p[6]) != attendus[p[1]]:
            raise EchecBuild(f"PT_LOAD {p[1]:#x} : {(p[3], p[5], p[6])} != plan "
                             f"{attendus[p[1]]} (layout, source unique)")
    lignes.append("[phdr] 3 PT_LOAD R/RX/RW + PT_GNU_STACK RW sans X — W^X "
                  "CONSTATÉ depuis les phdr (le durcissement M7-(a) hérité)")
    lignes.append(f"[phdr] ET_DYN (PIE) : e_machine {L.E_MACHINE:#x} (EM_RISCV), "
                  f"e_flags 0, e_entry {e_entry:#x} RELATIF, .bss pur (filesz 0)")
    # les fixtures dorées : conformes au plan (les MÊMES contenus que m1/unix)
    for rva, attendu, nom in ((L.R_SA, b"TRIADE\0", "SA"), (L.R_SB, b"TRIADE\0", "SB"),
                              (L.R_SC, b"TRIADF\0", "SC"), (L.R_SD, b"TRI\0", "SD"),
                              (L.R_MOTIF16, bytes(range(16)), "MOTIF16"),
                              (L.R_SENT16, b"\xaa" * 16, "SENT16"),
                              (L.R_MOTIF33, L.CORPUS_MOTIF33, "MOTIF33"),
                              (L.R_ZERO16, b"\x00" * 16, "ZERO16"),
                              (L.R_FF33, b"\xff" * 33, "FF33"),
                              (L.R_S_VIDE, b"\0", "S_VIDE"),
                              (L.R_S_TRIADE, b"TRIADE\0", "S_TRIADE"),
                              (L.R_S_33, L.CORPUS_S_33 + b"\0", "S_33"),
                              (L.R_I0, b"0\0", "I0"),
                              (L.R_IMAX, b"4294967295\0", "IMAX"),
                              (L.R_I123, b"1234567890\0", "I123"),
                              (L.R_I7, b"7\0", "I7"), (L.R_SLASH, b"/", "SLASH"),
                              (L.R_PREFIXE_M1, L.CORPUS_PREFIXE_M1, "PREFIXE_M1"),
                              (L.R_OK, b" OK\n", "OK"), (L.R_KO, b" KO\n", "KO"),
                              (L.R_J_PREF, L.CORPUS_J_PREF, "J_PREF"),
                              (L.R_J_SUFF, L.CORPUS_J_SUFF, "J_SUFF"),
                              (L.R_J2_MARK, L.CORPUS_J2_MARK, "J2_MARK")):
        if img[rva:rva + len(attendu)] != attendu:
            raise EchecBuild(f"fixture {nom} @ {rva:#x} divergente du plan")
    # le staging et la table (R10) : conformes au build
    st, taille, somme = octets_staging(staging)
    if img[L.R_STAGING_CORPUS:L.R_STAGING_CORPUS + taille] != st:
        raise EchecBuild("le staging de l'image != le staging assemblé (R10)")
    rva_t, taille_t, somme_t = struct.unpack_from("<IIQ", img, L.R_TAB_SUM_CORPUS)
    if (rva_t, taille_t, somme_t) != (L.R_STAGING_CORPUS, taille, somme):
        raise EchecBuild(f"table d'intégrité {(rva_t, taille_t, somme_t)} != build "
                         f"{(L.R_STAGING_CORPUS, taille, somme)} (R10)")
    lignes.append(f"[R10] staging {taille} o @ {L.R_STAGING_CORPUS:#x}, somme "
                  f"{somme:#x} — la porte AVANT tout effet")
    # la croissance : ebreak à l'état image (le remplaçant y sera copié)
    if img[L.A_CROISSANCE:L.A_CROISSANCE + 16] != struct.pack("<I", L.EBREAK) * 4:
        raise EchecBuild("la croissance n'est pas ebreak à l'état image (le plan)")
    return lignes


# --- Oracle d'exécution : qemu-riscv64, l'exécuteur du jalon (D149) -----------------

def chemin_qemu() -> str:
    """L'exécuteur du jalon : qemu-riscv64 (réserve instrumentale D149).

    L'installation est une PROCÉDURE du dépôt (outils/installer_qemu.sh —
    extraction locale sans privilèges, le binaire est un instrument
    gitignoré) ; l'environnement peut fournir le sien par QEMU_RISCV64.
    """
    env = os.environ.get("QEMU_RISCV64")
    if env and os.path.isfile(env) and os.access(env, os.X_OK):
        return env
    extrait = os.path.join(ICI, ".tmp", "qemu-extract", "usr", "bin",
                           "qemu-riscv64")
    if os.path.isfile(extrait) and os.access(extrait, os.X_OK):
        return extrait
    raise EchecBuild(
        "qemu-riscv64 ABSENT — le prérequis du jalon (fiche § 10, re-vérifié "
        "AVANT usage) : lancez riscv/outils/installer_qemu.sh ou QEMU_RISCV64")


class Terrain:
    """Exécution du corpus sous qemu-riscv64 (TCG — le noyau et les syscalls
    sont RÉELS, l'ISA est exécutée par l'émulateur : la réserve
    instrumentale D149 est PORTÉE par chaque verdict)."""

    def __init__(self, img: bytes, extra: list[str] | None = None,
                 dossier: str | None = None):
        self.qemu = chemin_qemu()
        self.extra = extra or []
        parent = dossier or os.path.join(ICI, ".tmp")
        os.makedirs(parent, exist_ok=True)
        self.dossier = tempfile.mkdtemp(prefix="corpus-rv-", dir=parent)
        self.chemin = os.path.join(self.dossier, "corpus")
        with open(self.chemin, "wb") as f:
            f.write(img)
        os.chmod(self.chemin, 0o755)

    def lancer(self) -> tuple[bytes, bytes, int]:
        cmd = [self.qemu] + self.extra + [self.chemin]
        try:
            r = subprocess.run(cmd, capture_output=True, timeout=30)
            return r.stdout, r.stderr, r.returncode
        except subprocess.TimeoutExpired:
            return b"", b"<timeout>", -99

    def nettoyer(self):
        import shutil
        shutil.rmtree(self.dossier, ignore_errors=True)


# LE RITUEL DE PARITÉ (corpus-13:R1 Q1) — les DEUX lignes exactes, octet
# pour octet : la ligne du patrimoine (la parité § 8.3 — le MÊME observable
# que l'instance Windows scellée et l'instance x86-64-linux) puis la ligne
# de journal du verdict. Terminateur \n (le profil Linux).
LIGNE_PATRIMOINE = b"TRIADE M1 : minilibc 21/21 OK\n"
LIGNE_JOURNAL = b"corpus : autotest 21 vecteurs\n"
SORTIE_ATTENDUE = LIGNE_PATRIMOINE + LIGNE_JOURNAL

# HORS-CHEMIN de la falsification : tcp-07 n'est PAS dans le flot du
# principal (le rituel ne le touche pas — I1 de corpus-13) : AUCUNE
# corruption d'un bloc non exécuté ne peut dévier l'artefact (le fait de
# plan, pas une vacuité de l'oracle). Le patch est épuisé par SON
# scénario au chantier (c) (apply/rollback/effet, intégrité R10, refus).
HORS_CHEMIN = {"f71012"}


def oracle_qemu(img: bytes, code: dict) -> dict:
    # — 6 exécutions nominales : les deux lignes exactes + code 0
    t = Terrain(img)
    try:
        for _ in range(6):
            sortie, err, code_sortie = t.lancer()
            if code_sortie != 0 or err or sortie != SORTIE_ATTENDUE:
                raise EchecBuild(
                    f"oracle qemu : code={code_sortie} sortie={sortie!r} "
                    f"err={err!r} — le rituel de parité diverge (les DEUX "
                    f"lignes exactes attendues : {SORTIE_ATTENDUE!r})")
        # — l'indifférence à la base par bases forcées du CHARGEUR (la
        # preuve ne dépend JAMAIS d'un ASLR émulé — le constat d'instrument
        # D155 s'applique : qemu 10 ne randomise pas l'image PIE invitée)
        configurations_forcees = [
            ("-R 1G", ["-R", "1G"]),
            ("-R 4G", ["-R", "4G"]),
            ("-B 0x100000000 -R 2G", ["-B", "0x100000000", "-R", "2G"]),
        ]
        for nom_cfg, extra in configurations_forcees:
            tf = Terrain(img, extra=extra)
            try:
                sortie, err, code_sortie = tf.lancer()
                if code_sortie != 0 or err or sortie != SORTIE_ATTENDUE:
                    raise EchecBuild(
                        f"base forcée ({nom_cfg}) : code={code_sortie} "
                        f"sortie={sortie!r} — l'image n'est PAS indifférente "
                        f"à la base (le contrat I3 est rompu)")
            finally:
                tf.nettoyer()
        # — la falsification : la corruption d'un octet d'instruction fait
        # dévier sortie, code ou signal (zéro silence — non-vacuité) ;
        # l'octet muté est le PREMIER de chaque instruction (l'opcode),
        # essayée L'UNE APRÈS L'AUTRE jusqu'à la déviation — si TOUTES
        # passent silencieusement, l'oracle est VACUE et refuse
        essais, rompus = 0, 0
        detail = []
        for bid, _, fichier, rva, _ in L.BLOCS_CORPUS:
            if bid in HORS_CHEMIN:
                continue
            bloc = code[bid]
            # les instructions réelles du bloc : jusqu'au premier ret
            # inclus (corpus-13 n'a pas de ret — le rituel ne revient pas :
            # tout son code est le chemin)
            adresses = []
            for i in bloc["insns"]:
                adresses.append(i.address)
                if i.mnemonic == "ret":
                    break
            rompu = False
            for adresse in adresses:
                mutant = bytearray(img)
                mutant[adresse] ^= 0xFF              # l'octet d'opcode
                essais += 1
                tm = Terrain(bytes(mutant),
                             dossier=os.path.join(ICI, ".tmp", "falsif"))
                try:
                    sortie, err, code_sortie = tm.lancer()
                    observe = (code_sortie, sortie)
                    if observe != (0, SORTIE_ATTENDUE):
                        rompu = True
                        detail.append(f"{fichier} rompu à {adresse:#x} "
                                      f"(essai n°{essais}, code {code_sortie})")
                        break
                finally:
                    tm.nettoyer()
            if not rompu:
                raise EchecBuild(
                    f"falsification : {fichier} — {len(adresses)} mutations "
                    f"TOUTES silencieuses — oracle vacue (V3 : zéro silence)")
            rompus += 1
        attendus = len(L.BLOCS_CORPUS) - len(HORS_CHEMIN)
        return {"cas": 6, "falsification": essais, "rompus": rompus,
                "attendus": attendus, "detail": detail,
                "bases_forcees": [n for n, _ in configurations_forcees]}
    finally:
        t.nettoyer()


# --- La carte du corpus : le frag-con des TROIS profils (§ 8.3-4) --------------------

# La convention d'appel PAR BLOC, pour les TROIS profils — le paramétrage
# physique qui a quitté la couche I (D149-(3)). Chaque ligne : le contrat
# nomme, frag-con porte. La TROISIÈME colonne (psABI RV64) est née au
# présent chantier : la parité § 8.3 se lit SUR LES TROIS COLONNES.
CONVENTIONS = {
    "f71001": ("écrire : flux/tampon/longueur",
               "msx64 : rcx/rdx/r8, 4e-5e args pile, shadow 0x28, WriteFile IAT (BOOL)",
               "SysV : rdi/rsi/rdx, aucune zone d'accueil, sys_write 1 (rax brut)",
               "psABI : a0/a1/a2, ecall a7=64 asm-generic (a0 brut)"),
    "f71002": ("sortir : code",
               "msx64 : rcx, ExitProcess IAT", "SysV : rdi, sys_exit_group 231",
               "psABI : a0, ecall a7=94 asm-generic"),
    "f71003": ("memcpy : dst/src/n",
               "msx64 : rcx/rdx/r8 (pousse rdi/rsi — non volatils msx64)",
               "SysV : rdi/rsi/rdx (rep movsb en place)",
               "psABI : a0/a1/a2 — la boucle explicite (l'observable : les octets)"),
    "f71004": ("memcmp : ptr1/ptr2/n",
               "msx64 : rcx/rdx/r8", "SysV : rdi/rsi/rdx (repz cmpsb en place)",
               "psABI : a0/a1/a2 — bltu/beq au site, -1/0/+1 en a0"),
    "f71005": ("strlen : chaîne", "msx64 : rcx", "SysV : rdi",
               "psABI : a0 — le marcheur en t0, la longueur par sub"),
    "f71006": ("itoa : valeur/tampon",
               "msx64 : ecx/rdx, travail en rbx sauvegardé",
               "SysV : edi/rsi, travail aux volatils r8/r9",
               "psABI : a0/a1 — le masque u32 (slli/srli 32), remu/divu (M)"),
    "f71007": ("zone-alloc : taille/alignement", "msx64 : rcx/rdx",
               "SysV : rdi/rsi ; arène au plan (0x3000/0x3040, la géométrie m1)",
               "psABI : a0/a1 — la fenêtre s2=base+0x3400 (LE CENTRE, la "
               "leçon imm12) : le curseur s2-0x400, l'arène s2-0x3C0"),
    "f71008": ("zone-reset : —", "msx64 : —", "SysV : — (le curseur au plan)",
               "psABI : — (sd zero, le curseur s2-0x400)"),
    "f71009": ("memset : dst/valeur/n",
               "msx64 : rcx/dl/r8 (pousse rbx/rdi)",
               "SysV : rdi/sil/rdx (rep stosb en place)",
               "psABI : a0/a1/a2 — la boucle explicite, le marcheur en t0"),
    "f71010": ("autotest : — (appelé par le principal)",
               "msx64 : point d'entrée PE, WriteFile/ExitProcess IAT, \\r\\n, "
               "terminaison par le bloc",
               "SysV : appelé par corpus-13, écrire fd 1, \\n, N rendu (rax) — "
               "le principal termine",
               "psABI : appelé par corpus-13 (jal), écrire fd 1, \\n, N rendu "
               "(a0) — D150 : s0=N/s7=ptr/s4=tampon/s5=courant, sauvegardés (s3 est EXCLUSIVEMENT la fenêtre de tcp-07)"),
    "f71011": ("journal : préfixe/longueur/valeur/suffixe/longueur",
               "msx64 : rcx/rdx/r8/r9 + 5e pile, Enter/LeaveCriticalSection IAT "
               "(initialisée par tcp-12), WriteFile (BOOL)",
               "SysV : rdi/rsi/rdx/rcx/r8 (cinq registres), verrou tournant "
               "lock xchg au plan (né déverrouillé), écrire (rax brut)",
               "psABI : a0/a1/a2/a3/a4 (cinq registres) — verrou tournant "
               "amoswap.d (l'extension A, le portage du lock xchg ; la "
               "restitution sd simple — mono-fil, fiche § 5), écrire (a0 brut)"),
    "f71012": ("patch : mode",
               "msx64 : ecx, VirtualProtect IAT x2, PAGE 0x40/0x20, zone "
               "d'accueil 0x28 (D41), cible echo 0x4600/croissance 0x4680",
               "SysV : edi, sys_mprotect x2 (10), PROT 0x7/0x5, aucune zone "
               "d'accueil, cible journal 0x1840/croissance 0x1D80",
               "psABI : a0 — la fenêtre s3=base+0x1840 (SA paire à LUI), "
               "mprotect 226 asm-generic x2, séquence § 5 : copie → fence "
               "rw,rw → LA BASCULE (un mot jal, construit en registres) → "
               "fence.i → RX ; .protger local (jal)"),
    "f71013": ("principal : l'ABI de démarrage du profil",
               "msx64 : point d'entrée PE (chargeur, PEB) — hello-01:R1, "
               "classe C (l'orchestration d'entrée EST la plateforme)",
               "SysV : _start ELF, [rsp]=argc/argv, rsp ≡ 0 mod 16 sans "
               "adresse de retour — le rituel de parité",
               "psABI : _start ELF, [sp]=argc/argv, sp ≡ 0 mod 16 — LES DEUX "
               "ANCRES posées d'emblée (s1 rodata, s2 bss CENTRE — la leçon "
               "imm12), N traverse en s0 (D150)"),
}


def fragments_clairs(code, img, verrous, specs, verdict, compteurs, journal,
                     staging, empreintes_I, porte, version=None):
    if version is None:
        version = L.VERSION_DEV2
    loc = ["[carte-frag] nom=frag-loc generation=1"]
    for bid, sid, _, rva, slot in L.BLOCS_CORPUS:
        loc.append(f"[bloc] id={bid} spec={sid} cible={L.CORPUS_PROFIL} "
                   f"addr={rva:#x} size={slot} v=1 etat=scelle "
                   f"(RVA — PIE : la base est choisie par le chargeur)")
    loc.append(f"[staging] id=f71991 pour={L.A_CROISSANCE:#x} "
               f"addr={L.R_STAGING_CORPUS:#x} taille={len(staging['octets'])}")
    loc.append(f"[ancres] s1=base+0x0 (rodata 0x140-0x580) ; "
               f"s2=base+0x3400 (bss CENTRE — LA LEÇON imm12 : la base "
               f"0x3000 mettrait le verrou 0x3800 à +0x800, hors plage de "
               f"UN ; curseur -0x400, arène -0x3C0, verrou +0x400) ; "
               f"s3=base+0x1840 (tcp-07, l'entrée du journal — SA paire à lui)")
    loc.append(f"[zones] io=0x1000-0x1080 libc=0x1080-0x1340 app=0x1340-0x1D80 "
               f"croissance={L.A_CROISSANCE:#x}-{L.A_CROISSANCE + L.CROISSANCE_TAILLE:#x} "
               f"rodata=0x140-0x560 bss=0x3000-0x3818")
    loc.append(f"[bss] curseur={L.R_CURSEUR_CORPUS:#x} arene={L.ARENE_BASE_CORPUS:#x} "
               f"verrou={L.R_VERROU:#x} etat_patch={L.R_ETAT_PATCH_CORPUS:#x} "
               f"entree_sauvee={L.R_ENTREE_SAUVEE:#x}")

    con = ["[carte-frag] nom=frag-con generation=1",
           "# La convention d'appel PAR BLOC, pour les TROIS profils (spec § 8.3-4 —",
           "# la granularité D149-(3) : la couche I nomme, frag-con porte le physique).",
           "# La TROISIÈME colonne est née au chantier M7-(b) : la parité inter-ISA",
           "# se lit sur les TROIS colonnes (§ 8.3 — à la paramétrisation près)."]
    for bid in code:
        spec = specs[bid]["texte"]
        sig = re.search(r"Intention : (.+?)\n", spec).group(1)
        nom, win, sysv, rv = CONVENTIONS[bid]
        con += [f"[bloc] id={bid}",
                f"  sig : {sig[:96]}",
                f"  args : {nom}",
                f"  x86-64-win11-pe : {win}",
                f"  x86-64-linux-elf64 : {sysv}",
                f"  riscv64-linux-elf64 : {rv}"]
    con.append("[alignement] x86-64 : rsp ≡ 8 mod 16 à l'entrée de tout bloc "
               "appelé ; psABI : sp ≡ 0 mod 16 au point d'appel (jal ne pousse "
               "rien, le lien vit dans ra) ; l'exception _start : sp ≡ 0 sans "
               "adresse de retour (les deux ABI de démarrage Linux)")
    con.append("[volatilite] msx64 : RAX,RCX,RDX,R8-R11 ; SysV : "
               "RAX,RCX,RDX,RSI,RDI,R8-R11 ; psABI : t0-t6,a0-a7 (x5-7,x10-17)"
               " — les non volatils psABI s0-s11 (ra par convention) ; t1 = "
               "registre de travail du projet (fiche § 2), respecté par "
               "contrat dans TOUT le corpus (jamais touché)")
    con.append("[zero-rouge] msx64 : zone rouge 128 o SOUS rsp interdite aux "
               "appelés ; SysV : idem ; psABI : AUCUNE zone rouge — le piège "
               "INVERSE : stocker sous sp est interdit à TOUS (frag-con)")

    prf = ["[carte-frag] nom=frag-prf generation=1"]
    for bid, _, fichier, _, _ in L.BLOCS_CORPUS:
        with open(os.path.join(ICI, "notation", fichier + ".asm"), "rb") as f:
            emp = sha(f.read())
        crist = min(compteurs.get(bid, 1), 10)
        prf += [f"[bloc] id={bid} etat={'cristallise' if crist >= 10 else 'scelle'} "
                f"crist={crist}/10",
                f"  vecteurs : roundtrip=ok structure=ok notation={emp}",
                f"  differentiel : qemu ok (rituel 6/6, code 0 ; falsification "
                f"{verdict['falsification']} mutations, zéro silence)"]
    prf.append("[couche-I] " + " ; ".join(
        f"{n}={e[:12]}" for n, e in sorted(empreintes_I.items())))
    prf.append(f"[verifications] runs=" + str(len(journal)))
    prf += ["  " + r for r in journal[-12:]]

    bld = ["[carte-frag] nom=frag-bld generation=1"]
    for bid, _, _, rva, slot in L.BLOCS_CORPUS:
        bld.append(f"[bloc] id={bid} addr={rva:#x} empreinte={sha(code[bid]['slot'])}")
    bld += [
        f"[build] artefact=corpus version={version} profil={L.CORPUS_PROFIL} "
        f"taille={len(img)} empreinte={sha(img)}",
        f"  outils : ASSEMBLEUR MAISON as_rv64 (RV64IMA+Zifencei+AMO-amoswap, "
        f"4 o, formats R/I/S/B/U/J) + capstone "
        f"{capstone.cs_version()[0]}.{capstone.cs_version()[1]} JUGE UNIQUE ; "
        f"verrous={len(verrous)} ; symboles vérifiés",
        f"  porte round-trip : AVANT {porte['avant']} textes + INVERSE "
        f"{porte['inverse']} encodages légaux — 100 % (l'extension A couverte "
        f"au chantier — amoswap)",
        f"  durcissement : ET_DYN/PIE, e_machine {L.E_MACHINE:#x} (EM_RISCV), "
        f"e_flags 0, 3 segments R/RX/RW, PT_GNU_STACK sans X, W^X depuis les "
        f"phdr — hérité du chantier M7-(a)",
        f"  corpus : 12 blocs du patrimoine (les MÊMES fichiers canoniques "
        f"unix/I/ — chargés, jamais copiés) + corpus-13 ; staging "
        f"{len(staging['octets'])} o (journal v2 POUR {L.A_CROISSANCE:#x}) ; "
        f"diff nul VERT (4 recoupements)",
        f"  oracle : qemu-riscv64 (réserve instrumentale D149 — TCG, noyau "
        f"et syscalls réels) — rituel 6/6 les DEUX lignes octet pour octet "
        f"code 0 ; bases forcées "
        + " / ".join(verdict["bases_forcees"])
        + " VERTES (indifférence à la base) ; falsification "
        f"{verdict['falsification']} mutations, {verdict['rompus']}/"
        f"{verdict['attendus']} blocs rompus (zéro silence ; tcp-07 "
        "hors-chemin du rituel — le scénario du patch est le chantier (c))",
    ]
    return {n: ("\n".join(l) + "\n").encode("utf-8")
            for n, l in (("frag-loc", loc), ("frag-con", con),
                         ("frag-prf", prf), ("frag-bld", bld))}


def verrou_croise(code: dict, img: bytes) -> int:
    """R8 : signature + empreintes re-vérifiées depuis le disque."""
    entete, fragments, signature, pub = cm.lire_carte()
    cm.verifier_signature(pub, entete, fragments, signature)
    phrase, graine = cm.charger_secrets(interactif=False)
    maitre = cm.cle_maitresse(phrase)
    bld = cm.dechiffrer_fragment(maitre, "frag-bld", fragments["frag-bld"]).decode()
    n = 0
    for bid, _, _, rva, slot in L.BLOCS_CORPUS:
        m = re.search(rf"\[bloc\] id={bid} addr=\S+ empreinte=(\S+)", bld)
        if not m or m.group(1) != sha(img[rva:rva + slot]):
            raise EchecBuild(f"verrou croisé : {bid} divergent (R8)")
        n += 1
    return n


def construire_carte(code, img, verrous, specs, verdict, compteurs, journal,
                     staging, empreintes_I, porte, version=None):
    clairs = fragments_clairs(code, img, verrous, specs, verdict, compteurs,
                              journal, staging, empreintes_I, porte,
                              version=version)
    phrase, graine = cm.charger_secrets(interactif=False)
    maitre = cm.cle_maitresse(phrase)
    fragments = {n: cm.chiffrer_fragment(maitre, n, clairs[n]) for n in cm.FRAGMENTS}
    prive, pub = cm.paire_cles(graine)
    entete = cm.construire_entete(empreinte_racine(fragments))
    signature = cm.signer(prive, entete, fragments)
    cm.ecrire_carte(entete, fragments, signature, pub)


# --- L'anti-rollback du jalon : ABSENT ≠ ILLISIBLE (D151) ---------------------------

BALISES_LIGNEE = {L.VERSION_DEV1, L.VERSION_DEV2, L.VERSION_RC1,
                  L.VERSION_FINALE}


def _anti_rollback() -> None:
    """La carte du corpus : ABSENTE = première construction ; PRÉSENTE et
    illisible = REFUS (l'incident de l'état zéro — jamais « illisible »
    traité comme « absente »). Dev : la reconstruction libre est permise
    tant qu'aucune balise rc/final n'est posée. SCELLÉE (rc/final — le
    chantier (c)) : reconstruction INTERDITE (R6) ; la balise courante doit
    vivre au registre de la lignée (plancher 0.8.0-dev.1)."""
    fragments_pres = any(os.path.exists(os.path.join(cm.CARTE_DIR, n + ".bin"))
                         for n in cm.FRAGMENTS)
    if not fragments_pres:
        return
    try:
        _, fragments, _, _ = cm.lire_carte()
        phrase, _ = cm.charger_secrets(interactif=False)
        maitre = cm.cle_maitresse(phrase)
        bld = cm.dechiffrer_fragment(maitre, "frag-bld", fragments["frag-bld"]).decode()
    except cm.ErreurCarte as e:
        raise EchecBuild(
            f"carte du corpus PRÉSENTE et illisible ({e}) — un état présent "
            f"et indéchiffrable est un REFUS, jamais une permission (absent "
            f"≠ illisible, la garde D151)") from e
    m = re.search(r"\[build\] artefact=corpus version=(\S+)", bld)
    if not m:
        raise EchecBuild("frag-bld : balise du corpus ILLISIBLE — refus "
                         "(absent ≠ illisible, la garde D151)")
    version_existante = m.group(1)
    if version_existante not in BALISES_LIGNEE:
        raise EchecBuild(f"balise {version_existante} HORS REGISTRE de la lignée "
                         f"{sorted(BALISES_LIGNEE)} — plancher 0.8.0-dev.1, "
                         f"anti-rollback R10 (fail-closed)")
    if "-rc" in version_existante or re.fullmatch(r"\d+\.\d+\.\d+", version_existante):
        raise EchecBuild(f"carte scellée ({version_existante}) : reconstruction "
                         f"interdite — procédure lourde R6 ou nouvelle version")


def tableau_de_bord(img, verrous, verdict, phdr_lignes, empreintes_I,
                    porte, version=None) -> str:
    if version is None:
        version = L.VERSION_DEV2
    return "\n".join([
        "[tableau] jalon=M7-(b) artefact=corpus version=" + version,
        "  profil                       : " + L.CORPUS_PROFIL
        + " (fiche — la parité inter-ISA du patrimoine)",
        "  moteur_notation              : ASSEMBLEUR MAISON as_rv64 "
        "(RV64IMA+Zifencei, formats R/I/S/B/U/J, 4 o, SANS extension C ; "
        "AMO amoswap au chantier — l'extension A) ; capstone JUGE UNIQUE",
        "  porte_roundtrip              : VERTE — " + str(porte["avant"])
        + " textes (avant) + " + str(porte["inverse"])
        + " encodages légaux (inverse), 100 % — l'extension A couverte",
        "  blocs_avec_spec_a_jour        : 13/13 : audit I->C->B (specs, carte, "
        "artefact) — les MÊMES fichiers canoniques que M6 (chargés)",
        "  chaines_I_C_B_tests           : 13/13 : " + str(len(verrous))
        + " verrous PASS (structurels) ; diff nul VERT (4 recoupements)",
        "  construction                 : 0 erreur / 0 avertissement : build script",
        "  format_durci                 : ET_DYN (PIE), e_machine 0xf3 "
        "(EM_RISCV), e_flags 0, 3 segments R/RX/RW, PT_GNU_STACK RW sans X, "
        "W^X constaté depuis les phdr (héritage M7-(a)), .bss pur, garde "
        "anti-C (taille 4 par instruction)",
        "  corpus_paritaire             : 12 blocs du patrimoine M0-M5 (les "
        "révisions R+1 de unix/I/, LES MÊMES fichiers canoniques — aucune "
        "copie) + corpus-13 (domaine neuf, modèle ah-09) ; GÉOMÉTRIE MIROIR "
        "du plan unix (D8) : les MÊMES RVA, les MÊMES fixtures",
        "  diff_nul                     : 4 recoupements VERT — canoniques "
        "empreintés ; observables R1<->R+1 (chaîne M6 rejouée) ; "
        + str(len(ETAT_ZERO_GARDE))
        + " scellés octet-identiques à l'état zéro ; parité § 8.3 par exécution",
        "  contrat_erreurs               : la propagation des verdicts bruts "
        "(écrire/tcp-11 Q2) et les codes nommés 1-5 (tcp-07 Q5) — le style "
        "des CONTRATS du patrimoine ; table asm-generic (write 64, "
        "mprotect 226, exit_group 94) avec garde anti-table-x86 (1/10/231 "
        "REFUSÉS nommément)",
        "  patch_a_chaud                : tcp-07 instancié (mprotect 226, "
        "cible = l'entrée du journal, staging journal v2 embarqué, séquence "
        "§ 5 : fence rw,rw + fence.i + la bascule UN mot) — le scénario "
        "complet (apply/effet/rollback) est le chantier (c)",
        "  tests_differentiels          : oracle qemu (réserve D149 — TCG, "
        "syscalls réels) : rituel 6/6 les DEUX lignes octet pour octet, "
        "code 0 ; bases forcées "
        + ", ".join(verdict["bases_forcees"])
        + " VERTES ; falsification " + str(verdict["falsification"])
        + " mutations, " + str(verdict["rompus"]) + "/" + str(verdict["attendus"])
        + " blocs rompus (zéro silence)",
        "  couche_I                     : " + str(len(empreintes_I))
        + " fichiers unix/I/ empreintés dans frag-prf (la même couche que "
        "M6 — la TROISIÈME instanciation)",
        "  defauts_ouverts              : 0",
        "  preversions                  : " + version
        + " conforme (R10 : monotonie, plancher " + hex(L.VERSION_U64_MIN)
        + " ; la sonde 0.8.0-dev.1 INTACTE)",
        "  artefact                     : " + str(len(img)) + " octets ; "
        "empreinte sha256:" + sha(img)[:24] + "…",
        "  verrou_croise                : 13 empreintes + signature Ed25519 (R8)",
    ]) + "\n" + "\n".join("  " + l for l in phdr_lignes) + "\n"


# --- Construction / vérification -----------------------------------------------------

CHEMIN_ARTIFACT = os.path.join(ICI, "corpus")

# L'état zéro mesuré à l'ouverture du chantier (diff_nul_corpus — la garde
# du diff nul : le chantier ne touche AUCUN scellé)
from diff_nul_corpus import ETAT_ZERO as ETAT_ZERO_GARDE  # noqa: E402


def construire(graine: int) -> int:
    print("=== M7-(b) : le corpus paritaire (riscv/, D149) — la TROISIÈME "
          "instanciation de la même couche I ===")
    t0 = time.perf_counter()
    _anti_rollback()

    print("[constat] qemu-riscv64 opérationnel (" + chemin_qemu() + ") — "
          "réserve instrumentale D149 nommée dans chaque verdict")

    porte = franchir_porte()
    print(f"[porte] round-trip 100 % : AVANT {porte['avant']} textes + INVERSE "
          f"{porte['inverse']} encodages légaux — capstone juge unique "
          f"(l'extension A couverte au chantier : amoswap)")

    diff = subprocess.run([sys.executable,
                           os.path.join(ICI, "diff_nul_corpus.py")],
                          capture_output=True, text=True)
    derniere = diff.stdout.strip().splitlines()
    print(derniere[-1] if derniere else "(diff nul : sans sortie)")
    if diff.returncode != 0:
        print(diff.stdout)
        raise EchecBuild("le diff nul n'est pas VERT — la chaîne s'arrête "
                         "(le critère du chantier est une garde, pas un vœu)")

    specs = charger_couche_I()
    print(f"[I] {len(specs)} specs chargées — LES MÊMES fichiers canoniques "
          f"que l'instance x86-64 (unix/I/, chargés jamais copiés)")

    code, staging = assembler_tout()
    total_insns = sum(len(code[b]["insns"]) for b in code)
    total_code = sum(len(code[b]["octets"]) for b in code)
    print(f"[R5] 13 blocs, {total_insns} instructions, {total_code} o de code — "
          f"round-trip assembleur maison/capstone 100 %")

    verrous = oracle_structurel(code, staging)
    n_symboles = verifier_symboles()
    print(f"[oracle] structurel : {len(verrous)} verrous PASS ; "
          f"{n_symboles} symboles @ vérifiés contre layout (leçon C1) ; "
          f"garde anti-table-x86 VIVANTE")

    img = composer_elf(code, staging)
    phdr_lignes = valider_elf(img, staging)
    for l in phdr_lignes[:3]:
        print("  " + l)
    print(f"[ELF] corpus : {len(img)} o (ET_DYN EM_RISCV, entrée "
          f"{L.CORPUS_ENTREE:#x} RVA, 13 blocs + staging "
          f"{len(staging['octets'])} o + croissance ebreak)")

    verdict = oracle_qemu(img, code)
    print(f"[oracle] qemu (réserve D149) : rituel 6/6 — les DEUX lignes octet "
          f"pour octet, code 0 (la parité § 8.3 PAR EXÉCUTION) ; bases "
          f"forcées " + ", ".join(verdict["bases_forcees"])
          + " VERTES ; falsification " + str(verdict["falsification"])
          + " mutations, " + str(verdict["rompus"]) + "/"
          + str(verdict["attendus"]) + " blocs rompus (zéro silence)")

    with open(CHEMIN_ARTIFACT, "wb") as f:
        f.write(img)
    os.chmod(CHEMIN_ARTIFACT, 0o755)

    journal = [f"run qemu date={datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} "
               f"build={L.VERSION_DEV2} rituel=6/6 falsif={verdict['falsification']}"]
    compteurs = {bid: 1 for bid, _, _, _, _ in L.BLOCS_CORPUS}
    construire_carte(code, img, verrous, specs, verdict, compteurs, journal,
                     staging, _empreintes_I(), porte)
    print("[carte] génération 1 écrite : 4 fragments chiffrés (SIXIÈME sel "
          "distinct), signature Ed25519, frag-con TROIS PROFILS par bloc "
          "(§ 8.3-4)")
    nb = verrou_croise(code, img)
    print(f"[R8] verrou croisé : {nb} empreintes re-vérifiées, signature OK")
    with open(os.path.join(cm.CARTE_DIR, "tableau-de-bord.txt"), "w",
              encoding="utf-8") as f:
        f.write(tableau_de_bord(img, verrous, verdict, phdr_lignes,
                                _empreintes_I(), porte))
    print("[tableau] tableau de bord écrit (carte-corpus/tableau-de-bord.txt)")
    print(f"[B] corpus : sha256:{sha(img)}")
    print(f"=== M7-(b) dev (oracles verts) : {L.VERSION_DEV2} — "
          f"{round(time.perf_counter() - t0, 1)} s ===")
    return 0


def verifier(graine: int) -> int:
    print(f"=== M7-(b) : re-vérification complète (R5/R8) ===")
    # La balise de la carte est PRÉSERVÉE (modèle m5/D147) : un scellé ne se
    # revertit pas — la re-vérification re-signe la carte SOUS sa balise.
    phrase, _ = cm.charger_secrets(interactif=False)
    maitre = cm.cle_maitresse(phrase)
    _, fragments, _, _ = cm.lire_carte()
    bld = cm.dechiffrer_fragment(maitre, "frag-bld", fragments["frag-bld"]).decode()
    manifeste_v = next(
        (dict(re.findall(r"(\w+)=(\S+)", l)).get("version") for l in bld.splitlines()
         if "artefact=corpus" in l), "?")
    version = manifeste_v if manifeste_v != "?" else L.VERSION_DEV2
    print(f"[balise] la carte vit sous {version} (préservée — la re-vérification "
          f"ne la déplace pas)")
    porte = franchir_porte()
    print(f"[porte] round-trip 100 % re-joué : AVANT {porte['avant']} + "
          f"INVERSE {porte['inverse']}")
    code, staging = assembler_tout()
    verrous = oracle_structurel(code, staging)
    verifier_symboles()
    with open(CHEMIN_ARTIFACT, "rb") as f:
        img = f.read()
    phdr = valider_elf(img, staging)
    for bid, _, _, rva, slot in L.BLOCS_CORPUS:
        if img[rva:rva + slot] != code[bid]["slot"]:
            raise EchecBuild(f"{bid} : notation et artefact divergent (R5)")
    verdict = oracle_qemu(img, code)
    print(f"[oracle] qemu : rituel 6/6 ; bases forcées VERTES ; falsification "
          f"{verdict['falsification']} mutations (zéro silence)")
    # Cristallisation : compteurs incrémentés dans frag-prf (R6)
    prf = cm.dechiffrer_fragment(maitre, "frag-prf", fragments["frag-prf"]).decode()
    compteurs, journal = {}, []
    for ligne in prf.splitlines():
        if ligne.startswith("[bloc]"):
            champs = dict(re.findall(r"(\w+)=(\S+)", ligne))
            compteurs[champs["id"]] = int(
                re.match(r"(\d+)/10", champs.get("crist", "1/10")).group(1))
        elif ligne.startswith("  run "):
            journal.append(ligne.strip())
    for bid, _, _, _, _ in L.BLOCS_CORPUS:
        compteurs[bid] = min(compteurs.get(bid, 0) + 1, 10)
    journal.append(f"run qemu date={datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} "
                   f"verif rituel=6/6 falsif={verdict['falsification']}")
    specs = charger_couche_I()
    construire_carte(code, img, verrous, specs, verdict, compteurs, journal,
                     staging, _empreintes_I(), porte, version=version)
    nb = verrou_croise(code, img)
    crist = ", ".join(f"{b}={compteurs.get(b, 0)}/10" for b, _, _, _, _ in L.BLOCS_CORPUS)
    print(f"[R6] cristallisation : {crist}")
    print(f"[R8] verrou croisé : {nb} empreintes conformes")
    with open(os.path.join(cm.CARTE_DIR, "tableau-de-bord.txt"), "w",
              encoding="utf-8") as f:
        f.write(tableau_de_bord(img, verrous, verdict, phdr, _empreintes_I(),
                                porte, version=version))
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    try:
        if "--verifier" in args:
            graine = int(args[args.index("--graine") + 1]) if "--graine" in args else 2
            sys.exit(verifier(graine))
        graine = int(args[args.index("--graine") + 1]) if "--graine" in args else 1
        sys.exit(construire(graine))
    except (EchecBuild, cm.ErreurCarte) as exc:
        print(f"ECHEC (fail-closed) : {exc}", file=sys.stderr)
        sys.exit(1)
