#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Porter la chaîne spec_v100 (copie de spec_v090) à la v0.10.0 — l'édition
académique (D182) : en-têtes de version, § 1.11 « Ce que change la v0.10.0 »,
correspondance v0.9.0 → v0.10.0, l'annexe A portée à sha256 (D184),
l'annexe décisionnelle étendue D181–D184.

Aucune règle modifiée, aucune couche d'exécution ajoutée, hiérarchie
inchangée — le protocole consigne, il ne légifère pas (le modèle D180).
"""
import pathlib
import re

R = pathlib.Path("/home/z/my-project/triade/scripts/spec_v100")

# ---------------------------------------------------------------- main.tex
m = R / "main.tex"
src = m.read_text(encoding="utf-8")
src = src.replace("PROTOCOLE TRIADE v0.9.0 — Manuscrit de spécification",
                  "PROTOCOLE TRIADE v0.10.0 — Manuscrit de spécification")
src = src.replace("Protocole TRIADE — spécification v0.9.0",
                  "Protocole TRIADE — spécification v0.10.0")
src = src.replace("pdftitle={Protocole TRIADE v0.9.0 — spécification technique}",
                  "pdftitle={Protocole TRIADE v0.10.0 — spécification technique}")
m.write_text(src, encoding="utf-8")

# ---------------------------------------------------------------- cover.html
c = R / "cover.html"
src = c.read_text(encoding="utf-8")
src = src.replace("v0.9.0", "v0.10.0")
c.write_text(src, encoding="utf-8")

# ---------------------------------------------------------------- sec-a.tex
a = R / "sec-a.tex"
src = a.read_text(encoding="utf-8")

nouvelle_section = r"""\subsection{Ce que change la v0.10.0}\label{sec:nouveautes100}

La révision de L'ÉDITION ACADÉMIQUE (D182, la commande du développeur du
11/11 : trois fichiers d'instructions au dossier \code{/instructions} du
coffre). La présente révision \textbf{consigne} l'édition académique du
protocole ; elle ne modifie AUCUNE règle, n'ajoute AUCUNE couche
d'exécution, laisse la hiérarchie de la fonction objectif inchangée — le
modèle D180 : le protocole consigne, il ne légifère pas.

\textbf{LE MANUSCRIT ACADÉMIQUE} (\code{docs/TRIADE\_manuscrit\_v0.10.0.pdf},
la chaîne \code{scripts/manuscrit\_v100/}) : une édition IMRAD en anglais
(résumé français inclus), structureée autour de QUATRE questions de
recherche — le taux de défauts échappés (onze classes nommées sur douze
runs terrain), le coût en tokens par changement validé (51 / 719 / 1 088
mesurés M1, D31/D34), les classes de défauts invisibles à l'émulation (les
cinq familles : chargeur/image, ABI/SSE, sémantique du chargeur de
bibliothèque, conventions de codes d'erreur, hypothèses du harnais), la
sûreté du patch à chaud (zéro régression post-patch, monotonie signée,
anti-rollback armé) ; l'auteur humain unique (l'agent IA décrit en
méthodes et remerciements, JAMAIS co-auteur) ; les déclarations
Ethics/dual-use, Data Availability, Limitations (N=1, circularité de
l'oracle, absence de baseline, sécurité mémoire non prouvée, temps
constant non analysé) ; chaque donnée du manuscrit est GÉNÉRÉE depuis le
journal par \code{scripts/extraire\_donnees\_v100.py} — le manuscrit
n'affirme rien qui ne soit extrait et vérifié.

\textbf{LA FORMULATION CORRIGÉE} (le manuscrit et, par lui, le protocole) :
« le compilateur disparaît » devient « AUCUNE chaîne de traduction
optimisante ni opaque ; assemblage WYSIWYG vérifié par round-trip » ;
« code volé inexploitable » devient « l'évolution du code volé est
bloquée, son exécution ne l'est pas » ; les majuscules emphatiques et le
vocabulaire sacralisant cèdent aux termes standards (key ceremony, signed
manifest, sealed build) ; l'invariant D19 (Sécurité > Performance >
Optimisation > Coût en tokens) est requalifié POLITIQUE DE PROJET
EXPLICITE — non un invariant de révision : la hiérarchie demeure la règle
du projet, et le document le dit dans les termes de l'ingénierie.

\textbf{LA PROPOSITION D183 (documentée, NON appliquée au coffre réel)} :
le séquestre chiffré de la phrase de contrôle — l'alternative à la garde
durable D81 (la phrase en clair au dépôt et au coffre Drive, l'arbitrage
PERTE > EXPOSITION) : la phrase chiffrée vers une clé hors-ligne, ou
partagée en parts Shamir à seuil, la phrase en clair RETIRÉE du dépôt ;
l'analyse comparative chiffrée des risques perte/exposition vit dans la
décision D183 ; le coffre réel du développeur DEMEURE à la garde D81 —
aucune clé touchée, aucun conteneur réécrit, la proposition attend le
geste du développeur.

\textbf{L'ANNEXE A PORÉE À SHA-256} (D184) : les empreintes de gouvernance
de l'annexe A (les modules du coffre) passent de md5 à sha-256, calculées
au contenu canonique LF du dépôt (la même méthode, l'empreinte longue) ;
md5 demeure UNIQUEMENT une fonctionnalité d'affichage de Loupe (le panneau
d'empreintes, loupe-06) — AUCUN octet de la pièce ne change, et les
empreintes md5 des preuves historiques (le journal, les archives) demeurent
ce qu'elles sont : les preuves ne se réécrivent jamais.

\textbf{LES LIVRABLES} : \code{TRIADE\_soumission\_v0.10.0.zip} (cinq
fichiers au plus, readme inclus, le manuscrit en pdf — prêt pour un comité
de révision) et \code{TRIADE\_complet\_v0.10.0.zip} (l'intégralité :
sources LaTeX, bibliographie, tableaux de données, script d'extraction,
extraits de journal, empreintes). La v0.9.0 demeure : ses sources et son
PDF archivés à \code{docs/}, la chaîne \code{spec\_v090} intacte — chaque
édition vit à sa chaîne.

"""
ancre = "\\section{La couche I : format normalisé des spécifications}\\label{sec:coucheI}"
assert ancre in src, "ancre sec-a introuvable"
src = src.replace(ancre, nouvelle_section + ancre)
a.write_text(src, encoding="utf-8")

# ---------------------------------------------------------------- sec-d.tex
d = R / "sec-d.tex"
src = d.read_text(encoding="utf-8")

# 1) La correspondance v0.9.0 -> v0.10.0 (avant la section Journal des décisions)
corr = r"""\subsection{Correspondance v0.9.0 $\to$ v0.10.0}\label{sec:evolutions100}

La v0.10.0 est LA RÉVISION DE L'ÉDITION ACADÉMIQUE (D182) : aucune règle
modifiée, aucune couche d'exécution ajoutée, hiérarchie inchangée — le
protocole CONSIGNE l'édition et porte l'annexe de gouvernance à sha-256
(D184) ; la proposition D183 (le séquestre chiffré de la phrase de
contrôle) est DOCUMENTÉE, non appliquée au coffre réel.

\begin{table}[tbp]
\centering
\small
\begin{tabularx}{\textwidth}{>{\raggedright\arraybackslash}p{3.4cm} X}
\textbf{Évolution} & \textbf{Le fait consigné (v0.10.0)} \\
\midrule
LE MANUSCRIT ACADÉMIQUE & L'édition IMRAD en anglais (résumé français) —
QUATRE questions de recherche, les données réelles du journal extraites
par script (51/719/1~088 tokens ; douze runs terrain, onze classes de
défauts nommées ; zéro régression post-patch), l'auteur humain unique,
l'agent IA en méthodes et remerciements, les déclarations
Ethics/Data/Limitations (D182). \\
LA FORMULATION CORRIGÉE & « aucune chaîne de traduction optimisante ni
opaque ; assemblage WYSIWYG vérifié par round-trip » (plus jamais « le
compilateur disparaît ») ; « l'évolution du code volé est bloquée, son
exécution ne l'est pas » ; les termes standards (key ceremony, signed
manifest, sealed build) ; D19 requalifiée politique de projet explicite. \\
LA PROPOSITION D183 & Le séquestre chiffré de la phrase de contrôle
(clé hors-ligne ou parts Shamir à seuil) — l'alternative DOCUMENTÉE à la
garde durable D81, avec l'analyse comparative chiffrée des risques
perte/exposition ; NON APPLIQUÉE au coffre réel : la garde D81 demeure,
aucune clé touchée, le geste appartient au développeur. \\
L'ANNEXE A À SHA-256 & Les empreintes de gouvernance des modules du
coffre passent de md5 à sha-256 (D184) — la même méthode au contenu
canonique LF, l'empreinte longue ; md5 demeure une fonctionnalité
d'affichage de Loupe (loupe-06) ; AUCUN octet de la pièce ne change ;
les preuves historiques md5 demeurent (les preuves ne se réécrivent
jamais). \\
LES LIVRABLES & \code{TRIADE\_soumission\_v0.10.0.zip} (cinq fichiers au
plus, readme inclus, le manuscrit en pdf) et
\code{TRIADE\_complet\_v0.10.0.zip} (l'intégralité — sources,
bibliographie, données, script d'extraction, extraits, empreintes). \\
\end{tabularx}
\end{table}

Modifications explicitement rejetées (v0.10.0) : appliquer D183 au coffre
réel sans le geste du développeur — rejeté : la proposition est documentée,
l'arbitrage PERTE > EXPOSITION demeure la décision active (D81). Réécrire
les empreintes md5 des preuves historiques en sha-256 — rejeté : les
preuves sont immuables, la migration ne porte que sur la documentation de
gouvernance vivante. Toucher à la pièce Loupe (le panneau md5) — rejeté :
md5 y est une fonctionnalité d'affichage (RFC 1321 notée à la spécification
loupe-06), l'artefact scellé ne bouge jamais. Modifier les règles ou la
hiérarchie — rejeté : l'édition consigne, elle ne légifère pas (D180).

"""
ancre = "\\section{Journal des décisions}\\label{sec:decisions}"
assert ancre in src
src = src.replace(ancre, corr + ancre)

# 2) Le récit du journal des décisions : la phrase v0.9.0 complétée
src = src.replace(
    "Le journal complet vit dans \\code{docs/DECISIONS.md} du dépôt du projet. La\nv0.9.0 consolide le programme d'après M10 :",
    "Le journal complet vit dans \\code{docs/DECISIONS.md} du dépôt du projet. La\nv0.10.0 consigne l'édition académique : D182 (le manuscrit, la formulation\ncorrigée, les livrables), D183 (la proposition de séquestre chiffré de la\nphrase de contrôle — documentée, non appliquée), D184 (l'annexe A portée à\nsha-256, md5 demeurant une fonctionnalité de Loupe). La v0.9.0 avait\nconsolidé le programme d'après M10 :")

# 3) L'annexe A : md5 -> sha256 (empreintes recalculées au dépôt, v0.10.0)
annexe_vieux_debut = "\\section{Empreintes md5 des modules du dépôt}\\label{sec:empreintes}"
assert annexe_vieux_debut in src
annexe_nouvelle = r"""\section{Empreintes sha-256 des modules du dépôt}\label{sec:empreintes}

Mesurées à l'édition académique v0.10.0 (contenu canonique LF du dépôt,
D184 — la migration de gouvernance md5 $\to$ sha-256 : la même méthode,
l'empreinte longue ; l'annexe md5 de la v0.9.0 demeure aux archives de la
chaîne \code{spec\_v090}) — la génération de code se lit, ne se devine pas :
un rapport de cérémonie affiche les mêmes empreintes, le recoupement est
mécanique. md5 demeure, côté application, une fonctionnalité d'affichage de
Loupe (le panneau d'empreintes) — aucun octet de la pièce ne change.

\begin{table}[tbp]
\centering\footnotesize
\caption{Empreintes sha-256 des modules du coffre (contenu canonique LF du
dépôt, D184).}
\label{tab:empreintes}
\begin{tabularx}{\textwidth}{@{}l l Y@{}}
\toprule
\textbf{Module} & \textbf{sha-256} & \textbf{Rôle} \\
\midrule
\code{coffre\_fort.py} (racine) & \code{f5b2fb90cc020ba7fafc735ffa2b8adfe896f169f52409b75fe837808b706198} & coffre
CF1 (migration CF1 $\to$ CF2 ; terrain : divergence du clone à recouper) \\
\code{v06/coffre\_cf2.py} & \code{603ab952b45243fa1d82b1fd0b4321a7e9af8cf97feda685d429814e6043f12f} & coffre CF2 —
Shamir, sentinelle, porte D120 \\
\code{v06/coffre\_cf3.py} & \code{ea871be616964a61677be92ca671ac3d12ce4cb96a105142a4d77a7694c24891} & coffre CF3 —
serrure piégée, migration, destruction \\
\code{v06/sceau\_I.py} & \code{89048e813043a3dd73b805ac82f55f3591694c5db37f3ec954ec2bafa8170810} & sceau de
l'Intention — préparateur, dépositeur, vérificateur (le registre étendu au 14\ieme{} arbre, D177) \\
\code{v06/ceremonie\_hors\_ligne.py} & \code{b5a3fc7ac25c7ab4aab22530e1882c48a6bc43f0603fecbbeb7c54060d7bb7b7} &
cérémonie air-gap (stdlib seule) \\
\code{v06/ceremonie\_gui.py} & \code{9df2583e6aa55d6a8bfd780dc1cc309ad238c2bab30da3d3c2009e54420a28d5} &
maître de cérémonie graphique (v2.2, D131) \\
\code{v06/migration\_cf3\_gui.py} & \code{ba5c2a92141deee0246e02015d718d8ba056412ff996b4b9a5e47403c5e86eda} &
GUI de migration CF2 $\to$ CF3 (v1.1, D132) \\
\code{v06/autotest\_cf3\_gui.py} & \code{557add0cf4f69346d5dbbda218923aa5dd1e90e6daf4fecdcdd5c89396d3c04b} &
autotest CF3 graphique \\
\code{v06/sentinelle\_cf2.py} & \code{9454e7563b4038537d0189044fe69f812017ad9b7dd4b4725549d6ce5708ead8} &
sentinelle CF2 (moteur laboratoire) \\
\code{v06/test\_cf2.py} & \code{8445d97e94e5a81294387c1dec120ce12e0bcc2cdd6cd1918ea007a7709b17b5} &
falsifiabilité CF2 (Shamir, sentinelle, restauration) \\
\code{v06/test\_coffre\_cf3.py} & \code{54066b1c5d7c7efe855e9a1cbcb3547dbd02b0470a6193980c1c60c463f21ce0} &
falsifiabilité CF3 (course de clôture, pannes) \\
\code{v06/test\_sceau\_I.py} & \code{6758133cf0f62dc1c192757d371df9a255c2f47e9adc1b238a97cf14e5685f0c} &
falsifiabilité du sceau de l'Intention \\
\code{v06/test\_migration\_cf3.py} & \code{adcfe77ce6659510745c83e802f54ce7377c64e7124cdba2d3c6247684bdc04c} &
falsifiabilité de la migration CF2 $\to$ CF3 \\
\code{v06/test\_migration\_cf3\_gui.py} & \code{370364a2d68c9005dab89ed59840dc83d5ebd1cdf17beb52bf68110f1f618f12} &
falsifiabilité du GUI de migration \\
\code{v06/test\_ceremonie\_gui.py} & \code{fbfd15d9e8a49dc3f8ce4bc8273be63cff26b869014f9885c2abd7cf6855a234} &
falsifiabilité du maître de cérémonie \\
\bottomrule
\end{tabularx}
\end{table}
"""
# remplace toute l'annexe A (du \section à la fin du tableau, jusqu'à la section suivante)
debut = src.index(annexe_vieux_debut)
fin = src.index("\\section{Tableau décisionnel du coffre-fort")
src = src[:debut] + annexe_nouvelle + "\n" + src[fin:]

# 4) L'annexe décisionnelle : titre + D181-D184
src = src.replace(
    "\\section{Tableau décisionnel du coffre-fort (D75--D180)}\\label{sec:annexedecisions}",
    "\\section{Tableau décisionnel du coffre-fort (D75--D184)}\\label{sec:annexedecisions}")

nouvelles_lignes = r"""D181 & La balise \code{loupe 0.1.1} scellée & LE DOUZIÈME RUN recoupé 39/39
(T0$\to$T7 tout vert la cinquième fois, la cascade 205 la deuxième, LA
VITRINE VIVANTE la troisième — 0 et 0, la première de la pièce 0.1.1) : la
version de la dette [R10-PÉRIMÉE] soldée — la bascule
$0.1.1\text{-dev.1} \to 0.1.1$ dans frag-bld, l'entête génération 17, la
cristallisation $26 \times 10/10$, la re-signature à la graine durable,
l'anti-rollback armé, \code{loupe.exe} intact \code{c1115105…} — LE MÊME
binaire que le douzième run a couru. \\
D182 & L'édition académique v0.10.0 & le manuscrit IMRAD en anglais
(résumé français), quatre questions de recherche, les données réelles du
journal extraites par script, la formulation corrigée (WYSIWYG par
round-trip ; l'évolution du code volé bloquée, son exécution non ; les
termes standards ; D19 requalifiée politique de projet), l'auteur humain
unique, l'agent IA en méthodes et remerciements, les déclarations
Ethics/Data/Limitations ; les livrables soumission (cinq fichiers au plus)
et complet ; la chaîne \code{manuscrit\_v100} et
\code{extraire\_donnees\_v100.py}. \\
D183 & La proposition de séquestre chiffré de la phrase de contrôle &
l'alternative DOCUMENTÉE à la garde durable D81 : la phrase chiffrée vers
une clé hors-ligne ou partagée en parts Shamir à seuil, la phrase en clair
retirée du dépôt — l'analyse comparative chiffrée des risques
perte/exposition au développement de la décision ; NON APPLIQUÉE au coffre
réel : la garde D81 demeure la décision active, aucune clé touchée, le
geste appartient au développeur. \\
D184 & L'annexe A portée à sha-256 & les empreintes de gouvernance des
modules du coffre migrent de md5 à sha-256 (contenu canonique LF, la même
méthode — l'empreinte longue) ; md5 demeure UNIQUEMENT une fonctionnalité
d'affichage de Loupe (le panneau d'empreintes, loupe-06) — AUCUN octet de
la pièce ne change ; les empreintes md5 des preuves historiques demeurent
: les preuves ne se réécrivent jamais. \\
\end{longtable}"""
assert src.count("\\end{longtable}") == 1
src = src.replace("\\end{longtable}", nouvelles_lignes)
d.write_text(src, encoding="utf-8")

print("[spec_v100] main.tex, cover.html, sec-a.tex (§ 1.11), sec-d.tex "
      "(correspondance + annexe sha256 + D181-D184) portés à la v0.10.0")
