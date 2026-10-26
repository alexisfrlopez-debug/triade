libc-07 · remplissage mémoire · révision 1
Intention : écrire n fois le même octet dans une région — la brique
d'initialisation et de neutralisation de la mini-libc. Ce bloc est aussi
l'instrument de la démonstration R7 : entré en dev.2 dans la réserve de la
zone libc, sans qu'aucun bloc scellé ne bouge.
Contrat :
  pre  : P1 rcx contient dst, région d'au moins n octets accessible en écriture ;
         P2 dl contient l'octet de remplissage (seuls les 8 bits bas de rdx
             sont significatifs) ;
         P3 r8 contient n, nombre d'octets à écrire (u64) ;
         P4 la pile est alignée à l'entrée du bloc (rsp ≡ 8 mod 16).
  post : Q1 les n octets de dst sont égaux à l'octet de remplissage ;
         Q2 rax contient dst ;
         Q3 les octets au-delà de dst+n ne sont pas écrits.
  inv  : I1 le bloc est une feuille : aucun appel, aucun accès système ;
         I2 la pile est équilibrée à la sortie ;
         I3 aucun registre non volatil n'est modifié ;
         I4 n = 0 : aucun octet n'est écrit.
Échecs :
  E1 : aucune condition d'échec — le remplissage est total.
Vecteurs :
  V1 : round-trip de notation 100 % (couvre P1-P4, Q1-Q3, I1-I4).
  V2 : propriété différentielle (oracle) : 12 000 cas à entrées aléatoires
       contraintes par P1-P4, n ∈ [0, 1024], octets aléatoires — région
       comparée à la référence, bornes au-delà de dst+n recontrôlées, rax,
       non volatils, rsp (couvre Q1-Q3, I2-I4).
  V3 : vecteurs dorés embarqués (autotest b20008) : zéros sur 16 octets,
       0xFF sur 33 octets, longueur nulle sur sentinelle (couvre Q1, Q3, I4).
  V4 : test de rejet : toute notation du bloc contenant un appel, un syscall ou
       une écriture hors de dst est refusée par l'oracle structurel (couvre I1).
Fixtures    : motifs .rdata ZERO16/FF33/SENT16 (référencés par libc-08).
Provenance  : écrite-avant-code.
Décisions   : D7, D8, D26, D28 (réserve libc — démonstration R7), D29.
