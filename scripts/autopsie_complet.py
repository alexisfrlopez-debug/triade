#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIADE D52e — inventaire EXHAUSTIF avec capstone de toutes les references
memoire [rip+disp] des sections executables (.text et .text2) du superviseur,
resolution de chaque cible, et confrontation aux 30 slots reellement remplis
par le chargeur Windows (marche des descripteurs).

Un appel/dereference vers un slot NON couvert = pointeur 0 au lancement reel
= CALL/lecture a l'adresse NULL = 0xC0000005 module unknown.
"""

import pathlib
import struct

from capstone import Cs, CS_ARCH_X86, CS_MODE_64

SUP = pathlib.Path("/home/z/my-project/triade/terrain/superviseur.exe")

d = SUP.read_bytes()
e = struct.unpack_from("<I", d, 0x3C)[0]
coff = e + 4
_, nsec, _, _, _, opt_sz, _ = struct.unpack_from("<HHIIIHH", d, coff)
opt = coff + 20
imp_rva = struct.unpack_from("<I", d, opt + 120)[0]

secs = []
so = opt + opt_sz
for i in range(nsec):
    o = so + 40 * i
    nom = d[o:o + 8].rstrip(b"\x00").decode("ascii", "replace")
    vs, va, rs, ra = struct.unpack_from("<IIII", d, o + 8)
    fl = struct.unpack_from("<I", d, o + 36)[0]
    secs.append((nom, va, vs, ra, rs, fl))


def rva2off(rva):
    for nom, va, vs, ra, rs, _ in secs:
        if va <= rva < va + max(vs, rs):
            return ra + (rva - va)
    return None


# slots remplis par le chargeur
couverts = {}
off = rva2off(imp_rva)
n = 0
while True:
    oft, _, _, nomrva, ft = struct.unpack_from("<IIIII", d, off + 20 * n)
    if oft == nomrva == ft == 0:
        break
    dll = d[rva2off(nomrva):].split(b"\x00")[0].decode()
    i = 0
    while True:
        val = struct.unpack_from("<Q", d, rva2off(oft + 8 * i))[0]
        if val == 0:
            break
        no = rva2off(val)
        fname = d[no + 2:].split(b"\x00")[0].decode("ascii", "replace")
        couverts[ft + 8 * i] = f"{dll}!{fname}"
        i += 1
    n += 1
print(f"[chargeur] {len(couverts)} slots remplis : "
      f"{min(couverts):#x}..{max(couverts):#x}")

# balayage capstone complet des sections executables
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = False

refs = []          # (rva, mnemo, cible_rva, texte)
segments_exec = [(nom, va, vs, ra, rs) for nom, va, vs, ra, rs, fl in secs
                 if fl & 0x20000000]
print(f"[sections exec] {[(s[0], hex(s[1])) for s in segments_exec]}")

for nom, va, vs, ra, rs in segments_exec:
    code = d[ra:ra + rs]
    for ins in md.disasm(code, va):
        op = ins.op_str
        if "rip" not in op:
            continue
        # extraire le deplacement : [rip + 0xNNN] ou [rip - 0xNNN]
        p = op.find("[rip")
        if p < 0:
            continue
        q = op.find("]", p)
        morceau = op[p + 4:q].replace(" ", "")
        if morceau.startswith("+"):
            disp = int(morceau[1:], 16)
        elif morceau.startswith("-"):
            disp = -int(morceau[1:], 16)
        else:
            disp = 0
        cible = ins.address + ins.size + disp
        refs.append((ins.address, ins.mnemonic, cible,
                     f"{ins.mnemonic} {op}", nom))

print(f"[scan] {len(refs)} references [rip+disp] dans le code\n")

# classification
fatales = []
par_type = {}
for rva, mn, cible, txt, sec in refs:
    if cible in couverts:
        continue
    # cible non couverte : dans quelle zone tombe-t-elle ?
    zone = next((s[0] for s in secs if s[1] <= cible < s[1] + max(s[2], s[4])),
                "HORS-SECTIONS")
    if mn in ("call", "jmp"):
        # un call/jmp indirect vers une donnee non-IAT : dangereux si nul
        val_fichier = struct.unpack_from("<Q", d, rva2off(cible))[0] \
            if rva2off(cible) is not None else None
        # heuristique : la cible est-elle dans une plage IAT connue ?
        dans_iat = any(c0 <= cible < c0 + 8 * 64 for c0 in
                       [0x20b0, 0x2300, 0x2360, 0x2800, 0x2980, 0x2e80])
        cle = "call/jmp vers slot IAT NON COUVERT" if dans_iat else \
              f"call/jmp indirect -> {zone}"
        par_type.setdefault(cle, []).append((rva, cible, txt, val_fichier))
        if dans_iat:
            fatales.append((rva, cible, txt))
    else:
        cle = f"donnees -> {zone}"
        par_type.setdefault(cle, []).append((rva, cible, txt, None))

for cle, lst in sorted(par_type.items()):
    print(f"--- {cle} : {len(lst)} references")
    for rva, cible, txt, val in lst[:12]:
        vs = f" contenu-fichier={val:#018x}" if val is not None else ""
        print(f"    {rva:#07x} {txt:<46} -> {cible:#06x}{vs}")
    if len(lst) > 12:
        print(f"    ... + {len(lst) - 12} autres")

print("\n=== FATALES (call/jmp vers slot IAT non couvert) ===")
if not fatales:
    print("  AUCUNE — toutes les cibles IAT du code sont couvertes")
for rva, cible, txt in fatales:
    print(f"  !!! {rva:#07x} {txt} -> {cible:#06x} NON COUVERT")

# ou se trouvent les cibles de calls indirects (toutes)
print("\n=== toutes les cibles call/jmp [rip+disp] ===")
appels = [(rva, cible, txt) for rva, mn, cible, txt, sec in refs
          if mn in ("call", "jmp")]
for rva, cible, txt in appels:
    statut = couverts.get(cible, "*** NON COUVERT ***")
    print(f"  {rva:#07x} {txt:<40} -> {cible:#06x} {statut}")
