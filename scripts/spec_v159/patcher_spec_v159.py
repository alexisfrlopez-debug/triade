#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""patcher_spec_v159.py — la spécification v0.15.17 (née de v0.15.16 par copie) :
LES RÉSIDUS ÉDITORIAUX (W27RESID, la vague 27, prompt 2). (a) La Table 12
(axe 3, filigrane de l'Intention) disait « treize arbres signés … verifier 13
arbres VERTS » à l'état courant alors que le sceau porte QUATORZE arbres depuis
D177 (loupe.1 le quatorzième) : porté à quatorze / verifier 14, les colonnes
historiques M8 (12 arbres, D162/D163) et M9 (13 arbres, D166/D168) DEMEURANT
DATÉES. (b) Les titres dupliqués §1.23/§1.24 « Ce que change la v0.15.16 »
DISTINGUÉS (D274 les six résidus ; D275 la prose de statut dérivée). (c) La
section de version v0.15.17 ajoutée. Chaque remplacement EST ANCRÉ."""
import pathlib
import shutil

ICI = pathlib.Path(__file__).resolve().parent
SRC = ICI.parent / "spec_v158"
for f in [SRC / "main.tex", *SRC.glob("sec-*.tex"), SRC / "chaine_cf.png"]:
    if f.exists():
        shutil.copy2(f, ICI / f.name)

M = (ICI / "main.tex").read_text(encoding="utf-8")
A = (ICI / "sec-a.tex").read_text(encoding="utf-8")
CF = (ICI / "sec-cf.tex").read_text(encoding="utf-8")
FAITS = []


def remplace(txt, ancien, nouveau, nom):
    if ancien not in txt:
        raise SystemExit(f"[v159] ANCRE INTROUVABLE — {nom}")
    if txt.count(ancien) != 1:
        raise SystemExit(f"[v159] ANCRE NON UNIQUE ({txt.count(ancien)}×) — {nom}")
    FAITS.append(nom)
    return txt.replace(ancien, nouveau)


# ---- l'en-tête et les versions (v0.15.17) -----------------------------------
M = remplace(M, "%  PROTOCOLE TRIADE v0.15.16 — Manuscrit de spécification",
             "%  PROTOCOLE TRIADE v0.15.17 — Manuscrit de spécification",
             "l'en-tête (v0.15.17)")
M = remplace(M, r"\fancyhead[L]{\small\itshape Protocole TRIADE — spécification v0.15.16}",
             r"\fancyhead[L]{\small\itshape Protocole TRIADE — spécification v0.15.17}",
             "le running header (v0.15.17)")
M = remplace(M, "pdftitle={Protocole TRIADE v0.15.16 — spécification technique},",
             "pdftitle={Protocole TRIADE v0.15.17 — spécification technique},",
             "le pdftitle (v0.15.17)")

# ---- (b) LES TITRES DUPLIQUÉS DISTINGUÉS -------------------------------------
A = remplace(A, r"\subsection{Ce que change la v0.15.16}\label{sec:nouveautes1514}",
             r"\subsection{Ce que change la v0.15.16 — les six résidus (D274)}\label{sec:nouveautes1514}",
             "le titre §1.23 distingué (D274)")
A = remplace(A, r"\subsection{Ce que change la v0.15.16}\label{sec:nouveautes1515}",
             r"\subsection{Ce que change la v0.15.16 — la prose de statut dérivée (D275)}\label{sec:nouveautes1515}",
             "le titre §1.24 distingué (D275)")

# ---- (a) LA TABLE 12, AXE 3 : quatorze arbres à l'état courant ---------------
CF = remplace(CF,
              "\\textbf{livré, prouvé terrain} — treize arbres signés ;\n"
              "re-cérémonie réelle D126, cérémonies d'ère M8 (12 arbres, D162/D163) et M9 (13\n"
              "arbres, D166/D168) passées sur pièces — verifier 13 arbres VERTS",
              "\\textbf{livré, prouvé terrain} — quatorze arbres signés (D177 : loupe.1 le\n"
              "quatorzième) ; re-cérémonie réelle D126, cérémonies d'ère M8 (12 arbres, D162/D163)\n"
              "et M9 (13 arbres, D166/D168) passées sur pièces — verifier 14 arbres VERTS",
              "la Table 12 axe 3 : quatorze arbres, verifier 14 (D177)")

# ---- (c) LA SECTION DE VERSION v0.15.17 ---------------------------------------
A = remplace(A,
             "\\subsection{Ce que change la v0.15.16 — la prose de statut dérivée (D275)}\\label{sec:nouveautes1515}",
             "\\subsection{Ce que change la v0.15.16 — la prose de statut dérivée (D275)}\\label{sec:nouveautes1515}\n"
             "\n"
             "\\subsection{Ce que change la v0.15.17}\\label{sec:nouveautes1517}\n"
             "\n"
             "La v0.15.17 porte les résidus éditoriaux de la vague 27 : la Table 12 (axe 3) dit\n"
             "\\textbf{quatorze arbres} à l'état courant — D177 avait fait entrer \\code{loupe.1} comme\n"
             "quatorzième arbre du sceau, la cellule était restée à treize —, les colonnes historiques\n"
             "(M8 : 12 arbres, D162/D163 ; M9 : 13 arbres, D166/D168) demeurant datées ; les deux\n"
             "sous-sections de la v0.15.16 portent des titres distincts (D274 les six résidus,\n"
             "D275 la prose de statut dérivée) ; la chronologie du terrain du Livre du Coffre est\n"
             "réordonnée aux dates imprimées. La porte de génération couvre les classes nouvelles\n"
             "de la vague (STATUS-INTERPIECES, COUNT-TABLECELL, TITLE-UNIQUE, LANG-BODY). Aucune\n"
             "valeur mesurée n'est modifiée.",
             "la section de version v0.15.17")

(ICI / "main.tex").write_text(M, encoding="utf-8")
(ICI / "sec-a.tex").write_text(A, encoding="utf-8")
(ICI / "sec-cf.tex").write_text(CF, encoding="utf-8")
print(f"[v159] {len(FAITS)} remplacements ancrés :")
for f in FAITS:
    print(f"  - {f}")
