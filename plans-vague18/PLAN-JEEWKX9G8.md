# PLAN GELÉ — JEEWKX9G8 — la liste blanche fermée des sources prescriptives

## L'instruction, en une phrase
Remplacer la détection heuristique du prescriptif par un manifeste racine
`SOURCES-PRESCRIPTIVES.txt` (chemin + sha256), une règle fail-closed dans le guide
agent (toute instruction de geste hors liste → SOURCE-NON-PRESCRIPTIVE), un scan de
tout l'arbre, et la garde au pre-commit ; le linter v234 reste en seconde ligne.

## Le geste
(a) le manifeste : les SEULS fichiers autorisés à prescrire (AGENTS.md, REVUE…, les
plans ?) — la liste est COURTE et motivée ; (b) `garde_prescriptif.py` : liste blanche
d'abord (indépendante des mots-clés), heuristique ensuite ; (c) le scan de tout
l'arbre lisible, classification lecture-seule ; (d) l'entrée au pre-commit ;
(e) les fixtures d'autotest (a)–(d) de l'instruction.

## Vérification exigée
Autotest (a) hors liste REFUSÉE ; (b) dans la liste ADMISE ; (c) reformulation inédite
hors liste REFUSÉE ; (d) fichier historique daté ADMIS en lecture ; scan complet
0 consigne active hors liste ; les comptes et les empreintes au journal, sans
imprimer aucun contenu de ligne.
