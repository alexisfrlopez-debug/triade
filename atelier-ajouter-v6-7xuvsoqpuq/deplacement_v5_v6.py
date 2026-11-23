#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""deplacement_v5_v6.py — le registre du déplacement par classe entre la
campagne v5 (yfkpml1j2) et la campagne v6 (7xuvsoqpuq) : les deux vertes ·
les conversions · les pertes · les deux refusées — par bloc, l'ordre
canonique. Le réseau v5 (5/18) confronté au réseau v6."""
from __future__ import annotations

import json
import pathlib

REPO = pathlib.Path("/home/z/my-project/depot")
V5 = REPO / "atelier-ajouter-v5-yfkpml1j2" / "resultats_v5.jsonl"
V6 = REPO / "atelier-ajouter-v6-7xuvsoqpuq" / "resultats_v6.jsonl"
SORTIE = REPO / "atelier-ajouter-v6-7xuvsoqpuq" / "registres" / \
    "deplacement-v5-v6.txt"


def charger(p: pathlib.Path) -> dict:
    d = {}
    for l in p.read_text(encoding="utf-8").splitlines():
        if l.strip():
            r = json.loads(l)
            d[r["bloc"]] = r
    return d


def main() -> int:
    v5, v6 = charger(V5), charger(V6)
    assert len(v5) == 18 and len(v6) == 18, \
        f"les 18 tâches exigées aux deux campagnes : v5 {len(v5)} v6 {len(v6)}"
    lignes = ["LE DÉPLACEMENT v5 → v6 (par classe, l'ordre canonique des "
              "blocs)", ""]
    deux_vertes, conversions, pertes, deux_refusees = [], [], [], []
    for bloc in v5:
        a, b = v5[bloc], v6[bloc]
        if a["vert"] and b["vert"]:
            deux_vertes.append(bloc)
        elif not a["vert"] and b["vert"]:
            conversions.append(bloc)
        elif a["vert"] and not b["vert"]:
            pertes.append(bloc)
        else:
            deux_refusees.append(bloc)
        lignes.append(f"{bloc:22s} v5 {a['verdict'][:28]:30s} → "
                      f"v6 {b['verdict'][:28]} (essais {a['essais']} → "
                      f"{b['essais']})")
    lignes.append("")
    lignes.append(f"LES DEUX VERTES ({len(deux_vertes)}) : "
                  + ", ".join(deux_vertes))
    lignes.append(f"LES CONVERSIONS v5→v6 ({len(conversions)}) : "
                  + (", ".join(conversions) if conversions else "AUCUNE"))
    lignes.append(f"LES PERTES v5→v6 ({len(pertes)}) : "
                  + (", ".join(pertes) if pertes else "AUCUNE"))
    lignes.append(f"LES DEUX REFUSÉES ({len(deux_refusees)}) : "
                  + ", ".join(deux_refusees))
    n5 = sum(1 for r in v5.values() if r["vert"])
    n6 = sum(1 for r in v6.values() if r["vert"])
    lignes.append("")
    lignes.append(f"LE RÉSEAU : v5 {n5}/18 → v6 {n6}/18")
    SORTIE.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    print("\n".join(lignes))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
