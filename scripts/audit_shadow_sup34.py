#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIADE — Audit ABI shadow-space des appels IAT du SUPERVISEUR terrain.9 (D62).

Contexte (D62, soir du 27/10) : la capture de l'Historique de protection
(20:51:30) montre AUCUNE action Defender aux instants des morts (19:23,
20:01, 20:47) — la théorie du kill externe s'affaiblit gravement. D53 avait
documenté « 4 défauts D=0x8 trouvés… tous post-clic (sup-31, sup-34 ×3) »
puis les avait écartés (« réels mais PAS le tueur pré-fenêtre ») : or la mort
actuelle est EXACTEMENT dans sup-34 (1er curl, entre S21 et S22, 4/4 runs).
Cet audit re-loe ces défauts sur le binaire livré terrain.9 (md5 a59931db…)
pour déterminer si un call IAT sans shadow space siège sur le chemin
bannière → curl → S22.

Méthode (héritée D41 audit_shadow_space.py) : suivi symbolique de RSP depuis
l'entrée de chaque bloc, remise à zéro aux entrées de fonctions imbriquées
(cibles d'appels directs internes au bloc), règles :
  - ALIGNEMENT : D ≡ 8 (mod 16)  [entrée ≡ 8, call exige RSP ≡ 0 mod 16] ;
  - SHADOW SPACE : D ≥ 0x28  [0x20 zone d'accueil + 8 adresse de retour] ;
  - site D < 0x28 ou mal aligné = DÉFAUT MORTEL POTENTIEL (homeparams écrit
    rcx/rdx/r8/r9 dans [rsp+8..0x18] → écrase l'adresse de retour du
    CALLER → ret vers garbage → c0000005, fenêtre fermée, WER AppCrash).

Usage : python3 scripts/audit_shadow_sup34.py [EXE]
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


LT = _charger("layout_terrain", REPO / "terrain" / "layout.py")

EXE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else
                   REPO / "terrain" / "livraison" / "superviseur-terrain9.exe")
BASE = 0x140000000

# Entrées secondaires documentées (win-05 : trace 0x5000 / scénario 0x5100 ;
# sup-37 : extraction 0x6600 / nettoyage dispatché à la même entrée).
ENTREES_SECONDAIRES = {0x5100}


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

    bornes = sorted(
        (rva, rva + taille, nom)
        for _bid, nom, rva, taille, _src, _n in LT.BLOCS_TERRAIN
    )

    total_defauts = 0
    sites = 0
    resume = []

    for lo, hi, nom in bornes:
        try:
            off = rva_to_off(pe, lo)
        except ValueError:
            continue
        code = data[off:off + (hi - lo)]

        # passe 1 : entrées de fonctions imbriquées (cibles d'appels directs
        # internes au bloc)
        entrees = set(ENTREES_SECONDAIRES) if lo <= 0x5100 < hi else set()
        for ins in md.disasm(code, BASE + lo):
            if ins.mnemonic == "call" and "rip" not in ins.op_str:
                try:
                    cible = int(ins.op_str.split()[-1], 16) - BASE
                except ValueError:
                    continue
                if lo <= cible < hi:
                    entrees.add(cible)

        # passe 2 : suivi symbolique de la profondeur D
        D = 0
        lignes, defauts_bloc = [], []
        for ins in md.disasm(code, BASE + lo):
            rva = ins.address - BASE
            m, ops = ins.mnemonic, ins.op_str
            if rva in entrees:
                D = 0
            if m == "push":
                D += 8
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
                        lignes.append(
                            f"    ✗ {rva:#06x}: {m} {ops}   D={D:#x} → "
                            f"DÉFAUT : {'; '.join(probs)}")
                    else:
                        lignes.append(
                            f"    ✓ {rva:#06x}: {m} {ops}   D={D:#x} (sain)")
            elif m == "ret":
                D = 0
        resume.append((nom, lo, len(defauts_bloc), sites))
        if defauts_bloc:
            total_defauts += len(defauts_bloc)
            print(f"◆ {nom} (@{lo:#x}) : {len(defauts_bloc)} DÉFAUT(S)")
            for l in lignes:
                if l.strip().startswith("✗"):
                    print(l)
            print()

    print("=" * 74)
    print(f"BILAN : {sites} sites d'appel IAT audités, "
          f"{total_defauts} défaut(s) shadow space/alignement")
    for nom, lo, nd, _ in resume:
        if nd:
            print(f"  - {nom} (@{lo:#x}) : {nd} défaut(s)")
    print("Rappel règle : D ≥ 0x28 (0x20 shadow + 8 retour) et D ≡ 8 (mod 16).")
    return 1 if total_defauts else 0


if __name__ == "__main__":
    sys.exit(main())
