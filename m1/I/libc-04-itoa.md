libc-04 · conversion décimale u32 · révision 2
Intention : convertir un entier non signé 32 bits en chaîne décimale ASCII
NUL-terminée, du premier chiffre au dernier — le formateur numérique de la
mini-libc, socle de tout affichage de compteur.
Contrat :
  pre  : P1 ecx contient la valeur à convertir (u32) ;
         P2 rdx contient l'adresse d'un tampon d'au moins 12 octets accessible
             en écriture (10 chiffres max + NUL) ;
         P3 la pile est alignée à l'entrée du bloc (rsp ≡ 8 mod 16).
  post : Q1 le tampon contient la représentation décimale de la valeur, sans
         zéro non significatif, immédiatement suivie d'un octet nul ;
         Q2 le premier chiffre est à l'offset 0 du tampon (représentation
             compacte, pas de champ fixe) ;
         Q3 rax contient l'adresse du tampon ;
         Q4 aucune écriture n'a lieu hors du tampon de douze octets ; les
             octets entre le NUL terminal et la fin du tampon constituent
             l'espace de travail de la génération (chiffres produits en ordre
             inverse puis compactés) — leur contenu final n'est pas spécifié
             et l'appelant ne doit pas en dépendre.
  inv  : I1 le bloc est une feuille : aucun appel, aucun accès système ;
         I2 la pile est équilibrée à la sortie (pousse/pop appariés) ;
         I3 aucun registre non volatil autre que rbx (sauvegardé puis
             restauré) n'est modifié ;
         I4 la valeur 0 produit la chaîne "0" (aucun cas particulier évité).
Échecs :
  E1 : aucune condition d'échec — la conversion est totale sur [0, 2^32-1].
Vecteurs :
  V1 : round-trip de notation 100 % (couvre P1-P3, Q1-Q4, I1-I4).
  V2 : propriété différentielle (oracle) : 12 000 valeurs couvrant les bornes
       (0, 1, 9, 10, 99, 100, 999, 1000, 2^31-1, 2^31, 2^32-1) et l'aléatoire
       uniforme — préfixe comparé à la référence, octets AU-DELÀ du tampon de
       douze octets recontrôlés intacts (garantie anti-débordement, Q4), rax,
       non volatils, rsp (couvre Q1-Q3, I2-I4).
  V3 : vecteurs dorés embarqués (autotest b20008) : 0 → "0",
       4294967295 → "4294967295", 1234567890 → "1234567890", 7 → "7"
       (couvre Q1, Q2, I4).
  V4 : test de rejet : toute notation du bloc contenant un appel, un syscall ou
       écrivant au-delà du tampon de douze octets est refusée par l'oracle
       (couvre I1, Q4).
Fixtures    : chaînes .rdata I0/IMAX/I123/I7 (référencées par libc-08).
Provenance  : écrite-avant-code.
Décisions   : D7, D8, D21 (aucune optimisation prématurée : division par 10
              explicite, pas de magie multiplicative), D26, D28, D29.
Historique  : R1 révisée avant scellage — l'oracle différentiel a démontré que
              « aucun octet écrit au-delà du NUL » (Q4 originelle) est
              irréalisable pour une génération en place ; R2 remplace cette
              exigence par la borne dure de douze octets et l'espace de travail
              non spécifié (le préfixe reste la seule partie significative).
