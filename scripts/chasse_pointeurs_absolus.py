#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Chasse aux pointeurs absolus : scan de .data/.rdata pour des qwords
dans l'enveloppe 0x140000000-0x140020000 (ImageBase + image).

Sous ASLR (DllCharacteristics DYNAMIC_BASE), la pièce charge ailleurs —
un tel pointeur serait STALE et sa déférence = 0xC0000005. Le scénario
charge à 0x7ff6... mais ne visite jamais les globales du peintre.
"""
import pefile
import struct

pe = pefile.PE("/home/z/my-project/run8/loupe.exe", fast_load=True)
base = pe.OPTIONAL_HEADER.ImageBase
size_img = pe.OPTIONAL_HEADER.SizeOfImage
print(f"ImageBase {base:#x} · SizeOfImage {size_img:#x} · "
      f"enveloppe [{base:#x}, {base + size_img:#x})")

for s in pe.sections:
    nom = s.Name.rstrip(b"\0").decode()
    if nom not in (".data", ".rdata"):
        continue
    va = s.VirtualAddress
    vs = s.Misc_VirtualSize
    ptr = s.PointerToRawData
    raw = pe.get_data(va, vs)
    trouves = []
    for off in range(0, vs - 7):
        q = struct.unpack_from("<Q", raw, off)[0]
        if base <= q < base + size_img:
            trouves.append((va + off, q))
    print(f"\n=== {nom} VA {va:#x} VS {vs:#x} : {len(trouves)} qwords dans l'enveloppe ===")
    for (rva, q) in trouves[:40]:
        # où pointe-t-il ?
        cible = rva = q - base
        dans = "?"
        for s2 in pe.sections:
            if s2.VirtualAddress <= cible < s2.VirtualAddress + s2.Misc_VirtualSize:
                dans = s2.Name.rstrip(b"\0").decode()
        print(f"  @{rva:#x} : {q:#x} → RVA {cible:#x} ({dans})")
