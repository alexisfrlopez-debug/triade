#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""patcher_spec_v130.py — LES CORRECTIONS CHIRURGICALES de la chaîne spec_v130
(née de spec_v120 par copie) : l'édition v0.13.0, la commande f3q3x9i7n
(point 1 « Spécification » + les corrections statistiques/neutralité
portées AU document normatif). Chaque remplacement EST ANCRÉ : le script
REFUSE si une ancre manque (jamais une retouche silencieuse)."""
import pathlib

ICI = pathlib.Path(__file__).resolve().parent
A = (ICI / "sec-a.tex").read_text(encoding="utf-8")
D = (ICI / "sec-d.tex").read_text(encoding="utf-8")
REMPLACEMENTS = []


def remplace(texte, ancien, nouveau, nom):
    global _
    if ancien not in texte:
        raise SystemExit(f"[spec_v130] ANCRE INTROUVABLE — {nom}")
    REMPLACEMENTS.append(nom)
    return texte.replace(ancien, nouveau, 1)


# ---- sec-a.tex : le paragraphe de consolidation ALIGNÉ sur D181 ----------
A = remplace(
    A,
    "au coffre \\code{/test} (M10-(d)) — ET ONZE RUNS TERRAIN (M10-(e), Entrées 202–219) :\n"
    "ONZE DÉFAUTS NOMMÉS, ONZE RETOUCHES DOCUMENTÉES — les refus du chargeur",
    "au coffre \\code{/test} (M10-(d)) — ET DOUZE RUNS TERRAIN (M10-(e), Entrées 202–222) :\n"
    "ONZE DÉFAUTS NOMMÉS SUR ONZE RUNS FAUTIFS (le douzième vert de bout en bout —\n"
    "le résidu [T0-PÉRIMÉ] divulgué, non compté : une bannière de texte, aucune\n"
    "porte touchée), ONZE RETOUCHES DOCUMENTÉES — les refus du chargeur",
    "A1 douze runs")

A = remplace(
    A,
    "0 OCTET AILLEURS — le code BYTE-IDENTIQUE au vécu des onze runs (R4 : le contrat",
    "0 OCTET AILLEURS — le code BYTE-IDENTIQUE au vécu des douze runs (R4 : le contrat",
    "A2 douze runs (byte-identique)")

A = remplace(
    A,
    "ARMÉ) — LE DOUZIÈME RUN ATTENDU : si le vert tient (le scénario ENTIER\n"
    "T0 $\\to$ S0 $\\to$ LA LIAISON ET la vitrine vivante), LA BALISE\n"
    "\\code{loupe 0.1.1} SCELLÉE sur run terrain recoupé (le miroir D165/D170 : la porte\n"
    "est de processus).",
    "ARMÉ) — LE DOUZIÈME RUN VÉCU ET RECOUPÉ 39/39 (l'Entrée 222 : T0$\\to$T7 tout\n"
    "vert pour la cinquième fois, la cascade 205 vécue pour la deuxième, la vitrine\n"
    "vivante la troisième — 0 et 0, aucune porte touchée) : LA BALISE\n"
    "\\code{loupe 0.1.1} SCELLÉE PAR FAIT DE CARTE sur run terrain recoupé (D181 :\n"
    "la dette [R10-PÉRIMÉE] soldée à la naissance, la cristallisation 26 × 10/10,\n"
    "l'anti-rollback armé — \\code{loupe.exe} INTACT \\code{c1115105…}, LE MÊME\n"
    "binaire que le douzième run a couru).",
    "A3 le douzième run vécu")

# ---- sec-a.tex : le renvoi manuscrit § 3.5 --------------------------------
A = remplace(
    A,
    "la section Results étendue (le § 4.5 du\nmanuscrit",
    "la section Results étendue (le § 3.5 du\nmanuscrit",
    "A4 renvoi § 3.5")

# ---- sec-a.tex : la cristallisation CORRIGÉE (§ 1.13, D190) --------------
A = remplace(
    A,
    "\\textbf{LA CRISTALLISATION ÉVALUÉE} (D189) : le seuil de 10 rebuilds\n"
    "analysé comme test séquentiel (SPRT de Wald : q₀ = 1 \\% contre q₁ = 50 \\%\n"
    "— 5 rebuilds identiques atteignent α = 5 \\%, le seuil historique 10\n"
    "atteint α = 1,08 × 10\\textsuperscript{−3}, 46× plus strict que le\n"
    "canonique) ; LE SEUIL DEMEURE 10",
    "\\textbf{LA CRISTALLISATION ÉVALUÉE} (D189, CORRIGÉE par D190) : les\n"
    "caractéristiques opérationnelles de la règle réelle (sceller ssi $n$\n"
    "rebuilds consécutifs identiques) : P(sceller$|q$) = $(1-q)^n$ — à\n"
    "$q = 50$\\,\\% : 3,1 \\% ($n{=}5$), 0,098 \\% ($n{=}10$), soit 32× plus\n"
    "strict (les quantiles unilatéraux exacts 1,87σ/3,10σ) ; à $q = 1$\\,\\% :\n"
    "la règle scelle un build sain avec probabilité 95,1 \\%/90,4 \\% — les\n"
    "valeurs « α = 3,29·10\\textsuperscript{−2} / 1,08·10\\textsuperscript{−3} »\n"
    "de D189 étaient des RAPPORTS DE VRAISEMBLANCE $(0,5/0,99)^n$ mal\n"
    "étiquetés (la correction D190) ; LE SEUIL DEMEURE 10",
    "A5 cristallisation corrigée")

# ---- sec-a.tex : le renvoi manuscrit § 4.1 --------------------------------
A = remplace(
    A,
    "la section § 4.6 (le modèle formel et",
    "la section § 4.1 (le modèle formel et",
    "A6 renvoi § 4.1")

# ---- sec-a.tex : le § 1.14 NOUVEAU ----------------------------------------
SEC114 = r"""\subsection{Ce que change la v0.13.0}\label{sec:nouveautes130}

LA RÉVISION DES CORRECTIONS DE L'ÉDITION (D190/D191/D192) — la commande du
développeur : une liste exhaustive d'incohérences vérifiées une par une, des
statistiques reformulées, la neutralité documentaire, un benchmark audité, un
état de l'art étendu. AUCUNE règle du cœur modifiée, AUCUNE couche d'exécution
ajoutée, AUCUN artefact scellé touché — l'édition CORRIGE les documents, elle
ne légifère pas (le modèle D180/D182).

\textbf{LES INCOHÉRENCES CORRIGÉES} (la liste de la commande, vérifiée une à
une) : les quatorze arbres signés (la cohérence avec le garde 14/14) ; la
référence au manuscrit accompagnant portée v0.13.0 ; le compte de lignes du
journal UNIFIÉ en valeur exacte extraite (les macros générées par le script
d'extraction — jamais un arrondi) ; « Fig.~5 » devient « Table 5 » ; la Data
Availability portée aux archives v0.13.0 ; la Table 6 des preuves RÉGÉNÉRÉE
intégralement en anglais par le générateur ANTI-TRONCATURE (les cellules ne
sont jamais coupées, chaque ligne est PARSÉE depuis les sorties brutes des
instruments) ; la note TOTAL/brouillons au tableau des budgets ($8\,774 +
5\,099 = 13\,873$, les brouillons exclus) ; le paragraphe de consolidation
du § 1.10 ALIGNÉ sur D181 (douze runs, la balise \code{loupe 0.1.1} scellée) ;
le tableau de menaces : « le code volé est inexploitable » devient
« l'évolution du code volé est bloquée, son exécution ne l'est pas » ; les
renvois au manuscrit recalés (§ 3.5 les preuves renforcées, § 4.1 le modèle
formel).

\textbf{LES STATISTIQUES REFORMULÉES} (D190) : la cristallisation — les
caractéristiques opérationnelles P(sceller$|q$) = $(1-q)^n$ remplacent les
« α » de D189 (des rapports de vraisemblance mal étiquetés) ; les conversions
sigma $\sqrt{-2\ln p}$ remplacées par les quantiles normaux unilatéraux
exacts (1,87σ/3,10σ) ; l'IC95~\% EXACT de 11/12 (Clopper-Pearson
$[0,615 ; 0,998]$, avec la réserve de non-indépendance des itérations
séquentielles) ; la règle de comptage opérationnelle des défauts échappés
DÉFINIE en méthodes du manuscrit (les runs 6/7 à deux défauts comptés une
fois chacun ; le résidu [T0-PÉRIMÉ] du run 12 divulgué, non compté — et
pourquoi).

\textbf{LA NEUTRALITÉ DOCUMENTAIRE} (D190) : l'anti-debug léger par mesure
de temps DOCUMENTÉ HONNÊTEMENT dans les deux documents (la portée : la
dissuasion, jamais la résistance — le résiduel « assumé » du tableau des
menaces demeure) ; la conséquence de D81 AJOUTÉE au modèle de menace (la
phrase de contrôle au dépôt + S\_serrure en en-tête clair = deux éléments
trivialement disponibles ; la confidentialité effective repose sur le seul
média piège) ; la frontière D105/D81 pour le clone du laboratoire (les tests
du labo tournent sur des clones temporaires à phrases de test visiblement
marquées — le conteneur réel jamais ouvert par un test) ; LE KIT DE LA
CÉRÉMONIE D183 PRÉPARÉ SANS L'APPLIQUER (\code{scripts/kit\_ceremonie\_d183/} :
l'outil au partage CF2 D120 TEL QUEL, l'autotest VERT sur phrase de test
publique — les 10 combinaisons de 3 parts exactes, les 10 paires sous le
seuil sans fuite —, le LISEZMOI pas à pas, le manifeste et les listes de
contrôle ; le geste appartient au développeur).

\textbf{LE BENCHMARK AUDITÉ} (D191) : le facteur « 15,3× » de v0.11.0
RETIRÉ — un ARTEFACT DE PÉRIMÈTRE (l'instrument lisait le compteur de la
FINALISATION SEULE après le retour du pipeline, comparé à l'opération
COMPLÈTE de la référence ; 4,16 instructions/ronde était le signe — sous
tout minimum scalaire plausible) ; les chiffres corrigés : l'opération
complète des blocs 75\,983 instructions contre 69\,132 (gcc~14.2 -O2) et
77\,505 (-Os), dans le même émulateur sur la même entrée, le condensé
vérifié AVANT le comptage et les 17 invocations de compression confirmées
mécaniquement — la notation WYSIWYG est COMPÉTITIVE ($-9$~\%/$+2$~\% en
instructions), plus compacte que -O2 (1\,021 contre 1\,482 octets, tables
comprises), moins que -Os (548) ; AUCUNE extension ISA au-delà du baseline
des deux côtés (gcc emploie des mouvements SSE2 du baseline que la notation
GPR pure n'emploie pas — l'écart rapporté sans ajustement) ; le terrain M7
REQUALIFIÉ (qemu-riscv64 TCG au noyau réel, la réserve instrumentale D149
nommée — la sémantique matérielle I-cache de \code{fence.i} NON prouvée sur
silicium, jamais revendiquée).

\textbf{L'ÉTAT DE L'ART ÉTENDU} (D192) : LLM Compiler (Meta 2024), CompCert
(Leroy 2009), Kitsune (2012) et POLUS (2007) pour la mise à jour dynamique,
SWE-agent (2024), la lignée sim-to-real (Jakobi 1995, Peng 2018) et le
hardware-in-the-loop (Bacic 2005) — chaque référence vérifiée DOI/arXiv ;
la revendication « first quantified account » SCOPÉE (le niveau notation
scellée sous gouvernance à intention signée) ; RQ3 RECADRÉE : la
quantification des GARANTIES SILENCIEUSES DU COMPILATEUR (ce que le
compilateur fournit gratuitement et que la notation à la main doit
re-dériver, leçon nommée par leçon).

\section{La couche I : format normalisé des spécifications}\label{sec:coucheI}"""
A = remplace(
    A,
    "\\section{La couche I : format normalisé des spécifications}\\label{sec:coucheI}",
    SEC114,
    "A7 § 1.14")

# ---- sec-d.tex : la phrase du tableau de menaces ---------------------------
D = remplace(
    D,
    "le code volé est inexploitable et ne peut pas évoluer ; l'axe 1 (TEE) reste une",
    "l'évolution du code volé est bloquée, son exécution ne l'est pas ; l'axe 1 (TEE) reste une",
    "D1 menace/exécution")

# ---- sec-d.tex : la rangée cristallisation du tableau des évolutions ------
D = remplace(
    D,
    "LA CRISTALLISATION & le seuil 10 justifié par le SPRT (α = 1,08 ×\n"
    "10\\textsuperscript{−3}, 46× plus strict) ; le seuil DEMEURE ; le",
    "LA CRISTALLISATION & le seuil 10 justifié par les caractéristiques\n"
    "opérationnelles P(sceller$|q$) = $(1-q)^n$ (à $q = 50$~\\% : 3,1~\\%\n"
    "à $n{=}5$, 0,098~\\% à $n{=}10$ — 32× plus strict ; les quantiles\n"
    "unilatéraux 1,87σ/3,10σ ; D190 corrige l'étiquetage en α des rapports\n"
    "de vraisemblance de D189) ; le seuil DEMEURE ; le",
    "D2 rangée cristallisation")

# ---- sec-d.tex : la limite assumée anti-debug + D190 -----------------------
D = remplace(
    D,
    "L'anti-debug reste léger et assumé.",
    "L'anti-debug reste léger et assumé — la portée documentée honnêtement dans\n"
    "les deux documents (l'arbitrage D190) : la dissuasion, jamais la résistance.",
    "D3 anti-debug D190")

# ---- sec-d.tex : la rangée D189 de l'annexe + D190/D191/D192 ---------------
D = remplace(
    D,
    "Cohen ≥ 0,61 ; les critères pré-enregistrés) — PROPOSÉ, jamais exécuté. \\\\",
    "Cohen ≥ 0,61 ; les critères pré-enregistrés) — PROPOSÉ, jamais exécuté ;\n"
    "l'étiquetage « α » des rapports de vraisemblance CORRIGÉ par D190. \\\\\n"
    "D190 & Les corrections de l'édition v0.13.0 & la liste exhaustive "
    "vérifiée une à une (quatorze arbres, comptes exacts du journal en macros, "
    "Table 6 régénérée par le générateur anti-troncature, la note "
    "TOTAL/brouillons, le paragraphe de consolidation aligné sur D181, la "
    "phrase du tableau de menaces, les renvois recalés) ; les statistiques "
    "reformulées (P(sceller$|q$) = $(1-q)^n$, quantiles 1,87σ/3,10σ, IC95 "
    "exact de 11/12 avec la réserve de non-indépendance, la règle de comptage "
    "opérationnelle) ; la neutralité documentaire (l'anti-debug documenté "
    "honnêtement, le terrain M7 requalifié — qemu TCG, fence.i non prouvé sur "
    "silicium). \\\\\n"
    "D191 & Le benchmark audité : le facteur 15,3× RETIRÉ & l'artefact de "
    "périmètre nommé (le compteur de la finalisation seule lu après le "
    "pipeline, comparé à l'opération complète de la référence — 4,16 "
    "instructions/ronde, le signe) ; les chiffres corrigés sur pièces : "
    "l'opération complète 75\\,983 instructions contre 69\\,132 (-O2) et "
    "77\\,505 (-Os), condensé vérifié avant comptage, 17 compressions "
    "confirmées, aucune extension ISA au-delà du baseline — la notation "
    "COMPÉTITIVE, jamais spectaculaire : la méthode appliquée à sa propre "
    "revendication. \\\\\n"
    "D192 & La conséquence D81 au modèle de menace et le kit D183 préparé & "
    "phrase au dépôt + S\\_serrure en en-tête clair = deux éléments "
    "trivialement disponibles, la confidentialité effective repose sur le "
    "seul média piège ; la frontière D105/D81 du clone du laboratoire "
    "(clones temporaires à phrases de test) ; le kit de cérémonie "
    "PRÉPARÉ SANS L'APPLIQUER (l'outil au partage CF2 D120, l'autotest "
    "VERT, le LISEZMOI, les listes de contrôle — le geste au développeur) ; "
    "l'état de l'art étendu (huit références vérifiées DOI/arXiv, la "
    "revendication scopée, RQ3 recadrée en garanties silencieuses du "
    "compilateur). \\\\",
    "D4 annexe D190-D192")

# ---- sec-d.tex : le § 19.15 NOUVEAU ----------------------------------------
SEC1915 = r"""\subsection{Correspondance v0.12.0 $\to$ v0.13.0}\label{sec:evolutions130}

La v0.13.0 est LA RÉVISION DES CORRECTIONS DE L'ÉDITION (D190/D191/D192) :
aucune règle modifiée, aucune couche d'exécution ajoutée, hiérarchie
inchangée — les documents deviennent cohérents avec leurs propres données.

\begin{table}[tbp]
\centering
\small
\begin{tabularx}{\textwidth}{>{\raggedright\arraybackslash}p{3.4cm} X}
\textbf{Évolution} & \textbf{Le fait consigné (v0.13.0)} \\
\midrule
LES INCOHÉRENCES & la liste de la commande vérifiée UNE À UNE (le rapport
de conformité joint aux livrables) : quatorze arbres signés, la référence au
manuscrit v0.13.0, les comptes exacts du journal en macros générées,
« Fig.~5 » $\to$ « Table 5 », la Data Availability v0.13.0, la Table 6
régénérée en anglais par le générateur anti-troncature, la note
TOTAL/brouillons, le § 1.10 aligné sur D181 (douze runs, loupe 0.1.1
scellée), la phrase du tableau de menaces, les renvois recalés (§ 3.5/§ 4.1)
(D190). \\
LES STATISTIQUES & la cristallisation aux caractéristiques opérationnelles
P(sceller$|q$) = $(1-q)^n$ (3,1~\%/0,098~\% à $q = 50$~\%, 32×, les
quantiles 1,87σ/3,10σ) ; l'IC95 exact de 11/12 ($[0,615 ; 0,998]$, la
réserve de non-indépendance) ; la règle de comptage opérationnelle des
défauts échappés (D190). \\
LE BENCHMARK & le facteur 15,3× RETIRÉ (l'artefact de périmètre : la
finalisation seule contre l'opération complète) ; les chiffres corrigés
75\,983 contre 69\,132/-Os 77\,505, la parité d'extensions ISA au baseline
constatée, le M7 requalifié (qemu TCG, fence.i non prouvé sur silicium)
(D191). \\
LA NEUTRALITÉ & l'anti-debug documenté honnêtement dans les deux documents ;
la conséquence D81 au modèle de menace (deux éléments trivialement
disponibles, le média piège seul rempart de confidentialité) ; la frontière
D105/D81 du clone ; le kit de cérémonie D183 PRÉPARÉ sans l'appliquer
(autotest VERT, LISEZMOI, manifeste) (D192). \\
L'ÉTAT DE L'ART & huit références vérifiées DOI/arXiv (LLM Compiler,
CompCert, Kitsune, POLUS, SWE-agent, Jakobi, Peng, Bacic) ; la revendication
« first quantified account » scopée ; RQ3 recadrée en garanties
silencieuses du compilateur (D192). \\
\end{tabularx}
\end{table}

Modifications explicitement rejetées (v0.13.0) : retirer l'anti-debug de la
spécification — rejeté : le mécanisme existe dans l'œuvre scellée, le retirer
du document le falsifierait ; l'arbitrage D190 le documente honnêtement dans
les DEUX documents. Corriger les décisions historiques D189/D178 en place —
rejeté : le journal est APPEND-ONLY, les décisions demeurent comme consignées,
les corrections vivent en décisions nouvelles (D190-D192). Masquer le retrait
du facteur 15,3× — rejeté : la correction est PUBLIÉE avec son mécanisme (la
méthode appliquée à sa propre revendication, jamais un chiffre faux).

\section{Journal des décisions}\label{sec:decisions}"""
D = remplace(
    D,
    "\\section{Journal des décisions}\\label{sec:decisions}",
    SEC1915,
    "D5 § 19.15")

# ---- sec-d.tex : la narration des décisions par version -------------------
D = remplace(
    D,
    "D183 (la proposition de séquestre chiffré de la\nphrase de contrôle — documentée, non appliquée), D184 (l'annexe A portée à\nsha-256, md5 demeurant une fonctionnalité de Loupe).",
    "D183 (la proposition de séquestre chiffré de la\nphrase de contrôle — documentée, non appliquée), D184 (l'annexe A portée à\nsha-256, md5 demeurant une fonctionnalité de Loupe). La v0.13.0 consigne\nles corrections de l'édition : D190 (les incohérences vérifiées une à une,\nles statistiques reformulées, la neutralité documentaire), D191 (le\nbenchmark audité — le facteur 15,3× retiré comme artefact de périmètre),\nD192 (la conséquence D81 au modèle de menace, le kit D183 préparé sans\nl'appliquer, l'état de l'art étendu).",
    "D6 narration v0.13.0")

(ICI / "sec-a.tex").write_text(A, encoding="utf-8")
(ICI / "sec-d.tex").write_text(D, encoding="utf-8")
print(f"[spec_v130] {len(REMPLACEMENTS)} remplacements ancrés :")
for r in REMPLACEMENTS:
    print("  -", r)
