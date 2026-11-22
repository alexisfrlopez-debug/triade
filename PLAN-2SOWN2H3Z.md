# PLAN GELÉ — 2SOWN2H3Z (la vague 15)
> L'atelier de la MESURE SUIVANTE nommée à l'Entrée 385 : la composition entrelacée
> CTR v4i × GHASH agrégé-4 — la projection ~1,6 c/octet@4096 DOIT devenir une
> mesure, cible pré-enregistrée ≤2,0 c/octet@4096.
> Gelé AVANT toute mesure ; l'empreinte du présent plan précède la première donnée.

## Le mandat
Le corridor v13 (GHASH agrégé 19,66 c/mult, l'AES-CTR dispatché) porte une
projection d'entrelacement ~1,6 c/octet@4096 ; la vague 14 l'a nommée « la MESURE
SUIVANTE ». Le présent atelier la mesure :

(1) **L'ENTRELACEMENT PAR GROUPES DE QUATRE** : construire l'entrelacement
CTR v4i × GHASH agrégé-4 dans le rig natif du corridor (les canaux rejoints par
groupes de quatre blocs) ; LE REPLI testé vers la chaîne scellée (le fallback
32/32 — l'entrelacement échoue → la chaîne de référence reprend, sans état corrompu).
(2) **LA DIFFÉRENTIELLE** : ≥320 vecteurs (graine consignée AVANT le premier
tirage) contre la chaîne de quatre appels scellés — zéro écart exigé octet pour
octet ; le mutant imm8 ATTRAPÉ au premier vecteur (la porte divise le rig honnête du faux).
(3) **LA MESURE** : RDTSCP n≥20, cœur épinglé, fréquence fixée, machine
virtualisée NOMMÉE (l'écart VM/métal nu nommé, jamais masqué) ; la baseline
OpenSSL EVP même machine même entrée ; LE PROTOCOLE MÉTAL NU (≥2 machines)
pré-enregistré pour le geste développeur — le laboratoire prépare le kit, ne simule jamais.
(4) **LE TRACE-HASH TEMPS-CONSTANT STRUCTUREL** : une empreinte par classe.

## Les gestes
1. Le plan gelé ; la cible ≤2,0 c/octet@4096 PRÉ-ENREGISTRÉE à l'empreinte.
2. Le rig entrelacé (notation assemblée depuis le corridor v13, groups-of-4) ;
   round-trip keystone==capstone==keystone exigé.
3. La différentielle ≥320 vecteurs ; le mutant imm8 ; le repli 32/32.
4. La mesure RDTSCP n≥20 + baseline OpenSSL EVP ; les opérandes NON ARRONDIS
   consignés (c/octet@4096, l'IQR, la machine, la fréquence).
5. Le kit métal nu pré-enregistré (le protocole, pas le chiffre).

## La vérification après modifications
Round-trip triple vert ; différentielle zéro divergence ; repli 32/32 ; sceau 14/14
et empreintes scellées intactes ; AUCUNE projection présentée comme mesure ;
l'écart VM/métal nu nommé ; entrée append-only avec opérandes non arrondis.

## Les refus
Jamais une projection habillée en mesure ; jamais le repli escamoté ; jamais la
machine virtualisée maquillée en métal nu ; jamais un vecteur retiré.
