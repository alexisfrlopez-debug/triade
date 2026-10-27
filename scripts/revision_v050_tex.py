#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Révision v0.5.0 des sources LaTeX (scripts/spec_v040/) + cover.html.

Chaque remplacement est vérifié (assert) — échec bruyant plutôt que silence.
Les sources LaTeX utilisent l'apostrophe typographique (convention conservée).
"""

from pathlib import Path

DIR = Path("/home/z/my-project/triade/scripts/spec_v040")


def remplace(nom_fichier: str, ancien: str, nouveau: str):
    p = DIR / nom_fichier
    s = p.read_text(encoding="utf-8")
    n = s.count(ancien)
    if n == 0:
        # idempotence : déjà appliqué ?
        ancre = nouveau.strip().splitlines()[0]
        assert ancre in s, f"{nom_fichier} : introuvable et absent : {ancien[:70]!r}"
        print(f"[--] {nom_fichier} : déjà appliqué ({ancre[:44]!r}…)")
        return
    assert n == 1, f"{nom_fichier} : {n} occurrence(s) de {ancien[:70]!r}"
    p.write_text(s.replace(ancien, nouveau, 1), encoding="utf-8")
    print(f"[ok] {nom_fichier} : {ancien[:48]!r}…")


# ================================================================ main.tex
remplace("main.tex",
         "%  PROTOCOLE TRIADE v0.4.0 — Manuscrit de spécification",
         "%  PROTOCOLE TRIADE v0.5.0 — Manuscrit de spécification")
remplace("main.tex",
         "\\fancyhead[L]{\\small\\itshape Protocole TRIADE — spécification v0.4.0}",
         "\\fancyhead[L]{\\small\\itshape Protocole TRIADE — spécification v0.5.0}")
remplace("main.tex",
         "  pdftitle={Protocole TRIADE v0.4.0 — spécification technique},",
         "  pdftitle={Protocole TRIADE v0.5.0 — spécification technique},")

# ================================================================ sec-a.tex
remplace("sec-a.tex",
         "La v0.4.0 tire les enseignements de la première validation à l’échelle — le recodage\n"
         "complet de RoomEq (démonstration v0.3) — et les convertit en normes : ce que la\n"
         "démonstration a pratiqué (reverse-specs, pré-versions, partage de fixtures, mesure avant\n"
         "optimisation) devient exigence ; ce que son analyse des défauts a révélé devient\n"
         "taxonomie ; ce que son étude de cas établit et ne prouve pas reste explicitement hors\n"
         "périmètre de preuve.",
         "La v0.4.0 tire les enseignements de la première validation à l’échelle — le recodage\n"
         "complet de RoomEq (démonstration v0.3) — et les convertit en normes : ce que la\n"
         "démonstration a pratiqué (reverse-specs, pré-versions, partage de fixtures, mesure avant\n"
         "optimisation) devient exigence ; ce que son analyse des défauts a révélé devient\n"
         "taxonomie ; ce que son étude de cas établit et ne prouve pas reste explicitement hors\n"
         "périmètre de preuve.\n\n"
         "La v0.5.0 est la révision du retour du terrain. Les jalons M0 (chaîne artefact), M1\n"
         "(mini-libc scellée) et M2 (patch à chaud en production, avec retour arrière) sont\n"
         "franchis — chacun sur validation terrain Windows 11, chacun scellé par une balise\n"
         "finale immuable (0.2.0, 0.3.0). La campagne M2 a coûté huit classes de défauts\n"
         "invisibles à l’émulation (§\\ref{sec:taxonomieX}) — le prix d’une leçon : un oracle\n"
         "valide un artefact contre un modèle d’environnement, et la complétude du modèle ne se\n"
         "démontre qu’en exécutant le binaire sur le système réel. Ce que le terrain a appris\n"
         "devient norme : la boucle d’évidence (§\\ref{sec:terrain}), la taxonomie X,\n"
         "l’instrumentation contractualisée — et l’ouverture du jalon M3, contrats renforcés\n"
         "sur entrées non fiables.")

# (§ 1.4 de sec-a : inséré par ancrage — voir plus bas, après l'exécution partielle)

remplace("sec-a.tex",
         "Indicateurs de santé : précision de localisation (cible 95 \\% dès M0), coût moyen d’une\n"
         "édition simple (cible 5 000 tokens), taux de régression post-patch (cible zéro). Ces\n"
         "budgets restent des cibles de conception jusqu’à leur instrumentation (M1) ; le tableau de\n"
         "bord les affiche alors comme métriques mesurées.",
         "Indicateurs de santé : précision de localisation (cible 95 \\% dès M0), coût moyen d’une\n"
         "édition simple (cible 5 000 tokens), taux de régression post-patch (cible zéro).\n"
         "Instrumentés depuis M1 : la mesure effective (51 / 719 / 1 088 tokens, D31) a corrigé\n"
         "le budget de localisation à 64 et valide les deux autres ; le tableau de bord les\n"
         "affiche comme métriques mesurées, avec leur écart.")

# ================================================================ sec-b.tex
remplace("sec-b.tex",
         "octet par octet ; volume de référence : douze mille cas par bloc critique. L’oracle dérive",
         "octet par octet ; volume de référence : douze mille cas par bloc critique — les campagnes\n"
         "effectives sont consignées au journal (76 010 cas en M1, 50 533 en M2, 86 pour la\n"
         "démonstration graphique). L’oracle dérive")

remplace("sec-b.tex",
         "stables garantissent qu’aucun appelant ne référence l’intérieur d’un bloc : seuls les\n"
         "points d’entrée — promis par R7 — sont trampolinés, et leur table est close et vérifiée\n"
         "par le verrou croisé. Le critère M2 : remplacer le bloc d’écho d’un serveur TCP pendant\n"
         "qu’il traite des connexions, sans interruption, avec rollback démontré.",
         "stables garantissent qu’aucun appelant ne référence l’intérieur d’un bloc : seuls les\n"
         "points d’entrée — promis par R7 — sont trampolinés, et leur table est close et vérifiée\n"
         "par le verrou croisé. Le critère M2 : remplacer le bloc d’écho d’un serveur TCP pendant\n"
         "qu’il traite des connexions, sans interruption, avec rollback démontré — \\textbf{démontré\n"
         "sur machine réelle le 27 octobre 2026} (D43) : la boucle complète (bascule pendant le\n"
         "trafic, vérification memcmp, retour arrière, re-vérification) s’est terminée par le\n"
         "constat « DÉMO OK » du journal d’exécution, au terme de la campagne relatée en\n"
         "§\\ref{sec:terrain}.")

TERRAIN_X = r"""
\subsection{La validation terrain — la boucle d'évidence}\label{sec:terrain}

La v0.5.0 élève la validation terrain au rang de couche de vérification normée (D43). Le
principe est né d'un constat structurel : l'oracle différentiel exécute le binaire contre un
\textbf{modèle} de l'environnement — chargeur, ABI, sémantique des API, protections mémoire.
Un binaire peut donc être exact au sens du round-trip, intègre au sens de la porte R10,
conforme au sens de la suite du profil, vert au sens de l'oracle — et mourir au premier appel
sur machine réelle, parce que le modèle était plus pauvre que la réalité. Les jalons M1 et
M2 en ont fourni la preuve expérimentale : huit classes de défauts ainsi invisibles
(§\ref{sec:taxonomieX}) n'ont été révélées que par l'exécution terrain.

La boucle d'évidence comporte cinq éléments normés :

\begin{enumerate}
\item \textbf{Le journal d'exécution} — l'artefact livré écrit ses preuves au fil de l'eau
(fichier à côté de l'exécutable, ligne par ligne). La règle d'honnêteté est absolue : une
ligne n'est écrite qu'après la vérification de l'étape qu'elle atteste (memcmp exact) — une
ligne présente vaut preuve ; la dernière ligne visible localise toute mortalité à
l'intervalle près.
\item \textbf{La lecture asymétrique} — le terrain retourne son verdict par un canal à
faible bande passante : le journal (éventuellement complété d'une capture). L'atelier
n'exige du terrain que ce document, jamais un diagnostic : la charge d'analyse reste à
l'agent.
\item \textbf{L'instrumentation contractualisée} — quand l'intervalle de mortalité reste
aveugle, l'itération suivante embarque des sondes de trace aux frontières (D40) : elles
journalisent des faits (positions d'exécution, retours vérifiés), jamais un succès non
prouvé ; leur retrait après constat vert est promis dans la spécification (D43 a honoré la
promesse) et vérifié par l'oracle — le journal nominal redevient exactement sa séquence de
preuves, toute ligne parasite est un échec.
\item \textbf{Le diff chirurgical} — chaque itération terrain ne modifie que les blocs
révisés ; l'audit d'itération vérifie mécaniquement qu'aucun octet hors des zones
autorisées (blocs révisés, chaînes, version, sommes) n'a bougé — l'héritage scellé reste
octet-identique (R7).
\item \textbf{L'archive brute} — chaque journal terrain est archivé tel quel (octets
d'origine, encodage et fins de ligne compris) avec son empreinte : la preuve est le
document, pas son résumé.
\end{enumerate}

Le protocole est ensuite économique : huit lectures de journal ont suffi à nommer huit
classes de défauts en deux jours (demo.1 à demo.8), et le dernier diagnostic a été obtenu
sans run supplémentaire — par lecture statique des octets appuyée sur les preuves
accumulées (D42). La contrepartie est la garantie de progression : chaque défaut nommé
devient un vecteur de falsification permanent de l'oracle — le modèle d'environnement
s'enrichit de chaque lecture terrain et ne peut plus régresser en silence.

\subsection{Taxonomie étendue — les défauts invisibles à l'émulation (X1--X8)}\label{sec:taxonomieX}

Les classes T1--T6 (§\ref{sec:taxonomie}) classent les défauts de contrat non écrit :
lisibles dans la spécification, corrigeables en écrivant le contrat. La campagne M2 a
révélé une seconde famille, structurellement différente : des défauts dont ni la
spécification, ni la notation, ni le round-trip, ni l'oracle ne parlent — parce que le
modèle d'environnement de l'oracle était, sur un point précis, plus pauvre que le système
réel. La v0.5.0 en fixe la taxonomie (D35--D43) :

\begin{table}[htbp]
\centering\footnotesize
\caption{Taxonomie des défauts invisibles à l'émulation (classes X).}
\label{tab:taxonomieX}
\begin{tabularx}{\textwidth}{@{}l l Y Y Y@{}}
\toprule
\textbf{Classe} & \textbf{Déc.} & \textbf{Modèle défaillant} & \textbf{Défaut de
référence} & \textbf{Garde permanente} \\
\midrule
X1 & D35 & sémantique du chargeur & \code{FirstThunk} $\neq$ slots appelés : le chargeur
résout ailleurs que le code n'appelle & verrou « chargeur réel » : FT = slots appelés \\
X2 & D36 & lecture de structure & \code{RECT.top} lu comme largeur : spec juste, octets
faux — bloc jamais exécuté, shim muet & coquille exécutée + invariant géométrique \\
X3 & D37 & canal de vérité & jumeau silencieux : le fichier vivait, l'écran restait vide —
défaut dans la spécification & miroir universel, les deux canaux contrôlés \\
X4 & D38 & ABI caller-saved & volatils relus après l'appel : un retour de syscall écrit
RFLAGS dans r11 & clobber des volatiles à chaque retour simulé \\
X5 & D39 & protections mémoire & phase de patch \code{PAGE\_READWRITE} sans execute : DEP
permanent x64 & le shim applique les permissions réelles \\
X6 & D40 & écart émulation/terrain & défaut latent qu'aucune exécution n'avait déclenché :
audit exhaustif vert & sondes aux frontières, instrumentation contractualisée \\
X7 & D41 & obligations ABI de l'appelant & zone d'accueil msx64 absente : l'appelé écrit
sur l'adresse de retour & shim \code{/homeparams} + audit systémique des sites \\
X8 & D42 & état hérité & section critique exigée par un bloc scellé, initialisée par un
bloc orchestrateur retiré & shims à état + exécution réelle du consommateur \\
\bottomrule
\end{tabularx}
\end{table}

Trois règles d'usage, miroir de celles de la taxonomie T. Premièrement, tout défaut terrain
corrigé est classé T ou X au journal des décisions — la métrique « défauts ouverts par
classe » du tableau de bord couvre désormais les deux familles. Deuxièmement, chaque classe
X est gardée par une falsification : réintroduire le défaut doit faire échouer l'oracle —
le modèle s'enrichit mais ne régresse jamais en silence. Troisièmement, la taxonomie est
ouverte : une neuvième classe sera nommée X9 avec sa décision, jamais dissimulée dans un
correctif muet.

La lecture académique : un oracle différentiel valide la conformité d'un artefact à un
modèle ; la validation terrain valide le modèle lui-même. Les deux couches sont
complémentaires, non redondantes — l'oracle couvre l'espace des entrées à coût nul, le
terrain couvre l'espace des environnements au coût d'un run. Le protocole exige les deux :
R5 (vérifie-puis-écrit) pour la première, la boucle d'évidence pour la seconde.
"""

remplace("sec-b.tex",
         "traçabilité vérifie ce maillon.\n\n"
         "\\subsection{Suite de conformité par profil}",
         "traçabilité vérifie ce maillon.\n\n" + TERRAIN_X +
         "\\subsection{Suite de conformité par profil}")

# ================================================================ sec-c.tex
remplace("sec-c.tex",
         "corrigés en patchs à contrat stable), qui demeure l’occurrence de référence.",
         "corrigés en patchs à contrat stable), qui demeure l’occurrence de référence. Le schéma\n"
         "a depuis été vécu deux fois par le cœur natif : les balises finales \\code{0.2.0} (M1,\n"
         "D32) et \\code{0.3.0} (M2, D43) sont posées, chacune après validation terrain consignée\n"
         "— la séquence rc.1 $\\to$ rc.4 de M2 (quatre générations, chacune sur défaut terrain\n"
         "nommé et corrigé) demeure l’occurrence de référence de la boucle d’évidence\n"
         "(§\\ref{sec:terrain}).")

# ================================================================ sec-d.tex
remplace("sec-d.tex",
         "Budgets tokens (localiser / éditer / ajouter) & $\\leq$ 40 / 3 000 / 6 000 &\n"
         "instrumentation (dès M1) \\\\",
         "Budgets tokens (localiser / éditer / ajouter) & $\\leq$ 64 / 3 000 / 6 000 &\n"
         "instrumentation — mesurés M1 : 51 / 719 / 1 088 (D31) \\\\")

# (tableau des jalons : header + 8 lignes traités par scripts/revision_v050_jalons.py)

remplace("sec-d.tex",
         "M0 est le jalon existentiel — il prouve la chaîne notation, octets, exécutable, exécution\n"
         "sans compilateur. M2 est le jalon de vérité — le patch à chaud a motivé l’architecture.",
         "M0 est le jalon existentiel — il prouve la chaîne notation, octets, exécutable, exécution\n"
         "sans compilateur ; il est franchi. M2 est le jalon de vérité — le patch à chaud a motivé\n"
         "l’architecture ; il est franchi : la boucle complète (bascule pendant le trafic,\n"
         "vérification memcmp, retour arrière, re-vérification) a été démontrée sur machine réelle\n"
         "le 27 octobre 2026 (D43), au terme de la campagne d’instrumentation relatée en\n"
         "§\\ref{sec:terrain} — huit itérations, huit classes de défauts nommées (§\\ref{sec:taxonomieX}),\n"
         "zéro régression possible : chaque classe est gardée par une falsification.")

remplace("sec-d.tex",
         "\\section{Correspondance v0.3 $\\to$ v0.4.0}\\label{sec:correspondance}",
         "\\section{Correspondance des versions}\\label{sec:correspondance}")

CORR_V050 = r"""
\subsection{Correspondance v0.4.0 $\to$ v0.5.0}\label{sec:evolutions050}

\begin{table}[htbp]
\centering\small
\caption{Les huit évolutions de la v0.5.0, tracées depuis la v0.4.0.}
\label{tab:correspondance050}
\begin{tabularx}{\textwidth}{@{}l Y Y l@{}}
\toprule
\textbf{Évolution} & \textbf{En v0.4.0} & \textbf{En v0.5.0} & \textbf{Statut} \\
\midrule
Validation terrain & constats dispersés au journal des décisions & couche normée :
boucle d'évidence, journal d'exécution, sondes contractualisées, diff chirurgical
(§\ref{sec:terrain}) & nouveau (D43) \\
Taxonomie des défauts & classes T1--T6 & + classes X1--X8, invisibles à l'émulation
(§\ref{sec:taxonomieX}) & étendu (D35--D42) \\
État des jalons & M0 planifié & M0, M1, M2 franchis — preuves terrain archivées
(§\ref{sec:jalons}) & constaté (D26, D32, D43) \\
Budgets de tokens & 40 / 3 000 / 6 000 (cibles) & 64 / 3 000 / 6 000 — corrigé et mesuré :
51 / 719 / 1 088 & corrigé (D31) \\
Suite de conformité & définie (7 éléments) & exécutée à chaque scellage rc/final — 124/124
sur le profil primaire & mesuré (D39--D43) \\
Volume d'oracle & 12 000 cas par bloc critique (référence) & campagnes effectives
consignées : 76 010 (M1), 50 533 (M2), 86 (démo) & consolidé \\
Preuves terrain & non normées & archives brutes (journaux octet-exacts, empreintes)
référencées au journal des décisions & officialisé (D43) \\
Fuzzing & mentionné (menace « fuzzing boîte noire ») & jalon M3 ouvert : fuzzing à
propriétés sur la surface d'entrées non fiables & structuré (D45) \\
\bottomrule
\end{tabularx}
\end{table}

\paragraph{Modifications explicitement rejetées (v0.5.0).} Ajouter une règle R12
« validation terrain obligatoire » — rejetée : la boucle d'évidence découle de R5 et des
critères de jalon, une règle de plus diluerait le corpus sans rien exiger de nouveau.
Étendre le fuzzing à tous les blocs scellés — rejetée : M3 cible la surface d'entrées non
fiables, les blocs à appelants de confiance relèvent des vecteurs existants. Reconstruire
les artefacts scellés 0.2.0 / 0.3.0 pour la documentation — rejetée : les balises finales
sont immuables, la documentation cite les empreintes. Fusionner les classes X dans les
classes T — rejetée : les deux familles appellent des remèdes distincts, écrire le contrat
(T) contre enrichir le modèle d'environnement et falsifier (X).
"""

remplace("sec-d.tex",
         "\\section{Journal des décisions}\\label{sec:decisions}",
         CORR_V050 + "\n\\section{Journal des décisions}\\label{sec:decisions}")

remplace("sec-d.tex",
         "est étendu aux balises finales ; le jalon de vérité M2 (patch à chaud) peut\n"
         "commencer.",
         "est étendu aux balises finales ; le jalon de vérité M2 (patch à chaud) peut\n"
         "commencer.\n\n"
         "La campagne M2 alimente ensuite le journal au rythme du terrain : D33 (base préférée\n"
         "par ancre RIP-relative — image indépendante de son adresse de chargement), D34\n"
         "(échelle d’auto-hébergement : la vérification migre vers le natif, chantier m7), D35\n"
         "(sémantique du chargeur — FirstThunk : la première classe X de la taxonomie du\n"
         "§\\ref{sec:taxonomieX}), D36 à D38 (les trois premières itérations de la démonstration\n"
         "graphique : lecture de structure, canal de vérité, ABI caller-saved — classes X2 à X4),\n"
         "D39 à D42 (la cascade : protections mémoire, écart émulation/terrain, zone d’accueil\n"
         "ABI, état hérité — classes X5 à X8), D43 (M2 clos : boucle § 5 démontrée sur machine\n"
         "réelle, retrait des sondes, scellage final 0.3.0 — la validation terrain devient\n"
         "couche normée). D44 consigne la présente révision v0.5.0 ; D45 ouvre le jalon M3\n"
         "(contrats renforcés sur entrées non fiables, fuzzing à propriétés).")

# ================================================================ cover.html
remplace("cover.html",
         '<div class="label">Sp&eacute;cification technique &middot; Version 0.4.0</div>',
         '<div class="label">Sp&eacute;cification technique &middot; Version 0.5.0</div>')

remplace("cover.html",
         "      <div class=\"subtitle\">\n"
         "        R&eacute;vision de gouvernance v&eacute;rifi&eacute;e&nbsp;: couche I normalis&eacute;e\n"
         "        (identifiants stables, cas d&rsquo;&eacute;chec, vecteurs), taxonomie des d&eacute;fauts\n"
         "        de contrat non &eacute;crit, mod&egrave;le de menace &eacute;tendu, R10 renforc&eacute;e\n"
         "        et R11 optimisation mesur&eacute;e, suite de conformit&eacute; par profil,\n"
         "        parit&eacute; inter-profils, pr&eacute;-versions dev&thinsp;/&thinsp;rc&thinsp;/&thinsp;final,\n"
         "        reverse-specs, tra&ccedil;abilit&eacute; I&thinsp;&middot;&thinsp;C&thinsp;&middot;&thinsp;B&thinsp;&middot;&thinsp;tests,\n"
         "        journal des d&eacute;cisions normalis&eacute; et tableau de bord de\n"
         "        conformit&eacute;. Hi&eacute;rarchie de la fonction objectif inchang&eacute;e&nbsp;:\n"
         "        S&eacute;curit&eacute; &gt; Performance &gt; Optimisation &gt; Co&ucirc;t en tokens.\n"
         "      </div>",
         "      <div class=\"subtitle\">\n"
         "        R&eacute;vision du retour du terrain&nbsp;: validation terrain norm&eacute;e (boucle\n"
         "        d&rsquo;&eacute;vidence, journal d&rsquo;ex&eacute;cution, instrumentation\n"
         "        contractualis&eacute;e, diff chirurgical), taxonomie &eacute;tendue X1&ndash;X8 des\n"
         "        d&eacute;fauts invisibles &agrave; l&rsquo;&eacute;mulation, jalons M0&ndash;M2 constat&eacute;s\n"
         "        franchis sur validations terrain Windows&nbsp;11 (balises 0.2.0 et 0.3.0), budgets\n"
         "        de tokens mesur&eacute;s, ouverture du jalon M3 (contrats renforc&eacute;s sur\n"
         "        entr&eacute;es non fiables). Hi&eacute;rarchie de la fonction objectif\n"
         "        inchang&eacute;e&nbsp;: S&eacute;curit&eacute; &gt; Performance &gt; Optimisation &gt;\n"
         "        Co&ucirc;t en tokens.\n"
         "      </div>")

remplace("cover.html",
         "      <div class=\"institution\">Projet TRIADE &mdash; d&eacute;veloppement agent-first<br>\n"
         "        Couche B instanci&eacute;e en code source &agrave; ce stade &middot; c&oelig;ur natif&nbsp;: jalons M0&ndash;M7</div>",
         "      <div class=\"institution\">Projet TRIADE &mdash; d&eacute;veloppement agent-first<br>\n"
         "        Jalons M0&ndash;M2 franchis&nbsp;&middot;&nbsp;M3 ouvert&nbsp;&middot;&nbsp;c&oelig;ur natif&nbsp;: jalons M0&ndash;M7</div>")

remplace("cover.html",
         "        <span>26 octobre 2026</span>",
         "        <span>27 octobre 2026</span>")

print("\nSources LaTeX + couverture révisées (v0.5.0).")
