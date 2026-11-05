#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""revision_v070_tex.py — les éditions LaTeX de la chaîne spec_v070 (miroir de
revision_v070_md.py) : axes (§ 12), sceau (§ 12.4), cérémonies (§ 13.1 + la
NOUVELLE § 13.5), profils (§ 11), jalons (M5-M7 constatés + M8/M9), la
correspondance v0.6.1 → v0.7.0 NOUVELLE, le journal des décisions (synthèse
v0.7.0) et l'annexe décisionnelle (D160–D169). Chaque ancrage est ASSERTÉ
(trouvé UNE fois) — un ancrage fautif = ÉCHEC NOMMÉ, rien n'est écrit.
"""
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
CH = REPO / "scripts" / "spec_v070"


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

# ================================================================ sec-cf.tex
# NOTE : l'édition (a) [axe 3 de la table des axes] a déjà été appliquée au
# fichier — elle est OMISE ici (le compte d'ancrages s'en souvient).
echecs += remplace("sec-cf.tex", [
    # (b) § 12.4 — l'ouverture du sceau
    (
        "Dix arbres de couche I vivent sous le sceau — les neuf lignées existantes \\emph{plus}\n"
        "l'arbre des axes lui-mêmes (\\code{v06/I}) : la spécification qui définit le sceau est la\n"
        "première couche I qu'il garde.",
        "Treize arbres de couche I vivent sous le sceau — les lignées m0 à m8 (le domaine\n"
        "\\code{sys} depuis l'ère M8), l'arbre \\code{tls13} (le domaine TLS 1.3 pur depuis\n"
        "l'ère M9), \\code{demo}, \\code{terrain}, et l'arbre des axes lui-mêmes\n"
        "(\\code{v06/I}) : la spécification qui définit le sceau est la première couche I\n"
        "qu'il garde. Chaque ère qui ouvre un arbre nomme sa dette de cérémonie à la\n"
        "naissance (D166, règle 8) : le registre figé étendu et l'arbre neuf exigent la clé\n"
        "hors-ligne avant tout build — la charge se prépare au geste qui sert la main du\n"
        "développeur (D168), et la continuité de la clé se prouve par le déterminisme\n"
        "Ed25519 (D163) : re-signer les arbres inchangés redonne exactement les signatures\n"
        "déposées.",
    ),
    # (c) § 13.1 — la table des cérémonies
    (
        "vérifiée AVANT écriture) ; \\code{verifier} & dix arbres VERTS, code 0 ; commit poussé \\\\",
        "vérifiée AVANT écriture) ; \\code{verifier} & treize arbres VERTS, code 0 ; commit poussé \\\\",
    ),
    # (d) § 13.5 NOUVELLE — entre la preuve terrain et la frontière des secrets
    (
        "\\subsection{La frontière des secrets — git, \\code{.keys}, sachet}\\label{sec:frontiere}",
        "\\subsection{Les cérémonies d'ère du sceau de l'Intention (5 novembre 2026)}\\label{sec:ceremoniesere}\n"
        "\n"
        "Le sceau a traversé deux cérémonies d'ère en un jour, chacune née d'un garde qui\n"
        "refusait. \\textbf{Ère M8} : l'ouverture du domaine \\code{sys} avait étendu le\n"
        "registre figé m0 et créé l'arbre m8 — le garde a nommé la dette AVANT tout build\n"
        "(D162 : un diff d'intention non signé ; la clé hors-ligne du développeur requise,\n"
        "le laboratoire ne signe jamais à sa place) ; le kit de cérémonie servi au dossier\n"
        "\\code{/Cérémonie} du Drive (la remise, le LISEZMOI pas à pas, la règle d'or\n"
        "« JAMAIS generer »), la cérémonie passée sur pièces : douze arbres, les dix\n"
        "inchangés rendant les MÊMES signatures que celles du 04/11 (la preuve D163 de la\n"
        "réutilisation de la clé, sans jamais voir la clé privée), le garde repassé VERT\n"
        "12/12 — puis le build \\code{0.9.0-dev.1} né, déterministe d'un poste à l'autre.\n"
        "\\textbf{Ère M9} : la dette fut nommée À LA NAISSANCE (D166, règle 8) ; le geste\n"
        "des 24 spécifications ayant bougé l'arbre, la charge fut RÉGÉNÉRÉE au geste de la\n"
        "cérémonie (D168 : la charge de l'ouverture était périmée — une remise signée\n"
        "dessus aurait laissé l'arbre divergé APRÈS installation) ; le développeur signa\n"
        "hors ligne la remise de TREIZE arbres et déposa \\code{signatures-I.txt} et\n"
        "\\code{cle-publique-I.txt} au coffre \\code{/test} ; le laboratoire rapatrie,\n"
        "recoupe — la clé déposée égale l'ancre \\code{173fae9c…}, les ONZE arbres\n"
        "inchangés rendent les signatures de l'ère M8, m0 re-signé, tls13 arbre neuf, les\n"
        "empreintes vivantes égales la remise, chaque signature vérifiée Ed25519 — puis\n"
        "installe canoniquement (tout vérifié AVANT toute écriture) et le garde est\n"
        "repassé VERT 13/13, l'état « reelle » tenant. La règle qui en découle : la\n"
        "cérémonie d'ère n'est pas une formalité de documentation — c'est le geste qui\n"
        "rend le build de l'ère possible, et il suit le calendrier du garde, jamais\n"
        "l'inverse.\n"
        "\n"
        "\\subsection{La frontière des secrets — git, \\code{.keys}, sachet}\\label{sec:frontiere}",
    ),
])

# ================================================================= sec-c.tex
echecs += remplace("sec-c.tex", [
    # les domaines du programme d'après M7 sur le profil primaire
    (
        "\\paragraph{Profil primaire, ABI Microsoft x64.} Arguments en RCX, RDX, R8, R9 puis la",
        "\\paragraph{Les domaines du programme d'après M7 (D160).} Deux domaines s'ajoutent\n"
        "sur le profil primaire : \\code{sys} (M8 — les syscalls directs, balise \\code{0.9.0} :\n"
        "le SSN lu de l'EAT de \\code{ntdll}, jamais un octet de code) et \\code{tls13} (M9 —\n"
        "TLS 1.3 pur, ère \\code{1.0.0}) ; chacun est une lignée de couche I à part entière\n"
        "sous le sceau (§\\ref{sec:sceauI}) et s'ajoute au profil sans le modifier —\n"
        "l'universalité demeure structurelle.\n"
        "\n"
        "\\paragraph{Profil primaire, ABI Microsoft x64.} Arguments en RCX, RDX, R8, R9 puis la",
    ),
])

# ================================================================= sec-d.tex
echecs += remplace("sec-d.tex", [
    # (a) le titre des jalons
    (
        "\\section{Critères d'acceptation des jalons M0 à M7}\\label{sec:jalons}",
        "\\section{Critères d'acceptation des jalons M0 à M9}\\label{sec:jalons}",
    ),
    # (b) l'intro — dix jalons
    (
        "Huit jalons, chacun avec des critères de sortie mesurables",
        "Dix jalons, chacun avec des critères de sortie mesurables",
    ),
    # (c) M5 franchi
    (
        "dans \\code{PLAN\\_MILESTONES.md} & \\textbf{ouvert} 31/10/2026 (D133) \\\\",
        "dans \\code{PLAN\\_MILESTONES.md} & \\textbf{franchi} 04/11/2026, \\code{0.6.0} (Entrée 143, D148 : critère (b) de D136 vert sur pièces au run e4 ; le chantier (c) refermé au M6 sur le profil Linux) \\\\",
    ),
    # (d) M6 franchi
    (
        "I} ; parité inter-profils vérifiée ; même oracle vert sur les deux profils & à venir \\\\",
        "I} ; parité inter-profils vérifiée ; même oracle vert sur les deux profils & \\textbf{franchi} 05/11/2026, \\code{0.7.0} (Entrée 149, D154 : run terrain WSL2 vert sur pièces, recoup labo 22/22 — le noyau de la machine du développeur distinct de celui du labo) \\\\",
    ),
    # (e) M7 franchi + les lignes M8 et M9
    (
        "multi-profils vérifié & à venir \\\\",
        "multi-profils vérifié & \\textbf{franchi} 05/11/2026, \\code{0.8.0} (Entrée 155 : run terrain M7-(d) vert sur pièces, recoup labo 29/29, export multi-profils de bout en bout — l'universalité démontrée : win \\code{0.6.0} / linux \\code{0.7.0} / riscv \\code{0.8.0}) \\\\\n"
        "M8 — syscalls directs (domaine \\code{sys}) & la charte à huit règles et les spécifications sys-01…03 écrites-avant-code ; le harnais sur fixtures \\code{ntdll} synthétiques (le labo ne connaît jamais le SSN du terrain) ; le motif du stub vérifié avant toute extraction ; le run terrain sur le VRAI \\code{ntdll} — la même observable par les DEUX chemins ; la cérémonie de l'ère avant le build & \\textbf{franchi} 05/11/2026, \\code{0.9.0} (Entrées 156--164, D160--D165 : harnais 61 verts ; cérémonie de l'ère passée 12/12 ; run terrain m8d vert — 35 verts / 0 échec, la twin octet pour octet, le refus $-4$ du stub crocheté ; recoup labo 30/30 ; finale scellée sur recoup exigé comme pièce) \\\\\n"
        "M9 — TLS 1.3 pur (domaine \\code{tls13}) & la charte à huit règles et les 28 spécifications en six familles écrites-avant-code ; les primitives aux vecteurs officiels (FIPS 180-4, RFC 2104/4231, RFC 5869, RFC 7748, SP 800-38D) ; la poignée rejouée sur le transcript RFC 8448 ; le socle socket par syscalls directs (sys-04+) ; la cérémonie de l'ère avant \\code{construire()} ; la session réelle — la ligne applicative chiffrée & \\textbf{ouvert} 05/11/2026 (D166) — couche I complète (28 spécifications, l'instrument 117 verts, D167) ; cérémonie de l'ère passée le 05/11 (13 arbres, garde 13/13) ; chantiers (b) notation, (c) harnais RFC 8448, (d) socle socket, (e) build \\code{1.0.0-dev.1}, (f) terrain $\\to$ finale \\code{1.0.0} \\\\",
    ),
    # (f) le paragraphe de clôture des jalons
    (
        "variable ; la suite de conformité par profil en est désormais le critère d'acceptation\n"
        "explicite.",
        "variable ; la suite de conformité par profil en est désormais le critère d'acceptation\n"
        "explicite. M8 et M9 sont les additions mesurées du programme d'après M7 (D160) : la\n"
        "fondation d'abord — le domaine \\code{sys} est la condition d'une pile TLS 1.3 qui\n"
        "n'émettrait plus par l'IAT userland ; chaque famille s'appuie sur les résultats\n"
        "mesurés de la précédente.",
    ),
    # (g) le paragraphe « Ouverture de M5 » devient le programme d'après M7
    (
        "\\paragraph{Ouverture de M5 (D133).} Le jalon de l'outil complet s'ouvre sur trois",
        "\\paragraph{Le programme d'après M7 (D160).} La clôture v0.6.1 tenait les additions\n"
        "mesurées « hors périmètre courant » ; la v0.7.0 lève la clause pour les deux\n"
        "premières familles, sur résultats mesurés. \\emph{M8, les syscalls directs} (domaine\n"
        "\\code{sys}) : la charte à huit règles — le SSN est une donnée, jamais un octet de\n"
        "code ; le motif du stub est vérifié avant toute extraction ; un stub divergent est\n"
        "un refus nommé — et la preuve d'observable : la MÊME ligne émise par les deux\n"
        "chemins (l'IAT \\code{kernel32} de hello-02 et le syscall direct \\code{NtWriteFile}\n"
        "de sys-03), comparées octet pour octet au fixture. \\emph{M9, TLS 1.3 pur} (domaine\n"
        "\\code{tls13}, ère 1.0.0) : la grande œuvre de la souveraineté complète — la\n"
        "cryptographie de session sans délégation, la couche I complète (28 spécifications,\n"
        "six familles), la cérémonie d'ère passée (13 arbres, garde 13/13). L'ordre est la\n"
        "fondation d'abord : une pile TLS pure qui émettrait encore par l'IAT userland\n"
        "garderait la surface de hook qu'elle prétend éliminer.\n"
        "\n"
        "\\paragraph{Archivé (D133, pour mémoire).} Le jalon de l'outil complet s'ouvrit sur trois",
    ),
    # (h) la correspondance v0.6.1 → v0.7.0 NOUVELLE (après les rejets v0.6.1)
    (
        "\\section{Journal des décisions}\\label{sec:decisions}",
        "\\subsection{Correspondance v0.6.1 $\\to$ v0.7.0}\\label{sec:evolutions070}\n"
        "\n"
        "\\begin{table}[htbp]\n"
        "\\centering\\small\n"
        "\\caption{Les évolutions de la v0.7.0, tracées depuis la v0.6.1 (D169).}\n"
        "\\label{tab:correspondance070}\n"
        "\\begin{tabularx}{\\textwidth}{@{}l Y Y l@{}}\n"
        "\\toprule\n"
        "\\textbf{Évolution} & \\textbf{En v0.6.1} & \\textbf{En v0.7.0} & \\textbf{Statut} \\\\\n"
        "\\midrule\n"
        "Programme d'après M7 & clause de clôture : syscalls directs et TLS 1.3 pur « hors\n"
        "périmètre courant » & le programme D160 entre en spécification : la clause est\n"
        "LEVÉE NOMMÉMENT pour les deux premières familles — M8 (domaine \\code{sys})\n"
        "franchi, M9 (domaine \\code{tls13}) ouvert ; les profils additionnels demeurent\n"
        "hors périmètre & révisé (D160, D166) \\\\\n"
        "Sceau de l'Intention & dix arbres sous le sceau & treize arbres (m0--m8, tls13,\n"
        "demo, terrain, v06) ; les cérémonies d'ère entrent au protocole : la dette nommée\n"
        "à la naissance (D166 règle 8), la charge préparée au geste qui sert la main\n"
        "(D168), la continuité de clé prouvée par le déterminisme Ed25519 (D163) & étendu\n"
        "(D162, D166, D168) \\\\\n"
        "État des jalons & M0--M6 franchis, M7 ouvert & M0--M8 franchis (balises 0.2.0 à\n"
        "0.9.0), M9 ouvert — la cérémonie de l'ère M9 passée (garde 13/13) & constaté\n"
        "(Entrées 155--168) \\\\\n"
        "Chaîne PDF & spec\\_v061 & chaîne spec\\_v070 ; l'archive v0.6.1 demeure (dernier\n"
        "build consigné : sha256 \\code{4aac10f1…}, 984 555 o) & révisé (D169) \\\\\n"
        "\\bottomrule\n"
        "\\end{tabularx}\n"
        "\\end{table}\n"
        "\n"
        "\\paragraph{Modifications explicitement rejetées (v0.7.0).} Réviser la spécification\n"
        "à chaque franchissement de jalon — rejeté : le versionnement suit les RÉVISIONS,\n"
        "jamais les franchissements (l'état des jalons vit aux sources de travail,\n"
        "régénérées à chaque geste ; la v0.7.0 consolide un PROGRAMME, pas un simple\n"
        "constat). Signer les sources \\code{docs/} sous le sceau courant — rejeté : le\n"
        "modèle par-version demeure (\\code{v06/I/README.md} § 1). Ouvrir les profils\n"
        "additionnels (\\code{aarch64-macos-macho}, \\code{wasm32-wasi}) dans la même\n"
        "révision — rejeté : chacun répétera M6/M7 sur résultats mesurés, hors périmètre.\n"
        "Fusionner les cérémonies d'ère dans la cérémonie CF3 — rejeté : trois gardes,\n"
        "trois menaces ; le sceau garde l'intention, le coffre garde les secrets.\n"
        "\n"
        "\\section{Journal des décisions}\\label{sec:decisions}",
    ),
    # (i) la synthèse du journal des décisions — la phrase v0.7.0 en tête
    (
        "Le journal complet vit dans \\code{docs/DECISIONS.md} du dépôt du projet. Synthèse :",
        "Le journal complet vit dans \\code{docs/DECISIONS.md} du dépôt du projet. La\n"
        "v0.7.0 consolide le programme d'après M7 : D160 (l'ordre des familles — la\n"
        "fondation d'abord), D162/D163 (la cérémonie de l'ère M8, la continuité de clé par\n"
        "le déterminisme Ed25519), D165 (la finale d'une ère se scelle sur le recoup\n"
        "exigé comme pièce), D166 (l'ouverture M9 — TLS 1.3 pur, la dette de cérémonie\n"
        "nommée à la naissance), D167 (les 28 spécifications avant tout octet de\n"
        "notation), D168 (la charge se prépare au geste de la cérémonie) et D169 (la\n"
        "présente consolidation). Synthèse des débuts :",
    ),
    # (j) l'annexe décisionnelle — les lignes D160 à D169
    (
        "explicitement invalidée ; la chaîne de migration demeure disponible ; le coffre réel\n"
        "reste CF3. \\\\",
        "explicitement invalidée ; la chaîne de migration demeure disponible ; le coffre réel\n"
        "reste CF3. \\\\\n"
        "D160 & L'ère d'après M7 & l'ordre des familles est syscalls directs $\\to$ TLS 1.3\n"
        "pur $\\to$ profils : la fondation I/O d'abord ; le jalon M8 naît sur le profil win\n"
        "(domaine \\code{sys}). \\\\\n"
        "D162 & La cérémonie d'ère avant tout build & le garde-sceau NOMME la dette\n"
        "(registre étendu non re-signé, arbre neuf) ; la table du sceau étendue à m8. \\\\\n"
        "D163 & Continuité de clé par le déterminisme Ed25519 & re-signer un arbre inchangé\n"
        "redonne exactement la signature déposée : la preuve de la réutilisation de la\n"
        "clé, sans jamais voir la clé privée. \\\\\n"
        "D165 & La finale d'une ère se scelle sur le recoup exigé comme pièce & le scellage\n"
        "REFUSE sans le verdict du recoup vert ; le scellage est un fait de carte,\n"
        "l'artefact ne bouge jamais. \\\\\n"
        "D166 & La seconde famille ouverte : TLS 1.3 pur & le jalon M9, le domaine\n"
        "\\code{tls13}, l'ère 1.0.0 ; la dette de cérémonie nommée à la naissance. \\\\\n"
        "D167 & Le chantier M9-(a) clos sur les 28 spécifications & la couche I complète\n"
        "avant tout octet de notation ; les constantes du plan dérivées par arithmétique. \\\\\n"
        "D168 & La charge de cérémonie se prépare au geste de la cérémonie & la charge de\n"
        "l'ouverture était périmée par le geste des 24 specs ; l'ouverture annonce, la\n"
        "cérémonie exige. \\\\\n"
        "D169 & La consolidation v0.7.0 & le programme d'après M7 entre en spécification :\n"
        "M8 franchi, M9 ouvert, le sceau à treize arbres, les cérémonies d'ère au\n"
        "protocole ; la clause « hors périmètre courant » levée pour les deux premières\n"
        "familles. \\\\",
    ),
])

if echecs:
    print(f"[revision-v070-tex] ÉCHEC — {len(echecs)} ancrage(s) fautif(s), RIEN n'est écrit :")
    for e in echecs:
        print(f"  ✗ {e}")
    sys.exit(1)
print("[revision-v070-tex] PASSÉ — sec-cf (3), sec-c (1), sec-d (10) : 14 remplacements assertés.")
