#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Disassemble le chemin d'entrée de loupe.exe dev.7 — CHAQUE référence
rip-relative résolue et vérifiée contre la carte (IAT, chaînes, structures).

Le but : le scénario est vert T0→T7 mais la vitrine meurt 0xC0000005 —
le chemin de l'entrée (0x5C00 → RegisterClassExW → CreateWindowExW →
boucle) n'est JAMAIS exécuté par le scénario. Chaque lea/call/jmp du bloc
est résolu : où tombe-t-il exactement ?
"""
import struct
import sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

EXE = "/home/z/my-project/run8/loupe.exe"
R_ENTREE = 0x5C00          # l'adresse scellée du point d'entrée
R_WNDPROC = 0x5DCB         # l'adresse scellée de la procédure

d = open(EXE, "rb").read()
e_lfanew = struct.unpack_from("<I", d, 0x3C)[0]
coff = e_lfanew + 4
machine, nsec, tds, ptrsym, nsym, opt_size, chars = struct.unpack_from("<HHIIIHH", d, coff)
opt = coff + 20
sec_off = opt + opt_size
sections = []
for i in range(nsec):
    s = sec_off + 40 * i
    nom = d[s:s + 8].rstrip(b"\0").decode("ascii", "replace")
    vs = struct.unpack_from("<I", d, s + 8)[0]
    va = struct.unpack_from("<I", d, s + 12)[0]
    ptr = struct.unpack_from("<I", d, s + 20)[0]
    sections.append((nom, va, vs, ptr))


def r2o(rva):
    for (nom, va, vs, ptr) in sections:
        if va <= rva < va + vs:
            return ptr + (rva - va)
    return None


def dans_section(rva):
    for (nom, va, vs, ptr) in sections:
        if va <= rva < va + vs:
            return nom
    return "HORS-SECTIONS"


# la carte IAT : slot → nom de fonction (depuis les FT des descripteurs)
imp_rva = struct.unpack_from("<I", d, opt + 112 + 8)[0]
carte_iat = {}
off = r2o(imp_rva)
i = 0
while True:
    oft, tds, fwd, namerva, ft = struct.unpack_from("<IIIII", d, off + 20 * i)
    if oft == 0 and namerva == 0 and ft == 0:
        break
    o = r2o(ft)
    n = 0
    while True:
        v = struct.unpack_from("<Q", d, o + 8 * n)[0]
        if v == 0:
            break
        no = r2o(v)
        fin = d.find(b"\0", no + 2)
        nomf = d[no + 2:fin].decode("ascii", "replace")
        carte_iat[ft + 8 * n] = nomf
        n += 1
    i += 1

md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True


def demonte(rva_debut, rva_fin, titre):
    print(f"\n=== {titre} [{rva_debut:#x}, {rva_fin:#x}) ===")
    o = r2o(rva_debut)
    code = d[o:r2o(rva_fin)]
    nb_appels = 0
    for ins in md.disasm(code, rva_debut):
        ligne = f"  {ins.address:#06x}  {ins.mnemonic:<8} {ins.op_str}"
        note = ""
        # résolution rip-relative
        if "rip" in ins.op_str:
            for op in ins.operands:
                if op.type == 3 and op.mem.base == 41:  # X86_REG_RIP = 41? non, capstone: x86_reg.X86_REG_RIP
                    pass
        # capstone: op.mem.base == X86_REG_RIP (en 64 bits)
        import capstone.x86_const as xc
        for op in ins.operands:
            if op.type == xc.X86_OP_MEM and op.mem.base == xc.X86_REG_RIP:
                cible = ins.address + ins.size + op.mem.disp
                sec = dans_section(cible)
                if cible in carte_iat:
                    note = f"  ; → IAT[{carte_iat[cible]}] @ {cible:#x}"
                else:
                    # que contient la cible ?
                    co = r2o(cible)
                    if co is not None:
                        q = struct.unpack_from("<Q", d, co)[0]
                        note = f"  ; → {sec} @ {cible:#x} (qword {q:#018x})"
                        if q in carte_iat and ins.mnemonic == "jmp":
                            note = f"  ; → jmp IAT[{carte_iat[q]}] (queue à {cible:#x})"
                    else:
                        note = f"  ; → {cible:#x} HORS-SECTIONS !!"
        if ins.mnemonic in ("call", "jmp") and "rip" in ins.op_str:
            nb_appels += 1
        print(ligne + note)
    print(f"  ({nb_appels} appels/sauts indirects)")


if __name__ == "__main__":
    import capstone.x86_const as xc  # noqa: F401
    demonte(0x15C0, 0x15C0 + 0x180, "LA BOUCLE DÉMO")
    demonte(0x4B00, 0x4B00 + 0x120, "LE PEINTRE (WM_PAINT → 0x4b00)")
