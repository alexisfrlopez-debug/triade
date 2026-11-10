#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""revision_v090_tex.py — LA CHAÎNE spec_v090 née de spec_v084 PAR COPIE (le
modèle D169/D176 : v0.7.0 après M8, v0.8.0 après M9, v0.9.0 après M10 —
l'archive v084 DEMEURE). La consolidation du programme d'après M10 :
LE JALON M10 FRANCHI (D178 — la balise `loupe 0.1.0` scellée, la méthode
TRIADE entière prouvée par la CRÉATION : onze runs, onze leçons) ET LE
PROGRAMME D'APRÈS M10 (D179/D180 — la version 0.1.1-dev.1 commandée : la
dette [R10-PÉRIMÉE] soldée à la naissance, le douzième run attendu ;
la spécification v0.9.0). Chaque remplacement ASSERTÉ."""

import shutil
from pathlib import Path

R = Path("/home/z/my-project/triade/scripts")
SRC = R / "spec_v084"
DST = R / "spec_v090"

# ═══════════ 0. LA CHAÎNE NÉE PAR COPIE (l'archive v084 demeure) ═══════════
if DST.exists():
    shutil.rmtree(DST)
shutil.copytree(SRC, DST)
print("[0] la chaîne spec_v090 née de spec_v084 par copie (l'archive demeure)")


def edite(nom, paires):
    chemin = DST / nom
    texte = chemin.read_text(encoding="utf-8")
    for ancien, nouveau in paires:
        n = texte.count(ancien)
        assert n == 1, f"[{nom}] ancre {n}x : {ancien[:70]!r}"
        texte = texte.replace(ancien, nouveau)
    chemin.write_text(texte, encoding="utf-8")
    print(f"[{nom}] {len(paires)} remplacement(s) asserté(s)")


# ═══════════ 1. main.tex — les trois littéraux de version ══════════════════
edite("main.tex", [
    ("%  PROTOCOLE TRIADE v0.8.4 — Manuscrit de spécification",
     "%  PROTOCOLE TRIADE v0.9.0 — Manuscrit de spécification"),
    ("\\fancyhead[L]{\\small\\itshape Protocole TRIADE — spécification v0.8.4}",
     "\\fancyhead[L]{\\small\\itshape Protocole TRIADE — spécification v0.9.0}"),
    ("pdftitle={Protocole TRIADE v0.8.4 — spécification technique},",
     "pdftitle={Protocole TRIADE v0.9.0 — spécification technique},"),
])

# ═══════════ 2. cover.html + merge_cover.py ════════════════════════════════
edite("cover.html", [
    ("Sp&eacute;cification technique &middot; Version 0.8.4",
     "Sp&eacute;cification technique &middot; Version 0.9.0"),
    ("r&eacute;vision v0.8.4 (quatri&egrave;me r&eacute;vision de terrain du TGN)",
     "r&eacute;vision v0.9.0 (consolidation du programme d'apr&egrave;s M10)"),
])
edite("merge_cover.py", [
    ('"/Title": "Protocole TRIADE v0.8.2 — spécification technique",',
     '"/Title": "Protocole TRIADE v0.9.0 — spécification technique",'),
])

# ═══════════ 3. sec-cf.tex — les deux phrases de l'ère du TGN ══════════════
edite("sec-cf.tex", [
    ("""déposées. L'ère du TGN (le domaine \\code{loupe}, D171) suit la même discipline : la
dette du quatorzième arbre est nommée depuis l'ouverture — le garde demeure à treize
arbres jusqu'à la cérémonie de l'ère (§\\ref{sec:ceremoniesere}). Pour chaque arbre,""",
     """déposées. L'ère du TGN (le domaine \\code{loupe}, D171) a suivi la même discipline :
la dette du quatorzième arbre fut nommée à la naissance puis SOLDÉE par la cérémonie
passée sur pièces (D177 : le garde à QUATORZE arbres, l'état « reelle » tenant — le
build de l'ère a vécu). Pour chaque arbre,"""),
    ("""\\textbf{L'ère du TGN (le domaine \\code{loupe}, D171/D175)} suit la même
discipline : la dette fut nommée à la naissance de la couche I (D171, règle 8) et la
notation des 18 blocs s'accomplit sous elle — quatre chantiers, la table de routage
de loupe-09 étendue en révision nommée sans cascade — AUCUN build : la cérémonie
précède (le miroir des ères M8/M9).""",
     """\\textbf{L'ère du TGN (le domaine \\code{loupe}, D171/D175)} a suivi la même
discipline : la dette fut nommée à la naissance de la couche I (D171, règle 8), la
notation des 18 blocs s'accomplit sous elle — quatre chantiers, la table de routage
de loupe-09 étendue en révision nommée sans cascade — AUCUN build avant la
cérémonie (le miroir des ères M8/M9) : LA CÉRÉMONIE EST PASSÉE SUR PIÈCES (D177 :
le garde à QUATORZE arbres), le build est NÉ, ONZE RUNS l'ont vécu — la balise
\\code{loupe 0.1.0} est SCELLÉE (D178) : l'ère du TGN est ACCOMPLIE."""),
])

# ═══════════ 4. sec-a.tex — le § 1.10 réécrit (la consolidation v0.9.0) ═════
_sec_a = (DST / "sec-a.tex").read_text(encoding="utf-8")
_debut = _sec_a.index("\\subsection{Ce que change la v0.8.0}")
_fin = _sec_a.index("\\section{La couche I : format normalisé des spécifications}")
NOUVEAU_110 = r"""\subsection{Ce que change la v0.9.0}\label{sec:nouveautes090}

La révision de consolidation du programme d'après M10 (D178/D179). Le \textbf{jalon
M10} (le test grandeur nature — le domaine \code{loupe}) est \textbf{franchi} :
l'application « Loupe », l'éditeur hexadécimal au panneau d'empreintes, est NÉE
ENTIÈREMENT DE LA MÉTHODE — la cérémonie d'ère passée sur pièces (le garde à
QUATORZE arbres, la dette D166/D171 soldée), la couche I de 18 spécifications
écrites-avant-code (D172), les QUATRE chantiers de notation (D173–D175 : les 18
blocs NOTÉS-MESURÉS-PROUVÉS, 159 contrôles verts aux trois graines), le kit déployé
au coffre \code{/test} (M10-(d)) — ET ONZE RUNS TERRAIN (M10-(e), Entrées 202–219) :
ONZE DÉFAUTS NOMMÉS, ONZE RETOUCHES DOCUMENTÉES — les refus du chargeur
0xc000007b (l'enveloppe prouvée de la lignée NORME DE FAIT), [CADRE-NÉ]
(l'initialiseur \code{.data} MIROIR EXACT du \code{CADRE\_VIERGE} du harnais — LE
GARDE GUÉRI : le contrôle dérive du plan, jamais de la pièce qu'il contrôle), la
classe des arguments pile (l'audit d'ABI msx64 NÉ AU BUILD), [SESSION] $-7$
VERROUILLÉ (L'OMBRE au kit, l'artefact acquitté), [HINSTANCE-PEB] (l'entrée
réécrite : r12 = GetModuleHandleW(NULL) LE VRAI MODULE), [D54-QUATRIÈME] +
[EAX-SANS-SIGNE] (l'IAT relogée à 0x3100 en QUATRE plages séparées par NULL, les 20
rendus négatifs étendus au 64 bits), [OFT-QWORD] (les QUATRE OFT au pas DWORD du
chargeur — la sixième mort NOMMÉE par le journal d'événements [4/4]),
[FREE-SANS-TYPE] (le HMODULE en POINTEUR, l'essai isolé pour TOUTE classe
d'exception), [RET-NU] (\code{mov eax, 1 ; ret} — le verdict ATTACH VRAI PAR
CONSTRUCTION), [SONDE-EXE] (le faux négatif STRUCTUREL de la sonde de liaison : le
chargeur de bibliothèque ne résout JAMAIS les imports d'un module exécutable — LA
LIAISON PROUVÉE PAR LE VIVANT) — ET LA VITRINE A VÉCU (0 et 0 aux dixième et
onzième runs : L'APPLICATION NÉE DE TRIADE A VÉCU CHEZ SON UTILISATEUR).

LE ONZIÈME RUN recoupé 39/39 : \textbf{LA BALISE \code{loupe 0.1.0} SCELLÉE PAR
FAIT DE CARTE} (D178 : la dette de la carte soldée par la RÉGÉNÉRATION DES
NOTATIONS — 18/18 notations == la pièce OCTET POUR OCTET, l'écart de l'audit
$587 \to 0$ ; la cristallisation $26 \times 10/10$ ; la re-signature à la graine
durable D144 — LE TÉMOIN NE BOUGE PAS ; l'anti-rollback ARMÉ ; \code{loupe.exe}
INTACT \code{054de960…} — LE MÊME binaire que le run a couru) : \textbf{LA MÉTHODE
TRIADE ENTIÈRE PROUVÉE PAR LA CRÉATION — de l'intention (la couche I) à l'octet
vécu chez son utilisateur}.

\textbf{LE PROGRAMME D'APRÈS M10 APPARTIENT AU DÉVELOPPEUR} : la version
\code{0.1.1-dev.1} est COMMANDÉE (D179) — la dette [R10-PÉRIMÉE] (les 17 sommes de
l'ère dev.5 que les retouches des Entrées 210/214 changèrent sans rafraîchir la
table) SOLDÉE À LA NAISSANCE : la pièce naît de LA RECOMPOSITION même (chaque
somme == son bloc relu, par construction), le qword version porté 0x00010101,
0 OCTET AILLEURS — le code BYTE-IDENTIQUE au vécu des onze runs (R4 : le contrat
stable ; R7 : les adresses intactes), la carte GÉNÉRATION 17 ; le kit
\code{0.1.1-dev.1} DÉPOSÉ au coffre \code{/test} (loupe-kit-13, le réceptacle
ARMÉ) — LE DOUZIÈME RUN ATTENDU : si le vert tient (le scénario ENTIER
T0 $\to$ S0 $\to$ LA LIAISON ET la vitrine vivante), LA BALISE
\code{loupe 0.1.1} SCELLÉE sur run terrain recoupé (le miroir D165/D170 : la porte
est de processus). Le projet fils COFFRE-FORT demeure dégelable au rythme du
développeur (D135 amendée par D171) : la frontière fondatrice demeure INTACTE.
Aucune règle du cœur n'est modifiée ; aucune couche n'est ajoutée à l'exécution ;
la hiérarchie de la fonction objectif est inchangée.

"""
(DST / "sec-a.tex").write_text(
    _sec_a[:_debut] + NOUVEAU_110 + _sec_a[_fin:], encoding="utf-8")
print("[sec-a.tex] le § 1.10 réécrit — la consolidation v0.9.0 "
      f"({len(NOUVEAU_110)} caractères)")

# ═══════════ 5. sec-d.tex — la rangée M10 FRANCHIE ══════════════════════════
_d = (DST / "sec-d.tex").read_text(encoding="utf-8")
_lignes = _d.split("\n")
_i_m10 = next(i for i, l in enumerate(_lignes)
              if l.startswith("M10 — le test grandeur nature"))
assert "\\textbf{ouvert} 07/11/2026 (D171)" in _lignes[_i_m10], "la rangée M10"
_lignes[_i_m10] = (
    "M10 — le test grandeur nature « Loupe » (domaine \\code{loupe}) & coder une "
    "application réelle NEUVE entièrement avec TRIADE, de l'intention (la couche "
    "I) à l'octet livré (le kit terrain) ; les 18 spécifications écrites-avant-"
    "code avant tout octet de notation (R2) ; les héritages PAR LA CARTE "
    "byte-identiques aux adresses scellées (R7) ; l'oracle à scénarios vert — "
    "l'écran attendu octet par octet ; le kit déployé au coffre \\code{/test} "
    "(modèle m9f) ; la balise \\code{loupe 0.1.0} scellée sur run terrain "
    "recoupé & \\textbf{franchi} 11/11/2026 (Entrées 218/219, D178) — "
    "l'application est NÉE ENTIÈREMENT DE LA MÉTHODE : la cérémonie d'ère PASSÉE "
    "SUR PIÈCES (le 14e arbre, la dette D166/D171 SOLDÉE — le garde 14/14), les "
    "18 blocs NOTÉS-MESURÉS-PROUVÉS (59 + 53 + 45 contrôles verts aux trois "
    "graines), le kit déployé (M10-(d)) — ET ONZE RUNS TERRAIN, ONZE DÉFAUTS "
    "NOMMÉS, ONZE RETOUCHES DOCUMENTÉES : les refus du chargeur 0xc000007b "
    "(dev.1/dev.2 — l'enveloppe de la lignée NORME DE FAIT), [CADRE-NÉ] (dev.4 — "
    "l'initialiseur .data MIROIR EXACT du CADRE\\_VIERGE, LE GARDE GUÉRI : le "
    "contrôle dérive du plan, jamais de la pièce qu'il contrôle), la classe des "
    "arguments pile (dev.5 — l'audit d'ABI msx64 NÉ AU BUILD), [SESSION] $-7$ "
    "VERROUILLÉ (dev.6 kit — L'OMBRE \\code{temoin-session.bin}, la pièce "
    "ACQUITTÉE), [HINSTANCE-PEB] (dev.6 — l'entrée réécrite r12 = "
    "GetModuleHandleW(NULL)), [D54-QUATRIÈME] + [EAX-SANS-SIGNE] (dev.7 — l'IAT "
    "relogée 0x3100 en QUATRE plages séparées par NULL, les 20 rendus au 64 "
    "bits), [OFT-QWORD] (dev.8 — les QUATRE OFT au pas DWORD : la sixième mort "
    "nommée par le journal d'événements [4/4]), [FREE-SANS-TYPE] (dev.12 kit — le "
    "HMODULE en POINTEUR, l'essai pour TOUTE classe), [RET-NU] (dev.11 kit — "
    "\\code{mov eax, 1 ; ret}), [SONDE-EXE] (le faux négatif STRUCTUREL : le "
    "chargeur de bibliothèque ne résout JAMAIS les imports d'un EXE — LA LIAISON "
    "PROUVÉE PAR LE VIVANT) ; LA VITRINE VIVANTE (0 et 0 aux 10e/11e runs — après "
    "six morts, L'APPLICATION NÉE DE TRIADE A VÉCU CHEZ SON UTILISATEUR) ; LE "
    "ONZIÈME RUN recoupé 39/39 (T0→T7 TOUT VERT la quatrième fois, LA CASCADE 205 "
    "VÉCUE ENTIÈRE la première, la vitrine la seconde) : LE VERT TIENT ENTIER — "
    "LA BALISE \\code{loupe 0.1.0} SCELLÉE PAR FAIT DE CARTE (D178 : la dette de "
    "la carte soldée par la RÉGÉNÉRATION DES NOTATIONS [18/18 == la pièce OCTET "
    "POUR OCTET, $587 \\to 0$], la cristallisation $26 \\times 10/10$, "
    "l'anti-rollback ARMÉ, loupe.exe INTACT \\code{054de960…}) — LA MÉTHODE "
    "TRIADE ENTIÈRE PROUVÉE PAR LA CRÉATION ; LA SUITE COMMANDÉE (D179) : la "
    "version 0.1.1-dev.1 née de la recomposition — la dette [R10-PÉRIMÉE] "
    "SOLDÉE À LA NAISSANCE (17 sommes rafraîchies à la vérité des blocs, le "
    "qword porté 0x00010101, 0 octet de code changé), le douzième run attendu : "
    "la balise \\code{loupe 0.1.1} sur le vert recoupé \\\\")
_d = "\n".join(_lignes)

edite("sec-d.tex", [
    # le préambule du § 18 — la phrase de l'épreuve menée à terme
    ("""développée de l'intention à l'octet livré, chaque geste prouvé ; la notation entière
(18 blocs) est notée-mesurée-prouvée, la cérémonie d'ère est PASSÉE (le garde à
quatorze arbres), le build est NÉ — et LE TERRAIN répond : trois refus NOMMÉS,
deux du chargeur (0xc000007b — l'oubli du BASERELOC, puis la table nécessaire
mais pas suffisante), puis LE PAS DÉCISIF : l'image cartographiée par LE VRAI
chargeur (l'enveloppe prouvée DEMEURE) et l'échec [CADRE-NÉ] nommé AU TÉMOIN
par le T0 du scénario — la retouche dev.4 fait de l'initialiseur \\code{.data} LE
MIROIR EXACT de l'état de naissance prouvé par le harnais, et le garde du build
relit LE MÊME miroir : le contrôle dérive du plan, jamais de la pièce qu'il
contrôle.""",
     """développée de l'intention à l'octet livré, chaque geste prouvé — ET ELLE EST
FRANCHIE (D178) : onze runs terrain, onze leçons — chaque défaut du kit ou de la
pièce nommé sur pièces (le chargeur, le CADRE-NÉ, la classe des arguments pile,
L'OMBRE, le HINSTANCE, l'IAT relogée, les OFT au pas DWORD, le POINTEUR du
FreeLibrary, le RET-NU, le SONDE-EXE), chaque enseignement consigné (le contrôle
dérive du plan, jamais de la pièce qu'il contrôle ; l'échec nommé vaut plus que
le vert muet ; la vitrine vivante prouve la liaison mieux que toute sonde) — et
la balise \\code{loupe 0.1.0} scellée sur le onzième run recoupé 39/39 : LA
CRÉATION A VÉCU CHEZ SON UTILISATEUR. La version \\code{0.1.1-dev.1} (D179)
poursuit : la dette [R10-PÉRIMÉE] soldée à la naissance, le douzième run attendu
scellera la balise \\code{loupe 0.1.1} sur le vert recoupé."""),
    # la ligne de chaîne PDF dans la correspondance v0.7.0 → v0.8.0
    ("""Chaîne PDF & spec\\_v070 & chaîne spec\\_v084 (née spec\\_v083 — les révisions de
terrain v0.8.1 puis v0.8.2/v0.8.3/v0.8.4) ; les archives v0.7.0, v0.8.0, v0.8.1,
v0.8.2 et v0.8.3 demeurent
(derniers builds consignés : \\code{dd36eb41…}, \\code{95226c2b…}, \\code{8907d50d…},
\\code{2c5abe4a…} et \\code{bc19403f…}) & révisé (D176, v0.8.1 puis v0.8.2/v0.8.3/v0.8.4) \\\\""",
     """Chaîne PDF & spec\\_v070 & chaîne spec\\_v090 (née spec\\_v084 par copie — la
consolidation du programme d'après M10) ; les archives v0.7.0 à v0.8.4 demeurent
(derniers builds consignés : \\code{dd36eb41…}, \\code{95226c2b…}, \\code{8907d50d…},
\\code{2c5abe4a…}, \\code{bc19403f…} et \\code{e92689ab…}) & révisé (D176, la
série de terrain v0.8.1–v0.8.4, puis D180 pour la v0.9.0) \\\\"""),
])
_d = (DST / "sec-d.tex").read_text(encoding="utf-8")

# la nouvelle correspondance v0.8.4 → v0.9.0 — insérée APRÈS la v0.8.3 → v0.8.4
# (juste avant la section « Journal des décisions »)
_deb_journal = _d.index("\\section{Journal des décisions}")
CORRESPONDANCE = r"""\subsection{Correspondance v0.8.4 $\to$ v0.9.0}\label{sec:evolutions090}

La v0.9.0 est LA RÉVISION DE CONSOLIDATION DU PROGRAMME D'APRÈS M10 (D180, le
modèle D169/D176) : aucune règle modifiée, aucune couche d'exécution ajoutée,
hiérarchie inchangée — le protocole CONSIGNE le jalon franchi et le programme
qui l'ouvre (chaque révision invalide explicitement ce qu'elle remplace, §
\ref{sec:gouvernance}).

\begin{table}[tbp]
\centering
\small
\begin{tabularx}{\textwidth}{>{\raggedright\arraybackslash}p{3.4cm} X}
\textbf{Évolution} & \textbf{Le fait consigné (v0.9.0)} \\
\midrule
LE JALON M10 FRANCHI & ONZE RUNS TERRAIN, ONZE DÉFAUTS NOMMÉS, ONZE RETOUCHES
DOCUMENTÉES (Entrées 209–219 : [HINSTANCE-PEB], [D54-QUATRIÈME] +
[EAX-SANS-SIGNE], [OFT-QWORD], [FREE-SANS-TYPE], [RET-NU], [SONDE-EXE]) — ET LA
VITRINE A VÉCU (0 et 0 aux dixième et onzième runs : L'APPLICATION NÉE DE TRIADE
A VÉCU CHEZ SON UTILISATEUR) ; le onzième run recoupé 39/39 : LE VERT TIENT
ENTIER (D178). \\
LA BALISE \code{loupe 0.1.0} SCELLÉE & PAR FAIT DE CARTE (D178) : la dette de la
carte soldée par la RÉGÉNÉRATION DES NOTATIONS (18/18 == la pièce OCTET POUR
OCTET, l'écart de l'audit $587 \to 0$), la cristallisation $26 \times 10/10$, la
re-signature à la graine durable D144 (LE TÉMOIN NE BOUGE PAS), l'anti-rollback
ARMÉ — \code{loupe.exe} INTACT \code{054de960…}, LE MÊME binaire que LE ONZIÈME
RUN a couru. \\
LA DETTE [R10-PÉRIMÉE] SOLDÉE & À LA NAISSANCE de la version \code{0.1.1-dev.1}
COMMANDÉE (D179) : la pièce naît de LA RECOMPOSITION même — les 17 sommes de
l'ère dev.5 rafraîchies à la VÉRITÉ des blocs (chaque somme == son bloc relu,
par construction), le qword porté $0x00010008 \to 0x00010101$, 0 OCTET
AILLEURS — le code BYTE-IDENTIQUE au vécu des onze runs (R4/R7) ; la carte
GÉNÉRATION 17 ; le kit \code{0.1.1-dev.1} DÉPOSÉ au coffre \code{/test}
(loupe-kit-13, le réceptacle ARMÉ). \\
LE DOUZIÈME RUN ATTENDU & LE MÊME CRITÈRE que le onzième (le scénario ENTIER
T0 $\to$ S0 $\to$ LA LIAISON ET la vitrine vivante) — si le vert tient : LA
BALISE \code{loupe 0.1.1} SCELLÉE sur run terrain recoupé (le miroir D165/D170 :
la porte est de processus, jamais de console). \\
\end{tabularx}
\end{table}

Modifications explicitement rejetées (v0.9.0) : rafraîchir la table R10 au
scellage de la 0.1.0 — rejeté : LA PIÈCE ne bouge jamais au scellage (fait de
carte) ; la dette se nomme et se paie à la version suivante, jamais un hot-fix
d'un scellé (D178). Sceller la 0.1.1 au build sans le run terrain — rejeté : le
miroir D165/D170 exige le verdict du recoup vert COMME PIÈCE. Rouvrir le jalon
M10 pour la 0.1.1 — rejeté : M10 est clos sur sa balise ; la 0.1.1 est une
version de maintenance à contrat stable (R4), pas une réépreuve du jalon.
Modifier les notations D172–D175 pour la 0.1.1 — rejeté : le code est
byte-identique au vécu des onze runs ; les notations décrivent LA PIÈCE
(R2/R5).

"""
_d = _d[:_deb_journal] + CORRESPONDANCE + _d[_deb_journal:]

# l'intro du Journal des décisions — la consolidation v0.9.0 nommée
_d = _d.replace(
    """La
v0.8.0 consolide le programme d'après M9 : D170 (le jalon M9 franchi — la finale
\\code{1.0.0} scellée sur le recoup exigé comme pièce, la session réelle la ligne
applicative chiffrée), D171 (le test grandeur nature ouvert — « Loupe » arbitrée,
le domaine \\code{loupe} fondé, la dette du quatorzième arbre nommée à la
naissance, le projet fils COFFRE-FORT dégelé), D172 (les 18 spécifications avant
tout octet de notation), D173/D174/D175 (les chantiers de notation — noyau,
rendu + navigation, édition : les 18 blocs notés-mesurés-prouvés) et D176 (la
présente consolidation). Synthèse des débuts :""",
    """La
v0.9.0 consolide le programme d'après M10 : D177 (la cérémonie d'ère du TGN
armée — le quatorzième arbre), D178 (LE JALON M10 FRANCHI — la balise
\\code{loupe 0.1.0} scellée par fait de carte sur le onzième run recoupé 39/39,
la dette de la carte soldée par la régénération des notations, la méthode TRIADE
entière prouvée par la CRÉATION), D179 (la version \\code{0.1.1-dev.1} commandée
— la dette [R10-PÉRIMÉE] soldée à la naissance, le douzième run attendu) et
D180 (la présente consolidation). Sous elle, la série de terrain v0.8.1–v0.8.4
consigne les enseignements des runs un à un ; la v0.8.0 consolide le programme
d'après M9 : D170 (le jalon M9 franchi — la finale \\code{1.0.0} scellée sur le
recoup exigé comme pièce, la session réelle la ligne applicative chiffrée),
D171 (le test grandeur nature ouvert — « Loupe » arbitrée, le domaine
\\code{loupe} fondé), D172 (les 18 spécifications avant tout octet de notation),
D173/D174/D175 (les chantiers de notation — noyau, rendu + navigation, édition :
les 18 blocs notés-mesurés-prouvés) et D176 (la consolidation d'après M9).
Synthèse des débuts :""")

# le titre du tableau décisionnel étendu
_d = _d.replace(
    "\\section{Tableau décisionnel du coffre-fort (D75--D137)}\\label{sec:annexedecisions}",
    "\\section{Tableau décisionnel du coffre-fort (D75--D180)}\\label{sec:annexedecisions}")

# l'annexe décisionnelle étendue : D177, D178, D179, D180
ANNEXE = r"""D177 & La cérémonie d'ère du TGN armée & le registre figé de m0 étendu au domaine
\code{loupe}, l'arbre \code{loupe} ENTRÉ à la table canonique (le quatorzième) ;
la remise FRAÎCHE des quatorze arbres servie au dossier \code{/Cérémonie} — le
geste hors-ligne du développeur demeure LE seul chemin vers le build de Loupe. \\
D178 & Le jalon M10 franchi : la finale \code{loupe 0.1.0} scellée & le miroir
D165/D170 porté à l'ère du TGN (le scellage REFUSE en l'absence du verdict du
recoup vert — la pièce vit au dépôt) ; la dette de la carte soldée par la
régénération des notations ; [R10-PÉRIMÉE] la dette nommée de la porte,
réparable à 0.1.1+ ; le scellage est un fait de carte, l'artefact ne bouge
jamais ; la règle des sessions parallèles : la pointe est la canonique. \\
D179 & La version 0.1.1 commandée : la dette soldée à la naissance & la pièce
\code{0.1.1-dev.1} née de la recomposition même — les 17 sommes rafraîchies à la
vérité des blocs, le qword porté, 0 octet de code changé (R4/R7) ; la carte
génération 17 ; l'anti-rollback ouvert à LA MONOTONIE R10 (la version
strictement supérieure ouvre l'ère, jamais elle ne referme l'ancienne) ; le kit
\code{0.1.1-dev.1} au coffre \code{/test} — LE DOUZIÈME RUN ATTENDU, la balise
\code{loupe 0.1.1} sur le vert recoupé. \\
D180 & La consolidation v0.9.0 & le programme d'après M10 entre en
spécification : M10 franchi (la balise \code{loupe 0.1.0} scellée sur le
onzième run recoupé — la méthode TRIADE entière prouvée par la CRÉATION), la
version \code{0.1.1-dev.1} commandée (la dette [R10-PÉRIMÉE] soldée à la
naissance), le douzième run attendu ; le projet fils COFFRE-FORT demeure
dégelable au rythme du développeur. \\
\end{longtable}"""
assert _d.count("\\end{longtable}") == 1, "l'annexe (longtable) attendue une fois"
_d = _d.replace("\\end{longtable}", ANNEXE)
(DST / "sec-d.tex").write_text(_d, encoding="utf-8")
print("[sec-d.tex] la rangée M10 FRANCHIE + le préambule + la correspondance "
      "v0.8.4 → v0.9.0 + l'annexe D177–D180")

# ═══════════ 6. verify_spec.py — le cahier v0.9.0 ═══════════════════════════
_v = (DST / "verify_spec.py").read_text(encoding="utf-8")
for ancien, nouveau in [
    ('"""Vérification post-révision du protocole TRIADE v0.8.0 (cahier de révision).',
     '"""Vérification post-révision du protocole TRIADE v0.9.0 (cahier de révision\n— la consolidation du programme d\'après M10, le modèle D169/D176).'),
    ('with pdfplumber.open(HERE / "docs" / "Protocole_TRIADE_v0.8.0_Specification.pdf") as pdf:',
     'with pdfplumber.open(HERE / "docs" / "Protocole_TRIADE_v0.9.0_Specification.pdf") as pdf:'),
    ('check("V8", "entrée v0.8.0 au journal des versions",\n      "| v0.8.0 | 8 nov. 2026 |" in SPEC_RAW)',
     'check("V8", "entrée v0.9.0 au journal des versions",\n      "| v0.9.0 | 11 nov. 2026 |" in SPEC_RAW)'),
    ('check("V8", "correspondance v0.7.0 → v0.8.0 présente",\n      "### 19.10 Correspondance v0.7.0 → v0.8.0" in SPEC_RAW)',
     'check("V8", "correspondance v0.7.0 → v0.8.0 présente",\n      "### 19.10 Correspondance v0.7.0 → v0.8.0" in SPEC_RAW)\n'
     'check("V8", "correspondance v0.8.4 → v0.9.0 présente",\n      "### 19.11 Correspondance v0.8.4 → v0.9.0" in SPEC_RAW)'),
    ('check("V9", "modifications rejetées v0.8.0 consignées",\n      "Modifications explicitement rejetées (v0.8.0)" in SPEC_RAW)',
     'check("V9", "modifications rejetées v0.8.0 consignées",\n      "Modifications explicitement rejetées (v0.8.0)" in SPEC_RAW)\n'
     'check("V9", "modifications rejetées v0.9.0 consignées",\n      "Modifications explicitement rejetées (v0.9.0)" in SPEC_RAW)'),
    ('check("V15", "§ 1.10 « Ce que change la v0.8.0 » présent",\n      "### 1.10 Ce que change la v0.8.0" in SPEC_RAW)',
     'check("V15", "§ 1.10 « Ce que change la v0.9.0 » présent",\n      "### 1.10 Ce que change la v0.9.0" in SPEC_RAW)'),
    ('check("V15", "D176 consignée aux décisions",\n      "## D176 —" in DEC_RAW)',
     'check("V15", "D176 consignée aux décisions",\n      "## D176 —" in DEC_RAW)\n'
     'check("V15", "D179 consignée aux décisions",\n      "## D179 —" in DEC_RAW)\n'
     'check("V15", "D180 consignée aux décisions",\n      "## D180 —" in DEC_RAW)'),
    ('check("V16", "§ 1.10 au PDF (Ce que change la v0.8.0)",\n      "Ce que change la v0.8.0" in PDF_SPEC)',
     'check("V16", "§ 1.10 au PDF (Ce que change la v0.9.0)",\n      "Ce que change la v0.9.0" in PDF_SPEC)'),
    ('check("V16", "version v0.8.0 au PDF (en-tête de page)",\n      "v0.8.0" in PDF_SPEC)',
     'check("V16", "version v0.9.0 au PDF (en-tête de page)",\n      "v0.9.0" in PDF_SPEC)\n'
     'check("V16", "M10 franchi au PDF (la rangée du § 18)",\n      "franchi" in PDF_SPEC and "loupe 0.1.0" in PDF_SPEC)\n'
     'check("V16", "la dette soldée au PDF (0.1.1, D179)",\n      "SOLDÉE" in PDF_SPEC and "0.1.1-dev.1" in PDF_SPEC)'),
    ('print(f"CAHIER v0.8.0 : TOUT PASSÉ — spécification {N_PAGES_SPEC} pages, "',
     'print(f"CAHIER v0.9.0 : TOUT PASSÉ — spécification {N_PAGES_SPEC} pages, "'),
]:
    n = _v.count(ancien)
    assert n == 1, f"[verify] ancre {n}x : {ancien[:70]!r}"
    _v = _v.replace(ancien, nouveau)
(DST / "verify_spec.py").write_text(_v, encoding="utf-8")
print("[verify_spec.py] le cahier porté à la v0.9.0 (journal, correspondance, "
      "rejets, D179/D180, M10 franchi, la dette soldée)")
print("\nLA CHAÎNE spec_v090 EST PRÊTE : build_pdf.sh construit, verify_spec.py"
      " vérifie — le PDF v0.9.0 attend ses pages")
