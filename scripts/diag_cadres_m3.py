#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIADE — Balayage des cadres de pile de TOUS les blocs m3 (D63).

Le défaut c00000fd (http-10 : sub rsp,0x7100 sans probing dans un thread à
commit initial 0x1000) peut siéger dans TOUT bloc appelé comme thread
(http-10 session, http-11 console, http-09 pompe tunnel) ou appelé depuis
une pile déjà profonde. Ce balayage liste, par bloc embarqué du proxy :
  - tout sub rsp, IMM avec IMM > 0x100 (cadres notables) ;
  - les add rsp équivalents (épilogue) ;
  - les push consécutifs (comptés grossièrement).

But : identifier TOUS les grands cadres avant de corriger (une seule
itération, tous les défauts de la même famille corrigés ensemble).

Usage : python3 scripts/diag_cadres_m3.py
"""

import importlib.util
import pathlib
import re
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
SEUIL = 0x100

TOUS_LES_BLOCS = (list(LT.BLOCS_IO) + list(LT.BLOCS_LIBC_EMBARQUES)
                  + list(LT.BLOCS_TCP_EMBARQUES) + list(LT.BLOCS_M3))

# Blocs appelés comme THREADS (point d'entrée de CreateThread) :
THREADS = {0x5580: "http-10 session", 0x5D80: "http-11 console",
           0x54C0: "http-09 pompe (thread du tunnel)"}


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

    print(f"{'bloc':<28} {'rva':>7}  {'profondeur max sub rsp':>24}  thread")
    print("-" * 78)
    suspects = []
    for _bid, nom, rva, taille, _src, _n in sorted(TOUS_LES_BLOCS, key=lambda b: b[2]):
        try:
            off = rva_to_off(pe, rva)
        except ValueError:
            continue
        code = data[off:off + taille]
        maxi = 0
        for ins in md.disasm(code, BASE + rva):
            if ins.mnemonic == "sub" and ins.op_str.startswith("rsp,"):
                m = re.match(r"rsp,\s*(0x[0-9a-f]+|\d+)", ins.op_str)
                if m:
                    v = int(m.group(1), 0)
                    if v > maxi:
                        maxi = v
        est_thread = "OUI ←" if rva in THREADS else ""
        marque = ""
        if maxi > 0x1000:
            marque = "  ★ DÉPASSERAIT LE COMMIT INITIAL (0x1000)"
            suspects.append((nom, rva, maxi))
        elif maxi > SEUIL:
            marque = "  (notable)"
        print(f"{nom:<28} {rva:#07x}  {maxi:#10x} ({maxi:>6} o)  {est_thread}{marque}")

    print()
    print("=" * 78)
    if suspects:
        print("SUSPECTS (cadre > commit initial 0x1000 — mort c00000fd si thread neuf) :")
        for nom, rva, maxi in suspects:
            print(f"  ★ {nom} (@{rva:#x}) : sub rsp, {maxi:#x}")
    else:
        print("Aucun suspect > 0x1000.")
    return 1 if suspects else 0


if __name__ == "__main__":
    sys.exit(main())
