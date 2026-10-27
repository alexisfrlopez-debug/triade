#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIADE D62 — Identification précise des 4 sites défectueux (D=0x8) dans
sup-31/sup-34 du superviseur terrain.9 : résolution IAT (nom d'API), contexte
désassemblé, structure de la fonction englobante (où est le ret ? que se
passe-t-il entre le call défectueux et le ret ?).
"""

import pathlib
import sys

import capstone
import pefile

REPO = pathlib.Path(__file__).resolve().parents[1]
EXE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else
                   REPO / "terrain" / "livraison" / "superviseur-terrain9.exe")
BASE = 0x140000000

SITES = [0x5382, 0x5d3c, 0x5d4c, 0x5d55]

data = EXE.read_bytes()
pe = pefile.PE(str(EXE), fast_load=True)
pe.parse_data_directories(
    directories=[pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_IMPORT']])

# --- table IAT : rva du slot -> nom -----------------------------------------
iat = {}
for desc in pe.DIRECTORY_ENTRY_IMPORT:
    for imp in desc.imports:
        if imp.address:
            iat[imp.address] = imp.name.decode() if imp.name else f"ord{imp.ordinal}"

md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = False


def rva_to_off(rva):
    for s in pe.sections:
        if s.VirtualAddress <= rva < s.VirtualAddress + s.Misc_VirtualSize:
            return s.PointerToRawData + (rva - s.VirtualAddress)
    raise ValueError(rva)


def disasm_zone(lo, hi, marqueurs=()):
    off = rva_to_off(lo)
    out = []
    for ins in md.disasm(data[off:off + (hi - lo)], BASE + lo):
        rva = ins.address - BASE
        note = ""
        if ins.mnemonic == "call" and "rip" in ins.op_str:
            # call [rip + disp] : cible = fin d'instruction + disp
            fin = ins.address + ins.size
            disp = int(ins.op_str.split("[rip")[1].strip(" +-]").lstrip("+ -")
                       .replace("]", ""), 0) if True else 0
            # op_str : "qword ptr [rip - 0x3a32]"
            txt = ins.op_str.split("rip")[1].strip(" ]")
            sign = -1 if txt.strip().startswith("-") else 1
            disp = sign * int(txt.strip().lstrip("+- ").strip(), 16)
            cible = fin - BASE + disp
            nom = iat.get(cible, f"slot@{cible:#x}?")
            note = f"   ; → {nom}"
        m = " ◀◀◀ DÉFAUT D=0x8" if rva in marqueurs else ""
        out.append(f"  {rva:#06x}: {ins.bytes.hex():<20} {ins.mnemonic} "
                   f"{ins.op_str}{note}{m}")
    return out


print("=" * 78)
print("[1] sup-31 — zone du défaut @0x5382 (contexte 0x5330-0x53C0)")
print("=" * 78)
for l in disasm_zone(0x5330, 0x53C0, {0x5382}):
    print(l)

print()
print("=" * 78)
print("[2] sup-34 — zone des défauts @0x5d3c/0x5d4c/0x5d55 (0x5CC0-0x5DC0)")
print("=" * 78)
for l in disasm_zone(0x5CC0, 0x5DC0, {0x5d3c, 0x5d4c, 0x5d55}):
    print(l)
