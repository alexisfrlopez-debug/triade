#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""La carte complète des imports (noms réels) + la boucle 0x15C0 + le
WndProc 0x5DCB démontés avec suivi de pile."""
import struct
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

donnees = open("/home/z/my-project/run9/loupe.exe", "rb").read()

def rva2f(rva):
    for nom, va, srd, prd in [(".text", 0x1000, 0x1000, 0x200),
                              (".rdata", 0x2000, 0x2000, 0x1200),
                              (".text2", 0x4000, 0xA000, 0x3200),
                              (".data", 0xE000, 0x12000, 0xD200)]:
        if va <= rva < va + srd:
            return prd + (rva - va)
    return None

def lis_zstring(rva):
    fo = rva2f(rva)
    fin = donnees.find(b"\0", fo)
    return donnees[fo:fin].decode("ascii", "replace")

# --- La carte des imports ----------------------------------------------------
print("=== LA CARTE DES IMPORTS ===")
descs = [(0x2830 + 20 * i) for i in range(4)]
for d in descs:
    oft, tds, fwd, nom, ft = struct.unpack_from("<IIIII", donnees, rva2f(d))
    dll = lis_zstring(nom)
    print(f"\n{dll} (OFT {oft:#x}, FT {ft:#x}) :")
    p = rva2f(oft)
    i = 0
    while True:
        e, = struct.unpack_from("<I", donnees, p + 4 * i)
        if e == 0:
            break
        if e & 0x80000000:
            print(f"  slot {ft + 4*i:#x} : ORDINAL {e & 0xFFFF}")
        else:
            fo2 = rva2f(e)
            hint, = struct.unpack_from("<H", donnees, fo2)
            nm = donnees[fo2 + 2:donnees.find(b'\0', fo2 + 2)].decode()
            print(f"  slot {ft + 4*i:#x} : {nm}")
        i += 1

# --- Le démontage générique --------------------------------------------------
md = Cs(CS_ARCH_X86, CS_MODE_64)

def demonte(rva_debut, rva_fin, titre):
    print(f"\n===== {titre} (rva {rva_debut:#x} → {rva_fin:#x}) =====")
    fo = rva2f(rva_debut)
    code = donnees[fo:fo + (rva_fin - rva_debut)]
    pile = 0
    for insn in md.disasm(code, rva_debut):
        m, ops = insn.mnemonic, insn.op_str
        note = ""
        if m == "push":
            pile += 8
        elif m == "pop":
            pile -= 8
        elif m in ("sub", "add") and ops.startswith("rsp,"):
            n = int(ops.split(",")[1], 16)
            pile += n if m == "sub" else -n
            note = f"  ; cadre {pile:+d}"
        elif m == "ret":
            note = f"  ; il reste {pile:+d} (attendu 0 aux pushes près)"
        elif m in ("call", "jmp") and "rip" in ops:
            if "+" in ops:
                off = int(ops.split("rip + ")[1].rstrip("]"), 16)
            else:
                off = -int(ops.split("rip - ")[1].rstrip("]"), 16)
            cible = insn.address + insn.size + off
            note = f"  ; → iat slot {cible:#x}" if cible >= 0x3100 and cible < 0x3248 \
                else f"  ; → rva {cible:#x}"
        elif m in ("call", "jmp") and ops.startswith("0x"):
            note = f"  ; → rva {int(ops, 16):#x}"
        elif m == "lea" and "rip" in ops:
            if "+" in ops:
                off = int(ops.split("rip + ")[1].rstrip("]"), 16)
            else:
                off = -int(ops.split("rip - ")[1].rstrip("]"), 16)
            cible = insn.address + insn.size + off
            note = f"  ; → rva {cible:#x}"
        print(f"  {insn.address:#07x}: {m:<8} {ops}{note}")

demonte(0x15C0, 0x1680, "LA BOUCLE À MESSAGES (« boucle démo ») @0x15C0")
demonte(0x5DCB, 0x5F40, "LE WNDPROC @0x5DCB")
