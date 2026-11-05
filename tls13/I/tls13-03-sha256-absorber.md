tls13-03 · SHA-256 : l'absorption tamponnée · révision 1
Intention : l'invariance de découpage — absorber N octets quelconques dans
le tampon du contexte, comprimer chaque fois que 64 octets sont complets,
garder le reste. Le contrat ah-06 (M6) : le découpage de l'appelant n'est
JAMAIS une entrée de la fonction — hacher(a puis b) == hacher(ab), la
preuve se joue au harnais en trois découpages distincts.
Contrat :
  pre  : P1 rcx = le pointeur du contexte (initialisé) ;
         P2 rdx = le pointeur des données (N octets lisibles, aucun
             alignement exigé) ;
         P3 r8 = N, la longueur en octets (0 ≤ N ≤ 2^61 — N = 0 est LÉGAL :
             le bloc ne fait rien, rend 0) ;
         P4 la pile alignée 16, l'ombre 0x20 fournie.
  post : Q1 les N octets absorbés : le tampon reçoit le couplage au
             remplissage courant, CHAQUE bloc complet de 64 o est comprimé
             par tls13-02 (l'appel direct entre blocs déclarés — I1), le
             remplissage et le total sont mis à jour (total += N) ;
         Q2 l'INVARIANCE : l'état final du contexte est IDENTIQUE
             quel que soit le découpage des mêmes octets en appels
             successifs (le harnais du chantier (b) le prouve sur pièces :
             un seul appel, par 1, par 3, par 63/64/65) ;
         Q3 les données d'entrée INTACTES (aucune écriture à rdx) ;
         Q4 rax = 0.
  inv  : I1 les appels à tls13-02 sont DIRECTS, à l'adresse scellée du
             plan (l'appel inter-blocs déclaré — miroir de la convention
             I1 du domaine av) ;
         I2 AUCUNE entrée IAT, AUCUN site syscall (charte § 7) ;
         I3 aucun état détenu hors du contexte pointé ; les transitoires
             vivent sur la pile (charte § 6) ;
         I4 le temps est constant PAR CONSTRUCTION sur le contenu (la
             longueur N est une donnée PUBLIQUE — le nombre de tours peut
             en dépendre, le contenu non) ;
         I5 aucun registre non volatil détruit ; la croissance du slot est
             NOP, 0x90.
