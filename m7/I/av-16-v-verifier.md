av-16 · vérification de signature Ed25519 (RFC 8032, sans E/S) · révision 1
Intention : le verdict de l'échelon 2 — exécuter l'algorithme de
vérification Ed25519 (RFC 8032 § 5.1.7) sur des entrées DÉJÀ chargées en
mémoire (le bloc ne fait AUCUNE entrée/sortie : c'est un calcul pur, la
spec av-17 porte le monde extérieur) :
  1. S' (octets 32..63 de la signature) : entier little-endian 256 bits ;
     REFUS si S' ≥ L (comparaison octet par octet du poids fort au
     poids faible, miroir big-endian de la lecture) ;
  2. décompression de A (clé publique) — échec → KO ; décompression de
     R' (octets 0..31 de la signature) — échec → KO (av-14) ;
  3. h = SHA-512(R' || A || M) : DÉJÀ CALCULÉ par l'appelant (av-17
     exécute av-01/03/04 dans l'ordre — le contrat I2 de av-17 verrouille
     la séquence : R' d'abord, A ensuite, M enfin) ;
  4. Q1 = [S']B, Q2 = [h]A, Q3 = R' + [h]A (av-13 ×2, av-12) ;
  5. verdict : Q1 == Q3 (av-15).
Contrat :
  pre  : P1 rdi pointe vers A (32 octets sérialisés) ; P2 rsi pointe
             vers la signature (64 octets : R' || S') ; P3 rdx pointe
             vers h (64 octets : digest SHA-512 déjà finalisé) ;
         P4 rcx pointe vers la zone de travail courbe (R_TRAVAIL —
             les sous-zones TRAV_PT_B, TRAV_Q1..Q3, TRAV_PA, TRAV_PR,
             la zone scalaire R_SCALAIRE pour la copie zéro-étendue de
             S') ; P5 pile alignée.
  post : Q1 rax = 0 : signature VALIDE (l'équation [S']B = R' + [h]A
             vérifiée) ; rax = 1 : signature INVALIDE (S' ≥ L, point
             hors courbe, ou équation fausse — les trois causes se
             valent : un rejet est un rejet, fail-closed) ;
         Q2 AUCUNE écriture hors zone de travail ; A, signature et h
             sont inchangés.
  inv  : I1 séquence d'appels : av-13 (Q1 : le point B est construit
             dans la zone de travail depuis R_BX/R_BY rodata, Z = 1),
             copie de S' vers R_SCALAIRE (32 octets + 32 zéros : la
             zone est pré-zéroée par mov), av-13 (Q2 : point A
             décompressé, scalaire h 64 octets direct), av-12 (Q3 =
             R' + Q2), av-15 (Q1 contre Q3) ;
         I2 la comparaison S' < L : cinq cmp des qwords 3→0 puis le
             demi-mot haut (octets 24..31 de S' vs L : L < 2^253, tout
             octet non nul au-delà du bit 252 suffit à rejeter —
             implémentation : comparaison 256 bits stricte par
             sub/sbb fantôme : l'emprunt sortant décide, sans écrire) ;
         I3 données RIP : R_BX, R_BY, R_L (déclarées) ;
         I4 prologue 5 pushes + sub 0x18 : pile 16-alignée aux appels.
Échecs :
  E1 : S' ≥ L → rax = 1 (rejet RFC 8032 : le scalaire doit être dans
       [0, L)).
  E2 : A ou R' hors courbe → rax = 1 (le rejet d'av-14 se propage).
  E3 : équation fausse → rax = 1 (la signature ne prouve rien).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : oracle différentiel (natif, dev.2+) : les TROIS vecteurs dorés
       RFC 8032 § 7.1 (sha, abc, 1024 octets) VALIDENT ; les mêmes
       signatures falsifiées d'un bit (dans R', dans S', dans le
       message, dans la clé) REJETTENT ; les signatures des cartes du
       projet (m0/m1/m2/m6) valident contre pynacl en référence croisée
       — le berceau Python devient le VÉRIFIÉ, la ligne de mire de
       l'échelon 2.
  V3 : falsification intégrale — zéro silence.
Fixtures    : Bx @ R_BX, By @ R_BY (membres), L @ R_L (32 o LE).
Provenance  : écrite-avant-code.
Décisions   : D34.
Historique  : R1. h NON réduit mod L : le double-and-add 512 bits
              d'av-13 économise une réduction modulaire de Barrett à
              écrire et sceller — l'équation [S']B = R' + [h]A est
              exacte sur les entiers, RFC 8032 n'exige PAS la réduction
              (elle est implicite dans le groupe). R11 : fenêtre 4 bits
              sur S' et h (×2,5 de vitesse), mesuré alors.
