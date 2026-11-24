# PLAN GELÉ — W17R1D81 (réconcilier D81 / D223 et les consignes actives)

> Instruction source : `/instructions/01_D81_D223.md`. Dépend du gel (W17R0GEL).

## Périmètre
1. Vérifier D81, D183, D223, D236 et leurs passages dans `REPRISE_PROJET.md`,
   `docs/DECISIONS.md`, `docs/PROTOCOLE_TRIADE.md`, le Livre du Coffre (source
   `scripts/livre_v17/`), les instructions actives, les README des kits.
2. Établir la **règle opérationnelle courante** : le séquestre 5/3 (D183 amendée par
   D223) est la garde active ; le statut de D81 doit être DATÉ et HISTORIQUE partout où
   il apparaît ; l'interdiction de phrase en clair (au dépôt, dans les packs, dans les
   rapports) doit être explicite dans toute procédure de reprise.
3. Corriger les consignes ACTIVES qui demanderaient encore de committer, pousser,
   restaurer ou téléverser un fichier de phrase en clair. Le verbatim historique n'est
   pas réécrit : erratum append-only si nécessaire.
4. Ajouter deux **tests négatifs** au linter : une consigne active reprenant l'ancien
   geste D81 est REFUSÉE ; une mention clairement datée comme historique est ADMISE.

## Fichiers touchés
- `docs/DECISIONS.md` : nouvelle décision (D252) actant la règle opérationnelle et son
  contrôle ; aucune réécriture des entrées 81/183/223/236.
- `docs/PROTOCOLE_TRIADE.md` : uniquement les passages prescriptifs de reprise/sauvegarde.
- Livre du Coffre : source LaTeX (`scripts/livre_v17/`) + erratum, jamais le PDF publié.
- `REPRISE_PROJET.md` : les consignes de reprise qui citeraient encore D81 au présent.
- `scripts/vague17/linter_v234.py` (nouveau, socle `scripts/vague16/linter_v233_residus.py`)
  avec les deux règles négatives.
- `atelier-w17-d81-d223/` : rapport, registre des occurrences (chemin, classe, résultat
  expurgé), sortie du linter.

## Hypothèses
- H1 : D236 (vague 8) a déjà purgé les instructions opératoires de remise D81 ; l'atelier
  est donc une VÉRIFICATION et un DURCISSEMENT, pas une réécriture — toute occurrence
  prescriptive restante est une régression à nommer.
- H2 : les mentions historiques datées (« De D81 au 19 novembre 2026 ») doivent demeurer
  intactes (append-only).
- H3 : le coffre réel n'est jamais touché (D105) ; le dossier `/Tokens` n'est pas ouvert.

## Critères d'acceptation
- Zéro occurrence PRESCRIPTIVE de remise/commit/push de `PHRASE-CONTROLE-COFFRE.txt`.
- Chaque occurrence restante classée HISTORIQUE-DATÉE, avec son ancre (fichier, section,
  date) dans le registre.
- Les deux tests négatifs verts, et le contrôle positif (mention datée admise) vert.
- Sceau-I vert au nombre d'arbres du manifeste, avant et après ; un commit seul.
- Aucune valeur secrète dans le rapport, le registre, le plan ou l'archive.

## Risques
- R1 : réécrire du verbatim → interdit ; erratum append-only.
- R2 : réintroduire un chemin de commit de phrase en « corrigeant » un runbook.
- R3 : un scan qui imprime une valeur trouvée → consigner chemin + classe + résultat
  expurgé seulement, jamais la valeur.

## Tests et preuves requis
- `grep` exhaustif sur le dépôt (hors `.git`, hors jetons), sortie expurgée.
- `python3 scripts/vague17/linter_v234.py --controle-negatif` : deux mutations plantées,
  deux refus attendus.
- `python3 v06/sceau_I.py verifier`.

## Dépendances
Gel (W17R0GEL). Aucune dépendance matérielle. Le geste de cérémonie (clé physique) reste
en attente explicite s'il est requis : jamais simulé.
