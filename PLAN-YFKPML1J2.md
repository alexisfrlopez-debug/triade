# PLAN GELÉ — YFKPML1J2 (la vague 15)
> L'atelier TPL-ADD-v5 : porter AJOUTER de 7/18 à ≥15/18 au coût médian
> ≤4 500 tokens par changement validé, sans affaiblir AUCUN juge.
> Gelé AVANT toute donnée ; les 18 tâches et graines 20261117 reconduites, l'ordre
> jamais re-tiré.

## Le mandat
La vague 14 a porté TPL-ADD-v4 à 7/18 (la première conversion d'un refus honnête,
coût 3 990). Le présent atelier change la MÉTHODE, pas les juges :

(1) **LES MÊMES 18 TÂCHES, graines 20261117 reconduites**, ordre jamais re-tiré ;
budget 3 consigné par tentative au JSONL ; les juges v3/v4 INTACTS (round-trip
keystone==capstone==keystone, validateurs, mutation, oracle différentiel).
(2) **LA RÉPARATION PAR DIFF D'EXPANSION STRUCTURÉ** : l'expandeur rend le diff
EXACT au niveau opcode/opérande/offset (PAS texte) ; le prompt de réparation
porte CE diff + les motifs canoniques ; le normaliseur canonique à la sortie de
l'expandeur (la forme canonique est celle que le juge compare déjà — aucun juge
affaibli).
(3) **LA GRAMMAIRE À TROUS TYPÉS versionnée par domaine** (dictionnaire de
domaine), l'exemplaire par plus proche contrat (référence littérale du dépôt).
(4) **LE DÉCODAGE CONTRAINT** si un endpoint local l'expose, sinon l'écart
d'instrument NOMMÉ.

## Les gestes
1. Le plan gelé ; l'infrastructure v5 (campagne_v5.py, l'expandeur à diff
   structuré, le normaliseur canonique, le dictionnaire de domaines).
2. La campagne sur les 18 tâches, budget 3 par tentative, tout consigné au JSONL
   (garde-brut, prompts archivés, resultats canoniques).
3. Les contrôles de falsification des juges re-verts (un octet muté au home
   space reste attrapé ; gle 87 → −6).
4. La re-tokenisation indépendante ±1 token ; le déplacement v4→v5 par classe
   consigné (conversions ET pertes).

## La vérification après modifications
Contrôles de falsification re-verts ; re-tokenisation indépendante ±1 token ;
refus nommés par classe au registre append-only ; AUCUN re-tirage ; le
déplacement v4→v5 par classe consigné ; sceau 14/14 ; entrée append-only.

## Les refus
Jamais un juge affaibli ; jamais les graines re-tirées ; jamais une tâche
remplacée ; jamais un échec masqué — la lecture défavorable consignée si la
cible est manquée.
