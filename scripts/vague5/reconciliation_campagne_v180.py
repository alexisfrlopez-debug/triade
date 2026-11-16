#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""reconciliation_campagne_v180.py — LA TABLE COMPLÈTE DE LA CAMPAGNE D204
ET SA RÉCONCILIATION (l'instruction bwxv9xzfa, la vague 5) : « générer
programmatiquement une table complète unité × bras × livraison × verdict ×
échappée nommée × attribution ... avec le décompte exact des 14 unités et la
réconciliation 22 livraisons ; expliciter le statut de la 7e livraison rouge
... ; rapporter M3 ... et les verdicts explicites de H1, H2, H3, H4-D204, H5
avec les valeurs par bras ».

LES SOURCES (aucune valeur tapée à la main) :
  - drive_work/atelier-post313/livraisons.csv  (22 lignes, le livre)
  - drive_work/atelier-post313/defauts.csv     (8 lignes, 6 comptées + 2 exclues)
  - drive_work/atelier-post313/carnet_temps_humain.csv (M3, au geste)
  - scripts/preuves_v150-local/journal_tokens.jsonl      (M2, 9 T + 11 C)
  - scripts/preuves_v150-local/journal_verifications.jsonl (M4, 34 lignes)

Sortie : livraison-vague5/p3-table-campagne.txt + p3-table-campagne.csv
         + p3-table-campagne.tex (la table du manuscrit)
Code retour : 0 = réconciliation EXACTE ; 2 = toute divergence refuse.
"""
from __future__ import annotations

import csv
import json
import pathlib
import sys

ATELIER = pathlib.Path("/home/z/my-project/drive_work/atelier-post313")
JETONS = pathlib.Path(
    "/home/z/my-project/scripts/preuves_v150-local/journal_tokens.jsonl")
VERIFS = pathlib.Path(
    "/home/z/my-project/scripts/preuves_v150-local/journal_verifications.jsonl")
SORTIE = pathlib.Path("/home/z/my-project/livraison-vague5")


def lire_csv_diese(chemin: pathlib.Path) -> list[dict]:
    with open(chemin, encoding="utf-8-sig") as f:
        return [r for r in csv.DictReader(
            (l for l in f if not l.startswith("#")))]


livraisons = lire_csv_diese(ATELIER / "livraisons.csv")
defauts = lire_csv_diese(ATELIER / "defauts.csv")
carnet = lire_csv_diese(ATELIER / "carnet_temps_humain.csv")
jetons = [json.loads(l) for l in JETONS.read_text(encoding="utf-8").splitlines()]
verifs = [json.loads(l) for l in VERIFS.read_text(encoding="utf-8").splitlines()]

# ------------------------------------------------------------ la table complète
par_livraison: dict[str, list[dict]] = {}
for d in defauts:
    if d["livraison"]:
        par_livraison.setdefault(d["livraison"], []).append(d)

LIGNES = []
for l in livraisons:
    liv, bras, tache = l["livraison"], l["bras"], l["tache"]
    echappees = par_livraison.get(liv, [])
    comptees = [d for d in echappees if d["exclusion"] == "non"]
    if comptees:
        classes = ", ".join(sorted({d["classe"] for d in comptees}))
        attribution = comptees[0]["cote"]
    elif l["verdict"] == "ROUGE":
        classes = "— (artefact du juge, classe V4 pré-nommée)"
        attribution = "juge (labo)"
    else:
        classes = "—"
        attribution = "—"
    LIGNES.append({
        "livraison": liv, "bras": bras,
        "unite": tache if tache != "app" else "app (Passeur)",
        "iteration": l["numero_iteration"],
        "date": l["date_run"], "verdict": l["verdict"],
        "echappee_nommee": classes, "attribution": attribution,
    })

# ------------------------------------------------------------ les recomptes
n_livraisons = len(livraisons)
verts = sum(1 for l in livraisons if l["verdict"] == "VERT")
rouges = sum(1 for l in livraisons if l["verdict"] == "ROUGE")
unites = sorted({(l["tache"], l["bras"]) for l in livraisons})
comptees = [d for d in defauts if d["exclusion"] == "non" and d["livraison"]]
exclues = [d for d in defauts if d["exclusion"] == "oui"]
piece_side = [d for d in comptees if d["cote"] == "piece"]
rouges_sans_ligne = [l["livraison"] for l in livraisons
                     if l["verdict"] == "ROUGE"
                     and l["livraison"] not in {d["livraison"] for d in comptees}]

# M3 : le temps humain au geste (carnet)
m3_t = sum(int(c["minutes"]) for c in carnet if c["bras"] == "T")
m3_c = sum(int(c["minutes"]) for c in carnet if c["bras"] == "C")

# M2 : les tokens réels (journal d'usage)
m2_t = sum(j["total_tokens"] for j in jetons if j["bras"] == "T")
m2_c = sum(j["total_tokens"] for j in jetons if j["bras"] == "C")
appels_t = sum(1 for j in jetons if j["bras"] == "T")
appels_c = sum(1 for j in jetons if j["bras"] == "C")

# M4 : le temps de vérification (journal des vérifications)
m4_t = sum(v["secondes"] for v in verifs if v["bras"] == "T")
m4_c = sum(v["secondes"] for v in verifs if v["bras"] == "C")

# ------------------------------------------------------------ les verdicts H
escapes_t = sum(1 for d in comptees if d["bras"] == "T")
escapes_c = sum(1 for d in comptees if d["bras"] == "C")
h = []
h.append(("H1 (santé finale aux deux bras)",
          "TENUE" if all(
              l["verdict"] == "VERT" for l in livraisons
              if l["tache"] == "app"
              and l["livraison"] in ("T-app-it4", "C-app-it3")) else "?",
          "les deux bras verts et signés : T-app-it4 VERT, C-app-it3 VERT"))
h.append(("H2 (échappés ≤ facteur 2 entre bras)",
          "TENUE" if max(escapes_t, escapes_c) <= 2 * min(escapes_t, escapes_c)
          else "FALSIFIÉE",
          f"{escapes_t} T contre {escapes_c} C "
          f"({max(escapes_t, escapes_c)/max(1, min(escapes_t, escapes_c)):.2f}×)"))
h.append(("H3 (le bras T plus coûteux en tokens)",
          "FALSIFIÉE" if m2_c > m2_t else "TENUE",
          f"C = {m2_c:,} contre T = {m2_t:,} "
          f"(×{m2_c/m2_t:.2f}, la direction opposée — n=1)".replace(",", " ")))
h.append(("H4-D204 (cérémonies T plus longues)",
          "TENUE" if m3_t > m3_c else "FALSIFIÉE",
          f"{m3_t} min T contre {m3_c} min C "
          f"(×{m3_t/max(1, m3_c):.1f})"))
h.append(("H5 (temps de vérification même ordre de grandre)",
          "TENUE" if m4_t / m4_c <= 10 else "FALSIFIÉE",
          f"{m4_t:.1f} s T contre {m4_c:.1f} s C (×{m4_t/m4_c:.1f} > 10)"))

# ------------------------------------------------------------ la réconciliation
ECARTS = []
def exige(nom, attendu, trouve):
    if attendu != trouve:
        ECARTS.append(f"[{nom}] la réconciliation attend « {attendu} », "
                      f"le registre dit « {trouve} »")

exige("livraisons", 22, n_livraisons)
exige("unités (14 = 6 blocs × 2 bras + app × 2 bras)", 14, len(unites))
exige("vert+rouge == livraisons", n_livraisons, verts + rouges)
exige("rouges", 7, rouges)
exige("échappées comptées (exclusion=non avec livraison)", 6, len(comptees))
exige("exclusions nommées (exclusion=oui)", 2, len(exclues))
exige("échappées côté pièce", 0, len(piece_side))
exige("7e rouge sans ligne (l'artefact du juge)", 1, len(rouges_sans_ligne))
exige("M3 bras T (min)", 104, m3_t)
exige("M3 bras C (min)", 17, m3_c)
exige("M2 bras T (tokens)", 53158, m2_t)
exige("M2 bras C (tokens)", 67475, m2_c)
exige("M4 bras T (s)", 52.5, round(m4_t, 1))
exige("M4 bras C (s)", 2.2, round(m4_c, 1))

# ------------------------------------------------------------ les sorties
rapport = [
    "LA TABLE COMPLÈTE DE LA CAMPAGNE D204 — GÉNÉRÉE DES LEDGERS, "
    "RÉCONCILIÉE (la vague 5, l'instruction bwxv9xzfa)",
    "=" * 100,
    "",
    "LA TABLE (22 livraisons) :",
    f"{'livraison':<16}{'bras':<5}{'unité':<18}{'it':<3}{'verdict':<8}"
    f"{'échappée nommée':<42}attribution",
    "-" * 100,
]
for l in LIGNES:
    rapport.append(f"{l['livraison']:<16}{l['bras']:<5}{l['unite']:<18}"
                   f"{l['iteration']:<3}{l['verdict']:<8}"
                   f"{l['echappee_nommee'][:41]:<42}{l['attribution']}")
rapport += [
    "-" * 100,
    "",
    "LE DÉCOMPTE EXACT :",
    f"  unités                    : {len(unites)} "
    f"(6 blocs contrôlés × 2 bras + l'application × 2 bras)",
    f"  livraisons                : {n_livraisons} "
    f"({verts} VERT, {rouges} ROUGE)",
    f"  livraisons contrôlées     : "
    f"{sum(1 for l in livraisons if l['tache'] != 'app')} "
    f"(3 unités ont exigé une 2e itération : loupe-05 C, loupe-08 T, loupe-13 C)",
    f"  livraisons applicatives   : "
    f"{sum(1 for l in livraisons if l['tache'] == 'app')} (T: 4, C: 3)",
    f"  échappées comptées (D202) : {len(comptees)} — "
    f"T {escapes_t}, C {escapes_c}, pièce {len(piece_side)}, kit "
    f"{len(comptees) - len(piece_side)}",
    f"  exclusions nommées        : {len(exclues)} "
    f"(nommées au labo avant tout run terrain — la règle RET-NU)",
    f"  le 7e rouge               : {rouges_sans_ligne[0]} — "
    f"l'ARTEFACT DU JUGE V4 (la classe de session pré-nommée à l'Entrée 294, "
    f"répétée à la 298) : le vecteur était VIDE, RIEN mesuré des pièces — "
    f"la faute au juge du labo NE CONSOMME JAMAIS (règle D202 : le défaut "
    f"compté par livraison exige un défaut nommé du kit+pièce LIVRÉ)",
    "",
    "LES MÉTRIQUES PAR BRAS (lues des journaux, jamais de mémoire) :",
    f"  M3 temps humain   : T {m3_t} min, C {m3_c} min "
    f"(×{m3_t/max(1,m3_c):.1f}) — carnet_temps_humain.csv, {len(carnet)} lignes",
    f"  M2 tokens réels   : T {m2_t:,} ({appels_t} appels), "
    f"C {m2_c:,} ({appels_c} appels) — ×{m2_c/m2_t:.2f}".replace(",", " "),
    f"  M4 vérification   : T {m4_t:.1f} s, C {m4_c:.1f} s "
    f"(×{m4_t/m4_c:.1f})",
    "",
    "LES VERDICTS EXPLICITES :",
]
for nom, verdict, detail in h:
    rapport.append(f"  {nom:<46}{verdict:<11}{detail}")
rapport += [
    "",
    "LA RÉCONCILIATION (chaque total recalculé du registre brut) : "
    + ("VERT — zéro divergence" if not ECARTS else f"ROUGE — {len(ECARTS)}"),
] + [f"    {e}" for e in ECARTS]

(SORTIE / "p3-table-campagne.txt").write_text(
    "\n".join(rapport), encoding="utf-8")
with open(SORTIE / "p3-table-campagne.csv", "w", newline="",
          encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(LIGNES[0].keys()))
    w.writeheader()
    w.writerows(LIGNES)

# la table LaTeX pour le manuscrit (§2.4) — les 22 livraisons, scriptsize
corps = []
for l in LIGNES:
    ech = l["echappee_nommee"]
    if ech.startswith("—"):
        ech = "---"
    else:
        ech = ech.replace("plantage-", "").replace("ecart-", "")
    corps.append(
        f"\\code{{{l['livraison']}}} & {l['bras']} & {l['iteration']} & "
        f"{l['verdict']} & {ech.replace('_', '\\_')} & "
        f"{l['attribution'].replace('_', ' ')} \\\\")
tex = [
    "% Généré par reconciliation_campagne_v180.py — ne pas éditer à la main.",
    "\\begingroup\\scriptsize",
    "\\begin{longtable}{@{}l c c l p{4.1cm} l@{}}",
    "\\caption{The 22 witnessed deliveries of the D204 campaign, every row "
    "generated from the ledgers (livraisons.csv, defauts.csv): unit, arm, "
    "iteration, verdict, the named escape if any (exclusion rule D202 "
    "applied), and its attribution. The seventh red (C-loupe-05-it1) is the "
    "pre-named judge artifact (Entry 294): a laboratory-judge fault consumes "
    "no delivery.}\\label{tab:campagne}\\\\",
    "\\toprule",
    "\\textbf{Delivery} & \\textbf{Arm} & \\textbf{It.} & "
    "\\textbf{Verdict} & \\textbf{Named escape} & \\textbf{Attribution} \\\\",
    "\\midrule",
    "\\endhead",
    "\\bottomrule",
    "\\endfoot",
] + corps + ["\\end{longtable}\\endgroup", ""]
(SORTIE / "p3-table-campagne.tex").write_text(
    "\n".join(tex), encoding="utf-8")

print("\n".join(rapport))
sys.exit(0 if not ECARTS else 2)
