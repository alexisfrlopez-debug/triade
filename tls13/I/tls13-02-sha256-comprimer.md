tls13-02 · SHA-256 : la compression d'un bloc de 64 octets · révision 1
Intention : UNE ronde de la fonction de compression FIPS 180-4 § 6.2.2 — le
message schedule W[0..63] depuis le bloc, les 64 tours sur H, la double
addition. Le cœur du hachage, exactement le contrat ah-05 (M6) : le bloc ne
connaît ni la longueur totale, ni le bourrage — il compresse, point.
Contrat :
  pre  : P1 rcx = le pointeur du contexte (initialisé par tls13-01 — H
             porte l'état courant du hachage) ;
         P2 rdx = le pointeur du bloc de 64 octets à comprimer (64 o
             lisibles, aucun alignement exigé — la spec ne suppose JAMAIS
             ce que l'appelant ne promet pas) ;
         P3 la pile alignée 16, l'ombre 0x20 fournie.
  post : Q1 H[0..7] = l'état APRÈS la compression du bloc (le schedule,
             les 64 tours, l'addition finale H := H + H') —
             conforme FIPS § 6.2.2, prouvé par les vecteurs de la § 6.3.1
             (le harnais du chantier (b) les joue : «abc» et les deux longs
             messages NIST) ;
         Q2 le bloc d'entrée et les champs du contexte HORS H[0..7] sont
             INTACTS (tampon, remplissage, total : la compression ne les
             touche pas — c'est l'affaire de tls13-03) ;
         Q3 rax = 0.
  inv  : I1 AUCUNE entrée IAT, AUCUN site syscall (charte § 7) ;
         I2 le schedule W[64] et les valeurs de tour vivent sur LA PILE du
             bloc (un état LOCAL transitoire — licite ; un état .data/.bss
             ne le serait pas : charte § 6) ;
         I3 le temps est constant PAR CONSTRUCTION sur le contenu (les 64
             tours s'exécutent toujours, aucune branche ne lit les données
             — la charte § 3 : le hachage du transcript digère des secrets
             DÉRIVÉS, la propriété est exigée ici) ;
         I4 aucun registre non volatil détruit ; aucune écriture hors du
             contexte pointé ;
         I5 la croissance du slot est NOP, 0x90.
