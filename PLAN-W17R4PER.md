# PLAN GELÉ — W17R4PER (séparer performance, coût de méthode et réplication)

> Instruction source : `/instructions/04_PERFORMANCE_REPLICATION.md`. Dépend du gel
> (W17R0GEL). Objet : ne plus confondre la contrainte d'architecture avec une mesure de
> vitesse, et rendre chaque nombre du dossier traçable à une source canonique.

## Périmètre
1. Reprendre les mesures RÉELLES déjà consignées : bras compilateur (bras C, bras C+G,
  C+G+), coûts de notation, budgets tokens (40/200 par bloc, 627/674/2 200 par changement,
  34 663 tokens de gouvernance mesurés), 832 mutants (93,3 %), le facteur 15,3 RETIRÉ par
  D191, médiane 4 604 tokens, décomposition des 37 s du bras T, ratio de régime 3,5×.
  Vérifier pour chacune : périmètre, unité, environnement, taille d'échantillon,
  médiane/distribution, statut (mesuré / émulé / en attente).
2. Séparer explicitement quatre grandeurs : (a) contrainte d'artefact natif sans
  compilateur, (b) performance d'exécution (latence, débit, mémoire, taille), (c) coût
  d'édition et de validation (tokens, temps, calcul), (d) sûreté et couverture.
3. Décrire le rôle des quatre bras de comparaison et du régime de
  gouvernance/vérification, pour attribuer les coûts à la notation, au processus ou à
  l'oracle.
4. Proposer un **paquet de réplication public** qui protège la carte privée : sources
  publiques autorisées, contrats/fixtures, code d'analyse, graines, versions, manifestes,
  preuves expurgées ; éléments confidentiels et procédure d'audit tiers listés à part.
5. Automatiser la provenance des tableaux et résumés depuis les sources canoniques
  (JSONL committés), avec contrôles négatifs mutants.

## Fichiers touchés
- `docs/JOURNAL_OPTIMISATION.md` (définitions et tableaux, statut par ligne).
- Manuscrit de l'édition courante (`scripts/vague15/pack-v233/1-manuscrit/`) — tableaux
  régénérés depuis les sources, jamais édités à la main.
- `scripts/vague17/provenance_tableaux.py` (nouveau : extraction → tableaux) et
  `scripts/vague17/linter_v234.py` (classes ratios/comptes/statuts, contrôle négatif).
- `replication-v17/` (nouveau : paquet public, README d'audit, liste des pièces
  confidentielles exclues).
- `atelier-w17-performance-replication/` : rapport, registre des mesures avec statut.

## Hypothèses
- H1 : les JSONL committés (campagnes v5/v6, corpus v2.1) sont la source canonique ; le
  `campagne-v5.log` gitignoré ne doit plus être une dépendance du linter (défaut nommé à
  l'Entrée 397).
- H2 : aucune mesure nouvelle au métal n'est possible ici → toute ligne non rejouable
  reste « en attente » ou « historique », jamais « courante ».
- H3 : aucune donnée de la couche I, de la carte C, ni aucune donnée personnelle ne peut
  entrer dans le paquet public.

## Critères d'acceptation
- Chaque nombre cité dans les tableaux porte : source canonique, graine/version,
  n, unité, statut.
- Les quatre grandeurs (a)-(d) ne sont jamais additionnées ni comparées entre elles.
- Résultats défavorables, refus et runs incomplets conservés ; aucune moyenne excluant un
  run sans règle pré-enregistrée.
- Contrôles négatifs : mutation d'une valeur, d'un ratio, d'un compte et d'un statut →
  quatre refus attendus.
- Paquet de réplication : aucun I/C, aucun secret ; liste explicite des éléments
  confidentiels et de la procédure d'audit tiers.
- Sceau-I avant/après ; un commit seul.

## Risques
- R1 : présenter une propriété d'architecture comme une mesure de vitesse.
- R2 : moyenne habillée (exclusion d'un run décidée après coup).
- R3 : fuite de la carte privée dans le paquet public.
- R4 : dérive d'extracteur (pdftotext) prise pour un écart de contenu — leçon de
  l'Entrée 397 : épingler l'extracteur ou porter l'extraction.

## Tests et preuves requis
- Régénération automatique des tableaux → diff nul avec l'édition courante (ou écart
  nommé et justifié).
- Linter avec contrôle négatif (4 mutations, 4 refus).
- Recoupement d'une mesure par re-calcul depuis les JSONL (médiane, ratio, comptes).

## Dépendances
Gel (W17R0GEL). Aucune dépendance matérielle pour la provenance ; les mesures au métal
restent en attente nommée.
