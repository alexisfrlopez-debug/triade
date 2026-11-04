libc-07 · remplissage mémoire · révision 2
Intention : écrire n fois le même octet dans une région — la brique
d'initialisation et de neutralisation de la mini-libc. Ce bloc est aussi
l'instrument de la démonstration R7 : entré en dev.2 dans la réserve de la
zone libc, sans qu'aucun bloc scellé ne bouge.
Contrat :
  pre  : P1 dst (argument 1) : région d'au moins n octets accessible en
             écriture ;
         P2 valeur (argument 2, 8 bits significatifs) : l'octet de
             remplissage ;
         P3 n (argument 3) : nombre d'octets à écrire (u64) ;
         P4 la pile est alignée à l'entrée du bloc (rsp ≡ 8 mod 16 —
             discipline partagée, frag-con, § 8.3-4).
  post : Q1 les n octets de dst sont égaux à l'octet de remplissage ;
         Q2 la valeur de retour (rax) contient dst ;
         Q3 les octets au-delà de dst+n ne sont pas écrits.
  inv  : I1 le bloc est une feuille : aucun appel, aucun accès système ;
         I2 la pile est équilibrée à la sortie ;
         I3 aucun registre non volatil du profil n'est modifié à la sortie
             (frag-con) — le travail vit dans les volatils ou dans un non
             volatil sauvegardé puis restauré ;
         I4 n = 0 : aucun octet n'est écrit.
Échecs :
  E1 : aucune condition d'échec — le remplissage est total sur la région.
Vecteurs :
  V1 : round-trip de notation 100 % (couvre P1-P4, Q1-Q3, I1-I4).
  V2 : propriété différentielle (oracle) : 12 000 cas à entrées aléatoires
       contraintes par P1-P4, n ∈ [0, 1024], octets aléatoires — région
       comparée à la référence, bornes au-delà de dst+n recontrôlées, retour,
       non volatils, rsp (couvre Q1-Q3, I2-I4).
  V3 : vecteurs dorés embarqués (autotest) : zéros sur 16 octets, 0xFF sur
       33 octets, longueur nulle sur sentinelle (couvre Q1, I4).
  V4 : test de rejet : toute notation du bloc contenant un appel, un syscall ou
       une écriture hors de dst est refusée par l'oracle structurel (couvre
       I1, Q3).
Fixtures    : régions ZERO16/FF33/SENT16 (référencées par libc-08, au plan de
              l'image).
Provenance  : écrite-avant-code.
Décisions   : D7, D8, D26, D28, R7 (démonstration d'entrée en réserve), D149
              (révision de granularité).
Historique  : R1 (m1/I, instance Windows scellée 0.2.0) révisée en R2 au
              chantier M6-(b) — granularité (D149-(3)) : arguments nommés
              dst/valeur/n, convention en frag-con, l'invariant I3 détaché du
              registre de travail particulier vers l'observable de sortie ;
              observables Q1-Q3, E1, vecteurs INVARIANTS.
