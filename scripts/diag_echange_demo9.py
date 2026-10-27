#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Désassemble la séquence réseau de win-09 (demo.8 vs demo.9) :
localise la chaîne E5 « réseau : échange en échec », trouve le lea qui la
référence, puis le code qui mène au verdict de win-10 (test eax) et à E5."""

import re
import struct
import sys

from capstone import Cs, CS_ARCH_X86, CS_MODE_64

md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = False

RDATA_RVA, RDATA_FILE = 0x2000, 0x1200
TEXT2_RVA, TEXT2_FILE = 0x4000, 0x2C00
TEXT_RVA, TEXT_FILE = 0x1000, 0x200

def rva2off(rva):
    if 0x1000 <= rva < 0x2000:
        return TEXT_FILE + (rva - TEXT_RVA)
    if 0x2000 <= rva < 0x3000:
        return RDATA_FILE + (rva - RDATA_RVA)
    if 0x3000 <= rva < 0x4000:
        return 0x2200 + (rva - 0x3000)
    if 0x4000 <= rva < 0x5400:
        return TEXT2_FILE + (rva - TEXT2_RVA)
    return None

def off2rva(off):
    for lo, hi, rva0, off0 in ((0x200, 0x1200, 0x1000, 0x200),
                               (0x1200, 0x2200, 0x2000, 0x1200),
                               (0x2200, 0x2C00, 0x3000, 0x2200),
                               (0x2C00, 0x4040, 0x4000, 0x2C00)):
        if lo <= off < hi:
            return rva0 + (off - off0)
    return None

def rva_chaine(d, s):
    """RVA d'une chaîne UTF-16LE (sans exiger de terminateur précis)."""
    needle = s.encode("utf-16-le")
    i = d.find(needle)
    while i != -1:
        # doit commencer sur frontière de chaîne (précédé par 0 ou aligné)
        rva = off2rva(i)
        if rva and 0x2000 <= rva < 0x3000:
            # le caractère précédent (2 octets avant) doit être un NUL (fin de chaîne)
            if i >= 2 and d[i-2:i] == b"\x00\x00":
                return rva
        i = d.find(needle, i + 1)
    return None

def scan_lea(d, cible_rva, zones=((0x1000, 0x2000), (0x4000, 0x5400))):
    """Tous les lea reg, [rip+X] pointant sur cible_rva."""
    res = []
    for lo, hi in zones:
        off = rva2off(lo)
        code = d[off:rva2off(hi)]
        for ins in md.disasm(code, lo):
            if ins.mnemonic == "lea" and "rip" in ins.op_str:
                m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", ins.op_str)
                if m:
                    sign = 1 if m.group(1) == "+" else -1
                    c = ins.address + ins.size + sign * int(m.group(2), 16)
                    if c == cible_rva:
                        res.append((ins.address, ins.op_str.split(",")[0].strip()))
    return res

def dump_zone(d, start, length, marqueurs=()):
    off = rva2off(start)
    code = d[off:off + length]
    for ins in md.disasm(code, start):
        m = ""
        for (a, lab) in marqueurs:
            if ins.address == a:
                m = f"   <<<<< {lab}"
        print(f"    {ins.address:#07x}: {ins.mnemonic:9} {ins.op_str}{m}")

for nom, chemin in (("demo.8 (terrain OK)", "/tmp/demo8.exe"),
                    ("demo.9 (terrain KO)", "/tmp/demo9.exe")):
    d = open(chemin, "rb").read()
    print(f"\n{'='*70}\n===== {nom} =====")
    chaines = {}
    for s in ("réseau : échange en échec", "écho réseau : aller-retour exact",
              "client : connecté", "serveur : écoute 127.0.0.1:25000",
              "patch en production : MAJUSCULES",
              "retour arrière : identité confirmée",
              "boucle § 5 complète - DÉMO OK"):
        r = rva_chaine(d, s)
        chaines[s] = r
        print(f"  {s!r:45} -> {'@' + hex(r) if r else 'ABSENTE'}")

    e5 = chaines["réseau : échange en échec"]
    echo_ok = chaines["écho réseau : aller-retour exact"]
    if e5 is None:
        print("  [!] chaîne E5 introuvable")
        continue
    refs = scan_lea(d, e5)
    refs_ok = scan_lea(d, echo_ok) if echo_ok else []
    print(f"  E5 référencée par : {[(hex(a), r) for a, r in refs]}")
    print(f"  J_ECHO_OK référencée par : {[(hex(a), r) for a, r in refs_ok]}")
    if refs:
        a = refs[0][0]
        print(f"\n  --- fenêtre de code autour du verdict échange 1 "
              f"[{a-0x100:#x} .. {a+0x30:#x}] ---")
        dump_zone(d, a - 0x100, 0x140,
                  marqueurs=[(a, "lea E5 (échec)")] +
                  [(x, "lea J_ECHO_OK") for x, _ in refs_ok])
