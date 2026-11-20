#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""recompte_decomposition.py — LE RECOMPTE DE LA DÉCOMPOSITION MÉMOIRE
(zho5vilpy, la correction (a) du PLAN-ZHO5VILPY.md) : la ligne publiée à
la v0.21.0 « pile 1247 · médiés 0 · constants 191 · plan-fixe 189 ·
plan-garde 13 · contrat-boucle 18 · nommés 92 » SOMME À 1750, PAS 2098.
Le recompte depuis atelier-securite-bk79jvzbm/surete_memoire_v200.csv
(52 lignes, acces_mem = 2098) — chaque catégorie sommée PAR CODE, la
somme exacte exigée, la cohérence 2006 + 34 + 58 = 2098 reconduite."""
from __future__ import annotations

import csv
import pathlib

REPO = pathlib.Path("/home/z/my-project/depot")
CSV = REPO / "atelier-securite-bk79jvzbm" / "surete_memoire_v200.csv"
OUT = REPO / "atelier-medians-zho5vilpy" / "rapport-recompte.txt"


def main() -> int:
    with open(CSV, newline="", encoding="utf-8") as f:
        lignes = list(csv.DictReader(f))
    tot = {k: 0 for k in lignes[0] if k not in ("domaine", "bloc")}
    for r in lignes:
        for k, v in r.items():
            if k in tot:
                tot[k] += int(v)

    publié = {"pile": 1247, "médiés": 0, "constants": 191, "plan-fixe": 189,
              "plan-garde": 13, "contrat-boucle": 18, "nommés": 92,
              "hors-cadre": 0}
    somme_publiée = sum(publié.values())
    réel = {"pile": tot["pile"], "médiés": tot["medies_contrat"],
            "constants": tot["constants_rip"], "plan-fixe": tot["plan_fixe"],
            "plan-garde": tot["plan_garde"],
            "contrat-boucle": tot["contrat_boucle"], "nommés": tot["nommes"],
            "hors-cadre": tot["hors_cadre"]}
    somme_réelle = sum(réel.values())

    lignes_out = [
        "LE RECOMPTE DE LA DÉCOMPOSITION MÉMOIRE (zho5vilpy, la correction (a))",
        "=" * 72,
        f"LA SOURCE : surete_memoire_v200.csv ({len(lignes)} lignes, "
        f"acces_mem = {tot['acces_mem']}) — chaque catégorie sommée PAR CODE",
        "",
        "LA LIGNE PUBLIÉE À LA v0.21.0 (la pièce 4 des preuves, le verbatim "
        "de rapport-gardes.txt) :",
        "  pile 1247 · médiés 0 · constants 191 · plan-fixe 189 · plan-garde "
        "13 · contrat-boucle 18 · nommés 92 · hors-cadre 0",
        f"  LA SOMME PUBLIÉE : {somme_publiée} — PAS 2098 : LA FAUTE NOMMÉE "
        f"(le compte « médiés 0 » : la colonne medies_contrat du CSV porte "
        f"{tot['medies_contrat']}, la valeur « 0 » publiée à la v0.21.0 est "
        f"UNE ERREUR — L'ERRATUM)",
        "",
        "LE RECOMPTE (chaque catégorie du CSV, sommée par code) :",
        "  " + " · ".join(f"{k} {v}" for k, v in réel.items()),
        f"  LA SOMME : {somme_réelle} == acces_mem {tot['acces_mem']} — "
        f"EXACTEMENT" if somme_réelle == tot["acces_mem"] else
        "  LA SOMME DIVERGE — REFUS",
        "",
        f"LA COHÉRENCE RECONDUITE : 2006 déchargés + 34 LEA relationnels + "
        f"58 gardes = {2006 + 34 + 58} == 2098 (les 92 nommés = 34 LEA + 58 "
        f"gardes — la vague 10 tenue)",
        f"LES CATÉGORIES DÉCHARGÉES : pile {tot['pile']} + médiés "
        f"{tot['medies_contrat']} + constants {tot['constants_rip']} + "
        f"plan-fixe {tot['plan_fixe']} + plan-garde {tot['plan_garde']} + "
        f"contrat-boucle {tot['contrat_boucle']} = "
        f"{tot['pile'] + tot['medies_contrat'] + tot['constants_rip'] + tot['plan_fixe'] + tot['plan_garde'] + tot['contrat_boucle']} "
        f"déchargés (2006 attendus)",
        "",
        "LA CORRECTION PORTÉE AUX PIÈCES : les preuves v0.22.0 publient la "
        "décomposition corrigée AVEC L'ERRATUM NOMMÉ (la valeur « 0 » "
        "publiée à la v0.21.0, la somme 1750 fautive) ; le verbatim de "
        "rapport-gardes.txt demeure OCTET POUR OCTET à la pièce publiée "
        "v0.21.0 (l'histoire n'est pas réécrite) — la correction vit au "
        "texte DES PREUVES v0.22.0, la ligne fautive démarquée.",
    ]
    OUT.write_text("\n".join(lignes_out) + "\n", encoding="utf-8")
    print("\n".join(lignes_out))
    return 0 if somme_réelle == tot["acces_mem"] == 2098 else 2


if __name__ == "__main__":
    raise SystemExit(main())
