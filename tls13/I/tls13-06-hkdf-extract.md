tls13-06 · HKDF-Extract (RFC 5869 § 2.1) · révision 1
Intention : l'extraction — PRK = HMAC-SHA-256(sel, IKM), le sel devenant
la CLÉ du HMAC ; le sel ABSENT (longueur 0) devient les 32 zéros du RFC
5869 § 2.2 (« a string of HashLen zeros »). Dans le calendrier TLS 1.3
(tls13-24), le sel est TOUJOURS fourni (le secret dérivé de l'étage amont)
SAUF au tout premier extrait (Early : sel vide) — le cas est PORTÉ par la
spec, jamais contourné par l'appelant.
Contrat :
  pre  : P1 rcx = le pointeur du sel (S octets) ; P2 rdx = S (0 ≤ S ≤
             2^61 ; S = 0 LÉGAL — rcx alors ignoré, les 32 zéros) ;
         P3 r8 = le pointeur de l'IKM (I octets) ; P4 r9 = I (1 ≤ I ≤
             2^61 — l'IKM vide est REFUSÉ : verdict -2, le calendrier
             ne l'exige jamais) ;
         P5 [rsp+0x28] = le pointeur du PRK (32 o) ; pile alignée 16.
  post : Q1 le PRK = HKDF-Extract(sel, IKM) — RFC 5869 § 2.1, prouvé par
             les vecteurs de l'appendice A (Test Cases 1 à 3, SHA-256 :
             le sel long, le sel vide — le cas zéro EXERCÉ, la règle de
             P2 n'est pas une parole) ;
         Q2 le sel et l'IKM INTACTS ; Q3 rax = 0 (ou -1/-2 NOMMÉS :
             pointeur de sortie nul, I = 0).
  inv  : I1 UNE composition : tls13-05 (l'HMAC, appelé UNE fois) —
             l'expulsion du sel en clé HMAC EST le geste du bloc (le
             sel de 32 o du calendrier devient la clé telle quelle ; un
             sel plus long suit la règle RFC 2104 du bloc appelé) ;
         I2 AUCUN état détenu (charte § 6) ; AUCUNE entrée IAT, AUCUN
             site syscall (charte § 7) ;
         I3 le temps est constant PAR RAPPORT À L'IKM (charte § 3 — le
             secret partagé x25519 est un IKM : la propriété hérite de
             tls13-05, le bloc n'ajoute AUCUNE branche sur le contenu) ;
         I4 aucun registre non volatil détruit ; NOP, 0x90 (charte § 8).
