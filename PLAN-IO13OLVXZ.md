# PLAN GELÉ — IO13OLVXZ (la vague 14)
> L'atelier de cohérence inter-pièces : les dix corrections (a)-(j) sourcées, le
> linter étendu, la génération v0.24.0. Aucune règle modifiée, aucun artefact
> scellé touché, aucun coffre réel (D105).
> Gelé AVANT toute modification ; empreinte consignée AVANT le premier geste.

## Le mandat
Corriger sur pièces, chacune sourcée (la localisation constatée au dépôt) :
(a) présentation + preuves (héritage) : le gain du cache round-trip 680,6× →
683,6× (canon non arrondi 285,725/0,418 publié, règle D244) — générateurs v230
corrigés à la source ;
(b) rapport de requalification + abstracts EN/FR : régénérer la décomposition des
15 exclusions DEPUIS le census CSV (`atelier-independance-peap6ws09/
classification-21-survivants.csv` : l'énumération manuelle somme à 13, pas 12 —
l'état mourant est ×5 ; l'abstract omet une famille — « the field beyond the
motif ») ; jamais une liste retapée : la table recomposée PAR CODE ;
(c) manuscrit §7 : le ratio plancher M4 3,4× — publier les opérandes non arrondis
(6,912/2,056) ou corriger (6,9/2,1 = 3,29) ;
(d) Livre v1.7 : bandeau couverture « Version 1.6 » → v1.7, date couverture
alignée sur la régénération, §10.1 « spécification v0.15.6 » → v0.15.8, chapitre
11 plage D75–D137 alignée sur la plage annoncée en couverture (D75–D250) ;
(e) manuscrit §2.1 « specification v0.15.7 » → v0.15.8 ; §4.1 et Table 9 : grille
T/X et classes T1–T5/X1–X3 → F1–F5/L1–L3 (D203, table de correspondance au kit) ;
(f) manuscrit corps : chaque « present edition » désignant une vague antérieure →
datation explicite (v0.18.0, v0.19.3…), la voix « présente édition » réservée à
l'édition courante ;
(g) spec Table 15 : « treize arbres VERTS » → quatorze ;
(h) H-CGP2 : nommer le dénominateur des pourcentages (T−(C+G)) et publier la
fermeture aux opérandes non arrondis (20,715 + 16,497 + 0,213 = 37,425 ; l'écart
aux arrondis est 13 ms, jamais « au millisecond » sans les opérandes) ;
(i) Table 8 D210 : colonne It. de T-loupe-16-d210-it2 (la correction nommée à la
caption — le registre as-filed demeure) ;
(j) titre GHASH : canon unique sur la variante ADOPTÉE (schoolbook 63,39 → 12,7×)
OU note explicite du choix karatsuba (l'écart 0,65 c dans l'IQR, non significatif).

## Le linter étendu
Bandeaux/couvertures/dates/plages décisionnelles dans les chaînes de version ;
décompositions de familles recomposées par code depuis les CSV ; tout ratio
publié porte ses opérandes non arrondis ; détection T/X hors marqueur d'époque
daté ; les ancres exigées gravées AVANT la régénération (la leçon vague 12).

## La génération v0.24.0
L'édition née de v0230 : les corrections (a)-(j) portées aux pièces, les
résultats de la vague 14 aux macros (H-CGP4, GHASH agrégé, TPL-ADD-v4, Tamarin,
H7), le changelog gelé étendu (chaque vague UNE ligne datée), les packs assemblés
(soumission, présentation, complet), les empreintes consignées.

## La vérification après modifications
Rejouer le linter étendu sur les CINQ pièces régénérées (zéro occurrence fautive,
contrôle négatif par réinjection synthétique REFUSÉ au premier nom) ; recomposer
par code chaque décomposition corrigée depuis les CSV bruts ; relecture intégrale
des paragraphes modifiés (zéro splice, zéro troncature) ; recouper les empreintes
des pièces historiques intactes ; sceau 14/14 avant/après ; consigner la décision
append-only avec la liste exhaustive des corrections et leurs sources.

## Les refus
Jamais le verbatim historique réécrit (l'erratum vit à côté) ; jamais une
correction sans sa source ; jamais un canon arrondi sans opérandes ; jamais la
voix « présente édition » datée d'une vague passée.
