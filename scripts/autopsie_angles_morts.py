#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIADE D52f — les trois angles morts restants :
  1. disassemblage COMPLET de sup-21 (0x1c40..0x1e60) et du helper 0x1cfb ;
  2. tous les appels indirects VIA REGISTRE (call/jmp rXX, FF D0-E7) dans
     .text et .text2 -> d'ou vient le pointeur appele ? ;
  3. tous les appels indirects de .text2 (le scan precedent etait tronque) ;
  4. demo : sections + .rsrc present ?
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
    _, nsec, _, _, _, opt_sz, _ = struct.unpack_from("<HHIIIHH", d, coff)
    opt = coff + 20
    imp_rva = struct.unpack_from("<I", d, opt + 120)[0]
    rsrc_rva, rsrc_sz = struct.unpack_from("<II", d, opt + 128)
    secs = []
    so = opt + opt_sz
    for i in range(nsec):
        o = so + 40 * i
        nom = d[o:o + 8].rstrip(b"\x00").decode("ascii", "replace")
        vs, va, rs, ra = struct.unpack_from("<IIII", d, o + 8)
        fl = struct.unpack_from("<I", d, o + 36)[0]
        secs.append((nom, va, vs, ra, rs, fl))
    return d, imp_rva, (rsrc_rva, rsrc_sz), secs


def rva2off(secs, rva):
    for nom, va, vs, ra, rs, _ in secs:
        if va <= rva < va + max(vs, rs):
            return ra + (rva - va)
    return None


d, imp_sup, rsrc_sup, secs = pe_info(SUP)
d_dem, imp_dem, rsrc_dem, secs_dem = pe_info(DEM)

print("=== sections DEMO vs SUPERVISEUR ===")
print("demo :")
for s in secs_dem:
    print(f"  {s[0]:<8} VA={s[1]:#06x} VS={s[2]:#06x} RAW={s[3]:#06x} RS={s[4]:#06x} fl={s[5]:#010x}")
print("superviseur :")
for s in secs:
    print(f"  {s[0]:<8} VA={s[1]:#06x} VS={s[2]:#06x} RAW={s[3]:#06x} RS={s[4]:#06x} fl={s[5]:#010x}")
print(f"demo .rsrc dir : {rsrc_dem[0]:#x} taille {rsrc_dem[1]:#x}")
print(f"sup  .rsrc dir : {rsrc_sup[0]:#x} taille {rsrc_sup[1]:#x}")

# slots couverts
couverts = {}
off = rva2off(secs, imp_sup)
n = 0
while True:
    oft, _, _, nomrva, ft = struct.unpack_from("<IIIII", d, off + 20 * n)
    if oft == nomrva == ft == 0:
        break
    dll = d[rva2off(secs, nomrva):].split(b"\x00")[0].decode()
    i = 0
    while True:
        val = struct.unpack_from("<Q", d, rva2off(secs, oft + 8 * i))[0]
        if val == 0:
            break
        no = rva2off(secs, val)
        fname = d[no + 2:].split(b"\x00")[0].decode("ascii", "replace")
        couverts[ft + 8 * i] = f"{dll}!{fname}"
        i += 1
    n += 1

md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = False

# ---------- 1. sup-21 complet ----------
print("\n=== sup-21 COMPLET (0x1c40..0x1e60) ===")
ra = rva2off(secs, 0x1c40)
code = d[ra:ra + 0x220]
for ins in md.disasm(code, 0x1c40):
    extra = ""
    if "[rip" in ins.op_str:
        p = ins.op_str.find("0x")
        try:
            base = int(ins.op_str[p:ins.op_str.find("]")].rstrip("]"), 16)
        except ValueError:
            base = 0
        cible = ins.address + ins.size + base
        zone = next((s[0] for s in secs if s[1] <= cible < s[1] + max(s[2], s[4])), "HORS")
        extra = f"   -> {cible:#06x} ({zone}) {couverts.get(cible, '')}"
    print(f"  {ins.address:#07x}: {ins.mnemonic:<10} {ins.op_str:<42}{extra}")

# ---------- 2. appels via registre ----------
print("\n=== appels/jmps via REGISTRE (FF /2 /4 avec modrm D0-F7) ===")
segments_exec = [(nom, va, vs, ra, rs) for nom, va, vs, ra, rs, fl in secs
                 if fl & 0x20000000]
regcalls = []
for nom, va, vs, ra, rs in segments_exec:
    code = d[ra:ra + rs]
    for ins in md.disasm(code, va):
        # call rXX = FF D0..D7 ; call r8-r15 = 41 FF D0..D7
        # jmp rXX = FF E0..E7
        octs = ins.bytes
        if len(octs) >= 2 and octs[0] in (0xFF,) and 0xD0 <= octs[1] <= 0xF7 and octs[1] < 0xE8:
            regcalls.append((ins.address, f"{ins.mnemonic} {ins.op_str}", nom))
        elif (len(octs) >= 3 and octs[0] == 0x41 and octs[1] == 0xFF
                and 0xD0 <= octs[2] <= 0xD7):
            regcalls.append((ins.address, f"{ins.mnemonic} {ins.op_str}", nom))
print(f"  {len(regcalls)} appels via registre trouves")
for ad, t, s in regcalls:
    print(f"    {ad:#07x} [{s}] {t}")

# ---------- 3. tous les appels indirects .text2 ----------
print("\n=== appels [rip+X] dans .text2 ===")
ra2 = rva2off(secs, 0x4000)
vs2 = next(s[2] for s in secs if s[0] == ".text2")
code2 = d[ra2:ra2 + vs2]
n2 = 0
for ins in md.disasm(code2, 0x4000):
    if ins.mnemonic in ("call", "jmp") and "[rip" in ins.op_str:
        p = ins.op_str.find("0x")
        try:
            base = int(ins.op_str[p:ins.op_str.find("]")].rstrip("]"), 16)
        except ValueError:
            base = 0
        cible = ins.address + ins.size + base
        statut = couverts.get(cible, "*** NON COUVERT ***")
        zone = next((s[0] for s in secs if s[1] <= cible < s[1] + max(s[2], s[4])), "HORS")
        print(f"  {ins.address:#07x} {ins.mnemonic:<5} {ins.op_str:<32} -> {cible:#06x} ({zone}) {statut}")
        n2 += 1
print(f"  total : {n2}")

# ---------- 4. contenu des trous IAT 0x2348..0x2360 ----------
print("\n=== octets a .rdata 0x2340..0x2380 (trou entre FT #4 et #5) ===")
o = rva2off(secs, 0x2340)
for i in range(0, 0x40, 8):
    v = struct.unpack_from("<Q", d, o + i)[0]
    print(f"  0x{0x2340 + i:#06x}: {v:#018x}")
