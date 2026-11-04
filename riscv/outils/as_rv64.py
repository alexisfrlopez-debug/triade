#!/usr/bin/env python3
"""as_rv64.py — L'ASSEMBLEUR RV64IMA+Zifencei MAISON DU DÉPÔT (jalon M7-(a)).

Le livrable propre du chantier (fiche riscv64 § 6) : keystone 0.9.2 ne porte
pas l'architecture RISC-V (constat re-vérifié au chantier) — l'encodage
RV64 est régulier (six formats R/I/S/B/U/J, 4 octets, champs fixes), il vit
ICI, dans le dépôt, sans dépendance nouvelle, dans la lignée « à la main »
du projet. Capstone 5.0.7 demeure le JUGE UNIQUE du round-trip : tout texte
que le juge émet doit ré-assembler en ses octets (assemble → désassemble →
ré-assemble, tout écart d'instruction, d'opérande ou de taille = échec).

SANS extension C (fiche § 1) : toute instruction fait EXACTEMENT 4 octets,
alignement 4 — un encodage 2 o n'existe pas ici, un décalage de saut impair
est REFUSÉ (imm[0] n'est jamais encodé en B/J).

Pseudos acceptés — le jeu EXACT du rendu capstone 5.0.7 (constaté au
catalogue du chantier, chaque forme est éprouvée par la porte round-trip
du corpus d'instructions du profil) :
  nop              = addi x0, x0, 0          sext.w rd, rs = addiw rd, rs, 0
  mv rd, rs        = addi rd, rs, 0          not rd, rs    = xori rd, rs, -1
  neg rd, rs       = sub rd, x0, rs          negw rd, rs   = subw rd, x0, rs
  snez rd, rs      = sltu rd, x0, rs         sgtz rd, rs   = slt rd, x0, rs
  sltz rd, rs      = slt rd, rs, x0          beqz/bnez/bgez/bltz rs, off
  bgtz/blez rs, off                           j off = jal x0, off
  jal off          = jal ra, off             jalr rs1 = jalr ra, rs1, 0
  jalr rd, rs1     = jalr rd, rs1, 0         ret = jalr x0, ra, 0
  fence            = fence iorw, iorw        fence.tso

Tout refus est NOMMÉ (EchecAssemblage) : plage immédiate, décalage hors
pas, champ hors domaine, mnémonique inconnu — jamais d'octet silencieux.

Usage (outil importé par auteur.py et build_m7.py) :
  from as_rv64 import assembler
  octets = assembler("addi a0, a1, 0x10", 0x1000)   # -> exactement 4 octets
"""

from __future__ import annotations

VERSION = "1.0.0"

# --- Registres : noms psABI + formes xN (les deux graphies, une seule vérité) ----

REGISTRES: dict[str, int] = {}
for _i in range(32):
    REGISTRES[f"x{_i}"] = _i
REGISTRES.update({
    "zero": 0, "ra": 1, "sp": 2, "gp": 3, "tp": 4,
    "t0": 5, "t1": 6, "t2": 7, "s0": 8, "fp": 8, "s1": 9,
    "a0": 10, "a1": 11, "a2": 12, "a3": 13, "a4": 14, "a5": 15,
    "a6": 16, "a7": 17, "s2": 18, "s3": 19, "s4": 20, "s5": 21,
    "s6": 22, "s7": 23, "s8": 24, "s9": 25, "s10": 26, "s11": 27,
    "t3": 28, "t4": 29, "t5": 30, "t6": 31,
})


class EchecAssemblage(Exception):
    """Tout refus de l'assembleur — nommé, jamais d'octet silencieux."""


# --- Encodages des six formats -----------------------------------------------------

def _enc_r(f7: int, rs2: int, rs1: int, f3: int, rd: int, op: int) -> int:
    return (f7 << 25) | (rs2 << 20) | (rs1 << 15) | (f3 << 12) | (rd << 7) | op


def _enc_i(imm: int, rs1: int, f3: int, rd: int, op: int) -> int:
    return ((imm & 0xFFF) << 20) | (rs1 << 15) | (f3 << 12) | (rd << 7) | op


def _enc_s(imm: int, rs2: int, rs1: int, f3: int, op: int) -> int:
    imm &= 0xFFF
    return ((imm >> 5) << 25) | (rs2 << 20) | (rs1 << 15) | (f3 << 12) | \
        ((imm & 0x1F) << 7) | op


def _enc_b(imm: int, rs2: int, rs1: int, f3: int, op: int) -> int:
    imm &= 0x1FFF
    return (((imm >> 12) & 1) << 31) | (((imm >> 5) & 0x3F) << 25) | \
        (rs2 << 20) | (rs1 << 15) | (f3 << 12) | \
        (((imm >> 1) & 0xF) << 8) | (((imm >> 11) & 1) << 7) | op


def _enc_u(imm: int, rd: int, op: int) -> int:
    return ((imm & 0xFFFFF) << 12) | (rd << 7) | op


def _enc_j(imm: int, rd: int, op: int) -> int:
    imm &= 0x1FFFFF
    return (((imm >> 20) & 1) << 31) | (((imm >> 1) & 0x3FF) << 21) | \
        (((imm >> 11) & 1) << 20) | (((imm >> 12) & 0xFF) << 12) | (rd << 7) | op


# --- Tables d'instructions ---------------------------------------------------------

# R-type op=0x33 : (f7, f3)
_R64 = {
    "add": (0x00, 0), "sub": (0x20, 0), "sll": (0x00, 1), "slt": (0x00, 2),
    "sltu": (0x00, 3), "xor": (0x00, 4), "srl": (0x00, 5), "sra": (0x20, 5),
    "or": (0x00, 6), "and": (0x00, 7),
    "mul": (0x01, 0), "mulh": (0x01, 1), "mulhsu": (0x01, 2), "mulhu": (0x01, 3),
    "div": (0x01, 4), "divu": (0x01, 5), "rem": (0x01, 6), "remu": (0x01, 7),
}
# R-type op=0x3B (mot 32 bits)
_R32W = {
    "addw": (0x00, 0), "subw": (0x20, 0), "sllw": (0x00, 1),
    "srlw": (0x00, 5), "sraw": (0x20, 5),
    "mulw": (0x01, 0), "divw": (0x01, 4), "divuw": (0x01, 5),
    "remw": (0x01, 6), "remuw": (0x01, 7),
}
# I-type arithmétique op=0x13 : f3
_I64 = {"addi": 0, "slti": 2, "sltiu": 3, "xori": 4, "ori": 6, "andi": 7}
# I-type arithmétique op=0x1B (mot)
_IW = {"addiw": 0}
# Chargements op=0x03 : f3
_LOADS = {"lb": 0, "lh": 1, "lw": 2, "ld": 3, "lbu": 4, "lhu": 5, "lwu": 6}
# Stockages op=0x23 : f3
_STORES = {"sb": 0, "sh": 1, "sw": 2, "sd": 3}
# Branches op=0x63 : f3
_BRANCHES = {"beq": 0, "bne": 1, "blt": 4, "bge": 5, "bltu": 6, "bgeu": 7}

# Décalages immédiats — RV64 : imm[11:6] = funct6, shamt 6 bits ;
# RV64W : imm[11:5] = funct7 (7 bits : 0000000 / 0100000), shamt 5 bits
_SHIFTS_64 = {"slli": (0x13, 1, 0x00), "srli": (0x13, 5, 0x00), "srai": (0x13, 5, 0x10)}
_SHIFTS_W = {"slliw": (0x1B, 1, 0x00), "srliw": (0x1B, 5, 0x00), "sraiw": (0x1B, 5, 0x20)}

# AMO op=0x2F (l'extension A du profil — chantier M7-(b) : le verrou tournant
# de tcp-11 exige amoswap, le portage RV64 du lock xchg de l'instance x86-64) :
# {mnemo: (funct3, funct5)} — amoswap SEUL (le seul AMO du corpus), aq/rl
# NULS (relaxed : le corpus est mono-fil, fiche § 5 ; la barrière mémoire vit
# au fence du profil, le chantier (c) porte le verrou multi-profils)
_AMO = {"amoswap.w": (2, 0x01), "amoswap.d": (3, 0x01)}

# fence : lettres du contrat pred/succ — i=8, o=4, r=2, w=1 (l'ordre canonique iorw)
_FENCE_LETTRES = {"i": 8, "o": 4, "r": 2, "w": 1}


# --- Utilitaires d'analyse ---------------------------------------------------------

def _reg(nom: str) -> int:
    nom = nom.strip()
    if nom not in REGISTRES:
        raise EchecAssemblage(f"registre inconnu : {nom!r}")
    return REGISTRES[nom]


def _imm(texte: str, bas: int, haut: int, quoi: str) -> int:
    """Immédiat signé dans [bas, haut] — accepte décimal et 0x (graphie capstone)."""
    t = texte.strip()
    try:
        v = int(t, 0)
    except ValueError:
        raise EchecAssemblage(f"{quoi} : {t!r} n'est pas un nombre") from None
    if not (bas <= v <= haut):
        raise EchecAssemblage(
            f"{quoi} = {v} hors plage [{bas}, {haut}] (imm12 signé) — refus nommé")
    return v


def _imm20(texte: str, quoi: str) -> int:
    """Champ 20 bits de lui/auipc : 0..0xFFFFF, négatif accepté (complément à deux)."""
    t = texte.strip()
    try:
        v = int(t, 0)
    except ValueError:
        raise EchecAssemblage(f"{quoi} : {t!r} n'est pas un nombre") from None
    if -0x80000 <= v <= 0xFFFFF:
        return v & 0xFFFFF
    raise EchecAssemblage(
        f"{quoi} = {v} hors domaine 20 bits ([-0x80000, 0xFFFFF]) — refus nommé")


def _offset(texte: str, bas: int, haut: int, quoi: str) -> int:
    v = _imm(texte, bas, haut, quoi)
    if v % 2:
        raise EchecAssemblage(
            f"{quoi} = {v} IMPAIR — imm[0] n'est jamais encodé (alignement "
            f"4, pas d'extension C — fiche § 1)")
    return v


def _memoire(op: str) -> tuple[int, int]:
    """'8(a1)' -> (8, reg a1) ; '(a1)' -> (0, reg)."""
    t = op.strip()
    if not (t.endswith(")") and "(" in t):
        raise EchecAssemblage(f"opérande mémoire {op!r} hors forme imm(rs1)")
    imm_s, reg_s = t[:-1].split("(", 1)
    imm_s = imm_s.strip()
    imm = int(imm_s, 0) if imm_s else 0
    if not -2048 <= imm <= 2047:
        raise EchecAssemblage(
            f"déplacement mémoire {imm} hors plage imm12 [-2048, 2047] — "
            f"refus nommé (fiche § 7 : l'accès lointain passe par une ancre)")
    return imm, _reg(reg_s)


# --- L'assembleur : une instruction, exactement 4 octets --------------------------

def assembler(texte: str, adresse: int = 0) -> bytes:
    """Assemble UNE instruction (texte) en exactement 4 octets.

    `adresse` est acceptée pour l'uniformité de l'interface (le juge
    round-trip ré-assemble AU MÊME RVA) : les formats B/J codent des
    décalages RELATIFS — le texte porte le décalage, jamais la cible.
    """
    ligne = texte.split(";", 1)[0].strip()
    ligne = ligne.split("#", 1)[0].strip()
    if not ligne:
        raise EchecAssemblage(f"ligne vide : {texte!r}")
    parts = ligne.split(None, 1)
    mnemo = parts[0].lower()
    ops_raw = parts[1] if len(parts) > 1 else ""
    ops = [o.strip() for o in ops_raw.split(",")] if ops_raw.strip() else []
    if any(not o for o in ops):
        raise EchecAssemblage(f"opérande vide dans {texte!r}")

    def besoin(n: int):
        if len(ops) != n:
            raise EchecAssemblage(
                f"{mnemo} : {len(ops)} opérande(s), {n} attendu(s) : {texte!r}")

    # — système
    if mnemo == "ecall":
        besoin(0)
        return (0x00000073).to_bytes(4, "little")
    if mnemo == "ebreak":
        besoin(0)
        return (0x00100073).to_bytes(4, "little")
    if mnemo == "nop":
        besoin(0)
        return (0x00000013).to_bytes(4, "little")

    # — AMO (extension A — l'ISA adresse [rs1] SANS déplacement : le champ
    #   imm12 n'existe pas dans ce format, funct5 occupe les bits 31:27.
    #   Toute demande de déplacement non nul est un REFUS NOMMÉ — jamais un
    #   octet silencieux ; le déplacement vit dans la formation addi déclarée)
    if mnemo in _AMO:
        largeur, f5 = _AMO[mnemo]
        besoin(3)
        imm, rs1 = _memoire(ops[2])
        if imm != 0:
            raise EchecAssemblage(
                f"AMO {mnemo} : déplacement {imm} — l'AMO adresse [rs1] SANS "
                f"déplacement (l'ISA) ; le déplacement vit dans la formation "
                f"addi (l'ancre), jamais ici (refus nommé, jamais un octet "
                f"silencieux)")
        return _enc_r(f5 << 2, _reg(ops[1]), rs1, largeur,
                      _reg(ops[0]), 0x2F).to_bytes(4, "little")

    # — fence (Zifencei : fence.i ; fence pred, succ ; fence.tso)
    if mnemo == "fence.i":
        besoin(0)
        return (0x0000100F).to_bytes(4, "little")
    if mnemo == "fence.tso":
        besoin(0)
        return (0x8330000F).to_bytes(4, "little")
    if mnemo == "fence":
        if not ops:
            pred = succ = 0xF                      # iorw, iorw (forme nue du juge)
        else:
            besoin(2)
            pred, succ = _champ_fence(ops[0]), _champ_fence(ops[1])
        mot = (0 << 28) | (pred << 24) | (succ << 20) | 0x0F
        return mot.to_bytes(4, "little")

    # — pseudos unaire/binaire du juge
    if mnemo == "mv":
        besoin(2)
        return _enc_i(0, _reg(ops[1]), 0, _reg(ops[0]), 0x13).to_bytes(4, "little")
    if mnemo == "sext.w":
        besoin(2)
        return _enc_i(0, _reg(ops[1]), 0, _reg(ops[0]), 0x1B).to_bytes(4, "little")
    if mnemo == "not":
        besoin(2)
        return _enc_i(0xFFF, _reg(ops[1]), 4, _reg(ops[0]), 0x13).to_bytes(4, "little")
    if mnemo == "neg":
        besoin(2)
        return _enc_r(0x20, _reg(ops[1]), 0, 0, _reg(ops[0]), 0x33).to_bytes(4, "little")
    if mnemo == "negw":
        besoin(2)
        return _enc_r(0x20, _reg(ops[1]), 0, 0, _reg(ops[0]), 0x3B).to_bytes(4, "little")
    if mnemo == "seqz":
        besoin(2)
        return _enc_i(1, _reg(ops[1]), 3, _reg(ops[0]), 0x13).to_bytes(4, "little")
    if mnemo == "snez":
        besoin(2)
        return _enc_r(0x00, _reg(ops[1]), 0, 3, _reg(ops[0]), 0x33).to_bytes(4, "little")
    if mnemo == "sgtz":
        besoin(2)
        return _enc_r(0x00, _reg(ops[1]), 0, 2, _reg(ops[0]), 0x33).to_bytes(4, "little")
    if mnemo == "sltz":
        besoin(2)
        return _enc_r(0x00, 0, _reg(ops[1]), 2, _reg(ops[0]), 0x33).to_bytes(4, "little")

    # — branches et leurs pseudos z
    if mnemo in ("beqz", "bnez", "bgez", "bltz", "bgtz", "blez"):
        besoin(2)
        f3 = {"beqz": 0, "bnez": 1, "bgez": 5, "bltz": 4,
              "bgtz": 4, "blez": 5}[mnemo]
        if mnemo in ("bgtz", "blez"):
            rs1, rs2 = 0, _reg(ops[0])             # blt/bge x0, rs
        else:
            rs1, rs2 = _reg(ops[0]), 0
        off = _offset(ops[1], -4096, 4094, f"décalage {mnemo}")
        return _enc_b(off, rs2, rs1, f3, 0x63).to_bytes(4, "little")
    if mnemo in _BRANCHES:
        besoin(3)
        off = _offset(ops[2], -4096, 4094, f"décalage {mnemo}")
        return _enc_b(off, _reg(ops[1]), _reg(ops[0]), _BRANCHES[mnemo],
                      0x63).to_bytes(4, "little")

    # — sauts
    if mnemo == "j":
        besoin(1)
        off = _offset(ops[0], -1048576, 1048574, "décalage j")
        return _enc_j(off, 0, 0x6F).to_bytes(4, "little")
    if mnemo == "jal":
        if len(ops) == 1:                           # jal off (ra implicite — juge)
            off = _offset(ops[0], -1048576, 1048574, "décalage jal")
            return _enc_j(off, 1, 0x6F).to_bytes(4, "little")
        besoin(2)
        off = _offset(ops[1], -1048576, 1048574, "décalage jal")
        return _enc_j(off, _reg(ops[0]), 0x6F).to_bytes(4, "little")
    if mnemo == "ret":
        besoin(0)
        return _enc_i(0, 1, 0, 0, 0x67).to_bytes(4, "little")   # jalr x0, ra, 0
    if mnemo == "jalr":
        if len(ops) == 1:                           # jalr rs1 (ra, 0 implicites)
            return _enc_i(0, _reg(ops[0]), 0, 1, 0x67).to_bytes(4, "little")
        if len(ops) == 2:                           # jalr rd, rs1 (imm 0)
            if "(" in ops[1]:                       #   — ou jalr rd, imm(rs1) (brouillon)
                imm, rs1 = _memoire(ops[1])
                return _enc_i(imm, rs1, 0, _reg(ops[0]), 0x67).to_bytes(4, "little")
            return _enc_i(0, _reg(ops[1]), 0, _reg(ops[0]), 0x67).to_bytes(4, "little")
        besoin(3)
        if "(" in ops[2]:                           # jalr rd, imm(rs1) (brouillon)
            imm, rs1 = _memoire(ops[2])
            return _enc_i(imm, rs1, 0, _reg(ops[0]), 0x67).to_bytes(4, "little")
        imm = _imm(ops[2], -2048, 2047, "décalage jalr")
        return _enc_i(imm, _reg(ops[1]), 0, _reg(ops[0]), 0x67).to_bytes(4, "little")

    # — U-type
    if mnemo in ("lui", "auipc"):
        besoin(2)
        op = 0x37 if mnemo == "lui" else 0x17
        return _enc_u(_imm20(ops[1], mnemo), _reg(ops[0]), op).to_bytes(4, "little")

    # — R-type (64 et W)
    if mnemo in _R64:
        besoin(3)
        f7, f3 = _R64[mnemo]
        return _enc_r(f7, _reg(ops[2]), _reg(ops[1]), f3, _reg(ops[0]),
                      0x33).to_bytes(4, "little")
    if mnemo in _R32W:
        besoin(3)
        f7, f3 = _R32W[mnemo]
        return _enc_r(f7, _reg(ops[2]), _reg(ops[1]), f3, _reg(ops[0]),
                      0x3B).to_bytes(4, "little")

    # — I-type arithmétique (64 et W)
    if mnemo in _I64:
        besoin(3)
        imm = _imm(ops[2], -2048, 2047, f"immédiat {mnemo}")
        return _enc_i(imm, _reg(ops[1]), _I64[mnemo], _reg(ops[0]),
                      0x13).to_bytes(4, "little")
    if mnemo in _IW:
        besoin(3)
        imm = _imm(ops[2], -2048, 2047, f"immédiat {mnemo}")
        return _enc_i(imm, _reg(ops[1]), _IW[mnemo], _reg(ops[0]),
                      0x1B).to_bytes(4, "little")

    # — décalages immédiats (shamt 6 bits / 5 bits W — le bit 25 haut reste 0)
    if mnemo in _SHIFTS_64:
        besoin(3)
        op, f3, f6 = _SHIFTS_64[mnemo]
        sh = _imm(ops[2], 0, 63, f"shamt {mnemo}")
        return _enc_i((f6 << 6) | sh, _reg(ops[1]), f3, _reg(ops[0]),
                      op).to_bytes(4, "little")
    if mnemo in _SHIFTS_W:
        besoin(3)
        op, f3, f7 = _SHIFTS_W[mnemo]
        sh = _imm(ops[2], 0, 31, f"shamt {mnemo}")
        return _enc_i((f7 << 5) | sh, _reg(ops[1]), f3, _reg(ops[0]),
                      op).to_bytes(4, "little")

    # — chargements / stockages
    if mnemo in _LOADS:
        besoin(2)
        imm, rs1 = _memoire(ops[1])
        return _enc_i(imm, rs1, _LOADS[mnemo], _reg(ops[0]), 0x03).to_bytes(4, "little")
    if mnemo in _STORES:
        besoin(2)
        imm, rs1 = _memoire(ops[1])
        return _enc_s(imm, _reg(ops[0]), rs1, _STORES[mnemo], 0x23).to_bytes(4, "little")

    raise EchecAssemblage(
        f"mnémonique inconnu : {mnemo!r} (hors RV64IMA+Zifencei du profil — "
        f"fiche § 1 : PAS d'extension C, PAS de flottants, PAS de CSR)")


def _champ_fence(texte: str) -> int:
    t = texte.strip().lower()
    if not t or any(c not in "iorw" for c in t):
        raise EchecAssemblage(
            f"champ fence {texte!r} hors alphabet iorw (contrat du juge)")
    if len(set(t)) != len(t):
        raise EchecAssemblage(f"champ fence {texte!r} : lettre répétée")
    v = 0
    for c in t:
        v |= _FENCE_LETTRES[c]
    return v


def mnemoniques() -> list[str]:
    """Le corpus de mnémoniques supportés (la porte round-trip le couvre à 100 %)."""
    return sorted(set(
        list(_R64) + list(_R32W) + list(_I64) + list(_IW) + list(_LOADS)
        + list(_STORES) + list(_BRANCHES) + list(_SHIFTS_64) + list(_SHIFTS_W)
        + list(_AMO)
        + ["lui", "auipc", "jal", "jalr", "j", "ret",
           "beqz", "bnez", "bgez", "bltz", "bgtz", "blez",
           "mv", "sext.w", "not", "neg", "negw", "seqz", "snez", "sgtz", "sltz",
           "nop", "ecall", "ebreak", "fence", "fence.i", "fence.tso"]))


if __name__ == "__main__":
    import sys
    rc = 0
    for ligne in sys.stdin:
        ligne = ligne.strip()
        if not ligne:
            continue
        try:
            octets = assembler(ligne)
            print(f"{octets.hex()}  {ligne}")
        except EchecAssemblage as exc:
            print(f"REFUS : {exc}")
            rc = 1
    sys.exit(rc)
