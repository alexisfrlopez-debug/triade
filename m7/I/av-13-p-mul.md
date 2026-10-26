av-13 · multiplication scalaire edwards25519 · révision 1
Intention : calculer [k]P par double-and-add de gauche à droite sur 512
bits : l'accumulateur Q part du NEUTRE (0:1:1) — coordonnées finies, la
courbe est complète, aucune dégénérescence — chaque itération fait
Q = add(Q, Q) puis, si le bit courant est 1, Q = add(Q, P). Les scalaires
de l'échelle 2 sont le S de la signature (256 bits, zéro-étendu à 64
octets) et le h de RFC 8032 (64 octets, NON réduit mod L : le
double-and-add sur 512 bits évite toute réduction modulaire de h —
simplicité contre ~0,3 ms de calcul, R11 mesurera).
Contrat :
  pre  : P1 rdi pointe vers P (point projectif valide, 120 o) ; P2 rsi
             pointe vers le scalaire k (64 octets little-endian, lu en
             ENTIER : les bits de 511 à 0) ; P3 rdx pointe vers la
             sortie Q (120 o, distincte de P et de la zone de travail
             interne) ; P4 pile alignée.
  post : Q1 la sortie est le point [k mod L]P — l'itération complète sur
             512 bits calcule [k]P où k est lu comme entier 512 bits
             (l'égalité [k]P = [k mod L]P est un théorème de groupe :
             l'ordre de la courbe est L, le contrat ne promet QUE le
             point) ;
         Q2 P est inchangé ; Q3 rax = rdx.
  inv  : I1 l'accumulateur interne vit à R_TRAVAIL+TRAV_Q, le
             temporataire à TRAV_T : chaque doublement est
             add(Q, Q → T) puis les rôles s'échangent par copie membre à
             membre (5×3 u64) ; l'addition conditionnelle est
             add(Q, P → T) ou add(T, P → Q) — la sortie finale copiée
             vers rdx ;
         I2 appels directs : av-12 (512 à 768 appels — déclarés I1) ;
         I3 le balayage des bits : octet 63 bit 7 d'abord (bit 511),
             masque 0x80 décrémenté par shr 1, au passage à zéro :
             masque = 0x80 et octet décrémenté — l'ordre little-endian
             est celui de RFC 8032, le bit de POIDS FORT d'abord ;
         I4 aucune donnée RIP chargée par le bloc (P et k viennent des
             pointeurs) ; aucun syscall ;
         I5 prologue 3 pushes + sub 8 : pile 16-alignée aux appels.
Échecs :
  E1 : aucun (boucle bornée 512 itérations, addition totale).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : oracle : [0]B == neutre ; [1]B == B ; [2]B == add(B,B) ; [L]B ==
       neutre (l'ordre exact) ; [L+1]B == B ; 200 scalaires aléatoires
       256 bits contre Python ; h aléatoire 512 bits contre Python
       (réduit mod L en Python pour la comparaison).
Fixtures    : néant (B est chargé par l'appelant).
Provenance  : écrite-avant-code.
Décisions   : D34.
Historique  : R1. Le neutre (0:1:1) initial plutôt qu'un point dégénéré
              Z=0 : la formule projective exige Z ≠ 0 — c'est le choix
              qui rend le double-and-add TOTAL sans cas particulier,
              l'avantage d'Edwards payé d'avance par la spec av-12.
