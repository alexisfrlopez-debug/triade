#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""garde_domaine.py — L'ANALYSE DU DOMAINE (la suite du chantier 1, hrbdfy6i4) :
les 155 divergences du corpus mutant sont-elles DANS le vocabulaire des blocs
(les 99 classes mnémonique × forme d'opérandes) ou HORS ?

LA GARDE QUI EN DÉCOULE : le lifter est SOUND sur son DOMAINE VALIDÉ (les
classes des blocs — zéro divergence au corpus 1) ; toute instruction d'une
classe HORS domaine est REFUSÉE au chargement (fail-closed, le refus nommé) —
les 155 divergences mutantes nomment les classes à modéliser avant usage.

Sortie : garde-domaine.json · la section pour le rapport."""
from __future__ import annotations

import csv
import json
import pathlib
import re
import sys

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "atelier-lifter-hrbdfy6i4"

# les notations des 13 blocs couverts (la vague 10) + tls13-17 (la présente)
BLOCS = ["tls13-01", "tls13-02", "tls13-03", "tls13-05", "tls13-06",
         "tls13-07", "tls13-13", "tls13-14", "tls13-15", "tls13-16",
         "tls13-18", "tls13-19", "loupe-06", "tls13-17", "tls13-04",
         "tls13-08"]


def forme_normale(op_str: str) -> str:
    """La forme d'opérandes NORMALISÉE (les registres et valeurs abstraits)."""
    ops = [o.strip() for o in op_str.split(",")] if op_str else []
    out = []
    for o in ops:
        if o.startswith("[") or "ptr" in o:
            out.append("mem")
        elif re.fullmatch(r"[re][a-z0-9]{1,5}", o) or o in ("rflags",):
            out.append("reg")
        elif o.startswith(("xmm", "ymm")):
            out.append("xmm")
        else:
            out.append("imm")
    return " × ".join(out) if out else "(sans opérande)"


def main() -> int:
    # ---- le vocabulaire des blocs (les classes réellement levées) ----------
    vocab = set()
    rows = list(csv.reader(open(ICI / "soundness_registres.csv",
                                encoding="utf-8"), delimiter="\t"))
    for r in rows[1:]:
        if r[0] != "MUTANT":
            vocab.add((r[3], forme_normale(r[4])))

    # ---- les mutants divergents : dans le domaine ou hors ? ----------------
    divergents = [r for r in rows[1:]
                  if r[0] == "MUTANT" and r[13] != "—"]
    dans, hors = [], []
    for r in divergents:
        cls = (r[3], forme_normale(r[4]))
        (dans if cls in vocab else hors).append((r, cls))

    # ---- la répartition par classe des hors-domaine ------------------------
    from collections import Counter
    rep = Counter(cls for _, cls in hors)
    print(f"LE VOCABULAIRE DES BLOCS : {len(vocab)} classes "
          f"(mnémonique × forme normalisée)")
    print(f"LES MUTANTS DIVERGENTS : {len(divergents)} — "
          f"DANS le domaine : {len(dans)} ; HORS domaine : {len(hors)}")
    print("LA RÉPARTITION HORS DOMAINE (les classes à modéliser avant usage) :")
    for (mn, f), n in rep.most_common(40):
        print(f"    {n:3d} × {mn:12} {f}")

    verdict_dans = len(dans) == 0
    print()
    print(f"LE VERDICT : {'VERT' if verdict_dans else 'ROUGE'} — "
          f"{'AUCUNE' if verdict_dans else str(len(dans))} divergence DANS le "
          f"domaine validé ; les {len(hors)} divergences mutantes vivent "
          f"HORS vocabulaire — LA GARDE : le refus nommé au chargement de "
          f"toute classe non modélisée (fail-closed)")

    (ICI / "garde-domaine.json").write_text(
        json.dumps({"vocabulaire_classes": len(vocab),
                    "mutants_divergents": len(divergents),
                    "dans_domaine": len(dans),
                    "hors_domaine": len(hors),
                    "repartition_hors": [
                        {"mnemonique": m, "forme": f, "occurrences": n}
                        for (m, f), n in rep.most_common()],
                    "verdict": "VERT" if verdict_dans else "ROUGE"},
                   indent=1, ensure_ascii=False), encoding="utf-8")
    return 0 if verdict_dans else 1


if __name__ == "__main__":
    sys.exit(main())
