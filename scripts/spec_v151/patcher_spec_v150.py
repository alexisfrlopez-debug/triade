#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""patcher_spec_v150.py — les éditions de la chaîne spec_v150 (née de
spec_v140 par copie) : la version, le § 1.16, le § 19.17, l'annexe
D197/D198, le journal des versions. Chaque remplacement EST ANCRÉ —
REFUS si une ancre manque."""
import pathlib

ICI = pathlib.Path(__file__).resolve().parent
A = (ICI / "sec-a.tex").read_text(encoding="utf-8")
D = (ICI / "sec-d.tex").read_text(encoding="utf-8")
FAITS = []


def remplace(texte, ancien, nouveau, nom):
    if ancien not in texte:
        raise SystemExit(f"[spec_v150] ANCRE INTROUVABLE — {nom}")
    FAITS.append(nom)
    return texte.replace(ancien, nouveau, 1)


# ---- les versions --------------------------------------------------------
for f in ("cover.html", "main.tex", "merge_cover.py"):
    p = ICI / f
    t = p.read_text(encoding="utf-8")
    t = t.replace("v0.14.0", "v0.15.0").replace("Version 0.14.0",
                                                "Version 0.15.0")
    t = t.replace("le programme empirique",
                  "les preuves non bornées et le raffinement")
    p.write_text(t, encoding="utf-8")
FAITS.append("les versions (couverture, corps, fusion)")

# ---- sec-a : le § 1.16 NOUVEAU (avant la couche I) -----------------------
SEC116 = r"""\subsection{Ce que change la v0.15.0}\label{sec:nouveautes150}

LES PREUVES NON BORNÉES ET LE RAFFINEMENT (le sixième fichier
d'instructions, ic09ydeli sous son vrai nom — le croisement
d'attribution d'hier RECROUPÉ et CORRIGÉ, D197) : le modèle formel
généralisé, l'équivalence modèle--implémentation vérifiée, les statuts
de preuve systématiques. AUCUNE règle du cœur modifiée, AUCUNE couche
d'exécution ajoutée, AUCUN artefact scellé touché.

\textbf{LA DÉVIATION CONSTATÉE} : Tamarin ET ProVerif demeurent ABSENTS
du laboratoire (constat re-vérifié au geste à l'ouverture de l'édition)
— la route consignée à D196 est suivie : la preuve par INVARIANT
INDUCTIF dans l'explorateur.

\textbf{L'INVARIANT INDUCTIF} (\code{scripts/preuves\_v150/
modele\_invariant\_v150.py}) : le plafond d'époque de l'explorateur
v0.12.0 (un artefact d'exploration, jamais du design — l'implémentation
fait $e \leftarrow e+1$ sans borne) est RETIRÉ ; l'invariant $I$
(I$_1$ secret $\Rightarrow$ seuil $=3$ ; I$_2$ aucune destruction
injuste ; I$_3$ média du piège et fragments CF2 intacts ; I$_4$ époque
$\ge 1$) est initialisé à l'état initial, PRÉSERVÉ par chacune des 13
règles sur l'ensemble FINI des formes d'état (288 formes, les valeurs
contraintes par $I$ énumérées dans le domaine $I$, les deux classes
d'époque $\{1\}$ et $\{\ge 2\}$), l'uniformité de la classe $\ge 2$
témoignée mécaniquement par translations $\delta \in \{7, 50, 1000\}$
aux verdicts IDENTIQUES ; la monotonie de l'époque vérifiée
INCONDITIONNELLEMENT (4\,096 formes, zéro décroissance) ; le rejeu
retourne l'état inchangé. LES QUATRE PROPRIÉTÉS P1--P4 SONT PROUVÉES
NON BORNÉES (toute époque, toute profondeur, sous A1--A4 ; A5 hors
modèle nommé). La FIDÉLITÉ du portage : l'explorateur aux bornes et au
plafond historiques reproduit EXACTEMENT D187 (154 états, 1~152
transitions) ; les bornes étendues (époques $\le 5$ profondeur 8 :
228/1~902 ; époques $\le 7$ profondeur 12 : 372/3~342) trouvent ZÉRO
état atteignable hors de $I$ — la preuve bornée CONFIRME désormais la
preuve non bornée au lieu d'y suppléer.

\textbf{LE RAFFINEMENT} (\code{scripts/preuves\_v150/
raffinement\_v150.py}) : chaque règle abstraite REJOUÉE contre
l'implémentation Python (un coffre de TEST à phrase publique marquée,
D192 — le coffre réel n'est jamais ouvert par un test) : le cycle
honnête sur CINQ époques VÉCUES aux deux niveaux (la borne v0.12.0
dépassée), la phrase erronée aux deux actes (quinze essais, zéro
destruction), la falsification du conteneur (une destruction LOCALE,
un procès-verbal, le média intact), la falsification du piège (refus
nommé, rien détruit), le rejeu d'époque passée en TROIS variantes (le
miroir local, les époques croisées, le témoin hors-bande), le piège
absent (IMPOSSIBLE, pas refusé), le piège d'un autre coffre, et
l'adversaire sous le seuil (32 triplets de moitiés forgées, zéro
passage du verif) : \textbf{34 pas de raffinement, ZÉRO ÉCART} — les
chemins d'échec inclus ; trois gestes hors modèle consignés comme
tels.

\textbf{LES TROIS KITS DE MESURE MATÉRIELLE} : le dudect temps réel
(quatre cibles extraites de la pièce scellée, l'appel natif VALIDÉ au
vecteur FIPS « abc », le mesureur C double backend dont l'autotest
POSIX n'éprouve que le mécanisme), le \code{fence.i} sur silicium (le
scénario M7, la cible changée), le terrain tiers Loupe (T0$\to$T7+S0
intégral) — TOUS \emph{EN ATTENTE DE RUN MATÉRIEL} : aucun chiffre
n'existe, aucun n'est fabriqué.

\textbf{LA RÉPLICATION} : la grille T/X FINALISÉE (les cinq classes
terrain et trois laboratoire, définitions opérationnelles, exemples
vécus), le calculateur $\kappa$ de Cohen AUTOTESTÉ (trois cas
synthétiques au $\kappa$ calculable à la main), les critères
pré-enregistrés D189 INCHANGÉS ; le second annotateur À RECRUTER, le
second domaine EN ATTENTE d'une vraie commande — les statuts consignés.

\textbf{LES STATUTS SYSTÉMATIQUES} (la commande, point 4) : chaque
affiliation de preuve porte son statut — \emph{prouvé non borné} /
\emph{prouvé borné} / \emph{en attente de run matériel} — la table
générée depuis les pièces (\code{scripts/statuts\_preuves\_v150.py}),
AUCUNE revendication matérielle tant que le run n'est pas recoupé.

\textbf{LA DETTE DOCUMENTAIRE GUÉRIE} : la table des preuves du
manuscrit (29 lignes en v0.13.0/v0.14.0) n'était JAMAIS RENDUE — le
flot dépassait la page et \LaTeX{} le rejetait silencieusement (« Float
too large », le constat de l'édition) : la table devient LONGTABLE,
les 34 lignes sont rendues, toutes les éditions sont relues.

\textbf{LA GOUVERNANCE} (D197) : le croisement d'attribution des
instructions n°5/n°6 recoupé aux métadonnées Drive (les deux fichiers
déposés 11/11 13:21 UTC, jamais modifiés — ysddxpk0o porte le programme
v0.14.0 exécuté, ic09ydeli porte le programme v0.15.0 ouvert) et
corrigé aux gestes (ysddxpk0o archivé, ic09ydeli rappelé d'ARCHIVE
vers \code{/instructions} — l'instruction active sous son vrai nom) ;
LA RÈGLE DU CONTENU CITÉ (à l'ouverture de toute instruction : lecture
intégrale, empreinte confrontée, le contenu cité à l'entrée qui ouvre
l'exécution) ; LA RÈGLE DU DÉVELOPPEUR (12/11) : à chaque livraison
d'une nouvelle version d'un document, les anciennes versions sont
archivées (racine $\to$ \code{/ARCHIVE}, déplacement vérifié — la
racine du coffre ne porte que les versions courantes).

"""
A = remplace(
    A,
    "\\section{La couche I : format normalisé des "
    "spécifications}\\label{sec:coucheI}",
    SEC116 + "\\section{La couche I : format normalisé des "
    "spécifications}\\label{sec:coucheI}",
    "sec-a : le § 1.16")

# ---- sec-d : le § 19.17 ---------------------------------------------------
SEC1917 = r"""\subsection{Correspondance v0.14.0 $\to$ v0.15.0}\label{sec:evolutions150}

La v0.15.0 est L'ÉDITION DES PREUVES NON BORNÉES ET DU RAFFINEMENT
(l'instruction ic09ydeli — le croisement d'attribution recoupé, D197) :

\begin{table}[h]\centering\small
\begin{tabularx}{\textwidth}{@{}l X X l@{}}
\toprule
Évolution & En v0.14.0 & En v0.15.0 & Statut \\
\midrule
Le modèle formel & prouvé BORNÉ (époques $\le 3$, le plafond de
l'explorateur) & PROUVÉ NON BORNÉ (l'invariant inductif $I$, la
préservation par les 13 règles, la translation $\delta$) & livré \\
La fidélité du portage & — & D187 reproduit EXACTEMENT (154/1~152),
bornes étendues zéro hors $I$ & livré \\
Le raffinement & — & 34 pas rejoués contre l'implémentation, ZÉRO
ÉCART, les chemins d'échec inclus & livré \\
Les statuts de preuve & « prouvé dans le modèle » (borné, la nuance
dans le texte) & SYSTÉMATIQUES : prouvé non borné / prouvé borné / en
attente de run matériel & livré \\
La table des preuves du manuscrit & générée mais JAMAIS RENDUE (le
flot rejeté silencieusement — la dette constatée) & LONGTABLE : les 34
lignes rendues & guéri \\
Les kits matériels & le kit terrain du bras C (en attente) & TROIS kits
(dudect temps réel [l'appel natif validé FIPS], fence.i sur silicium,
terrain tiers) — EN ATTENTE & préparés \\
La réplication & la grille T/X proposée (D189) & la grille FINALISÉE
(définitions opérationnelles, exemples vécus), le $\kappa$ AUTOTESTÉ,
les critères INCHANGÉS, les statuts consignés & outillé \\
La gouvernance & — & le croisement d'attribution RECOUPÉ et CORRIGÉ
(D197), la règle du contenu cité, la règle d'archivage des versions &
consigné \\
\bottomrule
\end{tabularx}
\end{table}

Modifications explicitement rejetées (v0.15.0) : relâcher la moindre
hypothèse A1--A5 au bénéfice de la preuve non bornée — rejeté (la
généralisation porte sur l'ÉPOQUE, jamais sur le modèle symbolique) ;
consigner un résultat matériel d'après l'autotest POSIX du kit dudect —
rejeté (l'autotest éprouve le MÉCANISME, le run appartient au
développeur) ; réécrire les entrées d'hier au sujet du croisement —
rejeté (append-only : la correction vit dans l'Entrée 230 et D197, les
entrées fausses demeurent lisibles avec leur renvoi).

"""
D = remplace(
    D,
    "\\section{Journal des décisions}\\label{sec:decisions}",
    SEC1917 + "\\section{Journal des décisions}\\label{sec:decisions}",
    "sec-d : le § 19.17")

# ---- sec-d : l'annexe des décisions — D197/D198 après D195 ---------------
D198_LIGNE = (
    "D197 & Le croisement d'attribution recoupé et la règle du contenu "
    "cité & les métadonnées Drive font foi (les deux fichiers déposés "
    "11/11 13:21 UTC, jamais modifiés : ysddxpk0o porte le programme "
    "v0.14.0 exécuté, ic09ydeli porte le programme v0.15.0 ouvert — les "
    "étiquettes d'hier étaient croisées, les travaux intègres) ; la "
    "correction aux gestes (ysddxpk0o archivé, ic09ydeli rappelé vers "
    "\\code{/instructions}, empreintes md5 recoupées avant et après, "
    "aucune suppression) ; LA RÈGLE DU CONTENU CITÉ (lecture intégrale, "
    "empreinte confrontée, contenu cité à l'entrée d'ouverture) ; LA "
    "RÈGLE DU DÉVELOPPEUR 12/11 : les anciennes versions archivées à "
    "chaque livraison d'une nouvelle (première application : la "
    "v0.15.0). \\\\\n"
    "D198 & Les preuves non bornées et le raffinement livrés & "
    "l'invariant inductif $I$ (quatre propriétés PROUVÉES NON BORNÉES, "
    "la fidélité D187 reproduite exactement, les bornes étendues zéro "
    "hors $I$) ; le raffinement 34 pas zéro écart (les chemins d'échec "
    "inclus, cinq époques vécues aux deux niveaux) ; les trois kits "
    "matériels préparés EN ATTENTE (le dudect à l'appel natif validé "
    "FIPS, le fence.i silicium, le terrain tiers) ; la réplication "
    "outillée (grille finalisée, $\\kappa$ autotesté, critères "
    "inchangés) ; les statuts systématiques ; la dette de la table des "
    "preuves guérie (longtable). \\\\"
)
ancre_d195 = "le kit terrain EN ATTENTE. \\\\"
if ancre_d195 not in D:
    raise SystemExit("[spec_v150] ANCRE INTROUVABLE — la ligne D195")
D = D.replace(ancre_d195, ancre_d195 + "\n" + D198_LIGNE, 1)
FAITS.append("sec-d : l'annexe D197/D198")

# ---- sec-d : le journal des versions (le préambule historique) ------------
D = remplace(
    D,
    "pièces), D195 (les résultats : le bras de référence, la re-mesure RQ2,\n"
    "l'indépendance, le re-jeu des survivants).",
    "pièces), D195 (les résultats : le bras de référence, la re-mesure RQ2,\n"
    "l'indépendance, le re-jeu des survivants). La v0.15.0 consigne les\n"
    "preuves non bornées et le raffinement : D197 (le croisement\n"
    "d'attribution recoupé, la règle du contenu cité, la règle\n"
    "d'archivage des versions), D198 (l'invariant inductif, le\n"
    "raffinement, les kits, la réplication, les statuts systématiques).",
    "sec-d : le journal des versions")

(ICI / "sec-a.tex").write_text(A, encoding="utf-8")
(ICI / "sec-d.tex").write_text(D, encoding="utf-8")
print(f"[spec_v150] {len(FAITS)} éditions ancrées :")
for f in FAITS:
    print(f"  - {f}")
