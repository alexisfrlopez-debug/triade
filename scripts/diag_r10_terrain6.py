#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Diagnostic porte R10 sur superviseur-terrain6.exe (livré, md5 2e582a64).

La porte réelle (win-06 @0x1AC0, héritage byte-identique de demo.exe) :
  - table @rva 0x2450 : entrées de 16 octets (u32 rva, u32 len, u64 somme)
  - boucle : TANT QUE entry.rva != 0 → somme des u64 LE de [rva, rva+len),
    comparée à entry.somme ; mismatch → retour -1 (porte KO)
  - TERMINATEUR = rva == 0 (PAS un compte !)
  - puis version u64 @0x2628 >= 0x30000, puis 4 tests libc.

Le patch terrain.6 n'a vérifié/ajusté que les entrées 0..19 (N=20 supposé).
S'il existe des entrées >= 20 couvrant une zone patchée (VERSIONINFO .rsrc
@0x70D4-0x72CD notamment), leur somme est périmée → porte KO sur machine
réelle, alors que la post-vérification du patch (bornée à 20) voyait vert.
"""

import struct
import sys
import pathlib

# --- géométrie PE (identique au patch) --------------------------------------
RDATA_RVA, RDATA_FILE = 0x2000, 0x1400
TEXT2_RVA, TEXT2_FILE = 0x4000, 0x2e00
R10_TABLE_RVA = 0x2450

def rva2off(rva):
    if 0x1000 <= rva < 0x2000:
        return 0x400 + (rva - 0x1000)
    if RDATA_RVA <= rva < 0x3000:
        return RDATA_FILE + (rva - RDATA_RVA)
    if 0x3000 <= rva < 0x4000:
        d = rva - 0x3000
        return 0x2400 + d if d < 0xA00 else None
    if TEXT2_RVA <= rva < 0x6E00:
        return TEXT2_FILE + (rva - TEXT2_RVA)
    if 0x7000 <= rva < 0x7800:
        return 0x5C00 + (rva - 0x7000)
    if 0x8000 <= rva < 0x10D10:
        return 0x6400 + (rva - 0x8000)
    if 0x11000 <= rva < 0x11200:
        return 0xF200 + (rva - 0x11000)
    return None

def somme_zone(data, rva, ln):
    """L'algorithme EXACT de la porte : somme de mots u64 LE, tronquée 64 bits."""
    o = rva2off(rva)
    s = 0
    for i in range(0, ln, 8):
        s = (s + struct.unpack_from("<Q", data, o + i)[0]) & 0xFFFFFFFFFFFFFFFF
    return s

def analyser(chemin, etiquettes_patch):
    data = pathlib.Path(chemin).read_bytes()
    table_off = rva2off(R10_TABLE_RVA)
    print(f"\n=== {pathlib.Path(chemin).name} — table R10 @rva {R10_TABLE_RVA:#x} "
          f"(file {table_off:#x}) ===")
    rouge = []
    k = 0
    while True:
        rva, ln, sm = struct.unpack_from("<IIQ", data, table_off + 16 * k)
        if rva == 0:
            print(f"  [{k:2d}] TERMINATEUR rva=0 len={ln:#x} — fin de table "
                  f"(la porte s'arrête ICI)")
            break
        o = rva2off(rva)
        if o is None or ln == 0:
            print(f"  [{k:2d}] ENTREE ILLISIBLE rva={rva:#x} len={ln:#x} "
                  f"— zone non mappée")
            rouge.append((k, rva, ln, sm, "illisible"))
            break
        calc = somme_zone(data, rva, ln)
        etat = "VERT" if calc == sm else "*** ROUGE ***"
        couvre = [lab for (arva, aln, lab) in etiquettes_patch
                  if not (rva + ln <= arva or arva + aln <= rva)]
        note = f"  COUVRE {couvre}" if couvre else ""
        print(f"  [{k:2d}] rva={rva:#06x} len={ln:#06x} somme={sm:#018x} "
              f"calc={calc:#018x} {etat}{note}")
        if calc != sm:
            rouge.append((k, rva, ln, sm, calc))
        k += 1
        if k > 60:
            print("  [!] plus de 60 entrées — table corrompue ?")
            break
    # version @0x2628
    off_v = rva2off(0x2628)
    v = struct.unpack_from("<Q", data, off_v)[0]
    print(f"  version @0x2628 = {v:#x} ({'OK >= 0x30000' if v >= 0x30000 else 'KO < 0x30000'})")
    return rouge

# zones modifiées par le patch terrain.6 (rva, len, étiquette)
zones_patch = [
    (0x544F, 9,   "sup-33 lea/xor (FindWindowW)"),
    (0x2450 + 16 * 19 + 8, 8, "somme R10[19] (champ table)"),
    (0x2ADA, 1,   "L00 'terrain.6'"),
    (0x4366, 1,   "S00 'terrain.6'"),
    (0x70D4, 2,   "VERSIONINFO FileVersion binaire"),
    (0x70DC, 2,   "VERSIONINFO ProductVersion binaire"),
    (0x71C4, 2,   "VERSIONINFO FileVersion chaîne"),
    (0x72CC, 2,   "VERSIONINFO ProductVersion chaîne"),
]

t5 = "/home/z/my-project/upload/superviseur-terrain5.exe"
t6 = "/home/z/my-project/upload/superviseur-terrain6.exe"
t7 = "/home/z/my-project/triade/terrain/livraison/superviseur-terrain7.exe"
r5 = analyser(t5, zones_patch)
r6 = analyser(t6, zones_patch)
r7 = analyser(t7, zones_patch)

print("\n=== VERDICT ===")
print(f"terrain.5 : {len(r5)} entrée(s) ROUGE(s)")
print(f"terrain.6 : {len(r6)} entrée(s) ROUGE(s)")
for (k, rva, ln, sm, calc) in r6:
    print(f"  → entrée [{k}] rva={rva:#x} len={ln:#x} : attendu {sm:#x}, "
          f"recalculé {calc if isinstance(calc, str) else hex(calc)}")
print(f"terrain.7 : {len(r7)} entrée(s) ROUGE(s)")
for (k, rva, ln, sm, calc) in r7:
    print(f"  → entrée [{k}] rva={rva:#x} len={ln:#x} : attendu {sm:#x}, "
          f"recalculé {calc if isinstance(calc, str) else hex(calc)}")
sys.exit(0)
