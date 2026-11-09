#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LA CHASSE DÉCISIVE — l'ASLR est ON (DllChars 0x160), la base préférée
est 0x140000000, la table BASERELOC ne porte qu'UNE entrée (12 o).

Si des qwords de l'image contiennent des adresses de l'enveloppe
préférée [0x140000000, +0x20000) et que la table ne les couvre pas :
sous ASLR ils restent PÉRIMÉS (ils pointent la base préférée, l'image
vit à 0x7FF6…) — tout saut au travers meurt sur une page non mappée,
EXÉCUTION sur mémoire non-exécutable, module « unknown » — LE NOM DU
BEX64 DU RUN 9.
"""
import struct

donnees = open("/home/z/my-project/run9/loupe.exe", "rb").read()
e_lfanew = struct.unpack_from("<I", donnees, 0x3C)[0]
opt = e_lfanew + 4 + 20
szopt = struct.unpack_from("<H", donnees, opt - 4)[0]
nsec = struct.unpack_from("<H", donnees, e_lfanew + 6)[0]
imgbase = struct.unpack_from("<Q", donnees, opt + 24)[0]
szimg = struct.unpack_from("<I", donnees, opt + 56)[0]
off_sec = opt + szopt

sections = []
for i in range(nsec):
    b = off_sec + 40 * i
    nom = donnees[b:b + 8].rstrip(b"\0").decode()
    vs, va, srd, prd = struct.unpack_from("<IIII", donnees, b + 8)
    sections.append((nom, va, vs, srd, prd))
    print(f"{nom:<8} VA {va:#07x} VS {vs:#07x} RS {srd:#07x} PR {prd:#07x}")

def rva_vers_fichier(rva):
    for nom, va, vs, srd, prd in sections:
        if va <= rva < va + max(vs, srd):
            return prd + (rva - va), nom
    return None, None

# --- 1. La table BASERELOC décortiquée --------------------------------------
rva_rel, taille_rel = struct.unpack_from("<II", donnees, opt + 112 + 8 * 5)
print(f"\nBASERELOC dirs[5] = ({rva_rel:#x}, {taille_rel})")
fo, sec = rva_vers_fichier(rva_rel)
print(f"  → fichier {fo:#x} ({sec})")
TYPES = {0: "ABSOLUTE", 1: "HIGH", 2: "LOW", 3: "HIGHLOW", 10: "DIR64"}
couverts = set()
p, fin = fo, fo + taille_rel
while p < fin:
    pagerva, blocksize = struct.unpack_from("<II", donnees, p)
    if blocksize == 0:
        break
    print(f"  bloc : PageRVA {pagerva:#x}, taille {blocksize}")
    for j in range((blocksize - 8) // 2):
        e, = struct.unpack_from("<H", donnees, p + 8 + 2 * j)
        t, off = e >> 12, e & 0xFFF
        cible = pagerva + off
        if t:
            f2, s2 = rva_vers_fichier(cible)
            val = struct.unpack_from("<Q", donnees, f2)[0] if f2 else None
            print(f"    {TYPES.get(t, t)} @rva {cible:#x} ({s2}) = "
                  f"{val:#018x}" if val is not None else
                  f"    {TYPES.get(t, t)} @rva {cible:#x} (HORS SECTIONS)")
            couverts.add(cible)
        else:
            print(f"    ABSOLUTE (bourrage) @rva {cible:#x}")
    p += blocksize

# --- 2. La chasse aux qwords de l'enveloppe préférée -------------------------
lo, hi = imgbase, imgbase + szimg
print(f"\nChasse aux qwords dans [{lo:#x}, {hi:#x}) :")
trouves = []
for nom, va, vs, srd, prd in sections:
    for fo2 in range(prd, prd + srd - 7):
        q, = struct.unpack_from("<Q", donnees, fo2)
        if lo <= q < hi:
            rva_q = va + (fo2 - prd)
            trouves.append((rva_q, nom, q))
for rva_q, nom, q in trouves:
    marque = "  ← COUVERT par la reloc" if rva_q in couverts else \
             "  ← *** PAS COUVERT — PÉRIMÉ SOUS ASLR ***"
    print(f"  {nom} @rva {rva_q:#06x} = {q:#x} (→ rva {q - lo:#x}){marque}")
if not trouves:
    print("  AUCUN")

# --- 3. L'« IAT démo réservée » @0x2818 --------------------------------------
print("\nLa zone .rdata 0x2800-0x28A0 (l'IAT démo « réservée » @0x2818) :")
for rva in range(0x2800, 0x28A0, 8):
    f3, s3 = rva_vers_fichier(rva)
    q, = struct.unpack_from("<Q", donnees, f3)
    note = ""
    if lo <= q < hi:
        note = f"  ← POINTEUR ABSOLU → rva {q - lo:#x}"
        if rva in couverts:
            note += " (couvert)"
        else:
            note += " (*** PAS COUVERT ***)"
    print(f"  @rva {rva:#06x} = {q:#018x}{note}")
