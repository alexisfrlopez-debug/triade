#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigner_v150_etat.py — L'ÉTAT v0.15.0 OUVERTE (le sixième fichier,
ysddxpk0o) : les faits exécutés au geste consignés, la suite nommée."""
import pathlib

D = pathlib.Path("/home/z/my-project/triade/docs/DECISIONS.md")
J = pathlib.Path("/home/z/my-project/triade/docs/JOURNAL_TRAVAIL.md")
W = pathlib.Path("/home/z/my-project/triade/worklog.md")

D.write_text(D.read_text(encoding="utf-8") + """

## D196 — LA v0.15.0 OUVERTE : LES FAITS AU GESTE (Tamarin ET ProVerif ABSENTS du laboratoire — constat re-vérifié, la déviation consignée : LA VOIE DE L'INVARIANT INDUCTIF dans l'explorateur, couvrant un nombre NON BORNÉ d'époques, est la route des preuves P1-P4 — À LA CONTINUATION, jamais simulée) ; LES TROIS KITS DE MESURE MATÉRIELLE préparés EN ATTENTE (scripts/kits_mesure_v150/ : le dudect temps réel [RDTSC/QPC, l'affinité cœur, le turbo, N≥60, |t|>5 — les cibles crypto par pièce scellée], le patch à chaud RISC-V sur silicium [fence.i — CE QUE L'ÉMULATION NE POUVAIT PAS PRÉUVER], le terrain tiers Loupe [une seconde machine Windows, le scénario intégral T0→T7+S0]) ; LA RÉPLICATION : la grille T/X D189 INCHANGÉE, le second annotateur À RECRUTER (le statut consigné), l'axe second domaine EN ATTENTE d'une vraie commande (jamais un exercice démonstratif) ; LES PREUVES P1-P4 NON BORNÉES, LES TESTS DE RAFFINEMENT modèle↔implémentation, LES BORNES ÉTENDUES de l'explorateur : LA SUITE NOMMÉE à la continuation — l'état est au journal, l'achèvement ne se simule jamais

**Le contexte.** Le sixième fichier (Qwen_text_20261111_ysddxpk0o.txt) : le modèle formel non borné, les kits de mesure matérielle, la réplication, les statuts systématiques. La session a livré la v0.14.0 MENÉE À TERME (l'Entrée 228) puis ouvert la v0.15.0 par les faits exécutables : le constat des vérificateurs (absents — la déviation honnête, la route alternative consignée), les trois kits préparés, l'état de la réplication.

**Frontières.** Aucun artefact scellé touché ; le garde 14/14 VERT au geste ; aucun résultat matériel fabriqué (les kits EN ATTENTE) ; les preuves non bornées NON prétendues — la suite nommée.
""", encoding="utf-8")

J.write_text(J.read_text(encoding="utf-8") + """

## Entrée 229 — le SIXIÈME FICHIER D'INSTRUCTION OUVERT : la v0.15.0 PAR LES FAITS EXÉCUTABLES (Tamarin/ProVerif absents — constat re-vérifié, la déviation consignée : la voie de l'invariant inductif à la continuation ; LES TROIS KITS de mesure matérielle préparés EN ATTENTE — le dudect temps réel, le fence.i sur silicium, le terrain tiers Loupe ; LA RÉPLICATION : la grille D189 inchangée, le second annotateur à recruter, le second domaine en attente d'une vraie commande ; D196) — les preuves P1-P4 non bornées, les tests de raffinement et les bornes étendues : LA SUITE À LA CONTINUATION (11/11, la passation)

**L'état.** La v0.14.0 est MENÉE À TERME (l'Entrée 228 : le re-jeu des 832, les documents, les livrables, l'instruction archivée — le commit a14ee30, les trois miroirs synchronisés). La v0.15.0 est OUVERTE par les faits : le constat des vérificateurs, les trois kits, l'état de la réplication — D196 consigne l'ouverture et nomme la suite : (a) LES PREUVES NON BORNÉES par invariant inductif dans l'explorateur (un nombre non borné d'époques — la généralisation du modèle D187) ; (b) LES TESTS DE RAFFINEMENT (les traces du modèle contre coffre_cf3.py — l'équivalence des transitions, y compris les chemins d'échec) ; (c) LES BORNES ÉTENDUES de l'explorateur (époques > 3, profondeur > 6) comme contre-vérification ; (d) LES STATUTS SYSTÉMATIQUES au manuscrit (« prouvé non borné » / « prouvé borné » / « en attente de run matériel ») ; (e) les documents d'édition, les zips, l'archivage de ysddxpk0o. Le dossier /instructions demeure : ysddxpk0o SEUL (le dernier).
""", encoding="utf-8")

W.write_text(W.read_text(encoding="utf-8") + """
Task ID: 136
Agent: Z.ai (agent principal)
Task: LA v0.15.0 OUVERTE par les faits exécutables — les constats, les
trois kits de mesure matérielle EN ATTENTE, l'état de la réplication ;
la suite (preuves non bornées, raffinement, statuts) nommée à D196.

Work Log:
- LE CONSTAT : Tamarin ET ProVerif ABSENTS (re-vérifié au geste) — la
  déviation consignée, la voie de l'invariant inductif (époques non
  bornées) la route de P1-P4.
- LES TROIS KITS (scripts/kits_mesure_v150/) : le dudect temps réel
  (RDTSC/QPC, affinité, turbo, N≥60, |t|>5, les crypto par pièce
  scellée) ; le fence.i sur SILICIUM (ce que qemu ne pouvait pas) ;
  le terrain tiers Loupe (le scénario intégral, l'autre machine).
  EN ATTENTE — jamais un chiffre fabriqué.
- LA RÉPLICATION : la grille D189 INCHANGÉE, le second annotateur À
  RECRUTER (consigné), le second domaine EN ATTENTE d'une vraie
  commande.
- LE GARDE : 14/14 VERT au geste — aucun artefact scellé touché.
- SUITE (D196) : les preuves non bornées, les tests de raffinement,
  les bornes étendues, les statuts systématiques, les documents, les
  zips, l'archivage ysddxpk0o — À LA CONTINUATION.
""", encoding="utf-8")
print("[consigner_v150_etat] D196 + Entrée 229 + Task 136")
