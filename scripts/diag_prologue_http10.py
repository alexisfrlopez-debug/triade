#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIADE — Diagnostic du prologue de session http-10 (D63).

Théorie à tester : le cadre de session http-10 (0x7100 o) est alloué d'un
coup (sub rsp, 0x7100) dans un thread neuf. Windows ne commet qu'ENVIRON UNE
PAGE de pile à la naissance d'un thread (le reste : réservé + guard page).
Un accès au BAS du cadre SANS avoir touché la guard page d'abord (stack
probing, le __chkstk des compilateurs) lève c00000fd (stack overflow) →
mort DU PROCESSUS ENTIER (exception de thread) → RST sur la socket cliente
(curl code 56), port 25000 libéré (curl suivant code 7), tuyau muet après
la bannière (S26 = 1 ligne), jamais d'« arret ».

L'émulation unicorn de l'oracle m3 mappe la pile en entier (pas de guard
page) → le défaut est INVISIBLE en émulation ; M2 réel (fil echo tcp-09)
avait un petit cadre → jamais vu en réel non plus. Le proxy M3 est le
PREMIER thread à grand cadre de la lignée.

Ce script désassemble :
  1. l'entrée de http-10 (rva 0x5580) — les ~40 premières instructions :
     prologue, ordre push/sub/premières écritures ;
  2. l'entrée de http-11 (console, rva 0x5D80) — pour contraste (petit
     cadre, thread aussi) ;
  3. l'entrée de tcp-09 (fil echo M2, 0x4400 ? NON — tcp-09 n'est PAS
     embarqué ; on contraste avec tcp-11 journal 0x4B00, appelé par le
     thread principal).

Usage : python3 scripts/diag_prologue_http10.py
"""

import importlib.util
import pathlib
import sys

import capstone
import pefile

REPO = pathlib.Path(__file__).resolve().parents[1]


def _charger(nom, chemin):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


LT = _charger("layout_m3", REPO / "m3" / "layout.py")

EXE = REPO / "m3" / "proxy.exe"
BASE = LT.IMAGE_BASE

CIBLES = [
    ("http-10 session (thread)", 0x5580, 48),
    ("http-11 console (thread)", 0x5D80, 24),
    ("http-12 orchestrateur (principal)", 0x1800, 24),
]


def rva_to_off(pe, rva):
    for s in pe.sections:
        if s.VirtualAddress <= rva < s.VirtualAddress + s.Misc_VirtualSize:
            return s.PointerToRawData + (rva - s.VirtualAddress)
    raise ValueError(f"RVA {rva:#x} hors sections")


def main():
    data = EXE.read_bytes()
    pe = pefile.PE(str(EXE), fast_load=True)
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    md.detail = False

    for titre, rva, n in CIBLES:
        off = rva_to_off(pe, rva)
        code = data[off:off + 256]
        print(f"=== {titre} — @{rva:#x} ===")
        vu = 0
        for ins in md.disasm(code, BASE + rva):
            print(f"  {ins.address - BASE:#06x}: {ins.mnemonic:<8} {ins.op_str}")
            vu += 1
            if vu >= n:
                break
        print()

    # Vérification PE : réserve/commit de pile dans le header optionnel.
    print(f"=== Pile PE (SizeOfStackReserve / SizeOfStackCommit) ===")
    print(f"  réserve : {pe.OPTIONAL_HEADER.SizeOfStackReserve:#x} octets")
    print(f"  commit  : {pe.OPTIONAL_HEADER.SizeOfStackCommit:#x} octets")
    return 0


if __name__ == "__main__":
    sys.exit(main())
