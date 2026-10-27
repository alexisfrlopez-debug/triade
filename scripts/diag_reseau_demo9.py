#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Désassemblage complet de la chaîne réseau du demo.9 (et comparaison demo.8).

Zones :
  tcp-01   @ 0x4000  (WSA + socket)
  tcp-02   @ 0x4100  (bind + listen + accept ?)
  écho     @ 0x4600  (bloc patchable v1)
  trampo   @ 0x4680
  fil écho @ 0x4800  (tcp-09 : recv -> CS -> console -> écho -> send)
  win-10   @ 0x4980  (échange client)
  win-09   @ 0x4C00  (scénario — phase réseau)
  win-05   @ 0x5000  (miroir journal — entrée trace)
"""

from capstone import Cs, CS_ARCH_X86, CS_MODE_64

md = Cs(CS_ARCH_X86, CS_MODE_64)

TEXT2_RVA, TEXT2_FILE = 0x4000, 0x2C00
TEXT_RVA, TEXT_FILE = 0x1000, 0x200

def rva2off(rva):
    if 0x1000 <= rva < 0x2000:
        return TEXT_FILE + (rva - TEXT_RVA)
    if 0x4000 <= rva < 0x5400:
        return TEXT2_FILE + (rva - TEXT2_RVA)
    return None

def affiche(d, rva, taille, titre, stop_sur_ret=True):
    off = rva2off(rva)
    print(f"\n--- {titre} @ {rva:#x} ---")
    n = 0
    for ins in md.disasm(d[off:off + taille], rva):
        print(f"  {ins.address:#07x}: {ins.mnemonic:9} {ins.op_str}")
        n += 1
        if stop_sur_ret and ins.mnemonic == "ret":
            break
        if n > 120:
            print("  ... (tronqué)")
            break

d9 = open("/tmp/demo9.exe", "rb").read()
d8 = open("/tmp/demo8.exe", "rb").read()

# vérif héritage : tcp-* identiques entre 8 et 9 ?
for nom, rva, t in (("tcp-01", 0x4000, 0x100), ("tcp-02", 0x4100, 0x100),
                    ("écho+trampo", 0x4600, 0x100), ("fil écho tcp-09", 0x4800, 0x180)):
    a = d8[rva2off(rva):rva2off(rva) + t]
    b = d9[rva2off(rva):rva2off(rva) + t]
    print(f"[héritage] {nom:15} @ {rva:#x} : "
          f"{'IDENTIQUE' if a == b else 'DIFFÉRENT'}")

affiche(d9, 0x4000, 0x80, "demo.9 tcp-01 (socket)")
affiche(d9, 0x4100, 0x100, "demo.9 tcp-02 (bind/listen/accept)")
affiche(d9, 0x4600, 0x80, "demo.9 bloc écho v1 (patchable)")
affiche(d9, 0x4680, 0x60, "demo.9 trampoline")
affiche(d9, 0x4800, 0x180, "demo.9 fil écho (tcp-09)")
