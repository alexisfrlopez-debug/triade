#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIADE D52d — analyse de la fonction 0x1c40 (premier appel de l'entree
superviseur, absent de demo) + detail complet des 6 descripteurs d'import
(noms, slots, recouvrements) + comparaison avec la table de demo.
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
    entry = struct.unpack_from("<I", d, opt + 16)[0]
    imp_rva, imp_sz = struct.unpack_from("<II", d, opt + 120)
    secs = []
    so = opt + opt_sz
    for i in range(nsec):
        o = so + 40 * i
        nom = d[o:o + 8].rstrip(b"\x00").decode("ascii", "replace")
        vs, va, rs, ra = struct.unpack_from("<IIII", d, o + 8)
        fl = struct.unpack_from("<I", d, o + 36)[0]
        secs.append((nom, va, vs, ra, rs, fl))
    return d, entry, imp_rva, imp_sz, secs


def rva2off(secs, rva):
    for nom, va, vs, ra, rs, _ in secs:
        if va <= rva < va + max(vs, rs):
            return ra + (rva - va)
    return None


def dump_imports(nom_f, d, imp_rva, secs):
    print(f"\n===== descripteurs d'import de {nom_f} =====")
    off = rva2off(secs, imp_rva)
    res = []
    n = 0
    while True:
        oft, _, _, nomrva, ft = struct.unpack_from("<IIIII", d, off + 20 * n)
        if oft == nomrva == ft == 0:
            break
        dll = d[rva2off(secs, nomrva):].split(b"\x00")[0].decode()
        print(f"  #{n} {dll}: OFT={oft:#x} FT={ft:#x}")
        walk = oft if ft == 0 else oft
        i = 0
        slots = []
        while True:
            o = rva2off(secs, walk + 8 * i)
            if o is None:
                print(f"     !! OFT+{i}: RVA {walk + 8 * i:#x} HORS SECTIONS")
                break
            val = struct.unpack_from("<Q", d, o)[0]
            if val == 0:
                break
            slot = ft + 8 * i
            if val >> 63:
                fname = f"ordinal#{val & 0xFFFF}"
            else:
                no = rva2off(secs, val)
                if no is None:
                    fname = f"!!RVA{val:#x} INVALIDE"
                else:
                    fname = d[no + 2:].split(b"\x00")[0].decode("ascii", "replace")
            zone = next((s[0] for s in secs if s[1] <= slot < s[1] + max(s[2], s[4])), "?")
            zone_oft = next((s[0] for s in secs if s[1] <= walk + 8 * i < s[1] + max(s[2], s[4])), "?")
            print(f"     slot {slot:#06x} ({zone:<7}) <- {fname:<34} [OFT en {zone_oft}]")
            slots.append((slot, fname))
            i += 1
            if i > 64:
                print("     !! >64 entrees, abandon")
                break
        res.append((dll, slots))
        n += 1
    return res


def desassembe(nom_f, d, secs, rva_debut, taille, titre):
    print(f"\n===== {titre} ({nom_f} @{rva_debut:#x}) =====")
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    ra = None
    for snom, va, vs, rao, rs, fl in secs:
        if va <= rva_debut < va + vs:
            ra = rao + (rva_debut - va)
            break
    if ra is None:
        print("  (RVA hors sections)")
        return
    code = d[ra:ra + taille]
    for ins in md.disasm(code, rva_debut):
        extra = ""
        if "[rip" in ins.op_str:
            p = ins.op_str.find("0x")
            try:
                base = int(ins.op_str[p:ins.op_str.find("]")].rstrip("]"), 16)
            except ValueError:
                base = 0
            cible = ins.address + ins.size + base
            zone = next((s[0] for s in secs if s[1] <= cible < s[1] + max(s[2], s[4])), "HORS")
            extra = f"   -> {cible:#06x} ({zone})"
        print(f"  {ins.address:#07x}: {ins.mnemonic:<9} {ins.op_str:<40}{extra}")


d_sup, e_sup, imp_sup, impsz_sup, secs_sup = pe_info(SUP)
d_dem, e_dem, imp_dem, impsz_dem, secs_dem = pe_info(DEM)

imp_sup_d = dump_imports("SUPERVISEUR", d_sup, imp_sup, secs_sup)
imp_dem_d = dump_imports("DEMO", d_dem, imp_dem, secs_dem)

# recouvrements FT/OFT dans superviseur
print("\n===== controle de recouvrements (superviseur) =====")
plages = []
for dll, slots in imp_sup_d:
    if slots:
        plages.append((slots[0][0], slots[-1][0] + 8, dll, "FT"))
# les OFT :
off = rva2off(secs_sup, imp_sup)
n = 0
while True:
    oft, _, _, nomrva, ft = struct.unpack_from("<IIIII", d_sup, off + 20 * n)
    if oft == nomrva == ft == 0:
        break
    dll = d_sup[rva2off(secs_sup, nomrva):].split(b"\x00")[0].decode()
    i = 0
    while struct.unpack_from("<Q", d_sup, rva2off(secs_sup, oft + 8 * i))[0] != 0:
        i += 1
    plages.append((oft, oft + 8 * i, dll, "OFT"))
    n += 1
plages.sort()
ok = True
for i in range(len(plages) - 1):
    if plages[i][1] > plages[i + 1][0]:
        print(f"  !! RECROUVREMENT : {plages[i]} chevauche {plages[i + 1]}")
        ok = False
if ok:
    print("  aucun recouvrement entre plages FT/OFT")
for p in plages:
    print(f"    {p[3]} {p[2]:<14} {p[0]:#06x}..{p[1]:#06x}")

desassembe("SUPERVISEUR", d_sup, secs_sup, 0x1c40, 0x130,
           "fonction 0x1c40 (premier appel de l'entree, ABSENT de demo)")
