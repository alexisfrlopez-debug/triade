#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""patcher_spec_v140.py — les éditions de la chaîne spec_v140 (née de
spec_v130 par copie) : la version, le § 1.15, le § 19.16, l'annexe D195.
Chaque remplacement EST ANCRÉ — REFUS si une ancre manque."""
import pathlib

ICI = pathlib.Path(__file__).resolve().parent
A = (ICI / "sec-a.tex").read_text(encoding="utf-8")
D = (ICI / "sec-d.tex").read_text(encoding="utf-8")
FAITS = []


def remplace(texte, ancien, nouveau, nom):
    if ancien not in texte:
        raise SystemExit(f"[spec_v140] ANCRE INTROUVABLE — {nom}")
    FAITS.append(nom)
    return texte.replace(ancien, nouveau, 1)


# ---- les versions --------------------------------------------------------
for f in ("cover.html", "main.tex", "merge_cover.py"):
    p = ICI / f
    t = p.read_text(encoding="utf-8")
    t = t.replace("v0.13.0", "v0.14.0").replace("Version 0.13.0",
                                                "Version 0.14.0")
    t = t.replace("les corrections de l'édition",
                  "le programme empirique")
    p.write_text(t, encoding="utf-8")
FAITS.append("les versions (couverture, corps, fusion)")

# ---- sec-a : le § 1.15 NOUVEAU (avant la couche I) -----------------------
SEC115 = r"""\subsection{Ce que change la v0.14.0}\label{sec:nouveautes140}

LA RÉVISION DU PROGRAMME EMPIRIQUE (D193/D194/D195, le cinquième fichier
d'instructions) : le bras de référence compilateur PRÉ-ENREGISTRÉ, la
re-mesure RQ2, l'indépendance par instance isolée, le re-jeu des
survivants de mutation. AUCUNE règle du cœur modifiée, AUCUNE couche
d'exécution ajoutée, AUCUN artefact scellé touché.

\textbf{LE PRÉ-ENREGISTREMENT} (D193) : le plan de comparaison (les
hypothèses H1-H4, les critères CA1-CA5, la méthode, les six blocs, les
vecteurs) consigné AVANT toute mesure, son empreinte sha256 verrouillée —
toute modification postérieure du plan serait une fraude attrapable.

\textbf{LE BRAS DE RÉFÉRENCE} (D195) : SIX blocs de Loupe réimplémentés
EN C depuis les MÊMES CONTRATS (les cinq familles couvertes), compilés
gcc 14.2 -O2/-Os (clang absent, l'écart nommé), les primitives OS prises
par table de pointeurs aux MÊMES shims du mini-OS, AUTO-VÉRIFIÉS contre
les vecteurs dorés AVANT toute mesure (l'autotest a attrapé deux fautes
de table K au geste — la méthode appliquée à elle-même). LA MESURE :
ZÉRO DIVERGENCE aux vecteurs (la notation scellée et la référence
compilée sont observationnellement équivalentes aux contrats) ; les
instructions à travail égal : sha-256 PARITAIRE (9~089 contre 9~146 —
l'héritage PAR LA CARTE), la lecture paritaire (48/47), les blocs purs
plus chers à la notation (641/477, 193/69, 39/16), la cascade saine
102~176/75~560 (l'adaptation du panneau nommée : le camp C calcule la
moitié sha seulement) ; les tailles MIXTES ; la mutation aux mêmes
tirages : la notation testable au MÊME DEGRÉ (H4 tenue), le camp compilé
plus fragile aux mutants d'appels OS (16/16 par le tueur de séquence).

\textbf{LA RE-MESURE RQ2} (D195) : les budgets de bout en bout sur la
carte de l'ère Loupe, distributions complètes (n=10/opération,
cl100k\_base) : localiser 580 [496..706], éditer 2~143 [1~085..3~463],
ajouter 3~510 [3~128..4~091], la baseline naive 300~304 tokens (le
désassemblage complet) — les valeurs M1 (51/719/1~088) HISTORIQUES,
jamais remplacées ; LA LECTURE DÉFAVORABLE AU PROTOCOLE consignée telle
quelle (les opérations coûtent 4-11$\times$ leur M1 : les notations plus
longues, les contrats plus denses) ; le raisonnement ESTIMÉ
($\times$1,08, le rapport génération/contenu des retouches réelles —
l'estimation nommée, jamais une mesure).

\textbf{L'INDÉPENDANCE} (D195) : l'oracle régénéré par une instance
isolée (un contexte neuf, la dérivation depuis les définitions
mathématiques) — ZÉRO DIVERGENCE sur les 128 constantes ; L'ÉCART NOMMÉ :
l'infrastructure d'agents du labo n'expose QU'UNE famille — l'indépendance
inter-familles DEMEURE ouverte ; la voie alternative (la racine cubique
entière exacte) confirme indépendamment.

\textbf{LE RE-JEU DES SURVIVANTS} (D195) : les 832 mutants de v0.11.0
re-jeués aux MÊMES tirages avec les tueurs de COMPOSITION (la boucle
winmain complète pour loupe, la composition de la poignée +
l'enregistrement pour l'orchestration tls13, le harnais autonome pour
sys) : 776/832 tués (93,3 \% — contre 83,4 \%), tls13 et sys à
100 \%, les 56 survivants loupe NOMMÉS (les chemins hors scénario).

\textbf{LE KIT TERRAIN} (\code{scripts/kit\_terrain\_bras\_c/} : les
binaires -O2/-Os + la source + le LISEZMOI) : EN ATTENTE DU RUN TERRAIN —
les runs appartiennent au développeur, le labo ne fabrique JAMAIS un
résultat.

\section{La couche I : format normalisé des spécifications}\label{sec:coucheI}"""
A = remplace(A, "\\section{La couche I : format normalisé des "
                "spécifications}\\label{sec:coucheI}", SEC115,
             "le § 1.15")

# ---- sec-d : le § 19.16 + l'annexe D195 ----------------------------------
SEC1916 = r"""\subsection{Correspondance v0.13.0 $\to$ v0.14.0}\label{sec:evolutions140}

La v0.14.0 est LA RÉVISION DU PROGRAMME EMPIRIQUE (D193/D194/D195) :
aucune règle modifiée, aucune couche d'exécution ajoutée, hiérarchie
inchangée — les AFFIRMATIONS du manuscrit passent aux MESURES contrôlées.

\begin{table}[tbp]
\centering
\small
\begin{tabularx}{\textwidth}{>{\raggedright\arraybackslash}p{3.4cm} X}
\textbf{Évolution} & \textbf{Le fait consigné (v0.14.0)} \\
\midrule
LE PRÉ-ENREGISTREMENT & le plan consigné AVANT toute mesure (D193,
l'empreinte verrouillée, les critères CA1-CA5 — la fraude post-mesure
attrapable). \\
LE BRAS DE RÉFÉRENCE & six blocs C depuis les mêmes contrats, les mêmes
shims, auto-vérifiés : ZÉRO DIVERGENCE aux vecteurs ; sha-256 PARITAIRE
à travail égal (9~089/9~146), les purs plus chers à la notation, la
mutation au même degré (H4) ; les résultats rapportés TELS QUELS,
y compris défavorables (D195). \\
LA RE-MESURE RQ2 & les distributions de bout en bout (580/2~143/3~510 de
médiane, la baseline naive 300~304, le raisonnement estimé NOMMÉ) — les
valeurs M1 historiques, la lecture défavorable consignée. \\
L'INDÉPENDANCE & l'instance isolée : zéro divergence sur 128 constantes ;
l'écart de famille nommé (une seule famille au labo) ; la voie entière
exacte en confirmation. \\
LES SURVIVANTS & le re-jeu des 832 aux composition-killers : 93,3 \%
(tls13/sys à 100 \%), les 56 loupe nommés (D195). \\
LE KIT TERRAIN & préparé, EN ATTENTE du geste du développeur (jamais un
résultat fabriqué). \\
\end{tabularx}
\end{table}

Modifications explicitement rejetées (v0.14.0) : mesurer sans le
pré-enregistrement — rejeté (la fraude que CA5 interdit) ; remplacer les
valeurs M1 par les nouvelles — rejeté (les mesures historiques demeurent,
les deux ères coexistent au rapport) ; extrapoler le raisonnement de
l'agent à la mesure — rejeté (l'estimation $\times$1,08 est NOMMÉE
estimation, jamais confondue).

\section{Journal des décisions}\label{sec:decisions}"""
D = remplace(D, "\\section{Journal des décisions}\\label{sec:decisions}",
             SEC1916, "le § 19.16")

# (la rangée D195 fut insérée directement à sec-d.tex — l'échappement multi-niveaux perdit, le geste simple gagna)


# la narration des versions
D = remplace(
    D, "D192 (la conséquence D81 au modèle de menace, le kit D183 préparé sans\nl'appliquer, l'état de l'art étendu).",
    "D192 (la conséquence D81 au modèle de menace, le kit D183 préparé sans\nl'appliquer, l'état de l'art étendu). La v0.14.0 consigne le programme\nempirique : D193 (le pré-enregistrement), D194 (l'état des mesures sur\npièces), D195 (les résultats : le bras de référence, la re-mesure RQ2,\nl'indépendance, le re-jeu des survivants).",
    "la narration v0.14.0")

(ICI / "sec-a.tex").write_text(A, encoding="utf-8")
(ICI / "sec-d.tex").write_text(D, encoding="utf-8")
print(f"[spec_v140] {len(FAITS)} remplacements ancrés :")
for f in FAITS:
    print("  -", f)
