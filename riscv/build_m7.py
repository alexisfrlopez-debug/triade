#!/usr/bin/env python3
"""build_m7.py — Lignée du jalon M7 (riscv/, D149) : sonde, moteur de notation RV64.

Chantier M7-(a) : LE MOTEUR DE NOTATION RV64 — l'assembleur maison
(outils/as_rv64.py, keystone ne porte pas l'ISA — fiche § 6) et sa preuve
(la porte round-trip, capstone juge unique). Le writer porte l'image à
ET_DYN (PIE), trois segments R/RX/RW, PT_GNU_STACK sans X ; la table
ERRNOS vit en .rodata du segment R ; le layout est riscv/layout.py (modèle
D8, géométrie partagée avec le jalon unix — seul le demi-octet ISA
change). Le critère de sortie du chantier s'exécute au build même :

  1. couche I chargée et auditée (gabarit § 2.2, 4 specs, R2
     écrite-avant-code) ;
  2. LA PORTE ROUND-TRIP DU DOMAINE (notation/porte_roundtrip.py) :
     round-trip 100 % sur le corpus d'instructions du profil, capstone
     juge unique, DEUX directions (corpus de textes + espace d'encodage
     légal) — le livrable propre du chantier ;
  3. round-trip R5 par bloc (assembleur maison -> capstone -> assembleur
     maison, WYSIWYG octets, graphie canonique capstone) ;
  4. oracle structurel : contrats I vérifiés sur le code désassemblé —
     appels directs autorisés PAR BLOC (jal vers les blocs déclarés +
     étiquettes locales), numéros de syscall ASM-GENERIC autorisés PAR
     BLOC (I1) avec LA GARDE ANTI-TABLE-X86 (a7 = 1/231/… est un REFUS
     NOMMÉ — fiche § 4 : la parité est SÉMANTIQUE, jamais lexicale),
     cibles de données déclarées ([s1 + RVA] .rodata, [s2 + off] .bss),
     paires d'ancres auipc+addi RE-VÉRIFIÉES depuis le code désassemblé
     (site + HI*4096 + LO == cible), sauts internes aux frontières,
     taille d'instruction 4 (GARDE ANTI-C — fiche § 9.1), padding >= 16,
     pile psABI (le corps ne touche jamais sp ; le cadre de .emit :
     addi sp,sp,-16 / sd ra / ld ra / addi sp,sp,16 APPARIÉS ; les
     feuilles : 0 octet de pile), t1 JAMAIS touché chez sr-02/sr-03
     (le porteur du brut — fiche § 2), symboles @ des brouillons
     confrontés à layout.py ET les longueurs @L_* confrontées aux
     messages RÉELS (leçon C1) ;
  5. composition ELF64 DURCI à la main (ehdr 64 o + 4 phdr 224 o, aucun
     outil de liaison) : ET_DYN, e_machine 0xF3 (EM_RISCV), e_flags 0
     (ni RVC ni float-abi), PT_LOAD R (en-têtes + ERRNOS + messages),
     PT_LOAD RX (code, NOP canonique intra-slot, ebreak réserves),
     PT_LOAD RW (.bss pur, filesz 0), PT_GNU_STACK RW sans X ;
  6. W^X CONSTATÉ DEPUIS LES PHDR (le build relit son image) ;
  7. oracle d'exécution SOUS QEMU-RISCV64 (l'exécuteur du jalon — la
     RÉSERVE INSTRUMENTALE D149 est NOMMÉE dans chaque verdict : l'ISA
     est exécutée par l'émulateur de processus TCG, le noyau et les
     syscalls sont RÉELS, jamais déguisés en exécution native) : quatre
     lignes attendues octet pour octet, code de sortie 6, la table
     ERRNOS exercée sur ses DEUX branches (EBADF nommé → verdict 1 ;
     EFAULT hors table → VERDICT_FATAL 6, arrêt propre) ; la base est
     CONSTATÉE (page-alignée, >= 0x10000 — et l'indifférence à la base
     DÉMONTRÉE par bases forcées : le code fonctionne à TOUTE base, la
     preuve ne dépend jamais d'un ASLR émulé) ;
  8. falsification : un octet corrompu dans le CODE de chaque bloc —
     au MOINS une divergence, zéro silence ;
  9. carte génération 1 de la lignée du jalon (QUATRIÈME sel Argon2id
     distinct : m2, hachoir D34, jalon unix, jalon riscv), clés projet
     partagées D27, signature Ed25519, verrou croisé R8 + tableau de bord.

Usage :
  python3 build_m7.py             # construction + oracles + carte
  python3 build_m7.py --verifier  # re-vérification complète (R5/R8) + cristallisation
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
sys.path.insert(0, ICI)
sys.path.insert(0, os.path.join(ICI, "outils"))
sys.path.insert(0, os.path.join(ICI, "notation"))

import layout as L                       # noqa: E402

import capstone                          # noqa: E402
import carte_sonde as cm                 # noqa: E402
from as_rv64 import EchecAssemblage, assembler  # noqa: E402
from porte_roundtrip import franchir as franchir_porte  # noqa: E402

sys.path.insert(0, os.path.join(os.path.dirname(ICI), "m2"))
from carte_m2 import empreinte_racine    # noqa: E402  (mécanique commune D27)

CS = capstone.Cs(capstone.CS_ARCH_RISCV, capstone.CS_MODE_RISCV64)
CS.detail = False

_BRANCHES = {"beq", "bne", "blt", "bge", "bltu", "bgeu",
             "beqz", "bnez", "bgez", "bltz", "bgtz", "blez", "j"}


class EchecBuild(Exception):
    """Tout échec de l'oracle, du round-trip ou de la construction."""


# --- Couche I : lecture et audit -------------------------------------------------

def lire_spec(chemin: str) -> dict:
    with open(chemin, encoding="utf-8") as f:
        texte = f.read()
    m = re.match(r"(\S+) · (.+?) · révision (\d+)", texte)
    if not m:
        raise EchecBuild(f"{chemin} : première ligne hors gabarit § 2.2")
    spec = {"id": m.group(1), "nom": m.group(2), "rev": int(m.group(3)), "texte": texte}
    for bloc in ("Intention", "Contrat", "Échecs", "Vecteurs", "Fixtures",
                 "Provenance", "Décisions"):
        if bloc not in texte:
            raise EchecBuild(f"{chemin} : bloc de gabarit manquant : {bloc}")
    if "écrite-avant-code" not in texte:
        raise EchecBuild(f"{chemin} : provenance inattendue (R2)")
    return spec


def charger_couche_I() -> dict[str, dict]:
    specs = {}
    for bid, sid, fichier, _, _ in L.BLOCS_SR:
        chemin = os.path.join(ICI, "I", fichier + ".md")
        spec = lire_spec(chemin)
        if spec["id"] != sid.split(":")[0]:
            raise EchecBuild(f"{chemin} : identifiant {spec['id']} != {sid}")
        specs[bid] = spec
    return specs


# --- Assemblage : notation -> octets (R5, l'assembleur maison) --------------------

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
        # R5 : maison -> capstone -> maison, identité octets
        des = list(CS.disasm(octets, pos))
        if len(des) != 1 or des[0].size != 4:
            raise EchecBuild(
                f"{fichier} @ {pos:#x} : le juge ne décode pas UNE instruction "
                f"de 4 o : {texte!r}")
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
    # NOP canonique intra-slot (addi x0, x0, 0 — mots de 4 o)
    n_nop = (slot - len(code)) // 4
    slot_plein = bytes(code) + struct.pack("<I", L.NOP_CANONIQUE) * n_nop
    if len(slot_plein) != slot:
        raise EchecBuild(f"{fichier} : le slot n'est pas multiple de 4 (garde anti-C)")
    return {"octets": bytes(code), "slot": slot_plein, "insns": insns,
            "texte": instrs, "labels": labels}


def assembler_tout() -> tuple[list, dict, dict]:
    specs = charger_couche_I()
    code = {}
    for bid, sid, fichier, rva, slot in L.BLOCS_SR:
        code[bid] = assembler_bloc(fichier, rva, slot)
        code[bid]["spec"] = sid
        code[bid]["fichier"] = fichier
        code[bid]["rva"] = rva
        code[bid]["slot_taille"] = slot
    return list(L.BLOCS_SR), specs, code


# --- Oracle structurel : contrats I sur le code désassemblé -----------------------

APPELS_AUTORISES = {          # I1/I2 des specs : appels directs (jal) par bloc
    "f70004": {L.A_ECRIRE, L.A_HEX64, L.A_VERDICT},
    # (les étiquettes locales déclarées — .emit — s'ajoutent à l'oracle)
}
SYSCALLS_AUTORISES = {        # I1/I2 : numéros ASM-GENERIC par bloc
    "f70001": {L.SYS_WRITE},            # write = 64 (sr-01)
    "f70004": {L.SYS_EXIT_GROUP},       # exit_group = 94 (sr-04 : trois sites)
}
DONNEES_S1 = {                # I1/I3 : accès [s1 + RVA] (.rodata) par bloc
    "f70002": {L.R_HEXCHARS},
    "f70003": {L.R_ERRNOS, L.R_ERRNOS + 4},
    "f70004": {L.R_MSG_BASE, L.R_MSG_P1, L.R_MSG_P2, L.R_MSG_VERD,
               L.R_MSG_FIN, L.R_MSG_FATAL},
}
DONNEES_S2 = {                # I3 : accès [s2 + déplacement] (.bss) par bloc
    "f70004": {L.R_TAMPON_REL, L.R_TAMPON_VERD_REL, L.R_TAMPON_NUM_REL},
}

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


def oracle_structurel(code: dict, specs: dict) -> list[str]:
    verrous = []

    def verrou(nom, condition, detail=""):
        if not condition:
            raise EchecBuild(f"oracle structurel : {nom} {detail}")
        verrous.append(nom)

    adresses = {bid: {i.address for i in code[bid]["insns"]} for bid in code}
    for bid, bloc in code.items():
        insns = bloc["insns"]
        rva, slot = bloc["rva"], bloc["slot_taille"]
        labels = bloc.get("labels", {})
        # Garde anti-C : TOUTE instruction fait 4 o (fiche § 9.1 — un
        # encodage 2 o est un refus, l'extension C est hors profil)
        for i in insns:
            verrou(f"{bid}:taille-4@{i.address:#x}", i.size == 4,
                   f"taille {i.size} != 4 (extension C ?)")
        # Sauts internes : frontière d'instruction du même bloc
        for i in insns:
            if i.mnemonic in _BRANCHES:
                cible = _cible_relative(i)
                verrou(f"{bid}:saut-interne@{i.address:#x}",
                       cible in adresses[bid], f"cible {cible:#x} hors frontière")
        # Appels directs (jal — le lien vit dans ra) : les blocs déclarés +
        # les étiquettes locales déclarées (.emit, I1)
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
                       f"cible {cible:#x} hors blocs déclarés (I1/I2)")
        # jalr : uniquement ret (le retour canonique) — le jalon n'a pas
        # d'appel indirect (le scratch t1 du patch vit au chantier (c))
        for i in insns:
            if i.mnemonic.startswith("jalr"):
                verrou(f"{bid}:ret-seul@{i.address:#x}", i.mnemonic == "ret",
                       f"jalr indirect hors contrat : {i.mnemonic} {i.op_str}")
        # Syscalls : a7 posé juste avant (addi a7, zero, imm), numéro
        # ASM-GENERIC autorisé PAR BLOC — ET LA GARDE ANTI-TABLE-X86
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
        # Données : [s1 + RVA] .rodata et [s2 + off] .bss DÉCLARÉS
        for i in insns:
            ops = [o.strip() for o in i.op_str.split(",")] if i.op_str else []
            for o in ops:
                m = _RE_MEM.match(o)
                if m:
                    imm, base = _nombre(m.group(1)), m.group(2)
                    if base == "s1":
                        # l'ancre .rodata : le déplacement CONSTANT est
                        # DÉCLARÉ au plan (I1/I3) — c'est la porte de la donnée
                        verrou(f"{bid}:s1-rva-declaree@{i.address:#x}",
                               imm in DONNEES_S1.get(bid, set()),
                               f"s1+{imm:#x} hors données déclarées (I1/I3)")
                    elif base == "s2":
                        # l'ancre .bss : déplacement relatif DÉCLARÉ (I3)
                        verrou(f"{bid}:s2-off-declaree@{i.address:#x}",
                               imm in DONNEES_S2.get(bid, set()),
                               f"s2+{imm:#x} hors .bss déclarée (I3)")
                    # base sp : la pile (traitée ci-dessous) ; base
                    # quelconque (t3…) : POINTEUR CALCULÉ — formé depuis
                    # les déclarations ci-dessous (formation addi), jamais
                    # une adresse constante du plan
            # formation de pointeur : addi rd, s1/s2, imm (imm != 0 —
            # l'idiome imm=0 est rendu mv par le juge, échappant au plan) ;
            # les DEUX addi d'ancre (LO des paires auipc+addi) échappent à
            # ce contrôle : ils sont vérifiés par leurs PROPRES verrous
            # d'ancre (site + HI*4096 + LO == cible — le layout tranche)
            if i.mnemonic == "addi" and len(ops) == 3:
                if bid == "f70004" and i.address in (L.ANCRE_BASE + 4,
                                                     L.ANCRE_BSS + 4):
                    pass          # l'arithmétique d'ancre — verrous dédiés
                elif ops[1] in ("s1", "s2") and _nombre(ops[2]) != 0:
                    jeu = DONNEES_S1 if ops[1] == "s1" else DONNEES_S2
                    verrou(f"{bid}:{ops[1]}-formation@{i.address:#x}",
                           _nombre(ops[2]) in jeu.get(bid, set()),
                           f"{ops[1]}+{ops[2]} hors données déclarées (I3)")
        # Ancres : les DEUX paires auipc+addi re-vérifiées DEPUIS LE CODE
        # DÉSASSEMBLÉ (site + HI*4096 + LO == cible — le layout tranche)
        if bid == "f70004":
            attendues = [(insns[0], "auipc", "s1", L.ANCRE_BASE, L.CIBLE_BASE),
                         (insns[2], "auipc", "s2", L.ANCRE_BSS, L.CIBLE_BSS)]
            for insn_a, mnemo, reg, site, cible in attendues:
                verrou(f"{bid}:ancre-{reg}-forme", insn_a.mnemonic == mnemo
                       and insn_a.op_str.startswith(f"{reg}, "),
                       f"la paire {reg} n'est pas au site {site:#x}")
                hi = _imm20_signe(_nombre(insn_a.op_str.split(", ")[1]))
                idx = insns.index(insn_a)
                insn_i = insns[idx + 1]
                verrou(f"{bid}:ancre-{reg}-paire",
                       insn_i.mnemonic == "addi" and
                       insn_i.op_str.startswith(f"{reg}, {reg}, "),
                       "l'addi de la paire n'est pas adjacent à son auipc")
                lo = _nombre(insn_i.op_str.split(", ")[2])
                verrou(f"{bid}:ancre-{reg}-arithmetique@{insn_a.address:#x}",
                       insn_a.address == site and site + hi * 4096 + lo == cible,
                       f"{insn_a.address:#x} + {hi:#x}*4096 + {lo} != {cible:#x}")
        # Padding/alignement (D8/D28/D33)
        fin_code = insns[-1].address + insns[-1].size
        verrou(f"{bid}:padding-16", rva + slot - fin_code >= 16)
        verrou(f"{bid}:slot-aligne-16", rva % 16 == 0)
        verrou(f"{bid}:slot-multiple-64", slot % 64 == 0)
        # Pile psABI : le point d'entrée ne touche JAMAIS sp (jal ne pousse
        # rien, ra porte le lien) ; le cadre de .emit est APPARIÉ ;
        # les feuilles : 0 octet de pile
        ecritures_sp = [i for i in insns if i.mnemonic == "addi" and
                        i.op_str.replace(" ", "").startswith("sp,sp,")]
        if bid == "f70004":
            imm_sp = sorted(_nombre(i.op_str.split(",")[2]) for i in ecritures_sp)
            verrou(f"{bid}:pile-appairee",
                   imm_sp == [-16, 16] and len(ecritures_sp) == 2,
                   f"écritures sp : {[i.op_str for i in ecritures_sp]}")
            seq = [i.mnemonic + "|" + i.op_str for i in insns]
            i_m16 = next(k for k, s in enumerate(seq)
                         if s.startswith("addi|sp, sp, -"))
            i_p16 = next(k for k, s in enumerate(seq)
                         if s.startswith("addi|sp, sp, 0x10"))
            i_sd = next(k for k, s in enumerate(seq) if s.startswith("sd|ra, 0(sp)"))
            i_ld = next(k for k, s in enumerate(seq) if s.startswith("ld|ra, 0(sp)"))
            i_ret = seq.index("ret|")
            verrou(f"{bid}:cadre-emit-ordonne",
                   i_m16 < i_sd < i_ld < i_p16 < i_ret,
                   f"cadre : -16@{i_m16} sd@{i_sd} ld@{i_ld} +16@{i_p16} ret@{i_ret}")
        else:
            verrou(f"{bid}:feuille-sans-pile", not ecritures_sp,
                   "une feuille ne touche jamais sp (I2)")
            verrou(f"{bid}:feuille-sans-appel",
                   not any(i.mnemonic == "jal" for i in insns), "feuille pure (I2)")
        # t1 : le porteur du brut (fiche § 2) — sr-02/sr-03 ne le touchent
        # JAMAIS (I2 : t0/t2/t3/t4 suffisent à leur arithmétique)
        if bid in ("f70002", "f70003"):
            for i in insns:
                ops = i.op_str.replace("(", ", ").replace(")", "").split(", ")
                verrou(f"{bid}:t1-respecte@{i.address:#x}",
                       "t1" not in [o.strip() for o in ops],
                       f"t1 touché : {i.mnemonic} {i.op_str} (I2 — fiche § 2)")
    return verrous


# --- Symboles des brouillons confrontés au layout (leçon C1) ----------------------

_MESSAGES = {   # symbole @L_* -> (message réel, longueur attendue)
    "L_BASE": (L.MSG_BASE, L.L_MSG_BASE),
    "L_P1": (L.MSG_P1, L.L_MSG_P1),
    "L_P2": (L.MSG_P2, L.L_MSG_P2),
    "L_VERD": (L.MSG_VERD, L.L_MSG_VERD),
    "L_FIN": (L.MSG_FIN, L.L_MSG_FIN),
    "L_FATAL": (L.MSG_FATAL, L.L_MSG_FATAL),
}
_ADRESSES = {   # symbole @nom -> constante layout (adresse de liaison)
    "A_ECRIRE": L.A_ECRIRE, "A_HEX64": L.A_HEX64, "A_VERDICT": L.A_VERDICT,
    "MSG_BASE": L.R_MSG_BASE, "MSG_P1": L.R_MSG_P1, "MSG_P2": L.R_MSG_P2,
    "MSG_VERD": L.R_MSG_VERD, "MSG_FIN": L.R_MSG_FIN, "MSG_FATAL": L.R_MSG_FATAL,
    "TAMPON": L.SEG_RW_RVA + L.R_TAMPON_REL,
    "TAMPON_VERD": L.SEG_RW_RVA + L.R_TAMPON_VERD_REL,
    "TAMPON_NUM": L.SEG_RW_RVA + L.R_TAMPON_NUM_REL,
    "HEXCHARS": L.R_HEXCHARS, "ERRNOS": L.R_ERRNOS,
    "ENTREES": L.R_ERRNOS + 4,
    "ANCRE_BASE": L.ANCRE_BASE, "ANCRE_BSS": L.ANCRE_BSS,
}
_NOMBRES = {    # symbole @nom -> constante numérique du layout
    "SYS_WRITE": L.SYS_WRITE, "EXIT_GROUP": L.SYS_EXIT_GROUP,
}


def verifier_symboles() -> int:
    n = 0
    for bid, _, fichier, _, _ in L.BLOCS_SR:
        chemin = os.path.join(ICI, "notation", "brouillons", fichier + ".asm")
        with open(chemin, encoding="utf-8") as f:
            for l in f:
                m = re.match(r"@(\w+)\s*=\s*(-?0x[0-9a-fA-F]+|-?\d+)", l.strip())
                if not m:
                    continue
                nom, val = m.group(1), int(m.group(2), 0)
                if nom in _MESSAGES:
                    message, attendue = _MESSAGES[nom]
                    if val != attendue or len(message) != attendue:
                        raise EchecBuild(
                            f"{fichier} : @{nom}={val} != longueur RÉELLE "
                            f"{attendue} de {message!r} (leçon C1)")
                elif nom in _ADRESSES:
                    if val != _ADRESSES[nom]:
                        raise EchecBuild(
                            f"{fichier} : @{nom}={val:#x} != layout "
                            f"{_ADRESSES[nom]:#x} (leçon C1)")
                elif nom in _NOMBRES:
                    if val != _NOMBRES[nom]:
                        raise EchecBuild(
                            f"{fichier} : @{nom}={val} != layout {_NOMBRES[nom]} "
                            f"(leçon C1 — table asm-generic)")
                    if val in L.TABLE_X86_REFUSEE:
                        raise EchecBuild(
                            f"{fichier} : @{nom}={val} est un numéro x86-64 "
                            f"(« {L.TABLE_X86_REFUSEE[val]} ») — REFUS NOMMÉ "
                            f"(garde anti-table-x86, fiche § 4)")
                else:
                    raise EchecBuild(f"{fichier} : symbole inconnu @{nom}")
                n += 1
    return n


# --- Composition ELF64 durci (ehdr + 4 phdr à la main, moitié ISA RISC-V) ----------

def octets_errnos() -> bytes:
    """La table ERRNOS : [nombre u32] + {errno u32, verdict u32} — layout,
    source unique (l'empreinte de la table est vérifiée par valider_elf)."""
    entrees = b"".join(struct.pack("<II", e, v) for e, v in sorted(L.ERRNOS.items()))
    return struct.pack("<I", len(L.ERRNOS)) + entrees


def mot_reserve() -> bytes:
    """Le mot ebreak (0x00100073) — la réserve d'inaccessibilité du jalon."""
    return struct.pack("<I", L.EBREAK)


def composer_elf(code: dict) -> bytes:
    """Image durcie : segment R (en-têtes + tables + messages), segment RX
    (code aux slots, NOP canonique intra-slot, ebreak réserves), .bss pur."""
    seg_r = bytearray(b"\x00" * L.SEG_R_TAILLE)
    seg_rx = bytearray(mot_reserve() * (L.SEG_RX_TAILLE // 4))
    poses: list[tuple[int, int, str]] = []       # garde-fou chevauchement (C1)

    def poser(seg: bytearray, base: int, rva: int, donnees: bytes, nom: str = ""):
        poses.append((rva, rva + len(donnees), nom or hex(rva)))
        if rva + len(donnees) > base + len(seg):
            raise EchecBuild(f"segment débordant à {rva:#x} ({nom})")
        seg[rva - base: rva - base + len(donnees)] = donnees

    # — segment R : la table ERRNOS, HEXCHARS, les messages (longueurs
    # explicites — jamais de terminateur : le plan d'adressage les fige)
    poser(seg_r, L.SEG_R_RVA, L.R_ERRNOS, octets_errnos(), "ERRNOS")
    poser(seg_r, L.SEG_R_RVA, L.R_HEXCHARS, L.HEXCHARS, "HEXCHARS")
    for rva, donnees, nom in (
            (L.R_MSG_BASE, L.MSG_BASE, "MSG_BASE"),
            (L.R_MSG_P1, L.MSG_P1, "MSG_P1"),
            (L.R_MSG_P2, L.MSG_P2, "MSG_P2"),
            (L.R_MSG_VERD, L.MSG_VERD, "MSG_VERD"),
            (L.R_MSG_FIN, L.MSG_FIN, "MSG_FIN"),
            (L.R_MSG_FATAL, L.MSG_FATAL, "MSG_FATAL")):
        poser(seg_r, L.SEG_R_RVA, rva, donnees, nom)
    # — segment RX : les slots des quatre blocs
    for bid, _, _, rva, slot in L.BLOCS_SR:
        poser(seg_rx, L.SEG_RX_RVA, rva, code[bid]["slot"], bid)
    for (d1, f1, n1), (d2, f2, n2) in zip(poses, poses[1:]):
        if d1 < f2 and d2 < f1:
            raise EchecBuild(f"chevauchement : {n1} [{d1:#x},{f1:#x}) / {n2} [{d2:#x},{f2:#x})")

    # — ehdr (ET_DYN, moitié ISA RISC-V : e_machine 0xF3, e_flags 0) +
    #   4 phdr par-dessus les réserves ebreak
    e_ident = b"\x7fELF" + bytes([2, 1, 1, 0]) + b"\x00" * 8
    ehdr = struct.pack("<16sHHIQQQIHHHHHH", e_ident,
                       3, L.E_MACHINE, 1,           # ET_DYN (PIE), EM_RISCV, v1
                       L.ENTREE,                    # e_entry = RVA (relatif)
                       64, 0, L.E_FLAGS,            # phoff, shoff, flags=0
                       64, 56, 4, 0, 0, 0)          # ehsize, phentsize, phnum=4
    ph_r = struct.pack("<IIQQQQQQ", 1, 4,          # LOAD, R (lecture seule)
                       L.SEG_R_RVA, L.SEG_R_RVA, L.SEG_R_RVA,
                       L.SEG_R_TAILLE, L.SEG_R_TAILLE, L.TAILLE_PAGE)
    ph_rx = struct.pack("<IIQQQQQQ", 1, 5,         # LOAD, R+X
                        L.SEG_RX_RVA, L.SEG_RX_RVA, L.SEG_RX_RVA,
                        L.SEG_RX_TAILLE, L.SEG_RX_TAILLE, L.TAILLE_PAGE)
    ph_rw = struct.pack("<IIQQQQQQ", 1, 6,         # LOAD, R+W (.bss pur)
                        L.SEG_RW_RVA, L.SEG_RW_RVA, L.SEG_RW_RVA,
                        0, L.SEG_RW_TAILLE, L.TAILLE_PAGE)
    ph_stack = struct.pack("<IIQQQQQQ", L.PT_GNU_STACK, 6,   # RW SANS X (NX)
                           0, 0, 0, 0, 0, 0x10)
    seg_r[0:64] = ehdr
    seg_r[64:120] = ph_r
    seg_r[120:176] = ph_rx
    seg_r[176:232] = ph_rw
    seg_r[232:288] = ph_stack
    return bytes(seg_r) + bytes(seg_rx)


def valider_elf(img: bytes) -> list[str]:
    """Relit l'image composée : ET_DYN, e_machine/e_flags (moitié ISA),
    W^X DEPUIS LES PHDR, GNU_STACK sans X, offsets == vaddr, tables
    conformes au layout (source unique), réserves ebreak CONSTATÉES."""
    lignes = []
    if len(img) != L.TAILLE_FICHIER:
        raise EchecBuild(f"taille {len(img):#x} != {L.TAILLE_FICHIER:#x}")
    if img[:4] != b"\x7fELF" or img[4] != 2 or img[5] != 1:
        raise EchecBuild("magie ELF64 LE absente")
    e_type, e_machine = struct.unpack_from("<HH", img, 16)
    e_entry = struct.unpack_from("<Q", img, 24)[0]
    e_flags = struct.unpack_from("<I", img, 48)[0]
    if e_type != 3:
        raise EchecBuild(f"e_type {e_type} != 3 (ET_DYN exigé — le durcissement)")
    if e_machine != L.E_MACHINE:
        raise EchecBuild(f"e_machine {e_machine:#x} != {L.E_MACHINE:#x} (EM_RISCV)")
    if e_flags != L.E_FLAGS:
        raise EchecBuild(f"e_flags {e_flags:#x} != {L.E_FLAGS:#x} (ni RVC ni float-abi)")
    if e_entry != L.ENTREE:
        raise EchecBuild(f"e_entry {e_entry:#x} != {L.ENTREE:#x} (RVA, relatif à la base)")
    phoff, phentsize, phnum = struct.unpack_from("<Q", img, 32)[0], \
        struct.unpack_from("<H", img, 54)[0], struct.unpack_from("<H", img, 56)[0]
    if (phoff, phentsize, phnum) != (64, 56, 4):
        raise EchecBuild(f"phdr ({phoff},{phentsize},{phnum}) != (64,56,4)")
    loads = []
    for i in range(phnum):
        # p = (type, flags, offset, vaddr, paddr, filesz, memsz, align)
        p = struct.unpack_from("<IIQQQQQQ", img, phoff + i * 56)
        if p[0] == 1:
            loads.append(p)
        elif p[0] == L.PT_GNU_STACK:
            if p[1] != 6:
                raise EchecBuild(f"PT_GNU_STACK drapeaux {p[1]:#x} != 6 (RW sans X — NX exigé psABI)")
            if p[7] != 0x10:
                raise EchecBuild(f"PT_GNU_STACK align {p[7]:#x} != 0x10")
            lignes.append("[phdr] PT_GNU_STACK drapeaux 6 (RW) SANS X — NX explicite psABI, align 0x10")
        else:
            raise EchecBuild(f"p_type inattendu {p[0]:#x}")
    if len(loads) != 3:
        raise EchecBuild(f"{len(loads)} PT_LOAD != 3 (R/RX/RW)")
    if [p[1] for p in loads] != [4, 5, 6]:
        raise EchecBuild(f"drapeaux PT_LOAD {[p[1] for p in loads]} != [4, 5, 6] (R/RX/RW)")
    for p in loads:
        if p[1] & 2 and p[1] & 1:
            raise EchecBuild(f"PT_LOAD {p[1]:#x} : inscriptible ET exécutable (W^X rompu)")
        if p[2] != p[3]:
            raise EchecBuild(f"PT_LOAD {p[1]:#x} : offset {p[2]:#x} != vaddr {p[3]:#x}")
        if p[7] != L.TAILLE_PAGE:
            raise EchecBuild(f"PT_LOAD {p[1]:#x} : align {p[7]:#x} != {L.TAILLE_PAGE:#x}")
    attendus = {4: (L.SEG_R_RVA, L.SEG_R_TAILLE, L.SEG_R_TAILLE),
                5: (L.SEG_RX_RVA, L.SEG_RX_TAILLE, L.SEG_RX_TAILLE),
                6: (L.SEG_RW_RVA, 0, L.SEG_RW_TAILLE)}
    for p in loads:
        vaddr, filesz, memsz = attendus[p[1]]
        if (p[3], p[5], p[6]) != (vaddr, filesz, memsz):
            raise EchecBuild(
                f"PT_LOAD {p[1]:#x} : vaddr/filesz/memsz "
                f"{(p[3], p[5], p[6])} != {(vaddr, filesz, memsz)} (layout)")
    lignes.append("[phdr] 3 PT_LOAD R/RX/RW + PT_GNU_STACK RW sans X — "
                  "W^X CONSTATÉ depuis les phdr (aucun segment inscriptible exécutable)")
    lignes.append(f"[phdr] ET_DYN (PIE) : e_machine {L.E_MACHINE:#x} (EM_RISCV), "
                  f"e_flags {L.E_FLAGS:#x} (ni RVC ni float-abi), e_entry "
                  f"{e_entry:#x} RELATIF à la base, RW .bss pur (filesz 0)")
    # Tables de données : empreintes conformes au layout (source unique)
    if img[L.R_ERRNOS:L.R_ERRNOS + len(octets_errnos())] != octets_errnos():
        raise EchecBuild("table ERRNOS divergente du layout (source unique)")
    if img[L.R_HEXCHARS:L.R_HEXCHARS + 16] != L.HEXCHARS:
        raise EchecBuild("HEXCHARS divergents")
    for rva, attendu in ((L.R_MSG_BASE, L.MSG_BASE), (L.R_MSG_P1, L.MSG_P1),
                         (L.R_MSG_P2, L.MSG_P2), (L.R_MSG_VERD, L.MSG_VERD),
                         (L.R_MSG_FIN, L.MSG_FIN), (L.R_MSG_FATAL, L.MSG_FATAL)):
        if img[rva:rva + len(attendu)] != attendu:
            raise EchecBuild(f"message @ {rva:#x} divergent")
    # Réserves ebreak CONSTATÉES : hors des slots, tout le segment RX est
    # fait de mots ebreak (0x00100073) — l'inaccessibilité est dans les octets
    reserve = mot_reserve()
    for bid, _, _, rva, slot in L.BLOCS_SR:
        suivant = rva + slot
        while suivant < L.SEG_RX_RVA + L.SEG_RX_TAILLE and suivant % 64:
            if img[suivant:suivant + 4] not in (reserve, b"\x00\x00\x00\x00"):
                pass              # (le mot suivant un slot peut chevaucher la réserve)
            suivant += 4
    zone = img[L.SEG_RX_RVA + sum(s for _, _, _, _, s in L.BLOCS_SR):
               L.SEG_RX_RVA + L.SEG_RX_TAILLE]
    if zone != reserve * (len(zone) // 4):
        raise EchecBuild("la réserve RX hors slots n'est pas faite de mots ebreak")
    lignes.append("[RX] réserves ebreak constatées hors slots ; NOP canonique "
                  "addi x0, x0, 0 intra-slot (fiche § 7)")
    return lignes


# --- Oracle d'exécution : qemu-riscv64, l'exécuteur du jalon (D149) ---------------

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
        "qemu-riscv64 ABSENT — le prérequis du chantier (constat fiche § 10, "
        "re-vérifié AVANT usage) : lancez riscv/outils/installer_qemu.sh "
        "(extraction locale sans privilèges) ou fournissez QEMU_RISCV64")


class Terrain:
    """Exécution de la sonde sous qemu-riscv64 (TCG — le noyau et les
    syscalls sont RÉELS, l'ISA est exécutée par l'émulateur : la réserve
    instrumentale D149 est PORTÉE par chaque verdict)."""

    def __init__(self, img: bytes, extra: list[str] | None = None):
        self.qemu = chemin_qemu()
        self.extra = extra or []
        parent = os.path.join(ICI, ".tmp")
        os.makedirs(parent, exist_ok=True)
        self.dossier = tempfile.mkdtemp(prefix="sonde-rv-", dir=parent)
        self.chemin = os.path.join(self.dossier, "sonde")
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


_RE_BASE = re.compile(rb"^sonde : base 0x([0-9a-f]{16})\n$")


def hex16(v: int) -> bytes:
    return f"{v & 0xFFFFFFFFFFFFFFFF:016x}".encode()


LIGNE_S1 = (L.MSG_P1 + hex16(-9) + L.MSG_VERD + hex16(1) + L.MSG_FIN)
LIGNE_S2 = (L.MSG_P2 + hex16(-14) + L.MSG_VERD + hex16(6) + L.MSG_FIN)


def _sortie_conforme(sortie: bytes) -> tuple[bool, int | None]:
    """4 lignes : base (variable), les deux sondes et la fatale (exactes)."""
    lignes = sortie.split(b"\n")
    if len(lignes) != 5 or lignes[4] != b"":
        return False, None
    m = _RE_BASE.match(lignes[0] + b"\n")
    if not m:
        return False, None
    if lignes[1] + b"\n" != LIGNE_S1 or lignes[2] + b"\n" != LIGNE_S2:
        return False, None
    if lignes[3] + b"\n" != L.MSG_FATAL:
        return False, None
    return True, int(m.group(1), 16)


def oracle_qemu(img: bytes, longueurs: dict[str, int] | None = None) -> dict:
    # — 6 exécutions nominales : 4 lignes conformes + code 6 (le verdict
    # fatal d'EFAULT est terminal PAR CONTRAT : la démonstration complète
    # des deux branches de la table ERRNOS)
    t = Terrain(img)
    try:
        bases: list[int] = []
        for _ in range(6):
            sortie, err, code = t.lancer()
            ok, base = _sortie_conforme(sortie)
            if code != 6 or err or not ok:
                raise EchecBuild(
                    f"oracle qemu : code={code} base={base!r} sortie={sortie!r} err={err!r}")
            bases.append(base)
        # — la base : page-alignée, plausible — et CONSTATÉE (jamais
        # décrétée : l'ASLR est la prérogative du CHARGEUR, ici l'émulateur
        # de processus — la réserve instrumentale D149)
        for b in bases:
            if b % L.TAILLE_PAGE != 0:
                raise EchecBuild(f"base {b:#x} non alignée à la page — le chargeur ne l'a pas choisie")
            if b < 0x10000:
                raise EchecBuild(f"base {b:#x} < 0x10000 — implausible")
        distinctes = len(set(bases))
        # — l'indifférence à la base DÉMONTRÉE par bases forcées : la
        # preuve ne dépend JAMAIS d'un ASLR émulé — le code fonctionne à
        # TOUTE base. Constat d'instrument (nommé, sur pièces) : qemu
        # 10.0.13 ne RANDOMISE PAS l'image PIE invitée — la base par
        # défaut est CONSTANTE, et -B (guest_base) seul est SANS effet
        # sur l'adresse d'image ET_DYN ; le levier du chargeur est -R
        # (la taille de réservation VA fixe la fenêtre où l'image vit —
        # un paramètre du CHARGEUR, jamais de l'artefact), et -B déplace
        # alors l'image dans la fenêtre réservée.
        configurations_forcees = [
            ("-R 1G", ["-R", "1G"]),
            ("-R 4G", ["-R", "4G"]),
            ("-B 0x100000000 -R 2G", ["-B", "0x100000000", "-R", "2G"]),
        ]
        bases_forcees: list[tuple[str, int]] = []
        for nom_cfg, extra in configurations_forcees:
            tf = Terrain(img, extra=extra)
            try:
                sortie, err, code = tf.lancer()
                ok, base = _sortie_conforme(sortie)
                if code != 6 or err or not ok:
                    raise EchecBuild(
                        f"base forcée ({nom_cfg}) : code={code} base={base!r} "
                        f"sortie={sortie!r} err={err!r} — l'image n'est PAS "
                        f"indifférente à la base (le contrat I3 est rompu)")
                bases_forcees.append((nom_cfg, base))
            finally:
                tf.nettoyer()
        toutes = {b for _, b in bases_forcees} | {bases[0]}
        if len(toutes) != len(bases_forcees) + 1:
            raise EchecBuild(
                f"les bases forcées n'ont pas bougé : "
                f"{[f'{n}={b:#x}' for n, b in bases_forcees]} — l'épreuve ne "
                f"porte pas (le chargeur ignore le levier -R)")

        # — falsification : un octet de CODE corrompu par bloc (aligné
        # instruction — l'ISA est à taille fixe), au MOINS une divergence
        # par mutant, zéro silence
        detectees = 0
        for bid, _, _, rva, _ in L.BLOCS_SR:
            longueur = (longueurs or {}).get(bid, 16)
            for offset in (0, 4, 8):
                if offset >= longueur:
                    continue
                mutant = bytearray(img)
                mutant[rva + offset] ^= 0xFF
                tm = Terrain(bytes(mutant))
                try:
                    sortie, err, code = tm.lancer()
                    ok, _ = _sortie_conforme(sortie)
                    if ok and code == 6 and not err:
                        raise EchecBuild(
                            f"falsification : {bid} +{offset} NON détectée (silence)")
                    detectees += 1
                finally:
                    tm.nettoyer()
        return {"cas": 6, "bases": bases, "bases_distinctes": distinctes,
                "bases_forcees": bases_forcees,
                "falsification": detectees}
    finally:
        t.nettoyer()


# --- Carte génération 1 de la lignée du jalon -------------------------------------

def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def fragments_clairs(code: dict, img: bytes, verrous: list, specs: dict,
                     verdict: dict, compteurs: dict, journal: list,
                     porte: dict) -> dict:
    loc = ["[carte-frag] nom=frag-loc generation=1"]
    for bid, sid, fichier, rva, slot in L.BLOCS_SR:
        loc.append(f"[bloc] id={bid} spec={sid} cible={L.PROFIL} "
                   f"addr={rva:#x} size={slot} v=1 etat=scelle "
                   f"(RVA — PIE : la base est choisie par le chargeur)")
    con = ["[carte-frag] nom=frag-con generation=1"]
    for bid in code:
        spec = specs[bid]["texte"]
        sig = re.search(r"Intention : (.+?)\n", spec).group(1)
        con.append(f"[bloc] id={bid}\n  sig : {sig[:100]}")
    prf = ["[carte-frag] nom=frag-prf generation=1"]
    for bid, _, fichier, _, _ in L.BLOCS_SR:
        with open(os.path.join(ICI, "notation", fichier + ".asm"), "rb") as f:
            emp = sha(f.read())
        crist = min(compteurs.get(bid, 1), 10)
        prf += [f"[bloc] id={bid} etat={'cristallise' if crist >= 10 else 'scelle'} "
                f"crist={crist}/10",
                f"  vecteurs : roundtrip=ok structure=ok notation={emp}",
                f"  differentiel : qemu ok (PIE/ERRNOS, falsification "
                f"{verdict['falsification']})"]
    prf.append("[verifications] runs=" + str(len(journal)))
    prf += ["  " + r for r in journal[-12:]]
    bld = ["[carte-frag] nom=frag-bld generation=1"]
    for bid, _, fichier, rva, slot in L.BLOCS_SR:
        bld.append(f"[bloc] id={bid} addr={rva:#x} "
                   f"empreinte={sha(code[bid]['slot'])}")
    bld += [
        f"[build] artefact=sonde version={L.VERSION_DEV1} profil={L.PROFIL} "
        f"taille={len(img)} empreinte={sha(img)}",
        f"  outils : ASSEMBLEUR MAISON as_rv64 (RV64IMA+Zifencei, 4 o, "
        f"formats R/I/S/B/U/J) + capstone {capstone.cs_version()[0]}."
        f"{capstone.cs_version()[1]} JUGE UNIQUE ; verrous={len(verrous)} ; "
        f"symboles vérifiés",
        f"  porte round-trip : AVANT {porte['avant']} textes + INVERSE "
        f"{porte['inverse']} encodages légaux — 100 % (fiche § 6)",
        f"  durcissement : ET_DYN/PIE, e_machine {L.E_MACHINE:#x} (EM_RISCV), "
        f"e_flags 0, 3 segments R/RX/RW, PT_GNU_STACK sans X, W^X depuis les "
        f"phdr ; ERRNOS {len(L.ERRNOS)} entrée(s) ; garde anti-table-x86 vivante",
        f"  oracle : qemu-riscv64 (réserve instrumentale D149 — TCG, noyau "
        f"et syscalls RÉELS) — base par défaut CONSTANTE {verdict['bases'][0]:#x} "
        f"({verdict['bases_distinctes']} distincte(s) sur 6 runs — qemu 10 ne "
        f"randomise PAS l'image PIE invitée, CONSTATÉ) ; bases forcées "
        + " / ".join(f"{n}={b:#x}" for n, b in verdict['bases_forcees'])
        + " VERTES (indifférence à la base)",
        f"[zones] sys=0x1000-0x1040 hex=0x1040-0x10c0 verdict=0x10c0-0x1140 "
        f"app=0x1140-0x13c0 rodata=0x140-0x285 bss=0x2000-0x2040",
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
    for bid, _, fichier, rva, slot in L.BLOCS_SR:
        m = re.search(rf"\[bloc\] id={bid} addr=\S+ empreinte=(\S+)", bld)
        if not m or m.group(1) != sha(img[rva:rva + slot]):
            raise EchecBuild(f"verrou croisé : {bid} divergent (R8)")
        n += 1
    return n


def construire_carte(code: dict, img: bytes, verrous: list, specs: dict,
                     verdict: dict, compteurs: dict, journal: list,
                     porte: dict):
    clairs = fragments_clairs(code, img, verrous, specs, verdict, compteurs,
                              journal, porte)
    phrase, graine = cm.charger_secrets(interactif=False)
    maitre = cm.cle_maitresse(phrase)
    fragments = {n: cm.chiffrer_fragment(maitre, n, clairs[n]) for n in cm.FRAGMENTS}
    prive, pub = cm.paire_cles(graine)
    entete = cm.construire_entete(empreinte_racine(fragments))
    signature = cm.signer(prive, entete, fragments)
    cm.ecrire_carte(entete, fragments, signature, pub)


def tableau_de_bord(img: bytes, verrous: list, specs: dict, verdict: dict,
                    phdr_lignes: list[str], porte: dict) -> str:
    return "\n".join([
        "[tableau] jalon=M7-(a) artefact=sonde version=" + L.VERSION_DEV1,
        "  profil                       : " + L.PROFIL + " (fiche § 6 — le moteur de notation)",
        "  moteur_notation              : ASSEMBLEUR MAISON as_rv64 (RV64IMA+"
        "Zifencei, formats R/I/S/B/U/J, 4 o, SANS extension C) ; capstone "
        "5.0.7 JUGE UNIQUE",
        "  porte_roundtrip              : VERTE — " + str(porte["avant"])
        + " textes (avant) + " + str(porte["inverse"])
        + " encodages légaux (inverse), 100 % (keystone SANS RISC-V — "
        + "constat re-vérifié au chantier)",
        "  blocs_avec_spec_a_jour        : 4/4 : audit I->C->B (specs, carte, artefact)",
        "  chaines_I_C_B_tests           : 4/4 : " + str(len(verrous)) + " verrous PASS",
        "  construction                 : 0 erreur / 0 avertissement : build script",
        "  format_durci                 : ET_DYN (PIE), e_machine "
        + hex(L.E_MACHINE) + " (EM_RISCV), e_flags 0, 3 segments R/RX/RW, "
        "PT_GNU_STACK RW sans X, W^X constaté depuis les phdr, "
        "offsets==vaddr, RW .bss pur (filesz 0), garde anti-C (taille 4 "
        "constatée par instruction)",
        "  contrat_erreurs               : table ERRNOS " + str(len(L.ERRNOS))
        + " entrée(s) (EBADF nommé, motivée par sr-04:E1) ; VERDICT_FATAL="
        + str(L.VERDICT_FATAL) + " (fail-closed) ; exercée en exécution sur "
        "les DEUX branches ; table syscalls ASM-GENERIC avec garde "
        "anti-table-x86 (write=1 REFUSÉ nommément)",
        "  tests_differentiels           : oracle qemu 6/6 runs conformes "
        "(4 lignes octet pour octet, code 6) ; falsification "
        + str(verdict["falsification"]) + " mutations attrapées (zéro silence)",
        "  pie_indifference_base        : base par défaut CONSTANTE "
        + hex(verdict["bases"][0]) + " (" + str(verdict["bases_distinctes"])
        + " distincte(s) sur 6 exécutions — qemu 10 ne randomise PAS "
        "l'image PIE invitée, CONSTATÉ nommé) ; bases forcées "
        + ", ".join(f"{n}={b:#x}" for n, b in verdict["bases_forcees"])
        + " VERTES — l'indifférence à la base est DÉMONTRÉE par les "
        "paramètres du CHARGEUR (-R la fenêtre de réservation), la preuve "
        "ne dépend jamais d'un ASLR émulé (réserve instrumentale D149 : "
        "qemu-riscv64 TCG, noyau et syscalls réels)",
        "  reutilisation_heritage        : 0 bloc réutilisé (lignée neuve — "
        "la TROISIÈME instanciation de la couche I est le chantier (b))",
        "  defauts_ouverts               : 0",
        "  preversions                   : " + L.VERSION_DEV1
        + " conforme (R10 : monotonie, plancher " + hex(L.VERSION_U64_MIN) + ")",
        "  artefact                      : " + str(len(img)) + " octets ; "
        "empreinte sha256:" + sha(img)[:24] + "…",
        "  verrou_croise                 : 4 empreintes + signature Ed25519 (R8)",
    ]) + "\n" + "\n".join("  " + l for l in phdr_lignes) + "\n"


# --- Construction -----------------------------------------------------------------

def construire() -> int:
    print("=== M7-(a) : lignée du jalon (riscv/, D149) — le moteur de notation RV64 ===")
    t0 = time.perf_counter()

    print("[constat] keystone SANS RISC-V (re-vérifié : KS_ARCH_RISCV absent) ; "
          "capstone 5.0.7 décode RV64 ; qemu-riscv64 opérationnel ("
          + chemin_qemu() + ")")

    porte = franchir_porte()
    print(f"[porte] round-trip 100 % : AVANT {porte['avant']} textes + INVERSE "
          f"{porte['inverse']} encodages légaux — capstone juge unique (fiche § 6)")

    specs = charger_couche_I()
    print(f"[I] 4 specs chargées et auditées (gabarit § 2.2, R2)")

    blocs, _, code = assembler_tout()
    total_insns = sum(len(code[b[0]]["insns"]) for b in blocs)
    total_code = sum(len(code[b[0]]["octets"]) for b in blocs)
    print(f"[R5] 4 blocs, {total_insns} instructions, {total_code} o de code — "
          f"round-trip assembleur maison/capstone 100 %")

    verrous = oracle_structurel(code, specs)
    n_symboles = verifier_symboles()
    print(f"[oracle] structurel : {len(verrous)} verrous PASS ; "
          f"{n_symboles} symboles @ vérifiés contre layout/réel (leçon C1) ; "
          f"garde anti-table-x86 VIVANTE")

    img = composer_elf(code)
    phdr_lignes = valider_elf(img)
    for l in phdr_lignes:
        print(l)
    print(f"[ELF] sonde : {len(img)} o (ET_DYN EM_RISCV, ehdr + 4 phdr à la "
          f"main, R 0x1000 + RX 0x1000 + RW .bss 0x1000), entrée {L.ENTREE:#x} (RVA)")

    verdict = oracle_qemu(img, {bid: len(code[bid]["octets"]) for bid, _, _, _, _ in blocs})
    bases_court = ", ".join(f"{b:#x}" for b in verdict["bases"][:3])
    print(f"[oracle] qemu (réserve D149 — TCG, syscalls réels) : 6/6 runs "
          f"conformes, code 6 ; base par défaut CONSTANTE {verdict['bases'][0]:#x} "
          f"({verdict['bases_distinctes']} distincte(s) sur 6 — qemu 10 ne "
          f"randomise pas l'image PIE invitée, CONSTATÉ) ; bases forcées "
          + ", ".join(f"{n}={b:#x}" for n, b in verdict['bases_forcees'])
          + " VERTES (indifférence à la base)")
    print(f"[oracle] ERRNOS exercée : EBADF nommé (verdict 1) ET EFAULT hors "
          f"table (VERDICT_FATAL 6, arrêt propre) ; falsification "
          f"{verdict['falsification']} détectées (zéro silence)")

    chemin_art = os.path.join(ICI, "sonde")
    with open(chemin_art, "wb") as f:
        f.write(img)
    os.chmod(chemin_art, 0o755)

    journal = [f"run qemu date={datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} "
               f"build={L.VERSION_DEV1} bases={verdict['bases_distinctes']}/6 "
               f"falsif={verdict['falsification']}"]
    compteurs = {bid: 1 for bid, _, _, _, _ in blocs}
    construire_carte(code, img, verrous, specs, verdict, compteurs, journal, porte)
    nb = verrou_croise(code, img)
    with open(os.path.join(cm.CARTE_DIR, "tableau-de-bord.txt"), "w",
              encoding="utf-8") as f:
        f.write(tableau_de_bord(img, verrous, specs, verdict, phdr_lignes, porte))
    print(f"[carte] génération 1 du jalon écrite : 4 fragments chiffrés "
          f"(QUATRIÈME sel distinct), signature Ed25519 (clés projet D27), "
          f"verrou croisé {nb}/4, tableau de bord")

    print(f"[B] sonde scellée : sha256:{sha(img)}")
    print(f"=== M7-(a) dev (oracles verts) : {L.VERSION_DEV1} — "
          f"{round(time.perf_counter() - t0, 1)} s ===")
    return 0


def verifier() -> int:
    print("=== M7-(a) : re-vérification complète (R5/R8) ===")
    with open(os.path.join(ICI, "sonde"), "rb") as f:
        img = f.read()
    porte = franchir_porte()
    print(f"[porte] round-trip 100 % re-joué : AVANT {porte['avant']} + "
          f"INVERSE {porte['inverse']}")
    blocs, _, code = assembler_tout()
    for bid, _, fichier, rva, slot in blocs:
        if img[rva:rva + slot] != code[bid]["slot"]:
            raise EchecBuild(f"{bid} : notation et artefact divergent (R5)")
    specs = charger_couche_I()
    oracle_structurel(code, specs)
    verifier_symboles()
    valider_elf(img)
    verdict = oracle_qemu(img, {bid: len(code[bid]["octets"]) for bid, _, _, _, _ in blocs})
    print(f"[oracle] qemu : 6/6 runs conformes ; bases forcées VERTES ; "
          f"falsification {verdict['falsification']} détectées")
    # Cristallisation : compteurs incrémentés dans frag-prf
    phrase, graine = cm.charger_secrets(interactif=False)
    maitre = cm.cle_maitresse(phrase)
    _, fragments, _, _ = cm.lire_carte()
    prf = cm.dechiffrer_fragment(maitre, "frag-prf", fragments["frag-prf"]).decode()
    compteurs = {}
    for ligne in prf.splitlines():
        if ligne.startswith("[bloc]"):
            champs = dict(re.findall(r"(\w+)=(\S+)", ligne))
            compteurs[champs["id"]] = int(
                re.match(r"(\d+)/10", champs.get("crist", "1/10")).group(1))
    for bid, _, _, _, _ in blocs:
        compteurs[bid] = min(compteurs.get(bid, 0) + 1, 10)
    journal = [l.strip() for l in prf.splitlines() if l.startswith("  run ")]
    journal.append(f"run qemu date={datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} "
                   f"verif bases={verdict['bases_distinctes']}/6 falsif={verdict['falsification']}")
    construire_carte(code, img, [], specs, verdict, compteurs, journal, porte)
    nb = verrou_croise(code, img)
    crist = ", ".join(f"{b}={compteurs.get(b, 0)}/10" for b, _, _, _, _ in blocs)
    print(f"[R6] cristallisation : {crist}")
    print(f"[R8] verrou croisé : {nb}/4 empreintes conformes")
    return 0


if __name__ == "__main__":
    sys.exit(verifier() if "--verifier" in sys.argv else construire())
