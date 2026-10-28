#!/usr/bin/env python3
"""diag_structure_m4.py — Extrait, pour chaque bloc M4 assemblé à son RVA exact,
les cibles d'appel (IAT / blocs directs / internes) et les cibles de données RIP.
Sert de vérité terrain pour écrire les tables d'autorisation de l'oracle
structurel de build_m4.py (I1/I2/I5)."""

from __future__ import annotations

import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
TRIADE = os.path.join(os.path.dirname(ICI), "triade")
sys.path.insert(0, os.path.join(TRIADE, "m4"))
sys.path.insert(0, os.path.join(TRIADE, "m4", "outils"))

import capstone  # noqa: E402
from keystone import Ks, KS_ARCH_X86, KS_MODE_64  # noqa: E402

import layout as L  # noqa: E402
import harnais_session_r2 as SR2  # noqa: E402

KS = Ks(KS_ARCH_X86, KS_MODE_64)
CS = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

# (clé, fichier notation, rva, chemin de base ou None pour m4/notation)
M4 = [
    ("tls-01", "tls-01-nom-utf16", 0x6000, None),
    ("tls-02", "tls-02-verdicts", 0x6080, None),
    ("tls-03", "tls-03-jetons", 0x6180, None),
    ("tls-04", "tls-04-poignee", 0x62C0, None),
    ("tls-05", "tls-05-cles", 0x65C0, None),
    ("tls-06", "tls-06-emission", 0x6740, None),
    ("tls-07", "tls-07-reception", 0x6A40, None),
    ("tls-08", "tls-08-session", 0x6D40, None),
    ("http-08-R2", "http-08-cible-r2", 0x7340, None),
    ("http-10-R2", "http-10-session-r2", 0x74C0, None),
]


def cible_rip(insn) -> int | None:
    m = re.search(r"\[rip \+ (0x[0-9a-f]+)\]", insn.op_str)
    if m:
        return insn.address + insn.size + int(m.group(1), 16)
    m = re.search(r"\[rip - (0x[0-9a-f]+)\]", insn.op_str)
    if m:
        return insn.address + insn.size - int(m.group(1), 16)
    return None


def main() -> int:
    slots_iat = dict(L.IAT_SLOTS)          # kernel32 + ws2_32
    slots_iat |= dict(L.IAT_SEC32_SLOTS)   # secur32
    # adresses des blocs hérités + M4 (pour classifier les appels directs)
    adresses = {
        0x1040: "hello-02", 0x1080: "hello-03", 0x1100: "libc-01",
        0x1180: "libc-02", 0x1200: "libc-03", 0x1280: "libc-04",
        0x13C0: "libc-07", 0x4000: "tcp-01", 0x4100: "tcp-02",
        0x4140: "tcp-03", 0x4180: "tcp-04", 0x41C0: "tcp-05",
        0x4300: "tcp-06", 0x4B00: "tcp-11", 0x4400: "tcp-13",
        0x4C00: "http-01", 0x4C80: "http-02", 0x4E80: "http-03",
        0x4F40: "http-04", 0x5080: "http-05", 0x5140: "http-06",
        0x5200: "http-07", 0x5380: "http-08-R1", 0x54C0: "http-09",
        0x5580: "http-10-R1", 0x5D80: "http-11", 0x1800: "http-12",
    }
    for cle, fichier, rva, chemin_base in M4:
        chemin = (os.path.join(TRIADE, "m4", "notation", fichier + ".asm")
                  if chemin_base is None else os.path.join(chemin_base, fichier + ".asm"))
        octets, declare = SR2.octets_notation(KS, fichier, rva, chemin=chemin)
        insns = list(CS.disasm(octets, rva))
        internes = {i.address for i in insns}
        appels_iat, appels_blocs, internes_ct, donnees = [], [], 0, []
        for i in insns:
            if i.mnemonic == "call":
                if "rip" in i.op_str:
                    c = cible_rip(i)
                    if c in slots_iat:
                        appels_iat.append((slots_iat[c], hex(i.address)))
                    else:
                        appels_iat.append((f"RIP?{c:#x}", hex(i.address)))
                elif i.op_str.startswith("0x"):
                    c = int(i.op_str, 16)
                    if c in internes and c != rva:
                        internes_ct += 1
                    elif c in adresses:
                        appels_blocs.append((adresses[c], hex(i.address)))
                    else:
                        appels_blocs.append((f"?{c:#x}", hex(i.address)))
                else:
                    internes_ct += 1  # call étiquette (registre/relatif interne)
            c = cible_rip(i)
            if c is not None and i.mnemonic != "call":
                etiquette = slots_iat.get(c) or ("bloc:" + adresses.get(c, hex(c)))
                donnees.append((etiqueta := etiquette, hex(i.address)))
        print(f"=== {cle} ({fichier}) — {len(octets)} o, {len(insns)} instructions")
        print(f"  IAT        : {sorted(set(n for n, _ in appels_iat))}")
        print(f"  blocs      : {sorted(set(n for n, _ in appels_blocs))}")
        print(f"  appels internes : {internes_ct}")
        dedup = {}
        for n, a in donnees:
            dedup.setdefault(n, []).append(a)
        print(f"  données RIP: ")
        for n, addrs in sorted(dedup.items()):
            print(f"    {n}  ({len(addrs)}x)  ex @{addrs[0]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
