#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIADE D52j — parseur STRICT (v2, offsets corrects) de .rsrc.

Layout reel IMAGE_RESOURCE_DIRECTORY :
  +0  Characteristics  u32
  +4  TimeDateStamp    u32
  +8  MajorVersion     u16
  +10 MinorVersion     u16
  +12 NumberOfNamedEntries u16
  +14 NumberOfIdEntries    u16
  +16 entrees (Name u32, OffsetToData u32) x N
Feuille : OffsetToData & 0x7FFFFFFF -> IMAGE_RESOURCE_DATA_ENTRY :
  DataRVA u32, Taille u32, CodePage u32, Reserve u32
"""

import pathlib
import struct

d = pathlib.Path("/home/z/my-project/triade/terrain/superviseur.exe").read_bytes()
RSRC_RVA, RSRC_SZ, RSRC_FILE = 0x7000, 0x800, 0x5C00
problemes = []
feuilles = []


def lire_dir(off, chemin, niveau):
    if off & 0x80000000 or off >= RSRC_SZ:
        problemes.append(f"offset dir invalide @{off:#x}")
        return
    base = RSRC_FILE + off
    car, tds, maj, mine, nb_nom, nb_id = struct.unpack_from("<IIHHHH", d, base)
    print("  " * niveau + f"[dir @{off:#x}] car={car:#x} tds={tds:#x} "
          f"ver={maj}.{mine} noms={nb_nom} ids={nb_id}")
    n = nb_nom + nb_id
    if n * 8 + 16 + off > RSRC_SZ:
        problemes.append(f"table d'entrees deborde @{off:#x} ({n} entrees)")
        return
    for i in range(n):
        nom_raw, val = struct.unpack_from("<II", d, base + 16 + 8 * i)
        if nom_raw & 0x80000000:
            stro = nom_raw & 0x7FFFFFFF
            if stro + 2 > RSRC_SZ:
                problemes.append(f"nom hors section @{stro:#x}")
                continue
            ln = struct.unpack_from("<H", d, RSRC_FILE + stro)[0]
            if ln > 128 or stro + 2 + 2 * ln > RSRC_SZ:
                problemes.append(f"nom UNICODE invalide @{stro:#x}")
                continue
            s = d[RSRC_FILE + stro + 2:RSRC_FILE + stro + 2 + 2 * ln]
            label = s.decode("utf-16-le", "replace")
        else:
            label = str(nom_raw)
        if val & 0x80000000:
            sous = val & 0x7FFFFFFF
            print("  " * niveau + f"  [{label}] -> dir @{sous:#x}")
            lire_dir(sous, chemin + [label], niveau + 1)
        else:
            if val + 16 > RSRC_SZ:
                problemes.append(f"data-entry hors section @{val:#x}")
                continue
            rva_data, taille, cp, rs = struct.unpack_from("<IIII",
                                                          d, RSRC_FILE + val)
            ok = RSRC_RVA <= rva_data and rva_data + taille <= RSRC_RVA + RSRC_SZ
            print("  " * niveau + f"  [{label}] DATA @{val:#x} : "
                  f"RVA={rva_data:#x} taille={taille:#x} cp={cp} "
                  f"{'OK' if ok else '!!! HORS .rsrc'}")
            if not ok:
                problemes.append(f"donnees {'/'.join(chemin+[label])} : "
                                 f"RVA {rva_data:#x}+{taille:#x} hors bornes")
            else:
                feuilles.append((chemin + [label], rva_data, taille))


lire_dir(0, [], 0)
print()
for chemin, rva, taille in feuilles:
    brut = d[RSRC_FILE + (rva - RSRC_RVA):RSRC_FILE + (rva - RSRC_RVA) + taille]
    if "24" in chemin:
        print("=== MANIFESTE (brut, {0} octets) ===".format(taille))
        print(brut.decode("utf-8", "replace"))
        print("=== fin manifeste ; dernier octet = {:#x}, "
              "NUL terminal present : {}".format(brut[-1], brut.endswith(b'\x00') or brut.endswith(b'\x00\x00')))
    if "16" in chemin:
        print(f"=== VERSIONINFO ({taille} octets) — decodage VS_FIXEDFILEINFO ===")
        # chercher la signature 0xFEEF04BD
        p = brut.find(b"\xbd\x04\xef\xfe")
        print(f"  signature @+{p} : " + ("OK" if p >= 0 else "ABSENTE !!"))
        if p >= 0:
            (sig, fvmaj, fvmin, fvrev, fvbuild, pvmaj, pvmin, pvrev,
             pvbuild) = struct.unpack_from("<IHHHHHHHH", brut, p)
            print(f"  FileVersion = {fvmaj}.{fvmin}.{fvrev}.{fvbuild}")
            print(f"  ProdVersion = {pvmaj}.{pvmin}.{pvrev}.{pvbuild}")

print()
print("=== hex .rsrc premiers 320 octets ===")
for i in range(0, 320, 32):
    ligne = d[RSRC_FILE + i:RSRC_FILE + i + 32]
    print(f"  +{i:#05x} : {ligne.hex(' ')}")

print()
if problemes:
    print("!!! PROBLEMES DETECTES :")
    for p in problemes:
        print("   -", p)
else:
    print("arbre .rsrc : structure et bornes VALIDES")
