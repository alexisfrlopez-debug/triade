av-12 · addition projective unifiée edwards25519 · révision 1
Intention : additionner deux points de la courbe en coordonnées
projectives (X:Y:Z), formule unifiée (marche pour P1 = P2 — le
doublement — et pour tout couple de points VALIDES de la courbe complète :
le neutre est (0:1:1), à coordonnées FINIES — c'est l'avantage structurel
d'Edwards sur Weierstrass, aucun point à l'infini à traiter) :
  A = Z1·Z2 ; B = A² ; C = X1·X2 ; D = Y1·Y2 ; E = d·C·D ; F = B−E ;
  G = B+E ; X3 = A·F·((X1+Y1)·(X2+Y2)−C−D) ; Y3 = A·G·(D+C) ; Z3 = F·G
(a = −1 : le terme (D − a·C) devient (D+C)).
Contrat :
  pre  : P1 rdi (P1), rsi (P2), rdx (P3) pointent vers trois points
             projectifs (120 o : X @ +0, Y @ +40, Z @ +80) ; P3 DOIT
             être distinct de P1 et P2 (la formule relit ses entrées
             après la première écriture de sortie) ; P1 PEUT égaler P2
             (doublement) ;
         P2 les points d'entrée sont des points VALIDES de la courbe
             (Z ≠ 0 : le neutre (0,1,1) et les points décomprimés le
             garantissent ; la courbe est complète — d non-résidu — les
             dénominateurs B±E ne s'annulent pas, Bernstein-Lange 2007) ;
         P3 pile alignée.
  post : Q1 P3 = P1 + P2 (addition de courbe, représentation
             projective quelconque) ;
         Q2 les points P1 et P2 sont INCHANGÉS (lecture seule) ;
         Q3 rax = rdx.
  inv  : I1 appels directs : av-07 (add), av-08 (sub), av-09 (mul) —
             11 multiplications (A, B, C, D, t=X1+Y1 fois X2+Y2, E=d·CD,
             puis A·F, (AF)·t', A·G, (AG)·(D+C), F·G), 2 additions
             (X1+Y1, X2+Y2, D+C — trois), 2 soustractions (t'−C−D par
             deux subs, B−E) ;
         I2 zone de travail .bss (R_TRAVAIL+TRAV_P1/P2/P3 pour les
             copies, +TRAV_A pour A,B,C,D,E,F,G et temporaires — 560 o) :
             les opérandes d'av-07/08/09 exigent des adresses STABLES,
             les résultats intermédiaires vivent dans la zone, le
             résultat final est copié vers P3 à la fin ; PAS de
             réentrance (mono-thread : av-13 appelle av-12 en boucle,
             jamais imbriqué) ;
         I3 d est chargé depuis R_D (5 membres rodata, cible RIP
             déclarée) ;
         I4 prologue 3 pushes + sub 8 : pile 16-alignée aux appels ;
         I5 aucune écriture sous rsp, aucun syscall.
Échecs :
  E1 : aucun pour des entrées conformes (la formule unifiée est totale
       sur la courbe complète — le contrat P2 porte la validité).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : oracle : pour des points aléatoires de la courbe (construits par
       multiplication scalaire depuis B, contre Python) : add(P, Q) ==
       add(Q, P) (commutativité), add(P, neutre) == P (les deux sens),
       add(P, P) == doublement vérifié par add(P, Q) avec Q = copie,
       add(P, −P) == neutre (0,1,1) — cent vecteurs par propriété.
  V3 : falsification intégrale — zéro silence.
Fixtures    : d @ R_D (5 membres) — le builder écrit et vérifie.
Provenance  : écrite-avant-code.
Décisions   : D34.
Historique  : R1. UNE formule pour addition ET doublement (coût ~11
              multiplications contre 7 pour un doublement dédié) : ~768
              additions par vérification, 15 % plus lent qu'une paire
              dédiée add/dbl — mais la moitié du code à écrire, relire
              et sceller. Le protocole préfère le simple vérifiable au
              rapide non vérifié ; R11 mesurera l'écart.
