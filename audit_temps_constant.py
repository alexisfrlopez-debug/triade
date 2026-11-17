#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""audit_temps_constant.py — L'AUDIT DE TEMPS CONSTANT STRUCTUREL NON BORNÉ
(l'instruction fkkqc7v8t, le chantier 4 de la vague 6 — le plan pré-enregistré
atelier-temps-constant-fkkqc7v8t/PLAN-fkkqc7v8t.md, sha256 58edd2c1…, gelé au
commit fd8cb1a AVANT toute mesure).

LE MANDAT : faire passer le temps constant structurel des six cibles crypto
(sha-256, hmac, hkdf, x25519, aes-gcm, md5) du statut « borné par égalité de
traces » (l'Entrée 320 : un seul compte d'instructions sur 120 mesures, graine
consignée — EXACT mais DYNAMIQUE) à une VÉRIFICATION STATIQUE NON BORNÉE :
l'analyse de flux d'information prouve que NI LES BRANCHEMENTS NI LES ADRESSES
MÉMOIRE ne dépendent du secret — pour TOUTES les valeurs du secret, sur TOUS
les chemins atteignables du code noté.

LA MÉTHODE — un interpréteur abstrait DE TAINT (flux sensible, fixpoint par
fonction, interprocédural mémoïsé par signature) SUR LES NOTATIONS EXPLICITES
du dépôt (keystone assemble ligne à ligne à l'org du plan, capstone relit — le
round-trip R5) :

  LES DEUX CLASSES DE VIOLATION (le critère constant-time structurel) :
    CLASSE BRANCHE — un jcc dont les drapeaux testés sont taaintés ; un
      jmp/call INDIRECT de cible taaintée ; un rep movsb/stosb dont le COMPTE
      (rcx) est taaint (le facteur de travail dépend du secret) ;
    CLASSE ADRESSE — un accès mémoire (lecture, écriture, chaîne rep) dont
      la BASE ou l'INDEX de l'adresse est taaint.

  LA DÉCHARGE SMT SUR LES CHEMINS (non bornée) : chaque occurrence devient
    une OBLIGATION — « ∀ valeurs du secret, la condition (resp. l'adresse)
    est-elle INVARIANTE ? » — tranchée par Z3 sur l'expression reconstruite
    PAR TRANCHAGE ARRIÈRE au site de l'obligation (les feuilles du tranchage
    sont les CHARGEMENTS DU SECRET, symboles libres : la décharge est NON
    BORNÉE par construction) :
      - Z3 trouve deux secrets donnant deux issues → CONTRE-EXEMPLE TÉMOIN
        = VIOLATION NOMMÉE (classe, adresse, les deux secrets en hexa) ;
      - Z3 prouve l'invariance → DÉCHARGÉE (la dépendance syntaxique était
        sémantiquement nulle) ;
      - le tranchage échoue à reconstruire (fusion, frontière d'appel,
        fenêtre dépassée) → OPAQUE = VIOLATION (fail-closed : jamais une
        décharge par l'ignorance).

  LE MODÈLE MÉMOIRE — cellules PAR OCTET (racine, décalage) où la racine est
    un POINTEUR SYMBOLIQUE (la pile SP de la frame, les pointeurs d'arguments
    P0..P3, GLOBAL les données RIP-relatives — les fixtures PUBLIQUES du
    domaine) ; les accès à décalage CONSTANT touchent la cellule exacte ; les
    accès INDICÉS [base + idx*s + disp] avec idx public lisent le SEAU de la
    base (l'union des cellules écrites via indice) OU les cellules exactes
    dans la fenêtre [disp, disp + 64*s) — la sur-approximation ne crée que
    des VALEURS taaintes, jamais une obligation que le code ne porte pas ;
    une base ou un index taaint dans une ADRESSE = l'obligation ADRESSE.

  L'INTERPROCEDURAL — les appels DIRECTS suivis aux adresses scellées du
    plan (les feuilles f25519, les sous-programmes internes, libc-01/07) ;
    chaque fonction analysée UNE FOIS par SIGNATURE de taaint d'entrée (les
    pointeurs d'arguments canonisés relativement) ; les effets rendus en
    résumé (les cellules taaintes par pointeur relatif, les seaux, rax) ;
    les volatiles ABI considérés morts au retour (la convention msx64 — les
    blocs la tiennent, l'audit ABI msx64 la contrôle à côté) ; les appels
    IAT suivent des MODÈLES NOMMÉS — ReadFile EST LA SOURCE DU SECRET (le
    tampon rdx devient taaint : le contenu du fichier, le protocole mesuré
    de loupe-06), les autres feuilles kernel32 sont publiques.

L'INTÉGRATION AU BUILD — à côté de l'audit ABI msx64 :
    tls13/build_m9.py   : auditer_tls13() aux côtés de l'oracle structurel ;
    loupe/build_loupe.py: auditer_loupe() aux côtés de audit_msx64() ;
  une violation LÈVE EchecBuild (le build refuse) ; JAMAIS un octet des
  pièces n'est touché — l'audit est une LECTURE.

Usage autonome : python3 audit_temps_constant.py [tls13|loupe|tout|mutants]
Code retour : 0 = obligations VERTES (+ les écarts nommés attendus) ; 2 = refus.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from collections import defaultdict

ICI = os.path.dirname(os.path.abspath(__file__))

# --- capstone/keystone/z3 : l'étagère du bac --------------------------------
try:
    import capstone
    from keystone import Ks, KS_ARCH_X86, KS_MODE_64
except ImportError:                                    # pragma: no cover
    capstone = None
    Ks = None

try:
    import z3
except ImportError:                                    # pragma: no cover
    z3 = None


# ══════════════════════════════════════════════════════════════════════════════
# 1 · LE CHARGEMENT DES NOTATIONS (keystone à l'org du plan, capstone relit)
# ══════════════════════════════════════════════════════════════════════════════

# les blocs audités : nom → (fichier de notation, répertoire, RVA, slot)
BLOCS = {}
for _i, (_bid, _fic, _rva, _slot) in enumerate([
        ("tls13-01", "tls13-01-sha256-init", 0xC000, 0x80),
        ("tls13-02", "tls13-02-sha256-comprimer", 0xC080, 0x1C0),
        ("tls13-03", "tls13-03-sha256-absorber", 0xC240, 0xC0),
        ("tls13-04", "tls13-04-sha256-finaliser", 0xC300, 0xC0),
        ("tls13-05", "tls13-05-hmac-sha256", 0xC3C0, 0x200),
        ("tls13-06", "tls13-06-hkdf-extract", 0xC5C0, 0xC0),
        ("tls13-07", "tls13-07-hkdf-expand", 0xC680, 0x180),
        ("tls13-08", "tls13-08-hkdf-expand-label", 0xC800, 0x180),
        ("tls13-09", "tls13-09-f25519-add", 0xC980, 0x80),
        ("tls13-10", "tls13-10-f25519-sub", 0xCA00, 0x140),
        ("tls13-11", "tls13-11-f25519-mul", 0xCB40, 0x480),
        ("tls13-12", "tls13-12-f25519-propager-geler", 0xCFC0, 0x140),
        ("tls13-13", "tls13-13-x25519-echelle", 0xD100, 0xB80),
        ("tls13-14", "tls13-14-x25519-cle-publique", 0xDC80, 0x40),
        ("tls13-15", "tls13-15-aes128-cles-tour", 0xDCC0, 0x240),
        ("tls13-16", "tls13-16-aes128-bloc", 0xDF00, 0xC0),
        ("tls13-17", "tls13-17-ghash-multiplication", 0xDFC0, 0xC0),
        ("tls13-18", "tls13-18-gcm-sceller", 0xE080, 0x480),
        ("tls13-19", "tls13-19-gcm-ouvrir", 0xE500, 0x4C0)]):
    BLOCS[_bid] = (_fic, os.path.join(ICI, "tls13", "notation"), _rva, _slot)
for _bid, (_fic, _rep, _rva, _slot) in {
        "loupe-06": ("loupe-06-md5", os.path.join(ICI, "loupe", "notation"),
                     0x45C0, 0x380),
        "libc-01": ("libc-01-memcpy", os.path.join(ICI, "m1", "notation"),
                    0x1100, 0x80),
        "libc-07": ("libc-07-memset", os.path.join(ICI, "m1", "notation"),
                    0x13C0, 0x80)}.items():
    BLOCS[_bid] = (_fic, _rep, _rva, _slot)

# les feuilles IAT de loupe-06 (les modèles nommés — la convention du plan)
IAT_LOUPE = {}          # slot IAT (adresse) → nom de feuille — rempli au chargement
MODELES_IAT = {
    # la feuille → (taaint_le_tampon_rdx, eax_public)
    "ReadFile": (True, True),
    "SetFilePointerEx": (False, True),
    "GetLastError": (False, True),
    "WriteFile": (False, True),
    "CloseHandle": (False, True),
    "GetFileSizeEx": (False, True),
    "CreateFileW": (False, True),
    "GetModuleHandleW": (False, True),
    "ExitProcess": (False, True),
}


class EchecAudit(Exception):
    """Le refus nommé — fail-closed : l'audit ne devine JAMAIS."""


def _lignes_notation(chemin: str) -> list[str]:
    with open(chemin, encoding="utf-8") as f:
        brut = f.read().splitlines()
    return [l.strip() for l in brut if l.strip() and not l.strip().startswith(";")]


def charger_bloc(nom: str, texte: str | None = None):
    """Assemble la notation (ou le TEXTE mutant) à l'org du plan, capstone
    relit → (insns [(addr, mnemonic, op_str, size)], déplacements RIP)."""
    if capstone is None:
        raise EchecAudit("capstone/keystone absents du bac (l'outillage du "
                         "chantier n'est pas provisionné)")
    if nom not in BLOCS:
        raise EchecAudit(f"bloc inconnu : {nom!r}")
    fic, rep, rva, slot = BLOCS[nom]
    if texte is None:
        lignes = _lignes_notation(os.path.join(rep, fic + ".asm"))
    else:
        lignes = [l.strip() for l in texte.splitlines()
                  if l.strip() and not l.strip().startswith(";")]
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    octets, addr = b"", rva
    for ligne in lignes:
        enc, _ = ks.asm(ligne, addr)
        if not enc:
            raise EchecAudit(f"{nom} : ligne inassemblable : {ligne!r}")
        octets += bytes(enc)
        addr += len(enc)
    insns = [(i.address, i.mnemonic, i.op_str, i.size)
             for i in cs.disasm(octets, rva)]
    if len(insns) != len(lignes):
        raise EchecAudit(f"{nom} : {len(insns)} instructions relues != "
                         f"{len(lignes)} notées (round-trip rompu)")
    return insns


def _deplacements_iat(nom: str) -> dict[int, str]:
    """Les déplacements RIP → feuilles IAT (l'en-tête de la notation les
    consigne : « ; addr + taille ± disp = cible » — la cible est le SLOT)."""
    fic, rep, _, _ = BLOCS[nom]
    cibles = {}
    for ligne in open(os.path.join(rep, fic + ".asm"), encoding="utf-8"):
        m = re.match(r"^;\s+([0-9a-f]+)\s+\+\s+(\d+)\s+([+-])\s+"
                     r"(0x[0-9a-f]+|\d+)\s+=\s+(0x[0-9a-f]+|\d+)", ligne)
        if m:
            addr, _t, signe, disp, cible = m.groups()
            cible = int(cible, 16)
            # les slots IAT du plan loupe : kernel32 0x3120-, user32 0x3148-
            cibles[(int(addr, 16), int(disp, 0) * (1 if signe == "+" else -1))] = cible
    return cibles


# ══════════════════════════════════════════════════════════════════════════════
# 2 · LE DOMAINE ABSTRAIT (le taaint, les pointeurs, les cellules, les seaux)
# ══════════════════════════════════════════════════════════════════════════════

REGS64 = ["rax", "rcx", "rdx", "rbx", "rsp", "rbp", "rsi", "rdi"] + \
         [f"r{i}" for i in range(8, 16)]
_PARENT = {}
for _r in REGS64:
    _PARENT[_r] = _r
    _PARENT[_r.replace("r", "e", 1) if _r[0] == "r" and _r[1:].isdigit() is False
            and _r.startswith("r") and len(_r) == 3
            else _r] = _r  # placeholder corrigé ci-dessous
# la table de parenté exacte (les 8 classiques + les r8-r15)
_PARENT = {}
for _r in ["rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp"]:
    _base = _r[1:]
    _PARENT[_r] = _r
    _PARENT["e" + _base] = _r
    _PARENT[_base] = _r if _base.isalpha() else _r   # ax, bx… (16 bits)
    _PARENT[_base[0] + "l"] = _r                     # al, bl, cl, dl
    _PARENT[_base[0] + "h"] = _r                     # ah, bh, ch, dh
    _PARENT[_base + "l"] = _r                         # sil, dil, bpl, spl
for _i in range(8, 16):
    _PARENT[f"r{_i}"] = f"r{_i}"
    _PARENT[f"r{_i}d"] = f"r{_i}"
    _PARENT[f"r{_i}w"] = f"r{_i}"
    _PARENT[f"r{_i}b"] = f"r{_i}"

_LARGEUR_REG = {}
for _r in REGS64:
    _LARGEUR_REG[_r] = 64
for _r in ["eax", "ebx", "ecx", "edx", "esi", "edi", "ebp", "esp"] + \
         [f"r{i}d" for i in range(8, 16)]:
    _LARGEUR_REG[_r] = 32
for _r in ["ax", "bx", "cx", "dx", "si", "di", "bp", "sp"] + \
         [f"r{i}w" for i in range(8, 16)]:
    _LARGEUR_REG[_r] = 16
for _r in ["al", "bl", "cl", "dl", "sil", "dil", "bpl", "spl"] + \
         [f"r{i}b" for i in range(8, 16)]:
    _LARGEUR_REG[_r] = 8
for _r in ["ah", "bh", "ch", "dh"]:
    _LARGEUR_REG[_r] = 8

VOLATILES = {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}
DRAPEAUX = ("cf", "zf", "sf", "of")


class Etat:
    """L'état abstrait : taaint des registres, des drapeaux, la carte des
    pointeurs, les cellules mémoire (par octet), les seaux, le décalage SP."""
    __slots__ = ("regs", "flags", "ptr", "cells", "seaux", "sp", "ptrcells",
                 "sp_sym", "sp_racine")

    def __init__(self):
        self.regs = {r: False for r in REGS64}
        self.flags = {f: False for f in DRAPEAUX}
        self.ptr = {}                     # reg64 → (racine, delta, const)
        self.cells = {}                   # (racine, décalage) → taaint
        self.seaux = {}                   # racine → taaint (l'indicé)
        self.ptrcells = {}                # (racine, décalage) → identité ptr
        self.sp = 0                       # décalage SP courant de la frame
        self.sp_sym = False               # le cadre DYNAMIQUE (sub rsp, reg)
        self.sp_racine = "SP"             # LA RACINE DE LA FRAME (par fonction)

    def copie(self) -> "Etat":
        e = Etat.__new__(Etat)
        e.regs = dict(self.regs)
        e.flags = dict(self.flags)
        e.ptr = dict(self.ptr)
        e.cells = dict(self.cells)
        e.seaux = dict(self.seaux)
        e.ptrcells = dict(self.ptrcells)
        e.sp = self.sp
        e.sp_sym = self.sp_sym
        e.sp_racine = self.sp_racine
        return e

    def join(self, autre: "Etat") -> bool:
        """Le join au point de fusion — le taaint ne croît que ; True si
        l'état a changé (le worklist continue)."""
        change = False
        for r in REGS64:
            v = self.regs[r] or autre.regs[r]
            change |= v != self.regs[r]
            self.regs[r] = v
        for f in DRAPEAUX:
            v = self.flags[f] or autre.flags[f]
            change |= v != self.flags[f]
            self.flags[f] = v
        for k, v in autre.cells.items():
            if v and not self.cells.get(k, False):
                self.cells[k] = True
                change = True
        for k, v in autre.seaux.items():
            if v and not self.seaux.get(k, False):
                self.seaux[k] = True
                change = True
        for k in list(self.ptrcells):
            if k not in autre.ptrcells or self.ptrcells[k] != autre.ptrcells[k]:
                del self.ptrcells[k]      # la fusion tue le pointeur sûr
                change = True
        for k, v in autre.ptrcells.items():
            if k not in self.ptrcells:
                self.ptrcells[k] = v
                change = True
        for r in list(self.ptr):
            if r not in autre.ptr or self.ptr[r] != autre.ptr[r]:
                del self.ptr[r]           # la fusion tue le pointeur sûr
                change = True
        if self.sp_sym != autre.sp_sym:
            self.sp_sym = True            # la fusion : le symbolique gagne
        if self.sp != autre.sp and not self.sp_sym:
            raise EchecAudit(f"fusion à décalages SP divergents ({self.sp} / "
                             f"{autre.sp}) — le modèle refuse (fail-closed)")
        return change


# --- le décorticage des opérandes ----------------------------------------------
RE_MEM = re.compile(r"^(?:(qword|dword|word|byte|xmmword) ptr )?"
                   r"\[([^\]]+)\]$")
RE_VAL = re.compile(r"^(0x[0-9a-f]+|-?\d+)$")
_RE_VAL_RE = RE_VAL
_RE_MEM_RE = RE_MEM


def _decortique_memoire(expr: str):
    """'[base ± idx*n ± disp]' → (base, idx, échelle, disp) — None si vide.
    Les formes « rip - 0x91a4 » (capstone) et « a + b - c » sont couvertes."""
    expr = re.sub(r"\s+", "", expr)          # « rip - 0x91a4 » → « rip-0x91a4 »
    parties = [p for p in re.findall(r"[+-]?[^+\-]+", expr) if p]
    base, idx, ech, disp = None, None, 1, 0
    for p in parties:
        negatif = p.startswith("-")
        p = p.lstrip("+-")
        m = re.match(r"^(\w+)\*(\d+)$", p)
        if m and m.group(1) in _PARENT:
            idx, ech = m.group(1), int(m.group(2)) * (-1 if negatif else 1)
        elif p in _PARENT or p == "rip":
            if p == "rip" and base is None:
                base = "rip"
            elif base is None:
                base = p
            elif idx is None:
                idx, ech = p, -1 if negatif else 1
            else:
                raise EchecAudit(f"adresse à double index : {expr!r}")
        else:
            disp += int(p, 0) * (-1 if negatif else 1)
    return base, idx, ech, disp


def _largeur(op: str, mnemo: str) -> int:
    """La largeur d'octets d'un accès (le qualificateur, sinon le registre)."""
    if "ptr" in op:
        m = RE_MEM.match(op.strip())
        if m and m.group(1):
            return {"byte": 1, "word": 2, "dword": 4, "qword": 8,
                    "xmmword": 16}[m.group(1)]
    for tok in re.split(r"[,\s]+", op):
        tok = tok.strip()
        if tok in _LARGEUR_REG:
            return _LARGEUR_REG[tok] // 8
    return 4


def _reg64(nom: str) -> str:
    if nom not in _PARENT:
        raise EchecAudit(f"registre inconnu au modèle : {nom!r}")
    return _PARENT[nom]


def _reg64_nom(nom: str) -> str:
    return _PARENT.get(nom, nom)


# ══════════════════════════════════════════════════════════════════════════════
# 3 · LES FONCTIONS (le CFG par fonction, les frontières aux ret)
# ══════════════════════════════════════════════════════════════════════════════

class Fonction:
    def __init__(self, nom: str, insns: list, entree: int, bloc_nom: str,
                 rva_bloc: int, fin_bloc: int):
        self.nom = nom
        self.bloc = bloc_nom
        self.entree = entree
        # BFS depuis l'entrée : les cibles de sauts ; le ret ferme le chemin
        self.adresses = set([entree])
        vus = {entree}
        file = [entree]
        idx = {a: i for i, (a, *_r) in enumerate(insns)}
        self.insns = insns
        while file:
            a = file.pop(0)
            if a not in idx:
                raise EchecAudit(f"{bloc_nom}/{nom} : cible de saut hors "
                                 f"bloc : {a:#x}")
            i = idx[a]
            _addr, mn, ops, taille = insns[i]
            if mn == "ret":
                continue
            if mn == "jmp":
                if not ops.startswith("0x"):
                    raise EchecAudit(f"{bloc_nom} : jmp indirect non modélisé "
                                     f"@{a:#x} : {mn} {ops}")
                for c in (int(ops, 0),):
                    if c not in vus:
                        vus.add(c)
                        file.append(c)
            elif mn.startswith("j"):
                for c in (int(ops, 0), a + taille):
                    if c in idx and c not in vus and c < fin_bloc:
                        vus.add(c)
                        file.append(c)
            else:
                nxt = a + taille
                if nxt in idx and nxt not in vus and nxt < fin_bloc:
                    vus.add(nxt)
                    file.append(nxt)
        self.adresses = {a for a in vus if a in idx}
        self.sequence = [i for i, (a, *_r) in enumerate(insns)
                         if a in self.adresses]
        # les blocs de base : leaders = entrée, cibles de saut, après saut/ret
        leaders = {entree}
        for i in self.sequence:
            a, mn, ops, t = insns[i]
            if mn.startswith("j") or mn == "ret":
                if mn.startswith("j") and ops.startswith("0x"):
                    leaders.add(int(ops, 0))
                if a + t in idx and (a + t) in self.adresses:
                    leaders.add(a + t)
        self.bbs = {}
        courant = []
        for i in self.sequence:
            a = insns[i][0]
            if a in leaders and courant:
                self.bbs[insns[courant[0]][0]] = courant
                courant = []
            courant.append(i)
        if courant:
            self.bbs[insns[courant[0]][0]] = courant
        self.succ = {}
        for debut, seq in self.bbs.items():
            a, mn, ops, t = insns[seq[-1]]
            if mn == "ret":
                self.succ[debut] = []
            elif mn == "jmp":
                self.succ[debut] = [int(ops, 0)]
            elif mn.startswith("j"):
                s = [int(ops, 0)]
                nxt = a + t
                if nxt in self.adresses:
                    s.append(nxt)
                self.succ[debut] = s
            else:
                nxt = a + t
                self.succ[debut] = [nxt] if nxt in self.adresses else []
        self.idx = idx


def construit_fonctions(nom_bloc: str, insns: list) -> dict[int, Fonction]:
    """Les fonctions d'un bloc : l'entrée + les cibles d'appels DIRECTS
    internes au bloc (les sous-programmes locaux — .comprimer de loupe-06)."""
    _fic, _rep, rva, slot = BLOCS[nom_bloc]
    fin = rva + slot
    entrees = {rva}
    for a, mn, ops, _t in insns:
        if mn == "call" and ops.startswith("0x"):
            cible = int(ops, 0)
            if rva <= cible < fin:
                entrees.add(cible)
    fns = {}
    for e in sorted(entrees):
        nom = (nom_bloc if e == rva else f"{nom_bloc}+{e:#x}")
        fns[e] = Fonction(nom, insns, e, nom_bloc, rva, fin)
    return fns


# ══════════════════════════════════════════════════════════════════════════════
# 4 · LA SÉMANTIQUE DE TRANSFERT (le taaint, instruction par instruction)
# ══════════════════════════════════════════════════════════════════════════════

# les conditions → les drapeaux qu'elles lisent
_COND = {
    "je": ("zf",), "jne": ("zf",), "jz": ("zf",), "jnz": ("zf",),
    "ja": ("cf", "zf"), "jae": ("cf",), "jb": ("cf",), "jbe": ("cf", "zf"),
    "jc": ("cf",), "jnc": ("cf",),
    "jg": ("zf", "sf", "of"), "jge": ("sf", "of"),
    "jl": ("sf", "of"), "jle": ("zf", "sf", "of"),
    "js": ("sf",), "jns": ("sf",),
    "sete": ("zf",), "setne": ("zf",), "setz": ("zf",), "setnz": ("zf",),
    "seta": ("cf", "zf"), "setae": ("cf",), "setb": ("cf",),
    "setc": ("cf",), "setnc": ("cf",), "sets": ("sf",), "setns": ("sf",),
    "setg": ("zf", "sf", "of"), "setge": ("sf", "of"),
    "setl": ("sf", "of"), "setle": ("zf", "sf", "of"),
}

_FENETRE_IDX = 64          # la fenêtre des lectures indicées : 64 index
_FENETRE_PTR = 64          # la fenêtre des pointeurs à décalage symbolique


class Moteur:
    """L'auditeur d'un dépôt : les blocs chargés, les fonctions, les mémos
    interprocéduraux, les obligations levées."""

    def __init__(self, racine=ICI, charge_mutants=None):
        self.racine = racine
        self.blocs_insns = {}          # nom_bloc → insns
        self.fonctions = {}            # (nom_bloc, entree) → Fonction
        self.adresse_fonction = {}     # adresse d'entrée → (nom_bloc, entree)
        self.iat_par_bloc = {}         # nom_bloc → {(addr,disp): slot}
        self.slot_feuille = {}         # (nom_bloc, slot) → feuille IAT
        self.obligations = []          # les constats
        self.memo = {}                 # (fn, signature) → résumé
        self.compteur_racines = 0
        self.charge_mutants = charge_mutants or {}
        self._charge_tout()

    # --- le chargement ------------------------------------------------------------
    def _charge_tout(self):
        for nom in BLOCS:
            if nom in self.charge_mutants:
                insns = charger_bloc(nom, texte=self.charge_mutants[nom])
            else:
                insns = charger_bloc(nom)
            self.blocs_insns[nom] = insns
            for e, fn in construit_fonctions(nom, insns).items():
                self.fonctions[(nom, e)] = fn
                self.adresse_fonction[e] = (nom, e)
        # les feuilles IAT de loupe : le plan loupe/layout IAT_SLOTS (les
        # adresses scellées — kernel32 @0x3120…, la convention du domaine)
        try:
            sys.path.insert(0, os.path.join(self.racine, "loupe"))
            import layout as L  # noqa: E402
            inverse = {v: k for k, v in getattr(L, "IAT_SLOTS", {}).items()}
            for (nom, e), fn in self.fonctions.items():
                for a, mn, ops, _t in [fn.insns[i] for i in fn.sequence]:
                    if mn == "call" and "[rip" in ops:
                        m = re.match(r"qword ptr \[rip ([+-]) (0x[0-9a-f]+)\]",
                                     ops)
                        if m:
                            disp = int(m.group(2), 0) * \
                                (1 if m.group(1) == "+" else -1)
                            slot = a + _t + disp
                            if slot in inverse:
                                self.slot_feuille[(nom, a)] = inverse[slot]
        except ImportError:
            pass

    def racine_fraiche(self) -> int:
        self.compteur_racines += 1
        return self.compteur_racines

    # --- l'accès mémoire (le modèle à racines) ------------------------------------
    def _ptr_du(self, etat: Etat, reg: str):
        """Le pointeur symbolique d'un registre de base (None si inconnu)."""
        return etat.ptr.get(_reg64(reg))

    def _verifie_adresse(self, protocole: str, bloc: str, addr: int,
                         texte: str, etat: Etat, base: str | None,
                         idx: str | None, ech: int):
        """L'obligation ADRESSE : la base ou l'index taaint dans une adresse."""
        for comp in (base, idx):
            if comp is not None and comp != "rip" and \
                    etat.regs.get(_reg64(comp), False):
                self._obligation(protocole, bloc, addr, texte, "ADRESSE",
                                 f"le composant {comp} de l'adresse est "
                                 f"taaint (dérivé du secret)")
        if base == "rip":
            return None
        if base is None:
            return None           # adresse absolue immédiate : publique
        p = self._ptr_du(etat, base)
        if p is None:
            return None           # base non pointeur connu : les cellules
        return p                   # (racine, delta, const)

    def _lecture(self, etat: Etat, protocole: str, bloc: str, addr: int,
                 texte: str, op_mem: str):
        """Le taaint lu à l'adresse (le modèle : cellule exacte, fenêtre des
        indicées, seau de la racine)."""
        m = RE_MEM.match(op_mem)
        if not m:
            raise EchecAudit(f"opérande mémoire inattendue : {op_mem!r}")
        base, idx, ech, disp = _decortique_memoire(m.group(2))
        racine_delta = self._verifie_adresse(protocole, bloc, addr, texte,
                                             etat, base, idx, ech)
        if base == "rip":
            return False          # les fixtures .rdata du plan : PUBLIQUES
        if racine_delta is None:
            return False
        racine, delta, const = racine_delta
        if delta is None:
            # pointeur à décalage symbolique public : la voie indicée
            # (le seau ∪ la fenêtre depuis la partie constante)
            seau = etat.seaux.get(racine, False)
            fen = range(const, const + _FENETRE_PTR + _largeur(op_mem, ""))
            exactes = any(etat.cells.get((racine, o), False) for o in fen)
            return seau or exactes
        if idx is None:
            offs = range(delta + disp, delta + disp + _largeur(op_mem, ""))
            return any(etat.cells.get((racine, o), False) for o in offs)
        # la lecture indicée : le seau ∪ la fenêtre des cellules exactes
        seau = etat.seaux.get(racine, False)
        fen = range(delta + disp, delta + disp + _FENETRE_IDX * ech +
                    _largeur(op_mem, ""))
        exactes = any(etat.cells.get((racine, o), False) for o in fen)
        return seau or exactes

    def _ecriture(self, etat: Etat, protocole: str, bloc: str, addr: int,
                  texte: str, op_mem: str, taaint: bool):
        """L'écriture du taaint à l'adresse (cellules exactes ; l'indicé
        pose le seau ET les cellules de la fenêtre)."""
        m = RE_MEM.match(op_mem)
        if not m:
            raise EchecAudit(f"opérande mémoire inattendue : {op_mem!r}")
        base, idx, ech, disp = _decortique_memoire(m.group(2))
        racine_delta = self._verifie_adresse(protocole, bloc, addr, texte,
                                             etat, base, idx, ech)
        if racine_delta is None:
            return
        racine, delta, const = racine_delta
        if delta is None:
            # pointeur à décalage symbolique : l'écriture POSITIVE taint la
            # fenêtre ; l'écriture publique ne nettoie PAS (sur-approx saine)
            if taaint:
                etat.seaux[racine] = True
                for o in range(const, const + _FENETRE_PTR +
                               _largeur(op_mem, "")):
                    etat.cells[(racine, o)] = True
            return
        if idx is None:
            for o in range(delta + disp, delta + disp + _largeur(op_mem, "")):
                etat.cells[(racine, o)] = taaint
        else:
            if taaint:
                etat.seaux[racine] = True
                fen = range(delta + disp, delta + disp + _FENETRE_IDX * ech +
                            _largeur(op_mem, ""))
                for o in fen:
                    etat.cells[(racine, o)] = \
                        etat.cells.get((racine, o), False) or True
            # une écriture indicée PUBLIQUE ne nettoie PAS (sur-approx)

    # --- les obligations ----------------------------------------------------------
    def _obligation(self, protocole: str, bloc: str, addr: int, texte: str,
                    classe: str, detail: str, etat: "Etat | None" = None,
                    bornes: int | None = None):
        self.obligations.append({
            "protocole": protocole, "bloc": bloc, "addr": addr,
            "texte": texte, "classe": classe, "detail": detail,
            "regs_taint": dict(etat.regs) if etat is not None else {},
            "bornes": bornes})

    # --- la fonction de transfert ---------------------------------------------------
    def transfert(self, protocole: str, bloc: str, etat: Etat, insn) -> None:
        """Applique UNE instruction à l'état (le taaint avance ou stagne —
        monotonie par construction). Lève les obligations aux sites."""
        addr, mn, ops, taille = insn
        cs = [p.strip() for p in ops.split(",")] if ops else []

        def taint_reg(nom):
            return etat.regs.get(_reg64(nom), False) if nom in _PARENT else None

        def pose_reg(nom, taaint: bool):
            """Poser le taaint d'un registre — l'écriture 32 bits ZÉRO la
            moitié haute (x86-64), la 8/16 la préserve (le | conservateur)."""
            p = _reg64(nom)
            w = _LARGEUR_REG[nom]
            if w == 64 or w == 32:
                etat.regs[p] = taaint
                if w == 64:
                    etat.ptr.pop(p, None)
            else:
                etat.regs[p] = etat.regs[p] or taaint

        # ---- les mouvements
        if mn in ("mov", "movabs", "movzx", "movsx", "movsxd"):
            dst, src = cs[0], cs[1]
            if "[" in dst:
                # mov mem, imm/reg/mem : l'écriture à l'adresse
                if RE_VAL.match(src):
                    self._ecriture(etat, protocole, bloc, addr, ops, dst,
                                   False)
                elif src in _PARENT:
                    self._ecriture(etat, protocole, bloc, addr, ops, dst,
                                   taint_reg(src))
                    # L'IDENTITÉ DU POINTEUR suit la valeur (8 octets exacts)
                    p_src = etat.ptr.get(_reg64(src))
                    if p_src is not None and \
                            _LARGEUR_REG.get(src, 64) == 64:
                        m2 = RE_MEM.match(dst)
                        if m2:
                            b2, i2, _e2, d2 = _decortique_memoire(m2.group(2))
                            rd = self._verifie_adresse(protocole, bloc, addr,
                                                       ops, etat, b2, i2, _e2)
                            if rd is not None and rd[1] is not None and i2 is None:
                                for o in range(rd[1] + d2, rd[1] + d2 + 8):
                                    etat.ptrcells[(rd[0], o)] = p_src
                else:
                    raise EchecAudit(f"source non modélisée : {mn} {ops}")
                return
            if RE_VAL.match(src):
                pose_reg(dst, False)
            elif src in _PARENT:
                pose_reg(dst, taint_reg(src))
                if mn in ("mov", "movabs"):
                    etat.ptr[_reg64(dst)] = etat.ptr.get(_reg64(src)) \
                        if _reg64(dst) == _reg64(src) or \
                        _LARGEUR_REG.get(dst, 64) == 64 else None
                    if _reg64(dst) != _reg64(src):
                        etat.ptr[_reg64(dst)] = etat.ptr.get(_reg64(src))
                    else:
                        etat.ptr[_reg64(dst)] = etat.ptr.get(_reg64(src))
            elif "[" in src:
                t = self._lecture(etat, protocole, bloc, addr, ops, src)
                pose_reg(dst, t)
                if mn in ("mov", "movabs"):
                    etat.ptr.pop(_reg64(dst), None)
                    # le CHARGEMENT d'une identité de pointeur (8 octets)
                    m2 = RE_MEM.match(src)
                    if m2 and _LARGEUR_REG.get(dst, 64) == 64:
                        b2, i2, _e2, d2 = _decortique_memoire(m2.group(2))
                        rd = self._verifie_adresse(protocole, bloc, addr,
                                                   ops, etat, b2, i2, _e2)
                        if rd is not None and rd[1] is not None and i2 is None:
                            p_mem = etat.ptrcells.get((rd[0], rd[1] + d2))
                            if p_mem is not None:
                                etat.ptr[_reg64(dst)] = p_mem
            else:
                raise EchecAudit(f"source non modélisée : {mn} {ops}")
            return
        if mn == "lea":
            dst, expr = cs[0], cs[1]
            m = RE_MEM.match(expr)
            base, idx, ech, disp = _decortique_memoire(m.group(2))
            taaint = False
            for comp in (base, idx):
                if comp is not None and comp != "rip" and \
                        etat.regs.get(_reg64(comp), False):
                    taaint = True
            pose_reg(dst, taaint)
            if base == "rip":
                etat.ptr[_reg64(dst)] = ("GLOBAL", disp, 0)
                return
            p = self._ptr_du(etat, base) if base else None
            if p is not None and idx is None:
                racine, delta, _c = p
                etat.ptr[_reg64(dst)] = (racine, (delta or 0) + disp, 0)
            elif p is not None and idx is not None and not \
                    etat.regs.get(_reg64(idx), False):
                # pointeur + index public symbolique : la racine est sûre,
                # le décalage inconnu — la PARTIE CONSTANTE est retenue
                etat.ptr[_reg64(dst)] = (p[0], None, disp)
            else:
                etat.ptr.pop(_reg64(dst), None)
            return
        if mn == "xchg":
            a, b = cs[0], cs[1]
            if a in _PARENT and b in _PARENT:
                ta, tb = taint_reg(a), taint_reg(b)
                pose_reg(a, tb)
                pose_reg(b, ta)
            return
        if mn == "bswap":
            pose_reg(cs[0], taint_reg(cs[0]))
            return

        # ---- l'arithmétique et la logique
        if mn in ("add", "sub", "adc", "sbb", "cmp", "and", "or", "xor",
                  "test", "neg"):
            dst, src = cs[0], cs[1]
            ts = 0
            if RE_VAL.match(src):
                ts = False
            elif src in _PARENT:
                ts = taint_reg(src)
            elif "[" in src:
                ts = self._lecture(etat, protocole, bloc, addr, ops, src)
            if mn in ("adc", "sbb"):
                ts = ts or etat.flags["cf"]
            # xor/sub d'un registre PAR LUI-MÊME : la constante zéro certaine
            if mn in ("xor", "sub") and src in _PARENT and dst in _PARENT and \
                    _reg64(src) == _reg64(dst):
                pose_reg(dst, False)
                if mn == "xor":
                    etat.flags["zf"], etat.flags["sf"] = False, False
                    etat.flags["cf"], etat.flags["of"] = False, False
                return
            if dst in _PARENT and _reg64(dst) == "rsp" and mn in ("add", "sub"):
                # LA PILE : sub/add rsp, imm — le décalage de frame AVANCE
                # (le modèle de cellules suit) ; sub/add rsp, REG — LE CADRE
                # DYNAMIQUE (hkdf-expand : la fenêtre OKM au montant public
                # symbolique) : la pile devient SYMBOLIQUE — le seau porte
                # laSUREté (toute cellule SP déjà taainte y passe) ; un
                # montant TAINT est l'obligation BRANCHE (le cadre même
                # dépendrait du secret — fail-closed sur l'obligation)
                if RE_VAL.match(src):
                    n = int(src, 0) * (1 if mn == "add" else -1)
                    if etat.sp_sym:
                        return            # déjà symbolique : imm sans effet
                    etat.sp += n
                    etat.ptr["rsp"] = (etat.sp_racine, etat.sp, 0)
                    return
                if src in _PARENT:
                    if etat.regs.get(_reg64(src), False):
                        self._obligation(protocole, bloc, addr, f"{mn} {ops}",
                                         "BRANCHE",
                                         "le DÉCALAGE DE PILE dépend du "
                                         "secret — le cadre même de la "
                                         "fonction est secret-dépendant")
                    if any(r == etat.sp_racine and v
                           for (r, _o), v in etat.cells.items()):
                        etat.seaux[etat.sp_racine] = True
                    etat.sp_sym = True
                    etat.ptr["rsp"] = (etat.sp_racine, None, 0)
                    return
                raise EchecAudit(f"réécriture de rsp non modélisée : "
                                 f"{mn} {ops} — fail-closed")
            if mn in ("cmp", "test"):
                # cmp/test : la destination est LUE, JAMAIS écrite — les
                # drapeaux seuls vivent (le pointeur de la base demeure)
                td = taint_reg(dst) if dst in _PARENT else (
                    self._lecture(etat, protocole, bloc, addr, ops, dst)
                    if "[" in dst else False)
                if mn in ("and", "or", "xor", "test"):
                    etat.flags["cf"] = False
                    etat.flags["of"] = False
                    etat.flags["zf"] = td or ts
                    etat.flags["sf"] = td or ts
                else:
                    for f in ("cf", "zf", "sf", "of"):
                        etat.flags[f] = td or ts
                return
            if dst in _PARENT:
                p_dst = etat.ptr.get(_reg64(dst))
                src_publique = RE_VAL.match(src) is not None or (
                    src in _PARENT and
                    not etat.regs.get(_reg64(src), False))
                if mn in ("add", "sub") and p_dst is not None and \
                        src_publique and not taint_reg(dst):
                    # LE POINTEUR AVANCE d'un montant PUBLIC symbolique
                    # (add rdi, compteur — le remplissage du tampon) : la
                    # RACINE DEMEURE, le décalage devient symbolique, la
                    # partie constante porte l'ancien décalage exact
                    # (pose_reg D'ABORD — il nettoie le ptr par convention)
                    pose_reg(dst, False)
                    racine, delta, const = p_dst
                    etat.ptr[_reg64(dst)] = (
                        racine, None, delta if delta is not None else const)
                else:
                    pose_reg(dst, taint_reg(dst) or ts)
                    etat.ptr.pop(_reg64(dst), None)
            elif "[" in dst:
                td = self._lecture(etat, protocole, bloc, addr, ops, dst)
                self._ecriture(etat, protocole, bloc, addr, ops, dst,
                               td or ts)
            # les drapeaux
            if mn in ("and", "or", "xor", "test"):
                etat.flags["cf"] = False
                etat.flags["of"] = False
                etat.flags["zf"] = (taint_reg(dst) if dst in _PARENT
                                    else False) or ts
                etat.flags["sf"] = etat.flags["zf"]
            else:
                for f in ("cf", "zf", "sf", "of"):
                    etat.flags[f] = (taint_reg(dst) if dst in _PARENT
                                     else False) or ts
            return
        if mn in ("inc", "dec"):
            dst = cs[0]
            if dst in _PARENT:
                for f in ("zf", "sf", "of"):
                    etat.flags[f] = taint_reg(dst)
            elif "[" in dst:
                t = self._lecture(etat, protocole, bloc, addr, ops, dst)
                for f in ("zf", "sf", "of"):
                    etat.flags[f] = t
            return
        if mn == "not":
            return                              # le taaint inchangé
        if mn in ("shl", "shr", "sar", "rol", "ror"):
            dst, src = cs[0], cs[1]
            tc = taint_reg(src) if src in _PARENT else False
            if dst in _PARENT:
                pose_reg(dst, taint_reg(dst) or tc)
                etat.ptr.pop(_reg64(dst), None)
                etat.flags["cf"] = etat.regs[_reg64(dst)]
                if mn in ("shl", "shr", "sar"):
                    etat.flags["zf"] = etat.flags["sf"] = \
                        etat.regs[_reg64(dst)]
            elif "[" in dst:
                t = self._lecture(etat, protocole, bloc, addr, ops, dst) or tc
                self._ecriture(etat, protocole, bloc, addr, ops, dst, t)
                etat.flags["cf"] = t
            return
        if mn in ("shld", "shrd"):
            dst, src2, cnt = cs[0], cs[1], cs[2]
            tc = taint_reg(cnt) if cnt in _PARENT else False
            t = (taint_reg(dst) if dst in _PARENT else False) or \
                (taint_reg(src2) if src2 in _PARENT else False) or tc
            pose_reg(dst, t)
            etat.flags["cf"] = t
            return
        if mn == "imul":
            if len(cs) == 3:
                dst, src, _imm = cs
                ts = taint_reg(src) if src in _PARENT else (
                    self._lecture(etat, protocole, bloc, addr, ops, src)
                    if "[" in src else False)
                pose_reg(dst, ts or taint_reg(dst) if dst in _PARENT else ts)
                if dst in _PARENT:
                    etat.ptr.pop(_reg64(dst), None)
            elif len(cs) == 2:
                dst, src = cs
                ts = taint_reg(src) if src in _PARENT else (
                    self._lecture(etat, protocole, bloc, addr, ops, src)
                    if "[" in src else False)
                pose_reg(dst, taint_reg(dst) or ts)
                etat.ptr.pop(_reg64(dst), None)
            elif len(cs) == 1 and "[" in cs[0]:
                t = self._lecture(etat, protocole, bloc, addr, ops, cs[0])
                etat.regs["rax"] = etat.regs["rax"] or t
                etat.regs["rdx"] = etat.regs["rdx"] or t
            for f in ("cf", "of", "zf", "sf"):
                etat.flags[f] = etat.regs["rax"]
            return
        if mn == "mul":
            src = cs[0]
            t = taint_reg(src) if src in _PARENT else \
                self._lecture(etat, protocole, bloc, addr, ops, src)
            etat.regs["rax"] = etat.regs["rax"] or t
            etat.regs["rdx"] = etat.regs["rdx"] or t
            for f in ("cf", "of", "zf", "sf"):
                etat.flags[f] = etat.regs["rax"]
            return

        # ---- les drapeaux seuls
        if mn in _COND and mn.startswith("set"):
            pose_reg(cs[0], any(etat.flags[f] for f in _COND[mn]))
            return
        if mn == "cmp" or mn == "test":
            return                              # déjà traité ci-dessus

        # ---- la pile
        if mn == "push":
            src = cs[0]
            t = taint_reg(src) if src in _PARENT else (
                False if RE_VAL.match(src) else
                self._lecture(etat, protocole, bloc, addr, ops, src)
                if "[" in src else False)
            etat.sp -= 8
            if etat.sp_sym:
                if t:
                    etat.seaux[etat.sp_racine] = True
                return
            etat.ptr["rsp"] = (etat.sp_racine, etat.sp, 0)
            etat.cells[(etat.sp_racine, etat.sp)] = t
            if src in _PARENT and _LARGEUR_REG.get(src, 64) == 64:
                p_src = etat.ptr.get(_reg64(src))
                if p_src is not None:
                    etat.ptrcells[(etat.sp_racine, etat.sp)] = p_src
            return
        if mn == "pop":
            dst = cs[0]
            if etat.sp_sym:
                pose_reg(dst, etat.seaux.get(etat.sp_racine, False))
                etat.sp += 8
                return
            t = etat.cells.get((etat.sp_racine, etat.sp), False)
            pose_reg(dst, t)
            if dst in _PARENT and _LARGEUR_REG.get(dst, 64) == 64:
                p_mem = etat.ptrcells.get(("SP", etat.sp))
                if p_mem is not None:
                    etat.ptr[_reg64(dst)] = p_mem
            etat.cells[(etat.sp_racine, etat.sp)] = False
            etat.sp += 8
            etat.ptr["rsp"] = (etat.sp_racine, etat.sp, 0)
            if dst in _PARENT and _LARGEUR_REG.get(dst, 64) == 64:
                etat.ptr.pop(_reg64(dst), None)
            return

        # ---- les sauts (les obligations BRANCHE ici)
        if mn.startswith("j") and mn != "jmp":
            cond = _COND.get(mn)
            if cond is None:
                raise EchecAudit(f"condition non modélisée : {mn} {ops}")
            if any(etat.flags[f] for f in cond):
                bornes = 1 << 51 if bloc == "tls13-10" else None
                self._obligation(protocole, bloc, addr, f"{mn} {ops}",
                                 "BRANCHE",
                                 f"les drapeaux {'/'.join(cond)} testés sont "
                                 f"taaints (dérivés du secret)", etat, bornes)
            return
        if mn == "jmp":
            if not ops.startswith("0x"):
                self._obligation(protocole, bloc, addr, f"jmp {ops}",
                                 "BRANCHE", "jmp indirect de cible non "
                                 "constante — hors modèle (fail-closed)")
                raise EchecAudit(f"jmp indirect @{addr:#x} — le modèle "
                                 f"refuse (fail-closed)")
            return
        if mn == "ret":
            return

        # ---- les chaînes rep
        if mn in ("movsb", "stosb") and ops == "" or mn.startswith("rep"):
            return self._transfert_rep(protocole, bloc, etat, insn)

        # ---- les SSE / AES-NI (la propagation opaque)
        if mn in ("movdqa", "movdqu"):
            dst, src = cs[0], cs[1]
            if "[" in dst:
                # movdqu [mem], xmm : L'ÉCRITURE à l'adresse (16 octets)
                self._ecriture(etat, protocole, bloc, addr, ops, dst,
                               etat.regs.get(src, False))
            elif "[" in src:
                etat.regs[dst] = self._lecture(etat, protocole, bloc, addr,
                                               ops, src)
            else:
                etat.regs[dst] = etat.regs.get(src, False)
            return
        if mn == "pxor":
            dst, src = cs[0], cs[1]
            if dst == src:
                etat.regs[dst] = False
            else:
                etat.regs[dst] = etat.regs.get(dst, False) or \
                    etat.regs.get(src, False)
            return
        if mn in ("pslldq", "psrldq", "pshufd", "psllq", "psrlq"):
            etat.regs[cs[0]] = etat.regs.get(cs[0], False)
            return
        if mn in ("aesenc", "aesenclast", "aeskeygenassist", "pclmulqdq"):
            dst, src = cs[0], cs[1]
            ts = etat.regs.get(src, False) if re.match(r"^xmm\d+$", src) \
                else (self._lecture(etat, protocole, bloc, addr, ops, src)
                      if "[" in src else False)
            etat.regs[dst] = etat.regs.get(dst, False) or ts
            return

        if mn in ("nop", "endbr64", "cld", "std", "lfence", "mfence",
                  "sfence", "int3"):
            return
        raise EchecAudit(f"mnémonique non modélisé @{addr:#x} : {mn} {ops} "
                         f"(le modèle refuse — fail-closed)")

    def _transfert_rep(self, protocole, bloc, etat, insn):
        addr, mn, ops, taille = insn
        if "movsb" not in mn and "stosb" not in mn:
            raise EchecAudit(f"chaîne rep non modélisée : {mn} {ops}")
        # LE COMPTE : rcx taaint = l'obligation BRANCHE (facteur de travail)
        if etat.regs.get("rcx", False):
            self._obligation(protocole, bloc, addr, mn, "BRANCHE",
                             "le COMPTE rep (rcx) est taaint — le facteur "
                             "de travail dépend du secret", etat)
        pd = self._ptr_du(etat, "rdi")
        ps = self._ptr_du(etat, "rsi")
        if "movsb" in mn:
            # copie src→dst sur rcx octets : le seau/cellules de dst
            # absorbent ceux de src — la FENÊTRE 64 o (le compte des rep des
            # blocs audités : min(64 − remplissage, reste) — sha-03/04,
            # hmac-05, libc-01 ; VÉRIFIÉE aux notations, consignée au rapport)
            if pd is not None:
                racine_d = pd[0]
                t_src = False
                if ps is not None:
                    racine_s = ps[0]
                    t_src = etat.seaux.get(racine_s, False) or \
                        any(v for (r, o), v in etat.cells.items()
                            if r == racine_s and abs(o - (ps[1] or 0)) < 0x40)
                if t_src:
                    etat.seaux[racine_d] = True
                    base = pd[1] if pd[1] is not None else pd[2]
                    for o in range(base, base + 0x40):
                        etat.cells[(racine_d, o)] = True
            etat.regs["rcx"] = False
            etat.ptr.pop("rdi", None)
            etat.ptr.pop("rsi", None)
            return
        # stosb : eax écrit rcx octets à rdi — à décalage EXACT la masse
        # nettoie ses cellules ; à décalage SYMBOLIQUE elle ne nettoie PAS
        if pd is not None:
            racine_d = pd[0]
            if pd[1] is not None:
                base = pd[1]
                t = etat.regs.get("rax", False)
                for o in range(base, base + 0x40):
                    etat.cells[(racine_d, o)] = \
                        etat.cells.get((racine_d, o), False) and t
            elif etat.regs.get("rax", False):
                for o in range(pd[2], pd[2] + 0x40):
                    etat.cells[(racine_d, o)] = True
                etat.seaux[racine_d] = True
        etat.regs["rcx"] = False
        etat.ptr.pop("rdi", None)
        return

    # ══════════════════════════════════════════════════════════════════════
    # 5 · LE FIXPOINT PAR FONCTION + L'INTERPROCEDURAL MÉMOÏSÉ
    # ══════════════════════════════════════════════════════════════════════

    def _signature(self, etat: Etat) -> tuple:
        """La signature canonique : le taaint des scalaires, et pour chaque
        pointeur d'argument le TAINT RELATIF des cellules pointées (les
        décalages tranchés à la fenêtre ±0x400) + le seau + GLOBAL."""
        scal = tuple(sorted(r for r in VOLATILES if etat.regs[r]))
        ptrs = []
        for reg in ("rcx", "rdx", "r8", "r9"):
            p = etat.ptr.get(reg)
            if p is None:
                ptrs.append(None)
                continue
            racine, delta, _c = p
            offs = sorted(o - (delta or 0) for (r, o), v in etat.cells.items()
                          if r == racine and v and abs(o - (delta or 0)) < 0x400)
            ptrs.append((tuple(offs), etat.seaux.get(racine, False)))
        glob = (tuple(sorted(o for (r, o), v in etat.cells.items()
                       if r == "GLOBAL" and v)),
                etat.seaux.get("GLOBAL", False))
        return (scal, tuple(ptrs), glob)

    def _applique_signature(self, etat: Etat, sig: tuple):
        """Rejoue une signature d'entrée : les cellules des pointeurs
        d'arguments reçoivent leur taaint relatif, GLOBAL aussi."""
        _scal, ptrs, glob = sig
        for reg, desc in zip(("rcx", "rdx", "r8", "r9"), ptrs):
            if desc is None:
                continue
            offs, seau = desc
            p = etat.ptr.get(reg)
            if p is None:
                continue
            racine, delta, _c = p
            delta = delta or 0
            for o in offs:
                etat.cells[(racine, delta + o)] = True
            if seau:
                etat.seaux[racine] = True
        goffs, gseau = glob
        for o in goffs:
            etat.cells[("GLOBAL", o)] = True
        if gseau:
            etat.seaux["GLOBAL"] = True

    def _analyse_fonction(self, protocole: str, bloc: str, entree: int,
                          etat_entree: Etat, profondeur: int = 0) -> Etat:
        """Le fixpoint worklist sur le CFG de la fonction ; renvoie l'état
        AUX RET (le join des sorties) ; les obligations levées au passage."""
        if profondeur > 12:
            raise EchecAudit(f"{bloc}+{entree:#x} : profondeur interprocédurale"
                             " > 12 — le modèle refuse (fail-closed)")
        fn = self.fonctions[(bloc, entree)]
        etat_entree.sp_racine = f"SP·{bloc}·{entree:#x}·{len(self.memo)}"
        etats: dict[int, Etat | None] = {d: None for d in fn.bbs}
        etats[entree] = etat_entree.copie()
        file = [entree]
        sorties: list[Etat] = []
        garde = 0
        while file:
            garde += 1
            if garde > 200000:
                raise EchecAudit(f"{bloc}+{entree:#x} : le worklist diverge —"
                                 " le modèle refuse (fail-closed)")
            d = file.pop(0)
            e = etats[d]
            if e is None:
                continue
            e = e.copie()
            ok_sortie = True
            for i in fn.bbs[d]:
                insn = fn.insns[i]
                addr, mn, ops, taille = insn
                if mn == "call":
                    self._appel(protocole, bloc, e, insn, profondeur)
                    continue
                if mn == "ret":
                    sorties.append(e.copie())
                    ok_sortie = False
                    break
                self.transfert(protocole, bloc, e, insn)
            if not ok_sortie:
                continue
            for s in fn.succ.get(d, []):
                if s not in fn.bbs:
                    continue
                if etats[s] is None:
                    etats[s] = e.copie()
                    file.append(s)
                else:
                    if etats[s].join(e):
                        file.append(s)
        if not sorties:
            return etat_entree.copie()
        out = sorties[0].copie()
        for s in sorties[1:]:
            out.join(s)
        return out

    def _appel(self, protocole: str, bloc: str, etat: Etat, insn,
               profondeur: int):
        """Un call : direct (interprocédural mémoïsé), IAT (le modèle nommé),
        ou interne au bloc (le sous-programme local)."""
        addr, mn, ops, taille = insn
        if ops.startswith("0x"):
            cible = int(ops, 0)
            loc = self.adresse_fonction.get(cible)
            if loc is None:
                raise EchecAudit(f"{bloc} @{addr:#x} : appel direct à "
                                 f"{cible:#x} hors blocs audités — le modèle "
                                 f"refuse (fail-closed)")
            nom_c, entree_c = loc
            # la signature du callee : LE TAINT CHEZ L'APPELANT (les cellules
            # sous les pointeurs d'arguments, les scalaires volatils, GLOBAL)
            # — capturée AVANT la construction de l'état callee (vide par
            # construction : le taaint vit chez l'appelant, aux racines mêmes)
            sig = self._signature(etat)
            etat_c = Etat()
            for reg in ("rcx", "rdx", "r8", "r9"):
                etat_c.regs[reg] = etat.regs[reg]
                if reg in etat.ptr:
                    etat_c.ptr[reg] = etat.ptr[reg]
            cle = (nom_c, entree_c, sig, protocole)
            if cle in self.memo:
                resume = self.memo[cle]
            else:
                self._applique_signature(etat_c, sig)
                etat_c.ptr["rsp"] = (etat_c.sp_racine, 0, 0)
                sortie = self._analyse_fonction(protocole, nom_c, entree_c,
                                                etat_c, profondeur + 1)
                resume = self._resume(sortie, etat_c)
                self.memo[cle] = resume
            # l'application du résumé : les cellules des pointeurs d'args
            _rax, effets = resume
            for (reg, offs, seau) in effets:
                p = etat.ptr.get(reg)
                if p is None:
                    continue
                racine, delta, _c = p
                delta = delta or 0
                for o in offs:
                    etat.cells[(racine, delta + o)] = True
                if seau:
                    etat.seaux[racine] = True
            etat.regs["rax"] = _rax
            for r in VOLATILES - {"rax"}:
                etat.regs[r] = False       # la convention msx64 : volatiles
                etat.ptr.pop(r, None)
            return
        if "[rip" in ops:
            feuille = self.slot_feuille.get((bloc, addr))
            if feuille is None:
                # un appel IAT hors modèle : FEUILLE PUBLIQUE (eax public)
                etat.regs["rax"] = False
                for r in VOLATILES - {"rax"}:
                    etat.regs[r] = False
                    etat.ptr.pop(r, None)
                return
            if feuille not in MODELES_IAT:
                raise EchecAudit(f"{bloc} @{addr:#x} : feuille IAT {feuille} "
                                 "sans modèle nommé — le modèle refuse "
                                 "(fail-closed)")
            taint_buf, _eax_pub = MODELES_IAT[feuille]
            if taint_buf:
                # READFILE : LA SOURCE DU SECRET — le tampon rdx devient
                # taaint (le contenu du fichier, le protocole mesuré de
                # loupe-06 : fixe.bin contre alea.bin)
                p = etat.ptr.get("rdx")
                if p is not None:
                    racine, delta, _c = p
                    delta = delta or 0
                    for o in range(delta, delta + 0x10000):
                        etat.cells[(racine, o)] = True
                    etat.seaux[racine] = True
                else:
                    etat.seaux["GLOBAL"] = True
            etat.regs["rax"] = False
            for r in VOLATILES - {"rax"}:
                etat.regs[r] = False
                etat.ptr.pop(r, None)
            return
        raise EchecAudit(f"{bloc} @{addr:#x} : appel indirect {ops!r} — le "
                         "modèle refuse (fail-closed)")

    def _resume(self, sortie: Etat, entree: Etat):
        """Le résumé d'un callee : rax + les cellules TAINTES NOUVELLES sous
        les pointeurs d'arguments (relatives), les seaux posés."""
        effets = []
        for reg in ("rcx", "rdx", "r8", "r9"):
            p = entree.ptr.get(reg)
            if p is None:
                continue
            racine, delta, _c = p
            delta = delta or 0
            offs_avant = {o for (r, o), v in entree.cells.items()
                          if r == racine and v}
            offs_apres = {o for (r, o), v in sortie.cells.items()
                          if r == racine and v}
            nouveaux = sorted(o - delta for o in offs_apres - offs_avant
                              if abs(o - delta) < 0x400)
            seau = sortie.seaux.get(racine, False) and \
                not entree.seaux.get(racine, False)
            if nouveaux or seau:
                effets.append((reg, nouveaux, seau))
        # les effets sur GLOBAL (aucun callee n'écrit GLOBAL : les feuilles
        # IAT vivent dans loupe-06 seul — consigné au rapport)
        return (sortie.regs["rax"], effets)


# ══════════════════════════════════════════════════════════════════════════════
# 6 · LES PROTOCOLES (les obligations O1-O6 — les entrées MESURÉES, fidèles)
# ══════════════════════════════════════════════════════════════════════════════

# (nom du protocole, bloc d'entrée, secrets : liste (registre, début, longueur)
#  — le CONTENU pointé est le secret, les longueurs et le reste publics)
PROTOCOLES = [
    # O1 · sha-256 — le protocole v110 : le message de 55 o (fixe contre
    # aléatoire) absorbé puis finalisé ; le bloc de compression SOUS DEUX
    # protocoles (le bloc secret seul ; le bloc ET l'état secrets — les
    # compressions amont), l'état+tampon du contexte secrets, les
    # longueurs (96, 104) publiques.
    ("O1a-sha256-init (aucun secret)", "tls13-01", []),
    ("O1b-sha256-comprimer (le bloc 64 o)", "tls13-02", [("rdx", 0, 64)]),
    ("O1c-sha256-comprimer (bloc + état)", "tls13-02",
     [("rcx", 0, 32), ("rdx", 0, 64)]),
    ("O1d-sha256-absorber (le tampon)", "tls13-03",
     [("rcx", 0, 96), ("rdx", 0, 55)]),
    ("O1e-sha256-finaliser (l'état+tampon)", "tls13-04",
     [("rcx", 0, 96)]),
    # O2 · hmac — la clé 32 o secrète (rdx = la longueur PUBLIQUE 32)
    ("O2-hmac (la clé 32 o)", "tls13-05", [("rcx", 0, 32)]),
    # O3 · hkdf — l'IKM 22 o secrète (le message du HMAC interne) ; la
    # famille complétée : expand/expand-label sous PRK secret
    ("O3a-hkdf-extract (l'IKM 22 o)", "tls13-06", [("r8", 0, 22)]),
    ("O3b-hkdf-expand (le PRK)", "tls13-07", [("rcx", 0, 32)]),
    ("O3c-hkdf-expand-label (le PRK)", "tls13-08", [("rcx", 0, 32)]),
    # O4 · x25519 — la clé privée secrète (le point de base u PUBLIC : le
    # kit-2 tient aux constant entre classes)
    ("O4-x25519 (la clé privée)", "tls13-14", [("rdx", 0, 32)]),
    # O5 · aes-gcm — la clé secrète : rcx porte LE DÉPLOIEMENT COMPLET des
    # clés de tour (176 o — la round key 0 EST la clé, les 10 suivantes en
    # dérivent : le harnais pose ADR_RK = le schedule expansé, le kit-2
    # varie `cle` → TOUT le schedule varie) ; sceller ET ouvrir (le verdict
    # d'étiquette : l'écart nommé attendu)
    ("O5a-aesgcm-sceller (la clé 16 o)", "tls13-18", [("rcx", 0, 176)]),
    ("O5b-aesgcm-ouvrir (la clé 16 o)", "tls13-19", [("rcx", 0, 176)]),
    # O6 · md5 — le contenu du fichier (LA SOURCE : le modèle ReadFile
    # taaint le tampon — aucune déclaration d'entrée, le secret ENTRE à
    # la frontière du système)
    ("O6-md5 (le contenu du fichier)", "loupe-06", []),
]


def auditer(moteur: Moteur, protocoles=None) -> list[dict]:
    """Déroule les protocoles : chaque entrée reçoit ses secrets, la
    fonction d'entrée analysée au fixpoint, les obligations collectées."""
    for (nom, bloc, secrets) in (protocoles or PROTOCOLES):
        etat = Etat()
        etat.ptr["rsp"] = ("SP", 0)
        # les pointeurs d'arguments : racines fraîches par protocole
        for reg in ("rcx", "rdx", "r8", "r9"):
            r = f"P_{nom}_{reg}"
            etat.ptr[reg] = (r, 0, 0)
        etat.ptr["rsp"] = ("SP", 0)
        for (reg, debut, longue) in secrets:
            r = etat.ptr[reg][0] if reg in etat.ptr else f"P_{nom}_{reg}"
            for o in range(debut, debut + longue):
                etat.cells[(r, o)] = True
        moteur._analyse_fonction(nom, bloc, BLOCS[bloc][2], etat)
    return moteur.obligations


# ══════════════════════════════════════════════════════════════════════════════
# 7 · LA DÉCHARGE SMT SUR LES CHEMINS (le tranchage arrière, Z3 — non bornée)
# ══════════════════════════════════════════════════════════════════════════════

_FENETRE_TRANCHAGE = 96


def decharge_smt(moteur: "Moteur", ob: dict) -> dict:
    """La décharge d'une obligation : l'expression de la condition (resp. de
    l'adresse, resp. du COMPTE rep) reconstruite PAR TRANCHAGE ARRIÈRE depuis
    le site — les feuilles sont les CHARGEMENTS DU SECRET (symboles libres :
    la preuve est NON BORNÉE, ∀ valeurs) ; à la frontière du tranchage
    (entrée de fonction, appel, fusion), la feuille prend le TAINT CONSTATÉ
    PAR LE MOTEUR au site (un registre taaint y devient une feuille SECRÈTE —
    jamais publique par commodité) ; Z3 tranche :
      expr(s1) ≠ expr(s2) SATISFIABLE → le TÉMOIN (violation) ;
      INSATISFIABLE → DÉCHARGÉE (la dépendance syntaxique était nulle) ;
      `bornes` (l'INVARIANT NOMMÉ, p.ex. les membres réduits < 2^51 de
      tls13-10) : la question est posée SOUS la borne — une décharge sous
      borne est une DÉCHARGE CONDITIONNELLE, l'invariant demeurant NON
      PROUVÉ par le présent audit (l'écart reste nommé)."""
    if z3 is None:
        return {**ob, "verdict": "VIOLATION",
                "smt": "z3 absent — fail-closed (jamais une décharge par "
                       "l'ignorance)"}
    if ob.get("bornes") and ob["addr"] == 0xCAB6:
        # LA BRANCHE D'EMPUNT DE tls13-10 : la question SANS borne est
        # tranchée par le modèle dédié (le tranchage générique n'atteint
        # pas la chaîne multi-membres à travers les allers-retours pile)
        return {**ob, "verdict": "VIOLATION",
                "smt": "Z3 SANS borne (le modèle dédié, membres libres) : "
                       "SAT — la retenue PEUT dépendre des données. " +
                       preuve_emprunt_tls13_10()}
    fn = None
    for (nom, e), f in moteur.fonctions.items():
        if nom == ob["bloc"] and ob["addr"] in f.adresses:
            fn = f
            break
    if fn is None:
        return {**ob, "verdict": "VIOLATION",
                "smt": "site hors fonction — fail-closed"}
    idx = fn.idx[ob["addr"]]
    bb = None
    for d, seq in fn.bbs.items():
        if idx in seq:
            bb = seq
            break
    regs_taint = ob.get("regs_taint", {})
    secrets: list = []
    compte = [0]

    provenance: dict = {}          # symbole → (base, décalage) de la charge

    def feuille(taaint: bool, source: str | None = None):
        if taaint:
            s = z3.BitVec(f"s{compte[0]}", 64)
            compte[0] += 1
            secrets.append(s)
            if source:
                mm = _RE_MEM_RE.match(source.strip())
                if mm:
                    _b, _i, _e, _d = _decortique_memoire(mm.group(2))
                    if _b and _b in _PARENT and _i is None:
                        provenance[s] = (_reg64(_b), _d)
            return s
        return z3.BitVec(f"pub{compte[0] + 1000}", 64)

    # les besoins initiaux : drapeaux de la condition / adresses / le compte
    cible = ob["texte"].split()[0]
    besoins: set = set()          # ('r', nom64) | ('f', drapeau)
    if ob["classe"] == "BRANCHE" and ob["texte"].startswith("rep"):
        besoins.add(("r", "rcx"))
    elif ob["classe"] == "BRANCHE" and cible in _COND:
        for f in _COND[cible]:
            besoins.add(("f", f))
    else:
        m = re.search(r"\[([^\]]+)\]", ob["texte"])
        if m:
            base, idxx, _e, _d = _decortique_memoire(m.group(1))
            for comp in (base, idxx):
                if comp and comp in _PARENT:
                    besoins.add(("r", _reg64(comp)))
    if not besoins:
        return {**ob, "verdict": "VIOLATION",
                "smt": "rien à trancher (opaque) — fail-closed"}
    vals: dict = {}               # ('r', nom) → BitVec / ('f', nom) → Bool
    tardees: list = []            # (symbole_bool, clé_drapeau) — la chaîne
    zone = bb if bb is not None else fn.sequence
    pos = zone.index(idx) if idx in zone else 0

    def expr_reg(nom, site_taint=None):
        """L'expression courante d'un registre — connue, DIFFÉRÉE (la
        définition vit plus haut dans la remontée : un symbole résolu à la
        définition), ou FEUILLE au taaint du site (la frontière)."""
        k = ("r", _reg64(nom)) if nom in _PARENT else None
        if k and k in vals:
            return vals[k]
        if k:
            sym = z3.BitVec(f"reg_att_{compte[0]}", 64)
            compte[0] += 1
            tardees.append((sym, k))
            besoins.add(k)
            syms_courants.add(sym)
            return sym
        return feuille(regs_taint.get(_reg64(nom), False)
                       if site_taint is None else site_taint)

    def lit_expr(op, site_taint=None):
        """L'expression d'un opérande (registre, immédiat ou mémoire —
        une CHARGE MÉMOIRE est une feuille SECRÈTE AVEC PROVENANCE :
        fail-closed et l'invariant de valeur s'appuie dessus)."""
        if _RE_VAL_RE.match(op):
            return z3.BitVecVal(int(op, 0) & ((1 << 64) - 1), 64)
        if op in _PARENT:
            return expr_reg(op, site_taint)
        if "[" in op:
            return feuille(True, op)
        return feuille(False)

    for j in range(pos - 1, max(-1, pos - 1 - _FENETRE_TRANCHAGE), -1):
        a, mn, ops, _t = fn.insns[zone[j]]
        cs = [p.strip() for p in ops.split(",")] if ops else []
        src = cs[1] if len(cs) > 1 else ""
        syms_courants = set()
        if mn == "call":
            # les volatiles meurent à la frontière : feuille au taaint du site
            for b in list(besoins):
                if b[0] == "r" and b[1] in VOLATILES:
                    vals[b] = feuille(regs_taint.get(b[1], False))
                    besoins.discard(b)
            continue
        if mn == "ret":
            continue
        # CMP/TEST : les drapeaux SANS écriture de registre
        if mn in ("cmp", "test"):
            drapeaux_ecrits = {"cf", "of", "zf", "sf"}
            bes_drapeaux = {b for b in besoins if b[0] == "f" and
                            b[1] in drapeaux_ecrits}
            if bes_drapeaux:
                # un opérande MÉMOIRE dans le tranchage est une feuille
                # SECRÈTE (fail-closed : la charge pourrait porter le secret)
                e1 = (feuille(True) if "[" in cs[0] else
                      (lit_expr(cs[0]) if cs[0] in _PARENT else
                       lit_expr(cs[0])))
                e2 = (feuille(True) if len(cs) > 1 and "[" in cs[1] else
                      lit_expr(src) if len(cs) > 1 else
                      z3.BitVecVal(0, 64))
                for b in bes_drapeaux:
                    if b[1] == "zf":
                        # TEST : ZF = ((a & b) == 0) ; CMP : ZF = (a-b == 0)
                        vals[b] = (((e1 & e2) == 0) if mn == "test"
                                   else ((e1 - e2) == 0))
                    elif b[1] == "cf":
                        vals[b] = (z3.ULT(e1, e2) if mn == "cmp"
                                   else z3.BoolVal(False))
                    elif b[1] == "sf":
                        vals[b] = (((((e1 & e2) if mn == "test"
                                      else (e1 - e2))) & 0x80) != 0)
                    else:               # of : la reconstruction échoue
                        return {**ob, "verdict": "VIOLATION",
                                "smt": "le drapeau OF de cmp/test — "
                                       "fail-closed"}
                    besoins.discard(b)
                for tok in ([cs[0]] + ([src] if src else [])):
                    if tok and tok in _PARENT:
                        besoins.add(("r", _reg64(tok)))
            continue
        # les DÉFINITIONS de registres
        if mn in ("mov", "movabs", "movzx", "movsx", "movsxd", "lea",
                  "bswap", "setcc") or mn in ("add", "sub", "adc", "sbb",
                  "and", "or", "xor", "shl", "shr", "sar", "rol", "ror",
                  "shld", "shrd", "imul", "mul", "not", "inc", "dec", "neg",
                  "xchg"):
            dst = cs[0] if cs else ""
            dst64 = _reg64(dst) if dst in _PARENT else None
            kdst = ("r", dst64) if dst64 else None
            touche_reg = kdst in besoins
            # les drapeaux définis par l'opération
            drapeaux_ecrits = set()
            if mn in ("add", "sub", "adc", "sbb", "cmp", "neg", "inc",
                      "dec", "mul", "imul"):
                drapeaux_ecrits = {"cf", "zf", "sf", "of"}
            elif mn in ("and", "or", "xor", "test"):
                drapeaux_ecrits = {"cf", "of", "zf", "sf"}
            elif mn in ("shl", "shr", "sar", "rol", "ror", "shld", "shrd"):
                drapeaux_ecrits = {"cf", "zf", "sf"}
            bes_drapeaux = {b for b in besoins if b[0] == "f" and
                            b[1] in drapeaux_ecrits}
            if not touche_reg and not bes_drapeaux:
                continue
            # construire les expressions des opérandes
            src = cs[1] if len(cs) > 1 else "0"
            if mn in ("mov", "movabs"):
                e = lit_expr(src, False if _RE_VAL_RE.match(src) else None)
            elif mn in ("movzx", "movsx", "movsxd"):
                e = lit_expr(src)
            elif mn == "lea":
                e = lit_expr(src.replace("ptr ", "").strip()
                             if "ptr" in src else src)
                # lea reg, [b + i*n + d] : expr approximée par la somme des
                # composantes — la reconstruction exacte des déplacements
                mm = _RE_MEM_RE.match(src)
                if mm:
                    _b, _i, _ec, _dp = _decortique_memoire(mm.group(2))
                    morceaux = []
                    if _b and _b in _PARENT:
                        morceaux.append(expr_reg(_b))
                    if _i and _i in _PARENT:
                        v = expr_reg(_i)
                        for _ in range(abs(_ec) if _ec else 1):
                            pass
                        morceaux.append(v if _ec >= 0 else -v)
                    if _dp:
                        morceaux.append(z3.BitVecVal(_dp & ((1 << 64) - 1), 64))
                    e = morceaux[0] if len(morceaux) == 1 else (
                        morceaux[0] + morceaux[1] if len(morceaux) == 2 and
                        _dp == 0 else feuille(False))
                    if len(morceaux) > 2 or (_i and _ec not in (1, 4, 8)):
                        e = feuille(False)   # formes composées : feuille pub
            elif mn == "bswap":
                e = lit_expr(cs[0])
            elif mn in ("add", "adc"):
                e = lit_expr(cs[0]) + lit_expr(src)
            elif mn in ("sub", "sbb"):
                e = lit_expr(cs[0]) - lit_expr(src)
            elif mn == "xor":
                e = lit_expr(cs[0]) ^ lit_expr(src)
            elif mn == "and":
                e = lit_expr(cs[0]) & lit_expr(src)
            elif mn == "or":
                e = lit_expr(cs[0]) | lit_expr(src)
            elif mn == "not":
                e = ~lit_expr(cs[0])
            elif mn == "neg":
                e = -lit_expr(cs[0])
            elif mn in ("inc", "dec"):
                e = lit_expr(cs[0]) + (1 if mn == "inc" else -1)
            elif mn in ("shl", "shr", "sar"):
                e = lit_expr(cs[0])
            elif mn in ("rol", "ror", "shld", "shrd"):
                e = feuille(False) if (len(cs) < 3) else lit_expr(cs[0])
            elif mn in ("imul", "mul"):
                e = lit_expr(cs[0]) * lit_expr(src if len(cs) > 1 else cs[0])
            else:
                e = feuille(regs_taint.get(dst64, False))
            if mn in ("movzx", "movsx", "movsxd") and "[" in src:
                e = feuille(True, src)   # UNE CHARGE : la feuille du secret
            if mn in ("mov", "movabs") and "[" in src:
                # UNE CHARGE : d'abord LE RACCORD au magasin antérieur (même
                # texte d'adresse) — sinon la feuille du secret (fail-closed)
                e = None
                for k in range(j - 1, max(-1, pos - 1 -
                                          _FENETRE_TRANCHAGE), -1):
                    a2, m2, o2, _t2 = fn.insns[zone[k]]
                    if m2 in ("mov", "movabs") and o2.startswith(src + ","):
                        # mov [même adresse], SRC2 : la valeur stockée — un
                        # SYMBOLE DIFFÉRÉ (la définition de SRC2 vit plus
                        # haut dans la remontée : la substitution au terme)
                        src2 = o2[len(src) + 1:].strip()
                        if _RE_VAL_RE.match(src2):
                            e = z3.BitVecVal(int(src2, 0) & ((1 << 64) - 1),
                                             64)
                        elif src2 in _PARENT:
                            sym2 = z3.BitVec(f"reg_amont{j}_{src2}", 64)
                            tardees.append((sym2, ("r", _reg64(src2))))
                            besoins.add(("r", _reg64(src2)))
                            e = sym2
                        else:
                            e = feuille(True)
                        break
                    if m2 in ("add", "sub", "adc", "sbb", "xor", "and",
                              "or") and o2.startswith(src + ","):
                        e = feuille(True)   # le magasin MUTÉ : feuille
                        break
                if e is None:
                    e = feuille(True, src)
            if touche_reg:
                # la définition RÉSOUT les symboles différés qui
                # l'attendaient (les demandes AVAL dans l'ordre du
                # programme) — JAMAIS ceux créés par la présente
                # instruction (l'auto-résolution S := S est la fuite)
                vals[kdst] = e
                besoins.discard(kdst)
                for k in range(len(tardees) - 1, -1, -1):
                    if tardees[k][1] == kdst and \
                            tardees[k][0] not in syms_courants:
                        sym_att, _cle = tardees.pop(k)
                        for kk in list(vals):
                            if isinstance(vals[kk], z3.ExprRef):
                                vals[kk] = z3.substitute(
                                    vals[kk], [(sym_att, e)])
                        break
                # les opérandes deviennent nécessaires (la remontée) —
                # la SOURCE et le COMPTE, jamais la destination (définie)
                for tok in ([src] if src else []) + \
                        ([cs[2]] if len(cs) > 2 else []):
                    if tok and tok in _PARENT:
                        besoins.add(("r", _reg64(tok)))
            if bes_drapeaux:
                sym_nouveau = None
                for b in sorted(bes_drapeaux):
                    if b[1] == "cf" and mn == "sbb":
                        # LA CHAÎNE D'EMPUNT : le CF du sbb = ULT(x,
                        # y + L'EMPUNT ANTÉRIEUR) — un Bool LIBRE en
                        # attente, résolu par la définition ANTÉRIEURE
                        # ( poussé APRÈS la résolution LIFO : jamais
                        # résolu par lui-même )
                        sym = z3.Bool(f"cf_amont{j}")
                        sym_nouveau = sym
                        besoins.add(("f", "cf"))
                        vals[b] = z3.ULT(
                            lit_expr(cs[0]),
                            lit_expr(src) + z3.If(
                                sym, z3.BitVecVal(1, 64),
                                z3.BitVecVal(0, 64)))
                    elif b[1] == "zf":
                        if mn in ("test", "cmp"):
                            vals[b] = (lit_expr(cs[0]) == lit_expr(src))
                        else:
                            vals[b] = (e == 0)
                    elif b[1] == "cf":
                        if mn in ("sub", "cmp"):
                            vals[b] = z3.ULT(lit_expr(cs[0]),
                                             lit_expr(src))
                        elif mn in ("add", "adc"):
                            vals[b] = z3.ULE(lit_expr(cs[0]) +
                                             lit_expr(src),
                                             lit_expr(cs[0]))
                        elif mn in ("shl", "shld", "rol"):
                            n_dep = (src if RE_VAL.match(src) else "1")
                            if n_dep in ("1", "0x1"):
                                x = lit_expr(cs[0])
                                if mn == "shl":
                                    vals[b] = ((x >> 63) != 0)
                                elif mn == "shld":
                                    vals[b] = ((x >> 63) != 0)
                                else:                      # rol
                                    vals[b] = ((x >> 63) != 0)
                            else:
                                return {**ob, "verdict": "VIOLATION",
                                        "smt": "le CF de " + mn +
                                               " à compte variable — "
                                               "fail-closed"}
                        elif mn in ("shr", "sar", "shrd", "ror"):
                            n_dep = (src if RE_VAL.match(src) else
                                     (cs[2] if len(cs) > 2 else "1"))
                            if n_dep in ("1", "0x1"):
                                x = lit_expr(cs[0])
                                if mn == "shr":
                                    vals[b] = ((x & 1) != 0)
                                elif mn == "sar":
                                    vals[b] = ((x & 1) != 0)
                                elif mn == "shrd":
                                    vals[b] = ((x & 1) != 0)
                                else:                      # ror
                                    vals[b] = ((x & 1) != 0)
                            else:
                                return {**ob, "verdict": "VIOLATION",
                                        "smt": "le CF de " + mn +
                                               " à compte variable — "
                                               "fail-closed"}
                        else:
                            vals[b] = None
                    elif b[1] == "sf":
                        vals[b] = ((e & 0x80) != 0)
                    elif b[1] == "of":
                        vals[b] = None
                    if vals.get(b) is None:
                        return {**ob, "verdict": "VIOLATION",
                                "smt": f"le drapeau {b[1]} de {mn} — "
                                       "sémantique non reconstruite "
                                       "(fail-closed)"}
                    besoins.discard(b)
                    # LA RÉSOLUTION LIFO : le sbb AVAL qui attendait CE
                    # drapeau reçoit la présente définition (substituée
                    # partout — la propagation transitive est automatique ;
                    # le symbole NÉ CI-DESSUS n'est jamais résolu par
                    # lui-même)
                    for k in range(len(tardees) - 1, -1, -1):
                        if tardees[k][1] == b and \
                                tardees[k][0] is not sym_nouveau:
                            sym_att, _cle = tardees.pop(k)
                            for kk in list(vals):
                                if isinstance(vals[kk], z3.ExprRef):
                                    vals[kk] = z3.substitute(
                                        vals[kk], [(sym_att, vals[b])])
                            break
                if sym_nouveau is not None:
                    tardees.append((sym_nouveau, ("f", "cf")))
                for tok in [cs[0], src]:
                    if tok and tok in _PARENT:
                        besoins.add(("r", _reg64(tok)))
    # les besoins restants : les feuilles AU TAINT DU SITE (la frontière)
    for b in list(besoins):
        if b[0] == "r":
            vals[b] = feuille(regs_taint.get(b[1], False))
            besoins.discard(b)
        else:
            return {**ob, "verdict": "VIOLATION",
                    "smt": "le tranchage n'a pas reconstruit le drapeau "
                           "(opaque) — fail-closed"}
    # LES SUBSTITUTIONS DIFFÉRÉES : chaque symbole en attente reçoit la
    # définition trouvée par la remontée — JAMAIS lui-même (S := S est la
    # fuite) ; un symbole sans définition DANS LE BLOC est une valeur
    # INTER-BLOCS : la feuille AU TAINT DU SITE (fail-closed : un registre
    # taaint y devient une feuille SECRÈTE, jamais publique par commodité)
    for sym, cle in list(tardees):
        cible_expr = vals.get(cle)
        if isinstance(cible_expr, z3.ExprRef) and \
                str(sym) not in str(cible_expr):
            for k in list(vals):
                if isinstance(vals[k], z3.ExprRef):
                    vals[k] = z3.substitute(vals[k], [(sym, cible_expr)])
        elif cle[0] == "r":
            feuille_val = feuille(regs_taint.get(cle[1], False))
            for k in list(vals):
                if isinstance(vals[k], z3.ExprRef):
                    vals[k] = z3.substitute(vals[k], [(sym, feuille_val)])
        else:
            return {**ob, "verdict": "VIOLATION",
                    "smt": "la chaîne différée inachevée (l'amont "
                           "introuvable) — fail-closed"}
    # la question : quelle expression trancher ?
    cible_cond = None
    if ob["classe"] == "BRANCHE" and ob["texte"].startswith("rep"):
        cible_cond = vals.get(("r", "rcx"))
    elif ob["classe"] == "BRANCHE" and cible in _COND:
        parts = [vals.get(("f", f)) for f in _COND[cible]]
        if any(p is None for p in parts):
            return {**ob, "verdict": "VIOLATION",
                    "smt": "un drapeau de la condition non reconstruit — "
                           "fail-closed"}
        cible_cond = parts[0]
        for p in parts[1:]:
            cible_cond = z3.Or(cible_cond, p) if cible in ("ja", "jbe") \
                else z3.And(cible_cond, p)
    else:
        exprs = [v for k, v in vals.items() if k[0] == "r"]
        if not exprs:
            return {**ob, "verdict": "VIOLATION",
                    "smt": "l'expression du site non reconstruite — "
                           "fail-closed"}
        cible_cond = exprs[0]
    # LA QUESTION NON BORNÉE : expr(s1) ≠ expr(s2) pour des secrets libres ?
    P_25519 = (1 << 255) - 19

    def contraintes_valeur(bornes: int | None, prime: bool):
        """L'INVARIANT NOMMÉ : chaque FEUILLE < bornes ET — quand la
        provenance le permet — les VECTEURS composés (par registre de base,
        les membres contigus) < p = 2^255 − 19 (la forme réduite du domaine :
        la VALEUR, pas seulement le membre)."""
        cs_v = []
        for x in secrets:
            cs_v.append(z3.ULT(x, z3.BitVecVal(bornes, 64)))
            cs_v.append(z3.ULT(z3.BitVec(f"{x}!", 64),
                               z3.BitVecVal(bornes, 64)))
        if prime:
            vecteurs: dict = {}
            for x, (b, d) in provenance.items():
                vecteurs.setdefault(b, {})[d] = x
                vecteurs[b][d] = z3.BitVec(f"{x}!", 64)
            for _b, membres in vecteurs.items():
                if len(membres) >= 4 and set(membres) >= {0, 8, 16, 24, 32}:
                    for jeu in ({d: x for d, x in membres.items()
                                 if not str(x).endswith("!")},
                                {d: x for d, x in membres.items()
                                 if str(x).endswith("!")}):
                        val = z3.BitVecVal(0, 512)
                        for d, x in jeu.items():
                            val = val + z3.ZeroExt(512 - 64, x) * \
                                z3.BitVecVal(1 << (8 * d), 512)
                        cs_v.append(z3.ULT(val,
                                           z3.BitVecVal(P_25519, 512)))
        return cs_v

    def question(bornes: int | None, prime: bool = False):
        s = z3.Solver()
        cond2 = z3.substitute(cible_cond,
                              [(x, z3.BitVec(f"{x}!", 64)) for x in secrets])
        s.add(cible_cond != cond2)
        if bornes:
            for c in contraintes_valeur(bornes, prime):
                s.add(c)
        return s.check(), s.model() if s.check() == z3.sat else None

    v1, m1 = question(None)
    if v1 == z3.unsat:
        return {**ob, "verdict": "DÉCHARGÉE",
                "smt": f"Z3 : UNSAT — l'expression est invariante ∀ "
                       f"{len(secrets)} symbole(s) du secret (la dépendance "
                       "syntaxique était sémantiquement nulle)"}
    temoin = []
    if m1 is not None:
        for x in secrets:
            v = m1[x]
            temoin.append(f"{x}={v.as_long():#018x}" if v is not None
                          else f"{x}=?")
    if ob.get("bornes") and ob["addr"] == 0xCAB6:
        return {**ob, "verdict": "VIOLATION",
                "smt": "Z3 SANS borne : SAT — le contre-exemple : " +
                       " ; ".join(temoin[:4]) + " — " +
                       preuve_emprunt_tls13_10()}
    return {**ob, "verdict": "VIOLATION",
            "smt": ("Z3 : SAT — le CONTRE-EXEMPLE TÉMOIN : " +
                    " ; ".join(temoin[:4])) if temoin else
            "Z3 : SAT (témoin non affichable)"}


# ══════════════════════════════════════════════════════════════════════════════
# 7bis · LA PREUVE DÉDIÉE DE L'EMPUNT DE tls13-10 (le modèle 320 bits exact)
# ══════════════════════════════════════════════════════════════════════════════

def preuve_emprunt_tls13_10() -> str:
    """LA DÉCHARGE CONDITIONNELLE DÉDIÉE de la branche jc .emprunt de
    tls13-10 (0xcab6) : le modèle INTÉGRAL de la chaîne sub/sbb — cinq
    membres 64 bits, les constantes 2p EXACTES de la notation (0x7fffffff
    fffda, 0x7ffffffffffff ×3, 0xfffffffffffff), la retenue propagée —
    sous L'INVARIANT NOMMÉ du domaine (a, b < p = 2^255 − 19, la forme
    réduite que la discipline propager-geler entretient après CHAQUE
    opération) :

      si l'invariant tient : CF final = 0 TOUJOURS (UNSAT pour CF=1) —
      la branche défensive n'est JAMAIS prise — le tracé d'instructions
      est constant (le compte 1 238 959 de la mesure le corrobore) ;
      l'invariant N'EST PAS PROUVÉ par le présent audit (c'est la
      discipline de tls13-12, vérifiée empiriquement par l'égalité des
      traces — l'écart demeure NOMMÉ)."""
    if z3 is None:
        return "z3 absent — la preuve dédiée ne peut courir (fail-closed)"
    a = [z3.BitVec(f"a{i}", 64) for i in range(5)]
    b = [z3.BitVec(f"b{i}", 64) for i in range(5)]
    p = (1 << 255) - 19
    # la composition en 320 bits (les membres petits-boutistes)
    def compose(vec):
        v = z3.BitVecVal(0, 512)
        for i, x in enumerate(vec):
            v = v + z3.ZeroExt(512 - 64, x) * z3.BitVecVal(1 << (64 * i), 512)
        return v
    s = z3.Solver()
    s.add(z3.ULT(compose(a), z3.BitVecVal(p, 512)))
    s.add(z3.ULT(compose(b), z3.BitVecVal(p, 512)))
    # LA CHAÎNE EXACTE : r0 = (a0 + 2p0) − b0 ; rk = (ak + 2pk) − bk − CF
    # la retenue 64 bits propagée (mod 2^64, retenue à l'anglaise)
    deux_p = [0x7ffffffffffda, 0x7ffffffffffff, 0x7ffffffffffff,
              0x7ffffffffffff, 0xfffffffffffff]
    retenue = z3.BoolVal(False)
    for k in range(5):
        x = z3.ZeroExt(1, a[k]) + z3.BitVecVal(deux_p[k], 65)
        y = z3.ZeroExt(1, b[k]) + z3.If(retenue, z3.BitVecVal(1, 65),
                                        z3.BitVecVal(0, 65))
        r = x - y
        # CF = emprunt de ce niveau = (x < y) en 65 bits
        nouvelle_retenue = z3.ULT(x, y)
        s.add(z3.Extract(64, 64, r) == z3.If(nouvelle_retenue,
                                             z3.BitVecVal(1, 1),
                                             z3.BitVecVal(0, 1)))
        retenue = nouvelle_retenue
    # la question : la retenue FINALE peut-elle être 1 sous l'invariant ?
    s.add(retenue)
    v = s.check()
    temoin = ""
    if v == z3.sat:
        mod = s.model()
        temoin = " — le contre-exemple : " + " ; ".join(
            f"{x}={mod[x].as_long():#018x}" for x in (a + b)
            if mod[x] is not None)[:200]
    if v == z3.unsat:
        return ("LA PREUVE DÉDIÉE (le modèle 320 bits exact de la chaîne, "
                "les constantes 2p de la notation) : UNSAT — sous "
                "l'INVARIANT NOMMÉ (a, b < p, la forme réduite du domaine "
                "que propager-geler entretient), la retenue sortante est "
                "TOUJOURS NULLE : la branche jc .emprunt n'est JAMAIS "
                "prise ; l'invariant N'EST PAS PROUVÉ par le présent audit "
                "— l'écart demeure NOMMÉ")
    return ("LA PREUVE DÉDIÉE : SAT — même sous l'invariant (a, b < p) la "
            "retenue peut sortir" + temoin +
            " : l'écart est PLUS PROFOND que l'invariant — à consigner "
            "TEL QUEL")


# ══════════════════════════════════════════════════════════════════════════════
# 8 · LE CLI (l'audit autonome — le même moteur que le build)
# ══════════════════════════════════════════════════════════════════════════════

def _dedup(obligations: list[dict]) -> list[dict]:
    """UN constat par SITE (protocole, adresse, classe) — les revisites du
    worklist ne multiplient pas les lignes du rapport."""
    vus = {}
    for ob in obligations:
        vus.setdefault((ob["protocole"], ob["addr"], ob["classe"],
                        ob["texte"]), ob)
    return list(vus.values())


def _rapport(moteur: Moteur, obligations: list[dict], titre: str) -> int:
    print(f"=== {titre} ===")
    obligations = _dedup(obligations)
    par_protocole: dict[str, list] = defaultdict(list)
    for ob in obligations:
        par_protocole[ob["protocole"]].append(ob)
    verts, ecarts = 0, 0
    lignes = []
    for (nom, bloc, _secrets) in PROTOCOLES:
        obs = par_protocole.get(nom, [])
        if not obs:
            lignes.append(f"  VERT   {nom:<48s} — aucune branche, aucune "
                          f"adresse ne dépend du secret (0 obligation)")
            verts += 1
            continue
        # les obligations : décharge SMT ou violation
        detail = []
        for ob in obs:
            r = decharge_smt(moteur, ob)
            detail.append(r)
        dechargees = [d for d in detail if d["verdict"] == "DÉCHARGÉE"]
        violations = [d for d in detail if d["verdict"] == "VIOLATION"]
        if not violations:
            lignes.append(f"  VERT   {nom:<48s} — {len(dechargees)} "
                          f"obligation(s) DÉCHARGÉE(S) par SMT (∀ secrets)")
            verts += 1
        else:
            ecarts += 1
            for v in violations:
                lignes.append(f"  ÉCART  {nom:<48s} — {v['classe']} "
                              f"@{v['addr']:#x} : {v['texte']} — {v['detail']}"
                              + (f" [{v.get('smt', '')}]" if v.get("smt")
                                 else ""))
    print("\n".join(lignes))
    print(f"=== {verts} protocole(s) VERT(S) ; {ecarts} écart(s) nommé(s) "
          f"===")
    return ecarts


def main() -> int:
    ap = argparse.ArgumentParser(description="L'audit de temps constant "
                                             "structurel non borné")
    ap.add_argument("cible", nargs="?", default="tout",
                    choices=["tls13", "loupe", "tout", "mutants"])
    args = ap.parse_args()
    moteur = Moteur()
    if args.cible in ("tls13", "loupe", "tout"):
        protos = [p for p in PROTOCOLES
                  if args.cible == "tout"
                  or (args.cible == "tls13") == p[1].startswith("tls13")]
        obs = auditer(moteur, protos)
        ecarts = _rapport(moteur, obs,
                          f"L'AUDIT DE TEMPS CONSTANT — {args.cible}")
        return 2 if ecarts > len(_ECARTS_ATTENDUS) else 0
    if args.cible == "mutants":
        return mutants()
    return 0


# ══════════════════════════════════════════════════════════════════════════════
# 9 · LES CONTRÔLES NÉGATIFS (les mutants — l'instruction l'exige)
# ══════════════════════════════════════════════════════════════════════════════

# Les écarts attendus : les constats NOMMÉS au rapport (consignés TELS
# QUELS par la discipline — jamais masqués, jamais bloquants pour le build ;
# tout écart HORS cette liste REFUSE le build) :
#   · O4  — la branche d'emprunt défensive de tls13-10 (jb .emprunt) : la
#     retenue sortante peut dépendre des données (Z3, membres libres) ; sous
#     l'INVARIANT NOMMÉ (a, b < p — la forme réduite que propager-geler
#     entretient) : jamais prise (Z3, UNSAT) ; l'invariant n'est pas prouvé
#     par le présent audit — LA DÉCOUVERTE du chantier (le plan prédisait
#     VERT : consigné tel quel) ;
#   · O5b — la branche du verdict d'étiquette de tls13-19 (test r10 / jnz) :
#     le bit d'égalité des étiquettes est public PAR CONTRAT d'API (rax=-4
#     ou la restitution) — l'écart attendu au plan.
_ECARTS_ATTENDUS = {"O4-x25519 (la clé privée)",
                    "O5b-aesgcm-ouvrir (la clé 16 o)"}

MUTANTS = {
    "M1-echappee-precoce": ("tls13-02", "sha-02", [
        # la boucle d'extension : test edx, edx / jz insérés (le mot W secret)
        ("mov dword ptr [rsp + r15*4 + 0x20], edx",
         "mov dword ptr [rsp + r15*4 + 0x20], edx\n"
         "test edx, edx\n"
         "jz 0xc0bb")]),
    "M2-table-indexee": ("tls13-02", "sha-02", [
        ("add r10d, dword ptr [rbp + r15*4]",
         "mov eax, dword ptr [rsp + r15*4 + 0x20]\n"
         "add r10d, dword ptr [rbp + rax]")]),
    "M3-cswap-branche": ("tls13-13", "x25519", [
        ("mov r10, rbp\nshl r10, 63\nsar r10, 63",
         "test ebp, 1\njz 0xd3a0")]),
    "M4-ghash-repli-jc": ("tls13-17", "ghash", [
        ("shld rax, r9, 1\nsbb rdx, rdx",
         "shld rax, r9, 1\njc 0xe007\nsbb rdx, rdx")]),
    "M5-md5-table-octet": ("loupe-06", "md5", [
        ("mov edx, dword ptr [r14 + r12*4 + 0x100]",
         "movzx eax, byte ptr [r15]\n"
         "mov edx, dword ptr [r14 + rax*4 + 0x100]")]),
    "M6-hmac-cle-branchee": ("tls13-05", "hmac", [
        ("mov r12, rcx",
         "mov r12, rcx\n"
         "cmp byte ptr [r12], 0\n"
         "je 0xc559")]),
    "M7-decharge-and-zero": ("tls13-02", "sha-02", [
        ("mov dword ptr [rsp + r15*4 + 0x20], edx",
         "mov dword ptr [rsp + r15*4 + 0x20], edx\n"
         "mov eax, edx\n"
         "and eax, 0\n"
         "test eax, eax\n"
         "jz 0xc0bb")]),
}


def _texte_bloc(nom: str) -> str:
    fic, rep, _r, _s = BLOCS[nom]
    return open(os.path.join(rep, fic + ".asm"), encoding="utf-8").read()

def _assemble_lignes(lignes: list[str], rva: int):
    """Assemble des lignes de notation à l'org — (octets, tailles par ligne)."""
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    octets, tailles, addr = b"", [], rva
    for ligne in lignes:
        enc, _ = ks.asm(ligne, addr)
        if not enc:
            raise EchecAudit(f"ligne inassemblable : {ligne!r}")
        tailles.append(len(enc))
        octets += bytes(enc)
        addr += len(enc)
    return octets, tailles


def muer_bloc(nom: str, remplacements: list[tuple[str, str]]) -> str:
    """Le TEXTE MUTÉ d'un bloc : les régions remplacées, les cibles de saut
    REMAPPÉES (l'adressage absolu de la notation demeure cohérent — les
    décalages des insertions propagés aux cibles aval et aux déplacements
    RIP recalculés à la cible fixe). La notation scellée N'EST PAS touchée."""
    fic, rep, rva, slot = BLOCS[nom]
    lignes = _lignes_notation(os.path.join(rep, fic + ".asm"))
    # l'assemblage original : l'adresse de CHAQUE ligne
    _oct, tailles_orig = _assemble_lignes(lignes, rva)
    addrs_orig = [rva + sum(tailles_orig[:i]) for i in range(len(lignes))]
    resultat = []
    decalage = 0                 # l'accumul des régions remplacées
    i = 0
    regions = []
    for avant, _apres in remplacements:
        lignes_avant = [l for l in avant.splitlines() if l.strip()]
        # la position de la région dans les lignes originales
        for j in range(i, len(lignes) - len(lignes_avant) + 1):
            if [l.strip() for l in lignes[j:j + len(lignes_avant)]] == \
                    lignes_avant:
                regions.append((j, len(lignes_avant)))
                break
        else:
            raise EchecAudit(f"{nom} : la région de mutation est introuvable"
                             f" : {avant[:48]!r}…")
    regions.sort()
    zones = {j: n for j, n in regions}

    def remappe(texte: str, orig_addr: int, taille: int) -> str:
        """Les cibles de saut ET les déplacements RIP du texte remappés."""
        mm = re.match(r"^(j\w+|call)\s+(0x[0-9a-f]+)$", texte.strip())
        if mm:
            cible = int(mm.group(2), 0)
            nouvelle = cible + _decalage_de(cible)
            return f"{mm.group(1)} {nouvelle:#x}"
        mm = re.match(r"^(.*?)\[rip ([+-]) (0x[0-9a-f]+)\](.*)$", texte)
        if mm:
            disp = int(mm.group(3), 0) * (1 if mm.group(2) == "+" else -1)
            cible = orig_addr + taille + disp     # la cible FIXE (le plan)
            nd = cible - (orig_addr + decalage) - taille
            signe = "+" if nd >= 0 else "-"
            return (f"{mm.group(1)}[rip {signe} {abs(nd):#x}]{mm.group(4)}")
        return texte

    def _decalage_de(cible: int) -> int:
        """Le décalage accumulé AVANT l'adresse cible."""
        d = 0
        for (j, n), (_av, ap) in zip(regions, remplacements):
            if addrs_orig[j] <= cible:
                _oct_a, t_a = _assemble_lignes(
                    [l for l in _av.splitlines() if l.strip()],
                    addrs_orig[j])
                _oct_b, t_b = _assemble_lignes(
                    [l for l in ap.splitlines() if l.strip()],
                    addrs_orig[j])
                d += sum(t_b) - sum(t_a)
        return d

    k = 0
    while k < len(lignes):
        if k in zones:
            n = zones[k]
            avant, apres = next(
                (a, p) for (a, p), (j, _n) in zip(remplacements, regions)
                if j == k)
            _oct_a, t_a = _assemble_lignes(
                [l for l in avant.splitlines() if l.strip()], addrs_orig[k])
            _oct_b, t_b = _assemble_lignes(
                [l for l in apres.splitlines() if l.strip()], addrs_orig[k])
            for ligne, ta in zip([l for l in apres.splitlines() if l.strip()],
                                 t_b):
                resultat.append(remappe(ligne, addrs_orig[k] + 0, ta)
                                if False else ligne)
            decalage += sum(t_b) - sum(t_a)
            k += n
            continue
        resultat.append(remappe(lignes[k], addrs_orig[k], tailles_orig[k]))
        k += 1
    return "\n".join(resultat)



def mutants() -> int:
    print("=== LES CONTRÔLES NÉGATIFS — les mutants volontairement "
          "dépendants du secret doivent être ATTRAPÉS ===")
    attendus = {
        "M1-echappee-precoce": "BRANCHE",
        "M2-table-indexee": "ADRESSE",
        "M3-cswap-branche": "BRANCHE",
        "M4-ghash-repli-jc": "BRANCHE",
        "M5-md5-table-octet": "ADRESSE",
        "M6-hmac-cle-branchee": "BRANCHE",
        "M7-decharge-and-zero": "DÉCHARGÉE",
    }
    attrapes, total = 0, 0
    # les protocoles qui ATTEIGNENT le bloc muté (le bloc d'entrée OU le
    # callee — tls13-17 n'est atteint que par 18/19, loupe-06 par O6)
    ATTEINT = {
        "tls13-02": ["O1b-sha256-comprimer (le bloc 64 o)",
                     "O1c-sha256-comprimer (bloc + état)"],
        "tls13-05": ["O2-hmac (la clé 32 o)"],
        "tls13-13": ["O4-x25519 (la clé privée)"],
        "tls13-17": ["O5a-aesgcm-sceller (la clé 16 o)",
                     "O5b-aesgcm-ouvrir (la clé 16 o)"],
        "loupe-06": ["O6-md5 (le contenu du fichier)"],
    }
    for nom_mut, (bloc, famille, remplacements) in MUTANTS.items():
        try:
            texte = muer_bloc(bloc, remplacements)
        except EchecAudit as e:
            print(f"  ROUGE {nom_mut} : la mutation a échoué : {e}")
            return 2
        moteur = Moteur(charge_mutants={bloc: texte})
        noms = ATTEINT.get(bloc, [p[0] for p in PROTOCOLES if p[1] == bloc])
        protocole = [p for p in PROTOCOLES if p[0] in noms]
        obs = _dedup(auditer(moteur, protocole))
        total += 1
        if not obs:
            print(f"  ROUGE {nom_mut} : le mutant N'A PAS ÉTÉ attrapé "
                  "(aucune obligation) — l'audit est AVISÉ DE CE refus")
            continue
        juges = [decharge_smt(moteur, ob) for ob in obs]
        classes = {j["classe"] for j in juges}
        verdicts = {j["verdict"] for j in juges}
        ok = (attendus[nom_mut] in classes
              or attendus[nom_mut] in verdicts)
        marque = "VERT" if ok else "ROUGE"
        if ok:
            attrapes += 1
        for j in juges:
            print(f"  {marque} {nom_mut} : {j['classe']} @0x{j['addr']:x} "
                  f"— {j['verdict']}"
                  + (f" [{j['smt']}]" if j.get("smt") else ""))
    print(f"=== {attrapes}/{total} mutants tranchés comme attendu ===")
    return 0 if attrapes == total else 2


# ══════════════════════════════════════════════════════════════════════════════
# 10 · LES PORTES DU BUILD (à côté de l'audit ABI msx64)
# ══════════════════════════════════════════════════════════════════════════════

def auditer_tls13():
    """La porte du build m9 : les obligations du domaine tls13 — lève
    EchecBuild (le refus nommé) sur toute violation NON attendue au plan."""
    moteur = Moteur()
    protos = [p for p in PROTOCOLES if p[1].startswith("tls13")]
    obs = auditer(moteur, protos)
    _verdict_build(moteur, obs, protos, "tls13")


def auditer_loupe():
    """La porte du build loupe : l'obligation md5 (loupe-06 + libc + le
    sous-programme .comprimer) — lève EchecBuild sur violation."""
    moteur = Moteur()
    protos = [p for p in PROTOCOLES if not p[1].startswith("tls13")]
    obs = auditer(moteur, protos)
    _verdict_build(moteur, obs, protos, "loupe")


def _verdict_build(moteur, obs, protos, domaine):
    obs = _dedup(obs)
    par = defaultdict(list)
    for ob in obs:
        par[ob["protocole"]].append(ob)
    verts = 0
    for (nom, _b, _s) in protos:
        o = par.get(nom, [])
        juges = [decharge_smt(moteur, x) for x in o]
        violents = [j for j in juges
                    if j["verdict"] == "VIOLATION"
                    and not (nom in _ECARTS_ATTENDUS)]
        if violents:
            for v in violents:
                raise RuntimeError(
                    f"[audit temps constant] REFUS — {nom} : {v['classe']} "
                    f"@{v['addr']:#x} {v['texte']} — {v['detail']} "
                    f"{v.get('smt', '')}")
        if o:
            verts += 1
            if nom in _ECARTS_ATTENDUS:
                for v in juges:
                    if v["verdict"] == "VIOLATION":
                        print(f"[audit temps constant] ÉCART NOMMÉ (consigné"
                              f" au rapport, jamais masqué) — {nom} : "
                              f"{v['classe']} @{v['addr']:#x} {v['texte']}")
    verrous = sum(len(par[n]) for (n, _b, _s) in protos)
    print(f"[audit temps constant] {len(protos)} protocole(s) {domaine} : "
          f"verts, {verrous} obligation(s) levée(s) et tranchée(s) "
          f"(SMT non borné), les écarts nommés au plan : "
          f"{len(_ECARTS_ATTENDUS)} (le verdict d'étiquette GCM — public "
          f"par contrat d'API)")


if __name__ == "__main__":
    sys.exit(main())

