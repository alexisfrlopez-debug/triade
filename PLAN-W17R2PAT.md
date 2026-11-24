# PLAN GELÉ — W17R2PAT (sûreté du patch à chaud, x86-64, exécution concurrente)

> Instruction source : `/instructions/02_PATCH_A_CHAUD.md`. Dépend du gel (W17R0GEL).
> Matière première : la spécification décrit un trampoline de 12 à 16 octets installé par
> une écriture alignée unique — la question est de savoir ce que la primitive RÉELLE
> garantit, par profil.

## Périmètre
1. Consulter les manuels primaires (Intel SDM vol. 3 — cohérence des instructions et
   auto-modification ; AMD APM ; documentation Windows sur la modification de code en
   cours d'exécution) et les règles applicables au cache d'instructions.
2. Distinguer sans les confondre : alignement, atomicité de l'accès mémoire, cohérence
   des instructions, état des threads.
3. Décrire, **par profil** (x86-64 Windows PE, x86-64 Linux ELF, RISC-V), le mécanisme
   réellement employé : instruction ou API atomique, taille, alignement, disponibilité
   CPU, ordre mémoire, permissions de page, vidage du cache, rendez-vous / quiescence
   des threads, traitement d'un thread dont RIP se trouve dans la zone modifiée.
4. Formaliser les états de la transaction : préparer le nouveau bloc, rendre exécutable,
   publier la cible, vérifier, rollback, reprendre les threads. Aucun état partiellement
   publié ne doit être exécutable.
5. Comparer les options compatibles avec les adresses stables de R7 ; ne pas retenir une
   primitive non prouvée au seul motif que l'écriture est alignée. Si l'architecture ne
   peut pas garantir la propriété annoncée, réduire la garantie explicitement ou proposer
   la modification minimale.
6. Définir préconditions, postconditions, cas de refus et vecteurs de test.

## Fichiers touchés
- `docs/PROTOCOLE_TRIADE.md` : section bascule/patch à chaud (garantie reformulée).
- `docs/PROFIL_x86-64-linux-elf64.md`, `docs/PROFIL_riscv64-linux-elf64.md` : mécanisme
  par profil.
- `docs/DECISIONS.md` : nouvelle décision (D25x) consignant la garantie retenue et ses
  limites, avec les alternatives rejetées (patch binaire, redémarrage, double map).
- `docs/FORMAT_CARTE.md` : uniquement si l'état de transaction doit être porté à la carte.
- `atelier-w17-patch-a-chaud/` : kit falsifiable (autotest bornes taille/alignement,
  refus si non aligné), rapport, vecteurs de test, statut matériel.

## Hypothèses
- H1 : aucune écriture atomique de 16 octets n'est garantie sur tous les profils visés
  (CMPXCHG16B/AVX n'est pas universel) — à vérifier, pas à supposer.
- H2 : un thread dont RIP est dans la zone modifiée exige quiescence ou trampoline de
  détournement ; sans cela la propriété ne peut pas être garantie.
- H3 : le métal requis pour les essais n'est pas disponible ici → statut « en attente de
  run matériel », aucun résultat annoncé.
- H4 : `unicorn` (émulation) ne modélise pas la cohérence du cache d'instructions ;
  l'émulation ne peut donc pas valider la propriété, seulement les états et refus.

## Critères d'acceptation
- Matrice profil → primitive → taille → alignement → disponibilité CPU → ordre mémoire →
  permissions de page → vidage → quiescence → RIP dans la zone.
- États de transaction formalisés, avec refus explicite de tout état partiel.
- Toute garantie non prouvée est RÉDUITE explicitement dans la spécification (pas de
  promesse conservée par inertie).
- Autotest du kit vert ; contrôle négatif (taille hors bornes / adresse non alignée)
  refusé.
- Sceau-I avant/après au nombre du manifeste ; un commit seul ; aucun artefact scellé
  historique modifié.

## Risques
- R1 : surestimer l'atomicité (alignement ≠ atomicité ≠ cohérence).
- R2 : exécution d'un état partiel pendant la bascule.
- R3 : toucher un artefact scellé (interdit).
- R4 : annoncer un résultat matériel non mesuré.

## Tests et preuves requis
- Autotest du kit (bornes, alignement, rollback, interruption à chaque étape).
- Vecteurs multi-threads documentés, exécutables au métal ; statut consigné.
- Vérification de l'absence de modification des arbres scellés (`sceau_I.py verifier`).

## Dépendances
Gel (W17R0GEL). Métal ≥ 2 machines pour les essais réels : EN ATTENTE, nommée. Le kit
est livré falsifiable dans l'intervalle.
