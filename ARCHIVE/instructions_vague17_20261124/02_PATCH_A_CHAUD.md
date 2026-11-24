# PROMPT 02 — Spécifier la sûreté du patch à chaud

Exécute le plan gelé sur la bascule atomique x86-64 et l’exécution concurrente. La spécification décrit un trampoline de 12 à 16 octets installé par écriture alignée unique ; il faut vérifier précisément ce que garantit la primitive réelle du profil.

1. Consulte les manuels primaires du processeur, de Windows et les règles applicables au cache d’instructions. Distingue alignement, atomicité de l’accès mémoire, cohérence des instructions et état des threads.
2. Décris le mécanisme réellement employé par TRIADE à chaque profil : instruction ou API atomique, taille, alignement, disponibilité CPU, ordre mémoire, permissions de page, vidage du cache, rendez-vous/quiescence des threads et gestion d’un thread dont RIP se trouve dans la zone modifiée.
3. Formalise les états de la transaction : préparer nouveau bloc, rendre exécutable, publier la cible, vérifier, rollback, reprendre les threads. N’autorise pas l’exécution d’un état partiellement publié.
4. Compare les options compatibles avec les adresses stables de R7. Ne choisis pas une primitive non prouvée uniquement parce que l’écriture est alignée. Si l’architecture actuelle ne peut pas garantir la propriété annoncée, propose une modification minimale ou réduis explicitement la garantie.
5. Définis les préconditions, postconditions, cas de refus et vecteurs de test, incluant plusieurs threads, mises à jour concurrentes, rollback, interruption à chaque étape et limites de taille/alignement.
6. Sépare preuve statique, émulation et essais sur matériel réel. Si le métal requis n’est pas disponible, livre le kit falsifiable et marque le statut « en attente de run matériel » ; n’annonce aucun résultat.

Mets à jour la spécification et la décision seulement lorsque la conclusion s’appuie sur les sources et preuves du plan. Ne modifie aucun artefact scellé historique. Lance les tests et contrôles négatifs disponibles, vérifie le sceau-I avant/après, committe cet atelier seul et consigne les essais matériels encore dus. Pas de release dans ce prompt.
