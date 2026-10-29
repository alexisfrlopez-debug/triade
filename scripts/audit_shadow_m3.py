#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIADE — Audit ABI shadow-space des appels IAT du PROXY M3 (D63).

Contexte (D63, soir du 27/10) : terrain.10 a SURVÉCU au curl (correctif D62
confirmé) mais T2 rend curl http code=56, https code=7, journal proxy 1 ligne
(bannière seule : aucun « connexion entrante », aucun « arret ») et T3 rend
jeton OAuth ÉCHEC. Le relais réel curl → proxy → amont n'a JAMAIS tourné
avant ce run (étape c prévue « sur le terrain », journal 37/38) : les blocs
M3 neufs (http-01..12, tcp-13) n'ont jamais été exécutés en conditions
réelles. code 56 = connexion acceptée puis RST → suspicion de mort du proxy
à SA PREMIÈRE session entrante. Cet audit cherche les défauts homeparams
(shadow space absent) du même genre que D41 (demo.6) et D62 (sup-34 .curl)
sur le binaire livré m3/proxy.exe (md5 8740e1ca…, S05 du kit terrain).

Méthode (héritée D41/D62) : suivi symbolique de RSP depuis l'entrée de
chaque bloc, remise à zéro aux entrées de fonctions imbriquées, règles :
  - ALIGNEMENT : D ≡ 8 (mod 16)  [entrée ≡ 8, call exige RSP ≡ 0 mod 16] ;
  - SHADOW SPACE : D ≥ 0x28  [0x20 zone d'accueil + 8 adresse de retour] ;
  - site D < 0x28 ou mal aligné = DÉFAUT MORTEL POTENTIEL (homeparams écrit
    rcx/rdx/r8/r9 dans [rsp+8..0x18] → écrase l'adresse de retour du
    CALLER → ret vers garbage → c0000005 → le proxy meurt SANS journaliser,
    la pile TCP envoie le RST que curl traduit en code 56).

Usage : python3 scripts/audit_shadow_m3.py [EXE]
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

EXE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else REPO / "m3" / "proxy.exe")
BASE = LT.IMAGE_BASE

# Tous les blocs embarqués dans proxy.exe (héritages + M3 neufs).
TOUS_LES_BLOCS = (list(LT.BLOCS_IO) + list(LT.BLOCS_LIBC_EMBARQUES)
                  + list(LT.BLOCS_TCP_EMBARQUES) + list(LT.BLOCS_M3))

# Entrées secondaires documentées (fils tcp-06 : cible du CreateThread —
# http-09 pompe tunnel ; l'entrée principale est ENTREE = 0x1800).
ENTREES_SECONDAIRES = {LT.ENTREE}


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

    bornes = sorted((rva, rva + taille, nom)
                    for _bid, nom, rva, taille, _src, _n in TOUS_LES_BLOCS)

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
        entrees = {e for e in ENTREES_SECONDAIRES if lo <= e < hi}
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
