libc-08 · auto-test de la mini-libc · révision 2
Intention : exécuter les vecteurs dorés de chaque bloc de la mini-libc au
lancement de l'artefact et imprimer le verdict global — le point d'entrée de
selftest.exe, premier jalon d'une vérification de santé à la R10.
Contrat :
  pre  : P1 le bloc est le point d'entrée PE de selftest.exe ;
         P2 la pile est alignée à l'entrée (rsp ≡ 8 mod 16, convention chargeur) ;
         P3 l'arène et son curseur sont vierges (image chargée, .data nulle) ;
         P4 l'entrée standard n'est pas consommée (aucune lecture).
  post : Q1 chaque vecteur doré est exécuté exactement une fois, dans l'ordre
         des dépendances : zone (libc-05/06), puis memcmp (libc-02),
         memcpy (libc-01), strlen (libc-03), itoa (libc-04), memset (libc-07) ;
         Q2 une ligne unique "TRIADE M1 : minilibc N/21" suivie de " OK" ou
             " KO" est soumise à WriteFile sur la sortie standard, où N est le
             nombre de vecteurs réussis ;
         Q3 le processus se termine par ExitProcess(0) si N = 21, sinon
             ExitProcess(1) ;
         Q4 la valeur N est formatée par libc-04 (auto-hébergement : l'auto-test
             utilise la bibliothèque qu'il teste).
  inv  : I1 le bloc n'appelle que les blocs libc-01…07, io-01 (write),
         io-02 (exit) et l'IAT GetStdHandle — jamais de syscall direct ;
         I2 le prologue alloue un frame de 0x40 octets (shadow space + logettes)
             et sauvegarde rbx, r12, r13, r14, r15 ; l'épilogue les restaure
             symétriquement ;
         I3 aucun stockage sous rsp ; la loge [rsp+0x30..0x3F] sert de tampon
             de conversion à libc-04 et la loge [rsp+0x20..0x27] de brouillon —
             aucun appelé du bloc ne déclare plus de quatre arguments ;
         I4 les compteurs et pointeurs de travail vivent dans les registres
             non volatils sauvegardés (r15 réussites, rbx ligne, r12 offset,
             r13 handle, r14 brouillon) ;
         I5 le tampon ligne est alloué dans l'arène en phase de verdict, après
             le vecteur de réinitialisation (libc-06) — jamais avant.
Échecs :
  E1 : WriteFile échoue (sortie indisponible) → le verdict de sortie reste
       porté par le code ExitProcess (Q3), propagation silencieuse documentée
       (repli : même discipline que hello-01).
Vecteurs :
  V1 : round-trip de notation 100 % (couvre la fidélité générale du bloc).
  V2 : propriété différentielle (oracle, émulation complète) : le binaire
       entier est exécuté avec émulation IAT — la sortie doit être
       exactement "TRIADE M1 : minilibc 21/21 OK\r\n" et le code de sortie 0 ;
       la corruption d'un octet quelconque d'un bloc libc fait dévier sortie ou
       code (non-vacuité) (couvre Q1-Q4).
  V3 : vecteurs dorés embarqués : zone (alignement, bornes disjointes,
       réutilisation après réinitialisation, dépassement → 0), memcmp (égal,
       inférieur, supérieur, préfixe), memcpy (16 octets, longueur nulle sur
       sentinelle, 33 octets), strlen (vide, "TRIADE", 33 lettres), itoa
       (0, 4294967295, 1234567890, 7), memset (zéros sur 16 octets, 0xFF sur
       33 octets, longueur nulle sur sentinelle) — 21 vecteurs (couvre Q1, Q4).
  V4 : test de rejet : toute notation du bloc appelant un bloc hors de I1, ou
       écrivant sous rsp, est refusée par l'oracle structurel (couvre I1, I3).
Fixtures    : motifs et chaînes .rdata de libc-01…04 et libc-07 (référence
              unique par identifiant, conformément à D20).
Provenance  : écrite-avant-code.
Décisions   : D7, D8, D26, D28, D29.
Historique  : R1 (dev.1, 18 vecteurs) révisée en R2 (dev.2) pour l'entrée de
              libc-07 memset dans la bibliothèque — l'extension du contrat
              d'auto-test accompagne l'ajout du bloc dans la réserve libc
              (démonstration R7 : aucun bloc scellé ne bouge).
