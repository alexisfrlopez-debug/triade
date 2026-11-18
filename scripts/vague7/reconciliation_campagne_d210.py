#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""reconciliation_campagne_d210.py — LA TABLE DE LA CAMPAGNE D210 (v0.19.0)
ET SA RÉCONCILIATION. Génère edition-v0190/donnees/table-campagne-d210.tex
depuis les registres reçus (reception-357) ; refuse toute divergence (code 2).

LES SOURCES (aucune valeur tapée à la main) :
  - scripts/campagne_d204/reception-357/livraisons.csv  (29 lignes, le livre)
  - scripts/campagne_d204/reception-357/defauts.csv     (11 défauts nommés)
  - scripts/campagne_d204/reception-357/carnet_temps_humain.csv (M3, au geste)

LA RÉCONCILIATION ATTENDUE (consignée aux Entrées 352/354/355/357) :
  - 29 lignes de campagne au livre dont SEPT de D210 (4 VERT + 3 ROUGE)
  - les TROIS échappées comptées de D210 : toutes côté kit, la pièce jamais fautive
  - l'attribution C-loupe-16-attr-it1 VERT, AUCUN défaut
  - le carnet : CINQ lignes run-terrain D210 (2 GUI + 3 main), T 4 min / C 1 min
"""
from __future__ import annotations

import csv
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
ATELIER = REPO / "scripts/campagne_d204/reception-357"
SORTIE = REPO / "edition-v0190/donnees/table-campagne-d210.tex"


def lire_csv_diese(chemin: pathlib.Path) -> list[dict]:
    with open(chemin, encoding="utf-8-sig") as f:
        return [r for r in csv.DictReader(
            (l for l in f if not l.startswith("#")))]


livraisons = lire_csv_diese(ATELIER / "livraisons.csv")
defauts = lire_csv_diese(ATELIER / "defauts.csv")
carnet = lire_csv_diese(ATELIER / "carnet_temps_humain.csv")

# ------------------------------------------------------------ le bloc D210
d210 = [l for l in livraisons if l["tache"].endswith("-d210") or l["tache"] == "loupe-16-attr"]
par_livraison: dict[str, list[dict]] = {}
for d in defauts:
    if d["livraison"]:
        par_livraison.setdefault(d["livraison"], []).append(d)

LIGNES = []
for l in d210:
    liv = l["livraison"]
    echappees = [d for d in par_livraison.get(liv, []) if d["exclusion"] == "non"]
    if echappees:
        classes = " / ".join(sorted({d["classe"] for d in echappees}))
        attribution = echappees[0]["cote"] + " (judge)"
    else:
        classes = "---"
        attribution = "—"
    LIGNES.append({
        "livraison": liv, "bras": l["bras"],
        "iteration": l["numero_iteration"],
        "date": l["date_run"], "verdict": l["verdict"],
        "echappee": classes, "attribution": attribution,
    })

# ------------------------------------------------------------ les recomptes
n_d210 = len(d210)
verts = sum(1 for l in d210 if l["verdict"] == "VERT")
rouges = sum(1 for l in d210 if l["verdict"] == "ROUGE")
comptees = [d for d in defauts
            if d["livraison"] and d["exclusion"] == "non"
            and (d["livraison"].startswith("T-loupe-16-d210"))]
cotes = sorted({d["cote"] for d in comptees})
attr = [l for l in d210 if "attr" in l["livraison"]]
attr_vert = [l for l in attr if l["verdict"] == "VERT"]
attr_defauts = [d for d in defauts if d["livraison"] and "attr" in d["livraison"]]

carnet_d210 = [c for c in carnet if c["geste"] == "run-terrain"
               and (c["tache"].endswith("-d210") or c["tache"] == "loupe-16-attr")]
minutes_t = sum(int(c["minutes"]) for c in carnet_d210 if c["bras"] == "T")
minutes_c = sum(int(c["minutes"]) for c in carnet_d210 if c["bras"] == "C")

# ------------------------------------------------------------ la table TeX
corps = []
for r in LIGNES:
    ech = r["echappee"] if r["echappee"] != "---" else "---"
    corps.append(
        "\\code{%s} & %s & %s & %s & %s & %s \\\\" % (
            r["livraison"], r["bras"], r["iteration"], r["verdict"],
            ech, r["attribution"]))
tex = """%% Généré par scripts/vague7/reconciliation_campagne_d210.py — ne pas éditer à la main.
%% Sources : les registres reçus (reception-357) — livraisons.csv (29 lignes), defauts.csv (11), le carnet.
\\begingroup\\scriptsize
\\begin{longtable}{@{}l c c c l l@{}}
\\caption{The seven witnessed deliveries of the D210 extension campaign (the plan pre-registered, hash consigned before any measurement; the arm order drawn publicly from the consigned seed: the T arm first in all four units, a one-in-eight event consigned as drawn). Every row is generated from the ledgers: the iteration column is the ledger's as filed. The fourth unit closed on its red at the delivery cap --- three counted escapes, every one kit-side in the shared scenario/judge, the piece never at fault at either format; the empirical attribution re-delivered the same C piece through a minimal standard kit and read 14 VERT, 0 ROUGE.}\\label{tab:campagne-d210}\\\\
\\toprule
\\textbf{Delivery} & \\textbf{Arm} & \\textbf{It.} & \\textbf{Verdict} & \\textbf{Named escape} & \\textbf{Attribution} \\\\
\\midrule
\\endhead
\\bottomrule
\\endfoot
%s
\\end{longtable}\\endgroup
""" % "\n".join(corps)
SORTIE.parent.mkdir(parents=True, exist_ok=True)
SORTIE.write_text(tex, encoding="utf-8")

# ------------------------------------------------------------ le verdict
ok = True
def check(cond, msg):
    global ok
    print(("  VERT  " if cond else "  ROUGE ") + msg)
    if not cond:
        ok = False

print("LA RÉCONCILIATION DE LA CAMPAGNE D210 (v0.19.0)")
check(n_d210 == 7, f"7 livraisons D210 au livre (lu {n_d210})")
check(verts == 4 and rouges == 3, f"4 VERT + 3 ROUGE (lu {verts}+{rouges})")
check(len(livraisons) == 29, f"le livre à 29 lignes de campagne (lu {len(livraisons)})")
check(len(comptees) == 3, f"3 échappées comptées D210 (lu {len(comptees)})")
check(cotes == ["kit"], f"toutes côté kit (lu {cotes})")
check(len(attr) == 1 and len(attr_vert) == 1, "l'attribution : 1 livraison VERT")
check(len(attr_defauts) == 0, "AUCUN défaut pour l'attribution (VERT)")
check(len(carnet_d210) == 5, f"le carnet : 5 lignes run-terrain D210 (lu {len(carnet_d210)})")
check(minutes_t == 4 and minutes_c == 1, f"M3 D210 : T {minutes_t} min / C {minutes_c} min")
check(all(r["echappee"] != "---" for r in LIGNES if r["verdict"] == "ROUGE"),
      "chaque ROUGE porte son échappée nommée")

print()
print(f"table générée : {SORTIE} ({len(tex)} o, {len(LIGNES)} lignes)")
sys.exit(0 if ok else 2)
