#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIADE — Audit ABI shadow-space de TOUS les appels IAT de demo.exe (D41).

Défaut trouvé (terrain demo.6, mort après sonde1) : .protger (tcp-07) appelle
VirtualProtect par IAT avec `sub rsp, 8` seulement — les 32 octets de shadow
space exigés par l'ABI msx64 ne sont PAS réservés. kernel32 (compilé
/homeparams) range rdx=0x700 sur l'adresse de retour de .protger → ret vers
0x700 → violation d'accès → processus mort. Corrigé en tcp-07:R3 (sub/add
rsp,0x28 + lea r9,[rsp+0x20]).

Méthode : pour CHAQUE site `call qword ptr [rip + X]` (appel IAT ou pointeur
dynamique), suivi symbolique de RSP depuis l'entrée de la FONCTION englobante
— avec remise à zéro aux entrées de fonctions imbriquées (cibles d'appels
directs internes au bloc) et aux entrées secondaires documentées (win-05 a
deux entrées : 0x5000 trace / 0x5100 scénario). Règles :
  - ALIGNEMENT : D ≡ 8 (mod 16)  [entrée ≡ 8 (mod 16), call exige RSP ≡ 0] ;
  - SHADOW SPACE : D ≥ 0x28  [0x20 zone d'accueil + 8 adresse de retour] ;
  - tout site D < 0x28 ou mal aligné est un DÉFAUT MORTEL POTENTIEL.

Vérification chirurgicale en prime : .protger (@0x4531) audité depuis sa
propre entrée — la correction D41 doit donner D = 0x28 exactement.

Usage : .venv/bin/python scripts/audit_shadow_space.py
"""

import pathlib
import sys

import capstone
import pefile

REPO = pathlib.Path(__file__).resolve().parents[1]
import importlib.util  # noqa: E402

def _charger(nom, chemin):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

L = _charger("layout_demo", REPO / "demo" / "layout.py")    # BLOCS_WIN
L2 = _charger("layout_m2", REPO / "m2" / "layout.py")       # héritage tcp

EXE = REPO / "demo" / "demo.exe"
BASE = 0x140000000

BLOCS_DEMO = (
    list(L.BLOCS_WIN)
    + [b for b in L2.BLOCS_TCP if b[1] not in ("tcp-10:R1", "tcp-12:R1")]
    + list(L2.BLOCS_LIBC_EMBARQUES)
    + list(L2.BLOCS_IO)
)

# Entrées secondaires documentées (plusieurs points d'entrée dans un bloc).
ENTREES_SECONDAIRES = {0x5100}   # win-05:R3 — JOURNAL_GUI (le bloc vit à 0x5000)


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

    bornes = [(rva, rva + taille, nom)
              for _bid, nom, rva, taille, _src, _n in BLOCS_DEMO]
    bornes.sort()

    total_defauts = 0
    sites = 0

    for lo, hi, nom in bornes:
        off = rva_to_off(pe, lo)
        code = data[off:off + (hi - lo)]

        # passe 1 : entrées de fonctions imbriquées = cibles d'appels directs
        # internes au bloc (ex. .protger dans tcp-07)
        entrees = set(ENTREES_SECONDAIRES) if lo <= 0x5000 < hi else set()
        for ins in md.disasm(code, BASE + lo):
            if ins.mnemonic == "call" and "rip" not in ins.op_str:
                try:
                    cible = int(ins.op_str.split()[-1], 16) - BASE
                except ValueError:
                    continue
                if lo <= cible < hi:
                    entrees.add(cible)

        # passe 2 : suivi symbolique de la profondeur D sous l'entrée courante
        D = 0
        lignes, defauts_bloc = [], []
        for ins in md.disasm(code, BASE + lo):
            rva = ins.address - BASE
            m, ops = ins.mnemonic, ins.op_str
            if rva in entrees:
                D = 0                      # entrée de fonction — cadre neuf
            if m == "push":                # (if, pas elif : l'entrée peut ÊTRE
                D += 8                     #  une instruction de pile — sub rsp)
            elif m == "pop":
                D -= 8
            elif m == "sub" and ops.startswith("rsp,"):
                D += int(ops.split(",")[1].strip(), 0)
            elif m == "add" and ops.startswith("rsp,"):
                D -= int(ops.split(",")[1].strip(), 0)
            elif m == "call":
                if "qword ptr [rip" in ops:
                    sites += 1
                    probs = []
                    if D % 16 != 8:
                        probs.append(f"ALIGNEMENT D={D:#x} (attendu ≡ 8 mod 16)")
                    if D < 0x28:
                        probs.append(f"SHADOW SPACE D={D:#x} < 0x28")
                    if probs:
                        defauts_bloc.append((rva, D))
                        lignes.append(f"    ✗ {rva:#06x}: {m} {ops}"
                                      f"   D={D:#x} → DÉFAUT : {'; '.join(probs)}")
                    else:
                        lignes.append(f"    ✓ {rva:#06x}: {m} {ops}"
                                      f"   D={D:#x} (sain)")
                # appels directs : la fonction appelée (autre bloc ou imbriquée)
                # restaure sa pile — bilan nul pour l'appelant
            elif m == "ret":
                D = 0                      # fin de fonction — contexte clos
        if defauts_bloc:
            total_defauts += len(defauts_bloc)
            print(f"◆ {nom} (@{lo:#x}) : {len(defauts_bloc)} DÉFAUT(S)")
            for l in lignes:
                print(l)
            print()

    # --- vérification chirurgicale : .protger (tcp-07:R3, D41) -------------
    print("=" * 74)
    print("[chirurgical] .protger @0x4531 — cadre audité depuis SA propre entrée")
    off = rva_to_off(pe, 0x4531)
    D = 0
    protger_ok = True
    for ins in md.disasm(data[off:off + 0x28], BASE + 0x4531):
        rva = ins.address - BASE
        m, ops = ins.mnemonic, ins.op_str
        if m == "push":
            D += 8
        elif m == "sub" and ops.startswith("rsp,"):
            D += int(ops.split(",")[1].strip(), 0)
        if m == "call" and "qword ptr [rip" in ops:
            verdict = []
            if D % 16 != 8:
                verdict.append(f"alignement D={D:#x} ✗")
                protger_ok = False
            if D < 0x28:
                verdict.append(f"shadow D={D:#x} < 0x28 ✗")
                protger_ok = False
            if not verdict:
                verdict.append(f"aligné ✓, shadow {D:#x} ≥ 0x28 ✓")
            print(f"    {rva:#06x}: {m} {ops}   D={D:#x} — {'; '.join(verdict)}")
        print(f"    {rva:#06x}: {ins.bytes.hex():<16} {m} {ops}")

    print("=" * 74)
    print(f"BILAN : {sites} sites d'appel IAT audités, "
          f"{total_defauts} défaut(s) shadow space/alignement ; "
          f".protger D41 {'CONFORME' if protger_ok else 'NON CONFORME !'}")
    print("Rappel règle : D ≥ 0x28 (0x20 shadow + 8 retour) et D ≡ 8 (mod 16).")
    return 1 if (total_defauts or not protger_ok) else 0


if __name__ == "__main__":
    sys.exit(main())
