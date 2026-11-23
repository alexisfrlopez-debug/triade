# PLAN GELÉ — IO3UH37CJ (les couloirs de performance scellés et le kit de mesure métal nu)

> Le mandat : sceller les couloirs de performance de laboratoire par la
> procédure lourde, préparer le kit de mesure MÉTAL NU (≥ 2 machines), explorer
> l'agrégation GHASH 8 blocs + VAES/VPCLMULQDQ, et mesurer le SURCOÛT TOKEN de
> la gouvernance. Gelé AVANT toute mesure ; l'empreinte précède la première
> donnée.

## Le mandat

(1) **LE SCELLEMENT** : la composition CTR × GHASH 0,7271 c/B, AES-NI 7,09
c/bloc, GHASH agrégé 19,66 c/mult — par la procédure lourde : la
cristallisation 10 rebuilds bit-identiques, la cérémonie d'ère du sceau, le
round-trip keystone == capstone == keystone, la différentielle contre la
chaîne scellée (zéro écart), le temps-constant trace-hash (une empreinte par
classe), les bornes fail-closed. Le couloir devient un ARTEFACT SCELLÉ à
adresse stable (R4/R7), plus une variante de marge.

(2) **LE KIT MÉTAL NU** (≥ 2 machines) : l'empreinte CPU, l'état de fréquence,
le cœur épinglé, la même entrée, l'agrégateur fail-closed — PRÉPARÉ, pas
exécuté au laboratoire (la machine nue est le geste du développeur).

(3) **L'EXPLORATION** : l'agrégation GHASH 8 blocs + VAES/VPCLMULQDQ avec
dispatch CPUID et repli scellé, **sans retirer aucun contrôle**.

(4) **LE SURCOÛT TOKEN DE GOUVERNANCE** : mesuré par changement (sceau,
linter, cristallisation), publié à côté des budgets 627 / 674 / 2 200 ; la
surface de gouvernance lue par l'agent compressée, la réduction mesurée.

## Les gestes

1. Le plan gelé ; l'empreinte consignée ; LE COMMIT D'ABORD.
2. **LE HARNAIS DE CRISTALLISATION** : 10 rebuilds bit-identiques, le
   round-trip keystone == capstone == keystone, la différentielle contre la
   chaîne scellée, le temps-constant trace-hash.
3. **L'ARTEFACT SCELLÉ** : le couloir à adresse stable (R4/R7) + la variante
   de marge, les bornes fail-closed (N=0 / N=257 refusées).
4. **LE KIT MÉTAL NU** : le manifeste de mesure (empreinte CPU, fréquence,
   cœur épinglé, même entrée), l'agrégateur qui REFUSE (exit 2) un run
   manquant — testé au laboratoire sur un jeu incomplet.
5. **L'EXPLORATION VAES/VPCLMULQDQ** : le dispatch CPUID et le repli scellé
   32/32 ; le surcoût gouvernance mesuré et publié.

## La vérification après modifications

La différentielle et le temps-constant rejoués sur le couloir scellé (zéro
divergence, une empreinte par classe) ; le repli scellé 32/32 ; les bornes
N=0 / N=257 REFUSÉES ; les empreintes avant/après recoupées (aucune pièce
scellée antérieure ne bouge) ; l'agrégateur métal nu sur un run manquant
(REFUS, exit 2, jamais un verdict partiel) ; le ratio perf recalculé depuis
les opérandes non arrondis ; la lecture honnête (VM contre métal nu) et le
surcoût gouvernance mesuré, append-only.

## Les refus

Jamais un verdict partiel ; jamais un contrôle retiré ; jamais une mesure sans
son empreinte CPU ; jamais un chiffre de VM habillé en métal nu ; jamais une
borne franchie en silence ; jamais un artefact scellé déplacé sans cérémonie.
