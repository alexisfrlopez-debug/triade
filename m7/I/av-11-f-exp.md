av-11 · exponentiation modulaire f25519 · révision 1
Intention : élever une base à une puissance fixée de 256 bits (exposant
sérialisé little-endian en .rodata) par carré-and-multiply de gauche à
droite : 256 itérations bornées, l'accumulateur part de 1 (le
multiplicatif : contrairement au monde additif des points, l'identité
1·x = x ne dégénère jamais) — sert DEUX fois dans l'échelle : inversion
(x^(p−2), exposant @ R_EXP_INV) et racine carrée (x^((p−5)/8), exposant
@ R_EXP_SQRT).
Contrat :
  pre  : P1 rdi pointe vers la base (5 membres, membres < 2^52, valeur
             quelconque < 2^255) ; P2 rsi pointe vers l'exposant (32
             octets rodata, little-endian) ; P3 rdx pointe vers la
             sortie (40 o, peut chevaucher rdi : la base est copiée en
             zone de travail avant la boucle) ; P4 pile alignée.
  post : Q1 la valeur de sortie ≡ base^exposant (mod p) et est < p ;
         Q2 membres de sortie < 2^52 ; Q3 rax = rdx.
  inv  : I1 la boucle balaie le bit 255 au bit 0 : accumulateur =
             accumulateur² (av-09), puis si bit = 1 : accumulateur =
             accumulateur · base (av-09) — 256 itérations FIXES (les
             zéros de tête coûtent des carrés de 1, exacts et inoffensifs :
             1² = 1) ;
         I2 appels directs : av-09 (multiplication — entre 256 et 512
             appels), av-07 (aucun), av-10 (aucun direct : les sorties
             de av-09 sont déjà réduites) ;
         I3 données RIP : l'exposant pointé par rsi (cible déclarée par
             l'appelant — av-14 déclare R_EXP_INV/R_EXP_SQRT) ; le bloc
             ne charge AUCUNE donnée RIP lui-même ;
         I4 zone de travail : accumulateur et copie de base en .bss
             (R_TRAVAIL+0x6d0 et +0x710, hors zones des specs aval —
             la carte le vérifie) — pas de réentrance (mono-thread,
             miroir av-12) ;
         I5 prologue 3 pushes + sub 8 : pile 16-alignée aux appels.
Échecs :
  E1 : aucun (boucle bornée, opérations totales).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : oracle : x^(p−2) · x ≡ 1 (mod p) pour 200 x aléatoires non nuls
       (l'inversion se vérifie par sa définition) ; x^((p−5)/8) contre
       Python pour 200 x ; cas x = 0, 1, p−1.
Fixtures    : exposants @ R_EXP_INV (p−2) et @ R_EXP_SQRT ((p−5)/8),
              32 octets LE chacun (le builder les écrit et vérifie).
Provenance  : écrite-avant-code.
Décisions   : D34.
Historique  : R1. Le carré-and-multiply générique plutôt qu'une chaîne
              d'additions optimisée (~11 multiplications pour
              l'inversion) : 380 multiplications contre 265 — deux fois
              plus lent, mais UN bloc de 100 lignes contre trois pages de
              chaîne codée à la main ; R11 mesurera, le protocole
              n'optimise jamais à l'aveugle.
