# PLAN PRÉ-ENREGISTRÉ — LA VAGUE 11, L'INSTRUCTION ahult8jgd : LA BOUCLE PORTEUSE AES-NI RESTRUCTURÉE, LE CACHE DE ROUND-TRIP, LA CRISTALLISATION INCRÉMENTALE, LA DÉCOMPOSITION DES 37 s

> Pré-enregistré AVANT toute mesure (l'empreinte sha256 consignée à
> EMPREINTES-PLANS-VAGUE11.txt, commitée AVANT la première donnée).

## 1. LA BOUCLE PORTEUSE (le constat mesuré, la cible)

La référence actuelle : 54 cycles/bloc ENVELOPPE COMPRISE au rig natif (le
flux v2 — le sondage hissé, la boucle par bloc au chemin pur), le corps NI
net 4 cycles/bloc, la calibration du stub msx64 4,1 cycles/appel. LA CHAÎNE
SÉRIALISÉE par registres porteurs : add (l'avance d'adresse) → mov (le
portage du pointeur) → call (l'entrée au bloc) — chaque bloc paie la chaîne.

LA RESTRUCTURE : (a) LA TABLE D'ADRESSES PRÉCALCULÉE (les adresses des N
blocs posées une fois, la boucle lit [table + i*8] — plus aucun add par
bloc) ; (b) LE DÉROULAGE (k blocs par itération, la chaîne payée une fois
par k) ; (c) LA SUPPRESSION DE LA CHAÎNE add→mov→call (le pointeur avance
par le mode d'adressage [reg + index*8], l'appel inline) ; (d) L'ÉVALUATION
DE L'INLINING DU BLOC NI (le corps aesenc posé dans la boucle — plus de
call : l'économie du stub, la perte éventuelle de l'isolement — MESURÉE,
les deux variantes livrées au rapport).

LA CIBLE MESURÉE : ≤12 cycles/bloc enveloppe comprise. LA MESURE : RDTSCP,
cœur fixé, n≥20, médiane + IQR, la même machine ; la parité observable avec
le bloc scellé (les sorties octet pour octet aux vecteurs FIPS + la
différentielle 64/64) ; LE SCELLÉ INTACT (la variante vit à la marge).

## 2. LE CACHE DE ROUND-TRIP (la clé = sha256 de la notation + version assembleur + config)

Le harnais re-vérifie aujourd'hui le round-trip de CHAQUE bloc à CHAQUE
ouverture (20 s l'échantillon Unicorn). LE CACHE : la clé = sha256(notation
|| version du moteur d'assemblage || configuration du profil) ; le hit
retourne le verdict caché SANS ré-exécution ; TOUT écart de clé = re-vérification
complète (fail-closed) ; le contrôle négatif : la notation mutée d'un octet
DOIT invalider la clé (ATTRAPÉ au premier nom). La mesure : le temps
d'ouverture avant/après (n≥10, la même machine).

## 3. LA CRISTALLISATION INCRÉMENTALE (le graphe de dépendances de la carte)

Le diff d'une modification touche k blocs ; la re-vérification full-card est
aujourd'hui la règle. L'INCREMENT : le graphe de dépendances de la carte
(déclaré aux entrées deps=), la fermeture transitive du diff SEULEMENT
re-vérifiée ; L'AUDIT 1/10 MAINTENU (un bloc sur dix tiré au hasard — graine
consignée — re-vérifié intégralement : la garantie statistique demeure) ; le
contrôle négatif : un bloc hors fermeture muté DOIT être attrapé par l'audit
(s'il ne l'est pas au tirage, l'écart nommé — l'audit est probabiliste,
jamais présenté comme une preuve).

## 4. LA DÉCOMPOSITION DES 37 s DU BRAS T (la table publiée)

La session M4 du bras T (39,24 s la médiane v0.21.0 — 37,07 s l'effet
notation) décomposée PAR CONTRÔLE : rebuilds de cristallisation, round-trips,
recomposition du plan, oracles — chaque poste chronométré par
instrumentation du rig (l'horloge monotone, n≥5, la médiane), la table
publiée au manuscrit et aux preuves. La réconciliation : la somme des postes
== le total mesuré (l'écart nommé et borné sinon).

## 5. LA VÉRIFICATION APRÈS MODIFICATION (la lettre de l'instruction)

Parité observable avec le bloc scellé sur tous les vecteurs ; le contrôle
négatif attrapé ; cycles n≥20 médiane + IQR sur la même machine ; les
consoles d'oracle LIGNE-IDENTIQUES aux originales ; les empreintes scellées
intactes ; la réconciliation des totaux par étape avec contrôle négatif
injecté ; journal OPT + décision.
