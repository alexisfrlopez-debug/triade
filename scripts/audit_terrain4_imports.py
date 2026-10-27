#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit PE du superviseur-terrain4 : tables d'imports vs slots IAT appelés.

Le terrain_20261027_162717.txt s'arrête après S03. Les premiers appels
d'API après S03 (extraction sup-37/sup-36) sont :
  - DeleteFileA  via slot 0x2330 (kernel32#3)  — PREMIER appel
  - CreateFileA   via slot 0x2e88 (kernel32#2)  — déjà prouvé (journal)
  - WriteFile     via slot 0x20b8 (kernel32#1)  — déjà prouvé (journal)
  - ReadFile      via slot 0x20f0 (kernel32#1)  — jamais appelé avant S04
Ce script liste les descripteurs d'import, leur IAT/INT, la section hôte,
et vérifie si chaque slot appelé est couvert par un lookup rempli.
"""

import struct
import sys
import pathlib

def rva_to_off(rva, sections):
    for name, vsz, va, rsz, roff in sections:
        if va <= rva < va + max(vsz, rsz):
            return roff + (rva - va)
    return None

def analyse(path, slots_attendus):
    data = pathlib.Path(path).read_bytes()
    print(f"\n===== {pathlib.Path(path).name} ({len(data)} octets) =====")
    e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
    assert data[e_lfanew:e_lfanew + 4] == b"PE\0\0"
    machine, nsec, _, _, _, optsz, _ = struct.unpack_from("<HHIIIHH", data, e_lfanew + 4)
    opt = e_lfanew + 24
    magic = struct.unpack_from("<H", data, opt)[0]
    pe32p = (magic == 0x20B)
    print(f"sections={nsec} optmagic={hex(magic)} machine={hex(machine)}")
    sec_off = opt + optsz
    sections = []
    for i in range(nsec):
        o = sec_off + 40 * i
        name = data[o:o + 8].rstrip(b"\0").decode(errors="replace")
        vsz, va, rsz, roff = struct.unpack_from("<IIII", data, o + 8)
        chars = struct.unpack_from("<I", data, o + 36)[0]
        sections.append((name, vsz, va, rsz, roff))
        print(f"  section {name:10s} va={va:#x} vsz={vsz:#x} raw={rsz:#x}@{roff:#x} chars={chars:#x}")
    # data directory : import = index 1, IAT = index 12
    if pe32p:
        dd_off = opt + 112
    else:
        dd_off = opt + 96
    imp_rva, imp_sz = struct.unpack_from("<II", data, dd_off + 8 * 1)
    iat_rva, iat_sz = struct.unpack_from("<II", data, dd_off + 8 * 12)
    print(f"  datadir IMPORT rva={imp_rva:#x} size={imp_sz:#x}")
    print(f"  datadir IAT    rva={iat_rva:#x} size={iat_sz:#x}")

    def read_cstr(off):
        end = data.index(b"\0", off)
        return data[off:end].decode(errors="replace")

    def section_of(rva):
        for name, vsz, va, rsz, roff in sections:
            if va <= rva < va + max(vsz, rsz):
                return name
        return "???"

    print("  --- descripteurs d'import ---")
    slots_couverts = {}
    d = rva_to_off(imp_rva, sections)
    idx = 0
    while d is not None:
        oft, ts, fwc, name_rva, iat = struct.unpack_from("<IIIII", data, d)
        if oft == 0 and name_rva == 0 and iat == 0:
            break
        name = read_cstr(rva_to_off(name_rva, sections))
        lookup_rva = oft or iat
        loff = rva_to_off(lookup_rva, sections)
        fns = []
        while True:
            (val,) = struct.unpack_from("<Q", data, loff)
            if val == 0:
                break
            if val & (1 << 63):
                fns.append(f"ord#{val & 0xFFFF}")
            else:
                n_off = rva_to_off(val & 0xFFFFFFFF, sections)
                hint = struct.unpack_from("<H", data, n_off)[0]
                fns.append(read_cstr(n_off + 2))
            loff += 8
        iat_off = rva_to_off(iat, sections)
        iat_end = iat_off + 8 * len(fns)
        print(f"  [{idx}] {name:12s} INT/OFT={lookup_rva:#x} IAT={iat:#x}"
              f" ({section_of(iat)}) n={len(fns)} ts={ts:#x}")
        for j, fn in enumerate(fns):
            slot_rva = iat + 8 * j
            mark = ""
            if slot_rva in slots_attendus and slots_attendus[slot_rva] == fn:
                mark = "  <== APPELE PAR LE CODE"
            elif slot_rva in slots_attendus:
                mark = f"  <== ATTENDU {slots_attendus[slot_rva]} ICI MAIS TROUVE {fn} !"
            print(f"        slot {slot_rva:#06x} ({section_of(slot_rva)}) {fn}{mark}")
            slots_couverts[slot_rva] = fn
        idx += 1
        d += 20
    print("  --- slots attendus ---")
    for slot, fn in sorted(slots_attendus.items()):
        got = slots_couverts.get(slot)
        if got == fn:
            print(f"  OK   {slot:#06x} {fn} (dans {section_of(slot)})")
        elif got is None:
            print(f"  ABSENT {slot:#06x} {fn} — SLOT JAMAIS COUVERT PAR UN IMPORT !")
        else:
            print(f"  DIFF {slot:#06x} attendu={fn} obtenu={got}")
    # vérifie les octets réels des slots dans le fichier (INT = valeurs non résolues)
    print("  --- octets de la zone 0x2300-0x2360 et 0x20a0-0x2100 (bruts) ---")
    for rva in (0x2330, 0x2e88, 0x20b8, 0x20f0, 0x20f8):
        off = rva_to_off(rva, sections)
        if off is None:
            print(f"  slot {rva:#x}: hors sections")
            continue
        val = struct.unpack_from("<Q", data, off)[0]
        print(f"  slot {rva:#x} (@file {off:#x}, section {section_of(rva)}) : {val:#018x}"
              f"  {'(zero -> saut sur 0 si non resolu)' if val == 0 else ''}")

if __name__ == "__main__":
    LIVR = "/home/z/my-project/triade/terrain/livraison"
    SLOTS = {
        0x2330: "DeleteFileA",   # sup-36 op2 — 1er appel après S03
        0x2e88: "CreateFileA",   # kernel32#2
        0x20b8: "WriteFile",     # kernel32#1
        0x20f0: "ReadFile",      # kernel32#1 — 1er appel après S04
        0x20f8: "CloseHandle",   # kernel32#1
    }
    analyse(f"{LIVR}/superviseur-terrain4.exe", SLOTS)
    analyse(f"{LIVR}/superviseur-terrain3-temoin.exe", SLOTS)
