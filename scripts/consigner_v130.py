#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigner_v130.py — LES CONSIGNATIONS DE L'ÉDITION v0.13.0 (append-only) :
D190/D191/D192 au format normalisé (contexte, règles, alternatives rejetées,
frontières), l'Entrée 226 au journal, le bloc Task 133 au worklog."""
import pathlib

D = pathlib.Path("/home/z/my-project/triade/docs/DECISIONS.md")
J = pathlib.Path("/home/z/my-project/triade/docs/JOURNAL_TRAVAIL.md")
W = pathlib.Path("/home/z/my-project/triade/worklog.md")

DECISIONS = """

## D190 — LES CORRECTIONS DE L'ÉDITION v0.13.0 : LA LISTE EXHAUSTIVE D'INCOHÉRENCES VÉRIFIÉE UNE À UNE (le rapport de conformité joint aux livrables : chaque item de la commande tranché par le code sur pièces) ; LES STATISTIQUES REFORMULÉES (la règle de comptage opérationnelle des défauts échappés DÉFINIE en méthodes — les runs 6/7 à deux défauts comptés UNE fois chacun, le résidu [T0-PÉRIMÉ] du run 12 divulgué NON compté : une bannière de texte, aucune porte touchée ; l'IC95 % EXACT de 11/12 par Clopper-Pearson [0,615 ; 0,998] AVEC la réserve de non-indépendance des itérations séquentielles ; la cristallisation aux CARACTÉRISTIQUES OPÉRATIONNELLES P(sceller|q) = (1-q)^n — 3,1 %/0,098 % à q = 50 %, 95,1 %/90,4 % à q = 1 %, les quantiles unilatéraux exacts 1,87σ/3,10σ — les « α = 3,29e-2 / 1,08e-3 » de D189 étaient des RAPPORTS DE VRAISEMBLANCE (0,5/0,99)^n MAL ÉTIQUETÉS, les conversions sqrt(-2 ln p) retirées) ; LA NEUTRALITÉ DOCUMENTAIRE ARBITRÉE (l'anti-debug léger par mesure de temps DOCUMENTÉ HONNÊTEMENT dans les DEUX documents — la dissuasion, jamais la résistance ; le terrain M7 REQUALIFIÉ : qemu-riscv64 TCG au noyau réel, la réserve instrumentale D149 nommée, la sémantique matérielle I-cache de fence.i NON PROUVÉE sur silicium, jamais revendiquée ; RQ3 RECADRÉE : la quantification des GARANTIES SILENCIEUSES DU COMPILATEUR)

**Le contexte qui fonde la décision (11/11).** Le quatrième fichier d'instruction (Qwen_text_20261111_f3q3x9i7n.txt) : « produis l'édition v0.13.0 en appliquant les corrections suivantes, sans toucher aucun artefact scellé… et en consignant chaque changement au journal append-only ». Le laboratoire exécute la liste UNE À UNE — le rapport de conformité (preuves_v130/rapport_conformite_v130.txt) tranche chaque item sur pièces.

**Les règles.** (1) LES INCOHÉRENCES : les quatorze arbres signés (cohérence avec le garde 14/14) ; la référence au manuscrit accompagnant v0.13.0 ; le compte de lignes du journal UNIFIÉ en valeur exacte EXTRAITE (les macros de extraire_donnees_v130.py, régénérées à chaque passe — jamais un arrondi, jamais une divergence abstract/intro) ; « Fig. 5 » devient « Table 5 » ; la Data Availability aux archives v0.13.0 ; la note TOTAL/brouillons du tableau des budgets (8 774 + 5 099 = 13 873) ; le paragraphe de consolidation du spec ALIGNÉ sur D181 (DOUZE runs, la balise loupe 0.1.1 scellée) ; le tableau de menaces (« l'évolution du code volé est bloquée, son exécution ne l'est pas ») ; les renvois recalés (§ 3.5 les preuves renforcées, § 4.1 le modèle formel) ; l'en-tête de couverture « VERSION 0.9.0 » porté v0.13.0 (la dette d'identité de la chaîne, héritée de spec_v090). (2) LES STATISTIQUES : ce qui précède au titre — la règle de comptage DÉFINIE (l'unité du taux est le RUN ; kit et pièce comptés l'un et l'autre, le livrable est l'ensemble ; la [D54-QUATRIÈME] du run 7 est la quatrième manifestation de la classe de dérive de dépôt née à l'ère M4, pas une classe neuve). (3) LA NEUTRALITÉ : l'anti-debug documenté dans les deux documents (la spécification porte le mécanisme et son résiduel « assumé », le manuscrit ne dit plus « no anti-analysis » mais nomme le mécanisme et sa portée) ; le M7 dit l'émulation (le run terrain : la machine RÉELLE du développeur, WSL2, noyau et syscalls réels, l'ISA exécutée par l'instrument EMBARQUÉ qemu-riscv64 10.0.13 — la preuve du MÉCANISME vaut dans CE régime, le silicium demeure non éprouvé).

**Alternatives rejetées.** Retirer l'anti-debug de la spécification — rejeté : le mécanisme existe dans l'œuvre documentée, le retirer du document le falsifierait ; l'arbitrage D190 le documente honnêtement dans les DEUX. Corriger D189/D178 en place — rejeté : le journal est APPEND-ONLY, les décisions demeurent comme consignées, les corrections vivent en décisions nouvelles. Compter le résidu [T0-PÉRIMÉ] comme un onzième+ défaut fonctionnel — rejeté : aucune porte touchée, aucun contrat violé ; le divulguer sans le compter est la règle qui dit ce que le taux MESURE.

**Frontières.** AUCUN artefact scellé touché (loupe.exe c1115105…, proxy.exe 446279f3… INTACTS, le garde 14/14) ; aucune règle du cœur modifiée ; aucune couche d'exécution ajoutée ; les corrections vivent aux documents (manuscrit, spécification, md) et aux décisions nouvelles.

## D191 — LE BENCHMARK AUDITÉ : LE FACTEUR « 15,3× » DE v0.11.0 RETIRÉ COMME ARTEFACT DE PÉRIMÈTRE (l'instrument lisait le compteur de la FINALISATION SEULE au retour du pipeline — Emulation.appeler() REMET le compteur à zéro à chaque appel — comparé à l'OPÉRATION COMPLÈTE de la référence : 4 524 instructions « pour sha256(1024 o) » = 4,16 instructions/ronde sur 17 blocs × 64 rondes, SOUS tout minimum scalaire plausible [une ronde SHA-256 exige au minimum 2 additions, 2 sélections Ch/Maj et 2 chaînes sigma] ; le débit du même rapport — 31,0 ops/s pour la référence contre 27,4 pour les blocs « 15× plus efficaces » — trahissait déjà l'artefact : à émulateur constant, 15× moins d'instructions aurait donné 15× plus d'ops/s) ; LES CHIFFRES CORRIGÉS SUR PIÈCES (l'opération COMPLÈTE des blocs : init 12 + absorb 71 447 [16 invocations de tls13-02] + finaliser 4 524 [1 invocation] = 75 983 instructions, le condensé CONFRONTÉ à hashlib AVANT le comptage, les 17 invocations de compression CONFIRMÉES mécaniquement par le mécanisme du harnais, deux passes identiques ; contre gcc -O2 69 132 et -Os 77 505 au MÊME émulateur sur la MÊME entrée : la notation WYSIWYG est COMPÉTITIVE — −9 % en instructions contre -O2, +2 % contre -Os [elle DEVANCE -Os], 1,45× plus compacte que -O2 [1 021 contre 1 482 octets, tables comprises], MOINS compacte que -Os [548] ; SECOND ARTEFACT nommé : le « 5 436 o » de v0.11.0 était l'IMAGE ENTIÈRE de la référence [trois fonctions, toutes tables], pas la fonction) ; LA PARITÉ D'EXTENSIONS ISA : AUCUN des deux camps hors le baseline x86-64 (pas d'AVX, pas de SHA-NI ; gcc -O2 emploie 101 mouvements SSE2 du BASELINE pour ses tampons, la notation est GPR pure — l'écart rapporté SANS ajustement, la parité stricte GPR-à-GPR jamais revendiquée)

**Le contexte qui fonde la décision (11/11).** La commande exigeait l'audit du comptage (« 4,16 instr/ronde, sous le minimum scalaire plausible ; vérifier la parité d'extensions ISA ; si la parité n'est pas établie, retirer le facteur 15,3 de l'abstract et de la conclusion et consigner la dette »). L'audit (scripts/audit_benchmark_v130.py, rejouable) a établi le mécanisme de l'artefact, rejoué la mesure à périmètre correct et rapporté les chiffres corrigés TELS QUELS.

**Les règles.** (1) Le facteur 15,3× RETIRÉ du manuscrit (le § 3.5 réécrit avec le mécanisme de l'artefact ET les chiffres corrigés ; la conclusion porte la parité audité ; les QUATRE mentions résiduelles de « 15.3 » sont toutes en contexte de retrait). (2) Le manuscrit n'affirme que ce qui est re-mesuré : compétitive, jamais spectaculaire — « le prix de l'auditabilité directe est quasi nul, le gain spectaculaire n'existe pas ». (3) Les tailles AU BON PÉRIMÈTRE (le code de la FONCTION + la table K, jamais l'image entière). (4) La leçon consignée aux menaces à la validité : « l'audit de notre propre benchmark, qui a attrapé un artefact de périmètre gonflant une revendication quinze fois, est lui-même une preuve de cette classe de menace ».

**Alternatives rejetées.** Conserver le 15,3× avec une réserve — rejeté : un chiffre faux avec une réserve demeure un chiffre faux (la doctrine md5/aes de v0.11.0 : mieux aucun chiffre qu'un chiffre faux). Ajuster l'écart pour neutraliser les mouvements SSE2 — rejeté : la parité stricte n'est pas mesurée, l'affirmer serait la même faute une seconde fois. Publier les chiffres corrigés sans le mécanisme de l'artefact — rejeté : la correction se PUBLIE avec son pourquoi (la méthode appliquée à sa propre revendication).

**Frontières.** Aucun artefact scellé touché (les blocs tls13-01..04 INTACTS, la pièce inchangée) ; les sorties brutes de v0.11.0 DEMEURENT (les preuves ne se réécrivent jamais — l'erreur documentée, pas effacée) ; l'audit vit à preuves_v130/ avec ses sorties brutes.

## D192 — LA CONSÉQUENCE DE D81 AU MODÈLE DE MENACE ET LE KIT DE LA CÉRÉMONIE D183 PRÉPARÉ SANS L'APPLIQUER (le compte honnête : la phrase de contrôle au dépôt [D81, la décision active] + S_serrure en EN-TÊTE CLAIR du conteneur [moitié MACHINE de la dérivation de clé, par conception] = DEUX des trois éléments TRIVIALEMENT DISPONIBLES à quiconque lit le dépôt ; sous l'adversaire à seuil du modèle formel deux éléments ne donnent rien, mais le TROISIÈME — le média piègé — est le SEUL rempart de confidentialité restant, et les garanties d'intégrité [témoins d'époque, destruction sur falsification prouvée] portent la charge protectrice) ; LA FRONTIÈRE D105/D81 DU CLONE DU LABORATOIRE (les tests du labo tournent sur des CLONES TEMPORAIRES à phrases de TEST visiblement marquées — le conteneur réel n'est JAMAIS ouvert par un test, l'état « test » visible de D105 appliqué au coffre) ; LE KIT DE LA CÉRÉMONIE D183 (scripts/kit_ceremonie_d183/ : l'OUTIL au partage CF2 D120 TEL QUEL — decouper/reconstituer de v06/coffre_cf2.py, GF(2^8), JAMAIS une réécriture, la doctrine D185 —, étendu au partage BLOC PAR BLOC pour la phrase de longueur libre [part = en-tête public {longueur, indice x} + tranches de 32 o] ; l'AUTOTEST VERT exécuté au labo sur une PHRASE DE TEST PUBLIQUE : les C(5,3) = 10 combinaisons reconstituent EXACTEMENT, les C(5,2) = 10 paires sous le seuil rendent un déchet, une part seule ne porte rien ; le LISEZMOI pas à pas [la répétition générale, le découpage, la répartition des médias — au moins DEUX hors nuage —, la PREUVE DE RECONSTITUTION À FROID AVANT TOUT RETRAIT, la liste de contrôle du retrait en gestes humains, l'exercice périodique] ; le manifeste aux empreintes sha256 — le coffre réel INTACT, le geste appartient au développeur [D87 : la clé nulle phrase réelle ne traverse le bac à sable]) ; L'ÉTAT DE L'ART ÉTENDU (huit références VÉRIFIÉES DOI/arXiv — LLM Compiler [Cummins 2024, arXiv 2407.02524, prépublication 7 auteurs], CompCert [Leroy, CACM 2009, DOI 10.1145/1538788.1538814], Kitsune [OOPSLA 2012, DOI 10.1145/2384616.2384635 — le piège du DOI GPUVerify 10.1145/2384616.2384625 évité, le 5e auteur Denchev rétabli], POLUS [ICSE 2007, DOI 10.1109/ICSE.2007.65 — le DSU userspace multi-threads], SWE-agent [NeurIPS 2024, arXiv 2405.15793], Jakobi [ECAL 1995, DOI 10.1007/3-540-59496-5_337 — le reality gap], Peng [ICRA 2018, DOI 10.1109/ICRA.2018.8460528 — la randomisation dynamique], Bacic [CDC 2005, DOI 10.1109/CDC.2005.1582653 — le hardware-in-the-loop] ; la revendication « first quantified account » SCOPÉE : le niveau notation scellée sous gouvernance à intention signée [SWE-agent quantifie au niveau source, CompCert quantifie le traducteur] ; RQ3 RECADRÉE : la quantification des GARANTIES SILENCIEUSES DU COMPILATEUR — ce que le compilateur fournit gratuitement [une image chargeable, des séquences d'appel conformes à l'ABI, des codes d'erreur conventionnels, des hypothèses d'exécution outillées] et que la notation à la main doit re-dériver, leçon nommée par leçon)

**Le contexte qui fonde la décision (11/11).** La commande : « Ajouter au modèle de menace la conséquence de D81… Préparer le kit de la cérémonie D183 (séquestre chiffré) SANS l'appliquer au coffre réel (le geste appartient au développeur) ; clarifier la frontière D105/D81 pour le clone du laboratoire » et l'état de l'art étendu. Le laboratoire exécute intégralement, l'instrument de partage étant CELUI du coffre.

**Alternatives rejetées.** Appliquer le séquestre au coffre réel — rejeté : D87/D183, le geste appartient au développeur, et D183 exige la cérémonie VÉCUE de bout en bout. Générer les parts maintenant et les garder au labo — rejeté : des parts créées sans répartition réelle AJOUTENT du risque (la raison 3 de D183). Citer les nouvelles références sans vérification DOI — rejeté : la doctrine bibliographique de D182 (chaque identifiant vérifié, jamais un DOI de mémoire). Réécrire un partage Shamir dédié — rejeté : l'instrument CF2 D120 existe et est prouvé (la doctrine D185).

**Frontières.** Le coffre réel INTACT (aucune phrase lue, aucun conteneur ouvert, D81 DEMEURE la décision active) ; aucun arbre signé touché (le garde 14/14) ; le kit est un OUTIL de laboratoire en attente ; les huit références vérifiées aux sources primaires (arXiv/Crossref/proceedings).
"""

ENTREE = """

## Entrée 226 — le QUATRIÈME FICHIER D'INSTRUCTION EXÉCUTÉ : LES CORRECTIONS DE L'ÉDITION v0.13.0 (la liste exhaustive d'incohérences vérifiée UNE À UNE avec le rapport de conformité ; les statistiques reformulées — l'IC95 exact de 11/12, les caractéristiques opérationnelles de la cristallisation, la règle de comptage opérationnelle ; LE FACTEUR 15,3× RETIRÉ PAR L'AUDIT DU BENCHMARK [D191 : un artefact de périmètre — la finalisation seule comptée contre l'opération complète, les chiffres corrigés 75 983 contre 69 132/-Os 77 505, la notation COMPÉTITIVE jamais spectaculaire] ; la neutralité documentaire [l'anti-debug arbitré, la conséquence D81 au modèle de menace, le M7 requalifié qemu TCG] ; LE KIT DE LA CÉRÉMONIE D183 PRÉPARÉ SANS L'APPLIQUER [l'outil CF2 D120 tel quel, l'autotest VERT] ; l'état de l'art étendu [huit références vérifiées DOI/arXiv, la revendication scopée, RQ3 recadrée en garanties silencieuses du compilateur] ; D190/D191/D192 ; le manuscrit v0.13.0 [17 pages, la Table 6 RÉGÉNÉRÉE par le générateur ANTI-TRONCATURE, les comptes exacts en macros] ; la chaîne spec_v130 [58 pages, l'en-tête VERSION enfin v0.13.0 — la dette d'identité héritée de spec_v090 soldée]) (11/11, la session des corrections)

**La commande et le geste.** Le quatrième fichier (Qwen_text_20261111_f3q3x9i7n.txt) : les corrections de l'édition v0.13.0 — incohérences, statistiques, neutralité, benchmark, état de l'art — sans toucher aucun artefact scellé, tout consigné. Le laboratoire exécute INTEGRALEMENT ; le rapport de conformité (preuves_v130/rapport_conformite_v130.txt) tranche la liste LIGNE PAR LIGNE : 31 contrôles VERTS, 0 rouge.

**Les moments de la session.** (a) L'AUDIT DU BENCHMARK : la commande soupçonnait le 4 524 (4,16 instructions/ronde, sous tout minimum scalaire) — le mécanisme fut établi sur le CODE puis REJOUÉ sur pièces : benchmarks_v110 lisait le compteur de la FINALISATION SEULE (appeler() remet le compteur à zéro à CHAQUE appel), comparé à l'opération complète de la référence ; re-mesuré à périmètre correct (condensé vérifié contre hashlib AVANT le comptage, 17 compressions confirmées par le mécanisme du harnais, deux passes identiques) : 75 983 instructions contre 69 132 (-O2) et 77 505 (-Os) — le facteur 15,3× RETIRÉ, la revendication honnête est la COMPÉTITIVITÉ (−9 %/+2 %), et l'audit est CONSIGNÉ comme preuve de la classe de menace « l'instrument lui-même fautif » (D191). (b) LE GÉNÉRATEUR ANTI-TRONCATURE : la Table 6 de v0.11.0/v0.12.0 était écrite à la main hors générateur (cellules coupées, français dans un manuscrit anglais) — extraire_donnees_v130.py la RÉGÉNÈRE depuis les sorties brutes (mutation, fuzzage, sûreté mémoire, temps constant, indépendance, benchmark audité, modèle formel, statistiques corrigées : 15 lignes PARSÉES, aucune valeur tapée, aucune cellule jamais coupée — les chemins monospaces portent leurs points de coupe, les colonnes p{} replient le texte). (c) L'EN-TÊTE DE COUVERTURE : la chaîne spec portait « VERSION 0.9.0 » depuis spec_v090 — la dette d'identité NOMMÉE par la commande, soldée (couverture, corps, fusion en v0.13.0). (d) LE KIT D183 : l'outil au partage CF2 D120 TEL QUEL (jamais une réécriture), étendu bloc par bloc pour la phrase de longueur libre, l'AUTOTEST VERT sur phrase de test publique (10 combinaisons exactes, 10 paires sans fuite), le LISEZMOI pas à pas — le coffre réel INTACT, le geste au développeur.

**L'étape de vérification obligatoire (exigée par la commande, exécutée avant la livraison).** (a) le script d'extraction RÉ-EXÉCUTÉ et TOUS les tableaux régénérés ; (b) chaque valeur numérique du manuscrit CONTRONTÉE aux sorties brutes (75 983/69 132/77 505 == audit_benchmark.csv ; 0,615/0,998 == stats_v130.csv ; les comptes du journal en macros == les comptes extraits) ; (c) la liste du point 1 vérifiée LIGNE PAR LIGNE (31 VERT/0 ROUGE) ; (d) les statistiques RECALCULÉES par script (stats_v130.py rejoué : identiques) ; (e) les PDF compilés et vérifiés (renvois, légendes, numéros de version, l'exposant 10^6 du Tableau 1 CONFIRMÉ RENDU [le « 6 » en 6 pt sur le « 10 » en 9 pt — le « 106 » des extractions texte était un artefact], AUCUN débordement de marge [12 hérités de v0.12.0 → 0]) ; (f) les empreintes INTACTES (loupe.exe c1115105…, proxy.exe 446279f3… mesurés ; le garde du sceau 14/14 VERT).

**Les livrables.** TRIADE_soumission_v0.13.0.zip (cinq fichiers au plus : le README, le manuscrit PDF, les tableaux CSV fusionnés, les empreintes, le rapport de conformité) et TRIADE_complet_v0.13.0.zip (l'intégralité : les sources du manuscrit + les preuves v0.11.0/v0.12.0/v0.13.0 AVEC leurs sorties brutes, l'audit du benchmark, les statistiques corrigées, la chaîne spec_v130, le kit D183, les données, les extraits, les empreintes) — déposés au coffre, l'instruction f3q3x9i7n ARCHIVÉE (ARCHIVE/, md5 recoupé après le déplacement).

**Détail.** FRONTIÈRES : aucun artefact scellé ne bouge, aucun arbre signé ne bouge (14/14), aucune notation ne bouge, le coffre réel INTACT (D81 demeure, le kit D183 en attente) ; le md PROTOCOLE_TRIADE.md en v0.13.0 (préambule corrigé — jamais un chiffre faux qui traîne ; § 1.14, § 19.15, journal des versions) ; le PDF formel v0.13.0 (58 pages, chaîne spec_v130, empreinte consignée au registre). SUITE : LES DEUX FICHIERS SUIVANTS (v0.14.0 le programme empirique — le bras de référence compilateur pré-enregistré, la re-mesure RQ2, l'indépendance par second agent, les survivants de mutation ; v0.15.0 le modèle formel non borné et les kits matériels).
"""

W_BLOC = """
Task ID: 133
Agent: Z.ai (agent principal)
Task: LE QUATRIÈME FICHIER D'INSTRUCTION EXÉCUTÉ — LES CORRECTIONS DE
L'ÉDITION v0.13.0 : les incohérences vérifiées une à une, les statistiques
reformulées, le benchmark audité, le kit D183 préparé, D190/D191/D192, les
deux livrables, l'instruction archivée.

Work Log:
- L'AUDIT DU BENCHMARK (D191) : le facteur 15,3× RETIRÉ — l'instrument
  de v0.11.0 lisait le compteur de la FINALISATION SEULE (4 524 = le
  compteur de tls13-04, jamais l'opération complète) ; re-mesure à
  périmètre correct : l'op complète des blocs 75 983 instructions (init
  12 + absorb 71 447 + final 4 524, condensé vérifié contre hashlib,
  17 compressions confirmées mécaniquement, deux passes identiques)
  contre gcc -O2 69 132 et -Os 77 505 — COMPÉTITIVE (−9 %/+2 %), 1,45×
  plus compacte que -O2, moins que -Os ; aucune extension ISA au-delà
  du baseline (gcc : 101 mouvements SSE2 du baseline ; blocs GPR purs) ;
  second artefact nommé : le « 5 436 o » était l'image ENTIÈRE.
- LES STATISTIQUES (D190) : l'IC95 EXACT de 11/12 (Clopper-Pearson
  [0,615 ; 0,998], la réserve de non-indépendance) ; la cristallisation
  aux caractéristiques opérationnelles P(sceller|q) = (1-q)^n (3,1 %
  /0,098 % à q = 50 % — 32× ; 95,1 %/90,4 % à q = 1 % ; quantiles
  1,87σ/3,10σ) — les « α » de D189 étaient des rapports de vraisemblance
  mal étiquetés ; la règle de comptage opérationnelle DÉFINIE (runs 6/7
  comptés une fois chacun ; [T0-PÉRIMÉ] divulgué non compté).
- LA NEUTRALITÉ (D190) : l'anti-debug léger documenté honnêtement dans
  les DEUX documents ; le M7 requalifié (qemu-riscv64 TCG au noyau
  réel, réserve D149 — fence.i NON prouvé sur silicium) ; la conséquence
  D81 au modèle de menace (phrase + S_serrure en clair = deux éléments
  trivialement disponibles, le média piège seul rempart).
- LE KIT D183 (D192) : l'outil au partage CF2 D120 TEL QUEL (découpe
  bloc par bloc pour la phrase libre, l'indice x dans l'en-tête public) ;
  l'AUTOTEST VERT (10 combinaisons exactes, 10 paires sans fuite) ; le
  LISEZMOI, le manifeste, les listes de contrôle — le coffre réel
  INTACT, le geste au développeur.
- L'ÉTAT DE L'ART (D192) : huit références VÉRIFIÉES DOI/arXiv (LLM
  Compiler, CompCert, Kitsune [le piège du DOI GPUVerify évité], POLUS,
  SWE-agent, Jakobi, Peng, Bacic) ; la revendication scopée ; RQ3
  recadrée en garanties silencieuses du compilateur.
- LE GÉNÉRATEUR ANTI-TRONCATURE (extraire_donnees_v130.py) : la Table 6
  RÉGÉNÉRÉE depuis les sorties brutes (15 lignes parsées, jamais une
  coupe) ; les comptes du journal en MACROS exactes ; la note
  TOTAL/brouillons ; les cinq tableaux historiques par le module v100
  (ancres vérifiées, empreintes mesurées).
- LE MANUSCRIT v0.13.0 (17 pages) : toutes les corrections appliquées
  (§3.5 le benchmark audité, §4.1 les stats et la D81, la règle de
  comptage en §2.3, l'IC95 en §3.1, le M7 en §3.4, l'état de l'art, la
  conclusion, les déclarations) ; AUCUN débordement de marge (12
  hérités → 0).
- LA SPÉCIFICATION v0.13.0 : la chaîne spec_v130 (le patcher à 13
  remplacements ancrés), l'en-tête VERSION 0.9.0 → 0.13.0 (la dette
  d'identité de spec_v090), le § 1.14, le § 19.15, le § 1.10 aligné
  sur D181 (douze runs), la cristallisation corrigée, la phrase du
  tableau de menaces, les renvois § 3.5/§ 4.1 ; le PDF 58 pages ;
  le md v0.13.0 (préambule corrigé, § 1.14, § 19.15, versions).
- LA VÉRIFICATION : le rapport de conformité LIGNE PAR LIGNE — 31
  VERT / 0 ROUGE (verifier_edition_v130.py) ; le garde du sceau 14/14 ;
  loupe.exe c1115105… et proxy.exe 446279f3… INTACTS.
- LES LIVRABLES au coffre + l'instruction f3q3x9i7n ARCHIVÉE (md5
  recoupé).
- SUITE : v0.14.0 (ic09ydeli — le programme empirique) puis v0.15.0
  (ysddxpk0o — le modèle formel non borné, les kits matériels).
"""

D.write_text(D.read_text(encoding="utf-8") + DECISIONS, encoding="utf-8")
J.write_text(J.read_text(encoding="utf-8") + ENTREE, encoding="utf-8")
W.write_text(W.read_text(encoding="utf-8") + W_BLOC, encoding="utf-8")
print("[consigner_v130] D190 + D191 + D192 + Entrée 226 + worklog Task 133")
