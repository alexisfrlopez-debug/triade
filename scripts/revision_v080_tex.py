#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""revision_v080_tex.py — les éditions LaTeX de la chaîne spec_v080 (miroir de
revision_v070_tex.py, modèle D169) : la consolidation du programme d'après M9
(D170/D171/D176). Chaque ancrage est ASSERTÉ (trouvé UNE fois) — un ancrage
fautif = ÉCHEC NOMMÉ, rien n'est écrit.

Vingt-trois remplacements :
  main.tex    (4)  titre, chaîne des révisions, fancyhead, pdftitle ;
  sec-a.tex   (1)  § 1.10 « Ce que change la v0.8.0 » NOUVEAU ;
  sec-c.tex   (1)  les domaines : sys + tls13 + loupe (le TGN) ;
  sec-cf.tex  (2)  § 12.4 la dette du quatorzième arbre ; § 13.5 l'ère du TGN ;
  sec-d.tex   (8)  titre M0 à M10, Onze jalons, M9 FRANCHI + la rangée M10
                   NOUVELLE, la clôture étendue, le paragraphe TGN, la
                   correspondance v0.7.0 → v0.8.0 NOUVELLE + rejets, la synthèse
                   du journal, l'annexe décisionnelle D170–D176 ;
  cover.html  (4)  label, sous-titre, institution, pied de page ;
  merge_cover (3)  miroir, /Title, /Creator.
"""
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
CH = REPO / "scripts" / "spec_v080"


def remplace(chemin, ancres):
    p = CH / chemin
    t = p.read_text(encoding="utf-8")
    echecs = []
    for anc, nouv in ancres:
        n = t.count(anc)
        if n != 1:
            echecs.append(f"{chemin} : ancrage {n} fois : {anc[:60]!r}…")
            continue
        t = t.replace(anc, nouv)
    if echecs:
        return echecs
    p.write_text(t, encoding="utf-8")
    return []


echecs = []

# ================================================================= main.tex
echecs += remplace("main.tex", [
    (
        "%  PROTOCOLE TRIADE v0.7.0 — Manuscrit de spécification",
        "%  PROTOCOLE TRIADE v0.8.0 — Manuscrit de spécification",
    ),
    (
        "%  TREIZE arbres, les cérémonies d'ère au protocole).",
        "%  TREIZE arbres, les cérémonies d'ère au protocole) → spec_v080\n"
        "%  (D176 — la consolidation du programme d'après M9 : le domaine\n"
        "%  `tls13` FRANCHI [finale 1.0.0, la session réelle], le test\n"
        "%  grandeur nature ouvert [M10 « Loupe », la notation 18/18], la\n"
        "%  dette du quatorzième arbre nommée — la cérémonie d'ère du TGN\n"
        "%  précède tout build).",
    ),
    (
        "\\fancyhead[L]{\\small\\itshape Protocole TRIADE — spécification v0.7.0}",
        "\\fancyhead[L]{\\small\\itshape Protocole TRIADE — spécification v0.8.0}",
    ),
    (
        "  pdftitle={Protocole TRIADE v0.7.0 — spécification technique},",
        "  pdftitle={Protocole TRIADE v0.8.0 — spécification technique},",
    ),
])

# ================================================================= sec-a.tex
echecs += remplace("sec-a.tex", [
    # § 1.10 NOUVEAU — entre la fin du § 1.9 (v0.7.0) et la couche I
    (
        "règle 8) ; la charge se prépare au geste qui sert la main du développeur (D168). Aucune\n"
        "règle du cœur n'est modifiée ; aucune couche n'est ajoutée à l'exécution ; la hiérarchie\n"
        "de la fonction objectif est inchangée.\n"
        "\n"
        "\\section{La couche I : format normalisé des spécifications}\\label{sec:coucheI}",
        "règle 8) ; la charge se prépare au geste qui sert la main du développeur (D168). Aucune\n"
        "règle du cœur n'est modifiée ; aucune couche n'est ajoutée à l'exécution ; la hiérarchie\n"
        "de la fonction objectif est inchangée.\n"
        "\n"
        "\\subsection{Ce que change la v0.8.0}\\label{sec:nouveautes080}\n"
        "\n"
        "La révision de consolidation du programme d'après M9 (D170/D171). Le \\textbf{jalon M9}\n"
        "(TLS 1.3 pur en blocs scellés — le domaine \\code{tls13}, l'ère 1.0.0) est franchi : les\n"
        "28 blocs notés-mesurés-prouvés — les primitives aux vecteurs officiels octet pour octet\n"
        "(FIPS 180-4, RFC 2104/4231, 5869, 7748, SP 800-38D), la poignée rejouée sur le\n"
        "transcript RFC 8448, les héritages PAR LA CARTE (R7) —, le socle socket par syscalls\n"
        "directs, le septième run terrain vert sur pièces et recoupé 34/34, LA SESSION RÉELLE\n"
        "(la ligne applicative chiffrée ÉCHANGÉE avec un serveur réel, le témoin\n"
        "« HTTP/1.1 200 OK » DÉCHIFFRÉ PAR LA MACHINE, l'épinglage $-6$ NOMMÉ contre le vrai\n"
        "serveur, la fermeture propre), la finale \\code{1.0.0} scellée sur le recoup exigé\n"
        "comme pièce (D170 : le scellage est un fait de carte, l'artefact ne bouge jamais) — et\n"
        "l'ère M8 refermée propre par l'export de continuité. \\textbf{LE TEST GRANDEUR NATURE\n"
        "est ouvert (D171)} : le protocole avait prouvé chaque capacité, M0 à M9 — il reste à\n"
        "prouver qu'il DÉVELOPPE une application réelle NEUVE, de l'intention à l'octet livré\n"
        "(le modèle RoomEq s'arrêtait au recodage ; le TGN exige la CRÉATION). L'application —\n"
        "arbitrée à D171, contredisable — est « Loupe », l'éditeur hexadécimal au panneau\n"
        "d'empreintes sur le profil primaire (l'outil du quotidien du projet : voir les octets,\n"
        "leurs lignes, leurs empreintes md5/sha-256, leur place) : le domaine \\code{loupe}\n"
        "fondé (la charte + le tableau des 18 blocs en cinq familles), la couche I posée\n"
        "écrite-avant-code (D172 : les 18 spécifications, le plan d'adressage arrêté avant\n"
        "toute notation, la table des sept verdicts), et les QUATRE chantiers de notation\n"
        "accomplis — le noyau fichier + empreintes (D173 : les héritages vivent à leurs\n"
        "adresses scellées, le mini-OS virtuel du harnais), le rendu + la navigation (D174 :\n"
        "l'oracle à scénarios — l'écran attendu octet par octet —, le mini-GUI virtuel, le\n"
        "plancher qui ne recule jamais), l'édition + la table de routage étendue de loupe-09\n"
        "r2 (D175 : le disque saisissable et la mort du harnais, le réseau de la garde\n"
        "16$\\leftrightarrow$17$\\leftrightarrow$18, l'écriture à l'octet prouvée différentielle) —\n"
        "les 18 blocs NOTÉS-MESURÉS-PROUVÉS, 45 + 53 + 59 contrôles verts aux trois graines sur\n"
        "les trois harnais. Le \\textbf{kit terrain attend LA CÉRÉMONIE D'ÈRE du TGN} : la dette\n"
        "D166/D171 est nommée à la naissance — le quatorzième arbre (\\code{loupe}) et\n"
        "l'extension du registre figé exigent la clé hors-ligne du développeur AVANT tout build\n"
        "(§\\ref{sec:ceremoniesere}) ; le garde demeure à treize arbres. Le projet fils\n"
        "COFFRE-FORT est dégelé en parallèle (D135 amendée par D171) : le père continue sans\n"
        "ralentir, la frontière fondatrice demeure INTACTE. Aucune règle du cœur n'est\n"
        "modifiée ; aucune couche n'est ajoutée à l'exécution ; la hiérarchie de la fonction\n"
        "objectif est inchangée.\n"
        "\n"
        "\\section{La couche I : format normalisé des spécifications}\\label{sec:coucheI}",
    ),
])

# ================================================================= sec-c.tex
echecs += remplace("sec-c.tex", [
    (
        "\\paragraph{Les domaines du programme d'après M7 (D160).} Deux domaines s'ajoutent\n"
        "sur le profil primaire : \\code{sys} (M8 — les syscalls directs, balise \\code{0.9.0} :\n"
        "le SSN lu de l'EAT de \\code{ntdll}, jamais un octet de code) et \\code{tls13} (M9 —\n"
        "TLS 1.3 pur, ère \\code{1.0.0}) ; chacun est une lignée de couche I à part entière\n"
        "sous le sceau (§\\ref{sec:sceauI}) et s'ajoute au profil sans le modifier —\n"
        "l'universalité demeure structurelle.",
        "\\paragraph{Les domaines du programme d'après M7 (D160), l'épreuve du TGN en plus (D171).}\n"
        "Trois domaines s'ajoutent sur le profil primaire : \\code{sys} (M8 — les syscalls\n"
        "directs, balise \\code{0.9.0} : le SSN lu de l'EAT de \\code{ntdll}, jamais un octet de\n"
        "code), \\code{tls13} (M9 — TLS 1.3 pur, ère \\code{1.0.0}, finale scellée) et\n"
        "\\code{loupe} (M10 — le test grandeur nature : l'éditeur hexadécimal au panneau\n"
        "d'empreintes, la première application réelle NEUVE développée de l'intention à\n"
        "l'octet livré) ; chacun est une lignée de couche I à part entière sous le sceau\n"
        "(§\\ref{sec:sceauI}) et s'ajoute au profil sans le modifier — l'universalité demeure\n"
        "structurelle.",
    ),
])

# ================================================================ sec-cf.tex
echecs += remplace("sec-cf.tex", [
    # (a) § 12.4 — la dette du quatorzième arbre (l'ère du TGN)
    (
        "Ed25519 (D163) : re-signer les arbres inchangés redonne exactement les signatures\n"
        "déposées. Pour chaque arbre, le \\textbf{manifeste} est le texte",
        "Ed25519 (D163) : re-signer les arbres inchangés redonne exactement les signatures\n"
        "déposées. L'ère du TGN (le domaine \\code{loupe}, D171) suit la même discipline : la\n"
        "dette du quatorzième arbre est nommée depuis l'ouverture — le garde demeure à treize\n"
        "arbres jusqu'à la cérémonie de l'ère (§\\ref{sec:ceremoniesere}). Pour chaque arbre,\n"
        "le \\textbf{manifeste} est le texte",
    ),
    # (b) § 13.5 — l'ère du TGN (la cérémonie attend son geste)
    (
        "cérémonie d'ère n'est pas une formalité de documentation — c'est le geste qui\n"
        "rend le build de l'ère possible, et il suit le calendrier du garde, jamais\n"
        "l'inverse.",
        "cérémonie d'ère n'est pas une formalité de documentation — c'est le geste qui\n"
        "rend le build de l'ère possible, et il suit le calendrier du garde, jamais\n"
        "l'inverse. \\textbf{L'ère du TGN (le domaine \\code{loupe}, D171/D175)} suit la même\n"
        "discipline : la dette fut nommée à la naissance de la couche I (D171, règle 8) et la\n"
        "notation des 18 blocs s'accomplit sous elle — quatre chantiers, la table de routage\n"
        "de loupe-09 étendue en révision nommée sans cascade — AUCUN build : la cérémonie\n"
        "précède (le miroir des ères M8/M9). Le kit de cérémonie vit au dossier\n"
        "\\code{/Cérémonie} du Drive (la remise FRAÎCHE des quatorze arbres — la charge se\n"
        "prépare AU GESTE de la cérémonie, D168 : les empreintes bougent avec chaque\n"
        "révision de spécification — le LISEZMOI pas à pas, la règle d'or « JAMAIS generer »)\n"
        ": le développeur signe hors ligne à la clé du 04/11 (l'ancre de toutes les ères),\n"
        "ramène \\code{signatures-I.txt} et \\code{cle-publique-I.txt} au coffre \\code{/test}\n"
        "; le laboratoire rapatrie, recoupe (l'ancre de clé, les arbres inchangés rendant\n"
        "les MÊMES signatures par le déterminisme Ed25519, m0 re-signé au registre étendu,\n"
        "l'arbre \\code{loupe} neuf), installe canoniquement — et le garde passe à QUATORZE\n"
        "arbres VERTS : le build de Loupe peut naître.",
    ),
])

# ================================================================= sec-d.tex
echecs += remplace("sec-d.tex", [
    # (a) le titre des jalons
    (
        "\\section{Critères d'acceptation des jalons M0 à M9}\\label{sec:jalons}",
        "\\section{Critères d'acceptation des jalons M0 à M10}\\label{sec:jalons}",
    ),
    # (b) l'intro — onze jalons
    (
        "Dix jalons, chacun avec des critères de sortie mesurables",
        "Onze jalons, chacun avec des critères de sortie mesurables",
    ),
    # (c) M9 FRANCHI + la rangée M10 NOUVELLE
    (
        "la session réelle — la ligne applicative chiffrée & \\textbf{ouvert} 05/11/2026 (D166) — couche I complète (28 spécifications, l'instrument 117 verts, D167) ; cérémonie de l'ère passée le 05/11 (13 arbres, garde 13/13) ; chantiers (b) notation, (c) harnais RFC 8448, (d) socle socket, (e) build \\code{1.0.0-dev.1}, (f) terrain $\\to$ finale \\code{1.0.0} \\\\",
        "la session réelle — la ligne applicative chiffrée & \\textbf{franchi} 07/11/2026, \\code{1.0.0} (Entrées 170--194, D166--D170 : les 28 blocs notés-mesurés-prouvés aux vecteurs officiels, la poignée sur le transcript RFC 8448, le socle socket par syscalls directs ; le septième run terrain vert recoupé 34/34 sur pièces croisées, LA SESSION RÉELLE — la ligne applicative chiffrée échangée avec un serveur réel, le témoin « HTTP/1.1 200 OK » déchiffré par la machine, l'épinglage $-6$ nommé ; la finale scellée sur recoup exigé comme pièce, \\code{proxy.exe} byte-identique \\code{446279f3…}) \\\\\n"
        "M10 — le test grandeur nature « Loupe » (domaine \\code{loupe}) & coder une application réelle NEUVE entièrement avec TRIADE, de l'intention (la couche I) à l'octet livré (le kit terrain) ; les 18 spécifications écrites-avant-code avant tout octet de notation (R2) ; les héritages PAR LA CARTE byte-identiques aux adresses scellées (R7) ; l'oracle à scénarios vert — l'écran attendu octet par octet ; le kit déployé au coffre \\code{/test} (modèle m9f) ; la balise \\code{loupe 0.1.0} scellée sur run terrain recoupé & \\textbf{ouvert} 07/11/2026 (D171) — la couche I complète (18 spécifications, D172) et les QUATRE chantiers de notation accomplis : le noyau (D173), le rendu + la navigation (D174), l'édition + la table de routage étendue de loupe-09 r2 (D175) — les 18 blocs NOTÉS-MESURÉS-PROUVÉS (59 + 53 + 45 contrôles verts aux trois graines) ; LA CÉRÉMONIE D'ÈRE du TGN précède le build (le 14e arbre, la dette D166/D171) puis le kit terrain (M10-(d) seconde moitié) et le run (M10-(e)) \\\\",
    ),
    # (d) la clôture des jalons — la phrase M10
    (
        "M8 et M9 sont les additions mesurées du programme d'après M7 (D160) : la\n"
        "fondation d'abord — le domaine \\code{sys} est la condition d'une pile TLS 1.3 qui\n"
        "n'émettrait plus par l'IAT userland ; chaque famille s'appuie sur les résultats\n"
        "mesurés de la précédente.",
        "M8 et M9 sont les additions mesurées du programme d'après M7 (D160) : la\n"
        "fondation d'abord — le domaine \\code{sys} est la condition d'une pile TLS 1.3 qui\n"
        "n'émettrait plus par l'IAT userland ; chaque famille s'appuie sur les résultats\n"
        "mesurés de la précédente. M10 est l'épreuve de la MÉTHODE ENTIÈRE (D171) : non plus\n"
        "une capacité, mais une application réelle neuve — l'outil du quotidien du projet —\n"
        "développée de l'intention à l'octet livré, chaque geste prouvé ; la notation entière\n"
        "(18 blocs) est notée-mesurée-prouvée, le build attend la cérémonie d'ère du TGN.",
    ),
    # (e) le paragraphe TGN après le programme d'après M7
    (
        "L'ordre est la\n"
        "fondation d'abord : une pile TLS pure qui émettrait encore par l'IAT userland\n"
        "garderait la surface de hook qu'elle prétend éliminer.",
        "L'ordre est la\n"
        "fondation d'abord : une pile TLS pure qui émettrait encore par l'IAT userland\n"
        "garderait la surface de hook qu'elle prétend éliminer.\n"
        "\n"
        "\\paragraph{Le test grandeur nature (D171).} Le protocole a prouvé chaque capacité,\n"
        "M0 à M9 ; il reste à prouver qu'il DÉVELOPPE une application réelle NEUVE, de\n"
        "l'intention à l'octet livré — le modèle RoomEq (v0.3) s'arrêtait au recodage d'une\n"
        "application existante, le TGN exige la CRÉATION. L'application arbitrée est\n"
        "« Loupe », l'éditeur hexadécimal natif au panneau d'empreintes sur le profil\n"
        "primaire (\\code{loupe.exe}, la lignée de balises propre \\code{loupe 0.1.0-dev.1} au\n"
        "premier build) : voir les octets, leurs lignes, leurs empreintes md5/sha-256, leur\n"
        "place — l'outil du quotidien du projet. La découpe du plan est la loi : la cérémonie\n"
        "d'ère précède le build (le miroir M8/M9 — Entrées 157/158), la notation s'accomplit\n"
        "sous la dette nommée (D166/D171).",
    ),
    # (f) la correspondance v0.7.0 → v0.8.0 NOUVELLE
    (
        "\\section{Journal des décisions}\\label{sec:decisions}",
        "\\subsection{Correspondance v0.7.0 $\\to$ v0.8.0}\\label{sec:evolutions080}\n"
        "\n"
        "\\begin{table}[htbp]\n"
        "\\centering\\small\n"
        "\\caption{Les évolutions de la v0.8.0, tracées depuis la v0.7.0 (D176).}\n"
        "\\label{tab:correspondance080}\n"
        "\\begin{tabularx}{\\textwidth}{@{}l Y Y l@{}}\n"
        "\\toprule\n"
        "\\textbf{Évolution} & \\textbf{En v0.7.0} & \\textbf{En v0.8.0} & \\textbf{Statut} \\\\\n"
        "\\midrule\n"
        "Programme d'après M9 & M9 ouvert : couche I complète, la cérémonie passée, les\n"
        "chantiers (b) à (f) attendent & M9 FRANCHI : les 28 blocs notés-mesurés-prouvés,\n"
        "le septième run terrain vert recoupé, LA SESSION RÉELLE (la ligne applicative\n"
        "chiffrée avec un serveur réel), la finale \\code{1.0.0} scellée sur recoup exigé\n"
        "comme pièce (D170) & révisé (D170) \\\\\n"
        "Le test grandeur nature & — & LE TGN ouvert (D171) : « Loupe », l'éditeur\n"
        "hexadécimal au panneau d'empreintes — coder une application réelle NEUVE\n"
        "entièrement avec TRIADE ; le domaine \\code{loupe} fondé, la couche I de 18\n"
        "spécifications posée (D172) et les QUATRE chantiers de notation accomplis\n"
        "(D173/D174/D175 : les 18 blocs notés-mesurés-prouvés, la table de routage de\n"
        "loupe-09 étendue en révision nommée) & nouveau (D171--D175) \\\\\n"
        "Sceau de l'Intention & treize arbres, les cérémonies d'ère M8/M9 passées & treize\n"
        "arbres + LA DETTE DU QUATORZIÈME nommée (l'ère du TGN : l'arbre \\code{loupe} et\n"
        "le registre figé étendu attendent la clé hors-ligne AVANT tout build —\n"
        "§\\ref{sec:ceremoniesere}) ; le garde demeure à 13/13 jusque-là & étendu\n"
        "(D166/D171/D175) \\\\\n"
        "Projet fils COFFRE-FORT & développement différé (D135) & DÉGELÉ en parallèle du\n"
        "TGN (D171) : le fils vit son rythme, la frontière fondatrice intacte — aucun code\n"
        "TRIADE forké, aucune dépendance vivante & révisé (D171) \\\\\n"
        "Chaîne PDF & spec\\_v070 & chaîne spec\\_v080 ; l'archive v0.7.0 demeure (dernier\n"
        "build consigné : sha256 \\code{dd36eb41…}, 999 631 o) & révisé (D176) \\\\\n"
        "\\bottomrule\n"
        "\\end{tabularx}\n"
        "\\end{table}\n"
        "\n"
        "\\paragraph{Modifications explicitement rejetées (v0.8.0).} Réviser la spécification\n"
        "à chaque franchissement de jalon — rejeté : le versionnement suit les RÉVISIONS (la\n"
        "v0.8.0 consolide le PROGRAMME d'après M9 : M9 franchi ET le TGN ouvert, deux\n"
        "moteurs d'une même passation). Mettre l'application « Loupe » sous le sceau AVANT\n"
        "la cérémonie — rejeté : le garde suit le calendrier de la cérémonie, jamais\n"
        "l'inverse (§\\ref{sec:ceremoniesere}). Ajouter un profil de cible pour le TGN —\n"
        "rejeté : le profil primaire \\code{x86-64-win11-pe} est l'épreuve ; l'universalité\n"
        "est déjà prouvée (M6/M7). Sceller la 0.1.0 de Loupe au build — rejeté : la balise\n"
        "de développement naît au build (geste de BUILD jamais scellage, miroir\n"
        "M6/M7/M8) ; la 0.1.0 se scellera sur le run terrain vert recoupé.\n"
        "\n"
        "\\section{Journal des décisions}\\label{sec:decisions}",
    ),
    # (g) la synthèse du journal — la phrase v0.8.0 en tête
    (
        "Le journal complet vit dans \\code{docs/DECISIONS.md} du dépôt du projet. La\n"
        "v0.7.0 consolide le programme d'après M7 : D160 (l'ordre des familles — la\n"
        "fondation d'abord), D162/D163 (la cérémonie de l'ère M8, la continuité de clé par\n"
        "le déterminisme Ed25519), D165 (la finale d'une ère se scelle sur le recoup\n"
        "exigé comme pièce), D166 (l'ouverture M9 — TLS 1.3 pur, la dette de cérémonie\n"
        "nommée à la naissance), D167 (les 28 spécifications avant tout octet de\n"
        "notation), D168 (la charge se prépare au geste de la cérémonie) et D169 (la\n"
        "présente consolidation). Synthèse des débuts :",
        "Le journal complet vit dans \\code{docs/DECISIONS.md} du dépôt du projet. La\n"
        "v0.8.0 consolide le programme d'après M9 : D170 (le jalon M9 franchi — la finale\n"
        "\\code{1.0.0} scellée sur le recoup exigé comme pièce, la session réelle la ligne\n"
        "applicative chiffrée), D171 (le test grandeur nature ouvert — « Loupe » arbitrée,\n"
        "le domaine \\code{loupe} fondé, la dette du quatorzième arbre nommée à la\n"
        "naissance, le projet fils COFFRE-FORT dégelé), D172 (les 18 spécifications avant\n"
        "tout octet de notation), D173/D174/D175 (les chantiers de notation — noyau,\n"
        "rendu + navigation, édition : les 18 blocs notés-mesurés-prouvés) et D176 (la\n"
        "présente consolidation). Synthèse des débuts :",
    ),
    # (h) l'annexe décisionnelle — les lignes D170 à D176
    (
        "D169 & La consolidation v0.7.0 & le programme d'après M7 entre en spécification :\n"
        "M8 franchi, M9 ouvert, le sceau à treize arbres, les cérémonies d'ère au\n"
        "protocole ; la clause « hors périmètre courant » levée pour les deux premières\n"
        "familles. \\\\\n"
        "\\end{longtable}",
        "D169 & La consolidation v0.7.0 & le programme d'après M7 entre en spécification :\n"
        "M8 franchi, M9 ouvert, le sceau à treize arbres, les cérémonies d'ère au\n"
        "protocole ; la clause « hors périmètre courant » levée pour les deux premières\n"
        "familles. \\\\\n"
        "D170 & Le jalon M9 franchi : la finale 1.0.0 & le scellage sur le recoup terrain\n"
        "exigé comme pièce (le miroir D165 à l'ère M9) ; un fait de carte, l'artefact ne\n"
        "bouge jamais — \\code{proxy.exe} byte-identique \\code{446279f3…}. \\\\\n"
        "D171 & Le test grandeur nature ouvert & « Loupe », l'éditeur hexadécimal au\n"
        "panneau d'empreintes, arbitrée (contredisable au message suivant) ; le domaine\n"
        "\\code{loupe} fondé ; la dette de cérémonie nommée à la naissance ; le projet\n"
        "fils COFFRE-FORT dégelé en parallèle. \\\\\n"
        "D172 & Le chantier M10-(a) clos sur les 18 spécifications & la couche I complète\n"
        "du TGN avant tout octet de notation (R2) ; le plan d'adressage arrêté avant la\n"
        "notation (D161 rejoué). \\\\\n"
        "D173 & Le chantier M10-(b) : le noyau noté-mesuré-prouvé & fichier + empreintes\n"
        "(sha-256 par la carte, md5 la notation neuve RFC 1321) ; les héritages vivent à\n"
        "leurs adresses scellées (R7) ; le mini-OS virtuel du harnais. \\\\\n"
        "D174 & Le chantier M10-(c) : rendu + navigation & l'oracle à scénarios vert —\n"
        "l'écran attendu octet par octet — et la falsification attrapée ; le mini-GUI\n"
        "virtuel du harnais ; le plancher qui ne recule jamais. \\\\\n"
        "D175 & Le chantier M10-(d), première moitié : l'édition & la famille édition\n"
        "notée-mesurée-prouvée (le disque saisissable, la mort du harnais, le réseau de\n"
        "la garde 16$\\leftrightarrow$17$\\leftrightarrow$18, l'écriture à l'octet prouvée\n"
        "différentielle) ; le kit terrain attend la cérémonie d'ère. \\\\\n"
        "D176 & La consolidation v0.8.0 & le programme d'après M9 entre en spécification :\n"
        "M9 franchi (finale \\code{1.0.0}), le TGN ouvert (« Loupe », la notation 18/18),\n"
        "la dette du quatorzième arbre nommée — la cérémonie d'ère du TGN précède tout\n"
        "build. \\\\\n"
        "\\end{longtable}",
    ),
])

# ================================================================ cover.html
echecs += remplace("cover.html", [
    (
        '<div class="label">Sp&eacute;cification technique &middot; Version 0.7.0</div>',
        '<div class="label">Sp&eacute;cification technique &middot; Version 0.8.0</div>',
    ),
    (
        "        Consolidation du programme d&rsquo;apr&egrave;s M7 (D160)&nbsp;: le jalon\n"
        "        M8 — syscalls directs (domaine sys) — est franchi (finale 0.9.0 scell&eacute;e\n"
        "        sur run terrain vert recoup&eacute; 30/30)&nbsp;; le jalon M9 — TLS 1.3 pur en\n"
        "        blocs scell&eacute;s (domaine tls13, &egrave;re 1.0.0) — est ouvert&nbsp;:\n"
        "        couche I compl&egrave;te, 28 sp&eacute;cifications. Le sceau de\n"
        "        l&rsquo;Intention porte d&eacute;sormais TREIZE arbres, ses c&eacute;r&eacute;monies\n"
        "        d&egrave;re (M8 puis M9) pass&eacute;es sur pi&egrave;ces — garde 13/13.\n"
        "        M0&ndash;M8 franchis, M9 ouvert. Hi&eacute;rarchie inchang&eacute;e&nbsp;:\n"
        "        S&eacute;curit&eacute; &gt; Performance &gt; Optimisation &gt; Co&ucirc;t en\n"
        "        tokens.",
        "        Consolidation du programme d&rsquo;apr&egrave;s M9 (D170/D171)&nbsp;: le jalon\n"
        "        M9 — TLS 1.3 pur en blocs scell&eacute;s — est FRANCHI (finale 1.0.0\n"
        "        scell&eacute;e sur run terrain recoup&eacute; 34/34&nbsp;; LA SESSION R&Eacute;ELLE&nbsp;:\n"
        "        la ligne applicative chiffr&eacute;e avec un serveur r&eacute;el). LE TEST\n"
        "        GRANDEUR NATURE est ouvert (M10)&nbsp;: &laquo;&nbsp;Loupe&nbsp;&raquo;,\n"
        "        l&rsquo;&eacute;diteur hexad&eacute;cimal au panneau d&rsquo;empreintes — les 18\n"
        "        blocs not&eacute;s-mesur&eacute;s-prouv&eacute;s&nbsp;; le kit attend la\n"
        "        c&eacute;r&eacute;monie d&rsquo;&egrave;re (le 14e arbre). M0&ndash;M9 franchis,\n"
        "        M10 ouvert. Hi&eacute;rarchie inchang&eacute;e&nbsp;: S&eacute;curit&eacute; &gt;\n"
        "        Performance &gt; Optimisation &gt; Co&ucirc;t en tokens.",
    ),
    (
        "c&eacute;r&eacute;monies et kit du terrain&nbsp;: jalons M0&ndash;M9</div>",
        "c&eacute;r&eacute;monies et kit du terrain&nbsp;: jalons M0&ndash;M10</div>",
    ),
    (
        "        <span>Document normatif &middot; s&eacute;rie TRIADE &middot; r&eacute;vision v0.7.0 (D169)</span>\n"
        "        <span>5 novembre 2026</span>",
        "        <span>Document normatif &middot; s&eacute;rie TRIADE &middot; r&eacute;vision v0.8.0 (D176)</span>\n"
        "        <span>8 novembre 2026</span>",
    ),
])

# ============================================================== merge_cover.py
echecs += remplace("merge_cover.py", [
    (
        "Miroir de scripts/spec_v061/merge_cover.py : normalisation A4 stricte de la",
        "Miroir de scripts/spec_v070/merge_cover.py : normalisation A4 stricte de la",
    ),
    (
        '    "/Title": "Protocole TRIADE v0.7.0 — spécification technique",',
        '    "/Title": "Protocole TRIADE v0.8.0 — spécification technique",',
    ),
    (
        '    "/Creator": "TRIADE — chaîne LaTeX/Tectonic (D25/D81/D133/D137/D169)",',
        '    "/Creator": "TRIADE — chaîne LaTeX/Tectonic (D25/D81/D133/D137/D169/D176)",',
    ),
])

if echecs:
    print(f"[revision-v080-tex] ÉCHEC — {len(echecs)} ancrage(s) fautif(s), RIEN n'est écrit :")
    for e in echecs:
        print(f"  ✗ {e}")
    sys.exit(1)
print("[revision-v080-tex] PASSÉ — main (4), sec-a (1), sec-c (1), sec-cf (2), "
      "sec-d (8), cover (4), merge (3) : 23 remplacements assertés.")
