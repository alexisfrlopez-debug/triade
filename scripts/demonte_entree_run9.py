#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Démontage du chemin d'entrée de loupe.exe (RVA 0x5C00, section .text2)
et de ses abords — avec suivi de pile (push/pop/sub/add) et cibles
rip-relatives nommées. On cherche : tout saut indirect HORS IAT, toute
écriture de pile qui déborde du cadre, tout lpfnWndProg qui ne serait
pas une adresse de code.
"""
import struct
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

donnees = open("/home/z/my-project/run9/loupe.exe", "rb").read()
# sections : .text2 VA 0x4000 PR 0x3200
def rva2f(rva):
    for nom, va, vs, srd, prd in [
        (".text", 0x1000, 0x1000, 0x1000, 0x200),
        (".rdata", 0x2000, 0x2000, 0x2000, 0x1200),
        (".text2", 0x4000, 0xA000, 0xA000, 0x3200),
        (".data", 0xE000, 0x12000, 0x12000, 0xD200),
    ]:
        if va <= rva < va + srd:
            return prd + (rva - va)
    return None

md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = False

def demonte(rva_debut, rva_fin, titre):
    print(f"\n===== {titre} (rva {rva_debut:#x} → {rva_fin:#x}) =====")
    fo = rva2f(rva_debut)
    code = donnees[fo:fo + (rva_fin - rva_debut)]
    pile = 0
    for insn in md.disasm(code, rva_debut):
        note = ""
        m = insn.mnemonic
        ops = insn.op_str
        if m == "push":
            pile += 8
        elif m == "pop":
            pile -= 8
        elif m == "sub" and ops.startswith("rsp,"):
            pile += int(ops.split(",")[1], 16)
            note = f"  ; cadre → {pile}"
        elif m == "add" and ops.startswith("rsp,"):
            pile -= int(ops.split(",")[1], 16)
            note = f"  ; cadre → {pile}"
        elif m == "ret":
            note = f"  ; pile nette attendue, reste {pile:+d}"
        elif m == "call":
            if "rip" in ops:
                # cible de l'appel indirect
                off = int(ops.split("rip + ")[1].rstrip("]"), 16) if "+" in ops \
                    else -int(ops.split("rip - ")[1].rstrip("]"), 16)
                cible_rva = insn.address + insn.size + off
                note = f"  ; → slot iat rva {cible_rva:#x}"
            elif ops.startswith("0x"):
                note = f"  ; → rva {int(ops, 16):#x}"
        elif m == "lea" and "rip" in ops:
            off = int(ops.split("rip + ")[1].rstrip("]"), 16) if "+" in ops \
                else -int(ops.split("rip - ")[1].rstrip("]"), 16)
            cible_rva = insn.address + insn.size + off
            note = f"  ; → rva {cible_rva:#x}"
        print(f"  {insn.address:#07x}: {insn.bytes.hex():<20} {m} {ops}{note}")

# L'entrée et tout le chemin jusqu'à la boucle
demonte(0x5C00, 0x5E80, "L'ENTRÉE (début)")
