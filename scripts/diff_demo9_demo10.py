#!/usr/bin/env python3
"""D66 (suite) — Diff binaire demo.9 (73c064fb) vs demo10-diagnostique (cf72462d)
+ lecture des paramètres de pile/sections du PE.

Cartographie chaque zone divergente sur la carte des blocs (demo/layout.py)
pour répondre : QUELLES blocs D43 a-t-il modifiés en retirant les sondes ?
"""
import difflib
import importlib.util
import pathlib
import sys

import pefile

REPO = pathlib.Path("/home/z/my-project/triade")
D9 = REPO / "demo" / "demo.exe"
D10 = REPO / "demo" / "livraison" / "demo10-diagnostique.exe"

spec = importlib.util.spec_from_file_location("layout_demo", REPO / "demo" / "layout.py")
L = importlib.util.module_from_spec(spec)
spec.loader.exec_module(L)

b9 = open(D9, "rb").read()
b10 = open(D10, "rb").read()
print(f"demo.9  : {len(b9)} o   demo10 : {len(b10)} o")

# --- 1) en-têtes PE : pile, sections ---------------------------------------
for nom, chemin in (("demo.9", D9), ("demo10", D10)):
    pe = pefile.PE(str(chemin))
    oh = pe.OPTIONAL_HEADER
    print(f"\n[{nom}] SizeOfStackReserve=0x{oh.SizeOfStackReserve:X} "
          f"SizeOfStackCommit=0x{oh.SizeOfStackCommit:X} "
          f"SizeOfHeapCommit=0x{oh.SizeOfHeapCommit:X}")
    for s in pe.sections:
        print(f"    {s.Name.decode().rstrip(chr(0)):8} VA=0x{s.VirtualAddress:06X} "
              f"VS=0x{s.Misc_VirtualSize:06X} raw=0x{s.PointerToRawData:06X}/0x{s.SizeOfRawData:06X} "
              f"carac=0x{s.Characteristics:08X}")

# --- 2) zones divergentes ----------------------------------------------------
print("\n--- zones divergentes (plages d'octets fichier) ---")
sm = difflib.SequenceMatcher(None, b9, b10, autojunk=False)
ops = [op for op in sm.get_opcodes() if op[0] != "equal"]
for tag, i1, i2, j1, j2 in ops:
    print(f"{tag:8} demo.9 [{i1:#06x}..{i2:#06x}] ({i2 - i1:4} o)  "
          f"demo10 [{j1:#06x}..{j2:#06x}] ({j2 - j1:4} o)")

# --- 3) cartographie sur les blocs (offset fichier ≈ RVA - 0x1400 pour .text2)
BLOCS = list(getattr(L, "BLOCS_WIN", [])) + list(getattr(L, "BLOCS_SUP", []))
print("\n(la cartographie précise sera faite sur les RVA .text2 0x4000-0x53FF)")
