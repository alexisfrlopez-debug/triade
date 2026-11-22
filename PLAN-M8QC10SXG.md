# PLAN GELÉ — M8QC10SXG (la vague 15)
> L'atelier documentation : produire la doc du kit en anglais canonique, deux
> audiences, fragmentée comme la carte (aucune opération ne lit le manuel
> entier), les tables numériques générées depuis les canons (jamais retapées).
> Gelé AVANT toute génération ; les budgets de fragments pré-enregistrés.

## Le mandat
(1) **LA DOUBLURE DE DOCUMENTS** : QUICKSTART, DEVELOPER_GUIDE, TROUBLESHOOTING,
SECURITY, REFERENCE (humain, EN narratif) ; AGENT-CORE + DOC-LOC/EDIT/ADD/REFUS/
CEREMONY/FEEDBACK + CAPABILITY_PROBE (agent, EN compact) ; les identifiants de
refus et de décision/règle demeurent LITTÉRAUX (constantes du protocole, jamais
traduits) ; l'EN explique.
(2) **LES BUDGETS par fragment mesurés au tokenizer natif** (cibles : CORE
≤1500, opérations ≤800, REFUS ≤600, CEREMONY ≤1200, FEEDBACK ≤400, PROBE ≤500),
les opérandes non arrondis publiés au MANIFESTE ; UN FRAGMENT HORS BUDGET EST UN
REFUS NOMMÉ, jamais un budget silencieusement élargi.
(3) **LE MIROIR FR optionnel** généré des mêmes sources ; LE LINTER vérifie la
parité numérique EN/FR et l'identité des identifiants littéraux ; sha256 par
fichier au MANIFESTE ; la cristallisation 10 rebuilds bit-identiques.

## Les gestes
1. Le plan gelé ; les sources de doc (les gabarits, les canons branchés).
2. La génération des fragments humains + agents (tables numériques DEPUIS les
   canons, jamais retapées).
3. La mesure des budgets au tokenizer natif (tiktoken, les opérandes publiés).
4. Le linter doc (la parité numérique EN/FR, l'identité des identifiants
   littéraux) + LE CONTRÔLE NÉGATIF (une valeur numérique divergente plantée
   EN/FR DOIT être attrapée, un identifiant de refus traduit DOIT être attrapé).
5. Le MANIFESTE + la cristallisation 10×.

## La vérification après modifications
Contrôle négatif du linter vécu ; budgets re-mesurés à la même graine, opérandes
publiés ; aucune table numérique retapée (génération depuis canons vérifiée) ;
scan de secrets du kit vert (contrôle négatif planté attrapé) ; archive
déterministe 10× ; sceau du dépôt 14/14 avant/après si le générateur touche le
dépôt ; entrée append-only.

## Les refus
Jamais un identifiant traduit ; jamais une table retapée ; jamais un budget
élargi en silence ; jamais un fragment hors budget livré.
