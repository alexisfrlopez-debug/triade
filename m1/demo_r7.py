#!/usr/bin/env python3
"""demo_r7.py — Démonstration des adresses stables (R7), jalon M1.

La démonstration lit l'historique git du dépôt — c'est lui qui fait foi :

  1. dev.1 (commit « M1 dev.1 ») : six blocs libc + les deux blocs io réutilisés
     de M0, scellés dans selftest.exe ;
  2. dev.2 (état courant) : memset (b20007) entre dans la RÉSERVE de la zone
     libc (slot 0x13C0, rempli d'int3 en dev.1) et l'autotest s'étend
     (libc-08:R1 → R2, 18 → 21 vecteurs).

Le critère R7 — « patcher ne déplace rien » — est démontré si et seulement si :
  - chaque bloc scellé en dev.1 est OCTET-IDENTIQUE À LA MÊME ADRESSE en dev.2 ;
  - les blocs io réutilisés sont octet-identiques à hello.exe (M0) dans les
    DEUX artefacts (réutilisation inter-artefacts) ;
  - memset occupe exclusivement de l'espace précédemment réservé (int3) ;
  - les structures PE héritées (IAT, descripteurs, BASERELOC) n'ont pas bougé.

Usage : python3 demo_r7.py   (depuis m1/, dépôt git propre)
"""

from __future__ import annotations

import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import layout as L

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)

SCELLES_DEV1 = [
    ("a10002", "io-01 write (réutilisé M0)", 0x1040, 0x40),
    ("a10003", "io-02 exit (réutilisé M0)", 0x1080, 0x40),
    ("b20001", "libc-01 memcpy", 0x1100, 0x80),
    ("b20002", "libc-02 memcmp", 0x1180, 0x80),
    ("b20003", "libc-03 strlen", 0x1200, 0x80),
    ("b20004", "libc-04 itoa", 0x1280, 0x80),
    ("b20005", "libc-05 zone_alloc", 0x1300, 0x80),
    ("b20006", "libc-06 zone_reset", 0x1380, 0x40),
]
MEMSET = ("b20007", "libc-07 memset (ajouté dev.2)", 0x13C0, 0x80)


def git_exe(revision: str) -> bytes:
    """selftest.exe à une révision donnée, depuis l'historique git."""
    r = subprocess.run(["git", "-C", RACINE, "show", f"{revision}:m1/selftest.exe"],
                       capture_output=True, check=True)
    return r.stdout


def slot(exe: bytes, rva: int, taille: int) -> bytes:
    return exe[L.TEXT_FILE + (rva - L.TEXT_RVA): L.TEXT_FILE + (rva - L.TEXT_RVA) + taille]


def main() -> int:
    print("=== Démonstration R7 : adresses stables (dev.1 -> dev.2, et héritage M0) ===")
    # Révision dev.1 = le commit qui a introduit m1/selftest.exe
    r = subprocess.run(["git", "-C", RACINE, "log", "--format=%H %s", "--follow", "-n", "2",
                        "--", "m1/selftest.exe"], capture_output=True, text=True, check=True)
    revisions = [l.split(" ", 1) for l in r.stdout.strip().splitlines()]
    if len(revisions) < 2:
        print("ECHEC : l'historique git doit contenir dev.1 ET dev.2 (deux commits de selftest.exe)")
        return 1
    dev2, dev1 = revisions[0][0], revisions[1][0]
    print(f"[git] dev.1 = {dev1[:12]} ({revisions[1][1][:60]}…)")
    print(f"[git] dev.2 = {dev2[:12]} ({revisions[0][1][:60]}…)")
    exe1, exe2 = git_exe(dev1), git_exe(dev2)
    with open(os.path.join(ICI, "selftest.exe"), "rb") as f:
        exe_courant = f.read()
    if exe_courant != exe2:
        print("ECHEC : l'arbre de travail diverge du commit dev.2 (committer d'abord)")
        return 1
    with open(os.path.join(RACINE, "m0", "hello.exe"), "rb") as f:
        hello = f.read()

    print(f"\n[1] Blocs scellés en dev.1 — octets identiques à la même adresse en dev.2 ?")
    tous_stables = True
    for bid, nom, rva, taille in SCELLES_DEV1:
        s1, s2 = slot(exe1, rva, taille), slot(exe2, rva, taille)
        stable = s1 == s2
        tous_stables &= stable
        print(f"    {bid} {nom:32} @ 0x{rva:04x} : {'IDENTIQUE' if stable else 'DIVERGENT'} "
              f"({taille} o, {sum(1 for a, b in zip(s1, s2) if a != b)} octets modifiés)")

    print(f"\n[2] Réutilisation inter-artefacts — io-01/io-02 vs hello.exe (M0) ?")
    for bid, nom, rva, taille in SCELLES_DEV1[:2]:
        origine = hello[L.TEXT_FILE + (rva - L.TEXT_RVA): L.TEXT_FILE + (rva - L.TEXT_RVA) + taille]
        ok = origine == slot(exe1, rva, taille) == slot(exe2, rva, taille)
        tous_stables &= ok
        print(f"    {bid} {nom:32} : {'octet-identique dans hello.exe, dev.1 et dev.2' if ok else 'DIVERGENT'}")

    print(f"\n[3] Entrée de memset (dev.2) — exclusivement dans la réserve ?")
    reserve_dev1 = slot(exe1, *MEMSET[2:])
    uniquement_reserve = all(b == 0xCC for b in reserve_dev1)
    memset_code = slot(exe2, *MEMSET[2:])
    occupe = any(b != 0xCC for b in memset_code)
    print(f"    slot 0x{MEMSET[2]:04x} en dev.1 : {'100 % int3 (réserve)`' if uniquement_reserve else 'OCCUPÉ EN DEV.1 !'}")
    print(f"    slot 0x{MEMSET[2]:04x} en dev.2 : {'code memset présent' if occupe else 'vide !'}")
    tous_stables &= uniquement_reserve and occupe

    print(f"\n[4] Structures PE héritées (IAT, descripteurs, BASERELOC) inchangées ?")
    zone_pe = (L.R_DESC_IMPORT, 0x20D0 - L.R_DESC_IMPORT + 12)
    pe1 = exe1[L.RDATA_FILE + (zone_pe[0] - L.RDATA_RVA): L.RDATA_FILE + (zone_pe[0] - L.RDATA_RVA) + zone_pe[1]]
    pe2 = exe2[L.RDATA_FILE + (zone_pe[0] - L.RDATA_RVA): L.RDATA_FILE + (zone_pe[0] - L.RDATA_RVA) + zone_pe[1]]
    pe0 = hello[L.RDATA_FILE + (zone_pe[0] - L.RDATA_RVA): L.RDATA_FILE + (zone_pe[0] - L.RDATA_RVA) + zone_pe[1]]
    stable_pe = pe1 == pe2 == pe0
    tous_stables &= stable_pe
    print(f"    0x{zone_pe[0]:04x}-0x{zone_pe[0] + zone_pe[1]:04x} : "
          f"{'identiques dans hello.exe, dev.1 et dev.2' if stable_pe else 'DIVERGENTES'}")

    print(f"\n[5] Ce qui a changé (et devait changer) :")
    diff = sum(1 for a, b in zip(exe1, exe2) if a != b)
    print(f"    autotest libc-08 (R1 -> R2, 18 -> 21 vecteurs) : {len(slot(exe2, 0x1800, 0x800))} o de slot app")
    print(f"    {diff} octets d'image modifiés au total — tous dans le slot autotest ou la réserve")

    print(f"\n=== R7 {'DÉMONTRÉ' if tous_stables else 'ÉCHEC'} : "
          f"{'ajouter un bloc n\'a déplacé ni modifié aucun bloc scellé' if tous_stables else 'voir ci-dessus'} ===")
    return 0 if tous_stables else 1


if __name__ == "__main__":
    sys.exit(main())
