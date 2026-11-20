#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cg_m4.py — LA MESURE M4 DES TROIS BRAS (3a91o5whb) : T, C, C+G sur LA
MÊME MACHINE (le ratio honnête exige les bras sur la même machine — le
plan § 3), n=5 exécutions par bras, l'horloge monotone, la liste fixe.

LA LISTE T : l'outil de la vague 9 TEL QUEL (outil_m4_v182, la liste
complète : garde-sceau, cristallisation×12, round-trips, oracles, build,
épreuve, kits) — la sortie REDIRIGÉE au présent atelier (les preuves de
la vague 9 JAMAIS écrasées).

LA LISTE C : les étapes de mesure_c_v182 (le build gcc-O2 des pièces,
la suite hash, l'épreuve de contrat POSIX, les contrôles binaires) —
la chaîne mingw re-provisionnée aux versions exactes.

LA LISTE C+G : LA MÊME LISTE C PLUS LES GESTES DE GOUVERNANCE (g1-g4) :
la garde des intentions signées (les SIX signatures Ed25519 vérifiées),
la chaîne de cristallisation re-vérifiée (les empreintes chaînées
recoupées), l'oracle du bloc (le juge modèle indépendant aux vecteurs du
contrat), le kit (l'assemblage du gabarit).

Sortie : m4-{bras}-run{N}.json (les JSON bruts) · rapport-cg-m4.txt."""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import time

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "atelier-cg-3a91o5whb"
V9 = REPO / "atelier-cout-boucle-cq01qv1za"
MINGW = "/home/z/my-project/work/mingw-debs/root/usr/bin/x86_64-w64-mingw32-gcc-posix"
U01C = REPO / "scripts" / "campagne_d204" / "unite-01-C"
U02C = REPO / "scripts" / "campagne_d204" / "unite-02-C"
N = 5


def une_etape(nom, cmd, mesures, cwd=REPO):
    t0 = time.monotonic()
    shell = isinstance(cmd, str) or (cmd and cmd[0] == "cd")
    args = " ".join(cmd) if isinstance(cmd, list) and cmd and cmd[0] == "cd" \
        else cmd
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True,
                       timeout=600, shell=shell)
    dt = time.monotonic() - t0
    mesures.append({"etape": nom, "secondes": round(dt, 3),
                    "code": r.returncode,
                    "console": (r.stdout + r.stderr)[-3000:]})
    print(f"  [{nom:<38}] {dt:7.3f} s  code {r.returncode}")
    return r.returncode


def bras_c(numero: int) -> int:
    """LA LISTE C — les étapes de mesure_c_v182 reconduites."""
    mesures = []
    t_total = time.monotonic()
    code = 0
    code |= une_etape(
        "build-gcc-O2-loupe-01",
        f"cd {U01C} && {MINGW} -O2 -shared -o epreuves/loupe-01-c.dll "
        f"source/loupe-01-c.c source/loupe-01-c.def".split(), mesures)
    code |= une_etape("suite-tests-c-hash",
                      ["python3", "epreuve_hash_posix.py"], mesures,
                      cwd=U01C)
    code |= une_etape(
        "suite-tests-c-contrat",
        f"cd {U01C}/epreuves && gcc -O2 -o epreuve_posix epreuve_posix.c "
        f"-I. && ./epreuve_posix > observe.txt && python3 "
        f"compare_epreuve.py".split(), mesures)
    code |= une_etape("controles-binaires-loupe-01",
                      ["python3", "controles_binaires.py"], mesures,
                      cwd=U01C)
    code |= une_etape(
        "build-gcc-O2-loupe-02",
        f"cd {REPO} && {MINGW} -O2 -shared -o scripts/campagne_d204/"
        f"unite-02-C/epreuves/loupe-02-c.dll scripts/campagne_d204/"
        f"unite-02-C/source/loupe-02-c.c scripts/campagne_d204/"
        f"unite-02-C/source/loupe-02-c.def".split(), mesures)
    code |= une_etape("epreuve-contrat-posix-loupe-02",
                      f"cd {U02C}/epreuves && gcc -O2 -I. -o epreuve_posix "
                      f"epreuve_posix.c && ./epreuve_posix > "
                      f"sortie-epreuve.txt && python3 compare_epreuve.py".split(),
                      mesures)
    code |= une_etape("controles-binaires-loupe-02",
                      ["python3", "scripts/campagne_d204/unite-02-C/"
                       "epreuves/controles_binaires.py"], mesures)
    total = time.monotonic() - t_total
    (ICI / f"m4-C-run{numero}.json").write_text(
        json.dumps({"bras": "C", "run": numero, "total_s": round(total, 3),
                    "etapes": mesures, "code": code}, indent=1),
        encoding="utf-8")
    print(f"  === TOTAL C run {numero} : {total:.1f} s ; code {code}")
    return code


def bras_cg(numero: int) -> int:
    """LA LISTE C+G — la liste C PLUS les gestes de gouvernance."""
    mesures = []
    t_total = time.monotonic()
    code = 0
    code |= une_etape(
        "garde-intentions-signees (g1)",
        ["python3", str(ICI / "cg_gouverne.py"), "--garde"], mesures)
    code |= une_etape(
        "build-gcc-O2-loupe-01",
        f"cd {U01C} && {MINGW} -O2 -shared -o epreuves/loupe-01-c.dll "
        f"source/loupe-01-c.c source/loupe-01-c.def".split(), mesures)
    code |= une_etape("suite-tests-c-hash",
                      ["python3", "epreuve_hash_posix.py"], mesures,
                      cwd=U01C)
    code |= une_etape(
        "suite-tests-c-contrat",
        f"cd {U01C}/epreuves && gcc -O2 -o epreuve_posix epreuve_posix.c "
        f"-I. && ./epreuve_posix > observe.txt && python3 "
        f"compare_epreuve.py".split(), mesures)
    code |= une_etape("controles-binaires-loupe-01",
                      ["python3", "controles_binaires.py"], mesures,
                      cwd=U01C)
    code |= une_etape("chaine-cristallisation (g2)",
                      ["python3", str(ICI / "cg_gouverne.py"),
                       "--cristallisation"], mesures)
    code |= une_etape(
        "build-gcc-O2-loupe-02",
        f"cd {REPO} && {MINGW} -O2 -shared -o scripts/campagne_d204/"
        f"unite-02-C/epreuves/loupe-02-c.dll scripts/campagne_d204/"
        f"unite-02-C/source/loupe-02-c.c scripts/campagne_d204/"
        f"unite-02-C/source/loupe-02-c.def".split(), mesures)
    code |= une_etape("epreuve-contrat-posix-loupe-02 (g3 l'oracle)",
                      f"cd {U02C}/epreuves && gcc -O2 -I. -o epreuve_posix "
                      f"epreuve_posix.c && ./epreuve_posix > "
                      f"sortie-epreuve.txt && python3 compare_epreuve.py".split(),
                      mesures)
    code |= une_etape("controles-binaires-loupe-02",
                      ["python3", "scripts/campagne_d204/unite-02-C/"
                       "epreuves/controles_binaires.py"], mesures)
    code |= une_etape("assemblage-kit (g4 le gabarit)",
                      ["python3", str(ICI / "cg_gouverne.py"), "--kit"],
                      mesures)
    total = time.monotonic() - t_total
    (ICI / f"m4-CG-run{numero}.json").write_text(
        json.dumps({"bras": "C+G", "run": numero,
                    "total_s": round(total, 3),
                    "etapes": mesures, "code": code}, indent=1),
        encoding="utf-8")
    print(f"  === TOTAL C+G run {numero} : {total:.1f} s ; code {code}")
    return code


def bras_t(numero: int) -> int:
    """LA LISTE T — l'outil de la vague 9, la sortie redirigée."""
    sys.path.insert(0, str(V9))
    import outil_m4_v182 as m4t
    m4t.SORTIE = ICI          # les preuves de la vague 9 jamais écrasées
    return m4t.une_execution("avant", numero)


def main() -> int:
    print("LA MESURE M4 DES TROIS BRAS — la même machine, n=5 par bras")
    for i in range(1, N + 1):
        bras_t(i)
    for i in range(1, N + 1):
        bras_c(i)
    for i in range(1, N + 1):
        bras_cg(i)
    # le rapport
    import statistics
    rap = ["LA MESURE M4 — LES TROIS BRAS SUR LA MÊME MACHINE "
           "(n=5, l'horloge monotone, la liste fixe)", ""]
    med = {}
    for bras in ("T", "C", "CG"):
        tot = [json.load(open(ICI / f"m4-{'avant' if bras == 'T' else bras}"
                              f"-run{i}.json"))["total_s"]
               for i in range(1, N + 1)]
        med[bras] = statistics.median(tot)
        rap.append(f"  LE BRAS {bras if bras != 'CG' else 'C+G'} : n={len(tot)}"
                   f" — médiane {med[bras]:.2f} s "
                   f"[min {min(tot):.2f}, max {max(tot):.2f}]")
    if med["CG"] and med["C"]:
        rap += [
            "",
            f"LE RATIO DE GOUVERNANCE C+G/C : {med['CG']/med['C']:.2f}× "
            f"(le coût des gestes de gouvernance ajoutés au bras C)",
            f"LE RATIO DE RÉGIME T/C+G : {med['T']/med['CG']:.1f}× — "
            f"L'EFFET NOTATION ISOLÉ : T−C+G = "
            f"{(med['T']-med['CG'])*1000:.0f} ms de vérification par "
            f"session — le bras C+G porte LA MÊME GOUVERNANCE que T (les "
            f"gestes g1-g4), l'écart restant est LA NOTATION manuscrite "
            f"elle-même (les preuves qu'elle exige : la cristallisation "
            f"des DOUZE rebuilds concurrents, les round-trips d'octets, "
            f"la recomposition du plan — jamais demandés au bras compilé)",
        ]
    (ICI / "rapport-cg-m4.txt").write_text("\n".join(rap) + "\n",
                                           encoding="utf-8")
    print("\n".join(rap))
    return 0


if __name__ == "__main__":
    sys.exit(main())
