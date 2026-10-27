#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIADE D52c — comparaison side-by-side superviseur vs demo : les call [rip+disp]
visent-ils des slots 8-alignes (demo, prouve terrain) ou impairs (superviseur) ?
"""

import pathlib
import struct

from capstone import Cs, CS_ARCH_X86, CS_MODE_64

SUP = pathlib.Path("/home/z/my-project/triade/terrain/superviseur.exe")
DEM = pathlib.Path("/home/z/my-project/triade/demo/demo.exe")


def pe_info(path):
    d = path.read_bytes()
    e = struct.unpack_from("<I", d, 0x3C)[0]
    coff = e + 4
    machine, nsec, _, _, _, opt_sz, _ = struct.unpack_from("<HHIIIHH", d, coff)
    opt = coff + 20
    entry = struct.unpack_from("<I", d, opt + 16)[0]
    secs = []
    so = opt + opt_sz
    for i in range(nsec):
        o = so + 40 * i
        nom = d[o:o + 8].rstrip(b"\x00").decode("ascii", "replace")
        vs, va, rs, ra = struct.unpack_from("<IIII", d, o + 8)
        fl = struct.unpack_from("<I", d, o + 36)[0]
        secs.append((nom, va, vs, ra, rs, fl))
    return d, entry, secs


def analyse(nom, path, bornes):
    d, entry, secs = pe_info(path)
    print(f"\n===== {nom} (entree {entry:#x}) =====")
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    ra = None
    for snom, va, vs, rao, rs, fl in secs:
        if va <= entry < va + vs:
            ra = rao + (entry - va)
            break
    code = d[ra:ra + 0x200]
    slots = []
    for ins in md.disasm(code, entry):
        if ins.mnemonic in ("call", "jmp") and "[rip" in ins.op_str:
            # extraire disp
            txt = ins.op_str
            p = txt.find("+")
            disp = int(txt[p + 1:txt.find("]")].strip(), 16) if p >= 0 else 0
            cible = ins.address + ins.size + disp
            aligne = "OK " if cible % 8 == 0 else "!!! IMPAIR"
            slots.append(cible)
            print(f"  {ins.address:#07x}: {ins.mnemonic:<5} {txt:<28} "
                  f"-> slot {cible:#06x}  {aligne}")
        elif ins.mnemonic == "call" and "qword" not in ins.op_str:
            print(f"  {ins.address:#07x}: call  {ins.op_str} (direct)")
    return slots


s_sup = analyse("SUPERVISEUR terrain.3 (crashe 0xC0000005)", SUP, None)
s_dem = analyse("DEMO 0.3.0 (prouve terrain, fonctionne)", DEM, None)

print("\n=== VERDICT ===")
print(f"superviseur : {len(s_sup)} appels indirects, "
      f"{sum(1 for s in s_sup if s % 8)} impairs")
print(f"demo        : {len(s_dem)} appels indirects, "
      f"{sum(1 for s in s_dem if s % 8)} impairs")
