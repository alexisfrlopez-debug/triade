shani-01 · la sonde CPUID de la variante SHA-NI · révision 1
Intention : rendre le verdict de capacité — le processeur exécute-t-il les
instructions SHA (sha256rnds2, sha256msg1, sha256msg2) ET SSSE3 (pshufb,
palignr — les deux que la compression shani-02 emploie hors SHA-NI) ? LA
SONDE est l'unique site où la variante lit le processeur : le dispatch de
shani-03 la rappelle UNE FOIS par appel d'absorption (jamais par bloc de
64 o — R11 : le hot path est la compression, pas le choix du chemin).
Contrat :
  pre  : P1 la pile alignée 16 à l'entrée, l'ombre msx64 0x20 fournie
             par l'appelant (le bloc est une fonction ordinaire de la
             lignée — il n'appelle personne, l'ombre demeure intacte).
  post : Q1 rax = 1 si (feuille 7, sous-feuille 0, EBX bit 29 = SHA) ET
             (feuille 1, ECX bit 9 = SSSE3), rax = 0 sinon — les DEUX
             drapeaux exigés ensemble : la compression emploie les DEUX
             familles, un processeur SHA sans SSSE3 n'aura PAS la
             variante (le repli scalaire, toujours disponible, le
             scellé lui-même) ;
         Q2 rax ∈ {0, 1} — le verdict est BINAIRE, jamais une capacité
             partielle ;
         Q3 AUCUN autre effet : aucune écriture mémoire, aucun état
             détenu (charte § 6 de la famille sha : le bloc ne détient
             RIEN).
  inv  : I1 la liste fermée des lectures : CPUID feuille 7 sous-feuille 0
             (EBX bit 29), CPUID feuille 1 (ECX bit 9) — RIEN D'AUTRE du
             processeur n'est lu (aucune feuille supplémentaire, aucun
             MSR, aucun registre de configuration) ;
         I2 rbx SAUVÉ/RESTAURÉ (push/pop) : CPUID détruit rbx, rbx est
             NON VOLATIL msx64 — le bloc rend la main propre (rax, rbx,
             rcx, rdx détruits par CPUID sont volatils SAUF rbx) ;
         I3 AUCUNE entrée IAT, AUCUN site syscall (charte § 7 — calcul
             pur : la lecture CPUID n'est ni un appel système ni un
             import) ;
         I4 le verdict ne dépend QUE du processeur — JAMAIS des données
             absorbées (le temps de la sonde est constant sur le contenu
             par construction : elle n'en touche aucune) ;
         I5 la croissance du slot est NOP, 0x90 (charte § 8).
Échecs :
  E1 : aucun — le processeur sans SHA-NI ou sans SSSE3 n'est PAS un
       échec : c'est le verdict 0, le repli scalaire de shani-03 (le
       chemin ordinaire, jamais une erreur nommée).
Vecteurs :
  V1 : différentiel au laboratoire — sur le CPU SHA-NI natif du labo :
       rax = 1 ; sur l'émulation Unicorn (le modèle qemu64 sans SHA) :
       rax = 0 — le dispatch prend le repli SANS intervention (la
       preuve que le repli n'est pas décoratif) ;
  V2 : la composition forcée — les épreuves du laboratoire forcent le
       verdict dans les DEUX sens (le chemin SHA-NI sur la machine
       native, le chemin scalaire par sonde neutralisée en copie de
       laboratoire) — « dispatch forcé dans les deux sens », l'exigence
       de l'instruction lfh49a1xf ;
  V3 : rejet implicite — un processeur hypothétique SHA sans SSSE3
       rendrait 0 : la conjonction ET n'est pas un OU (la preuve vit à
       la sonde du laboratoire qui BRANCHE le résultat de chaque
       feuille séparément).
Fixtures    : aucune donnée — le bloc lit le processeur, rien d'autre.
Provenance  : écrite-avant-code (le paquet 6/6 de la vague 3, D205) ;
              les sémantiques CPUID ne sont PAS devinées : la feuille 7
              bit 29 (SHA) et la feuille 1 bit 9 (SSSE3) sont les drapeaux
              documentés Intel SDV2 § CPUID — la sonde les LIT, le
              laboratoire les RECROISE au comportement (l'émulation sans
              SHA rend 0, la machine native rend 1 — V1).
Décisions   : D205 (la variante SHA-NI), R11 (le hot path mesuré d'abord),
              D161 (le plan d'adressage, la préfiguration n'est pas un
              droit), la charte § 3 du domaine (AUCUN scellage au labo).
