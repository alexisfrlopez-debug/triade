#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE — D97ter : comparaison bloc par bloc terrain16 vs terrain17-B.

sup-34 (T2 proxy, slot 0x5800 x 0x5C0) et sup-31 (lanceur, 0x5200 x 0x1C0)
extraits de CHAQUE exe via sa propre table de sections, puis :
  - diff octet ;
  - désassemblage capstone côte à côte des zones divergentes.
"""
import pathlib
import difflib

import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

A = pathlib.Path("/home/z/my-project/download/superviseur-terrain16.exe")
B = pathlib.Path("/home/z/my-project/download/superviseur-terrain17b.exe")

BLOCS = [
    ("sup-34 (T2)", 0x5800, 0x5C0),
    ("sup-31 (lanceur)", 0x5200, 0x1C0),
]


def extraire(path, rva, n):
    pe = pefile.PE(data=path.read_bytes(), fast_load=True)
    off = pe.get_offset_from_rva(rva)
    return path.read_bytes()[off:off + n], off


def desasm(buf, rva_base):
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = False
    out = []
    for ins in md.disasm(buf, rva_base):
        out.append(f"0x{ins.address:05X}: {ins.mnemonic} {ins.op_str}".rstrip())
    return out


for nom, rva, taille in BLOCS:
    ba, offa = extraire(A, rva, taille)
    bb, offb = extraire(B, rva, taille)
    print(f"\n===== {nom} — RVA 0x{rva:X} x {taille} o "
          f"(off fichier 16=0x{offa:X}, 17b=0x{offb:X}) =====")
    diffs = [i for i in range(taille) if ba[i] != bb[i]]
    if not diffs:
        print("  OCTET POUR OCTET IDENTIQUE")
        continue
    print(f"  {len(diffs)} octets divergents "
          f"(RVA 0x{rva + diffs[0]:X} .. 0x{rva + diffs[-1]:X})")
    # plages contiguës
    plages = []
    d0 = diffs[0]
    prev = diffs[0]
    for d in diffs[1:]:
        if d != prev + 1:
            plages.append((d0, prev))
            d0 = d
        prev = d
    plages.append((d0, prev))
    for s, e in plages:
        print(f"    plage RVA 0x{rva + s:05X}-0x{rva + e:05X} ({e - s + 1} o)")

    # diff désassemblé autour de la première plage divergente
    s = plages[0][0]
    lo = max(0, s - 0x40)
    hi = min(taille, plages[-1][1] + 0x40)
    la = desasm(ba[lo:hi], rva + lo)
    lb = desasm(bb[lo:hi], rva + lo)
    print("  --- diff désassemblé (contexte élargi) ---")
    for ligne in difflib.unified_diff(la, lb, lineterm="",
                                      fromfile="terrain16", tofile="terrain17b",
                                      n=3):
        if ligne.startswith(("---", "+++", "@@")):
            continue
        print(f"    {ligne}")
