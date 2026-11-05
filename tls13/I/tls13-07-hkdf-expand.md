tls13-07 · HKDF-Expand (RFC 5869 § 2.3) · révision 1
Intention : l'expansion — OKM = T(1) || T(2) || … || T(N), T(i) =
HMAC(PRK, T(i−1) || info || octet(i)), T(0) = vide ; N = ⌈L/32⌉. La
boucle est BORNÉE PAR CONSTRUCTION : l'octet compteur ne peut prendre que
256 valeurs, le RFC borne L ≤ 255·32 = 8160 (chaque i doit être DISTINCT
— la longueur est la garde).
Contrat :
  pre  : P1 rcx = le PRK (32 o — RFC 5869 admet plus, le calendrier de
             TLS 1.3 ne produit QUE 32 : la spec LE FIXE, verdict -2
             autrement) ;
         P2 rdx = le pointeur de l'info (F octets) ; P3 r8 = F (0 ≤ F ≤
             2^61 − 33 : le tampon local T(i−1) || info || i doit tenir
             — la borne arithmétique de la brique) ;
         P4 r9 = L, la longueur de sortie demandée (1 ≤ L ≤ 8160) ;
         P5 [rsp+0x28] = le pointeur de sortie OKM (L o) ; pile
             alignée 16.
  post : Q1 l'OKM = HKDF-Expand(PRK, info, L) — les vecteurs RFC 5869
             appendice A (Test Cases 1 à 3, SHA-256, L = 42 : le PRK, le
             sel et l'info de chaque cas rejoués octet pour octet) ;
         Q2 le PRK et l'info INTACTS ; Q3 rax = 0 (ou -1/-2 NOMMÉS :
             pointeur de sortie nul, L = 0 ou L > 8160, F hors borne).
  inv  : I1 la boucle : au plus 255 itérations, le compteur i de 1 à N —
             CHAQUE itération construit le tampon local (32 + F + 1 o
             sur la pile : T(i−1) copié, info recopié, l'octet i posé)
             puis appelle tls13-05 ;
         I2 T(i−1) est lu depuis la sortie OKM elle-même (les 32 octets
             de l'itération précédente : la sortie EST le tampon —
             AUCUNE seconde copie détenue) ;
         I3 le temps est constant PAR RAPPORT AU PRK (charte § 3 : le
             PRK est un secret dérivé — la propriété hérite de tls13-05
             ; la boucle ne dépend QUE de L et F, publiques) ;
         I4 AUCUN état détenu (charte § 6) ; AUCUNE entrée IAT, AUCUN
             site syscall (charte § 7) ;
         I5 aucun registre non volatil détruit ; NOP, 0x90 (charte § 8).
