#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Autopsie différentielle des tables d'import : loupe.exe dev.7 vs demo.exe 0.3.0.

LE BUT : la vitrine de dev.7 meurt encore 0xC0000005 alors que le contrôle
D54 du scénario (les plages FirstThunk marchées) est VERT — le différentiel
contre la lignée prouvée (demo.exe, la fenêtre VÉCUE au terrain) doit nommer
ce que le contrôle ne voit pas : les champs des DESCRIPTEURS (OFT/Name/FT),
les chaînes de noms, les caractéristiques de section, le BASERELOC.
"""
import struct
import sys

def rva_off(sections, rva):
    """RVA -> offset fichier (None si hors sections)."""
    for (va, vs, raw, ptr, car, nom) in sections:
        if va <= rva < va + vs:
            return ptr + (rva - va)
    return None

def parse(path):
    d = open(path, "rb").read()
    e_lfanew = struct.unpack_from("<I", d, 0x3C)[0]
    assert d[e_lfanew:e_lfanew + 4] == b"PE\0\0"
    coff = e_lfanew + 4
    nsec, tds = struct.unpack_from("<H", d, coff)[0], struct.unpack_from("<H", d, coff + 2)[0] if False else (struct.unpack_from("<H", d, coff)[0],)
    machine, nsec2, tds2, ptrsym, nsym, opt_size, chars = struct.unpack_from("<HHIIIHH", d, coff)
    opt = coff + 20
    magic = struct.unpack_from("<H", d, opt)[0]
    entry = struct.unpack_from("<I", d, opt + 16)[0]
    base = struct.unpack_from("<Q", d, opt + 24)[0] if magic == 0x20b else struct.unpack_from("<I", d, opt + 28)[0]
    # data directories
    ndir = struct.unpack_from("<I", d, opt + (108 if magic == 0x20b else 92))[0]
    dir_off = opt + (112 if magic == 0x20b else 96)
    dirs = []
    for i in range(ndir):
        rva, sz = struct.unpack_from("<II", d, dir_off + 8 * i)
        dirs.append((rva, sz))
    # sections
    sec_off = opt + opt_size
    sections = []
    for i in range(nsec2):
        s = sec_off + 40 * i
        nom = d[s:s + 8].rstrip(b"\0").decode("ascii", "replace")
        vs = struct.unpack_from("<I", d, s + 8)[0]
        va = struct.unpack_from("<I", d, s + 12)[0]
        raw = struct.unpack_from("<I", d, s + 16)[0]
        ptr = struct.unpack_from("<I", d, s + 20)[0]
        car = struct.unpack_from("<I", d, s + 36)[0]
        sections.append((va, vs, raw, ptr, car, nom))
    return d, magic, entry, base, dirs, sections

def cstr(d, off):
    fin = d.find(b"\0", off)
    return d[off:fin].decode("ascii", "replace")

def walk_imports(path, etiquette):
    d, magic, entry, base, dirs, sections = parse(path)
    print(f"=== {etiquette} ({path.split('/')[-1]}) ===")
    print(f"magic {'PE32+' if magic == 0x20b else 'PE32'} · entry RVA {entry:#x} · base {base:#x}")
    print("sections :")
    for (va, vs, raw, ptr, car, nom) in sections:
        flags = "".join([
            "R" if car & 0x40000000 else "-",
            "W" if car & 0x80000000 else "-",
            "X" if car & 0x20000000 else "-",
        ])
        print(f"  {nom:<10} VA {va:#8x} VS {vs:#8x} RAW {raw:#8x} PTR {ptr:#8x} {flags} car {car:#010x}")
    irva, isz = dirs[1]
    print(f"dir[1] IMPORT : RVA {irva:#x}, taille {isz} ({isz // 20} descripteurs + sentinelle)")
    rva, sz = dirs[5]
    print(f"dir[5] BASERELOC : RVA {rva:#x}, taille {sz}")
    off = rva_off(sections, irva)
    print(f"\ndescripteurs (format : i · OFT · TimeDate · FwdChain · NameRVA→nom · FirstThunk) :")
    i = 0
    resultats = []
    while True:
        o = off + 20 * i
        oft, tds, fwd, namerva, ft = struct.unpack_from("<IIIII", d, o)
        if oft == 0 and namerva == 0 and ft == 0:
            print(f"  [{i}] SENTINELLE (tout zéro) — fin")
            break
        noff = rva_off(sections, namerva)
        nom = cstr(d, noff) if noff is not None else "??HORS-SECTIONS??"
        print(f"  [{i}] OFT {oft:#010x} · tds {tds:#x} · fwd {fwd:#x} · "
              f"Name {namerva:#x} → « {nom} » · FT {ft:#010x}")
        resultats.append((nom, oft, ft))
        i += 1
        if i > 12:
            print("  (arrêt : plus de 12)")
            break
    # marche les plages OFT et FT de chaque descripteur
    print("\nmarche des plages (OFT puis FT), compte jusqu'au NULL :")
    for (nom, oft, ft) in resultats:
        for etiquette_plage, rva_plage in (("OFT", oft), ("FT", ft)):
            if rva_plage == 0:
                print(f"  {nom} {etiquette_plage} : ZÉRO (le chargeur marchera l'AUTRE plage)")
                continue
            o = rva_off(sections, rva_plage)
            n = 0
            entrees = []
            while True:
                v = struct.unpack_from("<Q", d, o + 8 * n)[0]
                if v == 0:
                    break
                entrees.append(v)
                n += 1
                if n > 64:
                    break
            # détail : chaque entrée est-elle un RVA de nom (pair, pointe vers hint+nom) ?
            details = []
            for v in entrees[:4]:
                if v & (1 << 63):
                    details.append(f"ORD#{v & 0xFFFF}")
                else:
                    eo = rva_off(sections, v)
                    if eo is None:
                        details.append(f"{v:#x}??HORS??")
                    else:
                        hint = struct.unpack_from("<H", d, eo)[0]
                        details.append(f"{v:#x}→« {cstr(d, eo + 2)} » (hint {hint})")
            suf = " …" if len(entrees) > 4 else ""
            print(f"  {nom} {etiquette_plage} @{rva_plage:#x} : {n} entrées — "
                  f"{'; '.join(details)}{suf}")
    return d, dirs, sections

if __name__ == "__main__":
    walk_imports("/home/z/my-project/run8/loupe.exe", "LOUPE dev.7 (la vitrine morte)")
    print()
    walk_imports("/home/z/my-project/triade/demo/demo.exe", "DEMO 0.3.0 (la lignée prouvée)")
