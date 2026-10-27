#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Révision v0.5.0 de docs/PROTOCOLE_TRIADE.md (source de vérité).

Chaque remplacement est vérifié (assert) — échec bruyant plutôt que silence.
"""

from pathlib import Path

P = Path("/home/z/my-project/triade/docs/PROTOCOLE_TRIADE.md")
s = P.read_text(encoding="utf-8")


def remplace(ancien: str, nouveau: str, occurrence: int = 1):
    global s
    n = s.count(ancien)
    if n == 0:
        # idempotence : le remplacement est-il déjà en place ?
        marqueur = nouveau.strip().splitlines()[0][:60]
        assert marqueur in s, f"introuvable et absent : {ancien[:80]!r} / {marqueur!r}"
        return
    s = s.replace(ancien, nouveau, occurrence)


# ---------------------------------------------------------------- 1. Titre + en-tête
remplace(
    "# PROTOCOLE TRIADE v0.4.0 — Spécification technique",
    "# PROTOCOLE TRIADE v0.5.0 — Spécification technique",
)
remplace(
    "> Source de travail faisant autorité pour la v0.4.0. Les archives formelles des versions\n"
    "> précédentes demeurent : `docs/Protocole_TRIADE_v0.3_Specification.pdf` (v0.3),",
    "> Source de travail faisant autorité pour la v0.5.0. Les archives formelles des versions\n"
    "> précédentes demeurent : `docs/Protocole_TRIADE_v0.4.0_Specification.pdf` (v0.4.0),\n"
    "> `docs/Protocole_TRIADE_v0.3_Specification.pdf` (v0.3),",
)
remplace(
    "> sources au stamp du dernier build et reconstruit avant chaque sauvegarde (`sync_backup.sh`).\n"
    "> La v0.4.0 est la première version numérotée à trois segments : la numérotation des\n"
    "> révisions du protocole s'aligne sur le schéma de pré-versions qu'elle définit elle-même\n"
    "> (§ 9) — l'édition académique « v0.4 » (D18) restait un document, le noyau normatif v0.3\n"
    "> inchangé ; la présente révision est le protocole.",
    "> sources au stamp du dernier build et reconstruit avant chaque sauvegarde (`sync_backup.sh`).\n"
    "> La v0.5.0 est la révision du retour du terrain : les jalons M0, M1 et M2 sont franchis\n"
    "> sur validations terrain Windows 11 (balises finales 0.2.0 et 0.3.0), et la campagne M2\n"
    "> — huit classes de défauts invisibles à l'émulation nommées en huit lectures de\n"
    "> journal — devient norme (§ 8.4, § 8.5).",
)
remplace(
    "- Version : v0.4.0 — gouvernance vérifiée : couche I normalisée, menace étendue, R10 renforcée, R11 ajoutée, conformité par profil, traçabilité et tableau de bord\n- Date : 26 octobre 2026",
    "- Version : v0.5.0 — révision du retour du terrain : validation terrain normée (boucle d'évidence), taxonomie étendue X1–X8, jalons M0–M2 constatés, budgets mesurés\n- Date : 27 octobre 2026",
)

# ---------------------------------------------------------------- 2. Vision : paragraphe v0.5.0
i = s.find("La v0.4.0 tire les enseignements de la première validation à l'échelle")
assert i > 0, "paragraphe v0.4.0 introuvable"
fin = s.find("hors périmètre de preuve.", i) + len("hors périmètre de preuve.")
s = s[:fin] + (
    "\n\nLa v0.5.0 est la révision du retour du terrain. Les jalons M0 (chaîne artefact), M1\n"
    "(mini-libc scellée) et M2 (patch à chaud en production, avec retour arrière) sont franchis\n"
    "— chacun sur validation terrain Windows 11, chacun scellé par une balise finale immuable\n"
    "(0.2.0, 0.3.0). La campagne M2 a coûté huit classes de défauts invisibles à l'émulation\n"
    "(§ 8.5) — le prix d'une leçon : un oracle valide un artefact contre un modèle\n"
    "d'environnement, et la complétude du modèle ne se démontre qu'en exécutant le binaire sur\n"
    "le système réel. Ce que le terrain a appris devient norme : la boucle d'évidence (§ 8.4),\n"
    "la taxonomie X, l'instrumentation contractualisée — et l'ouverture du jalon M3, contrats\n"
    "renforcés sur entrées non fiables."
) + s[fin:]

# ---------------------------------------------------------------- 3. § 1.4
remplace(
    "à l'exécution ; la hiérarchie de la fonction objectif est inchangée.\n\n## 2. La couche I",
    "à l'exécution ; la hiérarchie de la fonction objectif est inchangée.\n\n"
    "### 1.4 Ce que change la v0.5.0\n\n"
    "Huit évolutions, toutes tracées dans la correspondance (§ 17.3) et le journal des versions\n"
    "(§ 19), toutes rattachées aux décisions D26 à D45 : la validation terrain devient une\n"
    "couche de vérification normée — boucle d'évidence, journal d'exécution, instrumentation\n"
    "contractualisée, diff chirurgical (§ 8.4) ; la taxonomie des défauts s'étend des classes T\n"
    "(contrat non écrit) aux classes X — défauts invisibles à l'émulation, huit classes nommées\n"
    "par la campagne M2 (§ 8.5) ; l'état des jalons est constaté — M0, M1 et M2 franchis sur\n"
    "validations terrain Windows 11, balises finales 0.2.0 et 0.3.0 posées (§ 16) ; le budget\n"
    "de localisation est corrigé à 64 tokens (D31) et les budgets affichent leurs valeurs\n"
    "mesurées (§ 12, § 15.2) ; les volumes d'oracle effectifs sont consignés ; les preuves\n"
    "terrain sont archivées brutes avec leurs empreintes ; le corpus de démonstration (huit\n"
    "itérations instrumentées) devient l'occurrence de référence de la méthode ; le jalon M3\n"
    "est ouvert — contrats renforcés sur entrées non fiables et fuzzing à propriétés (D45).\n"
    "Aucune règle n'est modifiée ; aucune couche n'est ajoutée à l'exécution ; la hiérarchie de\n"
    "la fonction objectif est inchangée.\n\n## 2. La couche I",
)

# ---------------------------------------------------------------- 4. § 8 : intro + 8.4 + 8.5
remplace(
    "Elle repose sur trois piliers, complétés en v0.4.0 par la\n"
    "couverture des vecteurs, la suite de conformité par profil et la parité inter-profils\n"
    "(§ 8.1 à § 8.3).",
    "Elle repose sur trois piliers, complétés en v0.4.0 par la\n"
    "couverture des vecteurs, la suite de conformité par profil et la parité inter-profils\n"
    "(§ 8.1 à § 8.3), puis en v0.5.0 par la validation terrain normée (§ 8.4) et la taxonomie\n"
    "des défauts invisibles à l'émulation (§ 8.5).",
)

remplace(
    "un bytecode portable trahirait la fonction objectif Performance (rejet consigné, D14 et\n§ 17.2).",
    "un bytecode portable trahirait la fonction objectif Performance (rejet consigné, D14 et\n"
    "§ 17.2).\n\n"
    "### 8.4 La validation terrain — la boucle d'évidence\n\n"
    "La v0.5.0 élève la validation terrain au rang de couche de vérification normée (D43). Le\n"
    "principe est né d'un constat structurel : l'oracle différentiel exécute le binaire contre\n"
    "un **modèle** de l'environnement — chargeur, ABI, sémantique des API, protections\n"
    "mémoire. Un binaire peut donc être exact au sens du round-trip, intègre au sens de la\n"
    "porte R10, conforme au sens de la suite du profil, vert au sens de l'oracle — et mourir\n"
    "au premier appel sur machine réelle, parce que le modèle était plus pauvre que la\n"
    "réalité. Les jalons M1 et M2 en ont fourni la preuve expérimentale : huit classes de\n"
    "défauts ainsi invisibles (§ 8.5) n'ont été révélées que par l'exécution terrain.\n\n"
    "La boucle d'évidence comporte cinq éléments normés :\n\n"
    "1. **Le journal d'exécution** — l'artefact livré écrit ses preuves au fil de l'eau\n"
    "   (fichier à côté de l'exécutable, ligne par ligne). La règle d'honnêteté est absolue :\n"
    "   une ligne n'est écrite qu'après la vérification de l'étape qu'elle atteste (memcmp\n"
    "   exact) — une ligne présente vaut preuve ; la dernière ligne visible localise toute\n"
    "   mortalité à l'intervalle près.\n"
    "2. **La lecture asymétrique** — le terrain retourne son verdict par un canal à faible\n"
    "   bande passante : le journal (éventuellement complété d'une capture). L'atelier\n"
    "   n'exige du terrain que ce document, jamais un diagnostic : la charge d'analyse reste\n"
    "   à l'agent.\n"
    "3. **L'instrumentation contractualisée** — quand l'intervalle de mortalité reste\n"
    "   aveugle, l'itération suivante embarque des sondes de trace aux frontières (D40) :\n"
    "   elles journalisent des faits (positions d'exécution, retours vérifiés), jamais un\n"
    "   succès non prouvé ; leur retrait après constat vert est promis dans la spécification\n"
    "   (D43 a honoré la promesse) et vérifié par l'oracle — le journal nominal redevient\n"
    "   exactement sa séquence de preuves, toute ligne parasite est un échec.\n"
    "4. **Le diff chirurgical** — chaque itération terrain ne modifie que les blocs révisés ;\n"
    "   l'audit d'itération vérifie mécaniquement qu'aucun octet hors des zones autorisées\n"
    "   (blocs révisés, chaînes, version, sommes) n'a bougé — l'héritage scellé reste\n"
    "   octet-identique (R7).\n"
    "5. **L'archive brute** — chaque journal terrain est archivé tel quel (octets d'origine,\n"
    "   encodage et CRLF compris) avec son empreinte : la preuve est le document, pas son\n"
    "   résumé.\n\n"
    "Le protocole est ensuite économique : huit lectures de journal ont suffi à nommer huit\n"
    "classes de défauts en deux jours (demo.1 à demo.8), et le dernier diagnostic a été obtenu\n"
    "sans run supplémentaire — par lecture statique des octets appuyée sur les preuves\n"
    "accumulées (D42). La contrepartie est la garantie de progression : chaque défaut nommé\n"
    "devient un vecteur de falsification permanent de l'oracle — le modèle d'environnement\n"
    "s'enrichit de chaque lecture terrain et ne peut plus régresser en silence.\n\n"
    "### 8.5 Taxonomie étendue — les défauts invisibles à l'émulation (X1–X8)\n\n"
    "Les classes T1–T6 (§ 3) classent les défauts de contrat non écrit : lisibles dans la\n"
    "spécification, corrigeables en écrivant le contrat. La campagne M2 a révélé une seconde\n"
    "famille, structurellement différente : des défauts dont ni la spécification, ni la\n"
    "notation, ni le round-trip, ni l'oracle ne parlent — parce que le modèle d'environnement\n"
    "de l'oracle était, sur un point précis, plus pauvre que le système réel. La v0.5.0 en\n"
    "fixe la taxonomie (D35–D43) :\n\n"
    "| Classe | Décision | Dimension du modèle défaillant | Défaut de référence | Garde permanente |\n"
    "|---|---|---|---|---|\n"
    "| X1 | D35 | sémantique du chargeur | `FirstThunk` ≠ slots appelés : le chargeur réel résout ailleurs que le code n'appelle — `call 0` au premier appel réseau | verrou « chargeur réel » : FirstThunk = slots appelés, contrôlé au build et par l'oracle |\n"
    "| X2 | D36 | lecture de structure | `RECT.top` lu comme largeur : spécification juste, octets faux — bloc jamais exécuté, shim témoin muet | coquille entière exécutée + invariant géométrique + falsification de l'octet |\n"
    "| X3 | D37 | canal de vérité | jumeau silencieux : le journal fichier vivait, l'écran restait vide — le défaut vivait dans la spécification elle-même | miroir universel : chaque ligne écrite écran puis fichier, les deux canaux contrôlés |\n"
    "| X4 | D38 | ABI caller-saved | dimensions relues dans des registres volatils après l'appel : un retour de syscall écrit RFLAGS dans r11 | clobber des volatiles à chaque retour simulé + falsification |\n"
    "| X5 | D39 | protections mémoire | phase de patch `PAGE_READWRITE` sans bit execute : DEP permanent x64, le fetch suivant faute | le shim applique les permissions réelles + falsification 0x40 → 0x04 |\n"
    "| X6 | D40 | écart émulation/terrain | défaut latent qu'aucune exécution n'avait déclenché : l'audit exhaustif était vert | sondes de trace aux frontières (§ 8.4), instrumentation contractualisée |\n"
    "| X7 | D41 | obligations ABI de l'appelant | zone d'accueil msx64 absente : l'appelé (/homeparams) écrit sur l'adresse de retour — le ret saute à 0x700 | shim /homeparams + audit systémique des sites d'appel + falsification |\n"
    "| X8 | D42 | état hérité | section critique exigée par un bloc scellé (P5) mais initialisée par un bloc orchestrateur retiré de l'hôte | shims à état + exécution réelle du bloc consommateur + contrôle post-run |\n\n"
    "Trois règles d'usage, miroir de celles de la taxonomie T. Premièrement, tout défaut\n"
    "terrain corrigé est classé T ou X au journal des décisions — la métrique « défauts\n"
    "ouverts par classe » du tableau de bord (§ 15.2) couvre désormais les deux familles.\n"
    "Deuxièmement, chaque classe X est gardée par une falsification : réintroduire le défaut\n"
    "doit faire échouer l'oracle — le modèle s'enrichit mais ne régresse jamais en silence.\n"
    "Troisièmement, la taxonomie est ouverte : une neuvième classe sera nommée X9 avec sa\n"
    "décision, jamais dissimulée dans un correctif muet.\n\n"
    "La lecture académique : un oracle différentiel valide la conformité d'un artefact à un\n"
    "modèle ; la validation terrain valide le modèle lui-même. Les deux couches sont\n"
    "complémentaires, non redondantes — l'oracle couvre l'espace des entrées à coût nul, le\n"
    "terrain couvre l'espace des environnements au coût d'un run. Le protocole exige les\n"
    "deux : R5 (vérifie-puis-écrit) pour la première, la boucle d'évidence (§ 8.4) pour la\n"
    "seconde.",
)

# ---------------------------------------------------------------- 5. § 15.2 : budget corrigé
remplace(
    "| Budgets tokens (localiser / éditer / ajouter) | ≤ 40 / 3 000 / 6 000 | instrumentation (à partir de M1) |",
    "| Budgets tokens (localiser / éditer / ajouter) | ≤ 64 / 3 000 / 6 000 | instrumentation — mesurés M1 : 51 / 719 / 1 088 (D31) |",
)

# ---------------------------------------------------------------- 6. § 16 : jalons constatés
remplace(
    "| Jalon | Capacité | Critères de sortie mesurables |\n|---|---|---|\n"
    "| M0 | Chaîne artefact | exécution sur Windows 11 ; round-trip 100 % ; carte v0 signée et vérifiée ; exécutable < 4 Kio ; R1-R3, R8-R9 dès le premier octet |\n"
    "| M1 | Blocs réutilisables | oracle 100 % sur la mini-libc ; première cristallisation ; adresses stables démontrées ; budgets tokens instrumentés (première mesure) |\n"
    "| M2 | Patch à chaud | remplacement du bloc d'écho en exécution, sans interruption ; rollback démontré ; taux de régression post-patch nul |\n"
    "| M3 | Entrées non fiables | un million de requêtes fuzzées sans crash ; proxy transparent ; contrats renforcés sur la surface de parsing |",
    "| Jalon | Capacité | Critères de sortie mesurables | Statut |\n|---|---|---|---|\n"
    "| M0 | Chaîne artefact | exécution sur Windows 11 ; round-trip 100 % ; carte v0 signée et vérifiée ; exécutable < 4 Kio ; R1-R3, R8-R9 dès le premier octet | **franchi** 26/10/2026 (D26) |\n"
    "| M1 | Blocs réutilisables | oracle 100 % sur la mini-libc ; première cristallisation ; adresses stables démontrées ; budgets tokens instrumentés (première mesure) | **franchi** 26/10/2026 — balise 0.2.0 (D32) |\n"
    "| M2 | Patch à chaud | remplacement du bloc d'écho en exécution, sans interruption ; rollback démontré ; taux de régression post-patch nul | **franchi** 27/10/2026 — balise 0.3.0, boucle § 5 démontrée sur machine réelle (D43) |\n"
    "| M3 | Entrées non fiables | un million de requêtes fuzzées sans crash ; proxy transparent ; contrats renforcés sur la surface de parsing | **ouvert** 27/10/2026 (D45) |",
)
remplace(
    "| M4 | Tunnel chiffré | HTTPS en transit via Schannel ; échec propre sur certificat invalide |\n"
    "| M5 | Outil complet | interception d'un flux navigateur en VM isolée ; patch à chaud du journal en production ; empreintes par build actives |\n"
    "| M6 | Portabilité inter-OS | profil `x86-64-linux-elf64` : suite de conformité verte ; **diff nul sur la couche I** ; parité inter-profils vérifiée (§ 8.3) ; même oracle vert sur les deux profils |\n"
    "| M7 | Portabilité inter-ISA | profil `riscv64-linux-elf64` : round-trip 100 % sur la nouvelle ISA ; patch à chaud conforme (scratch + `fence.i`) ; verrou croisé multi-profils ; export de continuité multi-profils vérifié |",
    "| M4 | Tunnel chiffré | HTTPS en transit via Schannel ; échec propre sur certificat invalide | à venir |\n"
    "| M5 | Outil complet | interception d'un flux navigateur en VM isolée ; patch à chaud du journal en production ; empreintes par build actives | à venir |\n"
    "| M6 | Portabilité inter-OS | profil `x86-64-linux-elf64` : suite de conformité verte ; **diff nul sur la couche I** ; parité inter-profils vérifiée (§ 8.3) ; même oracle vert sur les deux profils | à venir |\n"
    "| M7 | Portabilité inter-ISA | profil `riscv64-linux-elf64` : round-trip 100 % sur la nouvelle ISA ; patch à chaud conforme (scratch + `fence.i`) ; verrou croisé multi-profils ; export de continuité multi-profils vérifié | à venir |",
)
remplace(
    "M0 est le jalon existentiel — il prouve la chaîne notation, octets, exécutable, exécution\n"
    "sans compilateur. M2 est le jalon de vérité — le patch à chaud sur code en exécution a\n"
    "motivé l'architecture.",
    "M0 est le jalon existentiel — il prouve la chaîne notation, octets, exécutable, exécution\n"
    "sans compilateur ; il est franchi. M2 est le jalon de vérité — le patch à chaud sur code\n"
    "en exécution a motivé l'architecture ; il est franchi : la boucle complète (bascule\n"
    "pendant le trafic, vérification memcmp, retour arrière, re-vérification) a été\n"
    "démontrée sur machine réelle le 27 octobre 2026 (D43), au terme de la campagne\n"
    "d'instrumentation relatée en § 8.4 — huit itérations, huit classes de défauts nommées,\n"
    "zéro régression possible (chaque classe est gardée par une falsification).",
)

# ---------------------------------------------------------------- 7. § 17 : correspondance v0.5.0
remplace(
    "## 17. Correspondance v0.3 → v0.4.0",
    "## 17. Correspondance des versions",
)
remplace(
    "| Optimisation validée sans mesure | rejetée | R11 : hot path + mesure avant/après + contrat stable |\n\n## 18. Glossaire",
    "| Optimisation validée sans mesure | rejetée | R11 : hot path + mesure avant/après + contrat stable |\n\n"
    "### 17.3 Correspondance v0.4.0 → v0.5.0\n\n"
    "| # | Évolution | En v0.4.0 | En v0.5.0 | Statut |\n|---|---|---|---|---|\n"
    "| 1 | Validation terrain | constats dispersés au journal des décisions | couche normée : boucle d'évidence, journal d'exécution, sondes contractualisées, diff chirurgical (§ 8.4) | nouveau (D43) |\n"
    "| 2 | Taxonomie des défauts | classes T1–T6 (contrat non écrit) | + classes X1–X8, défauts invisibles à l'émulation (§ 8.5) | étendu (D35–D42) |\n"
    "| 3 | État des jalons | M0 planifié, M1-M7 à venir | M0, M1, M2 franchis — preuves terrain archivées (§ 16) | constaté (D26, D32, D43) |\n"
    "| 4 | Budgets de tokens | 40 / 3 000 / 6 000 (cibles) | 64 / 3 000 / 6 000 — corrigé et mesuré : 51 / 719 / 1 088 (D31) | corrigé (D31) |\n"
    "| 5 | Suite de conformité | définie (7 éléments, 124 contrôles) | exécutée à chaque scellage rc/final — 124/124 sur le profil primaire | mesuré (D39–D43) |\n"
    "| 6 | Volume d'oracle | 12 000 cas par bloc critique (référence) | campagnes effectives consignées : M1 76 010 cas, M2 50 533 cas, démo 86 cas | consolidé |\n"
    "| 7 | Preuves terrain | non normées | archives brutes (journaux octet-exacts, empreintes) référencées au journal des décisions | officialisé (D43) |\n"
    "| 8 | Fuzzing | mentionné (menace « fuzzing boîte noire », § 13.1) | jalon M3 ouvert : fuzzing à propriétés sur la surface d'entrées non fiables (D45) | structuré |\n\n"
    "### 17.4 Modifications explicitement rejetées (v0.5.0)\n\n"
    "Conformément au cahier de révision, les modifications suivantes ont été examinées et\n"
    "**rejetées, donc non appliquées** :\n\n"
    "| Modification | Verdict | Motif |\n|---|---|---|\n"
    "| Ajouter une règle R12 « validation terrain obligatoire » | rejetée | la boucle d'évidence découle de R5 et des critères de jalon ; une règle de plus diluerait le corpus sans rien exiger de nouveau |\n"
    "| Étendre le fuzzing à tous les blocs scellés | rejetée | M3 cible la surface d'entrées non fiables ; les blocs à appelants de confiance relèvent des vecteurs existants (§ 8.1) |\n"
    "| Reconstruire les artefacts scellés 0.2.0 / 0.3.0 pour la documentation | rejetée | les balises finales sont immuables (§ 9) ; la documentation cite les empreintes |\n"
    "| Fusionner les classes X dans les classes T (T7–T14) | rejetée | les deux familles appellent des remèdes distincts : écrire le contrat (T) contre enrichir le modèle d'environnement et falsifier (X) |\n\n"
    "## 18. Glossaire",
)

# ---------------------------------------------------------------- 8. Glossaire
remplace(
    "| Round-trip | Contrôle de fidélité : assemblage puis désassemblage d'un bloc, comparaison exacte |\n",
    "| Round-trip | Contrôle de fidélité : assemblage puis désassemblage d'un bloc, comparaison exacte |\n"
    "| Validation terrain | Exécution de l'artefact livré sur système réel, preuve archivée — valide le modèle d'environnement de l'oracle (§ 8.4) |\n"
    "| Journal d'exécution | Fichier de preuves écrit au fil de l'eau par l'artefact ; une ligne n'est écrite qu'après vérification de l'étape qu'elle atteste |\n"
    "| Sonde de trace | Instrumentation temporaire aux frontières d'un intervalle suspect : journalise des faits vérifiés ; retrait promis dans la spécification (D40, D43) |\n"
    "| Défaut invisible à l'émulation | Défaut dont le modèle d'environnement de l'oracle ne rend pas compte — classes X1–X8 (§ 8.5) |\n"
    "| Diff chirurgical | Itération terrain dont l'audit vérifie qu'aucun octet hors des zones autorisées n'a changé |\n"
    "| Fuzzing à propriétés | Génération d'entrées aléatoires contraintes, vérifiées par propriétés (jamais de crash, domaines de retour, bornes mémoire) — cœur du jalon M3 |\n",
)

# ---------------------------------------------------------------- 9. Journal des versions
remplace(
    "| v0.4.0 | 26 oct. 2026 |",
    "| v0.5.0 | 27 oct. 2026 | Révision du retour du terrain : validation terrain normée — boucle d'évidence, journal d'exécution, instrumentation contractualisée, diff chirurgical (D43) ; taxonomie étendue X1–X8 des défauts invisibles à l'émulation (D35–D42) ; jalons M0–M2 constatés franchis (balises 0.2.0 et 0.3.0 — D26, D32, D43) ; budget de localisation corrigé à 64 tokens et budgets mesurés (D31) ; ouverture du jalon M3 — contrats renforcés sur entrées non fiables, fuzzing à propriétés (D45). Aucune règle modifiée, aucune couche d'exécution ajoutée, hiérarchie inchangée |\n"
    "| v0.4.0 | 26 oct. 2026 |",
)

# ---------------------------------------------------------------- 10. Paragraphe de clôture
remplace(
    "La présente version fige les arbitrages nécessaires au démarrage du jalon M0, qui s'effectue\n"
    "sur le profil primaire.",
    "La présente version consigne l'état au passage de relais : jalons M0, M1 et M2 franchis\n"
    "sur validations terrain, jalon M3 ouvert (contrats renforcés sur entrées non fiables).",
)
remplace(
    "de gouvernance demeure : toute évolution invalide explicitement ce qu'elle remplace, et\n"
    "rien ne se change en silence.",
    "de gouvernance demeure : toute évolution invalide explicitement ce qu'elle remplace, et\n"
    "rien ne se change en silence — le terrain compris : chaque lecture d'exécution est une\n"
    "révision potentielle du modèle, et son enseignement se consigne (§ 8.4, § 8.5).",
)

# ---------------------------------------------------------------- 11. § 13.2 : état des jalons
remplace(
    "documentées dans l'édition académique (D18) : la généralité reste à établir par\n"
    "réplication, le cœur natif par les jalons M0 à M7.",
    "documentées dans l'édition académique (D18) : la généralité reste à établir par\n"
    "réplication, le cœur natif par les jalons M0 à M7 — dont M0, M1 et M2 sont désormais\n"
    "franchis (§ 16), preuves terrain archivées.",
)

P.write_text(s, encoding="utf-8")
print(f"PROTOCOLE_TRIADE.md révisé : {len(s.splitlines())} lignes")
