#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Le décodage intégral de l'en-tête — où VIVENT réellement les répertoires ?

Faits connus (Entrées 204/206/213) : BASERELOC dirs[5] = (0x2E90, 12),
IAT dirs[12] = (0x3100, 0x148), imports 4 descripteurs (OFT 0x28A0…).
On cherche ces motifs dans le fichier pour localiser la VRAIE table.
"""
import struct

donnees = open("/home/z/my-project/run9/loupe.exe", "rb").read()
e_lfanew = struct.unpack_from("<I", donnees, 0x3C)[0]
opt = e_lfanew + 4 + 20

print("=== OptionalHeader brut (0x00 → 0x100) ===")
for i in range(0, 0x100, 16):
    chunk = donnees[opt + i:opt + i + 16]
    print(f"  opt+{i:03x}: " + " ".join(f"{b:02x}" for b in chunk))

# Recherche des motifs connus dans TOUT le fichier
print("\n=== Recherche des motifs des répertoires connus ===")
motifs = {
    "BASERELOC (0x2E90, 12)": struct.pack("<II", 0x2E90, 12),
    "IAT (0x3100, 0x148)": struct.pack("<II", 0x3100, 0x148),
    "IMPORT (0x2830, 0x64)": struct.pack("<II", 0x2830, 0x64),
    "IMPORT (0x2860, 0x64)": struct.pack("<II", 0x2860, 0x64),
    "IMPORT (0x2880, 0x64)": struct.pack("<II", 0x2880, 0x64),
}
for nom, motif in motifs.items():
    p = 0
    positions = []
    while True:
        p = donnees.find(motif, p)
        if p < 0:
            break
        positions.append(p)
        p += 1
    if positions:
        for pos in positions:
            rel = pos - opt
            print(f"  {nom} TROUVÉ @ fichier {pos:#x} (opt+{rel:#x}, "
                  f"dirs[{(rel - 96) // 8}] si table standard)")
    else:
        print(f"  {nom} : absent")

# Décodage COMME SI la table des dirs commençait à chaque offset candidat
print("\n=== Décodage de la table des répertoires à chaque offset candidat ===")
NOMS = ["EXPORT", "IMPORT", "RESOURCE", "EXCEPTION", "SECURITY",
        "BASERELOC", "DEBUG", "ARCH", "GLOBALPTR", "TLS", "LOAD_CONFIG",
        "BOUND_IMP", "IAT", "DELAY_IMP", "CLR", "RESERV"]
candidats = [96]  # standard
# plus tout offset où le motif IAT apparaît à position dirs[12]
for base in candidats:
    # cherchons base tel que base + 12*8 contienne le motif IAT
    pass
# Le motif IAT est-il à opt+96+96=opt+0xC0 ?
for guess in range(0x60, 0x90, 8):
    pos = opt + guess
    dirs = []
    for i in range(16):
        rva, taille = struct.unpack_from("<II", donnees, pos + 8 * i)
        dirs.append((rva, taille))
    # la table est-elle celle attendue ?
    score = 0
    if dirs[5] == (0x2E90, 12):
        score += 1
    if dirs[12] == (0x3100, 0x148):
        score += 1
    if dirs[1][1] == 0x64 and dirs[1][0] in (0x2830, 0x2860, 0x2880):
        score += 1
    if score:
        print(f"\n  TABLE @ opt+{guess:#x} — score {score}/3 :")
        for i, (rva, taille) in enumerate(dirs):
            if rva or taille:
                print(f"    [{i:2d}] {NOMS[i]:<12} ({rva:#x}, {taille:#x})")

# Les slots IAT PRÉREMLIS : que contiennent-ils dans le fichier ?
print("\n=== Les slots IAT du fichier (RVA 0x3100 → 0x3248) ===")
# .rdata : VA 0x2000, PR 0x1200 → RVA 0x3100 = fichier 0x1200+0x1100 = 0x2300
for i in range(0, 0x148, 8):
    q, = struct.unpack_from("<Q", donnees, 0x2300 + i)
    rva = 0x3100 + i
    print(f"  slot @rva {rva:#06x} = {q:#018x}"
          f"{'  ← NULL (séparateur)' if q == 0 else ''}")
