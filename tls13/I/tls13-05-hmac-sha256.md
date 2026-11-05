tls13-05 · HMAC-SHA-256 (RFC 2104) · révision 1
Intention : le code d'authentification à clé sur SHA-256 — la clé expulsée
à la taille du bloc (64 o : la clé plus longue est hachée d'abord, la plus
courte paddée de zéros), les masques ipad/opad (0x36/0x5c, les constantes
du plan d'adressage), la double composition H((K' ⊕ opad) || H((K' ⊕
ipad) || m)). LA brique d'authentification du domaine : HKDF (tls13-06/07)
et le Finished (tls13-25) ne sont QUE des compositions d'elle.
Contrat :
  pre  : P1 rcx = le pointeur de la clé (K octets lisibles, K ≥ 0) ;
         P2 rdx = K, la longueur de la clé (0 ≤ K ≤ 2^61 — la clé vide
             est LÉGALE : K' = 64 zéros, RFC 2104 § 2) ;
         P3 r8 = le pointeur du message (M octets lisibles, aucun
             alignement exigé) ; P4 r9 = M (0 ≤ M ≤ 2^61) ;
         P5 [rsp+0x28] = le pointeur de sortie (32 o accessibles en
             écriture) ; la pile alignée 16, l'ombre 0x20 fournie
             (fonction ordinaire de la lignée — miroir tls13-01 P2).
  post : Q1 la sortie (32 o à P5) = HMAC-SHA-256(clé, message) — RFC
             2104 § 2, prouvé par les vecteurs RFC 4231 appendice A (les
             SEPT cas, les clés de 131 et 149 o comprises — l'expulsion
             est EXERCÉE dans les deux sens) ;
         Q2 la clé et le message INTACTS (aucune écriture à P1/P3) ;
         Q3 rax = 0 (ou -1 NOMMÉ : pointeur de sortie nul).
  inv  : I1 le bloc est une COMPOSITION DÉCLARÉE : tls13-01 (init — DEUX
             contextes), tls13-03 (absorption), tls13-04 (finalisation)
             — appels directs aux adresses scellées (miroir I1 de
             tls13-03) ;
         I2 les DEUX contextes SHA (2 × 112 o) et le tampon K' (64 o)
             vivent sur la PILE du bloc (charte § 6 — aucun état détenu,
             le bloc est réentrant par construction) ;
         I3 le temps est constant PAR RAPPORT À LA CLÉ (charte § 3 — la
             clé EST une donnée secrète : le sel du calendrier, la clé
             Finished) : les masques sont posés sur 64 positions FIXES,
             la longueur K est publique (le nombre de tours du premier
             hachage peut en dépendre, le contenu JAMAIS) ;
         I4 AUCUNE entrée IAT, AUCUN site syscall (charte § 7) ;
         I5 aucun registre non volatil détruit ; la croissance du slot
             est NOP, 0x90 (charte § 8).
