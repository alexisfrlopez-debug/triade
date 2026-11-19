#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""patcher_spec_v154.py — l'édition v0.15.4 de la spécification (née de
spec_v153 par copie) : LE POINTEUR SEUL AU FORMAT DE RÉPONSE DE LOCALISER
(l'instruction cq01qv1za — UNE RÈGLE ADDITIVE, aucune règle existante
modifiée). Chaque remplacement EST ANCRÉ — REFUS si une ancre manque."""
import pathlib
import shutil

SRC = pathlib.Path(__file__).resolve().parents[1] / "spec_v153"
ICI = pathlib.Path(__file__).resolve().parent
shutil.copy2(SRC / "main.tex", ICI / "main.tex")
for f in SRC.glob("sec-*.tex"):
    shutil.copy2(f, ICI / f.name)
for f in ("chaine_cf.png",):
    if (SRC / f).exists():
        shutil.copy2(SRC / f, ICI / f)
FAITS = []


def remplace(texte, ancien, nouveau, nom):
    if ancien not in texte:
        raise SystemExit(f"[v154] ANCRE INTROUVABLE — {nom}")
    FAITS.append(nom)
    return texte.replace(ancien, nouveau, 1)


# ---- main.tex : l'en-tête, le fancyhead, le pdftitle ----------------------
M = (ICI / "main.tex").read_text(encoding="utf-8")
M = remplace(
    M,
    "%  PROTOCOLE TRIADE v0.15.3 — Manuscrit de spécification\n"
    "%  L'édition v0.15.3 est L'ALIGNEMENT DU MODÈLE SUR LA RÈGLE",
    "%  PROTOCOLE TRIADE v0.15.4 — Manuscrit de spécification\n"
    "%  L'édition v0.15.4 est LE POINTEUR SEUL (une règle ADDITIVE à\n"
    "%  l'opération localiser, l'instruction cq01qv1za — aucune règle\n"
    "%  existante modifiée). L'édition v0.15.3 est L'ALIGNEMENT DU MODÈLE "
    "SUR LA RÈGLE",
    "l'en-tête (v0.15.4)")
M = remplace(M, "spécification v0.15.3}", "spécification v0.15.4}",
             "le fancyhead (v0.15.4)")
M = remplace(M, "Protocole TRIADE v0.15.3 — spécification technique",
             "Protocole TRIADE v0.15.4 — spécification technique",
             "le pdftitle (v0.15.4)")
(ICI / "main.tex").write_text(M, encoding="utf-8")

# ---- sec-a.tex : la section « Ce que change » + la ligne du budget --------
A = (ICI / "sec-a.tex").read_text(encoding="utf-8")
A = remplace(
    A,
    "\\subsection{Ce que change la v0.15.3}\\label{sec:nouveautes153}",
    """\\subsection{Ce que change la v0.15.4}\\label{sec:nouveautes154}

LE POINTEUR SEUL (l'instruction cq01qv1za — la vague du 18/11, la
quatrième) : UNE RÈGLE ADDITIVE à l'opération \\emph{localiser}, aucune
règle existante modifiée, aucun artefact scellé touché. Le format de
réponse de localiser devient le \\textbf{pointeur seul} : l'agent rend
UNE ligne — l'identifiant de l'entrée de carte et l'empreinte
\\code{sha256} de la notation (deux champs LITTÉRAUX du matériau,
jamais un calcul — la leçon OPT-02 : le champ calculé est le champ
faussé). Le \\textbf{client expande} le pointeur auprès de la carte :
recherche de l'identifiant, confrontation de l'empreinte octet pour
octet, expansion de l'entête complet, confrontation au bloc soumis —
QUATRE refus nommés fail-closed (POINTEUR-INCONNU,
EMPREINTE-DIVERGENTE, EXPANSION-DIVERGENTE, HORS-FORMAT). La mesure
OPT-04 (la même graine que OPT-02, 18 appels réels au tokenizer natif,
le cl100k parallèle, la re-tokenisation indépendante à ±1 token) : le
total 1~714 → 1~103 natifs (−35,7~\\%), la réponse 770 → 52
(−93,3~\\%), zéro divergence 18/18, l'expansion client verte 18/18. Le
budget D31 (64 tokens à la première ligne) demeure : le pointeur le
tient avec marge. La décision D222 (append-only) consigne l'adoption.

\\subsection{Ce que change la v0.15.3}\\label{sec:nouveautes153}""",
    "la section nouveautés v0.15.4 (sec-a)")
A = remplace(
    A,
    "Localiser un bloc & frag-loc — une entrée & 64 tokens max (D31) \\\\",
    "Localiser un bloc & frag-loc — une entrée & 64 tokens max (D31) ; "
    "la réponse AU POINTEUR SEUL depuis la v0.15.4 (D222 : l'ID + "
    "l'empreinte, le client expande) \\\\",
    "la ligne du budget localiser (D222)")
(ICI / "sec-a.tex").write_text(A, encoding="utf-8")
print("[v154] les ancrages posés :", " ; ".join(FAITS))
