# PLAN GELÉ — S2P9BM3ZD (la vague 14)
> L'atelier d'optimisation du régime pré-enregistré : H-CGP4 — à volumes égalisés
> 10×6=60 par bras, réduire la part RÉGIME du T−C sans retirer AUCUN contrôle.
> Gelé AVANT toute mesure ; la part régime 88,4 % est le hot path mesuré vague 13 (R11).

## Le mandat
H-CGP4 (énoncé falsifiable) : la mémoïsation content-addressée du régime réduit la
part régime du T−C aux volumes égalisés, SANS qu'aucun graine, vecteur ou contrôle
soit retiré. Trois leviers, chacun mesuré, composés à la fin :

(1) **MÉMOÏSATION CONTENT-ADDRESSED DU RÉGIME** : étendre le memo v2 aux 60
rebuilds (clé = sha256 de tout ce qui détermine le résultat : notation assemblée,
contrat, profil, graine, configuration moteur ; un octet changé = miss, le rebuild
court vivant) ; l'audit 1-sur-10 vivant CONSERVÉ et chaîné (le compteur signé
déclenche la re-exécution complète, le relevé confronté champ par champ) ;
(2) **ORACLE NATIF (OPT-07 préparé)** : livrer le moteur natif d'exécution des
oracles avec jumeau Unicorn sur échantillon d'audit consigné (divergence zéro
exigée, octet pour octet ; un shim muté du moteur natif REFUSÉ au premier nom —
la porte divise les moteurs honnêtes des faux) ;
(3) **CRISTALLISATION INCRÉMENTALE au graphe réel** (déjà −54 %) composée avec (1).

## La mesure
Quatre bras T / C+G+ / C+G / C, n≥5 par bras, ordre randomisé à graine consignée
AVANT le premier tirage, volumes égalisés (10 rebuilds × 6 unités = 60 par bras),
horloge monotone, listes de commandes figées par bras ; médianes non arrondies +
IQR ; la sommation des médianes vs médiane des sommes nommée.

## Les contrôles
Réconciliation par poste aux tolérances publiées (T ±0,150 s · C+G+ ±0,100 s ·
C+G, C ±0,050 s) ; consoles d'oracle ligne-identiques aux runs de régime (hors
horodatages nommés) ; scellés INTACTS avant/après chaque run ; contrôle négatif
+500 ms ATTRAPÉ aux deux fenêtres et attribué au premier nom ; rejeu des tirages
bit-identique.

## La vérification après modifications
Rejouer la ventilation complète (la part régime et la part notation publiées côte
à côte, dénominateur unique nommé) ; vérifier qu'AUCUNE graine retirée, AUCUN
vecteur réduit, AUCUN contrôle retiré (les 24 consoles ligne-identiques) ; l'audit
1-sur-10 déclenché et vert au moins une fois par bras ; re-mesure avant/après
consignée au journal OPT avec contrat stable ; sceau 14/14 ; consigner H-CGP4
(tenue/falsifiée) avec les chiffres datés, jamais fusionnés avec H-CGP2/H-CGP3.

## Les refus
Jamais un contrôle retiré pour gagner ; jamais le compteur d'audit contourné ;
jamais une miss de cache maquillée en exécution ; jamais les chiffres fusionnés
entre hypothèses.
