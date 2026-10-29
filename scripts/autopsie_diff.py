#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIADE D52g — diff d'octets DEMO (prouve) vs SUPERVISEUR (crashe),
section par section + rescan ROBUSTE de .text2 (capstone relance apres
chaque octet indécodable) avec cibles corrigees (gestion du signe).
"""

import pathlib
import struct

from capstone import Cs, CS_ARCH_X86, CS_MODE_64

SUP = pathlib.Path("/home/z/my-project/triade/terrain/superviseur.exe")
DEM = pathlib.Path("/home/z/my-project/triade/demo/demo.exe")


def pe_sections(path):
    d = path.read_bytes()
    e = struct.unpack_from("<I", d, 0x3C)[0]
    coff = e + 4
    _, nsec, _, _, _, opt_sz, _ = struct.unpack_from("<HHIIIHH", d, coff)
    secs = {}
    so = coff + 20 + opt_sz
    for i in range(nsec):
        o = so + 40 * i
        nom = d[o:o + 8].rstrip(b"\x00").decode("ascii", "replace")
        vs, va, rs, ra = struct.unpack_from("<IIII", d, o + 8)
        secs[nom] = (va, vs, ra, rs)
    return d, secs


d_sup, s_sup = pe_sections(SUP)
d_dem, s_dem = pe_sections(DEM)

print("=== diff d'octets par section (demo vs superviseur) ===")
for nom in (".text", ".rdata", ".data", ".text2"):
    if nom not in s_dem or nom not in s_sup:
        print(f"  {nom}: absent d'un des deux")
        continue
    va_d, vs_d, ra_d, rs_d = s_dem[nom]
    va_s, vs_s, ra_s, rs_s = s_sup[nom]
    if va_d != va_s:
        print(f"  {nom}: VA differents demo={va_d:#x} sup={va_s:#x} — pas comparable")
        continue
    n = min(vs_d, vs_s, rs_d, rs_s)
    b_dem = d_dem[ra_d:ra_d + n]
    b_sup = d_sup[ra_s:ra_s + n]
    diffs = [i for i in range(n) if b_dem[i] != b_sup[i]]
    if not diffs:
        print(f"  {nom}: IDENTIQUE sur {n:#x} octets communs "
              f"(demo VS={vs_d:#x}, sup VS={vs_s:#x})")
    else:
        # regrouper en plages
        plages = []
        debut = diffs[0]
        prec = diffs[0]
        for i in diffs[1:]:
            if i > prec + 16:
                plages.append((debut, prec))
                debut = i
            prec = i
        plages.append((debut, prec))
        print(f"  {nom}: {len(diffs)} octets differents en {len(plages)} plages "
              f"(sur {n:#x} octets communs) :")
        for a, b in plages[:20]:
            rva = va_d + a
            print(f"    VA {rva:#06x}..{rva + (b - a):#06x} : "
                  f"demo={b_dem[a:b + 1].hex(' ')[:48]}  sup={b_sup[a:b + 1].hex(' ')[:48]}")
        if len(plages) > 20:
            print(f"    ... + {len(plages) - 20} plages")

# ---------- rescan robuste de .text2 superviseur ----------
print("\n=== rescan ROBUSTE .text2 superviseur (tous les appels [rip+-disp]) ===")
imp_rva = 0x2380
secs_liste = [(nom, *v) for nom, v in s_sup.items()]


def rva2off(rva):
    for nom, va, vs, ra, rs in secs_liste:
        if va <= rva < va + max(vs, rs):
            return ra + (rva - va)
    return None


# slots couverts (marche des descripteurs)
couverts = {}
off = rva2off(imp_rva)
n = 0
while True:
    oft, _, _, nomrva, ft = struct.unpack_from("<IIIII", d_sup, off + 20 * n)
    if oft == nomrva == ft == 0:
        break
    dll = d_sup[rva2off(nomrva):].split(b"\x00")[0].decode()
    i = 0
    while True:
        val = struct.unpack_from("<Q", d_sup, rva2off(oft + 8 * i))[0]
        if val == 0:
            break
        no = rva2off(val)
        fname = d_sup[no + 2:].split(b"\x00")[0].decode("ascii", "replace")
        couverts[ft + 8 * i] = f"{dll}!{fname}"
        i += 1
    n += 1

va2, vs2, ra2, rs2 = s_sup[".text2"]
code = d_sup[ra2:ra2 + rs2]
md = Cs(CS_ARCH_X86, CS_MODE_64)

pos = 0
appels = []
taille = len(code)
while pos < taille:
    decoupe = False
    for ins in md.disasm(code[pos:], va2 + pos):
        if ins.mnemonic in ("call", "jmp") and "[rip" in ins.op_str:
            op = ins.op_str
            p = op.find("[rip")
            q = op.find("]", p)
            morceau = op[p + 4:q].replace(" ", "")
            if morceau.startswith("+"):
                disp = int(morceau[1:], 16)
            elif morceau.startswith("-"):
                disp = -int(morceau[1:], 16)
            else:
                disp = 0
            cible = ins.address + ins.size + disp
            appels.append((ins.address, ins.mnemonic, cible))
        pos = ins.address - va2 + ins.size
        decoupe = True
    if not decoupe:
        pos += 1   # octet indécodable -> avancer d'un octet

print(f"  {len(appels)} appels indirects dans .text2")
fataux = 0
for ad, mn, cible in appels:
    statut = couverts.get(cible)
    marque = ""
    if statut is None:
        # cible dans une plage IAT ?
        dans_iat = any(a <= cible < a + 8 * 20
                       for a in (0x20b0, 0x2300, 0x2360, 0x2800, 0x2980, 0x2e80))
        if dans_iat:
            # trouver le slot le plus proche
            slot = cible & ~7
            marque = (f"  <<< IAT MAIS NON COUVERT — "
                      f"proche {couverts.get(slot, hex(slot))} (decalage {cible - slot})")
            fataux += 1
        else:
            zone = next((nm for nm, v, s, r, rz in
                         [(x[0], x[1], x[2], x[3], x[4]) for x in secs_liste]
                         if v <= cible < v + max(s, rz)), "?")
            marque = f"  -> hors IAT ({zone})"
    print(f"    {ad:#07x} {mn:<5} cible {cible:#06x}  {statut or marque}")
print(f"\n  *** {fataux} APPELS VERS IAT NON COUVERTS ***")
