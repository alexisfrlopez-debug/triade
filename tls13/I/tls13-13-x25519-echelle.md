tls13-13 · X25519 : l'échelle de Montgomery (RFC 7748 § 5) · révision 1
Intention : LA fonction X25519 — l'échelle de Montgomery en 255 itérations
(les bits 254 → 0 du scalaire CLAMPÉ), la permutation conditionnelle
cswap à chaque itération, l'inversion finale x2 · z2^(p−2). Le miroir win
de l'arithmétique prouvée par av-05..11 (M7), RE-COMPOSÉE pour la
coordonnée seule : les opérateurs de tls13-09..12, la représentation
membres radix 2^51 — et la discipline SANS BRANCHE DE DONNÉES sur le
scalaire (charte § 3 : le scalaire EST la clé privée).
Contrat :
  pre  : P1 rcx = la sortie (32 o accessibles en écriture — le résultat
             SÉRIALISÉ little-endian) ;
         P2 rdx = le scalaire (32 o — BRUT : le clamp RFC 7748 [octet 0
             &= 248 ; octet 31 &= 127 puis |= 64] est FAIT PAR LE BLOC
             dans une copie locale, une opération PUBLIQUE sur la clé) ;
         P3 r8 = le point u (32 o — le bit 255 est MASQUÉ par le bloc :
             RFC 7748 § 5, le décodage de la coordonnée) ;
         P4 la pile alignée 16, l'ombre 0x20 fournie.
  post : Q1 la sortie = X25519(scalaire, u) — RFC 7748 § 5, prouvé par
             les vecteurs de la § 6.1 : les DEUX paires (la clé publique
             d'Alice × la privée de Bob == la publique de Bob × la
             privée d'Alice == LE secret partagé consigné) ET le test
             ITÉRÉ (l'entrée u = 9 itérée 1 fois puis 1000 fois : les
             résultats consignés) ;
         Q2 le scalaire et u INTACTS (le clamp et le masque vivent dans
             des copies locales — la sortie seule est écrite) ;
         Q3 rax = 0.
  inv  : I1 LE SANS-BRANCHE NOMMÉ (charte § 3) : le bit du scalaire est
             extrait par décalage en registre, la permutation cswap est
             un XOR MASQUÉ membre à membre (le masque 0/−1 diffusé du
             bit par sar — RFC 7748 § 5 exige un échange en temps
             constant) ; AUCUNE instruction de branch ne lit le
             scalaire ni les intermédiaires ; les 255 itérations
             s'exécutent TOUJOURS ;
         I2 la recette RFC 7748 § 5 À CHAQUE itération : A = x2 + z2,
             B = x2 − z2, AA = A², BB = B², E = AA − BB, C = x3 + z3,
             D = x3 − z3, DA = D·A, CB = C·B, x3 = (DA + CB)², z3 =
             x1·(DA − CB)², x2 = AA·BB, z2 = E·(AA + a24·E) — a24 =
             121665, la constante du plan d'adressage ;
         I3 les états de l'échelle (x1, x2, z2, x3, z3 et les
             transitoires d'étape) vivent sur la PILE (le sous-cadre
             ≈ 0x300) — LA DIVERGENCE NOMMÉE sur le miroir av-11 : le
             M7 tenait ses zones de travail en .bss à adresse fixe
             (av-11 I4), la charte § 6 du M9 l'INTERDIT — tout est
             pile, le bloc est réentrant par construction ;
         I4 l'inversion finale : z2^(p−2) par carré-et-multiplie de
             gauche à droite sur l'exposant FIXE p − 2 (32 o
             little-endian, la constante PUBLIQUE du plan d'adressage —
             miroir av-11 : 255 itérations bornées, les zéros de tête
             coûtent des carrés de 1, exacts et inoffensifs), PUIS la
             multiplication x2 · z2^(p−2) et la sérialisation 32 o
             little-endian ;
         I5 les appels : tls13-09/10/11 (entre 4 et 6 opérations par
             itération d'échelle, entre 255 et 510 pour l'inversion) —
             TOUJOURS réduits en sortie (l'invariant de tls13-09..11) ;
         I6 AUCUNE entrée IAT, AUCUN site syscall (charte § 7) ; AUCUN
             état détenu (charte § 6) ; aucun registre non volatil
             détruit ; NOP, 0x90 (charte § 8).
