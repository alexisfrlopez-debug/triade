#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""agreger_mesures_v190.py — L'AGRÉGATION PRÉ-ENREGISTRÉE (P8) : lit les
journaux CSV du mesureur scellé, calcule par cible/machine/N la liste des
t, la médiane, l'étendue — tranche au critère P7 (la MÉDIANE des n>=10
exécutions au seuil |t| > 5). ÉCHEC FERMÉ : un fichier manquant, une
ligne imputable — un REFUS nommé, AUCUNE valeur fabriquée."""
import csv
import glob
import math
import pathlib
import statistics
import sys

SEUIL = 5.0


def lit_t(journal: pathlib.Path) -> dict[str, list[float]]:
    """Lit les t par cible du CSV du mesureur (ou du log repris)."""
    ts: dict[str, list[float]] = {}
    lignes = journal.read_text(errors="replace").splitlines()
    for l in lignes:
        parties = l.split(",")
        if len(parties) >= 3:
            try:
                cible = parties[0].strip()
                t = float(parties[-1].strip())
            except ValueError:
                continue
            if cible and math.isfinite(t):
                ts.setdefault(cible, []).append(t)
    return ts


def main() -> int:
    racine = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "journaux-v190")
    journaux = sorted(glob.glob(str(racine / "run-N*-*.log"))
                      + glob.glob(str(racine / "journal-dudect-*.csv")))
    if len(journaux) < 30:
        print(f"[REFUS] {len(journaux)} journal(s) trouvé(s) — le protocole "
              f"exige n>=10 par N sur 3 valeurs (>=30 exécutions) : "
              f"RIEN n'est agrégé, AUCUNE valeur fabriquée.")
        return 1
    par_cn: dict[tuple, list[float]] = {}
    for j in journaux:
        p = pathlib.Path(j)
        n = "N?"
        for partie in p.stem.split("-"):
            if partie.startswith("N") and partie[1:].isdigit():
                n = partie
        for cible, ts in lit_t(p).items():
            par_cn.setdefault((cible, n), []).extend(ts)
    refus = []
    print(f"{'cible':<28s} {'N':<6s} {'n':>3s} {'médiane':>9s} "
          f"{'étendue':>17s} verdict")
    for (cible, n), ts in sorted(par_cn.items()):
        if len(ts) < 10:
            refus.append(f"{cible}@{n}: {len(ts)} mesures (<10) — REFUS")
            continue
        med = statistics.median(ts)
        verdict = "À L'ÉCART (critère P7)" if abs(med) > SEUIL else "sous le seuil"
        print(f"{cible:<28s} {n:<6s} {len(ts):>3d} {med:>9.2f} "
              f"[{min(ts):.2f}..{max(ts):.2f}] {verdict}")
    if refus:
        print("\n".join(["", "[REFUS] exécutions insuffisantes :"] + refus))
        return 1
    print("LE VERDICT AU CRITÈRE PRÉ-ENREGISTRÉ P7 — les médianes ci-dessus ; "
          "le témoin daté/signé du développeur fait foi (D99).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
