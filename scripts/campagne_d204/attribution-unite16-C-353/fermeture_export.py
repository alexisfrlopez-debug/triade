#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fermeture_export.py — LA FERMETURE DE L'EXPORT (l'analyse pure-fichier, v4 :
le MNEMONIQUE mené, l'opérande cible, les thunks résolus). La fermeture
appelante de loupe_16_saisie et la LISTE NOMMÉE des feuilles IAT."""
import re
import subprocess
import sys

DLL = sys.argv[1] if len(sys.argv) > 1 else "loupe-16-d210-c-mingw.dll"
BASE = 0x25BFA0000
EXPORT_RVA = 0x1420

out = subprocess.run(["objdump", "-d", DLL], capture_output=True, text=True).stdout
instrs = {}
sym = {}
pat = re.compile(r"^\s+([0-9a-f]+):\t([0-9a-f ]+)\t(\S+)\s*(.*)$")
for line in out.splitlines():
    m = pat.match(line)
    if m:
        a = int(m.group(1), 16)
        op = m.group(4).strip()
        instrs[a] = (m.group(3), op, m.group(2))
        s = re.search(r"<([^>]+)>$", op)
        if s:
            sym[a] = s.group(1)
adresses = sorted(instrs)
IAT_LO, IAT_HI = BASE + 0x9100, BASE + 0x91b8


def nxt(a):
    i = adresses.index(a)
    return adresses[i + 1] if i + 1 < len(adresses) else None


HEX = re.compile(r"^(?:0x)?([0-9a-f]+)")
atteints = set()
iat = {}
thunks = {}
pile = [BASE + EXPORT_RVA]
while pile:
    a = pile.pop()
    while a is not None and a not in atteints and a in instrs:
        atteints.add(a)
        mn, op, raw = instrs[a]
        # toute adresse absolue (le commentaire # abs) tombant dans l'IAT
        for mm in re.finditer(r"(?:0x)?([0-9a-f]{10,})", op):
            v = int(mm.group(1), 16)
            if IAT_LO <= v < IAT_HI:
                iat[v] = sym.get(a, "?")
        if mn == "call":
            m = HEX.match(op)
            if m:
                pile.append(int(m.group(1), 16))
            a = nxt(a)
        elif mn == "jmp":
            if op.startswith("*"):
                # le thunk : jmp *off(%rip) # abs <__imp_X> — LA FEUILLE
                mm = re.search(r"#\s*([0-9a-f]+)\s+<__imp_([^>]+)>", op)
                if mm:
                    v = int(mm.group(1), 16)
                    if IAT_LO <= v < IAT_HI:
                        iat[v] = mm.group(2)
                        thunks[a] = (v, mm.group(2))
                break                      # le thunk finit le chemin
            m = HEX.match(op)
            if m:
                a = int(m.group(1), 16)
                continue
            break
        elif mn.startswith("j"):
            m = HEX.match(op)
            if m:
                pile.append(int(m.group(1), 16))
            a = nxt(a)
        elif mn in ("ret", "retq"):
            break
        else:
            a = nxt(a)

print(f"la fermeture de loupe_16_saisie : {len(atteints)} instructions atteintes")
print(f"les FEUILLES IAT appelées par la fermeture : {len(iat)}")
for v in sorted(iat):
    print(f"  le slot @+{v - BASE:#x} — {iat[v]}")
locaux = sorted({sym[a] for a in atteints if a in sym and "+" in sym[a] and "loupe_16_saisie" not in sym[a]})
print(f"les fonctions locales atteintes : {locaux}")
print(f"les thunks traversés : {[(hex(t[0]),) + t[1:] for t in thunks.values()]}")
