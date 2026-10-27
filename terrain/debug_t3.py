#!/usr/bin/env python3
"""debug_t3.py — Localise le crash de sup-35."""
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util as ilu
_spec = ilu.spec_from_file_location("layout_terrain", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "layout.py"))
L = ilu.module_from_spec(_spec)
_spec.loader.exec_module(L)

import oracle_terrain as od
import build_terrain as bt
from unicorn import UcError

blocs, specs, code, verrous = bt.assembler_tout()
texte, rdata, data, text2 = bt.composer_sections(code, blocs)
exe = bt.ecrire_pe32plus(texte, rdata, data, text2)

demo17 = od._journal_demo_17()
em = od.Emulateur(exe)
em.installer_shims()
em.uc.mem_write(od.IMAGE + L.HWND_JOURNAL, struct.pack("<Q", od.FAKE_HWND_EDIT))
od.preparer_scenario(em, demo17)

try:
    r = em.appeler(L.ZONE_T3[0])
    print("T3 rax =", r)
except UcError as exc:
    rip = em.uc.reg_read(od.UC_X86_REG_RIP if hasattr(od, "UC_X86_REG_RIP") else 0)
    from unicorn.x86_const import UC_X86_REG_RSP, UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_RIP
    rip = em.uc.reg_read(UC_X86_REG_RIP)
    rsp = em.uc.reg_read(UC_X86_REG_RSP)
    print(f"CRASH : {exc} @ RIP {rip:#x} (RVA {rip - od.IMAGE:#x})")
    print(f"RSP {rsp:#x} | zone .data = {od.IMAGE + 0x3000:#x}..{od.IMAGE + 0x4000:#x}")
    import capstone
    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    autour = bytes(em.uc.mem_read(rip - 16, 48))
    for i in cs.disdb(autour, rip - 16) if False else cs.disasm(autour, rip - 16):
        marque = " <<<<" if i.address == rip else ""
        print(f"  {i.address:#x}  {i.mnemonic} {i.op_str}{marque}")
    print("Journal T3 avant crash :")
    for ligne in em.journal_fichier:
        print("   ", ligne[:76])
    print("FS:", {k: v[:40] for k, v in em.fichiers.items()})
