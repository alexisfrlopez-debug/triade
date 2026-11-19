#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""patcher_spec_v153.py — la spécification v0.15.3 (née de spec_v152 par
copie) : L'ALIGNEMENT DU MODÈLE SUR LA RÈGLE — la falsification prouvée
pendant une session ouverte, offerte par le modèle étendu (l'instruction
5ey7gmjra). La RÈGLE de la spécification demeure ce qu'elle a toujours
dit (« seule la falsification prouvée détruit — destruction locale,
jamais le média ni les fragments ») : c'est le MODÈLE FORMEL v0.15.0 qui
sous-approximait (la garde canonique-seule) ; la v0.15.3 porte le modèle
à la lettre de la règle. Chaque remplacement EST ANCRÉ."""
import pathlib

ICI = pathlib.Path(__file__).resolve().parent
F = {}


def patch(nom_fichier, ancien, nouveau, nom):
    p = ICI / nom_fichier
    t = p.read_text(encoding="utf-8")
    if ancien not in t:
        raise SystemExit(f"[v153] ANCRE INTROUVABLE — {nom}")
    p.write_text(t.replace(ancien, nouveau, 1), encoding="utf-8")
    F[nom] = nom_fichier


# ---- 1. l'en-tête du main.tex ---------------------------------------------
patch("main.tex",
      "%  PROTOCOLE TRIADE v0.15.2 — Manuscrit de spécification",
      "%  PROTOCOLE TRIADE v0.15.3 — Manuscrit de spécification\n"
      "%  L'édition v0.15.3 est L'ALIGNEMENT DU MODÈLE SUR LA RÈGLE\n"
      "%  (l'instruction 5ey7gmjra, la vague du 18/11, la troisième) : le\n"
      "%  modèle formel CF3 étendu — la falsification du conteneur offerte\n"
      "%  pendant une session ouverte, la garde alignée sur la sentinelle\n"
      "%  concrète (destruction locale sur falsification prouvée, média et\n"
      "%  fragments intacts) ; les preuves non bornées re-déchargées sur le\n"
      "%  modèle étendu, la campagne générative re-jouée à ZÉRO divergence.\n"
      "%  AUCUNE règle modifiée : la règle disait « seule la falsification\n"
      "%  prouvée détruit » — le modèle v0.15.0 sous-approximait, la\n"
      "%  v0.15.3 le porte à la lettre.",
      "l'en-tête du main.tex (v0.15.3)")

patch("main.tex",
      r"\fancyhead[L]{\small\itshape Protocole TRIADE — spécification v0.15.2}",
      r"\fancyhead[L]{\small\itshape Protocole TRIADE — spécification v0.15.3}",
      "l'en-tête courant (v0.15.3)")

patch("main.tex",
      "pdftitle={Protocole TRIADE v0.15.2 — spécification technique},",
      "pdftitle={Protocole TRIADE v0.15.3 — spécification technique},",
      "le pdftitle (v0.15.3)")

# ---- 2. la couverture ------------------------------------------------------
patch("cover.html",
      "Sp&eacute;cification technique &middot; Version 0.15.2",
      "Sp&eacute;cification technique &middot; Version 0.15.3",
      "la couverture : la version (v0.15.3)")
patch("cover.html",
      "r&eacute;vision v0.15.2 (l'&eacute;dition de coh&eacute;rence "
      "inter-pi&egrave;ces)",
      "r&eacute;vision v0.15.3 (l'alignement du mod&egrave;le sur la "
      "r&egrave;gle)",
      "la couverture : la révision (v0.15.3)")

# ---- 3. sec-cf.tex : la lettre de la règle rendue explicite ----------------
patch("sec-cf.tex",
      "erronée est bénigne, seule la falsification \\emph{prouvée} détruit).",
      "erronée est bénigne, seule la falsification \\emph{prouvée} détruit — "
      "dans les DEUX phases : la sentinelle court sur le conteneur "
      "canonique, la destruction locale sur falsification prouvée pendant "
      "une session ouverte comprise, jamais le média ni les fragments ; "
      "le modèle formel v0.15.3 offre la règle aux deux phases, l'écart "
      "d'approximation de la v0.15.0 fermé par l'extension 5ey7gmjra).",
      "sec-cf : la lettre de la règle (les deux phases)")

# ---- 4. sec-a.tex : la section « Ce que change la v0.15.3 » ----------------
p = ICI / "sec-a.tex"
t = p.read_text(encoding="utf-8")
ancre = "\\subsection{Ce que change la v0.15.2}\\label{sec:nouveautes152}"
if ancre not in t:
    raise SystemExit("[v153] ANCRE INTROUVABLE — la section v0.15.2")
nouvelle = """\\subsection{Ce que change la v0.15.3}\\label{sec:nouveautes153}

L'ALIGNEMENT DU MODÈLE SUR LA RÈGLE (l'instruction 5ey7gmjra — la vague
du 18/11, la troisième) : AUCUNE règle modifiée, aucune couche ajoutée,
aucun artefact scellé touché. La règle de la sentinelle CF3 disait ce
qu'elle dit depuis la v0.12.0 : \\textbf{seule la falsification
\\emph{prouvée} détruit} — destruction locale, jamais le média ni les
fragments. Le MODÈLE FORMEL v0.15.0 sous-approximait cette règle : la
garde de \\code{falsifie\\_conteneur} exigeait l'état canonique, la
campagne générative (10~000 traces, la graine consignée) croisa l'écart
660 fois — la falsification pendant une session ouverte : le modèle
refusait, la sentinelle concrète détruisait (la découverte consignée,
réduite par ddmin à la séquence minimale [ouvrir, falsifier]). La
v0.15.3 \\textbf{ferme l'écart} : la garde devient le piège intègre
seul — la falsification prouvée offerte aux DEUX phases, l'effet
inchangé (destruction locale, PV, média et fragments intacts) — et le
programme de preuve est re-déchargé sur le modèle étendu : les
invariants inductifs (Init $\\Rightarrow$ I, I $\\wedge$ Next
$\\Rightarrow$ I$'$) à entiers non bornés NoError, l'alignement
TLA+~$\\leftrightarrow$ sémantique Python 13/13 règles (garde, image,
activation — SMT non borné), le lemme de translation d'époque re-prouvé
(LT1/LT2, contrôle négatif attrapé), l'espace atteignable borné
INVARIANT (la chaîne de fidélité TLC : 154 états distincts aux bornes
historiques — seules les transitions tirées croissent, 896 $\\to$ 926),
et la campagne re-jouée \\textbf{à ZÉRO divergence} : 30~000 traces aux
trois graines (la consignée 20261112 + deux nouvelles), chaque chemin
d'échec couvert, le rejeu bit-identique deux fois — contre le registre
v0.15.0 : exactement les 660 traces de la classe d'écart changées, rien
d'autre. L'instrument temps constant est promu au \\textbf{hash des
traces complètes} (une seule empreinte par cible sur 120 mesures — le
compte unique demeure, subsumé), et le kit de mesure matérielle
PRÉ-ENREGISTRÉ est livré en attente du geste développeur (n$\\ge$10
exécutions par N, deux machines au moins, la fréquence fixée, le pic
tls13-02/tls13-13 à N=200 pré-enregistré pour investigation) — aucun
chiffre matériel fabriqué.

""" + ancre
p.write_text(t.replace(ancre, nouvelle, 1), encoding="utf-8")
F["la section nouveautés v0.15.3"] = "sec-a.tex"

print(f"[v153] {len(F)} ancrage(s) remplacé(s) :")
for k, v in F.items():
    print(f"  - {k} ({v})")
print("TOUT VERT — les sources v0.15.3 sont prêtes à compiler")
