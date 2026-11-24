# PLAN GELÉ — CMAH20ZA5 — le linter v2 porté à v0.24.0 et les résidus soldés

## L'instruction, en une phrase
Porter le linter d'édition v2 (cinq classes) à la génération v0.24.0 des cinq pièces,
corriger les résidus listés par amendements datés append-only (sans toucher un PDF
scellé ni une valeur mesurée), régénérer les cinq pièces sous le linter, et tout
re-vérifier.

## Les résidus à solder (dans l'ordre du plan)
(1) manuscrit : abstract « v0.23.3 » → v0.24.0 ; changelog ordonné (v0.23.3 avant
v0.24.0) ; plage D1–D251 → D1–D255 ; « corpus 109 triples » étiqueté historique ou
porté à v2.1 ; Data Availability v0.23.2 → v0.23.3/v0.24.0.
(2) spécification : annexe B D75–D251 → D75–D255, lignes D252–D255, D223 en ordre.
(3) Livre : avant-propos v1.7/v0.15.8 → v1.8/v0.15.9 ; §10.1 ; date de couverture.
(4) preuves : renvois §7.1.1/§8.6 → §7.6/§7.7 (ou table de correspondance) ; « six
états » → « sept états (0–6) » ; ventilation aux opérandes non arrondis
(20,715+16,497+0,213 = 37,425) ou résidu 13 ms nommé ; mutants 776/832 étiqueté
ère v0.14.0 vs 811/832 v0.19.5 ; ghash 49,12× par-appel (78 888/1 606) distinct du
par-multiplication (19,66/63,39) ; médiane éditer 712 → 712,5 ou troncature nommée.
(5) présentation : « 11/11 refus » → « 11/11 contrôles dont 9 refus nommés ».

## Vérification exigée
Linter v2 : 0 résidu sur les cinq pièces ; test du lecteur : chaque ratio/somme publié
se recompose depuis ses opérandes imprimés ; 4 contrôles négatifs de provenance ;
empreintes des artefacts scellés AVANT/APRÈS (aucun octet déplacé) ; verdict au journal.

## Conséquence prévue
Une ÉDITION v0.25.0 (les cinq pièces régénérées), puis la mise à jour des packs.
