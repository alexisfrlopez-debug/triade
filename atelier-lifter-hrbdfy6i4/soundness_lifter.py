#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""soundness_lifter.py — LE CHANTIER 1 DE L'INSTRUCTION hrbdfy6i4 (la vague 11,
le PLAN-HRBDFY6I4 gelé § 1) : LA SOUNDNESS DU LIFTER CONFRONTÉE À L'OBSERVÉ.
VERSION CORRIGÉE (la reprise de l'atelier) — LA MÉTHODE EXACTE.

LA CORRECTION MÉTHODOLOGIQUE (le premier passage, ses artefacts NOMMÉS) :
le premier passage rapportait « 1110 DIVERGENCES » dont la quasi-totalité
était des ARTÉFACTS DE MÉTHODE sur les DRAPEAUX — la méthode d'observation
(diff avant/après + perturbation des drapeaux PAR MOT ENTIER 0x247/0xA82)
ne pouvait PAS distinguer LECTURE et ÉCRITURE de rflags :
  — « lecture observée non déclarée : rflags » pour inc/ror/rol : ces
    instructions ÉCRIVENT certains bits de rflags (inc : OF/SF/ZF/AF/PF ;
    ror : CF/OF) et laissent les autres PERSISTER — la perturbation par
    mot entier mutait des bits ÉCRITS (recomposés — pas de trace) ET des
    bits NON ÉCRITS (persistants) : la valeur finale mélangait les deux,
    n'était NI la valeur mutée NI la valeur de référence → le test
    « auto-référentiel » du premier passage déclarait une LECTURE
    FANTÔME ;
  — « écriture déclarée non observée : rflags » pour sub : l'écriture des
    drapeaux depuis le seul état initial 0x202 était INVISIBLE quand les
    drapeaux calculés valaient exactement 0x202 (une écriture qui réécrit
    la même valeur ne se voit pas au diff).
LA MÉTHODE EXACTE (la lettre de la reprise) — la confrontation
INSTRUCTION PAR INSTRUCTION :
  — ÉCRITURES OBSERVÉES : exécution depuis l'état S ; tout registre (les
    GPR ET les XMM ET rflags par la lecture Unicorn EFLAGS) dont la valeur
    diffère après exécution = écrit ; l'observation est l'UNION sur les
    ESSAIS (2 familles d'états P/S × 5 états initiaux de drapeaux
    0x202/0x247/0xA82/0x602/0x212 — l'essai 0x602 porte DF=1 : l'écriture
    de DF par cld/std devient OBSERVABLE, l'essai 0x212 porte AF=1) ;
    toute adresse mémoire touchée par les crochets UC_MEM_WRITE = écrite
    (adresses et tailles exactes — le crochet tire même si la valeur
    réécrite est identique : l'écriture mémoire N'A PAS le problème
    d'invisibilité) ;
  — LECTURES OBSERVÉES — LA SENTINELLE DIFFÉRENTIELLE : pour l'instruction
    I depuis l'état S, pour CHAQUE registre R : ré-exécution depuis S avec
    R muté — R xor 0xA5A5A5A5A5A5A5A5 pour les GPR (rsp : +0x11111/−0x9AC1
    dans la pile mappée — l'xor full-width sortirait de la région mappée :
    la dépendance de rsp se lit sur les ADRESSES des événements, pas sur
    une faute), les XMM par un masque 128 bits ; rflags par BASCULE D'UN
    SEUL BIT à la fois (CF, PF, AF, ZF, SF, DF, OF — les 7 drapeaux
    observables ; TF/AC/IOPL exclus : la bascule changerait le MODE, pas
    la donnée) ; si UNE QUELCONQUE sortie (n'importe quel registre, rflags,
    rip — le canal d'observation des branches — ou un octet mémoire écrit)
    diffère de l'exécution de référence, ALORS R était LU ; LE TEST
    D'ÉVIDENCE PAR OCTET (GPR/XMM) ET PAR BIT (rflags) sur le registre
    muté LUI-MÊME tue l'artéfact de persistance : un octet/bit muté qui
    n'est pas réécrit persiste à la valeur mutée — ce n'est PAS une
    lecture ; un octet/bit réécrit depuis des sources indépendantes vaut
    la référence — PAS une lecture ; SEUL un octet/bit réécrit DEPUIS
    LUI-MÊME (bswap, shl, xchg, cmc…) échappe aux deux valeurs — LECTURE ;
    une SECONDE mutation complémentaire (xor 0x5A5A… — chaque bit basculé
    par exactement l'une des deux mutations) est tentée quand la première
    ne montre rien ET que le lifter ne déclare pas la lecture (les
    lectures masquées — test al, 0x40 ne lit al qu'au bit 6, l'xor 0xA5
    ne le bascule pas — l'oubli resterait dans la direction bénigne, la
    seconde mutation le rattrape) ;
  — LA FAUTE DÉPENDANTE : la sentinelle faute là où la référence réussit
    (l'xor 0xA5A5 produit des adresses non mappées : tout usage du registre
    comme base/index/destination de saut faute) = le registre était LU
    (l'adresse dépend de sa valeur) ; de même un essai de drapeaux qui
    faute là où le canonical réussit = rflags LU ;
  - LES LECTURES MÉMOIRE : les crochets UC_MEM_READ donnent les
    adresses/tailles exactes.
LE RIP (nommé, reconduit du premier passage) : exclu des ensembles
comparés (le moteur de taint ne suit pas rip), CANAL D'OBSERVATION des
drapeaux (une branche dont le sens change = les drapeaux lus).

LES ENSEMBLES DÉCLARÉS (le lifter) : capstone CS.detail (opérandes
access + regs_read/regs_write, au grain du PARENT 64 bits — écrire al
ÉCRIT rax) PLUS LA TABLE D'AUGMENTATION ci-dessous (chaque ligne NOMMÉE :
le lifter validé = capstone + ces lignes — les implicites que capstone
5.0 ne porte pas). Le modèle v200/v210 de non-interférence repose sur ces
ensembles (les sites d'adresse par les opérandes mémoire, la condition des
branches par les drapeaux, la propagation par les lectures).

LA RÈGLE DE VERDICT : une DIVERGENCE = un accès OBSERVÉ non DÉCLARÉ (le
lifter rate un accès — LA UNSOUNDNESS RÉELLE) ; une déclaration JAMAIS
observée à AUCUN essai = SUR-DÉCLARATION conservative (BÉNIGNE, comptée à
part) ; les déclarations HORS UNIVERS OBSERVABLE (st(i), mm*, bnd*, fpsw,
mxcsr — l'oracle ne voit que GPR+XMM+rflags+ mémoire) : comptées à part,
jamais un échec.

LE CORPUS : (1) les 16 blocs (les 13 de la vague 10 + tls13-04, tls13-08,
tls13-17 — la réponse « le lifter porte-t-il leurs instructions » vit
ici) confrontés AUX ENCODAGES DISTINCTS (1818 instructions → 942
encodages ; l'oracle est indépendant de l'adresse : l'instruction est
placée à 0x400000, l'adresse d'origine ne change NI les ensembles
déclarés NI l'observation — JUSTIFICATION : la sentinelle coûte ~150
exécutions par encodage, les 1818 instructions ne portent que 942
encodages distincts, confronter chaque occurrence ne ferait que répéter
la même preuve) ; (2) LE CORPUS MUTÉ — chaque classe (mnémonique × forme
d'opérandes) des blocs mutée systématiquement (octets 0 et 1 parcourus de
0x00 à 0xFF), les mutants VALIDES (capstone décode UNE instruction de la
longueur exacte ET keystone ré-assemble aux MÊMES octets) confrontés.
LE CONTRÔLE NÉGATIF : le lifter muté (le modèle d'ensemble altéré d'UNE
instruction — une écriture déclarée retirée, puis une lecture déclarée
retirée) ATTRAPÉ à la première divergence.

Sorties : soundness_registres.csv (les ensembles par encodage/mutant) ·
soundness_console.txt (la capture) · code retour 0 si zéro divergence et
le contrôle négatif attrapé."""
from __future__ import annotations

import importlib.util
import pathlib
import sys
import time

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "atelier-lifter-hrbdfy6i4"
sys.path.insert(0, str(REPO / "loupe"))
sys.path.insert(0, str(REPO / "m4"))
sys.path.insert(0, str(REPO / "tls13"))

import capstone  # noqa: E402
import keystone  # noqa: E402
import unicorn  # noqa: E402
from unicorn import Uc, UcError  # noqa: E402
from unicorn import (  # noqa: E402
    UC_ARCH_X86, UC_MODE_64, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE,
    UC_HOOK_CODE, UC_ERR_FETCH_UNMAPPED,
)
from unicorn.x86_const import UC_X86_REG_RIP, UC_X86_REG_EFLAGS  # noqa: E402
import unicorn.x86_const as x86c  # noqa: E402

KS = keystone.Ks(keystone.KS_ARCH_X86, keystone.KS_MODE_64)
CS = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
CS.detail = True
X86 = capstone.x86

# ---------------------------------------------------------- les blocs du corpus
LES_13 = ["tls13-01", "tls13-02", "tls13-03", "tls13-05", "tls13-06",
          "tls13-07", "tls13-13", "tls13-14", "tls13-15", "tls13-16",
          "tls13-18", "tls13-19", "loupe-06"]
EXTENSION = ["tls13-04", "tls13-08", "tls13-17"]       # la couverture étendue


def charger_module(nom, chemin):
    s = importlib.util.spec_from_file_location(nom, chemin)
    m = importlib.util.module_from_spec(s)
    sys.modules[nom] = m
    s.loader.exec_module(m)
    return m


B4 = charger_module("b4_lft", REPO / "m4" / "build_m4.py")
LAY = charger_module("lay_lft", REPO / "tls13" / "layout.py")
HN = charger_module("hn_lft", REPO / "loupe" / "harnais_noyau.py")


def assembler_bloc_bid(bid):
    """La notation assemblée (keystone, la machinerie v210 en lecture)."""
    num = int(bid.split("-")[1])
    if bid.startswith("tls13"):
        f = list((REPO / "tls13" / "notation").glob(f"{bid}-*.asm"))[0]
        rva, slot = LAY.SLOTS_TLS13[f"h100{num:03d}"]
    else:
        f = list((REPO / "loupe" / "notation").glob(f"{bid}-*.asm"))[0]
        rva, slot = HN.L.SLOTS_LOUPE[f"i110{num:03d}"]
    octets, _ = B4.assembler_bloc(KS, str(f), rva, slot)
    return rva, octets


# --------------------------------------------- LE MODÈLE DÉCLARÉ (le lifter)
# le parent 64 bits de chaque nom de registre (la comparaison au grain du
# parent : écrire al ÉCRIT rax — l'observation voit le parent)
_PARENT = {}
for _i, (_b8, _b32, _b64) in enumerate([
        ("al", "eax", "rax"), ("cl", "ecx", "rcx"), ("dl", "edx", "rdx"),
        ("bl", "ebx", "rbx"), ("sil", "esi", "rsi"), ("dil", "edi", "rdi"),
        ("spl", "esp", "rsp"), ("bpl", "ebp", "rbp")] + [
        (f"r{i}b", f"r{i}d", f"r{i}") for i in range(8, 16)]):
    _PARENT[_b8] = _b64
    _PARENT[_b32] = _b64
    _PARENT[_b64] = _b64
for _i, (_w, _b64) in enumerate([
        ("ax", "rax"), ("cx", "rcx"), ("dx", "rdx"), ("bx", "rbx"),
        ("si", "rsi"), ("di", "rdi"), ("sp", "rsp"), ("bp", "rbp")] + [
        (f"r{i}w", f"r{i}") for i in range(8, 16)]):
    _PARENT[_w] = _b64
for _h, _b64 in [("ah", "rax"), ("ch", "rcx"), ("dh", "rdx"), ("bh", "rbx")]:
    _PARENT[_h] = _b64
for _i in range(16):
    _PARENT[f"xmm{_i}"] = f"xmm{_i}"

GPR = ["rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp",
       "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15"]
XMM = [f"xmm{i}" for i in range(16)]
UNIVERS = set(GPR) | set(XMM) | {"rflags"}     # l'oracle ne voit QUE cela

UC_GPR = {r: getattr(x86c, f"UC_X86_REG_{r.upper()}") for r in GPR}
UC_XMM = {f"xmm{i}": getattr(x86c, f"UC_X86_REG_XMM{i}") for i in range(16)}

# LES PRÉFIXES (le mnémonique de base pour la table : « lock add » → add,
# « rep movsb » → movsb, « repz ret » → ret — le RET ignore le préfixe)
PREFIXES = ("lock ", "rep ", "repe ", "repne ", "repz ", "repnz ")
OPS_CHAINE = ("movs", "stos", "lods", "scas", "cmps", "ins", "outs")

# ============================ LA TABLE D'AUGMENTATION (chaque ligne NOMMÉE) ==
# A1  PARENT : la granularité parent 64 bits (al/ax/eax → rax).
# A2  lea : AUCUN accès mémoire (le calcul d'adresse seul).
# A3  push/call : l'empilement W [rsp-8] (capstone ne porte pas le memop).
# A4  pop/ret : le dépilement R [rsp+0] (« repz ret » compris — préfixe ignoré).
# A5  leave : la lecture R [rbp+0] (leave = mov rsp,rbp + pop rbp).
# A6  test : rflags ÉCRIT (capstone ne le déclare que pour cmp) ET les
#     opérandes d'accès nul (acc=0 — le [r14] de « test [r14], al ») LUES.
# A7  cmps* : les opérandes mémoire d'accès nul (cmpsd décode acc=0) LUES.
# A8  rol/ror/rcl/rcr/shl/sar [mem] : lecture-modification-ÉCRITURE —
#     capstone déclare l'accès R seul (a1).
# A9  movhps/movlps/movnt*/movnti [mem], reg : des MAGASINS — capstone
#     déclare R (a1), c'est W (l'opérande mémoire en position destination).
# A10 xadd : rflags ÉCRIT (capstone : rien). cmpxchg : rflags ÉCRIT, rax
#     ÉCRIT (l'accumulateur reçoit la mémoire à l'échec) et le [mem] ÉCRIT
#     (à la réussite) — capstone : lecture seule.
# A11 lar/lsl : rflags ÉCRIT (ZF de la validité du sélecteur).
# A12 cmc : rflags LU (complément du CF) ; rcl/rcr : rflags LU (le CF
#     entre dans la rotation) — capstone ne déclare RIEN.
# A13 xlatb : lit rbx et al, écrit al, lit 1 octet à [rbx + zext(al)]
#     (capstone : aucun opérande).
# A14 enter imm, L : lit rbp/rsp, écrit rbp/rsp, W [rsp-8] (l'empilement
#     de rbp) et pour i = 1..L-1 : R [rbp-8i] + W [rsp-8-8i] (la chaîne des
#     cadres — vérifié sur unicorn, la sémantique Intel SDM ENTER).
# A15 maskmovq/maskmovdqu : le magasin masqué W taille 8/16 à [rdi]
#     (capstone : rien ; le masque nul n'écrit rien — sur-déclaration
#     bénigne quand le masque est nul).
# A16 bt/bts/btr/btc [mem], reg : l'ACCÈS ÉTENDU — le mot CONTENANT le bit
#     à [ea + taille × (idx >> log2(taille×8))] (Intel SDM : le déplacement
#     de bit au-delà du premier mot sort de l'opérande) — R pour bt, W pour
#     bts/btr/btc (l'accès de base [ea, ea+taille) déclaré par capstone
#     demeure : sur-déclaration bénigne quand le bit est dans le premier mot).
# A17 x87 — les DIRECTIONS/TAILLES que capstone porte mal : fst/fstp/fist/
#     fistp/fisttp/fbstp [mem] : ÉCRITURES (capstone dit R) ; fnsave W 108,
#     fstenv/fnstenv W 28, fstcw/fnstcw/fstsw/fnstsw W 2, fxsave W 512,
#     frstor R 108, fldenv R 28, fldcw R 2, fxrstor R 512 (capstone : tailles
#     4/8 et directions fausses).
# A18 cpuid/rdtsc/div/idiv/mul/imul/cdq/bsf/bsr/shld/shrd/comiss : portés
#     correctement par capstone — aucune ligne.
# =============================================================================

A6_TEST = {"test"}
A7_CMPS = ("cmpsb", "cmpsw", "cmpsd", "cmpsq")
A8_SHIFTS = {"rol", "ror", "rcl", "rcr", "shl", "shr", "sar", "sal"}
A9_STORES = {"movhps", "movhpd", "movlps", "movlpd", "movnti", "movntps",
             "movntpd", "movntss", "movntsd", "movntq", "movntdq"}
A10_XADD = {"xadd"}
A11_LAR = {"lar", "lsl"}
A12_LIT_DRAPEAUX = {"cmc", "rcl", "rcr"}
A17_X87 = {          # mnémonique -> (direction, taille|None = celle de l'opérande)
    "fst": ("W", None), "fstp": ("W", None), "fist": ("W", None),
    "fistp": ("W", None), "fisttp": ("W", None), "fbstp": ("W", None),
    "fnsave": ("W", 108), "fstenv": ("W", 28), "fnstenv": ("W", 28),
    "fstcw": ("W", 2), "fnstcw": ("W", 2), "fstsw": ("W", 2),
    "fnstsw": ("W", 2), "fxsave": ("W", 512),
    "frstor": ("R", 108), "fldenv": ("R", 28), "fldcw": ("R", 2),
    "fxrstor": ("R", 512),
}


def base_mnemo(m):
    """Le mnémonique de base (les préfixes strippés)."""
    for p in PREFIXES:
        if m.startswith(p):
            return m[len(p):]
    return m


def parent(nom):
    return _PARENT.get(nom, nom)


def ensembles_declares(ins):
    """LES ENSEMBLES DÉCLARÉS par le lifter pour UNE instruction : les
    registres lus/écrits (parents 64 bits) et les accès mémoire déclarés
    (type, taille, base, index, déplacement, échelle, registre-décaleur
    pour l'accès étendu de bt)."""
    lectures, ecritures = set(), set()
    memops = []          # (typ, taille, base, index, disp, scale, idxreg)
    m = ins.mnemonic
    mb = base_mnemo(m)
    mem_idx = []
    for op in ins.operands:
        if op.type == X86.X86_OP_MEM:
            base = ins.reg_name(op.mem.base) if op.mem.base else None
            index = ins.reg_name(op.mem.index) if op.mem.index else None
            mem_idx.append((op, base, index))
    for pos, op in enumerate(ins.operands):
        if op.type == X86.X86_OP_REG:
            p = parent(ins.reg_name(op.reg))
            if (op.access & 1) or mb in A6_TEST:          # A6 : test lit ses opérandes
                lectures.add(p)
            if op.access & 2:
                ecritures.add(p)
        elif op.type == X86.X86_OP_MEM:
            base = ins.reg_name(op.mem.base) if op.mem.base else None
            index = ins.reg_name(op.mem.index) if op.mem.index else None
            if base and base != "rip":
                lectures.add(parent(base))       # le calcul d'adresse LIT
            if index and index != "rip":
                lectures.add(parent(index))
            if mb == "lea":
                continue          # A2 : lea — aucun accès mémoire
            acc = op.access
            if mb in A6_TEST or mb in A7_CMPS:
                acc |= 1                                   # A6/A7 : acc=0 → LU
            if mb in A8_SHIFTS and (acc & 1):
                acc |= 2                                   # A8 : RMW → ÉCRIT
            if mb in A9_STORES and pos == 0:
                acc = 2                                     # A9 : le magasin
            if mb == "cmpxchg":
                acc |= 3                                    # A10 : RMW cmpxchg
            taille = op.size
            if mb in A17_X87:
                d, t = A17_X87[mb]
                acc = 2 if d == "W" else 1
                if t:
                    taille = t
            if acc & 1:
                memops.append(("R", taille, base, index, op.mem.disp,
                               op.mem.scale, None))
            if acc & 2:
                memops.append(("W", taille, base, index, op.mem.disp,
                               op.mem.scale, None))
    for r in ins.regs_read:
        n = ins.reg_name(r)
        if n not in ("rip",):
            lectures.add(parent(n))
    for r in ins.regs_write:
        n = ins.reg_name(r)
        if n not in ("rip",):
            ecritures.add(parent(n))
    # ---------------- les augmentations implicites ----------------
    if mb in ("push", "call"):                          # A3 : l'empilement
        memops.append(("W", 8, "rsp", None, -8, 1, None))
    if mb in ("pop", "ret"):                            # A4 : le dépilement
        memops.append(("R", 8, "rsp", None, 0, 1, None))
    if mb == "leave":                                   # A5 : leave
        memops.append(("R", 8, "rbp", None, 0, 1, None))
    if mb in A10_XADD:                                  # A10 : xadd → drapeaux
        ecritures.add("rflags")
    if mb == "cmpxchg":                     # A10 : cmpxchg → drapeaux + rax
        ecritures.add("rflags")
        ecritures.add("rax")
    if mb in A11_LAR:                                   # A11 : lar/lsl → ZF
        ecritures.add("rflags")
    if mb in A12_LIT_DRAPEAUX:                          # A12 : cmc/rcl/rcr
        lectures.add("rflags")
    if mb == "xlatb":                                   # A13 : xlatb
        lectures.update({"rbx", "rax"})
        ecritures.add("rax")
        memops.append(("RXLAT", 1, "rbx", None, 0, 1, None))
    if mb == "enter":                                   # A14 : enter
        lectures.update({"rbp", "rsp"})
        ecritures.update({"rbp", "rsp"})
        niveau = ins.operands[1].imm if len(ins.operands) > 1 else 0
        memops.append(("W", 8, "rsp", None, -8, 1, None))
        for i in range(1, max(niveau, 1)):
            memops.append(("R", 8, "rbp", None, -8 * i, 1, None))
            memops.append(("W", 8, "rsp", None, -8 - 8 * i, 1, None))
    if mb in ("maskmovq", "maskmovdqu"):                # A15 : maskmov*
        lectures.add("rdi")
        memops.append(("W", 8 if mb == "maskmovq" else 16,
                       "rdi", None, 0, 1, None))
    if mb in ("bt", "bts", "btr", "btc") and len(mem_idx) == 2 \
            and mem_idx[1][0].type == X86.X86_OP_REG:   # A16 : l'accès étendu
        op0, base0, index0 = mem_idx[0]
        reg1 = ins.reg_name(mem_idx[1][0].reg)
        typ = "Rext" if mb == "bt" else "Wext"
        memops.append((typ, op0.size, base0, index0, op0.mem.disp,
                       op0.mem.scale, reg1))
    return lectures, ecritures, memops


# ------------------------------------------------------- L'ORACLE UNICORN
CODE = 0x400000                    # l'instruction placée à adresse fixe
FPUSTUB = 0xC00000                 # la page du stub fninit + pxor mm* (A-hygiène)
RSP_BASE = 0x7E000000              # la pile (fenêtre aléatoire ±0x20000)
SLOTS_P = [0x411234 + i * 0x10879 for i in range(16)]   # les pointeurs (P)
VALS_S = [0x1000 + i * 0x661 for i in range(16)]        # les petits (S)
GRAINE = 20261120                  # la mémoire aléatoire REPRODUCTIBLE
MUT_GPR = [0xA5A5A5A5A5A5A5A5, 0x5A5A5A5A5A5A5A5A]     # les mutations (complémentaires)
MUT_RSP = [RSP_BASE + 0x11111, RSP_BASE - 0x9AC1]      # rsp : dans la pile mappée
MASQUE_XMM1 = 0x9E3779B97F4A7C15001632632B6D5A88       # la mutation xmm (128 bits)
MASQUE_XMM2 = MASQUE_XMM1 ^ ((1 << 128) - 1)           # ... et sa complémentaire
ESSAIS_FLAGS = [0x202, 0x247, 0xA82, 0x602, 0x212]
#    0x202 : canonical (CF=PF=AF=ZF=SF=DF=OF=0, IF=1)
#    0x247 : CF=1, PF=1, ZF=1 · 0xA82 : SF=1, OF=1 · 0x602 : DF=1 · 0x212 : AF=1
BITS_DRAPEAUX = [0, 2, 4, 6, 7, 10, 11]   # CF, PF, AF, ZF, SF, DF, OF
NOMS_BITS = {0: "CF", 2: "PF", 4: "AF", 6: "ZF", 7: "SF", 10: "DF", 11: "OF"}

STUB_FPU = bytes.fromhex("dbe3") + b"".join(
    bytes.fromhex(f"0fefc{r}") for r in range(8))     # fninit + pxor mm0..7


def touche_fpu(ins):
    """L'instruction peut-elle toucher l'état FPU/MMX (l'hygiène : le stub
    fninit+pxor avant CHAQUE passe — sinon l'état persistant fausserait la
    comparaison sentinelle/référence des flottants) ?"""
    m = ins.mnemonic
    if base_mnemo(m).startswith("f") or m == "wait":
        return True
    if base_mnemo(m) in ("emms", "femms", "maskmovq", "maskmovdqu"):
        return True
    for op in ins.operands:
        if op.type == X86.X86_OP_REG and ins.reg_name(op.reg).startswith("mm"):
            return True
    return False


class Oracle:
    """L'observation EXACTE d'une instruction : les écritures (l'union des
    diffs avant/après sur les ESSAIS + les crochets mémoire), les lectures
    (la sentinelle différentielle, registre par registre, octet par octet
    pour les GPR/XMM, bit par bit pour rflags), la mémoire (les crochets
    UC_MEM_READ/WRITE aux adresses et tailles exactes)."""

    def __init__(self):
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        self.uc.mem_map(0x1000, 0x3FF000)          # donnée basse
        self.uc.mem_map(CODE, 0x1000)              # code
        self.uc.mem_map(0x401000, 0x7FF000)        # donnée haute
        self.uc.mem_map(0x7C000000, 0x4000000)     # pile 64 Mio
        self.uc.mem_map(FPUSTUB, 0x1000)           # la page du stub FPU
        import random
        rng = random.Random(GRAINE)
        self.uc.mem_write(0x1000, rng.randbytes(0x3FF000))
        self.uc.mem_write(0x401000, rng.randbytes(0x7FF000))
        self.uc.mem_write(RSP_BASE - 0x20000, rng.randbytes(0x40000))
        self.uc.mem_write(FPUSTUB, STUB_FPU)
        # l'hygiène des registres SYSTÈME (un mutant lmsw/clts/ldmxcsr/fxrstor
        # polluerait CR0/MXCSR pour les passes suivantes — restaurés à CHAQUE
        # passe ; les valeurs initiales FIXES consignées)
        self.cr = [self.uc.reg_read(x86c.UC_X86_REG_CR0),
                   self.uc.reg_read(x86c.UC_X86_REG_CR2),
                   self.uc.reg_read(x86c.UC_X86_REG_CR3),
                   self.uc.reg_read(x86c.UC_X86_REG_CR4)]
        self.sysregs = []
        for nom in ("UC_X86_REG_GDTR", "UC_X86_REG_IDTR", "UC_X86_REG_LDTR",
                    "UC_X86_REG_TR"):
            try:
                rid = getattr(x86c, nom)
                self.sysregs.append((rid, self.uc.reg_read(rid)))
            except Exception:
                pass
        self.evens = []
        self.touches = {}
        self.uc.hook_add(UC_HOOK_MEM_READ, self._hr)
        self.uc.hook_add(UC_HOOK_MEM_WRITE, self._hw)

    def _hr(self, uc, access, address, size, value, ud):
        self.evens.append(("R", address, size, value))

    def _hw(self, uc, access, address, size, value, ud):
        # le crochet tire AVANT l'engagement de l'écriture : l'original est
        # capturé pour la restauration (la mémoire aléatoire est FIXE — la
        # comparaison référence/sentinelle exige la même mémoire)
        self.evens.append(("W", address, size, value))
        if address not in self.touches:
            self.touches[address] = bytes(uc.mem_read(address, size))

    def _etat(self):
        et = {}
        for r in GPR:
            et[r] = self.uc.reg_read(UC_GPR[r])
        for x in XMM:
            et[x] = self.uc.reg_read(UC_XMM[x])
        et["rflags"] = self.uc.reg_read(UC_X86_REG_EFLAGS)
        et["rip"] = self.uc.reg_read(UC_X86_REG_RIP)
        return et

    def _poser(self, variante, overrides=None, fpu=False):
        if fpu:      # l'hygiène FPU/MMX : l'état DÉTERMINISTE (fninit + mm=0)
            self.uc.emu_start(FPUSTUB, FPUSTUB + len(STUB_FPU), 250000, 0)
        for rid, val in self.sysregs:      # GDTR/IDTR/LDTR/TR restaurés
            try:
                self.uc.reg_write(rid, val)
            except Exception:
                pass
        self.uc.reg_write(x86c.UC_X86_REG_CR0, self.cr[0])
        self.uc.reg_write(x86c.UC_X86_REG_CR2, self.cr[1])
        self.uc.reg_write(x86c.UC_X86_REG_CR3, self.cr[2])
        self.uc.reg_write(x86c.UC_X86_REG_CR4, self.cr[3])
        self.uc.reg_write(x86c.UC_X86_REG_MXCSR, 0x1F80)
        for i, r in enumerate(GPR):
            v = SLOTS_P[i] if variante == "P" else VALS_S[i]
            self.uc.reg_write(UC_GPR[r], v)
        for i, x in enumerate(XMM):
            self.uc.reg_write(UC_XMM[x],
                              0x0102030405060708090A0B0C0D0E0000 + i * 0x1111
                              if variante == "P" else
                              0xF0E0D0C0B0A0900807006005004003000 + i * 0x111)
        self.uc.reg_write(UC_GPR["rsp"], RSP_BASE)
        self.uc.reg_write(UC_X86_REG_EFLAGS, 0x202)
        self.uc.reg_write(UC_X86_REG_RIP, CODE)
        if overrides:
            for k, v in overrides.items():
                if k == "rflags":
                    self.uc.reg_write(UC_X86_REG_EFLAGS, v)
                elif k in UC_GPR:
                    self.uc.reg_write(UC_GPR[k], v)
                elif k in UC_XMM:
                    self.uc.reg_write(UC_XMM[k], v)

    def executer(self, octets, variante, overrides=None, repete=False,
                 fpu=False):
        """UNE passe : retourne None si la passe faute (l'instruction ne
        s'exécute pas dans cet état), sinon (avant, après, événements).
        LA FAUTE AU SUIVANT (UC_ERR_FETCH_UNMAPPED) : le flot de contrôle a
        débarqué sur une adresse non mappée APRÈS l'instruction (ret sur
        pile aléatoire, appel indirect) — les effets de l'instruction SONT
        commis (les crochets ont tiré) : la passe réussit. TOUTE AUTRE
        faute (lecture/écriture non mappée pendant l'instruction, #DE, #UD,
        timeout d'une répétition démesurée) : la passe FAUTE. Le garde-fou
        de temps : 50 ms — une répétée honnête (rcx borné à 0x37/0x29)
        tient en microsecondes ; la sentinelle de rcx par xor produit un
        compte démesuré — le TIMEOUT est la faute dépendante (rcq LU)."""
        self.evens = []
        self.touches = {}
        self.uc.mem_write(CODE, octets)
        self._poser(variante, overrides, fpu)
        avant = self._etat()
        try:
            self.uc.emu_start(CODE, CODE + len(octets), 50000,
                              0 if repete else 1)
        except UcError as e:
            if e.errno != UC_ERR_FETCH_UNMAPPED:
                return None
        finally:
            apres = self._etat()
            for a, b in self.touches.items():
                self.uc.mem_write(a, b)      # la mémoire FIXE restaurée
        return avant, apres, list(self.evens)

    # ------------------------------------------ la confrontation d'une passe
    @staticmethod
    def _depend(base, sent, exclu, mut_val):
        """LA DÉPENDANCE (le critère de lecture) : une QUELCONQUE sortie —
        tout registre, rflags, rip (le canal des branches), les accès
        mémoire (adresses, tailles, valeurs) — diffère entre la référence
        et la sentinelle ; POUR LE REGISTRE MUTÉ LUI-MÊME : le TEST
        D'ÉVIDENCE PAR OCTET (GPR/XMM) OU PAR BIT (rflags) — un octet/bit
        muté non réécrit PERSISTE à la valeur mutée (pas une lecture), un
        octet/bit réécrit depuis des sources indépendantes vaut la
        référence (pas une lecture) ; SEUL l'octet/bit réécrit DEPUIS
        LUI-MÊME échappe aux deux (lecture)."""
        avant_b, apres_b, ev_b = base
        avant_s, apres_s, ev_s = sent
        for k in apres_b:
            if k == exclu:
                continue
            if apres_b[k] != apres_s[k]:
                return True
        if ev_b != ev_s:
            return True
        if exclu == "rflags":
            for b in range(32):
                fb = (apres_b["rflags"] >> b) & 1
                fs = (apres_s["rflags"] >> b) & 1
                fm = (mut_val >> b) & 1
                if fs != fm and fs != fb:
                    return True
        else:
            taille = 8 if exclu in GPR else 16
            for i in range(taille):
                dec = 8 * i
                fb = (apres_b[exclu] >> dec) & 0xFF
                fs = (apres_s[exclu] >> dec) & 0xFF
                fm = (mut_val >> dec) & 0xFF
                if fs != fm and fs != fb:
                    return True
        return False

    def observer(self, ins):
        """L'OBSERVATION COMPLÈTE : retourne (lectures, écritures,
        événements_canoniques, essais_ok) ou None si aucune passe ne
        réussit (l'encodage n'est pas observable sous unicorn)."""
        octets = bytes(ins.bytes)
        m = ins.mnemonic
        mb = base_mnemo(m)
        repete = any(m.startswith(p) for p in PREFIXES) \
            and mb.startswith(OPS_CHAINE)
        fpu = touche_fpu(ins)
        passes = {}
        for variante in ("P", "S"):
            ov = {"rcx": 0x37 if variante == "P" else 0x29} if repete else None
            for fi in ESSAIS_FLAGS:
                ovf = dict(ov) if ov else {}
                ovf["rflags"] = fi
                passes[(variante, fi)] = self.executer(
                    octets, variante, ovf, repete, fpu)
        essais_ok = sum(1 for p in passes.values() if p is not None)
        if essais_ok == 0:
            return None
        # --- LES ÉCRITURES : l'union des diffs sur les essais -------------
        ecritures = set()
        for (variante, fi), passe in passes.items():
            if passe is None:
                continue
            avant, apres, ev = passe
            for r in GPR + XMM:
                if apres[r] != avant[r]:
                    ecritures.add(r)
            if apres["rflags"] != fi:
                ecritures.add("rflags")
        # --- la mémoire observée : les canonical (0x202) des deux variantes
        evenements = []
        canon = {}
        for variante in ("P", "S"):
            canon[(variante, 0x202)] = passes[(variante, 0x202)]
            if passes[(variante, 0x202)] is not None:
                evenements.extend(
                    (variante, *e) for e in passes[(variante, 0x202)][2])
        # --- LES LECTURES : la sentinelle différentielle ------------------
        lectures = set()
        for variante in ("P", "S"):
            ov = {"rcx": 0x37 if variante == "P" else 0x29} if repete else {}
            base = passes[(variante, 0x202)]
            if base is None:
                continue
            # (a) la faute dépendante des DRAPEAUX : un essai faute là où le
            #     canonical réussit → la conduite dépend des drapeaux → LUS
            for fi in ESSAIS_FLAGS[1:]:
                if passes[(variante, fi)] is None:
                    lectures.add("rflags")
            # (b) les sentinelles GPR (les DEUX mutations complémentaires ;
            #     la seconde ne roule que si la première ne montre rien — la
            #     seconde bascule les bits que la première laisse immobiles)
            for r in GPR:
                muts = (MUT_RSP if r == "rsp" else
                        [base[0][r] ^ g for g in MUT_GPR])
                for g in muts:
                    sent = self.executer(octets, variante,
                                         {**ov, r: g}, repete, fpu)
                    if sent is None:
                        lectures.add(r)
                        break
                    if self._depend(base, sent, r, g):
                        lectures.add(r)
                        break
            # (c) les sentinelles XMM (la porte : le mutant porte un
            #     opérande registre de 16 octets — aucun autre chemin ne
            #     lit un XMM ; l'indice de forme, le juge reste l'observé)
            if any(op.type == X86.X86_OP_REG and op.size == 16
                   for op in ins.operands):
                for x in XMM:
                    for masque in (MASQUE_XMM1, MASQUE_XMM2):
                        g = base[0][x] ^ masque
                        sent = self.executer(octets, variante,
                                             {**ov, x: g}, repete, fpu)
                        if sent is None:
                            lectures.add(x)
                            break
                        if self._depend(base, sent, x, g):
                            lectures.add(x)
                            break
            # (d) les sentinelles DRAPEAUX : un bit à la fois
            for b in BITS_DRAPEAUX:
                g = 0x202 ^ (1 << b)
                sent = self.executer(octets, variante,
                                     {**ov, "rflags": g}, repete, fpu)
                if sent is None:
                    lectures.add("rflags")
                elif self._depend(base, sent, "rflags", g):
                    lectures.add("rflags")
        return lectures, ecritures, evenements, essais_ok, canon


# --------------------------------------------- la confrontation d'une instruction
_taille_courante = 0


def _ea(memop, avant):
    """L'adresse effective d'un memop déclaré depuis l'état avant."""
    typ, taille, base, index, disp, scale, idxreg = memop
    ea = disp
    if base == "rip":
        ea += CODE + _taille_courante
    elif base:
        ea += avant[parent(base)]
    if index:
        ea += avant[parent(index)] * scale
    return ea


def att_couverture(ins, memops, passes):
    """La couverture en OCTETS déclarée (les répétées : n itérations à la
    taille de l'élément depuis le canonical DF=0 ; l'accès étendu de bt :
    le mot contenant le bit ; xlatb : rbx + zext(al) ; enter : la chaîne
    des cadres)."""
    global _taille_courante
    _taille_courante = ins.size
    att = {"R": set(), "W": set()}
    for variante in ("P", "S"):
        passe = passes.get((variante, 0x202))
        if passe is None:
            continue
        avant = passe[0]
        n = avant["rcx"] if (any(ins.mnemonic.startswith(p) for p in PREFIXES)
                             and base_mnemo(ins.mnemonic).startswith(OPS_CHAINE)) \
            else 1
        for memop in memops:
            typ, taille, base, index, disp, scale, idxreg = memop
            if typ in ("Rext", "Wext"):
                ea = _ea(memop, avant) + taille * (
                    avant[parent(idxreg)] >> ((taille * 8).bit_length() - 1))
                att[typ[0]].update(range(ea, ea + taille))
                continue
            if typ == "RXLAT":
                ea = avant["rbx"] + (avant["rax"] & 0xFF)
                att["R"].update(range(ea, ea + taille))
                continue
            ea = _ea(memop, avant)
            for k in range(n):
                att[typ].update(range(ea + k * taille,
                                      ea + k * taille + taille))
    return att


def confronter(ins, oracle, mutation=None):
    """LA CONFRONTATION : déclaré vs observé. Retourne (divergences,
    surdéclarations, hors_observable, observation) — les divergences = la
    direction qui casse la soundness (observé non déclaré) ; les
    surdéclarations = la direction conservatrice (déclaré non observé à
    AUCUN essai) ; hors_observable = les déclarations hors GPR+XMM+rflags
    (st(i), mm*, bnd*, fpsw, mxcsr — l'oracle est aveugle là)."""
    octets = bytes(ins.bytes)
    lectures_d, ecritures_d, memops = ensembles_declares(ins)
    hors = sorted((lectures_d | ecritures_d) - UNIVERS)
    lectures_d &= UNIVERS
    ecritures_d &= UNIVERS
    if mutation == "ecriture":
        cible = next((r for r in sorted(ecritures_d) if r in GPR), None)
        if cible:
            ecritures_d = ecritures_d - {cible}
    elif mutation == "lecture":
        cible = next((r for r in sorted(lectures_d) if r in GPR
                      and r != "rsp"), None)
        if cible:
            lectures_d = lectures_d - {cible}
    obs = oracle.observer(ins)
    if obs is None:
        return None, None, hors, None
    lectures_o, ecritures_o, evenements, essais_ok, canon = obs
    divergences, surdecl = [], []
    for r in sorted(ecritures_o):
        if r not in ecritures_d:
            divergences.append(f"écriture observée non déclarée : {r}")
    for r in sorted(lectures_o):
        if r not in lectures_d:
            divergences.append(f"lecture observée non déclarée : {r}")
    for r in sorted(ecritures_d):
        if r not in ecritures_o:
            surdecl.append(f"écriture déclarée non observée : {r}")
    for r in sorted(lectures_d):
        if r not in lectures_o:
            surdecl.append(f"lecture déclarée non observée : {r}")
    # LA MÉMOIRE : la couverture en octets (les répétées et les accès
    # vector non alignés sont fractionnés par unicorn — la COUVERTURE
    # d'octets par type est le juge exact) — depuis les passes canonical
    # DE L'OBSERVATION (les mêmes — jamais ré-exécutées : la cohérence
    # référence/sentinelle/mémoire tient au MÊME jeu de passes)
    att = att_couverture(ins, memops, canon)
    obsp = {"R": set(), "W": set()}
    for (variante, typ, adresse, taille, valeur) in evenements:
        obsp[typ].update(range(adresse, adresse + taille))
    for typ in ("R", "W"):
        hors_oct = obsp[typ] - att[typ]
        if hors_oct:
            divergences.append(
                f"accès mémoire {typ} observé hors déclaration : "
                f"{len(hors_oct)} octet(s) à {min(hors_oct):#x}")
        manq = att[typ] - obsp[typ]
        if manq:
            surdecl.append(
                f"accès mémoire {typ} déclaré non observé : "
                f"{len(manq)} octet(s) à {min(manq):#x}")
    return divergences, surdecl, hors, (lectures_o, ecritures_o, evenements,
                                        essais_ok)


# ---------------------------------------------------------------------- main
def main():
    t0 = time.time()
    rap = ["LE CHANTIER 1 DE hrbdfy6i4 — LA SOUNDNESS DU LIFTER CONFRONTÉE "
           "À L'OBSERVÉ UNICORN — LA VERSION CORRIGÉE (la méthode exacte)",
           ""]
    oracle = Oracle()
    lignes_csv = [["bloc", "adresse", "octets", "mnémonique", "forme",
                   "lectures_déclarées", "lectures_observées",
                   "écritures_déclarées", "écritures_observées",
                   "mem_R_déclarées", "mem_W_déclarées", "mem_observées",
                   "essais", "divergences", "surdéclarations",
                   "hors_observable"]]

    # ---- (0) LE CONTRÔLE DES ARTÉFACTS du premier passage ------------------
    # les cinq familles faussement divergentes : inc/ror (la « lecture »
    # fantôme de rflags), sub (l'« écriture invisible » de rflags), mov al,
    # [r15+rcx] (la « lecture » fantôme de rax par persistance partielle) —
    # la méthode exacte doit les tenir PROPRES
    rap.append("LE CONTRÔLE DES ARTÉFACTS (les faux positifs du premier "
               "passage, la correction à l'œuvre) :")
    for hexs, attendu in [
            ("41ffc5", "inc r13d : ÉCRIT rflags, ne LE LIT PAS"),
            ("c1ca11", "ror edx, 0x11 : ÉCRIT rflags, ne LE LIT PAS"),
            ("4829d8", "sub rax, rbx : ÉCRIT rflags (multi-essais), "
                       "ne LE LIT PAS"),
            ("418a040f", "mov al, [r15+rcx] : ÉCRIT rax, ne LE LIT PAS"),
            ("f3a4", "rep movsb : LIT rflags (DF) et rcx/rsi/rdi"),
            ("7540", "jne +0x40 : LIT rflags (le canal rip)"),
            ("4811d8", "adc rax, rbx : LIT et ÉCRIT rflags")]:
        ins = next(CS.disasm(bytes.fromhex(hexs), CODE), None)
        div, sur, hors, obs = confronter(ins, oracle)
        ld, ed, _ = ensembles_declares(ins)
        rap.append(f"  {ins.mnemonic} {ins.op_str:28s} [{hexs}] — {attendu}"
                   f" ; divergences={div} ; surdécl={sur}")
    rap.append("")

    # ---- (1) les instructions des blocs ------------------------------------
    encodages = {}          # octets -> (premier bloc, ins, occurrences)
    occurrences = {}
    for bid in LES_13 + EXTENSION:
        rva, octets = assembler_bloc_bid(bid)
        n = 0
        for ins in CS.disasm(octets, rva):
            n += 1
            b = bytes(ins.bytes)
            if b not in encodages:
                encodages[b] = (bid, ins)
            occurrences[b] = occurrences.get(b, 0) + 1
        rap.append(f"  {bid} : {n} instructions")
    total_instr = sum(occurrences.values())
    rap.insert(3, f"LES BLOCS : {len(LES_13) + len(EXTENSION)} "
                  f"({', '.join(LES_13 + EXTENSION)}) — {total_instr} "
                  f"instructions, {len(encodages)} encodages distincts")

    divergences_tot, surdecl_tot, non_obs, hors_tot = 0, 0, 0, 0
    detail_div = []
    for b, (bid, ins) in sorted(encodages.items(),
                                key=lambda kv: kv[1][1].address):
        div, sur, hors, obs = confronter(ins, oracle)
        if div is None:
            non_obs += 1
            continue
        divergences_tot += len(div)
        surdecl_tot += len(sur)
        hors_tot += len(hors)
        if div:
            detail_div.append((bid, ins, div))
        lectures_o, ecritures_o, evenements, vok = obs
        ld, ed, memops = ensembles_declares(ins)
        lignes_csv.append([
            bid, hex(ins.address), b.hex(), ins.mnemonic,
            ins.op_str, ";".join(sorted(ld)), ";".join(sorted(lectures_o)),
            ";".join(sorted(ed)), ";".join(sorted(ecritures_o)),
            sum(1 for m in memops if m[0].startswith("R")),
            sum(1 for m in memops if m[0].startswith("W")), len(evenements),
            vok, " | ".join(div) if div else "—",
            " | ".join(sur) if sur else "—", ";".join(hors)])
    rap += ["",
            f"LE CORPUS (1) — LES BLOCS : {total_instr} instructions "
            f"({len(encodages)} encodages distincts — chaque encodage "
            f"confronté une fois, l'oracle étant indépendant de l'adresse) : "
            f"{divergences_tot} DIVERGENCE(S) — "
            f"{'ZÉRO — la soundness tenue' if divergences_tot == 0 else 'ROUGE'}"
            f" ; {surdecl_tot} sur-déclarations bénignes (la direction "
            f"conservatrice, comptée à part) ; {hors_tot} déclarations hors "
            f"univers observable ; {non_obs} encodages non observables"]
    for bid, ins, div in detail_div[:12]:
        rap.append(f"    !! {bid} {ins.address:#x} "
                   f"{ins.mnemonic} {ins.op_str} : {div}")

    # ---- (2) le corpus muté -------------------------------------------------
    formes = {}
    for b, (bid, ins) in encodages.items():
        t = tuple(("R" if op.type == X86.X86_OP_REG else
                   ("M" if op.type == X86.X86_OP_MEM else "I"),
                   op.size if op.type != X86.X86_OP_IMM else 0)
                  for op in ins.operands)
        formes.setdefault((ins.mnemonic, t), b)
    rap += ["",
            f"LES FORMES : {len(formes)} classes (mnémonique × forme "
            f"d'opérandes) — chaque classe mutée systématiquement : "
            f"l'octet 0 ET l'octet 1 parcourus de 0x00 à 0xFF"]
    mut_ess = mut_val = mut_conf = mut_div = mut_sur = mut_nobs = 0
    mut_hors = 0
    mut_excl = {}
    for (mnemo, forme), b in sorted(formes.items()):
        for pos in (0, 1):
            if len(b) <= pos:
                continue
            for octet in range(256):
                if b[pos] == octet:
                    continue
                m = bytearray(b)
                m[pos] = octet
                mb = bytes(m)
                mut_ess += 1
                ins_m = next(CS.disasm(mb, CODE), None)
                if ins_m is None or ins_m.size != len(mb):
                    continue            # le mutant ne décode pas à l'identique
                try:
                    renc, _ = KS.asm(f"{ins_m.mnemonic} {ins_m.op_str}"
                                     if ins_m.op_str else ins_m.mnemonic, CODE)
                    if renc is None or bytes(renc) != mb:
                        continue        # l'assembleur ne le re-encode pas
                except Exception:
                    continue            # l'assembleur le rejette : invalide
                mut_val += 1
                div, sur, hors, obs = confronter(ins_m, oracle)
                if div is None:
                    mut_nobs += 1
                    mut_excl[base_mnemo(ins_m.mnemonic)] = \
                        mut_excl.get(base_mnemo(ins_m.mnemonic), 0) + 1
                    continue
                mut_conf += 1
                mut_div += len(div)
                mut_sur += len(sur)
                mut_hors += len(hors)
                if div:
                    detail_div.append(("MUTANT", ins_m, div))
                lectures_o, ecritures_o, evenements, vok = obs
                ld, ed, memops = ensembles_declares(ins_m)
                lignes_csv.append([
                    "MUTANT", hex(CODE), mb.hex(), ins_m.mnemonic,
                    ins_m.op_str, ";".join(sorted(ld)),
                    ";".join(sorted(lectures_o)), ";".join(sorted(ed)),
                    ";".join(sorted(ecritures_o)),
                    sum(1 for mm in memops if mm[0].startswith("R")),
                    sum(1 for mm in memops if mm[0].startswith("W")),
                    len(evenements), vok,
                    " | ".join(div) if div else "—",
                    " | ".join(sur) if sur else "—", ";".join(hors)])
    rap += ["",
            f"LE CORPUS (2) — LES MUTANTS : {mut_ess} mutants essayés, "
            f"{mut_val} VALIDES (capstone décode la longueur exacte ET "
            f"keystone ré-assemble aux mêmes octets), {mut_conf} confrontés "
            f"({mut_nobs} non exécutables sous unicorn — "
            f"{';'.join(f'{k}:{v}' for k, v in sorted(mut_excl.items()))}) : "
            f"{mut_div} DIVERGENCE(S) — "
            f"{'ZÉRO — la soundness tenue' if mut_div == 0 else 'ROUGE'} ; "
            f"{mut_sur} sur-déclarations bénignes ; {mut_hors} hors "
            f"univers observable"]

    # ---- (3) le contrôle négatif : le lifter muté ---------------------------
    # le modèle d'ensemble altéré d'UNE instruction : l'écriture déclarée
    # d'un registre retirée, puis la lecture — le juge doit l'attraper À LA
    # PREMIÈRE divergence
    cible = None
    for b, (bid, ins) in sorted(encodages.items(),
                                key=lambda kv: kv[1][1].address):
        if ins.mnemonic == "mov" and ins.op_str.startswith("rax, qword ptr"):
            cible = (b, bid, ins)
            break
    neg = []
    for mode in ("ecriture", "lecture"):
        div, sur, hors, obs = confronter(cible[2], oracle, mutation=mode)
        if div:
            neg.append((mode, div[0]))
    ok_neg = len(neg) == 2
    rap += ["",
            f"LE CONTRÔLE NÉGATIF (le lifter muté — le modèle d'ensemble "
            f"altéré d'UNE instruction, {cible[1]} "
            f"{cible[2].mnemonic} {cible[2].op_str}) : "
            + (" ; ".join(f"le retrait de la {m} déclarée ATTRAPÉ : {d}"
                          for m, d in neg)
               if ok_neg else "NON ATTRAPÉ — ROUGE (le juge est aveugle)")]

    # ---- les sorties ---------------------------------------------------------
    with open(ICI / "soundness_registres.csv", "w", encoding="utf-8") as f:
        for ligne in lignes_csv:
            f.write("\t".join(str(x) for x in ligne) + "\n")
    rap += ["",
            f"LE BILAN : {total_instr} instructions de blocs ({len(encodages)}"
            f" encodages distincts) + {mut_conf} mutants confrontés ; "
            f"{divergences_tot + mut_div} DIVERGENCES "
            f"({'ZÉRO — LA SOUNDNESS DU LIFTER TENUE' if divergences_tot + mut_div == 0 else 'ROUGE'}) ; "
            f"{surdecl_tot + mut_sur} sur-déclarations bénignes (comptées à "
            f"part — la direction conservatrice) ; "
            f"{hors_tot + mut_hors} déclarations hors univers observable ; "
            f"le contrôle négatif "
            f"{'ATTRAPÉ' if ok_neg else 'NON ATTRAPÉ'} ; "
            f"{time.time() - t0:.1f} s"]
    texte = "\n".join(rap) + "\n"
    (ICI / "soundness_console.txt").write_text(texte, encoding="utf-8")
    print(texte)
    return 0 if (divergences_tot + mut_div == 0 and ok_neg) else 2


if __name__ == "__main__":
    raise SystemExit(main())
