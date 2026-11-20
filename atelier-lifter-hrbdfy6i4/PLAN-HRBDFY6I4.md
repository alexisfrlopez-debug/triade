# PLAN PRÉ-ENREGISTRÉ — LA VAGUE 11, L'INSTRUCTION hrbdfy6i4 : LA SOUNDNESS DU LIFTER AU-DELÀ DU ROUND-TRIP, LE STATUT DE H, LA COUVERTURE ÉTENDUE

> Pré-enregistré AVANT toute mesure (l'empreinte sha256 consignée à
> EMPREINTES-PLANS-VAGUE11.txt, commitée AVANT la première donnée).

## 1. LA SOUNDNESS DU LIFTER CONFRONTÉE À L'OBSERVÉ (la validation exigée)

Le round-trip (13/13) prouve la ré-versibilité d'encodage, PAS la justesse
des ENSEMBLES LUS/ÉCRITS que le lifter déclare (les registres et la mémoire
lus/écrits par instruction — la base de la preuve de non-interférence).
LA VALIDATION : pour CHAQUE instruction des blocs couverts, les ensembles
read/write DU LIFTER confrontés aux accès OBSERVÉS PAR UNICORN — le hook
par instruction (les registres lus : le diff des valeurs avant/après +
les opérandes sources ; la mémoire : les hooks UC_MEM_READ/WRITE avec
adresses et tailles exactes) ; la comparaison INSTRUCTION PAR INSTRUCTION.

LE CORPUS : (1) les 13 blocs couverts (tls13-01/02/03/05/06/07/13/14/15/16/
18/19 + loupe-06) ; (2) UN CORPUS D'INSTRUCTIONS MUTÉES — chaque mnémonique
des blocs muté systématiquement (l'octet d'opcode/ModRM parcouru), les
mutants valides (l'assembleur les accepte) confrontés au lifter — zéro
divergence exigée sur tout le corpus. LE CONTRÔLE NÉGATIF : le lifter muté
(son modèle d'ensemble altéré d'une instruction) ATTRAPÉ à la première
divergence.

## 2. LE STATUT DE SECRET DE H DANS GHASH (H = E_K(0))

LA QUESTION : H (la clé de hachage GHASH, dérivée de la clé AES) est-elle
un SECRET au sens de la non-interférence ? DEUX VOIES, la décision gelée
ici : (1) LE CONTRAT LE DÉCLARE PUBLIC avec justification — H n'entre QUE
dans le calcul du tag (une sortie publique), par des opérations SANS
BRANCHE ni ACCÈS À ADRESSE DÉPENDANTE (PCLMULQDQ/shifts non conditionnels —
la preuve exigée : le taint de H ne tache AUCUNE branche ni aucune adresse,
le même critère que les secrets) ; (2) SINON couvrir tls13-17 (GHASH) avec
H TAINTÉ COMME SECRET. LA VOIE CHOISIE : la couverture directe de tls13-17
avec H secret (la voie forte — aucune justification à porter), PLUS la
preuve que le taint de H ne tache ni branche ni adresse (qui vaut la
déclaration de toute façon au rapport).

## 3. LA COUVERTURE ÉTENDUE (tls13-04 et tls13-08 — ou le trou résiduel nommé)

tls13-04 (la poignée de main) et tls13-08 (la réception) — les blocs non
couverts nommés par la vague 10. LA VOIE : étendre la couverture (les
secrets nommés : les clés de session, le secret du trafic) SI le lifter
porte leurs instructions (sinon LE TROU RÉSIDUEL NOMMÉ au tableau de
couverture — blocs ET familles, jamais une globalité).

## 4. LA RE-DÉCHARGE DE LA NON-INTERFÉRENCE (la couverture étendue)

La preuve re-roulée sur la couverture étendue (13 + 17 [+ 04/08 si portés])
— les taints propagés, zéro branche/accès tainté exigé, le contrôle négatif
(une branche sur secret injectée) ATTRAPÉ, LA COUVERTURE PUBLIÉE EN BLOCS
ET FAMILLES avec les trous nommés, le hash de trace temps-constant reconduit.

## LA VÉRIFICATION APRÈS MODIFICATION (la lettre de l'instruction)

Zéro divergence des ensembles read/write sur le corpus ; le contrôle
négatif (lifter muté) attrapé à la première divergence ; le round-trip
13/13 (ou la couverture étendue) intact ; le taint re-joué avec zéro
branche/accès tainté sur les blocs couverts ; la couverture publiée en
blocs ET familles avec trous nommés ; la décision consignée.
