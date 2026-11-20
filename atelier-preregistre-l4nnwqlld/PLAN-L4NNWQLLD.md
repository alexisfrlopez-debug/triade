# PLAN PRÉ-ENREGISTRÉ — LA VAGUE 11, L'INSTRUCTION l4nnwqlld : LES KITS ET PLANS QUI FERMENT LES LIGNES « AWAITING » — HASHÉS AVANT TOUTE MESURE

> Pré-enregistré AVANT toute livraison (l'empreinte sha256 consignée à
> EMPREINTES-PLANS-VAGUE11.txt, commitée AVANT le premier kit).
> LA RÈGLE DE L'INSTRUCTION : « aucun résultat n'est produit sans le geste
> du développeur » — la présente LIVRE des kits et des plans HASHÉS ; aucune
> mesure n'est prise.

## 1. LE KIT FENCE.I SUR CARTE RV64 PHYSIQUE (M7 au silicium)

Le kit : le scénario M7 retargeté (la fiche de la carte visée — RV64GC, le
profil riscv64-linux-elf64), le script de préparation (le cross-assembleur,
la séquence fence.i + la bascule du registre scratch, le témoin signé), le
protocole d'acceptation (les critères mesurés : la bascule vue par le cœur,
l'invalidation du cache d'instructions prouvée au témoin, n≥5 runs), LA
GRILLE DE TÉMOIN (le format du fichier signé que le développeur retourne).
L'empreinte du kit consignée AVANT la remise.

## 2. LE KIT LOUPE TROISIÈME MACHINE (T0→T7+S0 intégral)

Le scénario complet T0→T7+S0 (le même que la campagne D204, la machine de
record + la seconde) : le paquet (l'exécutable, les données de test, le
script d'orchestration), la feuille de route pas à pas, LA GRILLE DE TÉMOIN
(le journal + les empreintes des sorties, signés). Le protocole exige
l'EMPREINTE CPU et la fréquence consignées au témoin.

## 3. LE PROTOCOLE DUDECT (n≥10 par N∈{60,200,400} sur ≥2 machines)

Le protocole : le kit dudect retargeté (les quatre cibles — tls13-02/13
comprises), n≥10 RUNS par N∈{60, 200, 400}, ≥2 machines, L'EMPREINTE CPU ET
LA FRÉQUENCE CONSIGNÉES, l'affinité de cœur fixée ; L'INVESTIGATION DES PICS
tls13-02/tls13-13 À N=200 PRÉ-ENREGISTRÉE (l'hypothèse de cause écrite
AVANT les données — la fausse cache du compilateur, l'alias de ligne, le
partage de port — chaque cause testable nommée avec son test discriminant) ;
LA RÈGLE DE JUGEMENT gelée (le seuil t, la correction de Welch, la décision
par cible). L'agrégateur FAIL-CLOSED : tout run manquant = le protocole
REFUSÉ (jamais d'agrégat partiel).

## 4. LA CAMPAGNE H7 (randomisation stratifiée garantissant le contraste d'ordre)

Le plan : H7 (l'effet d'ordre des livraisons) exige le CONTRASTE — la
randomisation STRATIFIÉE (les unités appariées par famille, l'ordre tiré
DANS les strates, la graine consignée, le nombre de tirages garanti
contraint par le plan de puissance — α=0,05, puissance 0,8, l'effet
attendu dérivé des campagnes D204/D210) ; les critères d'arrêt et la règle
de jugement gelés AVANT le premier tirage réel.

## 5. LE RECRUTEMENT DU SECOND ANNOTATEUR (la grille F/L, κ≥0,61)

Le kit de recrutement : LA GRILLE F/L (les classes de défauts — les
fausses négatives/positives par axe), LES CONSIGNES D'ANNOTATION (le
manuel, les exemples étalonnés), LE CALCULATEUR κ AUTOTESTÉ (les cas
synthétiques — l'accord attendu exact par construction), LA RÈGLE
D'ACCEPTATION (κ ≥ 0,61 Landis-Koch modéré, n≥50 items doubles), le
protocole d'arbitrage des désaccords.

## 6. LE MODÈLE CF3 EN TAMARIN (l'indépendance au niveau du modèle)

Le modèle : CF3.spthy — les actions du protocole (la création du coffre,
la migration CF1→CF2→CF3, le changement de phrase sous séquestre, la
destruction locale), les lemmas de sécurité (la non-divulgation de la
phrase sous le seuil, la conservation de la clé utilisateur, l'absence de
destruction par corruption), LA RÈGLE DE RESTRICTION nommée (l'attaquant
Dolev-Yao au seuil des parts) ; le modèle livré HASHÉ avec son protocole
de vérification (les commandes, les lemmas, les bornes) — la vérification
au geste du développeur (Tamarin au poste réel, le gap nommé si le bac ne
le porte pas).

## LA VÉRIFICATION APRÈS MODIFICATION (la lettre de l'instruction)

Les autotests des kits VERTS sur fixtures synthétiques ; les empreintes des
plans pré-enregistrées et verrouillées ; l'agrégateur fail-closed refusant
tout run manquant ; la table des statuts INCHANGÉE tant que les témoins
signés ne sont pas recoupés ; la décision consignée.
