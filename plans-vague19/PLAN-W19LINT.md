# PLAN GELÉ — W19LINT (porte de génération complète, linter v2 porté, six classes, six résidus)

> Instruction source : Prompt 1 du message du maître du 24/11/2026 12:42. Exécution seule,
> aucune valeur mesurée touchée, aucun artefact scellé (v0.24.0, v0.25.0) modifié.

## Périmètre
1. Porter le linter d'édition v2 (les cinq classes de `scripts/vague18/linter_v250.py`) dans la
   porte de génération du pack (`scripts/vague19/porte_generation_v260.py`), et l'étendre de
   SIX classes fail-closed :
   - VERSION-TABLE : les libellés de la présentation §10 == manifeste du pack (version par pièce) ;
   - DECISION-RANGE : tout ID `Dnnn` cité dans une pièce ∈ [D1, dernière décision réelle] et
     toute plage annoncée cohérente avec son bord haut ;
   - CHANGELOG-ORDER : les entrées datées du changelog gelé sont en ordre chronologique strict ;
   - NUMEROTATION : une seule convention de renvoi (spécification désignée `spec § x.y`,
     pièces du dépôt `doc § x`) — aucune forme mixte dans Preuves §2 ;
   - BENCH-COUNT : tout « n/n » annoncé se recompose depuis le JSON/les cas du kit ;
   - SEMANTIC-THREAT : chaque ligne « détecté — … » de spec §15.1 nomme sa classe d'adversaire
     et son bord de modèle, et le §15.1 ne revendique plus « toutes neutralisées » (D254).
2. Corriger les six résidus constatés : étiquettes v0.24.0 de la présentation (tableau §10 et
   titre de vague), §15.1 non qualifiée, D262–D264 annoncés-absents de la spécification,
   « +1 » du banc 16/16 (le cas nominal, à nommer ou à corriger), ordre du changelog
   (v0.25.0 avant v0.24.0), numérotation mixte des Preuves §2.
3. Régénérer les cinq pièces : manuscrit v0.26.0, spécification v0.15.11, Livre v1.10,
   preuves v0.26.0, présentation v0.26.0.

## Contraintes
- Append-only : corrections par amendement daté ou par source régénérée, jamais de réécriture
  d'un verbatim scellé ; les PDF v0.24.0/v0.25.0 restent intacts (empreintes recoupées avant/après).
- Aucune valeur mesurée modifiée ; aucun secret lu ni imprimé (garde pre-commit).
- Commit d'abord : les cinq plans gelés + leurs empreintes AVANT toute donnée.

## Fichiers touchés
`scripts/vague19/linter_v260.py`, `scripts/vague19/porte_generation_v260.py`,
`edition-v0230/main.tex`, `scripts/spec_v158/*.tex`, `scripts/livre_v18/*.tex`,
`scripts/vague17/generer_pieces_v240.py` (copie v19), `pack-v260/`, rapports.

## Critères d'acceptation
- Porte v0.26.0 : ZÉRO rouge ; onze classes vertes sur les cinq pièces.
- Test du lecteur rejoué sur chaque numéral des cinq pièces depuis ses opérandes imprimés.
- Versions et sha256 des cinq pièces == manifeste `empreintes_livrables_v0.26.0.txt`.
- Quatre contrôles négatifs REFUSÉS nommément : libellé de version muté, ID hors plage,
  ligne de menace non qualifiée, compte de banc muté.
- Sceau-I 14/14 avant et après ; scellés v0.25.0 intactes (5/5 sha256).
- Rapport avant/après avec empreintes.
