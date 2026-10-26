av-15 · égalité projective edwards25519 · révision 1
Intention : comparer deux points projectifs SANS inversion : les points
(X1:Y1:Z1) et (X2:Y2:Z2) sont égaux si et seulement si X1·Z2 = X2·Z1 ET
Y1·Z2 = Y2·Z1 (multiplications croisées — les coordonnées affines ne sont
jamais calculées : une inversion de sauvée, deux par comparaison).
Contrat :
  pre  : P1 rdi et rsi pointent vers les deux points (120 o chacun) ;
         P2 les valeurs membres sont réduites (< p — les sorties de
             av-09/av-12 le garantissent : la comparaison membre à
             membre de produits réduits est EXACTE) ; P3 pile alignée.
  post : Q1 rax = 1 si les points sont égaux (même classe
             projective), rax = 0 sinon ;
         Q2 les points d'entrée sont inchangés ; aucune écriture hors
             zone de travail.
  inv  : I1 séquence : t1 = X1·Z2, t2 = X2·Z1 (av-09), comparaison des
             5 membres : divergence → rax = 0 ; t3 = Y1·Z2, t4 = Y2·Z1
             (av-09), comparaison : divergence → rax = 0 ; égalité des
             deux → rax = 1 ;
         I2 appels directs : av-09 (quatre multiplications) ;
         I3 zone de travail .bss (4×40 o, offsets layout, hors zones
             des autres) ; aucune donnée RIP, aucun syscall ;
         I4 prologue 3 pushes + sub 8 : pile 16-alignée aux appels.
Échecs :
  E1 : aucun (quatre multiplications et des comparaisons).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : oracle : égal(P, P) ; égal(neutre, [0]B) ; égal([k]B, [k]B avec
       représentation différente — construit par add(P, neutre) dont la
       sortie a un Z ≠ 1) ; inégal([k1]B, [k2]B) pour k1 ≠ k2 mod L —
       cent vecteurs par famille.
Fixtures    : néant.
Provenance  : écrite-avant-code.
Décisions   : D34.
Historique  : R1. La comparaison croisée plutôt que l'inversion vers
              l'affine : 4 multiplications (≈ 300 cycles) contre 2
              inversions (≈ 500 multiplications) par comparaison — le
              verdict de la vérification Ed25519 en profite
              directement.
