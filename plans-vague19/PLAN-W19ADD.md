# PLAN GELÉ — W19ADD (frontière « add » : pointeur-seul, expandeur déterministe, boucle de réparation)

> Instruction source : Prompt 5 du message du maître du 24/11/2026 12:42. Aucun juge affaibli,
> aucune cible re-tirée après mesure ; la lecture défavorable est consignée telle quelle.

## Périmètre
1. `scripts/vague19/expandeur_add.py` — l'expandeur DÉTERMINISTE côté client : l'agent n'émet
   qu'un diff sémantique structuré (opcode / opérande / offset au point exact) ; l'expandeur
   compile la notation complète, sans choix ni créativité, et la confronte au juge.
   Quatre refus nommés fail-closed conservés (HORS-FORMAT, ID-INCONNU, EXPANSION-DIVERGENTE,
   FORME-INVALIDE) — un pointeur ambigu est refusé, jamais deviné.
2. `scripts/vague19/boucle_reparation.py` — la boucle de réparation par contre-exemple : le refus
   exact du juge (classe, position, attendu) est réinjecté, bornée à 3 tours, chaque conversion
   consignée par classe de refus.
3. Pré-enregistrement : ≥ 15/18 verts à ≤ 3 000 tokens par changement validé ; médiane sur les
   18 tâches ET sur les seules vertes (deux conventions nommées) ; graine consignée ;
   re-tokenisation indépendante à ±1 token. `atelier-w19-add/preregistrement.json` AVANT mesure.
4. Fixtures : pointeurs honnêtes (expansion verte 18/18 attendue) et fixtures MUTÉES pour chacun
   des quatre refus.

## Contraintes
- Aucun juge affaibli : l'expandeur ne « répare » jamais un verdict ; il rend la notation, le
  juge décide.
- Aucune campagne réelle servie depuis ce bac : la campagne part EN ATTENTE d'un serving ;
  l'instrument et ses autotests sont livrés.
- La lecture défavorable (cible manquée) est consignée telle quelle si elle survient.

## Critères d'acceptation
- Expansion cliente verte 18/18 sur les pointeurs honnêtes ; quatre refus exercés sur fixtures
  mutées (chacun REFUSÉ nommément).
- Campagne re-jouable deux fois à graine consignée (verdicts bit-identiques) — rejeu sur les
  fixtures ; la campagne réelle reste EN ATTENTE.
- Comptes par classe de refus recomposés depuis les journaux bruts.
- Ratios publiés recalculés depuis les opérandes non arrondis.
- Empreintes des pièces scellées intactes.
