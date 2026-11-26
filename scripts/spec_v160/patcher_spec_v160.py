#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""patcher_spec_v160.py — la spécification v0.15.18 (née de v0.15.17 par copie) :
LA VAGUE 28 (W28IMRAD). (a) L'en-tête, le running header et le pdftitle portés
à v0.15.18. (b) La section de version v0.15.18 ajoutée (les résultats de la
vague 28 : le harnais à carte dérivée 229/235, le moteur généralisé 4,56 × C,
OPT-16 à 79,5 tokens, les classes C30/C31, le budget OPT-20, la restructuration
IMRAD du manuscrit). Chaque remplacement EST ANCRÉ."""
import pathlib
import shutil

ICI = pathlib.Path(__file__).resolve().parent
SRC = ICI.parent / "spec_v159"
for f in [SRC / "main.tex", *SRC.glob("sec-*.tex"), SRC / "chaine_cf.png"]:
    if f.exists():
        shutil.copy2(f, ICI / f.name)

M = (ICI / "main.tex").read_text(encoding="utf-8")
A = (ICI / "sec-a.tex").read_text(encoding="utf-8")
FAITS = []


def remplace(txt, ancien, nouveau, nom):
    if ancien not in txt:
        raise SystemExit(f"[v160] ANCRE INTROUVABLE — {nom}")
    if txt.count(ancien) != 1:
        raise SystemExit(f"[v160] ANCRE NON UNIQUE — {nom}")
    FAITS.append(nom)
    return txt.replace(ancien, nouveau)


# ---- l'en-tête et les versions (v0.15.18) -----------------------------------
M = remplace(M, "%  PROTOCOLE TRIADE v0.15.17 — Manuscrit de spécification",
             "%  PROTOCOLE TRIADE v0.15.18 — Manuscrit de spécification",
             "l'en-tête (v0.15.18)")
M = remplace(M, r"\fancyhead[L]{\small\itshape Protocole TRIADE — spécification v0.15.17}",
             r"\fancyhead[L]{\small\itshape Protocole TRIADE — spécification v0.15.18}",
             "le running header (v0.15.18)")
M = remplace(M, "pdftitle={Protocole TRIADE v0.15.17 — spécification technique}",
             "pdftitle={Protocole TRIADE v0.15.18 — spécification technique}",
             "le pdftitle (v0.15.18)")
for vieux, neuf in [
    ("La présente révision est la v0.15.17", "La présente révision est la v0.15.18"),
]:
    if vieux in M:
        M = remplace(M, vieux, neuf, "la révision courante")

# ---- la section de version v0.15.18 (ajoutée avant la couche I) -------------
NOUVELLE = r"""\subsection{Ce que change la v0.15.18}\label{sec:nouveautes1518}

La v0.15.18 porte la vague 28 (les objectifs poussés à leur maximum) : le manuscrit
de l'édition est restructuré en cœur IMRAD (le journal d'optimisation, les programmes
étendus, les notes post-édition et le changelog en annexes ; la décomposition quatre
bras hissée au cœur des résultats) ; le harnais à carte dérivée exécute 229/235
vecteurs d'oracle avec la carte mémoire dérivée mécaniquement de la carte C (le
voisinage des blocs porteurs à leurs RVA réelles, l'IAT aux adresses de l'image, les
globaux en pages zéro ; la console du jumeau ligne-identique 81/81 ; les six tls-06
refusés DEPASSEMENT — un arrêt au timeout n'est jamais un OK) ; le moteur natif
généralisé aux volumes complets (12 000 cas, régime chaud 4,56 × C contre le pilote
nu, la console différée ligne-identique, l'audit 1-sur-10 sans écart) ; l'opération
éditer par diff structuré tient la cible OPT-16 à 79,5 tokens natifs médians ; la
rejouabilité symétrique de la pièce T vit ses cinq sondes vertes ; le plan de vague
terrain groupée est pré-enregistré ; le registre des cibles porte CIB-VOL-REGIME et
CIB-HARNAIS-200 soldée à 229/235. Deux classes de linter couvrent les résidus
d'édition nouveaux : C30 N-VALUE (toute médiane publiée porte son n=) et
C31 CLAIM-SCOPE (toute revendication « first/only » porte son scope et sa source).
Le budget token par vague est mesuré et pré-enregistré (OPT-20 : la production de
la vague à 19 269 tokens natifs, le budget de la vague suivante). Aucune valeur
mesurée n'est modifiée.

"""
A = remplace(A, r"\section{La couche I : format normalisé des spécifications}\label{sec:coucheI}",
             NOUVELLE + r"\section{La couche I : format normalisé des spécifications}\label{sec:coucheI}",
             "la section de version v0.15.18")

(ICI / "main.tex").write_text(M, encoding="utf-8")
(ICI / "sec-a.tex").write_text(A, encoding="utf-8")
print(f"[v160] {len(FAITS)} remplacements ancrés :")
for f in FAITS:
    print(f"  - {f}")
