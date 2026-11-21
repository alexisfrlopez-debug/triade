#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""audit_ratios.py — L'AUDIT DE RECOMPOSABILITÉ DES RATIOS PUBLIÉS v0.22.0
(6kbfrpn7k, l'item 1 : « tout ratio dont le recalcul depuis les valeurs
imprimées diverge de plus de 0,05 de la valeur publiée »).

MÉTHODE : chaque ratio publié aux cinq pièces est recalculé DEPUIS LES
VALEURS IMPRIMÉES à côté de lui (ce que le lecteur peut faire) ET depuis
les canons non arrondis lus des JSON/rapports bruts des ateliers. Les deux
écarts sont publiés ; toute divergence supérieure à la tolérance — 0,05
ABSOLU aux ratios de pourcentage, 0,2 % RELATIF aux gains multiplicatifs —
est ROUGE et nommée. Aucune valeur n'est inventée : chaque canon cite sa
source brute.

Sortie : audit-ratios.json · rapport-audit-ratios.txt"""
from __future__ import annotations

import json
import pathlib

ICI = pathlib.Path(__file__).resolve().parent
REPO = ICI.parent

# LA TOLÉRANCE (l'instruction) : le recalcul depuis les valeurs imprimées
# ne diverge de plus de 0,05 de la valeur publiée — la demi-unité de la
# dernière décimale publiée (0,05 à une décimale, 0,5 à l'entier).
TOL_DEFAUT = 0.05

# (nom, imprimés, canon_non_arrondi, ratio_publié, calculeur, tolérance, note)
RATIOS = [
    # ---- LE CACHE DE ROUND-TRIP (ahult8jgd) — ROUGE v0.22.0 ----
    ("cache round-trip (ms)",
     "283.7 -> 0.4", "285.725 -> 0.418 (reprise µs)",
     680.6, lambda a, b: a / b, TOL_DEFAUT,
     "le lecteur : 283.7/0.4 = 709.25 ; le canon après arrondi à 0,1 ms"),
    # ---- L'AJOUTER (o5apue194) — ROUGE v0.22.0 ----
    ("ajouter (tokens request)",
     "3074 -> 2200", "3073.5 -> 2199.5 (le JSONL brut)",
     -28.5, lambda a, b: (b - a) / a * 100, TOL_DEFAUT,
     "le lecteur : (2200-3074)/3074 = -28.43 ; les médianes non arrondies"),
    # ---- LE RATIO DE RÉGIME T/C+G (3a91o5whb) — ROUGE v0.22.0 ----
    ("régime T/C+G (s)",
     "39.24 / 2.16", "39.244 / 2.163 (les m4-*.json bruts)",
     18.1, lambda a, b: a / b, TOL_DEFAUT,
     "le lecteur : 39.24/2.16 = 18.17 -> 18.2 ; le canon C+G à 3 décimales"),
    # ---- LES AUTRES RATIOS DES CINQ PIÈCES (conformes) ----
    ("éditer (tokens request)", "1106 -> 674", "1105.5 -> 673.5", -39.1,
     lambda a, b: (b - a) / a * 100, TOL_DEFAUT, ""),
    ("localiser (tokens request)", "1053 -> 627", "1053.0 -> 627.0", -40.5,
     lambda a, b: (b - a) / a * 100, TOL_DEFAUT, ""),
    ("hybride sous le scellé (cycles)", "18226 / 704", "18226 / 704", 25.9,
     lambda a, b: a / b, TOL_DEFAUT, ""),
    ("porteuse v4-inline (c/bloc)", "50.56 / 7.09", "50.56 / 7.09", 7.1,
     lambda a, b: a / b, TOL_DEFAUT, ""),
    ("plancher éditer natif", "674 / 27.5", "674 / 27.5", 24.5,
     lambda a, b: a / b, TOL_DEFAUT, ""),
    ("part notation propre (%)", "20.72 / 37.21", "20.715 / 37.212", 55.7,
     lambda a, b: a / b * 100, TOL_DEFAUT, ""),
    ("part régime (%)", "16.50 / 37.21", "16.497 / 37.212", 44.3,
     lambda a, b: a / b * 100, TOL_DEFAUT, ""),
    ("fenêtre éditer (%)", "2452 -> 1146", "2452 -> 1146", -53.3,
     lambda a, b: (b - a) / a * 100, TOL_DEFAUT, ""),
    ("prose de prescription (%)", "866 -> 372", "866 -> 372", -57.0,
     lambda a, b: (b - a) / a * 100, 0.5, ""),
    ("sse2 sous gcc-O2 (temps réel)", "16040 / 833", "16040 / 833", 19.3,
     lambda a, b: a / b, TOL_DEFAUT, ""),
    ("sse2 sur l'idiome memchr", "833 / 561", "833 / 561", 1.5,
     lambda a, b: a / b, TOL_DEFAUT, ""),
    ("sha-ni sous le scellé (c/bloc)", "832 / 128.5", "53243/8227 = 6.472", 6.5,
     lambda a, b: a / b, TOL_DEFAUT, ""),
    ("cristallisation incrémentale (%)", "13 / 28 blocs", "13 / 28", 54.0,
     lambda a, b: (1 - a / b) * 100, 0.5,
     "la fermeture transitive : 13 de 28 blocs re-vérifiés, -54 % du poste "
     "(publié à l'entier)"),
]

# les paires de valeurs pour chaque entrée (imprimé_a, imprimé_b, brut_a, brut_b)
VALEURS = [
    (283.7, 0.4, 285.725, 0.418),
    (3074.0, 2200.0, 3073.5, 2199.5),
    (39.24, 2.16, 39.244, 2.163),
    (1106.0, 674.0, 1105.5, 673.5),
    (1053.0, 627.0, 1053.0, 627.0),
    (18226.0, 704.0, 18226.0, 704.0),
    (50.56, 7.09, 50.56, 7.09),
    (674.0, 27.5, 674.0, 27.5),
    (20.72, 37.21, 20.715, 37.212),
    (16.50, 37.21, 16.497, 37.212),
    (2452.0, 1146.0, 2452.0, 1146.0),
    (866.0, 372.0, 866.0, 372.0),
    (16040.0, 833.0, 16040.0, 833.0),
    (833.0, 561.0, 833.0, 561.0),
    (832.0, 128.5, 53243.0, 8227.0),
    (13.0, 28.0, 13.0, 28.0),
]


def main() -> int:
    lignes = [
        "L'AUDIT DE RECOMPOSABILITÉ DES RATIOS PUBLIÉS v0.22.0 (6kbfrpn7k)",
        "chaque ratio recalculé depuis les imprimés ET depuis les canons",
        "bruts — la tolérance : 0,05 ABSOLU (la demi-unité de la",
        "aux gains multiplicatifs (l'arrondi du canon nommé)",
        "",
        f"{'ratio':38s} {'imprimés':22s} {'depuis impr.':>13s} "
        f"{'publié':>9s} {'écart':>8s}  VERDICT",
        "-" * 104,
    ]
    rouges = []
    js = []
    for (nom, imp, brut, pub, calc, tol, note), (ia, ib, ba, bb) in zip(RATIOS, VALEURS):
        r_imp = calc(ia, ib)
        r_brut = calc(ba, bb)
        ecart = r_imp - pub
        ok = abs(ecart) <= tol
        verdict = "VERT" if ok else "ROUGE"
        if not ok:
            rouges.append((nom, note))
        lignes.append(f"{nom:38s} {imp:22s} {r_imp:13.2f} {pub:9.1f} "
                      f"{ecart:8.2f}  {verdict}")
        js.append({"ratio": nom, "imprimes": imp, "canon": brut,
                   "recalc_imprimes": round(r_imp, 2),
                   "recalc_canons": round(r_brut, 2),
                   "publie": pub, "ecart": round(ecart, 2),
                   "tolerance": tol, "verdict": verdict})
    lignes += ["-" * 108, ""]
    if rouges:
        lignes.append(f"LES {len(rouges)} RATIOS ROUGES — les corrections portées :")
        for nom, note in rouges:
            lignes.append(f"  - {nom} : {note}")
    lignes += [
        "",
        "LES TROIS CORRECTIONS DE L'INSTRUCTION (portées à l'édition) :",
        "  (1) le cache round-trip : la médiane après publiée EN MS À TROIS",
        "      DÉCIMALES (0,418) et le gain RECOMPOSÉ des canons imprimés",
        "      (285,725/0,418 = 683,6×) — la re-mesure au protocole exact à",
        "      la précision µs : atelier-porteuse-ahult8jgd/reprise-6kbfrpn7k/",
        "  (2) l'ajouter : les médianes NON ARRONDIES publiées (3 073,5 ->",
        "      2 199,5) — le ratio -28,4 % recompose exactement ;",
        "  (3) le régime T/C+G : le canon C+G à TROIS DÉCIMALES (2,163 s)",
        "      publié à la table — 39,24/2,163 = 18,14 -> 18,1× recompose.",
        "",
        "LES CANONS SOURCES (aucune valeur inventée) :",
        "  - le cache : reprise-6kbfrpn7k/mesure-precision.json (la re-mesure)",
        "  - l'ajouter : atelier-gabarits-o5apue194/resultats_gabarits.jsonl",
        "    (les médianes du champ prompt : 3073.5 / 2199.5)",
        "  - le régime : atelier-cg-3a91o5whb/m4-CG-run*.json (2.163) et le",
        "    rapport-cgp-m4.txt (T 39.244 — la médiane des m4-T du dépôt v0.21)",
        "",
        "LA SOMME DE MÉDIANES N'EST PAS LA MÉDIANE DES SOMMES (l'item 2) : la",
        "table de décomposition §4 du rapport C+G+ porte désormais l'étiquette",
        "— Σ des posts imprimés C+G+ = 18,672 contre la médiane par run",
        "18,678 ; T = 39,405 contre 39,393 — la réconciliation PAR RUN (20/20)",
        "demeure la preuve d'exactitude (atelier-quatrebras-3lmyfb2xa/, les",
        "m4-*-run*.json : T 39.3930 · C+G+ 18.6780 · C+G 2.1810 · C 1.9680).",
        "",
        "LE CENSUS 559 (l'item 3) : 16+3+4+13+3+8+512 = 559 EXACT (le rapport",
        "rapport-census.txt de la présente) — la ligne v0.22.0 « 64 + 3 + 4 +",
        "13 + 3 + 8 + 512 » sommait à 607 : L'ERRATUM NOMMÉ.",
        "",
        f"LE VERDICT : {len(rouges)} ROUGE{'S' if len(rouges) > 1 else ''} nommé"
        f"{'s' if len(rouges) > 1 else ''} sur {len(RATIOS)} ratios audités — "
        "les trois corrections portées à l'édition v0.23.0.",
    ]
    (ICI / "rapport-audit-ratios.txt").write_text(
        "\n".join(lignes) + "\n", encoding="utf-8")
    (ICI / "audit-ratios.json").write_text(json.dumps(
        {"ratios": js, "rouges": len(rouges), "tolerance": TOL_DEFAUT},
        ensure_ascii=False, indent=1), encoding="utf-8")
    print("\n".join(lignes))
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
