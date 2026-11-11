PROTOCOLE DE RÉPLICATION — v0.12.0 (la commande du développeur,
l'append-only : le protocole est PROPOSÉ, aucune réplication n'est
exécutée à cette édition — N = 1 demeure la limite déclarée)
====================================================================

LES TROIS AXES (indépendants, cumulables) :

  R1 SECOND DÉVELOPPEUR — un développeur externe mène UN jalon complet
     (le modèle M0 : la chaîne notation → octets → PE32+ → exécution)
     avec l'agent, sur ses propres machines, depuis le dépôt public ;
     MESURÉ : le temps au jalon, le nombre d'itérations terrain, les
     défauts nommés (la grille ci-dessous), la conformité 7/7 ;
     L'ATTENTE : les CLASSES de défauts recouvrent celles du premier
     développeur (les chargeurs, l'ABI, les conventions — pas les
     idiosyncrasies).

  R2 SECOND DOMAINE — une application RÉELLE NEUVE dans un domaine
     diffèrent de Loupe (le candidat : un visualiseur de registres
     Windows — l'Event Viewer minimal), même profil, même méthode ;
     MESURÉ : les 18+ spécifications écrites-avant-code, le premier
     build, les runs terrain jusqu'au vert, la balise scellée.

  R3 SECOND PROFIL — le port d'UN bloc existant vers un profil non
     primaire (aarch64-macos-macho, le « réservé » de la spécification) :
     la couche I demeure, le profil est écrit (les SEPT éléments + la
     suite de conformité § 8.2) ; MESURÉ : le round-trip, le run terrain,
     la parité inter-profils à contrat constant (§ 8.3).

LA GRILLE DE CODAGE T/X (la double annotation) :

  Chaque défaut rencontré (terrain OU laboratoire) est codé par DEUX
  annotateurs indépendants (le développeur originel + le réplicant) sur
  la grille :

    T — défaut du TERRAIN (invisible au laboratoire) :
       T1 chargeur/image (BASERELOC, enveloppe, BSS, initialiseur)
       T2 ABI/convention matérielle (ombre msx64, alignement SSE, zone
          rouge SysV, fence.i)
       T3 sémantique du chargeur (gle 32, OFT au pas, imports EXE)
       T4 codes d'erreur/conventions système (HINSTANCE, signe EAX)
       T5 environnement (antivirus, console, résolution)
    X — défaut de l'INSTRUMENT (visible au laboratoire) :
       X1 logique (round-trip, différentiel, vecteurs)
       X2 structure (adresses, plan, IAT, déplacements)
       X3 harnais/rig (l'instrument lui-même fautif)

  DÉSACCORD → un troisième codeur tranche (consigné).

LE KAPPA DE COHEN — l'accord inter-annotateurs sur les classes :

  κ = (p₀ − pₑ) / (1 − pₑ)

  p₀ = l'accord observé, pₑ = l'accord attendu par hasard (les marges).
  INTERPRÉTATION (Landis & Koch) : < 0 désaccord · 0–0,20 très faible ·
  0,21–0,40 faible · 0,41–0,60 modéré · 0,61–0,80 substantiel ·
  0,81–1 presque parfait. L'ATTENTE : κ ≥ 0,61 (substantiel) sur les
  classes T/X — sinon la grille est révisée AVANT la réplication
  suivante (la taxonomie doit être PARTAGEABLE, pas idiosyncratique).

LES CRITÈRES D'ACCEPTATION DE LA RÉPLICATION :

  (1) le jalon franchi aux critères de sortie mesurables (§ 18) ;
  (2) les défauts codés par la grille, κ ≥ 0,61 ;
  (3) les classes T1-T5 du réplicant ⊆ les classes constatées par le
      premier développeur (la méthode ENSEIGNE ce qu'elle a appris) —
      une classe NOUVELLE est un RÉSULTAT (la taxonomie s'étend,
      consigné), jamais un échec ;
  (4) les budgets tokens mesurés à l'instrumentation (± 2× les
      mesures M1 — la variance inter-développeurs est attendue,
      consignée).

LE COÛT ESTIMÉ : R1 ≈ 2 jours (le modèle des 17 jours du projet pour
11 jalons), R2 ≈ 5 jours, R3 ≈ 3 jours — le protocole PROPOSÉ, jamais
exécuté : l'arbitrage appartient au développeur.
