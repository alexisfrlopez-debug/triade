# PLAN PRÉ-ENREGISTRÉ — LA VAGUE 9, L'INSTRUCTION bkobf06nu : L'OPTIMISATION DE LA BOUCLE DE VÉRIFICATION (la vérification incrémentale, le double moteur à l'ouverture de session, le régime « oracle natif », la mesure M4)

> Pré-enregistré AVANT toute mesure (la règle D204/D211 reconduite : le
> présent plan, son empreinte sha256 consignée au journal, PRÉCÈDE la
> première donnée de la présente atelier). Aucun contrôle retiré, aucune
> graine supprimée, aucun vecteur réduit, LE JUGE NE PARTAGE JAMAIS
> L'ÉTAT DU JUGÉ (le refus de la vague 5 reconduit).

## 1. LES HYPOTHÈSES (falsifiables, pré-enregistrées)

H1 — LA VÉRIFICATION INCRÉMENTALE : le graphe de dépendances
I↔C↔B↔tests construit depuis la carte (les dépendances des entrées, le
réseau des specs de l'oracle structurel, les héritages R7), la
vérification devient UNE FONCTION DU DIFF : un changement au bloc X ne
re-vérifie QUE X et ses dépendants transitifs ; les blocs scellés
INCHANGÉS portent leur CERTIFICAT DE CRISTALLISATION (lié à l'empreinte
du bloc ‖ du contrat ‖ de la configuration ; TOUT écart force le rejeu
complet). Attente : la session d'ouverture ne re-joue pas les blocs
certifiés — le temps de vérification d'un diff d'UN bloc tombe de
l'ordre de la session complète à l'ordre du bloc + ses dépendants.

H2 — LE DOUBLE MOTEUR À L'OUVERTURE (le chemin chaud des condensés
émulés sur FICHIER ENTIER) : le volume sous QEMU-user (le lanceur C
statique, la même image que le harnais — les octets PAR CONSTRUCTION
identiques) avec COMPTEUR PAR BLOC ; l'échantillon d'audit sous Unicorn
(la référence, TEL QUEL, D185) ; la clé de mémo ÉTENDUE à tout ce qui
détermine le résultat (le bloc, l'entrée, le contrat, la configuration
émulateur, la graine, l'oracle, LE FICHIER ENTIER condensé — la clé v2
sur-ensemble de D222). Attente : divergence 0 octet pour octet entre
les deux moteurs sur le volume consigné.

H3 — LE RÉGIME « ORACLE NATIF » (le troisième régime de preuve) : un
exécuteur Windows AUTOMATISÉ (le runner CI) qui exécute les octets
scellés et les scénarios, produit des TÉMOINS HASHÉS ET SIGNÉS, les
confronte aux attentes du laboratoire. CE QU'IL ATTRAPE : l'écart
émulation/native (le comportement des octets scellés au VRAI Windows —
l'ABI, l'IAT, les feuilles kernel32 réelles) ; CE QU'IL N'ATTRAPE PAS :
la mesure du terrain du développeur (la machine du maître, ses
conditions), la preuve de sûreté face aux entrées non fiables à volume
(harnais), la mesure de performance en régime (l'horloge du CI n'est
PAS l'horloge du terrain). IL N'EST JAMAIS CONFONDU avec le terrain du
développeur : TOUT résultat du régime natif est NOMMÉ « natif » partout
où il apparaît. Le régime est PRÉPARÉ au laboratoire (le runner, les
scénarios, la confrontation, les témoins signés) — SON EXÉCUTION vit au
Windows du CI, le delta au modèle de menace consigné aux DEUX bords.

H4 — LA MESURE M4 : la liste de commandes fixe de la campagne (le
runner vljfs6pcj TEL QUEL, AUCUNE étape ajoutée, AUCUNE retirée),
horloge monotone, n≥5 par configuration, la même machine ; le bras C
re-mesuré à la même session. Attente : l'avant médiane ~39 s (le canon
39,1 de la vague 8 à ±1,5 s), le chaud médian ~6,6 s à ±1 s, le bras C
~1,9 s ; TOUT écart défavorable NOMMÉ (le record consigné tel quel).

## 2. LE GRAPHE DE DEPENDANCES ET LES CERTIFICATS (H1)

LA SOURCE : la carte du domaine loupe (les entrées : deps, héritages,
slots — LUES du plan et du build, la carte demeurant scellée) + le
réseau des specs (l'oracle structurel 43 verrous — les feuilles IAT par
bloc, les dépendances inter-blocs) + les tests (les vecteurs par bloc).
LA CONSTRUCTION : verifier_incrementale.py — le graphe orienté (bloc →
dépendants transitifs), le certificat = sha256(bloc assemblé ‖ contrat
‖ configuration de vérification ‖ empreinte d'oracle) SIGNÉ par la clé
de TEST publique du sceau-I (le modèle D214 : le mémo n'est jamais
cru, chaîne et signature recalculées à chaque chargement). LE REJEU :
un diff au bloc X → la re-vérification de X et de ses dépendants
transitifs SEULEMENT ; les certificats intacts portent la preuve. LE
CONTRÔLE NÉGATIF : un certificat VOLONTAIREMENT FALSIFIÉ (le bloc, le
contrat OU la configuration changé) force le REJEU COMPLET et est
refusé NOMMÉMENT (CERTIFICAT-DIVERGENT) — les TROIS variantes vécues.

## 3. LE DOUBLE MOTEUR À L'OUVERTURE (H2)

LE VOLUME : le lanceur C (l'atelier cq01qv1za reconduit : l'ELF64
statique lié haut, les shims ms_abi aux SIX feuilles kernel32, les
sentinelles, le LANDING) exécuté sous qemu-x86_64 1:10.0.13 (extrait
sans root, l'empreinte consignée) — LE COMPTEUR PAR BLOC : chaque
opération d'ouverture de session traverse les blocs ; le compteur
nomme LE BLOC exécuté (le routage nommé aux deux sens, la règle
OPT-01). L'ÉCHANTILLON : le MÊME programme au harnais Unicorn — la
comparaison octet pour octet des deux flux EST l'audit (divergence 0
exigée sur le volume consigné). LA CLÉ ÉTENDUE : la mémo v2 + le
condensé du FICHIER ENTIER (tout ce qui détermine le résultat — la
règle D222 étendue à l'ouverture).

## 4. LE RÉGIME ORACLE NATIF (H3 — PRÉPARÉ, PAS EXÉCUTÉ AU LABO)

LE LIVRABLE : oracle_natif/ — le runner Windows (le script CI :
l'acquisition de l'image, l'exécution des octets scellés aux adresses
du plan, les scénarios de la campagne, le témoin hashé + signé, la
confrontation aux attentes), le manifeste des attentes (les vecteurs
dorés, les oracles hashlib), la documentation CE QU'IL ATTRAPE / CE
QU'IL N'ATTRAPE PAS, la décision append-only + le delta au modèle de
menace AUX DEUX BORDS. LE CONTRÔLE NÉGATIF (au labo) : un SHIM DE
LANCEUR MUTÉ attrapé À LA PREMIÈRE LIGNE (le témoin signé refuse le
lanceur divergent — la falsification vécue au labo sur le mécanisme de
confrontation).

## 5. LA MESURE M4 (H4)

LE PROTOCOLE : le runner outil_m4_v182.py reconduit TEL QUEL (la liste
fixe, la garde-sceau-I, la cristallisation 12 rebuilds, les round-trips,
les deux oracles, l'épreuve, l'assemblage) — les modes avant (les
outils v180), froid, chaud (l'audit 1/10 vit au compteur), le bras C
(mesure_c_v182.py). n=5 par configuration. LES CONSOLES capturées
INTÉGRALEMENT — l'identité ligne à ligne avec les originales exigée
(24 consoles). LES EMPREINTES SCELLÉES avant/après CHAQUE exécution.

## 6. LES RÈGLES DE VERDICT PRÉ-ENREGISTRÉES (fail-closed)

  - les 24 consoles d'oracles CAPTURÉES ligne-identiques aux originales ;
  - le rejeu complet de la batterie de mutation AUX MÊMES GRAINES :
    811/832 intact, AUCUN tueur affaibli ;
  - le certificat incrémental falsifié (bloc, contrat, configuration)
    force le rejeu complet — refus nommé, les trois variantes ;
  - les empreintes des artefacts scellés INTACTES avant/après chaque
    run ; l'expansion client verte ; zéro divergence ;
  - le régime natif NOMMÉ partout où ses résultats apparaissent ;
  - le contrôle négatif : le shim de lanceur muté attrapé à la
    première ligne ;
  - tout écart défavorable NOMMÉ au rapport (jamais lissé).

## 7. LA CONSIGNATION

OPT-07 (la vérification incrémentale + le double moteur à l'ouverture)
au journal d'optimisation (format D205) ; la décision append-only du
régime natif (le troisième régime, le delta au modèle de menace) ; la
décision append-only du certificat de cristallisation ; les gains
consignés avant/après avec les conditions nommées ; la présente
empreinte au journal AVANT la première donnée.
