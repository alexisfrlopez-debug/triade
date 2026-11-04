libc-03 · longueur de chaîne · révision 2
Intention : retourner le nombre d'octets qui précèdent le premier octet nul
d'une chaîne — le compteur de la mini-libc, borné par la discipline de l'appelant.
Contrat :
  pre  : P1 chaîne (argument 1) : l'adresse d'une chaîne NUL-terminée,
             accessible en lecture ;
         P2 la chaîne contient au moins un octet nul ;
         P3 la pile est alignée à l'entrée du bloc (rsp ≡ 8 mod 16 —
             discipline partagée, frag-con, § 8.3-4).
  post : Q1 la valeur de retour (rax) contient l'offset du premier octet nul
             (longueur, u64) ;
         Q2 la chaîne est inchangée.
  inv  : I1 le bloc est une feuille : aucun appel, aucun accès système ;
         I2 la pile est équilibrée à la sortie (aucun registre sauvegardé) ;
         I3 aucun registre non volatil du profil n'est modifié (frag-con) ;
         I4 la lecture s'arrête strictement au premier octet nul.
Échecs :
  E1 : chaîne sans octet nul (P2 violée) → parcours hors contrat, jamais généré
       par l'oracle (la sanction — l'octet nul terminal — appartient à l'appelant).
Vecteurs :
  V1 : round-trip de notation 100 % (couvre P1-P3, Q1-Q2, I1-I4).
  V2 : propriété différentielle (oracle) : 12 000 chaînes aléatoires de
       longueur 0 à 200 sur l'alphabet des octets 0x01-0xFF — longueur exacte
       contre la référence, chaîne recontrôlée, non volatils, rsp (couvre Q1-Q2,
       I2-I4).
  V3 : vecteurs dorés embarqués (autotest) : chaîne vide → 0, "TRIADE" → 6,
       33 lettres → 33 (couvre Q1).
  V4 : test de rejet : toute notation du bloc contenant un appel, un syscall ou
       une écriture mémoire est refusée par l'oracle structurel (couvre I1).
Fixtures    : chaînes S_VIDE/S_TRIADE/S_33 (référencées par libc-08, au plan
              de l'image).
Provenance  : écrite-avant-code.
Décisions   : D7, D8, D26, D28, D29, D149 (révision de granularité).
Historique  : R1 (m1/I, instance Windows scellée 0.2.0) révisée en R2 au
              chantier M6-(b) — granularité (D149-(3)) : l'argument quitte
              rcx pour son NOM (chaîne), la convention vit en frag-con ;
              observables et vecteurs INVARIANTS.
