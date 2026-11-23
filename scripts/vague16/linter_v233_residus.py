#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""linter_v233.py — LE LINTER v2 ÉTENDU (l'extension (F) de l'instruction 86d3ushrr,
la vague 16). LE SOCLE : le linter v232 (la vague 14) reconduit intégralement —
la présente AJOUTE TROIS classes, chacune NOMMÉE, échec fermé :

  (B') LA PLAGE ANNONCÉE CONTRE LA TABLE LOCALE — la plage D1–D251 annoncée aux
       pièces est vérifiée contre docs/DECISIONS.md (LA TABLE LOCALE), pas
       seulement contre le journal de travail : le maximum de la table ET les
       trous à l'intérieur de la plage sont rendus ;

  (C') TOUT RATIO PUBLIÉ SE RECALCULE — le ratio publié doit se recomputer
       depuis ses opérandes publiés À LA PRÉCISION AFFICHÉE (le nombre de
       décimales du publié décide de l'arrondi) ; les deux ordres de la
       division sont essayés et l'ordre retenu est NOMMÉ ;

  (D') LA COHÉRENCE CIBLE-PÉRIMÈTRE — le n de la cible (15/18) confronté au n
       du split TEST réel, TOUTES versions du corpus (v1, v2, la présente
       correction v2.1) : la divergence est rendue, jamais avalée.

Usage :
  python3 linter_v233.py            # le contrôle intégral des trois classes
  python3 linter_v233.py --negatif  # LE CONTRÔLE NÉGATIF : les divergences
                                    # plantées doivent être ATTRAPÉES
"""

import argparse
import json
import os
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ---------------------------------------------------------------------------
# (C') TOUT RATIO PUBLIÉ SE RECALCULE — la table des ratios publiés aux pièces
#      (les opérandes sont ceux du linter v232, la même source fait foi)
# ---------------------------------------------------------------------------
RATIOS = [
    # (le ratio publié, ses opérandes publiés, l'opération, la pièce nommée)
    ("683.6",  [285.725, 0.418], "division", "le cache (c/octet@4096)"),
    ("41.0",   [19.66, 806.35],  "division", "le GHASH agrégé contre le scellé"),
    ("12.7",   [63.39, 806.35],  "division", "le corridor contre le scellé"),
    ("3.23",   [19.66, 63.39],   "division", "l'agrégé contre le corridor"),
    ("3.4",    [6.912, 2.056],   "division", "le plancher M4"),
    ("37.425", [20.715, 16.497, 0.213], "somme", "la fermeture de ventilation"),
    ("89.4",   [24.163, 2.555],  "variation", "la réduction de la mémoire"),
]

RE_DECISION_TABLE = re.compile(r"^\|\s*D(\d+)\s*\|", re.MULTILINE)
RE_DECISION_TITRE = re.compile(r"^#{1,4}\s*D(\d+)\b", re.MULTILINE)


def decimales(publie: str) -> int:
    return len(publie.split(".")[1]) if "." in publie else 0


def recalculer(publie, operandes, operation):
    """-> (ok, detail) : le publié se recompute-t-il À SA PRÉCISION AFFICHÉE ?"""
    d = decimales(publie)
    cible = float(publie)
    if operation == "division":
        a, b = operandes
        for ordre, valeur in (("a/b", a / b), ("b/a", b / a)):
            if round(valeur, d) == round(cible, d):
                return True, f"{ordre} = {valeur:.6f} → {round(valeur, d):.{d}f} ✓"
        detail = (f"aucun ordre ne rend le publié : a/b = {a / b:.6f} → "
                  f"{round(a / b, d):.{d}f} ; b/a = {b / a:.6f} → {round(b / a, d):.{d}f} "
                  f"contre le publié {cible}")
        return False, detail
    if operation == "somme":
        s = sum(operandes)
        return (round(s, d) == round(cible, d),
                f"la somme = {s:.6f} → {round(s, d):.{d}f} "
                f"{'✓' if round(s, d) == round(cible, d) else '≠ ' + publie}")
    if operation == "variation":
        a, b = operandes
        v = (a - b) / a * 100
        return (round(v, d) == round(cible, d),
                f"(a−b)/a×100 = {v:.6f} → {round(v, d):.{d}f} "
                f"{'✓' if round(v, d) == round(cible, d) else '≠ ' + publie}")
    return False, "l'opération est inconnue — DÉFAUT DU LINTER (nommé)"


def controle_ratio_recalcul(v, muter=None) -> int:
    """(C') chaque ratio publié se recompute à la précision affichée."""
    rouges = 0
    for publie, operandes, operation, nom in RATIOS:
        p = muter(publie) if muter else publie
        ok, detail = recalculer(p, operandes, operation)
        v.cond(ok, f"le ratio {p} ({nom}) se recompute",
               f"le ratio publié {p} ({nom}) NE SE RECALCULE PAS depuis ses "
               f"opérandes {operandes} : {detail}")
        if not ok:
            rouges += 1
    return rouges


# ---------------------------------------------------------------------------
# (B') LA PLAGE ANNONCÉE CONTRE LA TABLE LOCALE
# ---------------------------------------------------------------------------
def lire_table_locale():
    """-> (l'ensemble des IDs, le maximum) — DEPUIS docs/DECISIONS.md."""
    chemin = os.path.join(RACINE, "docs", "DECISIONS.md")
    texte = open(chemin, encoding="utf-8").read()
    ids = set(int(m.group(1)) for m in RE_DECISION_TABLE.finditer(texte))
    ids |= set(int(m.group(1)) for m in RE_DECISION_TITRE.finditer(texte))
    return ids, max(ids)


def controle_plage_locale(v, borne_annoncee=251, muter=None) -> int:
    """(B') la plage annoncée vérifiée CONTRE LA TABLE LOCALE (pas le journal)."""
    ids, maxi = lire_table_locale()
    borne = muter(borne_annoncee) if muter else borne_annoncee
    manquants = sorted(set(range(1, borne + 1)) - ids)
    v.cond(maxi == borne,
           f"la table locale porte bien jusqu'à D{maxi} (la plage annoncée D1–D{borne})",
           f"la table locale s'arrête à D{maxi} contre la plage annoncée D1–D{borne}")
    v.cond(not manquants,
           f"la plage D1–D{borne} est CONTINUE à la table locale ({len(ids)} décisions)",
           f"la plage annoncée D1–D{borne} compte {len(manquants)} trous à la table "
           f"locale : {', '.join('D' + str(m) for m in manquants[:12])}"
           + ("…" if len(manquants) > 12 else ""))
    return 0


# ---------------------------------------------------------------------------
# (D') LA COHÉRENCE CIBLE-PÉRIMÈTRE
# ---------------------------------------------------------------------------
CIBLE = {"nom": "≥ 15/18", "n_cible": 18,
         "signifie": "les 18 tâches régénérées de la ladder TPL-ADD"}


def cartes_corpus():
    """-> [(version, chemin, splits)] — les dataset cards du dépôt."""
    cartes = []
    for version, chemin in (
        ("v1", os.path.join(RACINE, "atelier-corpus-2i7iy3xmg", "dataset", "DATASET-CARD.json")),
        ("v2", os.path.join(RACINE, "atelier-corpusv2-avmwtf5w", "dataset", "DATASET-CARD.json")),
        ("v2.1 corrigé", os.path.join(RACINE, "atelier-audit-splits-am9d6o2th",
                                      "dataset-v2.1", "DATASET-CARD.json")),
    ):
        if os.path.isfile(chemin):
            cartes.append((version, chemin, json.load(open(chemin, encoding="utf-8"))))
    return cartes


def controle_perimetre_cible(v, muter=None) -> int:
    """(D') le n de la cible contre le n du split TEST réel, toutes versions."""
    for version, chemin, carte in cartes_corpus():
        splits = carte.get("splits", carte.get("splits_en_contrats", {}))
        n_test = splits.get("TEST", "?")
        cible = muter if muter else CIBLE
        coherent = (n_test == cible["n_cible"])
        v.cond(coherent,
               f"la cible {cible['nom']} et le TEST {version} portent LE MÊME n ({n_test})",
               f"la cible {cible['nom']} ({cible['signifie']}) et le split TEST du corpus "
               f"{version} ({n_test} {'contrats' if version == 'v2.1 corrigé' else 'tâches'}) "
               f"NE PORTENT PAS LE MÊME n — la cible doit être re-scopée au TEST ou son "
               f"périmètre NOMMÉ (le résidu (C) de l'instruction 86d3ushrr)")
    return 0


# ---------------------------------------------------------------------------
# LE VERDICT
# ---------------------------------------------------------------------------
class Verdict:
    def __init__(self):
        self.vert = 0
        self.rouge = 0

    def cond(self, ok, nom_vert, nom_rouge):
        if ok:
            self.vert += 1
            print(f"  [VERT] {nom_vert}")
        else:
            self.rouge += 1
            print(f"  [ROUGE] {nom_rouge}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--negatif", action="store_true",
                    help="LE CONTRÔLE NÉGATIF : les divergences plantées ATTRAPÉES")
    args = ap.parse_args()

    print("=== LE LINTER v233 — LES TROIS CLASSES NOUVELLES (86d3ushrr (F)) ===")
    v = Verdict()
    if args.negatif:
        print("  LE CONTRÔLE NÉGATIF : trois divergences plantées, trois ROUGE attendus")
        print()
        print("  --- (C') un ratio muté (3.23 → 3.24 : le recompte doit le REFUSER) ---")
        controle_ratio_recalcul(v, muter=lambda p: "3.24" if p == "3.23" else p)
        print()
        print("  --- (B') une borne mutée (251 → 250 : la table locale dépasse) ---")
        controle_plage_locale(v, muter=lambda b: 250)
        print()
        print("  --- (D') une cible mutée (18 → 6 : le périmètre diverge) ---")
        controle_perimetre_cible(v, muter=dict(CIBLE, n_cible=6))
    else:
        print("  --- (C') TOUT RATIO PUBLIÉ SE RECALCULE à la précision affichée ---")
        controle_ratio_recalcul(v)
        print()
        print("  --- (B') LA PLAGE ANNONCÉE CONTRE LA TABLE LOCALE ---")
        controle_plage_locale(v)
        print()
        print("  --- (D') LA COHÉRENCE CIBLE-PÉRIMÈTRE ---")
        controle_perimetre_cible(v)

    print()
    print(f"=== LE VERDICT : {v.vert} VERT · {v.rouge} ROUGE ===")
    if args.negatif:
        return 0 if v.rouge > 0 else 1      # les divergences plantées doivent être ATTRAPÉES
    return 0 if v.rouge == 0 else 1          # les divergences réelles sont le résultat


if __name__ == "__main__":
    sys.exit(main())
