#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_decouverte.py — LE TEST POSIX DE LA DÉCOUVERTE PE du scénario du
bras C : les mêmes lectures (les tables d'exports et d'imports de la
pièce), l'image mappée simulée par la cartographie des sections du
FICHIER. VERT : les QUATRE exports (les deux fonctions, les deux
DONNÉES) et les CINQ feuilles kernel32 aux slots réels de l'IAT."""
import pathlib
import struct
import sys

ICI = pathlib.Path(__file__).resolve().parent
DLL = ICI / "epreuves" / "loupe-01-c.dll"

d = DLL.read_bytes()
e = struct.unpack_from("<I", d, 0x3C)[0]
assert d[e:e + 4] == b"PE\x00\x00"
nb_sec = struct.unpack_from("<H", d, e + 6)[0]
tail_opt = struct.unpack_from("<H", d, e + 20)[0]
print(f"[entêtes] e_lfanew={e:#x}, {nb_sec} sections, "
      f"l'optionnel {tail_opt:#x} o")

# la cartographie RVA → offset fichier (l'image mappée simulée)
secs = []
for i in range(nb_sec):
    s = e + 24 + tail_opt + 40 * i
    vsize, vaddr, rsize, raddr = struct.unpack_from("<IIII", d, s + 8)
    secs.append((vaddr, max(vsize, rsize), raddr))
taille_entetes = struct.unpack_from("<I", d, e + 24 + 60)[0]


def lit(rva: int, n: int) -> bytes:
    if rva < taille_entetes:
        return d[rva:rva + n]
    for vaddr, etendue, raddr in secs:
        if vaddr <= rva < vaddr + etendue:
            o = raddr + (rva - vaddr)
            if o + n <= len(d):
                return d[o:o + n]
    raise KeyError(hex(rva))


u32 = lambda r: struct.unpack("<I", lit(r, 4))[0]
u16 = lambda r: struct.unpack("<H", lit(r, 2))[0]


def chaine(r: int) -> str:
    brut = lit(r, 256)
    fin = brut.find(b"\x00")
    return brut[:fin if fin >= 0 else 256].decode("ascii",
                                                  errors="replace")


# --- les répertoires de données ------------------------------------------------
opt = e + 24
rva_exports = struct.unpack_from("<I", d, opt + 112)[0]
rva_imports = struct.unpack_from("<I", d, opt + 120)[0]
print(f"[répertoires] export @+{rva_exports:#x}, import @+{rva_imports:#x}")

# --- LA TABLE D'EXPORTS (Name +12, Base +16, NB fonctions +20, NB noms +24,
#     Functions +28, Names +32, Ordinals +36) ----------------------------------
nb_noms = u32(rva_exports + 24)
tab_fct = u32(rva_exports + 28)
tab_noms = u32(rva_exports + 32)
tab_ord = u32(rva_exports + 36)
print(f"[exports] {nb_noms} noms ; fonctions @+{tab_fct:#x}, "
      f"noms @+{tab_noms:#x}, ordinaux @+{tab_ord:#x}")
rva_par_nom = {}
for i in range(nb_noms):
    rva_nom = u32(tab_noms + 4 * i)
    nom = chaine(rva_nom)
    rva_f = u32(tab_fct + 4 * u16(tab_ord + 2 * i))
    rva_par_nom[nom] = rva_f
    print(f"  {nom:18s} (le nom @+{rva_nom:#x}) → la donnée/la fonction "
          f"@+{rva_f:#x}")
assert set(rva_par_nom) == {"cadre", "loupe_01_ouvrir",
                            "loupe_03_fermer", "panneau"}, rva_par_nom

# --- LA TABLE D'IMPORTS (les six du kit — celles déclarées par la pièce) ------
FEUILLES = ("CreateFileW", "GetFileSizeEx", "SetFilePointerEx",
            "ReadFile", "CloseHandle", "GetLastError")
slots = {}
desc = rva_imports
for tour in range(32):
    rva_nom_dll = u32(desc + 12)
    if rva_nom_dll == 0:
        break
    nom_dll = chaine(rva_nom_dll)
    if "kernel32" in nom_dll.lower():
        ilt = u32(desc + 0)
        iat = u32(desc + 16)
        print(f"[imports] {nom_dll} : ILT @+{ilt:#x}, IAT @+{iat:#x}")
        j = 0
        while True:
            entree = struct.unpack("<Q", lit(ilt + 8 * j, 8))[0]
            if entree == 0:
                break
            if not (entree >> 63):
                feuille = chaine((entree & 0xFFFFFFFF) + 2)
                if feuille in FEUILLES:
                    slots[feuille] = iat + 8 * j
            j += 1
    desc += 20
print("[slots]", {k: hex(v) for k, v in sorted(slots.items())})
assert set(slots) == {"CreateFileW", "GetFileSizeEx", "ReadFile",
                      "CloseHandle", "GetLastError"}, sorted(slots)
print("[VERT] la découverte trouve les QUATRE exports et les CINQ feuilles "
      "aux slots réels (SetFilePointerEx : l'écart nommé du bras C)")
sys.exit(0)
