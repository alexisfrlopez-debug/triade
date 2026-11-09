#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Chasse SSE dans le code joignable depuis l'entrée de loupe.exe dev.7.

Les défauts SSE (movaps/movdqa sur adresse non alignée à 16) ont déjà tué
la vitrine à l'ère dev.4 (Entrée 208 les nomma). Le scénario appelle les
fonctions scellées avec SES propres tampons alignés — le chemin de l'entrée
(peintre, WndProc, minilibc) peut vivre les mêmes instructions sur des
adresses DIFFÉRENTES. Ici : inventaire de chaque SSE alignement-sensible
et de sa contrainte effective.
"""
import struct
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
import capstone.x86_const as xc

EXE = "/home/z/my-project/run8/loupe.exe"
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

# .text2 : VA 0x4000 VS 0xA000 PTR 0x3200 ; .text : VA 0x1000 PTR 0x200
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

SSE_SENSIBLES = {"movaps", "movdqa", "movaps128"}

# cartographie des appels : on part de l'entrée et on suit les call directs
APPELS_DEPUIS = {}


def demonte_bloc(rva_debut, taille_max=0x800, prof=0, vus=None):
    """Démonte un bloc, note les SSE et suit les appels directs (profondeur 3)."""
    if vus is None:
        vus = set()
    if rva_debut in vus or prof > 3:
        return
    vus.add(rva_debut)
    o = None
    for (nom, va, vs, ptr) in sections:
        if va <= rva_debut < va + vs:
            o = ptr + (rva_debut - va)
    if o is None:
        return
    code = d[o:o + taille_max]
    sse_trouves = []
    cibles = []
    for ins in md.disasm(code, rva_debut):
        if ins.mnemonic in ("movaps", "movdqa"):
            # destination
            for op in ins.operands:
                if op.type == xc.X86_OP_MEM:
                    m = op.mem
                    base = md.reg_name(m.base) if m.base else None
                    index = md.reg_name(m.index) if m.index else None
                    sse_trouves.append((ins.address, ins.mnemonic, ins.op_str,
                                        base, index, m.disp))
        if ins.mnemonic == "call" and ins.operands and ins.operands[0].type == xc.X86_OP_IMM:
            cibles.append(ins.operands[0].imm)
        if ins.mnemonic == "ret":
            break
    for (adr, mn, ops, base, index, disp) in sse_trouves:
        # contrainte : (base + index + disp) ≡ 0 mod 16
        expr = f"{base or ''}{(' + ' + index) if index else ''}{(' + %#x' % disp) if disp else ''}"
        print(f"  SSE {adr:#06x}  {mn:<8} {ops:<40} contrainte : {expr} ≡ 0 (mod 16)")
    for c in cibles:
        demonte_bloc(c, taille_max=0x800, prof=prof + 1, vus=vus)


print("=== LE CHEMIN DE L'ENTRÉE (0x5C00) : les SSE rencontrés, profondeur 3 ===")
demonte_bloc(0x5C00)
print("\n=== LE PEINTRE (0x4B00) ===")
demonte_bloc(0x4B00)
