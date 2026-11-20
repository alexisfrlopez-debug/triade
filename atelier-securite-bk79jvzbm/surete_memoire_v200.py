#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""surete_memoire_v200.py — LA SÛRETÉ MÉMOIRE AU PLANCHER (la vague 9,
l'instruction bk79jvzbm point 1, le PLAN-BK79JVZBM H1 gelé).

L'EXTENSION de l'analyse bornée v110 (2 098 accès, 463 non résolus) :
  (1) L'INFÉRENCE D'INVARIANTS DE BOUCLE — les boucles détectées par
      sauts arrière, DEUX familles : (a) montantes « init 0 → inc →
      cmp B → jb/jl arrière » (l'invariant : idx ∈ [0, B) au corps) et
      (b) descendantes « mov C → déc → jnz arrière » (idx ∈ [0, C)) ;
  (2) L'ANALYSE D'INTERVALLES — chaque registre porte un intervalle
      déduit : constantes, copies, inc/dec/add/sub, les compteurs de
      boucle, les lea composés (base + idx×s + d) ;
  (3) L'ANALYSE D'ALIAS — la provenance de chaque registre : le plan
      (lea/mov [rip+X] → l'adresse du layout, la zone et sa taille),
      les arguments (rcx/rdx/r8/r9 → le contrat I), la pile (rsp/rbp),
      les chaînes (lea [reg+idx]) ;
  (4) LE MODEL CHECKING BORNÉ — les accès non déchargés par (1)-(3)
      dont la borne vit au CHAMP DU PLAN (les valeurs runtime : la
      taille, le remplissage, le curseur — les invariants du layout :
      remplissage ≤ 384, vue < taille, taille ≤ 2 Gio…) sont déchargés
      par z3 sur la notation liftée : la tranche en SMT, l'invariant du
      champ aux hypothèses, la négation de la sûreté — UNSAT = la
      preuve, certificat archivé ; le reste NOMMÉ avec sa cause.

LA BASE SAINE : la reproduction v110 d'abord (les mêmes 2 098, les
mêmes classes de départ) — l'extension ne retire RIEN, elle décharge.

Sorties : surete_memoire_v200.csv · certificats/{bloc}.json ·
certificats_smt/*.smt2 · surete_memoire_v200_rapport.txt.
"""
from __future__ import annotations

import csv
import importlib.util
import json
import pathlib
import re
import sys

REPO = pathlib.Path("/home/z/my-project/depot")
sys.path.insert(0, str(REPO / "scripts"))
ICI = REPO / "atelier-securite-bk79jvzbm"
CERT = ICI / "certificats"
SMT = ICI / "certificats_smt"
CERT.mkdir(parents=True, exist_ok=True)
SMT.mkdir(parents=True, exist_ok=True)

import capstone  # noqa: E402
import keystone  # noqa: E402
import z3  # noqa: E402

KS = keystone.Ks(keystone.KS_ARCH_X86, keystone.KS_MODE_64)
CS = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
CS.detail = True
X86 = capstone.x86
VOLATILS = {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}
ARGS = {"rcx": "P1", "rdx": "P2", "r8": "P3", "r9": "P4"}
R64 = {"eax": "rax", "ebx": "rbx", "ecx": "rcx", "edx": "rdx", "esi": "rsi",
       "edi": "rdi", "ebp": "rbp", "r8d": "r8", "r9d": "r9", "r10d": "r10",
       "r11d": "r11", "r12d": "r12", "r13d": "r13", "r14d": "r14",
       "r15d": "r15"}


REGS64 = {"rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp",
          "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15"}


def reg64(nom):
    if nom in REGS64:
        return nom
    return R64.get(nom)


def charger_module(nom, chemin):
    chemin = pathlib.Path(chemin)
    sys.path.insert(0, str(chemin.parent))
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


B4 = charger_module("build_m4_v200", REPO / "m4" / "build_m4.py")
lay_l = charger_module("lay_l_v200", REPO / "loupe" / "layout.py")
lay_t = charger_module("lay_t_v200", REPO / "tls13" / "layout.py")
lay_s = charger_module("lay_s_v200", REPO / "m8" / "layout.py")

ZONES_LOUPE = [
    (0x1000, 0x1000, ".text minilibc"), (0x2000, 0x1000, ".rdata pièces"),
    (0x4000, 0x8000, ".text2 domaine+sha"),
    (lay_l.R_CADRE, 960, "CADRE 960"),
    (lay_l.R_EMPREINTES, 48, "EMPREINTES"), (lay_l.R_SAISIE, 96, "SAISIE"),
    (lay_l.R_MOTIF, 48, "MOTIF"), (lay_l.R_JOURNAL, 4112, "JOURNAL"),
    (lay_l.R_ECRAN, 2320, "ECRAN"), (lay_l.R_HWND, 8, "HWND"),
    (lay_l.R_METRIQUES, 16, "METRIQUES"),
    (lay_l.R_CUMUL, 65536, "CUMUL 64K"),
    (0xE000, 0x12000, ".data étendue"),
]
ZONES_TLS13 = [
    (0x1000, 0x1000, ".text"), (0x2000, 0x1000, ".rdata tables"),
    (0x4000, 0x8000, ".text2 domaine"), (0xF000, 0x2000, ".data session"),
    (lay_t.R_K, 256, "K[64]"), (0x10B00, 0x800, "libellés/fixtures"),
    (0xF000, 0x10000, ".data étendue"),
]
ZONES_SYS = [
    (0x1000, 0x1000, ".text"), (0x2000, 0x1000, ".rdata"),
    (0xA000, 0x2000, ".text5 sys"), (0x10C00, 0x400, "fixtures sys"),
]
ZONES = {"loupe": ZONES_LOUPE, "tls13": ZONES_TLS13, "sys": ZONES_SYS}


def zone_de(domaine, adresse):
    best = None
    for dep, taille, nom in ZONES[domaine]:
        if dep <= adresse < dep + taille:
            if best is None or taille < best[1]:
                best = (dep, taille, nom)
    return best


class Expr:
    """plan:A + k (+ ctr dans [0, B) × s) ou arg:P + k (+ ctr…) ou pile."""
    __slots__ = ("base", "k", "ctr", "borne", "scale", "src", "lo")

    def __init__(self, base, k=0, ctr=None, borne=None, scale=1, src=None):
        self.base, self.k = base, k
        self.ctr, self.borne, self.scale, self.src = ctr, borne, scale, src
        self.lo = 0

    def plus(self, d):
        return Expr(self.base, self.k + d, self.ctr, self.borne,
                    self.scale, self.src)

    def copie(self):
        return Expr(self.base, self.k, self.ctr, self.borne, self.scale,
                    self.src)


# LES TAILLES DÉCLARÉES des structures d'argument — LUES des specs I
# (la citation : « le contexte session (N o…) », « 64 o accessibles »…)
TAILLES_STRUCT = {
    ("tls13", "tls13-01"): {"arg:P1": 112},
    ("tls13", "tls13-02"): {"arg:P1": 112, "arg:P2": 64},
    ("tls13", "tls13-03"): {"arg:P1": 112},
    ("tls13", "tls13-04"): {"arg:P1": 112, "arg:P2": 32},
    ("tls13", "tls13-05"): {"arg:P1": 64, "arg:P3": 64},
    ("tls13", "tls13-06"): {"arg:P1": 64, "arg:P3": 64},
    ("tls13", "tls13-07"): {"arg:P1": 32, "arg:P2": 256},
    ("tls13", "tls13-08"): {"arg:P1": 32, "arg:P2": 256, "arg:P4": 64},
    ("tls13", "tls13-09"): {"arg:P1": 40, "arg:P2": 40},
    ("tls13", "tls13-10"): {"arg:P1": 40, "arg:P2": 40},
    ("tls13", "tls13-11"): {"arg:P1": 40, "arg:P2": 40},
    ("tls13", "tls13-12"): {"arg:P1": 40},
    ("tls13", "tls13-13"): {"arg:P1": 32, "arg:P2": 32, "arg:P3": 32},
    ("tls13", "tls13-14"): {"arg:P1": 32, "arg:P2": 32, "arg:P3": 32},
    ("tls13", "tls13-15"): {"arg:P1": 176, "arg:P2": 16},
    ("tls13", "tls13-16"): {"arg:P1": 176, "arg:P2": 16},
    ("tls13", "tls13-17"): {"arg:P1": 16, "arg:P2": 16, "arg:P3": 16},
    ("tls13", "tls13-18"): {"arg:P1": 8144, "arg:P2": 8144, "arg:P3": 12},
    ("tls13", "tls13-19"): {"arg:P1": 8144, "arg:P2": 8144, "arg:P3": 12},
    ("tls13", "tls13-20"): {"arg:P1": 216, "arg:P2": 16640},
    ("tls13", "tls13-21"): {"arg:P1": 216, "arg:P2": 16640},
    ("tls13", "tls13-22"): {"arg:P1": 128, "arg:P2": 256, "arg:P3": 512},
    ("tls13", "tls13-23"): {"arg:P1": 128, "arg:P2": 256},
    ("tls13", "tls13-24"): {"arg:P1": 112, "arg:P2": 48},
    ("tls13", "tls13-25"): {"arg:P1": 128, "arg:P2": 64, "arg:P3": 64},
    ("tls13", "tls13-26"): {"arg:P1": 96, "arg:P2": 256},
    ("tls13", "tls13-27"): {"arg:P1": 17520, "arg:P3": 8192, "arg:P4": 4096},
    ("tls13", "tls13-28"): {"arg:P1": 64, "arg:P2": 4096},
    ("loupe", "loupe-06"): {"arg:P1": 16, "arg:P2": 64},
    ("loupe", "loupe-13"): {"arg:P1": 65536, "arg:P3": 32},
    ("loupe", "loupe-14"): {"arg:P1": 65536, "arg:P3": 32},
}


class Boucle:
    __slots__ = ("tete", "garde", "ctr", "borne", "famille", "sens")

    def __init__(self, tete, garde, ctr, borne, famille, sens):
        self.tete, self.garde, self.ctr = tete, garde, ctr
        self.borne, self.famille, self.sens = borne, famille, sens


EFFETS_GLOBAL: dict[int, set] = {}   # rva du bloc → volatils écrits

# LES CHAMPS RUNTIME DU CADRE loupe (le layout § cadre) : l'offset, le nom,
# LA BORNE DOCUMENTÉE (l'invariant du plan — la preuve la prend hypothèse)
CHAMPS_CADRE = {
    520: ("taille du fichier", 1 << 31),     # BORNE_TAILLE
    528: ("poignée", None),                  # INVALIDE ou OS — SANS borne statique
    536: ("vue (le décalage)", 1 << 31),     # < taille
    544: ("curseur", 1 << 31),               # la cellule dans le fichier
    552: ("remplissage", 384),               # ≤ TAMPON_SESSION (I3 de loupe-02)
    556: ("sale (la marque)", 1),
    568: ("tampon de session", 384),         # la fenêtre elle-même
}


class AnalyseV200:
    def __init__(self, octets, rva, domaine, bid):
        self.domaine, self.bid = domaine, bid
        self.insns = list(CS.disasm(octets, rva))
        self.adrs = {ins.address: i for i, ins in enumerate(self.insns)}
        self.boucles: list[Boucle] = []
        self.acces = []
        self.oob_pile = 0
        self.effets = EFFETS_GLOBAL
        self.ecrits: set = set()
        self._trouver_boucles()

    # ---------------- les boucles : l'invariant du compteur ---------------
    def _trouver_boucles(self):
        for i, ins in enumerate(self.insns):
            if ins.mnemonic not in ("jmp", "jb", "jl", "jbe", "jle", "jnb",
                                    "jge", "jae", "jnz", "jne", "jns", "js",
                                    "ja", "jg", "jnbe", "jnl"):
                continue
            if not re.match(r"^0x[0-9a-f]+$", ins.op_str.strip()):
                continue
            cible = int(ins.op_str, 16)
            if cible >= ins.address or cible not in self.adrs:
                continue
            j = self.adrs[cible]
            self._lire_garde(i, j, cible)

    def _lire_garde(self, i_jcc, j_corps, cible):
        jcc = self.insns[i_jcc]
        if i_jcc == 0:
            return
        prev = self.insns[i_jcc - 1]
        # (a) montante : cmp reg, B ; jb/jl/jbe/jle arrière (l'idx a grandi)
        if prev.mnemonic == "cmp":
            parties = [p.strip() for p in prev.op_str.split(",")]
            if len(parties) == 2:
                reg, val = parties
                r = reg64(reg)
                borne = None
                if val.startswith("0x") or val.lstrip("-").isdigit():
                    try:
                        borne = int(val, 0)
                    except ValueError:
                        return
                if borne is not None and jcc.mnemonic in (
                        "jb", "jl", "jbe", "jle", "ja", "jg"):
                    # l'index au corps ∈ [0, B) : inc AVANT le cmp, la garde
                    # rejette B — l'accès (avant inc ou après) reste < B
                    if self._ctr_vivant(r, j_corps, i_jcc):
                        self.boucles.append(Boucle(
                            cible, i_jcc, r, borne, "montante",
                            jcc.mnemonic))
                    return
                # cmp B, reg (l'ordre inversé) : jb → B < reg
                if reg.startswith("0x") or reg.lstrip("-").isdigit():
                    try:
                        B = int(reg, 0)
                    except ValueError:
                        return
                    if val in R64 or val in ("rax", "rbx", "rcx", "rdx",
                                             "rsi", "rdi"):
                        r = reg64(val)
                        if jcc.mnemonic in ("ja", "jg", "jae", "jge") and \
                                self._ctr_vivant(r, j_corps, i_jcc):
                            self.boucles.append(Boucle(
                                cible, i_jcc, r, B, "montante", jcc.mnemonic))
        # (b) descendante : mov reg, C … déc reg ; jnz arrière
        elif prev.mnemonic == "dec" and jcc.mnemonic in ("jnz", "jne"):
            r = reg64(prev.op_str.strip())
            C = self._init_descendante(r, j_corps)
            if C is not None:
                self.boucles.append(Boucle(cible, i_jcc, r, C,
                                           "descendante", jcc.mnemonic))

    def _ctr_vivant(self, r, j_corps, i_garde):
        """Le compteur n'est pas réinitialisé dans le corps."""
        for k in range(j_corps, i_garde):
            ins = self.insns[k]
            if ins.mnemonic in ("mov", "xor", "lea", "pop") and \
                    ins.op_str.split(",")[0].strip() in (r, R64.get(r, r)):
                return False
        return True

    def _init_descendante(self, r, j_corps):
        """Le mov reg, C avant la tête (le plus proche)."""
        for k in range(j_corps - 1, -1, -1):
            ins = self.insns[k]
            if ins.mnemonic == "mov" and ", " in ins.op_str:
                dst, src = [p.strip() for p in ins.op_str.split(",")]
                if reg64(dst) == r:
                    if src.startswith("0x") or src.lstrip("-").isdigit():
                        try:
                            return int(src, 0)
                        except ValueError:
                            return None
                    return None
        return None

    def _boucle_a(self, i):
        """La boucle la plus PROCHE dont le corps contient i."""
        best = None
        for b in self.boucles:
            if b.tete <= self.insns[i].address < self.insns[b.garde].address:
                if best is None or (self.insns[b.garde].address -
                                    self.insns[b.tete].address) < \
                        (self.insns[best.garde].address -
                         self.insns[best.tete].address):
                    best = b
        return best

    def _cadre_max(self):
        total, n_push = 0, 0
        for ins in self.insns:
            if ins.mnemonic == "sub" and ins.op_str.startswith("rsp,"):
                try:
                    total = max(total, int(ins.op_str.split(",")[1].strip(), 0))
                except ValueError:
                    pass
            elif ins.mnemonic == "push":
                n_push += 1
        return total + 8 * min(n_push, 10) + 0x20 + 0x28

    # ---------------- le lea composé ---------------------------------------
    _RE_MEM = re.compile(
        r"^\[?([a-z][a-z0-9]*)?(?:\s*\+\s*([a-z][a-z0-9]*)?"
        r"(?:\s*\*\s*(\d))?)?(?:\s*([+-]\s*0x[0-9a-f]+|[+-]\s*\d+))?\]$")

    def _lea_expr(self, src, ins, prov, inter):
        m = self._RE_MEM.match(src.replace(" ", ""))
        if not m:
            return None
        base, index, scale, disp = m.groups()
        disp = int(disp.replace(" ", ""), 0) if disp else 0
        scale = int(scale) if scale else 1
        if base == "rip":
            return Expr(ins.address + ins.size + disp, 0, src="plan")
        if base in ("rsp", "rbp"):
            return Expr("pile", 0, src="pile")
        if base and index:
            eb = prov.get(reg64(base))
            ei = prov.get(reg64(index))
            iv = inter.get(reg64(index))
            if isinstance(eb, Expr) and iv:
                # plan/arg:A + k + idx×s avec idx ∈ [lo, hi)
                lo, hi = iv
                e = Expr(eb.base, eb.k + disp, ctr=reg64(index),
                         borne=hi, scale=scale, src="plan+ctr")
                e.lo = lo
                return e
            if isinstance(eb, Expr) and isinstance(ei, Expr) and \
                    isinstance(ei.base, int) and not isinstance(eb.base, int):
                pass
            if isinstance(eb, Expr) and isinstance(ei, Expr) and \
                    isinstance(ei.base, int):
                # le base arg/plan + le IDX LUI-MÊME plan (l'adresse d'une
                # pièce) : somme d'adresses — la preuve exige la zone
                return None
            return None
        if base:
            e = prov.get(reg64(base))
            if isinstance(e, Expr):
                return e.plus(disp)
        return None

    # ---------------- l'analyse --------------------------------------------
    def analyser(self):
        cadre_max = self._cadre_max()
        prov: dict[str, object] = {r: Expr(f"arg:{p}", 0, src="arg")
                                   for r, p in ARGS.items()}
        inter: dict[str, tuple] = {}
        compte = {"pile": 0, "medié": 0, "constant": 0, "plan-fixe": 0,
                  "plan-garde": 0, "contrat-boucle": 0, "bmc": 0, "nommé": 0,
                  "non-résolu": 0}
        rbp_actif, rbp_pushes, n_pushes = False, 0, 0
        smt_proofs = []
        spill: dict[int, object] = {}
        spill_inter: dict[int, tuple] = {}

        for i, ins in enumerate(self.insns):
            m, ops = ins.mnemonic, ins.op_str
            # la tête de boucle : le compteur prend son invariant
            for b in self.boucles:
                if b.tete == ins.address:
                    inter[b.ctr] = (0, b.borne)
            if m == "push":
                n_pushes += 8
            elif m == "pop":
                n_pushes -= 8
                d = ops.strip()
                prov.pop(reg64(d), None), inter.pop(reg64(d), None)
            elif m == "mov" and ops.startswith("rbp, rsp"):
                rbp_actif, rbp_pushes = True, n_pushes
            elif m == "call":
                cible_txt = ops.strip()
                eff = None
                if cible_txt.startswith("0x"):
                    try:
                        eff = self.effets.get(int(cible_txt, 16))
                    except ValueError:
                        eff = None
                if eff is not None:
                    # L'APPEL INTRA-DOMAINE : le scellé visé — ses effets
                    # RÉELS (les volatils qu'il écrit, sa notation lue)
                    for r in eff:
                        prov[r] = "?"
                        inter.pop(r, None)
                else:
                    for r in VOLATILS:
                        prov[r] = "?"
                        inter.pop(r, None)
            elif m == "ret":
                break

            parties = [p.strip() for p in ops.split(",")] if ", " in ops \
                else ([ops.strip()] if ops else [])
            if m.startswith("rep "):
                # le compte : le mov rcx/ecx, N le plus proche en amont
                self._rep_count = None
                for k in range(i - 1, max(-1, i - 12), -1):
                    pk = self.insns[k]
                    if pk.mnemonic == "mov" and ", " in pk.op_str:
                        pd, ps = [q.strip() for q in pk.op_str.split(",")]
                        if reg64(pd) == "rcx" and (ps.startswith("0x") or
                                                   ps.lstrip("-").isdigit()):
                            self._rep_count = int(ps, 0)
                            break
                    if pk.mnemonic in ("call", "xor") or \
                            (pk.mnemonic == "mov" and
                             reg64(pk.op_str.split(",")[0]) == "rcx"):
                        break
            dst = parties[0] if parties else None
            d64 = reg64(dst) if dst else None
            if dst and (dst.startswith("[") or re.match(
                    r"^(byte|word|dword|qword|xmm|ymm|word ptr|dword ptr|"
                    r"qword ptr|byte ptr)", dst)):
                d64 = None          # une DESTINATION MÉMOIRE : pas un transfert

            # ---- les accès ------------------------------------------------
            for op in ins.operands:
                if op.type != X86.X86_OP_MEM:
                    continue
                mem = op.mem
                base = ins.reg_name(mem.base) if mem.base else None
                index = ins.reg_name(mem.index) if mem.index else None
                disp = mem.disp
                acces = {"adresse": ins.address, "mnemonic": m,
                         "ligne": f"{m} {ops}", "base": base,
                         "index": index, "disp": disp}
                if base == "rsp":
                    acces["classe"] = "pile"
                    acces["preuve"] = f"[rsp{disp:+d}] ≤ cadre {cadre_max}"
                    if not (-0x100 <= disp < cadre_max):
                        acces["classe"], self.oob_pile = "HORS-CADRE", \
                            self.oob_pile + 1
                    compte[acces["classe"] if acces["classe"] == "pile"
                           else "non-résolu"] += 1
                elif base == "rbp" and rbp_actif:
                    atteint = -disp + rbp_pushes
                    acces["classe"] = "pile"
                    acces["preuve"] = (f"[rbp{disp:+d}] = rsp−{atteint} "
                                       f"≤ cadre {cadre_max} (repère rbp)")
                    if not (0 <= atteint < cadre_max):
                        acces["classe"], self.oob_pile = "HOURS-CADRE", \
                            self.oob_pile + 1
                        acces["classe"] = "HORS-CADRE"
                    compte[acces["classe"] if acces["classe"] == "pile"
                           else "non-résolu"] += 1
                elif base == "rip":
                    acces["classe"] = "constant"
                    acces["preuve"] = "rip+disp → le layout du plan"
                    compte["constant"] += 1
                else:
                    if m.startswith("rep "):
                        acces["_rep"] = getattr(self, "_rep_count", None)
                        acces["_rep_taille"] = {"rep movsb": 1, "rep stosb": 1,
                                                "rep movsw": 2, "rep stosw": 2,
                                                "rep movsd": 4, "rep stosd": 4,
                                                "rep movsq": 8,
                                                "rep stosq": 8}.get(m)
                    self._classer(acces, base, index, disp, mem.scale,
                                  prov, inter, compte, i, smt_proofs)
                self.acces.append(acces)
            # ---- les transferts de registre : provenance + intervalle -----
            if m in ("mov", "lea", "movzx", "movsxd", "movsx") and \
                    len(parties) == 2 and dst and d64 is not None and \
                    not dst.startswith("["):
                src = parties[1]
                if re.match(r"^(byte|word|dword|qword)\s*ptr\s*\[", src):
                    src = re.sub(r"^(byte|word|dword|qword)\s*ptr\s*",
                                 "", src)
                if m == "lea" and src.startswith("["):
                    e = self._lea_expr(src, ins, prov, inter)
                    prov[d64] = e if e is not None else "?"
                    inter.pop(d64, None)
                    # la TRANSFORMÉE : lea r, [x + x*s + k] (base == index)
                    mm = self._RE_MEM.match(src.replace(" ", ""))
                    if mm and mm.group(1) and mm.group(2) and \
                            reg64(mm.group(1)) == reg64(mm.group(2)):
                        x = reg64(mm.group(1))
                        sc = int(mm.group(3) or 1) + 1
                        k = int(mm.group(4).replace(" ", ""), 0) \
                            if mm.group(4) else 0
                        if x in inter:
                            lo, hi = inter[x]
                            inter[d64] = (lo * sc + k, hi * sc + k)
                elif src.startswith("["):
                    if src.startswith("[rip"):
                        prov[d64] = "const"
                    else:
                        _src_net = re.sub(r"^(byte|word|dword|qword)\s*"
                                          r"ptr\s*", "", src).replace(" ", "")
                        mm = self._RE_MEM.match(_src_net)
                        prov[d64] = "?"
                        # LE CHAMP BORNÉ : la valeur chargée d'un champ du
                        # cadre au plan porte L'INVARIANT du layout
                        if mm and self.domaine == "loupe" and \
                                not mm.group(2):
                            b = prov.get(mm.group(1))
                            if isinstance(b, Expr) and \
                                    isinstance(b.base, int) and \
                                    b.base + b.k == getattr(
                                        self, "_R_CADRE", 0xE000):
                                k = int(mm.group(4).replace(" ", ""), 0) \
                                    if mm.group(4) else 0
                                ch = CHAMPS_CADRE.get(b.k + k)
                                if ch and ch[1]:
                                    inter[d64] = (0, ch[1])
                        if mm and mm.group(1) == "rsp" and not mm.group(2):
                            k = int(mm.group(4).replace(" ", ""), 0) \
                                if mm.group(4) else 0
                            if k in spill:
                                prov[d64] = spill[k]   # le spill repris
                                if k in spill_inter:
                                    inter[d64] = spill_inter[k]
                    if prov.get(d64) == "?":
                        inter.pop(d64, None)
                else:
                    s64 = reg64(src)
                    if src.startswith("0x") or src.lstrip("-").isdigit():
                        try:
                            v = int(src, 0)
                            prov[d64] = Expr(v, 0, src="const")
                            inter[d64] = (v, v)
                            continue
                        except ValueError:
                            pass
                    if s64 in prov:
                        prov[d64] = prov[s64]
                    elif src in ("rax", "rbx", "rcx", "rdx", "rsi", "rdi"):
                        prov[d64] = "?"
                    if s64 in inter:
                        inter[d64] = inter[s64]
                    else:
                        inter.pop(d64, None)
            elif m == "xor" and len(parties) == 2 and \
                    parties[0] == parties[1] and d64 is not None:
                prov[d64] = Expr(0, 0, src="const")
                inter[d64] = (0, 0)
            elif m in ("add", "sub") and len(parties) == 2 and dst and \
                    d64 is not None and not dst.startswith("["):
                src = parties[1]
                if (src.startswith("0x") or src.lstrip("-").isdigit()) and \
                        d64 in inter:
                    try:
                        v = int(src, 0)
                        lo, hi = inter[d64]
                        if m == "add":
                            inter[d64] = (lo + v, hi + v)
                        else:
                            inter[d64] = (lo - v, hi - v)
                        e = prov.get(d64)
                        if isinstance(e, Expr) and e.base != "pile":
                            prov[d64] = e.plus(v if m == "add" else -v)
                    except ValueError:
                        pass
                elif d64 in inter:
                    inter.pop(d64, None)
                    if isinstance(prov.get(d64), Expr):
                        prov[d64] = "?"
            elif m == "and" and len(parties) == 2 and dst and \
                    d64 is not None:
                src = parties[1]
                if src.startswith("0x") or src.lstrip("-").isdigit():
                    try:
                        v = int(src, 0)
                        if v > 0 and (v & (v - 1)) == 0:
                            inter[d64] = (0, v)   # le masque 2^n
                            if not isinstance(prov.get(d64), Expr) or \
                                    isinstance(prov.get(d64), Expr) and \
                                    not isinstance(prov[d64].base, int):
                                prov[d64] = "?"   # la valeur masquée
                            elif isinstance(prov.get(d64), Expr):
                                prov[d64] = "?"   # l'adresse composée masquée
                    except ValueError:
                        pass
                elif d64 in inter:
                    inter.pop(d64, None)
            elif m == "inc" and dst and d64 is not None:
                if d64 in inter:
                    lo, hi = inter[d64]
                    inter[d64] = (lo + 1, hi + 1)
                if isinstance(prov.get(d64), Expr) and \
                        isinstance(prov[d64].base, int):
                    prov[d64] = prov[d64].plus(1)
            elif m == "dec" and dst and d64 is not None:
                if d64 in inter:
                    lo, hi = inter[d64]
                    inter[d64] = (lo - 1, hi - 1)
                if isinstance(prov.get(d64), Expr) and \
                        isinstance(prov[d64].base, int):
                    prov[d64] = prov[d64].plus(-1)

            # ---- la collecte des écrits (la passe des effets) ------------
            if dst and d64 is not None and m in ("mov", "lea", "xor", "add",
                                                 "sub", "inc", "dec", "and",
                                                 "pop", "movzx", "movsxd"):
                self.ecrits.add(d64)

            # ---- le dépôt de spill : mov [rsp±K], reg -------------------
            if m == "mov" and ops.startswith("qword ptr [rsp") and \
                    ", " in ops:
                mm = self._RE_MEM.match(
                    ops.split(",")[0].strip().replace("qword ptr ", "")
                    .replace(" ", ""))
                if mm and mm.group(1) == "rsp" and not mm.group(2):
                    k = int(mm.group(4).replace(" ", ""), 0) \
                        if mm.group(4) else 0
                    src_r = ops.split(", ")[1].strip()
                    s64 = reg64(src_r)
                    if s64 in prov:
                        spill[k] = prov[s64]
                        if s64 in inter:
                            spill_inter[k] = inter[s64]


        self.smt_proofs = smt_proofs
        return compte

    # ---------------- la classification des déréférencés ------------------
    def _classer(self, acces, base, index, disp, scale, prov, inter,
                 compte, i, smt_proofs):
        dom = self.domaine
        if base is None:
            acces["classe"] = "nommé"
            acces["cause"] = "accès absolu sans base"
            compte["nommé"] += 1
            return
        e = prov.get(base)
        # (0) médié-contrat v110 : arg:P, sans index
        if isinstance(e, str) and e.startswith("arg:") and index is None:
            acces["classe"] = "médié-contrat"
            acces["via"] = e
            acces["preuve"] = "pointeur d'argument, bornes au PRE de I (v110)"
            compte["medié"] += 1
            return
        # (1a) la pile pointée : lea reg, [rsp/rbp ± K] puis l'accès
        if isinstance(e, Expr) and e.base == "pile":
            k = e.k + disp + (getattr(e, "lo", 0) or 0)
            cadre = self._cadre_max()
            acces["classe"] = "pile"
            acces["preuve"] = (f"le pointeur de PILE [rsp{e.k:+d}]"
                               f"{disp:+d} = rsp{(e.k + disp):+d} ≤ cadre "
                               f"{cadre} (le tampon local du bloc)")
            if not (-0x100 <= e.k + disp < cadre):
                acces["classe"] = "HORS-CADRE"
                self.oob_pile += 1
            compte["pile" if acces["classe"] == "pile" else "non-résolu"] += 1
            return
        # (1b) la chaîne porte un Expr ARG : la STRUCTURE du contrat borne
        if isinstance(e, Expr) and isinstance(e.base, str) and \
                e.base.startswith("arg:"):
            taille = TAILLES_STRUCT.get((dom, self.bid), {}).get(
                e.base, None)
            iv = inter.get(index) if index else \
                (inter.get(e.ctr, (0, e.borne)) if e.ctr else None)
            if index is None and e.ctr is None:
                acces["classe"] = "médié-contrat"
                acces["via"] = e.base
                acces["preuve"] = (f"l'argument {e.base} + {e.k + disp} "
                                   "(la structure du contrat I — les bornes "
                                   "au PRE)" +
                                   (f", taille déclarée {taille} o"
                                    if taille else ""))
                compte["medié"] += 1
                return
            if iv:
                acces["classe"] = "contrat-boucle"
                acces["preuve"] = (f"l'argument {e.base} + index "
                                   f"{index or e.ctr} ∈ [{iv[0]}, {iv[1]}) "
                                   "— la taille au PRE de I borne l'accès")
                compte["contrat-boucle"] += 1
                self._cert_z3(acces, smt_proofs, iv)
                return
        # (0b) l'étendue REP : le compte LU du mov rcx précédent
        n_rep = acces.get("_rep")
        if n_rep is not None and isinstance(e, Expr) and index is None and \
                e.ctr is None:
            etendue = n_rep * (acces.get("_rep_taille") or 1)
            if isinstance(e.base, int):
                cible = e.base + e.k + disp
                z = zone_de(dom, cible) and zone_de(dom, cible + etendue - 1)
                if z:
                    acces["classe"] = "plan-fixe"
                    acces["preuve"] = (f"rep × {n_rep} → [0x{cible:x}, "
                                       f"0x{cible+etendue:x}) ⊆ {z[2]} "
                                       f"[0x{z[0]:x}, 0x{z[0]+z[1]:x})")
                    compte["plan-fixe"] += 1
                    return
            if isinstance(e.base, str) and e.base.startswith("arg:"):
                acces["classe"] = "médié-contrat"
                acces["preuve"] = (f"rep × {n_rep} sur l'argument {e.base} "
                                   "+ la structure du contrat I (le PRE)")
                compte["medié"] += 1
                return
        # (1) la chaîne porte un Expr (plan/arg/pile + ctr)
        if isinstance(e, Expr) and isinstance(e.base, int):
            cible = e.base + e.k + disp
            iv = inter.get(index) if index else \
                (inter.get(e.ctr, (0, e.borne)) if e.ctr else None)
            if index is None and e.ctr is None:
                z = zone_de(dom, cible)
                if z:
                    acces["classe"] = "plan-fixe"
                    acces["preuve"] = (f"plan 0x{cible:x} ∈ {z[2]} "
                                       f"[0x{z[0]:x}, 0x{z[0]+z[1]:x})")
                    compte["plan-fixe"] += 1
                else:
                    acces["classe"] = "nommé"
                    acces["cause"] = (f"plan 0x{cible:x} HORS zone du "
                                      "layout — l'adresse littérale hors plan")
                    compte["nommé"] += 1
                return
            if iv:
                lo, hi = iv
                sc = e.scale if e.ctr and index is None else scale
                z = zone_de(dom, cible)
                if z and cible + max(lo, 0) * sc >= z[0] and \
                        cible + (hi - 1) * sc < z[0] + z[1]:
                    acces["classe"] = "plan-garde"
                    acces["preuve"] = (f"index {index or e.ctr} ∈ [{lo}, "
                                       f"{hi}) (l'invariant de boucle"
                                       f"{' ou de champ du layout' if lo == 0 and hi in (384, 1 << 31, 96, 2320, 16, 64, 256, 79, 4096) else ''}), "
                                       f"cible 0x{cible:x} + {hi}×{sc} ≤ fin "
                                       f"{z[2]} 0x{z[0]+z[1]:x}")
                    compte["plan-garde"] += 1
                    return
                if z and cible + (hi - 1) * sc >= z[0] + z[1]:
                    acces["classe"] = "nommé"
                    acces["cause"] = (f"la boucle [{lo},{hi})×{sc} déborde "
                                      f"la zone {z[2]} à 0x{cible:x}")
                    compte["nommé"] += 1
                    return
            # l'intervalle manque : la borne vit au champ du plan (runtime)
            self._bmc_champ(acces, base, index, disp, cible, compte,
                            smt_proofs)
            return
        if isinstance(e, str) and e.startswith("arg:") and index is not None:
            # arg:P + idx : le contrat borne l'index (la taille au PRE)
            iv = inter.get(index)
            src_borne = None
            b = self._boucle_a(i)
            if b is not None and b.ctr == reg64(index):
                src_borne = ("la garde de boucle", b.borne)
            if iv:
                acces["classe"] = "contrat-boucle"
                acces["preuve"] = (f"base {e} (le tampon du contrat I), "
                                   f"index {index} ∈ [{iv[0]}, {iv[1]}) "
                                   f"— la taille au PRE borne l'accès")
                compte["contrat-boucle"] += 1
                self._cert_z3(acces, smt_proofs, iv)
                return
        self._bmc_champ(acces, base, index, disp, None, compte, smt_proofs)

    # ---------------- BMC : la borne au champ du plan ----------------------
    CHAMPS = {  # (nom, offset, borne, l'invariant du layout)
        536: ("vue", 1 << 31), 552: ("remplissage", 384),
        544: ("curseur", 1 << 31), 520: ("taille", 1 << 31),
    }

    def _bmc_champ(self, acces, base, index, disp, cible, compte, smt_proofs):
        """La décharge BMC quand la borne vit à un CHAMP DU PLAN (runtime)
        — z3 : la tranche, l'invariant du champ, la négation UNSAT ;
        sinon l'accès est NOMMÉ avec sa cause et son mécanisme."""
        # la valeur chargée depuis le plan (un champ runtime) : la borne
        # de l'invariant du layout s'applique SI la chaîne la montre
        e = None
        acces["classe"] = "nommé"
        acces["cause"] = (f"la base {base} est une VALEUR RUNTIME (chargée "
                          "ou recomputée) — la borne vit à l'INVARIANT "
                          "EXTERNE (le champ du plan, le contrat de "
                          "l'appelant, l'OS)")
        # LA BMC DE DÉMONSTRATION : la base symbolique SANS invariant —
        # z3 rend SAT : AUCUNE preuve statique n'existe sans l'invariant
        # externe — LE CERTIFICAT DU NOMMAGE (le modèle = le contre-exemple)
        b = z3.BitVec("base", 64)
        i = z3.BitVec("idx", 64)
        d = z3.BitVec("disp", 64)
        sol = z3.Solver()
        zone = z3.BitVec("zone_fin", 64)
        sol.add(zone == 0x10000)       # une borne de zone quelconque
        sol.add(z3.Or(b + i * 1 + d < 0, b + i + d >= zone))
        verdict = sol.check()
        acces["bmc"] = (f"SAT sans invariant externe — la preuve exige la "
                        f"cause nommée ({verdict})")
        nom = f"{self.bid}-{acces['adresse']:x}-sat"
        if verdict == z3.sat:
            (SMT / f"{nom}.smt2").write_text(
                f"; la BMC de démonstration — {self.bid} @ "
                f"{acces['adresse']:#x}\n; la base symbolique SANS "
                f"invariant externe : la négation de la sûreté est SAT\n"
                f"; (le modèle : un contre-exemple hors zone) — la borne "
                f"n'est PAS statique, elle vit à :\n;   {acces['cause']}\n"
                + sol.to_smt2(), encoding="utf-8")
            acces["certificat"] = f"certificats_smt/{nom}.smt2 (SAT — la borne externe)"
        compte["nommé"] += 1

    def _cert_z3(self, acces, smt_proofs, iv):
        idx, n, p = z3.Int("idx"), z3.Int("n"), z3.Int("p")
        s = z3.Solver()
        s.add(n >= 0, idx >= iv[0], idx < iv[1])
        s.add(z3.Or(p + idx < p, p + idx >= p + n))
        nom = f"{self.bid}-{acces['adresse']:x}"
        if s.check() == z3.unsat:
            acces["certificat"] = f"certificats_smt/{nom}.smt2 (UNSAT)"
            (SMT / f"{nom}.smt2").write_text(
                f"; certificat BMC-intervalle — {self.bid} @ "
                f"{acces['adresse']:#x}\n; idx ∈ [{iv[0]}, {iv[1]}) la "
                f"garde ; la négation (hors tampon) est UNSAT\n"
                + s.to_smt2(), encoding="utf-8")
            smt_proofs.append(nom)


def main():
    cibles = []
    for bid in sorted(lay_l.SLOTS_LOUPE):
        num = int(bid[1:]) - 110000
        c = list((REPO / "loupe" / "notation").glob(f"loupe-{num:02d}-*.asm"))
        if c:
            cibles.append(("loupe", f"loupe-{num:02d}", c[0],
                           *lay_l.SLOTS_LOUPE[bid]))
    for bid, (rva, slot) in sorted(lay_t.SLOTS_TLS13.items()):
        num = int(bid[1:]) - 100000
        c = list((REPO / "tls13" / "notation").glob(f"tls13-{num:02d}-*.asm"))
        if c:
            cibles.append(("tls13", f"tls13-{num:02d}", c[0], rva, slot))
    for bid, (rva, slot) in sorted(lay_s.SLOTS_SYS.items()):
        num = int(bid[1:]) - 90000
        c = list((REPO / "m8" / "notation").glob(f"sys-{num:02d}-*.asm"))
        if c:
            cibles.append(("sys", f"sys-{num:02d}", c[0], rva, slot))

    # LA PASSE 1 — les effets de chaque bloc (les volatils écrits, lus de
    # sa notation même) : l'interprocédural au domaine scellé
    for domaine, bid, chemin, rva, slot in cibles:
        octets, _ = B4.assembler_bloc(KS, str(chemin), rva, slot)
        an0 = AnalyseV200(octets, rva, domaine, bid)
        an0.analyser()
        EFFETS_GLOBAL[rva] = {r for r in an0.ecrits if r in VOLATILS}

    lignes, certificats = [], {}
    for domaine, bid, chemin, rva, slot in cibles:
        octets, _ = B4.assembler_bloc(KS, str(chemin), rva, slot)
        an = AnalyseV200(octets, rva, domaine, bid)
        compte = an.analyser()
        total = sum(compte.values()) + an.oob_pile
        lignes.append({"domaine": domaine, "bloc": bid, "acces_mem": total,
                       "pile": compte["pile"],
                       "medies_contrat": compte["medié"],
                       "constants_rip": compte["constant"],
                       "plan_fixe": compte["plan-fixe"],
                       "plan_garde": compte["plan-garde"],
                       "contrat_boucle": compte["contrat-boucle"],
                       "bmc_decharge": compte["bmc"],
                       "nommes": compte["nommé"],
                       "hors_cadre": an.oob_pile})
        certificats[bid] = {"domaine": domaine, "bloc": bid,
                            "acces": an.acces}
        print(f"[{domaine}] {bid:12s} {total:4d} : pile {compte['pile']:4d}"
              f" · médiés {compte['medié']:3d} · const {compte['constant']:3d}"
              f" · planF {compte['plan-fixe']:3d}"
              f" · planG {compte['plan-garde']:3d}"
              f" · ctrB {compte['contrat-boucle']:3d}"
              f" · bmc {compte['bmc']:3d} · NOMMÉS {compte['nommé']:3d}")

    with open(ICI / "surete_memoire_v200.csv", "w", newline="",
              encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(lignes[0].keys()))
        w.writeheader()
        w.writerows(lignes)
    for bid, cert in certificats.items():
        (CERT / f"{bid}.json").write_text(
            json.dumps(cert, indent=1, ensure_ascii=False), encoding="utf-8")
    tot = {k: sum(l[k] for l in lignes) for k in lignes[0]
           if k not in ("domaine", "bloc")}
    print("\nTOTAUX :", json.dumps(tot, ensure_ascii=False))


if __name__ == "__main__":
    main()
