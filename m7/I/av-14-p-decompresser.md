av-14 · décompression de point edwards25519 · révision 1
Intention : reconstruire la coordonnée X d'un point depuis sa forme
sérialisée Ed25519 (32 octets : y little-endian sur 255 bits, bit 255 =
parité de x) : l'équation de courbe x² = (y²−1)/(dy²+1) se résout par
l'astuce racine : x = u·v³·(u·v⁷)^((p−5)/8) avec u = y²−1, v = dy²+1 ;
si x²v ≠ u, une seconde tentative x = x·sqrt(−1) ; l'échec des deux
signifie un point HORS courbe (réjection stricte RFC 8032 § 5.1.7) ; la
parité de x est ensuite ajustée au bit de signe.
Contrat :
  pre  : P1 rdi pointe vers les 32 octets sérialisés ; P2 rsi pointe
             vers le point projectif de sortie (120 o) ; P3 pile
             alignée.
  post : Q1 en cas de succès (rax = 0) : la sortie est le point
             projectif (x, y, 1) AVEC la parité de x égale au bit 255
             de l'entrée (parité ajustée par négation conditionnelle
             x = p − x, av-08 sur 0−x) et y = les 255 bits de poids
             faible de l'entrée (le bit 255 est le signe, ignoré de y) ;
         Q2 en cas d'échec (rax = 1) : point HORS courbe (x²·v ≠ u
             après les deux tentatives) — la sortie n'est PAS écrite,
             l'appelant DOIT rejeter (fail-closed, la signature est KO) ;
         Q3 les 32 octets d'entrée sont inchangés.
  inv  : I1 séquence : bit de signe lu et sauvé ; av-05 (y → membres,
             255 bits bas) ; av-09 pour y² ; av-07/av-08 pour u = y²−1
             et v = d·y²+1 ; av-09 pour v³, v⁷ (par v², v³ = v²·v,
             v⁷ = v³·v³·v), uv⁷ ; av-11 avec exposant @ R_EXP_SQRT ;
             test x²v == u (comparaison membre à membre de valeurs
             RÉDUITES — les sorties de av-09 le garantissent) ;
             deuxième tentative : av-09 par sqrt(−1) @ R_SQRTM1 puis
             re-test ; parité : bit 0 du membre 0 de x comparé au signe,
             négation conditionnelle av-08(0, x) ; Z = 1 posé en
             membres [1,0,0,0,0] ;
         I2 appels directs : av-05, av-07, av-08, av-09, av-11 ;
         I3 données RIP : R_D, R_SQRTM1, R_EXP_SQRT (déclarées) ;
         I4 zone de travail .bss (y, u, v, v2, v3, v7, uv7, x, t —
             offsets fixés par le layout, hors zones av-12/13/16) ;
         I5 prologue 4 pushes + sub 8 : pile 16-alignée aux appels.
Échecs :
  E1 : point hors courbe (Q2) — renvoyé comme VERDICT (rax=1), pas
       comme crash : le rejet est une valeur de retour, la porte
       fail-closed est chez l'appelant (av-16 E2).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : oracle : les points de base B et A des vecteurs dorés RFC 8032
       (§ 7.1 TEST 1-3) se décompressent et recompressent identiquement
       (aller-retour) ; 200 points aléatoires valides (construits par
       [k]B en Python) : décompression → recompression octet-identique ;
       200 sérialisations aléatoires INVALIDES : rejet rax=1 dans
       l'écrasante majorité (et aucune acceptation fausse — le test x²v
       == u est exact) ; le point y = 1 (neutre, x = 0, signe 0/1).
  V3 : falsification intégrale — zéro silence.
Fixtures    : d @ R_D, sqrt(−1) @ R_SQRTM1, (p−5)/8 @ R_EXP_SQRT —
              le builder écrit et vérifie les trois.
Provenance  : écrite-avant-code.
Décisions   : D34.
Historique  : R1. L'astuce (p−5)/8 avec correction sqrt(−1) évite le
              test de résidu quadratique général : DEUX multiplications
              de plus, zéro théorie du symbole de Legendre dans le code
              — la spécification porte la théorie, la notation exécute
              l'arithmétique.
