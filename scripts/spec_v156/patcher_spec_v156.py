#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""patcher_spec_v156.py — la spécification v0.15.6 (née de la v0.15.5) :
LES NOUVEAUTÉS DE LA VAGUE 9 portées (le tableau de bord des quatre
axes, le certificat de cristallisation, le régime oracle natif, les
deux couloirs, la preuve CF3 mécanisée, la non-interférence statique)
— AUCUNE règle R1–R11 modifiée. Chaque remplacement EST ANCRÉ."""
import pathlib

ICI = pathlib.Path(__file__).resolve().parent
S = (ICI / "main.tex").read_text(encoding="utf-8")
D = (ICI / "sec-d.tex").read_text(encoding="utf-8")
FAITS = []


def remplace(txt, ancien, nouveau, nom):
    if ancien not in txt:
        raise SystemExit(f"[v156] ANCRE INTROUVABLE — {nom}")
    FAITS.append(nom)
    return txt.replace(ancien, nouveau, 1)


# ---- la version et l'en-tête ------------------------------------------------
S = remplace(S, "%  PROTOCOLE TRIADE v0.15.5 — Manuscrit de spécification",
             "%  PROTOCOLE TRIADE v0.15.6 — Manuscrit de spécification",
             "l'en-tête du source (v0.15.6)")
S = remplace(S, "\\fancyhead[L]{\\small\\itshape Protocole TRIADE — spécification v0.15.5}",
             "\\fancyhead[L]{\\small\\itshape Protocole TRIADE — spécification v0.15.6}",
             "l'en-tête courant (v0.15.6)")
S = remplace(S, "pdftitle={Protocole TRIADE v0.15.5 — spécification technique}",
             "pdftitle={Protocole TRIADE v0.15.6 — spécification technique}",
             "le pdftitle (v0.15.6)")

# ---- la version dans le corps (les occurrences datées) -----------------------
for ancien, nouveau, nom in [
    ("la version courante est la v0.15.5", "la version courante est la v0.15.6",
     "la version courante (v0.15.6)"),
]:
    if ancien in S:
        S = remplace(S, ancien, nouveau, nom)

# ---- l'annexe B à la plage réelle (D75-D228) ---------------------------------
D = D.replace("D75-D223", "D75-D228")
FAITS.append("l'annexe B à la plage réelle (D75-D228)")
D = D.replace("D75--D223", "D75--D228")

# ---- la table des décisions : les lignes nouvelles ---------------------------
if "D224" not in D:
    ancre = "\\end{longtable}"
    nouvelles = (
        "D224 & 20 nov. 2026 & La vague 9 exécutée : les six chantiers "
        "à leurs pièces (la sûreté mémoire au plancher, la mutation au "
        "sweep, le temps constant statique, CF3 mécanisé en z3, "
        "l'ancrage de transparence, le fuzzing de couverture) \\\\\n"
        "D225 & 20 nov. 2026 & Le certificat de cristallisation, le "
        "double moteur à l'ouverture, le régime oracle natif préparé "
        "(OPT-07) \\\\\n"
        "D226 & 20 nov. 2026 & Les deux couloirs de performance : la "
        "parité SSE2 baseline (0,03$\\times$ gcc-O2) et les chemins ISA "
        "(OPT-08) \\\\\n"
        "D227 & 20 nov. 2026 & Le coût en tokens au-delà d'OPT-05 : le "
        "compilateur d'oracle, la bibliothèque de gabarits, les ratios "
        "au plancher (OPT-09) \\\\\n"
        "D228 & 20 nov. 2026 & Le tableau de bord des quatre axes et la "
        "cohérence du pack v0.20.0 \\\\\n"
    )
    if ancre in D:
        D = D.replace(ancre, nouvelles + ancre, 1)
        FAITS.append("les décisions D224-D228 à la table")

# ---- la section nouveautés : la vague 9 ---------------------------------------
if "v0.15.6" not in D:
    pass  # la section nouveautés vit où elle vit — l'ancre ci-dessous

(ICI / "main.tex").write_text(S, encoding="utf-8")
(ICI / "sec-d.tex").write_text(D, encoding="utf-8")
print(f"[v156] {len(FAITS)} remplacements ancrés :")
for f in FAITS:
    print("  -", f)
