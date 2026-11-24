# PLAN GELÉ — W20LINT (linter v4 : quatre classes, quatre résidus, cinq pièces)

> Prompt 1 de l'évaluation v0.26.0 (24/11/2026). Append-only ; aucune valeur mesurée
> modifiée ; aucun artefact scellé v0.24.0–v0.26.0 touché.

## Périmètre
1. Quatre classes fail-closed ajoutées à `scripts/vague19/linter_v260.py` (copie v4 en
   `scripts/vague20/linter_v4.py`, la v3 demeurant pour l'histoire) :
   C12 VERSION-PROSE — toute occurrence « édition courante vX » / « révision vX » /
       « spécification vX » dans les cinq pièces confrontée au manifeste (le trou C6 :
       la prose du Livre n'était pas scannée) ;
   C13 WAVE-CONTINUITY — toute « vague N » renvoie à une entrée datée du changelog gelé
       ou porte une marque hors-édition ;
   C14 ABSTRACT-LENGTH — résumé du manuscrit ≤ 250 mots (convention nommée) ;
   C15 READER-TEST-COUNT — le compte du test du lecteur se recompose depuis une liste
       de cas énumérés (une ligne par cas, comme le banc 16/16).
2. Quatre résidus soldés à la source :
   (a) Livre du Coffre : couverture « v0.15.10 », page de titre « révision v1.9 », §10.1
       et légende de table 12 « spécification v0.15.10 » ;
   (b) Présentation §8 « vague 16 » alors que le changelog saute 15→17 : vérifier au
       journal quelle vague porte TPL-ADD-v5 et aligner ;
   (c) Manuscrit « −35,7 % » (1714→1103) : épingler les opérandes non arrondis dans le
       registre de provenance (ou noter l'arrondi) ;
   (d) Preuves : « test du lecteur 7/7 » qui liste neuf recompositions — décomposer.
3. Régénérer les cinq pièces en v0.27.0 / spec v0.15.12 / Livre v1.11 ; consigner D269.

## Contraintes
- Les pièces v0.24.0–v0.26.0 restent intactes (empreintes recoupées avant/après).
- Aucune valeur mesurée modifiée : seules des références, comptes et conventions.
- Commit des plans AVANT toute donnée.

## Critères d'acceptation
- Porte V1..V7 + L1..L15 : zéro rouge.
- Une mutation par nouvelle classe, chacune REFUSÉE nommément (4/4).
- Empreintes des scellés v0.26.0 intactes (5/5).
- Test du lecteur recomposé ET décomposé (une ligne par cas).
- D269 au journal, limites nommées.
