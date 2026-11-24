# PLAN GELÉ — W20ADD (campagne add structurée + voie d'entraînement)

> Prompt 3 de l'évaluation v0.26.0. Aucun juge affaibli ; aucune cible re-tirée.

## Périmètre
1. `scripts/vague20/campagne_add_structuree.py` : le client à décodage contraint
   (structured output) — schéma JSON fermé {op, dst, src, offset} + 11 opcodes — et la
   boucle de réparation bornée à trois tours réutilisant `scripts/vague19/expandeur_add.py`
   (importé, jamais recopié).
2. Pré-enregistrement AVANT mesure : ≥ 15/18 à ≤ 3 000 tokens, médiane sur 18 et sur les
   vertes, graine, re-tokenisation ±1, juge intact (empreinte recoupée).
3. Voie d'entraînement décrite (SFT/DPO/RLVR, récompense typée du juge), sans run.

## Contraintes
- Aucun serving à structured output dans ce bac : la campagne part EN ATTENTE ; les
  fixtures (18 honnêtes, 4 mutées) sont rejouées et consignées.
- Le juge n'est jamais affaibli : empreinte de `expandeur_add.py` recoupée avant/après.

## Critères d'acceptation
- 18/18 pointeurs honnêtes verts ; 4 refus nommés ; deux compteurs à écart ≤ 1.
- Rejeu bit-identique à graine consignée ; pré-enregistrement hashé avant mesure.
- Statut EN ATTENTE consigné au journal, lecture défavorable portée telle quelle.
