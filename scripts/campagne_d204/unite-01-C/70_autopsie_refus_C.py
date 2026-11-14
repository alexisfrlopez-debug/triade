#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE — L'AUTOPSIE DU REFUS DU BRAS C (D122, au POSIX) : rejouer la
traversée de la table d'imports DU SCÉNARIO contre les octets RÉELS de la
pièce loupe-01-c.dll — reproduire le plantage du terrain AVEC SON ADRESSE
EXACTE (0x7FFA23900094), ou le nommer autrement."""
import pathlib
import struct

KIT = pathlib.Path("/home/z/my-project/download/nouveau-run/"
                   "kit-unite-loupe-01-C-20261114")
dll = (KIT / "loupe-01-c.dll").read_bytes()
BASE_TERRAIN = 0x7FF9B74D0000      # la console : « DONT_RESOLVE @ 0x7ff9b74d0000 »
CRASH_TERRAIN = 0x7FFA23900094     # la console : « access violation reading »

# ---- l'image mappée par sections (comme le chargeur : RVA → octets) ----------
e_lfanew = struct.unpack("<I", dll[0x3C:0x40])[0]
opt = e_lfanew + 4 + 20
magic = struct.unpack("<H", dll[opt:opt + 2])[0]
nb_sections = struct.unpack("<H", dll[e_lfanew + 6:e_lfanew + 8])[0]
taille_headers = struct.unpack("<I", dll[opt + 60:opt + 64])[0]
taille_image = struct.unpack("<I", dll[opt + 56:opt + 60])[0]
sections = []
sec_off = opt + struct.unpack("<H", dll[e_lfanew + 20:e_lfanew + 22])[0]
for i in range(nb_sections):
    s = dll[sec_off + 40 * i: sec_off + 40 * (i + 1)]
    nom = s[:8].rstrip(b"\x00").decode()
    vsize, vaddr, rsize, roff = struct.unpack("<IIII", s[8:24])
    sections.append((nom, vaddr, vsize, roff, rsize))
print(f"[PE] magic {magic:#x} (PE32+ attendu 0x20b) — {nb_sections} sections, "
      f"SizeOfImage {taille_image:#x}")
for n, va, vs, ro, rs in sections:
    print(f"  {nom if False else n:<10} va {va:#8x} vsize {vs:#8x} "
          f"raw {ro:#8x}+{rs:#x}")

def octets(rva: int, n: int) -> bytes:
    """l'équivalent EXACT de lire_octets(base, rva, n) : l'image par sections ;
    hors sections mappées → là où le terrain reçoit son ACCESS VIOLATION."""
    if rva < taille_headers:                   # les en-têtes : mappés tels quels
        return dll[rva:rva + n]
    for _, va, vs, ro, rs in sections:
        if va <= rva < va + max(vs, rs):
            d = rva - va
            if d + n <= rs:
                return dll[ro + d:ro + d + n]
            retour = dll[ro + d:ro + min(rs, d + n)]
            return retour + b"\x00" * (n - len(retour))   # le bourrage de fin
    raise MemoryError(f"HORS IMAGE : rva {rva:#x} (taille image {taille_image:#x})")

def u32(rva): return struct.unpack("<I", octets(rva, 4))[0]
def u16(rva): return struct.unpack("<H", octets(rva, 2))[0]
def chaine(rva, limite=64):
    brut = octets(rva, limite)
    fin = brut.find(b"\x00")
    return brut[:fin if fin >= 0 else limite].decode("ascii", errors="replace")

rva_exports = u32(opt + 112)
rva_imports = u32(opt + 120)
print(f"\n[tables] export @ {rva_exports:#x} — import @ {rva_imports:#x}")

# ---- la table d'imports : LES DESCRIPTEURS RÉELS ------------------------------
print("\n===== LA TABLE D'IMPORTS DE LA PIÈCE (les descripteurs réels) =====")
desc = rva_imports
i = 0
while i < 16:
    oft, _, fwd, nom_rva, iat = struct.unpack("<IIIII", octets(desc, 20))
    if oft == 0 and nom_rva == 0 and iat == 0:
        print(f"  [{i}] @+{desc:#x} LE TERMINATEUR (les cinq champs NULS)")
        break
    print(f"  [{i}] @+{desc:#x} «{chaine(nom_rva)}»  OFT {oft:#x} IAT {iat:#x}")
    desc += 20
    i += 1

# ---- LE REJEU DE LA TRAVERSÉE DU SCÉNARIO (le code de la ligne 213-232) -------
print("\n===== LE REJEU : la boucle du scénario, octet par octet =====")
FEUILLES_KIT = ("CreateFileW", "GetFileSizeEx", "SetFilePointerEx",
                "ReadFile", "CloseHandle", "GetLastError")
slots = {}
desc = rva_imports
iteration = 0
crash_reproduit = None
while True:
    nom_rva = u32(desc + 12)
    try:
        nom_dll = chaine(nom_rva) if True else ""
    except MemoryError as e:
        print(f"  itération {iteration}: desc+{12} = {nom_rva:#x} → "
              f"L'ADRESSE HORS IMAGE (le plantage du terrain)")
        crash_reproduit = nom_rva
        break
    print(f"  itération {iteration}: desc+{desc:#x} → Name rva {nom_rva:#x} "
          f"→ «{nom_dll}»")
    if not nom_dll:
        print("    (chaîne vide — la boucle s'arrêterait ICI)")
        break
    if "kernel32" in nom_dll.lower():
        ilt = u32(desc + 0)
        iat = u32(desc + 16)
        j = 0
        while True:
            entree = struct.unpack("<Q", octets(ilt + 8 * j, 8))[0] if ilt \
                else u32(iat + 8 * j)
            if not entree:
                break
            if not (entree >> 63):
                feuille = chaine((entree & 0xFFFFFFFF) + 2)
                if feuille in FEUILLES_KIT:
                    slots[feuille] = f"slot iat+{8*j} @+{iat + 8*j:#x}"
            j += 1
    desc += 20
    iteration += 1

print(f"\n[rejeu] les feuilles kernel32 résolues AVANT le plantage : "
      f"{len(slots)} → {sorted(slots)}")
print(f"[rejeu] le pas où la boucle quitte la table : "
      f"desc+{desc:#x}, l'itération {iteration}")

# ---- LA PREUVE D'ADRESSE -------------------------------------------------------
print("\n===== LA PREUVE D'ADRESSE (la console du terrain) =====")
if crash_reproduit is not None:
    adresse = BASE_TERRAIN + crash_reproduit
    print(f"  base terrain {BASE_TERRAIN:#x} + l'RVA bogué {crash_reproduit:#x} "
          f"= {adresse:#x}")
    print(f"  l'adresse du plantage à la console : {CRASH_TERRAIN:#x}")
    print(f"  [{'VERT — LE MÊME OCTET' if adresse == CRASH_TERRAIN else 'ÉCART'}]"
          f" la reproduction est EXACTE"
          if adresse == CRASH_TERRAIN else
          f"  [écart nommé] l'adresse rejouée diffère — à creuser")
else:
    print("  [!] le rejeu n'a pas planté — le diagnostic tient à l'examen seul")

# ---- CE QUE LA BOUCLE AURAIT DÛ LIRE AU TERMINATEUR ---------------------------
print("\n===== LE CŒUR DE LA FAUTE (le terminateur lu à l'RVA 0) =====")
nom_rva_term = u32(rva_imports + 20 * (iteration if crash_reproduit else i) + 12) \
    if False else None
# plus simple : à l'itération du terminator, montrer ce que lire_chaine(base,0) rend
print(f"  au terminate (Name rva = 0), lire_chaine(base, 0) lit l'en-tête DOS : "
      f"«{dll[:8]}» → la chaîne «{dll[:3].decode('ascii', errors='replace')}» "
      f"(NON VIDE — la boucle ne s'arrête JAMAIS là)")
