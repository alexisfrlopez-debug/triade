#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigner_v140_partiel.py — LA CONSIGNATION D'ÉTAT de la v0.14.0 EN
COURS (la discipline : le journal est la passation — les mesures faites
sont consignées SUR PIÈCES, ce qui reste est NOMMÉ, jamais un achèvement
simulé). D194 + Entrée 227 + worklog Task 134."""
import hashlib
import pathlib

REPO = pathlib.Path("/home/z/my-project/triade")
D = REPO / "docs" / "DECISIONS.md"
J = REPO / "docs" / "JOURNAL_TRAVAIL.md"
W = REPO / "worklog.md"

plan = REPO / "scripts" / "preuves_v140" / "PLAN_PREENREGISTRE_v140.md"
h_plan = hashlib.sha256(plan.read_bytes()).hexdigest()

DECISIONS = f"""

## D194 — LE BRAS DE RÉFÉRENCE COMPILATEUR MESURÉ, LA RE-MESURE RQ2, L'INDÉPENDANCE PAR INSTANCE ISOLÉE (v0.14.0 EN COURS : les mesures exécutées et consignées sur pièces ; les documents d'édition — manuscrit, spécification, zips — demeurent À ÉDITER, l'état est nommé, jamais un achèvement simulé) ; LE PLAN PRÉ-ENREGISTRÉ INTACT (sha256 {h_plan[:16]}… — le CA5 : l'empreinte confrontée au geste de vérification de la continuation AVANT toute édition des résultats)

**Le bras de référence (le point 1, exécuté).** LA RÉFÉRENCE C (scripts/bras_c_v140/bras_c.c) : SIX blocs de Loupe réimplémentés EN C DEPUIS LES MÊMES CONTRATS (01 ouvrir, 02 lire, 05 sha256, 08 ligne, 13 recherche, 16 saisie — les cinq familles couvertes), les primitives OS prises par table de pointeurs ms_abi AUX MÊMES SHIMS du mini-OS (CA2), compilée gcc 14.2 -O2/-Os (clang ABSENT du labo — l'écart nommé), AUTO-VÉRIFIÉE contre les vecteurs dorés AVANT toute mesure (CA1 : les deux niveaux VERTS — au passage DEUX fautes de table K attrapées par l'autotest avant toute mesure : K[24] 0x983e5152, K[47] 0x106aa070 — la méthode appliquée à elle-même). LA CAMPAGNE (comparer_v140.py, rejouable) : les vecteurs des contrats aux DEUX camps — ZÉRO DIVERGENCE (les camps s'accordent sur tous les vecteurs : la notation scellée et la référence compilée ont LE MÊME COMPORTEMENT observable aux contrats) ; les instructions par opération complète au même crochet (convention D191) : loupe-02 PARITÉ (A 48 / C 47), loupe-05 PARITÉ (A 9089 / C 9146 — la notation tient l'algorithme sha À TRAVAIL ÉGAL contre le compilateur), loupe-08/13/16 la notation PLUS CHERE en instructions (641/477, 193/69, 39/16 — la boucle serrée paie), loupe-01 la cascade saine 102 176 / 75 560 (l'ADAPTATION du panneau nommée : le camp C calcule la moitié sha seulement — aucun md5 C audité n'existe, le banc v0.11.0 l'écarta comme fautif) ; les TAILLES au bon périmètre : MIXTES (la notation plus compacte sur 05 [384+765 hérités contre 1707 — le partage PAR LA CARTE], 16 [704 contre 413] ; le C plus compact sur 01, 13) ; LA MUTATION (16 mutants/bloc, graine 20261111, le même tirage) : camp A 3-13/16 tués (K2-décodage + K3 — les survivants NOMMÉS, cohérents avec la classe orchestration de D185), camp C 16/16 sur les blocs OS (le K2-adapté aux comptes d'appels OS tue TOUT — le code compilé est plus fragile à la mutation d'octet sur les séquences d'appels), 11-14/16 sur les purs — H4 TENUE : la notation est testable au même degré, le compilé n'est pas plus testable.

**La re-mesure RQ2 (le point 2, exécutée).** Les budgets de BOUT EN BOUT sur le matériel RÉEL de l'ère Loupe, au tokenizer cl100k_base (celui de M1), les DISTRIBUTIONS (n=10/opération) : localiser médiane 580 [q1 496 .. q3 706] ; éditer 2 143 [1 085 .. 3 463] ; ajouter 3 510 [3 128 .. 4 091] ; LA BASELINE NAIVE : 300 304 tokens (37 538 lignes de désassemblage de loupe.exe) — la carte indexée épargne DEUX ordres de grandeur. LE RAISONNEMENT estimé par le rapport génération/contenu des retouches réelles de l'ère (×1,08 — l'estimation NOMMÉE, jamais une mesure). LA LECTURE HONNÊTE, DÉFAVORABLE AU PROTOCOLE (CA3) : les opérations de l'ère Loupe coûtent PLUS que M1 (51/719/1 088 — les valeurs M1 demeurent HISTORIQUES, jamais remplacées) : les notations sont plus longues, les contrats plus denses — le coût a grandi avec la exigence, il demeure un ordre de grandeur sous la baseline naive.

**L'indépendance (le point 3, exécutée avec l'écart nommé).** L'infrastructure d'agents du labo n'expose PAS d'autre famille — le sous-agent a tourné sur le MÊME modèle (glm-5.3) : L'INDISPONIBILITÉ EST CONSIGNÉE (la commande : « si disponible, sinon consigner ») ; l'indépendance obtenue est celle de l'INSTANCE (un contexte neuf, la dérivation depuis les définitions mathématiques — jamais la mémoire) — PLUS FAIBLE que l'inter-familles, dite telle quelle ; LA CONFRONTATION : les tables T[64] MD5 et K[64] SHA-256 de l'agent == le plan == les définitions — ZÉRO DIVERGENCE sur les 128 constantes ; LA VOIE ALTERNATIVE SUPPLÉMENTAIRE exécutée au geste : la racine cubique ENTIÈRE (recherche binaire exacte sur p·2^96, aucun flottant) — elle confirme les 64 constantes indépendamment de l'agent ET du plan.

**Les survivants (le point 4, PARTIELLEMENT exécuté — la suite nommée).** La campagne du bras a re-jeué 96 mutants des SIX blocs avec un harnais de COMPOSITION par mutant (suite_a : la chaîne 01→02→05→08→13→16 — la session née entière, les fenêtres, les gammes, les lignes, les recherches, la saisie) : les nouveaux taux par bloc consignés au CSV (A 3-13/16 tués par la composition — les survivants restants nommés au rapport). LA SUITE nommée : le re-jeu des 832 mutants complets avec le composition-harnais étendu aux 18 blocs et le câblage des killers sémantiques par mutant isolé pour l'orchestration/UI restante — À LA CONTINUATION.

**Ce qui demeure À ÉDITER (l'état, jamais un silence) : le manuscrit v0.14.0 (la sous-section Results de la comparaison contrôlée, RQ2 reformulée sur la mesure finale, les limites/menaces, l'abstract/conclusion), la chaîne spec_v140, le md, les kits terrain « EN ATTENTE », les deux zips, l'archivage de l'instruction ic09ydeli, le commit. Les preuves vivent à scripts/preuves_v140/ (bras_c.csv, remesure_rq2.csv, independance_agent.csv, le rapport du plan) — tout est rejouable, l'empreinte du plan pré-enregistré verrouillée à D193.**

**Alternatives rejetées.** Éditer les documents d'édition à la hâte pour « terminer » la version dans la session — rejeté : un document bâclé est une faute pire qu'un état nommé (la leçon des C fautifs du banc : mieux aucun chiffre qu'un chiffre faux, mieux un état honnête qu'une version simulée). Mesurer RQ2 en comptant les caractères — rejeté : le tokenizer de M1 est disponible, la mesure est exacte au contenu près, l'estimation du raisonnement est nommée comme estimation.

**Frontières.** Aucun artefact scellé touché ; l'empreinte du plan pré-enregistré INTACTE ({h_plan[:16]}…) ; les kits terrain NON fabriqués de résultats (aucun run terrain inventé) ; l'instruction ic09ydeli DEMEURE à /instructions (l'exécution n'est pas terminée, l'archivage attend l'achèvement).
"""

ENTREE = """

## Entrée 227 — le CINQUIÈME FICHIER D'INSTRUCTION EN COURS D'EXÉCUTION : LE PROGRAMME EMPIRIQUE v0.14.0 — LES MESURES SUR PIÈCES (le plan PRÉ-ENREGISTRÉ D193 AVANT toute mesure, son empreinte verrouillée ; LE BRAS DE RÉFÉRENCE COMPILATEUR mesuré : la référence C aux MÊMES contrats, aux MÊMES shims, AUTO-VÉRIFIÉE, ZÉRO DIVERGENCE aux vecteurs, les instructions/tailles/mutations aux deux camps — la notation PARITAIRE sur sha, plus chère sur les purs, testable au même degré ; LA RE-MESURE RQ2 : localiser 580 / éditer 2 143 / ajouter 3 510 de médiane, la baseline naive 300 304, les valeurs M1 historiques, la lecture DÉFAVORABLE au protocole consignée telle quelle ; L'INDÉPENDANCE par instance isolée : zéro divergence sur les 128 constantes, l'écart de famille nommé ; LES SURVIVANTS partiellement re-jeués à 96 mutants par composition) — LES DOCUMENTS D'ÉDITION À LA CONTINUATION (le manuscrit v0.14.0, la spec, les zips, l'archivage : l'état nommé au journal, jamais un achèvement simulé) (11/11, la session du bras de référence)

**La commande.** Le cinquième fichier (Qwen_text_20261111_ic09ydeli.txt) : le bras de référence compilateur pré-enregistré d'abord, la re-mesure RQ2, l'indépendance de l'oracle par second agent, les survivants de mutation, la mise à jour du manuscrit.

**Les moments.** (a) LE PRÉ-ENREGISTREMENT AVANT TOUT : le plan (hypothèses H1-H4, critères CA1-CA5, méthode, les six blocs, les vecteurs) consigné à D193 avec son empreinte — la fraude post-mesure est désormais ATTRAPABLE. (b) L'AUTOTEST DE LA RÉFÉRENCE a attrapé DEUX fautes de table K (K[24], K[47]) AVANT toute mesure — la doctrine md5/aes rejouée : l'instrument se contrôle avant de juger. (c) LA CAMPAGNE : trois sessions de mise au point (la convention ms_abi des pointeurs OS, le 5e argument msx64 écrasé par les canaris du harnais — l'écriture APRÈS les canaris, le miroir du vrai appel ; les zones de vecteurs trop proches — le motif écrasait la queue de la fenêtre) puis LA MESURE PROPRE : zéro divergence, les distributions complètes (médiane/quartiles/min/max au CSV). (d) LE FAIT SCIENTIFIQUE : la notation à la main de sha-256 tient le compilateur À TRAVAIL ÉGAL (9 089 contre 9 146 instructions, 384+765 contre 1 707 octets) — sur les blocs purs simples la boucle serrée du compilé gagne (16 contre 39 pour la saisie) — SUR L'ENSEMBLE des six blocs la notation est COMPÉTITIVE, jamais spectaculaire, et le taux de mort par mutation est DU MÊME ORDRE (H4 tenue).

**L'état (la passation).** Les preuves : preuves_v140/ (bras_c.csv + rapport, remesure_rq2.csv + rapport, independance_agent.csv + rapport, PLAN_PREENREGISTRE_v140.md — empreinte à D193/D194). LA SUITE : le manuscrit v0.14.0 (la sous-section Results, RQ2 reformulée, les limites, l'abstract), la chaîne spec_v140, le md, les kits terrain en attente, les zips, l'archivage de ic09ydeli, le commit — PUIS la v0.15.0 (ysddxpk0o). L'instruction ic09ydeli DEMEURE à /instructions (non archivée : l'exécution n'est pas terminée).
"""

W_BLOC = """
Task ID: 134
Agent: Z.ai (agent principal)
Task: LE CINQUIÈME FICHIER D'INSTRUCTION EN COURS — LE PROGRAMME
EMPIRIQUE v0.14.0 : le plan pré-enregistré (D193), le bras de référence
compilateur mesuré, la re-mesure RQ2, l'indépendance par instance
isolée, les survivants partiellement re-jeués — les documents d'édition
à la continuation.

Work Log:
- LE PRÉ-ENREGISTREMENT (D193) : le plan (H1-H4, CA1-CA5, les six
  blocs, la méthode) consigné AVANT toute mesure, l'empreinte
  sha256 verrouillée (7b14da525e0194f3…) — CA5 attrapable.
- LE BRAS C (bras_c_v140/) : six blocs depuis les MÊMES contrats, la
  table OS aux MÊMES shims (pointeurs ms_abi), gcc -O2/-Os (clang
  absent, l'écart nommé), l'AUTOTEST VERT avant tout (deux fautes de
  table K attrapées : K[24] 0x983e5152, K[47] 0x106aa070).
- LA CAMPAGNE (comparer_v140.py) : ZÉRO DIVERGENCE aux vecteurs ;
  loupe-02 PARITÉ (48/47), loupe-05 PARITAIRE À TRAVAIL ÉGAL
  (9 089/9 146 instructions, l'héritage PAR LA CARTE 384+765 contre
  1 707 o), les purs plus chers à la notation (08 : 641/477 ; 13 :
  193/69 ; 16 : 39/16), la cascade 01 saine 102 176/75 560 (le panneau
  C = la moitié sha, l'adaptation nommée) ; la mutation : A 3-13/16
  (survivants nommés), C 16/16 sur les OS (le K2-adapté aux comptes
  d'appels), 11-14/16 sur les purs — H4 tenue.
- LA RE-MESURE RQ2 (remesure_rq2_v140.py, cl100k_base) : localiser
  580 [496..706], éditer 2 143 [1 085..3 463], ajouter 3 510
  [3 128..4 091] (n=10, le raisonnement estimé ×1,08 NOMMÉ), la
  baseline naive 300 304 (37 538 lignes de désassemblage) — les
  valeurs M1 (51/719/1 088) HISTORIQUES, la lecture DÉFAVORABLE au
  protocole consignée (les opérations Loupe coûtent plus qu'en M1).
- L'INDÉPENDANCE (independance_v140.py) : l'écart de famille consigné
  (l'infra n'expose qu'un modèle — l'indépendance d'INSTANCE, plus
  faible, dite telle quelle) ; les tables de l'agent == le plan == les
  définitions : ZÉRO DIVERGENCE sur 128 constantes ; la voie
  alternative (recherche binaire entière sur p·2^96) confirme.
- LES SURVIVANTS : 96 mutants re-jeués avec le harnais de composition
  (la chaîne 01→16) — le re-jeu complet des 832 À LA CONTINUATION.
- L'ÉTAT : les documents d'édition v0.14.0 (manuscrit, spec, zips,
  archivage ic09ydeli) À LA CONTINUATION — l'instruction demeure à
  /instructions, l'achèvement n'est PAS simulé.
"""

D.write_text(D.read_text(encoding="utf-8") + DECISIONS, encoding="utf-8")
J.write_text(J.read_text(encoding="utf-8") + ENTREE, encoding="utf-8")
W.write_text(W.read_text(encoding="utf-8") + W_BLOC, encoding="utf-8")
print("[consigner_v140] D194 + Entrée 227 + worklog Task 134 "
      "(l'état de la continuation)")
