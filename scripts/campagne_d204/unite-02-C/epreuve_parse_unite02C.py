#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""epreuve_parse_unite02C.py — L'ÉPREUVE DE LA DÉCOUVERTE : le parse v2 (le
scénario réparé de la 286 — le terminateur au CHAMP Name, les gardes
fail-closed) exécuté CONTRE LA PIÈCE LOUVE-02-C.DLL, l'image mappée par
sections comme au terrain (RVA → offset fichier, la table des sections
lue). Les SIX exports et les SIX feuilles kernel32 doivent être lus — la
pièce C appelle SetFilePointerEx (l'écart nommé du kit 01 n'existe plus)."""
import pathlib
import struct
import sys

UNITE = pathlib.Path(__file__).resolve().parent
PIECE = UNITE / "epreuves" / "loupe-02-c.dll"

b = PIECE.read_bytes()

# ---- l'image mappée par sections (RVA → offset fichier, comme le chargeur) ----
e_lfanew = struct.unpack_from("<I", b, 0x3C)[0]
nb_sections = struct.unpack_from("<H", b, e_lfanew + 6)[0]
taille_opt = struct.unpack_from("<H", b, e_lfanew + 20)[0]
sections = []
for k in range(nb_sections):
    o = e_lfanew + 24 + taille_opt + k * 40
    va = struct.unpack_from("<I", b, o + 12)[0]
    vs = struct.unpack_from("<I", b, o + 8)[0]
    ra = struct.unpack_from("<I", b, o + 20)[0]
    sections.append((va, vs, ra))

def depuis_rva(rva: int, n: int) -> bytes:
    for va, vs, ra in sections:
        if va <= rva < va + vs:
            off = ra + (rva - va)
            assert off + n <= ra + vs, f"la lecture déborde la section @ {rva:#x}"
            return b[off:off + n]
    if rva < sections[0][0]:            # l'en-tête : l'identité RVA ↔ offset
        return b[rva:rva + n]
    raise SystemExit(f"REFUS : la RVA {rva:#x} hors des sections")

def lire_u32(rva): return struct.unpack("<I", depuis_rva(rva, 4))[0]
def lire_u16(rva): return struct.unpack("<H", depuis_rva(rva, 2))[0]
def lire_chaine(rva, limite=64):
    # la lecture souple : la chaîne NUL-terminée peut vivre au bord de
    # section (à l'image mappée, la section suivante suit de contiguïté)
    for va, vs, ra in sections:
        if va <= rva < va + vs:
            off = ra + (rva - va)
            brut = b[off:min(off + limite, len(b))]
            fin = brut.find(b"\x00")
            return brut[:fin if fin >= 0 else limite].decode(
                "ascii", errors="replace")
    raise SystemExit(f"REFUS : la RVA {rva:#x} hors des sections")

opt = e_lfanew + 4 + 20
rva_exports = lire_u32(opt + 112)
rva_imports = lire_u32(opt + 120)
print(f"[pièce] {len(b):,} o — export dir @{rva_exports:#x}, "
      f"import dir @{rva_imports:#x}")

# ---- LA DÉCOUVERTE PAR LA TABLE D'EXPORTS (le parse VERBATIM du v2) ----------
noms_vus, rva_par_nom = [], {}
nb_noms = lire_u32(rva_exports + 24)
tab_fonctions = lire_u32(rva_exports + 28)
tab_noms = lire_u32(rva_exports + 32)
tab_ordinaux = lire_u32(rva_exports + 36)
for i in range(nb_noms):
    nom = lire_chaine(lire_u32(tab_noms + 4 * i))
    ordinal = lire_u16(tab_ordinaux + 2 * i)
    rva_par_nom[nom] = lire_u32(tab_fonctions + 4 * ordinal)
    noms_vus.append(nom)
print(f"[découverte] {nb_noms} exports : "
      + ", ".join(f"{n} @+{rva_par_nom[n]:#x}" for n in noms_vus))
assert set(rva_par_nom) == {"loupe_01_ouvrir", "loupe_02_lire",
                            "loupe_03_fermer", "cadre", "journal",
                            "panneau"}, rva_par_nom

# ---- LA TRAVERSÉE DES IMPORTS (le parse v2 — le terminateur au CHAMP) --------
taille_image = lire_u32(opt + 56)
slots = {}
desc = rva_imports
for _garde in range(64):
    nom_rva = lire_u32(desc + 12)
    if not nom_rva:                      # LE TERMINATEUR : le champ NUL
        break
    if nom_rva >= taille_image:          # la garde fail-closed
        raise SystemExit(f"REFUS : un Name hors image @{nom_rva:#x}")
    nom_dll = lire_chaine(nom_rva)
    if not nom_dll:
        break
    if "kernel32" in nom_dll.lower():
        ilt = lire_u32(desc + 0)
        iat = lire_u32(desc + 16)
        j = 0
        while True:
            entree = struct.unpack(
                "<Q", depuis_rva(ilt + 8 * j, 8))[0] if ilt \
                else lire_u32(iat + 8 * j)
            if not entree:
                break
            if not (entree >> 63):
                feuille = lire_chaine((entree & 0xFFFFFFFF) + 2)
                slots[feuille] = iat + 8 * j
            j += 1
    desc += 20
else:
    raise SystemExit("REFUS : la table d'imports sans terminateur")
print(f"[imports] kernel32 : {', '.join(sorted(slots))} "
      f"({len(slots)} feuilles aux slots réels)")
assert {"CreateFileW", "GetFileSizeEx", "SetFilePointerEx", "ReadFile",
        "CloseHandle", "GetLastError"} <= set(slots), sorted(slots)
assert all(slots[f] for f in slots)

print("\nLE PARSE v2 (287) LIT LA PIÈCE : les SIX exports (loupe_02_lire "
      "comprise, journal DONNÉE) et les SIX feuilles kernel32 — "
      "SetFilePointerEx PRÉSENTE cette fois (la pièce l'appelle à chaque "
      "lecture, l'écart nommé du kit 01 n'existe plus) — VERT")
