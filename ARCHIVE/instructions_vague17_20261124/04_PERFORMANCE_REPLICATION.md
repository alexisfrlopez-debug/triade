# PROMPT 04 — Séparer performance, coût de méthode et réplication

Exécute le plan gelé sur la fonction objectif, les preuves empiriques et la réplication externe.

1. Reprends les mesures réelles déjà consignées (bras compilateur, C+G/C+G+, coûts de notation, budgets tokens, mutations, tests de terrain). Vérifie leur périmètre, unité, environnement, taille d’échantillon, médiane/distribution et statut. Les nombres des anciens manuscrits ne sont pas des valeurs courantes sans vérification.
2. Sépare explicitement : (a) contrainte d’artefact natif sans compilateur, (b) performance d’exécution — latence, débit, mémoire, taille —, (c) coût d’édition et de validation — tokens, temps, calcul, (d) sûreté et couverture. Une propriété d’architecture ne doit pas servir de mesure de vitesse.
3. Compare des contrats et charges équivalents sur des conditions documentées et pré-enregistrées. Conserve les résultats défavorables, refus, pannes et runs incomplets ; pas de moyenne qui exclut un run sans règle préalable.
4. Décris le rôle des quatre bras de comparaison et du régime de gouvernance/vérification, afin d’attribuer les coûts à la notation, au processus ou à l’oracle. N’extrapole pas des mesures d’émulation en temps matériel.
5. Propose un paquet de réplication public qui protège la carte privée : sources publiques autorisées, contrats/fixtures, code d’analyse, graines, versions, manifestes et preuves expurgées. Indique séparément les éléments confidentiels et la procédure d’audit tiers autorisée. Ne publie pas I, C, secrets ou données personnelles.
6. Automatise la provenance des tableaux et résumés depuis des sources canoniques, et ajoute des contrôles négatifs qui mutent les valeurs, ratios, comptes et statuts. Conserve l’append-only pour les pièces historiques.

N’affirme qu’une mesure dont les données brutes et le plan pré-enregistré existent et sont recoupés. Mets à jour les tableaux et définitions selon le plan, vérifie les linter/contrôles négatifs, le sceau-I avant/après, puis committe cet atelier seul. Aucun nouvel essai matériel n’est simulé.
