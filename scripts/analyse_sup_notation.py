#!/usr/bin/env python3
"""analyse_sup_notation.py — Extrait la structure des notations terrain.

Pour chaque bloc sup-*.asm de terrain/notation/ : assemble (keystone),
désassemble (capstone), puis liste :
  - appels IAT (call [rip+X] -> adresse résolue -> nom IAT)
  - appels directs (call 0x... / jmp 0x... externes)
  - références RIP de données (hors call)
Sert à dériver les tables d'autorisation (I1/I2) de build_terrain.py.
"""
from __future__ import annotations

import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
TERRAIN = os.path.join(os.path.dirname(ICI), "terrain")
sys.path.insert(0, TERRAIN)

import importlib.util as ilu
_spec = ilu.spec_from_file_location("layout_terrain", os.path.join(TERRAIN, "layout.py"))
L = ilu.module_from_spec(_spec)
_spec.loader.exec_module(L)

import capstone
from keystone import Ks, KS_ARCH_X86, KS_MODE_64

ks = Ks(KS_ARCH_X86, KS_MODE_64)
cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

# (fichier, rva, slot) — d'après layout.BLOCS_TERRAIN
BLOCS = {f: (rva, slot) for _, _, f, rva, slot in
         [(b[0], b[1], b[2], b[3], b[4]) for b in []]}

# reconstruire depuis auteur.py BLOCS (fichier, bid, spec, rva, slot)
sys.path.insert(0, os.path.join(TERRAIN, "outils"))
import importlib
auteur = importlib.import_module("auteur")

SLOTS_IAT = {v: k for k, v in L.IAT_SLOTS.items()}


def assembler(chemin, rva):
    instructions = []
    with open(chemin, encoding="utf-8") as f:
        for brut in f.read().splitlines():
            ligne = brut.split(";")[0].strip()
            if ligne and not ligne.startswith(";"):
                instructions.append(ligne)
    octets = b""
    adresse = rva
    for ligne in instructions:
        enc, _ = ks.asm(ligne, adresse)
        if not enc:
            raise SystemExit(f"inassemblable : {ligne!r}")
        octets += bytes(enc)
        adresse += len(enc)
    return octets


print("=== structure réelle des notations terrain ===\n")
rapport = {}
for fichier, bid, spec, rva, slot, _deps in auteur.BLOCS:
    chemin = os.path.join(TERRAIN, "notation", fichier + ".asm")
    code = assembler(chemin, rva)
    insns = list(cs.disasm(code, rva))
    iat, directs, donnees = set(), set(), set()
    for i in insns:
        if i.mnemonic == "call":
            if "rip" in i.op_str:
                m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", i.op_str)
                disp = int(m.group(2), 16) * (1 if m.group(1) == "+" else -1)
                cible = i.address + i.size + disp
                iat.add(SLOTS_IAT.get(cible, hex(cible)))
            elif i.op_str.startswith("0x"):
                cible = int(i.op_str, 16)
                if rva <= cible < rva + slot:
                    pass  # interne
                else:
                    directs.add(cible)
        elif i.mnemonic == "jmp" and i.op_str.startswith("0x"):
            cible = int(i.op_str, 16)
            if not (rva <= cible < rva + slot):
                directs.add(cible)
        else:
            if "rip" in i.op_str:
                m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", i.op_str)
                if m:
                    disp = int(m.group(2), 16) * (1 if m.group(1) == "+" else -1)
                    cible = i.address + i.size + disp
                    if cible >= L.IMAGE_BASE:
                        cible -= L.IMAGE_BASE
                    donnees.add(cible)
    rapport[fichier] = (iat, directs, donnees)
    print(f"--- {fichier} ({bid}) @0x{rva:x} ---")
    print(f"  IAT     : {sorted(iat, key=str)}")
    print(f"  directs : {[hex(d) for d in sorted(directs)]}")
    print(f"  donnees : {[hex(d) for d in sorted(donnees)]}")
    print()

# correspondance adresses -> noms symboliques
NOMS = {}
for nom, adr in auteur.SYMBOLES.items():
    NOMS.setdefault(adr, nom)
for nom, (adr, _t, _n) in L.CHAINES_SUP.items():
    NOMS.setdefault(adr, "SUP:" + nom)
for nom, (adr, _o, _n) in L.CHAINES_ASCII.items():
    NOMS.setdefault(adr, "ASCII:" + nom)
for nom, (adr, _t, _n) in L.CHAINES_UTF16.items():
    NOMS.setdefault(adr, "U16:" + nom)

print("=== données avec noms symboliques ===\n")
for fichier, (iat, directs, donnees) in rapport.items():
    nommes = sorted((hex(d), NOMS.get(d, "?")) for d in donnees)
    print(f"--- {fichier} ---")
    for a, n in nommes:
        print(f"  {a} {n}")
    print()
