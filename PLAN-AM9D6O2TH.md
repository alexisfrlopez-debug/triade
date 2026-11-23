# PLAN GELÉ — AM9D6O2TH (l'audit d'étanchéité des splits du corpus d'entraînement)

> Le mandat : auditer l'étanchéité des splits du corpus d'entraînement — pour
> chaque identifiant de contrat (`loupe-XX`, `tls13-XX`, `sys-XX`), vérifier
> qu'AUCUN contrat n'apparaît à la fois dans TRAIN et dans DEV/TEST, toutes
> versions de campagne confondues (v3 et v4). Si une fuite inter-splits
> existe, re-générer les splits PAR GROUPE-DE-CONTRAT. Gelé AVANT toute
> lecture de split ; l'empreinte précède la première donnée.

## Le mandat

(1) **L'AUDIT** : la vérification mécanique, contrat par contrat, de la
présence dans les splits — l'identifiant de contrat est l'unité, jamais
l'instance de tâche. Deux contrats distincts portant le même identifiant
(comme `tls13-05` en v3 ET en v4) sont LE MÊME contrat pour l'étanchéité.

(2) **LA RÉPARATION SI FUITE** : la re-génération des splits par
GROUPE-DE-CONTRAT (group-by identifiant de contrat, graine consignée) au lieu
de par instance de tâche — en préservant le TEST SANS AUCUNE notation dorée
(les validateurs seuls) et le canari unique dans TRAIN.

(3) **LA MISE À JOUR** : la dataset card, le manifeste sha256 par fichier, le
vecteur de versions.

## Les gestes

1. Le plan gelé ; l'empreinte consignée ; LE COMMIT D'ABORD.
2. **L'AUDITEUR** : `scripts/vague16/auditer_splits.py` — déterministe, la
   table des contrats par split rendue, la fuite nommée contrat par contrat si
   elle existe.
3. **LA RÉPARATION** (si fuite) : le group-by contrat, la graine consignée, la
   preuve que TEST reste sans dorée et que le canari reste unique au TRAIN.
4. **LA CRISTALLISATION** : le re-jeu de l'extraction déterministe 10× (des
   rebuilds bit-identiques), la sonde de contamination (overlap n-gram +
   canari) entre TRAIN et TEST, la somme des triples par split contre le
   total, l'intégrité des juges de la chaîne v2 (les falsifications
   re-vertes).
5. **LE RAPPORT APPEND-ONLY AVEC LES EMPREINTES**.

## La vérification après modifications

Le re-jeu de l'extraction déterministe 10× (rebuilds bit-identiques) ; la sonde
de contamination entre TRAIN et TEST rend ZÉRO fuite de contrat ; la somme des
triples par split égale le total ; le TEST ne contient AUCUNE dorée ; le canari
UNIQUE au TRAIN ; les juges de la chaîne v2 intacts ; le rapport append-only
avec les empreintes ; le sceau-I 14/14 avant et après.

## Les refus

Jamais un split déplacé en silence ; jamais un canari hors du TRAIN ; jamais
une dorée au TEST ; jamais un compte qui ne somme pas ; jamais une fuite
trouvée et non nommée ; jamais une graine re-tirée.
