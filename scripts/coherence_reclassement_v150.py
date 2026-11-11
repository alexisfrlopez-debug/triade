#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""coherence_reclassement_v150.py — LE CONTRÔLE DE COHÉRENCE
abstract ↔ résultats ↔ conclusion (l'exigence de l'instruction
xboh1kljq : « contrôle la cohérence abstract↔résultats↔conclusion »).

Le contrôle est MÉCANIQUE : chaque affirmation du reclassement doit se
trouver, COHÉRENTE, aux QUATRE endroits du manuscrit (abstract EN,
abstract FR, §2.3 la règle, §3.1 les résultats, la conclusion) et dans
la table 4 régénérée — et les PHRASES PÉRIMÉES (le compte unique de la
v0.15.0) doivent avoir DISPARU. Les chiffres du texte sont confrontés
aux CSV bruts du recompte (taux.csv) : 7/12 et 11/12, les deux
intervalles arrondis à 10⁻³, les 13 classes (7 pièce + 6 kit).

Verdict : VERT si toutes les assertions tiennent ; ÉCHEC sinon
(exception levée — aucune cohérence déclarée sans preuve).
"""
from __future__ import annotations

import csv
import pathlib

REPO = pathlib.Path(__file__).resolve().parents[1]
MAIN = REPO / "scripts" / "manuscrit_v150" / "main.tex"
TABLES = REPO / "scripts" / "manuscrit_v150" / "donnees" / "tables_generees.tex"
TAUX_CSV = REPO / "scripts" / "preuves_v150" / "reclassement" / "taux.csv"
DEFAUTS_CSV = REPO / "scripts" / "preuves_v150" / "reclassement" / "defauts.csv"

tex = MAIN.read_text(encoding="utf-8")
tables = TABLES.read_text(encoding="utf-8")
taux = {l["taux"]: l for l in csv.DictReader(open(TAUX_CSV, encoding="utf-8"))}
defauts = list(csv.DictReader(open(DEFAUTS_CSV, encoding="utf-8")))

# les chiffres BRUTS du recompte (jamais tapés à la main ici)
n_piece = sum(1 for d in defauts if d["catégorie"] == "PIÈCE")
n_kit = sum(1 for d in defauts if d["catégorie"] == "KIT")
t_piece = int(taux["pièce seule (métrique primaire RQ1 — le code natif "
                   "écrit par agent)"]["numérateur"])
t_ens = int(taux["ensemble kit+pièce (métrique de livraison)"]["numérateur"])
ic_piece = taux["pièce seule (métrique primaire RQ1 — le code natif "
                "écrit par agent)"]["ic95_scipy"].strip("[]").split(",")
ic_ens = taux["ensemble kit+pièce (métrique de livraison)"]["ic95_scipy"] \
    .strip("[]").split(",")
arr = lambda x: f"{float(x):.3f}"  # noqa: E731  (arrondi d'affichage)

assert n_piece == 7 and n_kit == 6 and len(defauts) == 13
assert t_piece == 7 and t_ens == 11

CONTROLES = [
    # (endroit, description, la condition)
    ("abstract EN", "la métrique primaire pièce seule (7/12)",
     "seven of twelve field iterations" in tex
     and "escaped defect of the sealed piece" in tex),
    ("abstract EN", "la métrique de livraison (11/12)",
     "the delivery\nmetric counts the kit+piece ensemble (eleven of "
     "twelve)" in tex),
    ("abstract EN", "le nommage par côté",
     "a class, a mechanism and a side before any fix" in tex),
    ("abstract FR", "la métrique primaire pièce seule (7/12)",
     "sept itérations de terrain sur douze" in tex
     and "défaut échappé de la pièce scellée" in tex),
    ("abstract FR", "la métrique de livraison (11/12)",
     "l'ensemble kit+pièce (onze sur douze)" in tex),
    ("abstract FR", "le nommage par côté",
     "chaque défaut nommé par classe,\nmécanisme et côté" in tex),
    ("§2.3", "les deux métriques définies",
     "primary RQ1\nmetric" in tex and "delivery metric}" in tex),
    ("§2.3", "la classification par côté",
     "classified by \\emph{side}" in tex),
    ("§2.3", "les trois exclusions",
     all(x in tex for x in ("[RET-NU]", "[CORBEILLE-VIDE]",
                            "[T0-P\\'ERIM\\'E]"))),
    ("§3.1", "le taux PRIMAIRE 7/12 en gras",
     "\\textbf{seven of twelve}" in tex),
    ("§3.1", "l'IC exact de la métrique primaire",
     f"$[{arr(ic_piece[0])}, {arr(ic_piece[1])}]$" in tex),
    ("§3.1", "le taux de livraison 11/12",
     "\\emph{eleven of twelve}" in tex),
    ("§3.1", "l'IC exact de la métrique de livraison",
     f"$[{arr(ic_ens[0])}, {arr(ic_ens[1])}]$" in tex),
    ("§3.1", "les 13 classes (7 pièce + 6 kit)",
     "\\textbf{thirteen} named defect classes" in tex
     and "\\emph{seven piece-side}" in tex
     and "\\emph{six kit-side}" in tex),
    ("§3.1", "la réserve de non-indépendance aux DEUX taux",
     "applies to\nthe piece-alone and the ensemble rate alike" in tex),
    ("§3.1", "l'archive du recompte citée",
     "preuves\\_v150/reclassement/" in tex),
    ("§3.1", "les six défauts de kit ne touchent pas la pièce",
     "The six kit-side classes never\ntouch the sealed native code"
     in tex),
    ("table 4", "la colonne Side",
     "\\textbf{Side}" in tables),
    ("table 4", "les runs 6 et 7 aux deux côtés",
     "6 & \\code{dev.6} & piece+kit" in tables
     and "7 & \\code{dev.7} & piece+kit" in tables),
    ("table 4", "la légende nomme le reclassement",
     "per-side recount" in tables),
    ("conclusion", "les 13 classes scindées",
     "thirteen named defect classes over\ntwelve field iterations" in tex
     and "seven in the sealed piece, six in the\nterrain kit" in tex),
    # --- les phrases périmées doivent avoir DISPARU ---
    ("périmé", "l'ancien compte unique «eleven named defect classes»",
     "eleven named defect classes" not in tex),
    ("périmé", "l'ancien «each of the eleven Loupe classes»",
     "eleven Loupe classes" not in tex),
    ("périmé", "l'ancienne phrase §3.1 «The exact Clopper-Pearson…for "
     "eleven of twelve is»",
     "for eleven of twelve is" not in tex),
    ("périmé", "l'ancienne règle «kit-side and piece-side defects both "
     "count» (remplacée par les deux métriques)",
     "kit-side and piece-side defects both count" not in tex),
    ("périmé", "l'ancien abstract FR «onze itérations…chacun nommé par "
     "classe et mécanisme»",
     "onze itérations de terrain sur" not in tex),
]

echecs = 0
print("LE CONTRÔLE DE COHÉRENCE abstract↔résultats↔conclusion "
      "(xboh1kljq)\n")
for endroit, description, ok in CONTROLES:
    etat = "VERT " if ok else "ÉCHEC"
    if not ok:
        echecs += 1
    print(f"  [{etat}] {endroit:10s} — {description}")

print()
if echecs:
    raise SystemExit(f"ÉCHEC : {echecs} contrôle(s) incohérent(s)")
print("VERDICT : VERT — les "
      f"{len(CONTROLES)} contrôles de cohérence tiennent "
      "(chiffres confrontés aux CSV bruts du recompte).")
