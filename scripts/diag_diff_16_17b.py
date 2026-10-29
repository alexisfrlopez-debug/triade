#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE — D97bis : différentiel binaire superviseur-terrain16.exe vs
superviseur-terrain17b.exe, interprété par sections PE (RVA -> offset),
pour circonscrire la différence de comportement T2 (crash pendant .curl).

Sortie :
  - plages d'octets divergentes par section (RVA, longueur) ;
  - chaînes ASCII des zones de données divergentes (cmdlines curl,
    messages S2x, fixtures) ;
  - dump des cmdlines curl/powershell des deux binaires.
"""
import sys
import pathlib

import pefile

A = pathlib.Path("/home/z/my-project/download/superviseur-terrain16.exe")
B = pathlib.Path("/home/z/my-project/download/superviseur-terrain17b.exe")

SZ = 0x1000  # granularité d'affichage des plages divergentes


def sections(pe):
    out = []
    for s in pe.sections:
        out.append((s.VirtualAddress,
                    s.Misc_VirtualSize,
                    s.PointerToRawData,
                    s.SizeOfRawData,
                    s.Name.decode(errors="replace").rstrip("\x00")))
    return out


def rva_to_off(pe, rva):
    for va, vs, pr, sr, name in sections(pe):
        if va <= rva < va + max(vs, sr):
            return pr + (rva - va), name
    return None, None


def dump_diff():
    ba = A.read_bytes()
    bb = B.read_bytes()
    print(f"[diff] terrain16 : {len(ba)} o   terrain17b : {len(bb)} o")
    if len(ba) != len(bb):
        print("[diff] ATTENTION : tailles différentes — comparaison tronquée")
    n = min(len(ba), len(bb))
    pa = pefile.PE(data=ba, fast_load=True)
    pb = pefile.PE(data=bb, fast_load=True)

    # plages divergentes par offset fichier
    ranges = []
    start = None
    for i in range(n):
        if ba[i] != bb[i]:
            if start is None:
                start = i
        else:
            if start is not None:
                ranges.append((start, i))
                start = None
    if start is not None:
        ranges.append((start, n))
    print(f"[diff] {len(ranges)} plages divergentes sur {n} octets communs\n")

    # regroupement par section + granularité SZ
    cur_sec = None
    bucket = {}
    for s, e in ranges:
        rva_s, sec = rva_to_off(pa, s) if False else (None, None)
        # on raisonne en offset fichier -> RVA via les 2 PE (mêmes sections
        # attendues ; on prend le PE A comme référence de nommage)
        for va, vs, pr, sr, name in sections(pa):
            if pr <= s < pr + sr:
                rva = va + (s - pr)
                key = (name, (rva // SZ) * SZ)
                bucket.setdefault(key, [0, 10**9, []])
                bucket[key][0] = max(bucket[key][0], va + (e - pr))
                bucket[key][1] = min(bucket[key][1], rva)
                bucket[key][2].append((s, e))
                break
    for (name, base), (rva_end, rva_start, _) in sorted(bucket.items(),
                                                        key=lambda kv: kv[0][1]):
        print(f"  [{name:8s}] RVA 0x{rva_start:05X}-0x{rva_end:05X}"
              f"  ({rva_end - rva_start} o de plage)")

    # chaînes des plages divergentes (dans .rdata/.data des deux)
    print("\n[chaînes divergentes terrain16] (plages, >=6 caractères)")
    for (name, base), _ in sorted(bucket.items(), key=lambda kv: kv[0][1]):
        if name not in (".rdata", ".data"):
            continue
        for s, e in bucket[(name, base)][2]:
            extraire_chaines(ba, s, e, "16")
            extraire_chaines(bb, s, e, "17b")


def extraire_chaines(buf, s, e, tag):
    cur = bytearray()
    debut = None
    for i in range(s, e):
        c = buf[i]
        if 0x20 <= c < 0x7F:
            if debut is None:
                debut = i
            cur.append(c)
        else:
            if len(cur) >= 6:
                print(f"    [{tag} @0x{debut:05X}] {cur.decode('ascii')!r}")
            cur = bytearray()
            debut = None
    if len(cur) >= 6:
        print(f"    [{tag} @0x{debut:05X}] {cur.decode('ascii')!r}")


def dump_cmdlines(path, tag):
    buf = path.read_bytes()
    pe = pefile.PE(data=buf, fast_load=True)
    print(f"\n[cmdlines {tag}] chaînes contenant curl / powershell / proxy"
          f" / terrain_ / http (zones données, >=10 caractères)")
    cur = bytearray()
    debut = 0
    for i, c in enumerate(buf):
        if 0x20 <= c < 0x7F:
            if not cur:
                debut = i
            cur.append(c)
        else:
            if len(cur) >= 10:
                s = cur.decode("ascii")
                if any(k in s for k in ("curl", "powershell", "proxy.exe",
                                        "terrain_", "http://", "https://",
                                        "neverssl")):
                    off, sec = rva_to_off(pe, debut)
                    if off is None:
                        off, sec = rva_to_off(pe, debut) or (debut, "?")
                    loc = f"RVA 0x{debut:05X}" if off is None else f"off 0x{debut:05X}"
                    print(f"    [{loc}] {s!r}")
            cur = bytearray()
    # file offset brut pour repérage


if __name__ == "__main__":
    dump_diff()
    dump_cmdlines(A, "terrain16")
    dump_cmdlines(B, "terrain17b")
