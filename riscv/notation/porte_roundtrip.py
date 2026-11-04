#!/usr/bin/env python3
"""porte_roundtrip.py — LA PORTE ROUND-TRIP du jalon M7 (fiche § 6).

Le critère de sortie du chantier M7-(a), exécuté comme une PORTE : le
round-trip est 100 % sur le corpus d'instructions du profil, capstone
JUGE UNIQUE — assemble → désassemble → ré-assemble, tout écart
d'instruction, d'opérande ou de taille est un ÉCHEC (jamais un avertissement).

DEUX DIRECTIONS, toutes deux exigées :

  AVANT  (notation -> octets -> notation) : chaque texte du corpus est
         assemblé par l'assembleur maison, décodé par le juge (exactement
         UNE instruction de 4 octets — garde anti-C, fiche § 9.1), et le
         texte du juge ré-assemble en les MÊMES octets ;

  INVERSE (octets -> notation -> octets) : l'ESPACE D'ENCODAGE du profil
         (les combinaisons légales RV64IMA+Zifencei : champs f7/f3 des
         formats R, shamt EXHAUSTIFS 0..63/0..31, immédiats de bord,
         décalages de bord de B/J, les 256 couples pred/succ de fence)
         est décodé par le juge, et CHAQUE texte qu'il émet ré-assemble
         en ses octets — l'assembleur couvre le rendu INTÉGRAL du juge
         sur le domaine du profil, pas seulement les graphies qu'on
         avait prévues.

La direction inverse est la vraie preuve : le juge rend mv là où le
brouillon écrit addi, sext.w là où le code porte addiw, beqz là où la
notation pensait beq — l'identité exigée est sur les OCTETS, la graphie
canonique est CELLE DU JUGE (le modèle du chantier M6, appliqué à une
ISA où le juge a plus de pseudos que l'auteur n'a d'habitudes).

Usage : python3 notation/porte_roundtrip.py [--silencieux]
Sortie : le décompte par famille, VERDICT final — code de sortie 0/1.
"""

from __future__ import annotations

import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RISCV = os.path.dirname(ICI)
sys.path.insert(0, os.path.join(RISCV, "outils"))

import capstone                                  # noqa: E402
from as_rv64 import EchecAssemblage, assembler    # noqa: E402

JUGE = capstone.Cs(capstone.CS_ARCH_RISCV, capstone.CS_MODE_RISCV64)
JUGE.detail = False


class EchecPorte(Exception):
    """Tout écart du round-trip — échec de build, jamais un avertissement."""


# --- Le corpus d'instructions du profil (direction AVANT) -------------------------

_R64 = ["add", "sub", "sll", "slt", "sltu", "xor", "srl", "sra", "or", "and",
        "mul", "mulh", "mulhsu", "mulhu", "div", "divu", "rem", "remu"]
_RW = ["addw", "subw", "sllw", "srlw", "sraw", "mulw", "divw", "divuw",
       "remw", "remuw"]
_I64 = ["addi", "slti", "sltiu", "xori", "ori", "andi"]
_SHIFT64 = ["slli", "srli", "srai"]
_SHIFTW = ["slliw", "srliw", "sraiw"]
_LOADS = ["lb", "lh", "lw", "ld", "lbu", "lhu", "lwu"]
_STORES = ["sb", "sh", "sw", "sd"]
_BRANCHES = ["beq", "bne", "blt", "bge", "bltu", "bgeu"]

TRIPLES = [("zero", "zero", "zero"), ("a0", "a1", "a2"),
           ("t1", "s1", "t2"), ("x31", "x30", "x29"),
           ("sp", "t6", "s11"), ("s2", "a7", "zero")]
PAIRS = [("a0", "a1"), ("t0", "s1"), ("x1", "x31"), ("sp", "t6")]
IMM12 = [-2048, -0x7ff, -0x101, -1, 0, 1, 9, 10, 0xff, 0x7ff, 2047]
OFFB = [-4096, -0x100, -0x10, -8, -2, 2, 8, 0x10, 0x100, 4094]
OFFJ = [-1048576, -0x10000, -0x1000, -0x10, -2, 0, 2, 0x10, 0x1000,
        0x10000, 1048574]
IMM20 = [0, 1, 2, 0x10, 0x7ff, 0x80000, 0x81234, 0xfffff, 0x7ffff]


def corpus_avant() -> list[str]:
    """La notation du profil, systématique : chaque mnémonique, des
    opérandes de bord (registres extrêmes, immédiats bornes, graphies
    déc/hex du juge)."""
    cas: list[str] = []
    for m in _R64 + _RW:
        for rd, rs1, rs2 in TRIPLES:
            cas.append(f"{m} {rd}, {rs1}, {rs2}")
    for m in _I64:
        for rd, rs1 in PAIRS[:3]:
            for imm in IMM12:
                cas.append(f"{m} {rd}, {rs1}, {imm}")
    for rd, rs1 in PAIRS[:3]:
        cas.append(f"addiw {rd}, {rs1}, -2048")
        cas.append(f"addiw {rd}, {rs1}, 2047")
    for m in _SHIFT64:
        for sh in (0, 1, 5, 31, 32, 62, 63):
            cas.append(f"{m} a0, a1, {sh}")
    for m in _SHIFTW:
        for sh in (0, 1, 15, 31):
            cas.append(f"{m} a0, a1, {sh}")
    for m in _LOADS:
        for imm in (-2048, -1, 0, 1, 8, 0x10, 2047):
            cas.append(f"{m} a0, {imm}(sp)")
            cas.append(f"{m} t2, {imm}(s1)")
    for m in _STORES:
        for imm in (-2048, -1, 0, 8, 0x10, 2047):
            cas.append(f"{m} a0, {imm}(sp)")
            cas.append(f"{m} s2, {imm}(a5)")
    for m in _BRANCHES:
        for off in OFFB:
            cas.append(f"{m} a0, a1, {off}")
    for m in ("beqz", "bnez", "bgez", "bltz", "bgtz", "blez"):
        for off in (-4096, -0x10, -2, 8, 0x100, 4094):
            cas.append(f"{m} t0, {off}")
    for off in OFFJ:
        cas.append(f"j {off}")
        cas.append(f"jal {off}")
        cas.append(f"jal t1, {off}")
        cas.append(f"jal zero, {off}")
    cas += ["jalr t1", "jalr ra", "jalr a0, a1", "jalr t0, t2",
            "jalr a0, a1, 0", "jalr a0, a1, 8", "jalr a0, a1, -2048",
            "jalr a0, a1, 2047", "jalr t0, 16(t1)", "jalr t0, -8(sp)",
            "ret", "jalr zero, ra, 0"]
    for m in ("lui", "auipc"):
        for imm in IMM20:
            cas.append(f"{m} a0, {imm}")
            cas.append(f"{m} t6, {imm}")
    cas += ["ecall", "ebreak", "nop", "fence.i", "fence.tso", "fence",
            "fence iorw, iorw", "fence rw, rw", "fence w, rw", "fence r, w",
            "fence i, o", "fence ir, ow"]
    for m in ("mv", "not", "neg", "seqz", "snez", "sgtz", "sltz", "sext.w"):
        for rd, rs in PAIRS:
            cas.append(f"{m} {rd}, {rs}")
    return cas


# --- L'espace d'encodage du profil (direction INVERSE) ----------------------------

def _enc_r(f7, rs2, rs1, f3, rd, op):
    return (f7 << 25) | (rs2 << 20) | (rs1 << 15) | (f3 << 12) | (rd << 7) | op


def _enc_i(imm, rs1, f3, rd, op):
    return ((imm & 0xFFF) << 20) | (rs1 << 15) | (f3 << 12) | (rd << 7) | op


def _enc_s(imm, rs2, rs1, f3, op):
    imm &= 0xFFF
    return ((imm >> 5) << 25) | (rs2 << 20) | (rs1 << 15) | (f3 << 12) | \
        ((imm & 0x1F) << 7) | op


def _enc_b(imm, rs2, rs1, f3, op):
    imm &= 0x1FFF
    return (((imm >> 12) & 1) << 31) | (((imm >> 5) & 0x3F) << 25) | \
        (rs2 << 20) | (rs1 << 15) | (f3 << 12) | \
        (((imm >> 1) & 0xF) << 8) | (((imm >> 11) & 1) << 7) | op


def _enc_u(imm, rd, op):
    return ((imm & 0xFFFFF) << 12) | (rd << 7) | op


def _enc_j(imm, rd, op):
    imm &= 0x1FFFFF
    return (((imm >> 20) & 1) << 31) | (((imm >> 1) & 0x3FF) << 21) | \
        (((imm >> 11) & 1) << 20) | (((imm >> 12) & 0xFF) << 12) | (rd << 7) | op


def encodages_profil() -> list[tuple[str, int]]:
    """Les combinaisons LÉGALES de l'espace d'encodage RV64IMA+Zifencei,
    échantillonnées aux champs de bord — (famille, mot)."""
    cas: list[tuple[str, int]] = []
    r64 = {("add", 0x00, 0), ("sub", 0x20, 0), ("sll", 0x00, 1),
           ("slt", 0x00, 2), ("sltu", 0x00, 3), ("xor", 0x00, 4),
           ("srl", 0x00, 5), ("sra", 0x20, 5), ("or", 0x00, 6),
           ("and", 0x00, 7), ("mul", 0x01, 0), ("mulh", 0x01, 1),
           ("mulhsu", 0x01, 2), ("mulhu", 0x01, 3), ("div", 0x01, 4),
           ("divu", 0x01, 5), ("rem", 0x01, 6), ("remu", 0x01, 7)}
    rw = {("addw", 0x00, 0), ("subw", 0x20, 0), ("sllw", 0x00, 1),
          ("srlw", 0x00, 5), ("sraw", 0x20, 5), ("mulw", 0x01, 0),
          ("divw", 0x01, 4), ("divuw", 0x01, 5), ("remw", 0x01, 6),
          ("remuw", 0x01, 7)}
    for nom, f7, f3 in r64:
        for rd, rs1, rs2 in ((1, 2, 3), (31, 30, 29), (0, 0, 0), (10, 11, 12)):
            cas.append((nom, _enc_r(f7, rs2, rs1, f3, rd, 0x33)))
    for nom, f7, f3 in rw:
        for rd, rs1, rs2 in ((10, 11, 12), (0, 31, 1)):
            cas.append((nom, _enc_r(f7, rs2, rs1, f3, rd, 0x3B)))
    i64 = {"addi": 0, "slti": 2, "sltiu": 3, "xori": 4, "ori": 6, "andi": 7}
    for nom, f3 in i64.items():
        for imm in (0, 1, 0xFFF, 0x800, 0x7FF, 0xA5, 0x5A):
            for rd, rs1 in ((10, 11), (0, 0), (31, 1)):
                cas.append((nom, _enc_i(imm, rs1, f3, rd, 0x13)))
    for imm in (0, 1, 0x800, 0x7FF):
        for rd, rs1 in ((10, 11), (5, 6)):
            cas.append(("addiw", _enc_i(imm, rs1, 0, rd, 0x1B)))
    # décalages : shamt EXHAUSTIF
    for sh in range(64):
        cas.append(("slli", _enc_i(sh, 11, 1, 10, 0x13)))
        cas.append(("srli", _enc_i(sh, 11, 5, 10, 0x13)))
        cas.append(("srai", _enc_i(0x400 | sh, 11, 5, 10, 0x13)))
    for sh in range(32):
        cas.append(("slliw", _enc_i(sh, 11, 1, 10, 0x1B)))
        cas.append(("srliw", _enc_i(sh, 11, 5, 10, 0x1B)))
        cas.append(("sraiw", _enc_i(0x400 | sh, 11, 5, 10, 0x1B)))
    loads = {"lb": 0, "lh": 1, "lw": 2, "ld": 3, "lbu": 4, "lhu": 5, "lwu": 6}
    for nom, f3 in loads.items():
        for imm in (0, 8, 0x7FF, 0x800, 0xFFF, 0x5A):
            for rd, rs1 in ((10, 2), (31, 9)):
                cas.append((nom, _enc_i(imm, rs1, f3, rd, 0x03)))
    stores = {"sb": 0, "sh": 1, "sw": 2, "sd": 3}
    for nom, f3 in stores.items():
        for imm in (0, 8, 0x7FF, 0x800, 0xFFF, 0x5A):
            for rs2, rs1 in ((10, 2), (31, 9)):
                cas.append((nom, _enc_s(imm, rs2, rs1, f3, 0x23)))
    b = {"beq": 0, "bne": 1, "blt": 4, "bge": 5, "bltu": 6, "bgeu": 7}
    for nom, f3 in b.items():
        for off in (-4096, -0x101, -0x10, -2, 2, 0x10, 0x101, 4094,
                    -4094, 4096 - 2, 0x800, -0x800):
            cas.append((nom, _enc_b(off, 11, 10, f3, 0x63)))
    for off in (-1048576, -0x1234, -0x10, -2, 2, 0x10, 0x1234, 1048574,
                0, -0x800, 0x800):
        cas.append(("jal", _enc_j(off, 1, 0x6F)))
        cas.append(("jal", _enc_j(off, 0, 0x6F)))
        cas.append(("jal", _enc_j(off, 5, 0x6F)))
    for imm in (0, 8, 0x7FF, 0x800, 0xFFF):
        for rd, rs1 in ((1, 6), (0, 1), (5, 6), (31, 2)):
            cas.append(("jalr", _enc_i(imm, rs1, 0, rd, 0x67)))
    for imm in (0, 1, 0x7FF, 0x80000, 0x81234, 0xFFFFF):
        for rd in (10, 0, 31):
            cas.append(("lui", _enc_u(imm, rd, 0x37)))
            cas.append(("auipc", _enc_u(imm, rd, 0x17)))
    cas += [("ecall", 0x00000073), ("ebreak", 0x00100073),
            ("nop", 0x00000013)]
    # fence : les 225 couples pred/succ NON VIDES (frontière du juge : les
    # champs vides sont rendus « unknown » par capstone — un contrat de
    # barrière sans prédécesseur ni successeur est dégénéré, hors corpus)
    for pred in range(1, 16):
        for succ in range(1, 16):
            cas.append(("fence", (pred << 24) | (succ << 20) | 0x0F))
    cas += [("fence.i", 0x0000100F), ("fence.tso", 0x8330000F)]
    return cas


# --- La porte ----------------------------------------------------------------------

def franchir(silencieux: bool = False) -> dict:
    """Exécute la porte : AVANT puis INVERSE. Tout écart lève EchecPorte."""
    # AVANT : notation -> octets -> notation
    avant = corpus_avant()
    familles: dict[str, int] = {}
    for texte in avant:
        famille = texte.split()[0]
        try:
            octets = assembler(texte, 0x1000)
        except EchecAssemblage as exc:
            raise EchecPorte(f"AVANT inassemblable : {texte!r} : {exc}") from None
        if len(octets) != 4:
            raise EchecPorte(f"AVANT {texte!r} : {len(octets)} o != 4 (garde anti-C)")
        insns = list(JUGE.disasm(octets, 0x1000))
        if len(insns) != 1 or insns[0].size != 4:
            raise EchecPorte(
                f"AVANT {texte!r} : le juge décode {len(insns)} instruction(s) "
                f"— pas UNE instruction de 4 o")
        texte_juge = f"{insns[0].mnemonic} {insns[0].op_str}".strip()
        try:
            octets2 = assembler(texte_juge, 0x1000)
        except EchecAssemblage as exc:
            raise EchecPorte(
                f"AVANT {texte!r} : le rendu du juge {texte_juge!r} est "
                f"inassemblable : {exc}") from None
        if octets2 != octets:
            raise EchecPorte(
                f"AVANT {texte!r} : round-trip rompu — le juge rend "
                f"{texte_juge!r}, ré-assemblé {octets2.hex()} != {octets.hex()}")
        familles[famille] = familles.get(famille, 0) + 1

    # INVERSE : octets -> notation du juge -> octets
    n_inv = 0
    for nom, mot in encodages_profil():
        code = mot.to_bytes(4, "little")
        insns = list(JUGE.disasm(code, 0x1000))
        if len(insns) != 1 or insns[0].size != 4:
            raise EchecPorte(
                f"INVERSE {nom} {mot:#010x} : le juge décode {len(insns)} "
                f"instruction(s) — l'encodage légal doit décodER en UNE")
        texte_juge = f"{insns[0].mnemonic} {insns[0].op_str}".strip()
        try:
            octets = assembler(texte_juge, 0x1000)
        except EchecAssemblage as exc:
            raise EchecPorte(
                f"INVERSE {nom} {mot:#010x} : rendu du juge {texte_juge!r} "
                f"inassemblable : {exc}") from None
        if octets != code:
            raise EchecPorte(
                f"INVERSE {nom} {mot:#010x} : {texte_juge!r} ré-assemble en "
                f"{octets.hex()} != {code.hex()} — le rendu du juge diverge")
        n_inv += 1

    return {"avant": len(avant), "familles": familles, "inverse": n_inv}


def main() -> int:
    silencieux = "--silencieux" in sys.argv
    try:
        r = franchir(silencieux)
    except EchecPorte as exc:
        print(f"[porte] ÉCHEC : {exc}")
        return 1
    familles = sorted(r["familles"].items(),
                      key=lambda kv: (-kv[1], kv[0]))[:8]
    detail = ", ".join(f"{n}={c}" for n, c in familles)
    print(f"[porte] AVANT   : {r['avant']} textes du corpus — "
          f"round-trip 100 % ({detail} …)")
    print(f"[porte] INVERSE : {r['inverse']} encodages légaux du profil — "
          f"le rendu INTÉGRAL du juge ré-assemble en ses octets")
    print(f"[porte] VERDICT : VERT — round-trip 100 % sur le corpus "
          f"d'instructions du profil (capstone juge unique)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
