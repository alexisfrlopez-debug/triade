shani-02 · SHA-256 : la compression d'un bloc de 64 octets, PAR LES INSTRUCTIONS SHA-NI · révision 1
Intention : LE MÊME CŒUR que tls13-02 — une ronde de la fonction de
compression FIPS 180-4 § 6.2.2, le message schedule W[0..63] depuis le bloc,
les 64 tours sur H, la double addition — exécuté par les instructions
matérielles sha256rnds2 (deux tours), sha256msg1/sha256msg2 (le calendrier).
LE CONTRAT EST CELUI DU SCELLÉ, À LA LETTRE (R4) : la variante est un
remplaçant possible au site d'appel de la compression, JAMAIS une refonte —
la disposition du contexte, la sémantique FIPS, les invariants du scellé
demeurent INTACTS. La raison d'être : le hot path mesuré (R11 — tls13-02 =
98,11 % des instructions du hachage d'un fichier volumineux, la mesure
consignée AVANT ce bloc à preuves_v150/hotpath_shani/).
Contrat :
  pre  : P1 rcx = le pointeur du contexte (initialisé par tls13-01 — H
             porte l'état courant du hachage) ;
         P2 rdx = le pointeur du bloc de 64 octets à comprimer (64 o
             lisibles, aucun alignement exigé — la spec ne suppose
             JAMAIS ce que l'appelant ne promet pas) ;
         P3 la pile alignée 16, l'ombre 0x20 fournie.
  post : Q1 H[0..7] = l'état APRÈS la compression du bloc (le schedule,
             les 64 tours, l'addition finale H := H + H') —
             conforme FIPS § 6.2.2, prouvé par les vecteurs de la § 6.3.1 :
             l'épreuve du laboratoire (epreuve_compression_shani.py) a
             joué les QUATRE vecteurs AVANT la notation — le vide,
             « abc », les 448 bits, les 896 bits — plus 100 blocs
             aléatoires contre le juge Python pur et le corpus aux
             bords : TOUT VERT sur le chemin matériel ;
         Q2 le bloc d'entrée et les champs du contexte HORS H[0..7] sont
             INTACTS (tampon, remplissage, total : la compression ne les
             touche pas — c'est l'affaire de shani-03) — MIROIR EXACT de
             Q2 de tls13-02 ;
         Q3 rax = 0.
  inv  : I1 AUCUNE entrée IAT, AUCUN site syscall (charte § 7 — calcul
             pur, le miroir de tls13-02 I1) ;
         I2 LES CONSTANTES AUX SOURCES DU PLAN, JAMAIS RE-DÉCLARÉES : la
             table K[64] @0x2F00 — LA TABLE DU SCELLÉ, lue par 16
             mouvements movdqa alignés aux 16 groupes de 4 constantes
             (0x2F00 ≡ 0 mod 16 — le plan du scellé sert la variante
             TEL QUEL) ; le masque BE @0x2800 (16 o — la marge .rdata
             VIERGE du scellé) — les DEUX cités par déplacement RIP,
             calculés depuis shani/layout.py, la source unique (T5) ;
         I3 LE TEMPS CONSTANT PAR CONSTRUCTION SUR LE CONTENU (miroir de
             tls13-02 I3, l'exigence RENFORCÉE par la nature matérielle) :
             les 64 tours s'exécutent TOUJOURS — sha256rnds2 exécute ses
             deux tours sans lire les données hors des voies SIMD, le
             calendrier sha256msg1/msg2 est SANS BRANCHE, les SEULS sauts
             du bloc sont AUCUN (le corps est DÉROULÉ : 16 phases
             explicites, ni boucle ni branch de contenu — le contrôle
             structurel du vérificateur le constate sur la notation :
             ZÉRO instruction de saut dans le corps) ;
         I4 AUCUN registre non volatil détruit : rbx, rbp, rdi, rsi,
             r12-r15 JAMAIS touchés (le corps ne vit que sur les
             volatils rax/rcx/rdx et la pile) ; XMM6 et XMM7 — NON
             VOLATILS msx64 — SAUVÉS/RESTAURÉS sur la pile du bloc (les
             transitoires SIMD vivent sur la pile, miroir de la charte
             § 6 : le budget des six volatils xmm0-5 ne suffit pas à la
             compression, le septième et le huitième y vivent LOUÉS,
             rendus INTACTS) ; la pile rendue à l'identique ;
         I5 la croissance du slot est NOP, 0x90 (charte § 8).
Échecs :
  E1 : aucun — la compression ne connaît ni la longueur totale, ni le
       bourrage (il compresse, point — le miroir exact de tls13-02) ;
       l'absence d'instructions SHA sur le processeur n'est PAS un échec
       du bloc : c'est l'AFFAIRE DE LA SONDE — shani-03 ne l'appelle
       JAMAIS si le verdict est 0 (le repli scalaire, le scellé).
Vecteurs :
  V1 : doré — les QUATRE vecteurs FIPS 180-4 § 6.3.1 au pipeline complet
       (le vide, « abc », les 448 bits, les 896 bits) : chaque condensé
       octet pour octet, RECROISÉ à hashlib.sha256 — VÉCUS sur le
       chemin matériel AVANT la notation (l'épreuve) puis REJOUÉS à la
       notation assemblée (le vérificateur) ;
  V2 : différentiel — 100 blocs aléatoires (graine fixée) : H sortant
       == le juge Python pur de la compression, ÉGALEMENT l'égalité
       avec tls13-02 LE SCELLÉ sur les mêmes entrées (la variante et le
       scellé rendent le MÊME H — la propriété fondatrice du dispatch) ;
  V3 : invariance de découpage (via shani-03) — hacher(a puis b) ==
       hacher(ab) aux TROIS découpages (1, 3, 63/64/65) sur le chemin
       SHA-NI comme sur le scalaire ;
  V4 : falsification — un bit du bloc muté : le condensé diverge (la
       composition n'est pas muette), un bit du condensé attendu muté :
       l'égalité échoue (la comparaison non plus) — le miroir de la
       falsification du harnais.
Fixtures    : le masque BE @0x2800 (shani/layout.py, 16 o — les valeurs
              [3,2,1,0, 7,6,5,4, 11,10,9,8, 15,14,13,12], chaque dword
              renversé) ; la table K du SCELLÉ @0x2F00 (jamais copiée).
Provenance  : écrite-avant-code ; les sémantiques des instructions SHA-NI
              ÉPINGLÉES PAR LE CODE AVANT la notation
              (experience_semantique_shani.py — les hypothèses
              d'opérandes et d'opérande implicite tranchées par
              l'exécution sur le CPU natif du laboratoire contre la
              référence FIPS en Python pur : l'opérande implicite de
              sha256rnds2 vit dans XMM0 [63:0] — les sommes W+K —, dst
              reçoit le nouvel état (C,D,G,H)→(A,B,E,F), src demeure ;
              sha256msg1 : dst += σ0([dst1, dst2, dst3, src0]) ;
              sha256msg2 : dst += σ1 chaîné [src2, src3, dst0′, dst1′] —
              les éléments 2-3 lisent les éléments 0-1 DÉJÀ CALCULÉS) ;
              la structure complète éprouvée à la main
              (epreuve_compression_shani.py) AVANT le premier octet de
              la notation.
Décisions   : D205, R11 (le hot path mesuré : 98,11 % — la mesure AVANT),
              R4 (le contrat du scellé à la lettre), R7 (K et les
              adresses du scellé, jamais re-déclarés), D161 (l'ARRÊT des
              slots sur les longueurs réelles).
