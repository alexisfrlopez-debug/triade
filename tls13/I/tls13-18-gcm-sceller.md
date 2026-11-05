tls13-18 · GCM : sceller · révision 1
Intention : le mode authentifié SP 800-38D — le compteur : J0 = nonce ||
0^31 || 1 (le nonce de 12 o, la taille du IV du protocole — RFC 8446
§ 5.3) ; le chiffrage CTR (les blocs de compteur 2, 3, 4… chiffrés par
tls13-16, XOR au clair) ; l'étiquette : GHASH sur AAD || bourre au 16 ||
chiffré || bourre au 16 || [longueur(AAD) en BITS]64 || [longueur
(chiffré) en BITS]64 (les u64 GROS-BOUTISTES), puis l'étiquette = E(K,
J0) ⊕ GHASH — avec H = E(K, 0^128), calculé au geste même, JAMAIS détenu.
Contrat :
  pre  : P1 rcx = les clés de tour (176 o — le produit de tls13-15) ;
         P2 rdx = le nonce (12 o) ; P3 r8 = le clair (N octets) ;
         P4 r9 = N (0 ≤ N ≤ 2^14 — la borne de la couche
             enregistrement : le GCM tolère 2^39 bits, le protocole
             TLS n'émet jamais plus de 2^14 par enregistrement, la
             brique prend la borne du protocole) ;
         P5 [rsp+0x28] = l'AAD (A octets) ; P6 [rsp+0x30] = A (0 ≤ A ≤
             2^14) ; P7 [rsp+0x38] = la sortie chiffrée (N o) ;
         P8 [rsp+0x40] = la sortie étiquette (16 o) ; la pile alignée
             16.
  post : Q1 le chiffré = CTR(K, nonce, clair) et l'étiquette = le tag
             GCM — SP 800-38D § 7.1, prouvé par les vecteurs GCM de la
             validation NIST/CAVP (AES-128-GCM : les Test Cases 1 à 6
             de McGrew–Viega — clés/IV/AAD/clairs de tailles 0, 16 et
             20 octets, repris par la suite CAVP) ET par le TRANSFERT
             RFC 8448 (les enregistrements chiffrés du transcript,
             octet pour octet, par les clés du calendrier) ;
         Q2 le clair, l'AAD et le nonce INTACTS ; Q3 rax = 0 (ou -1/-2
             NOMMÉS : pointeurs nuls, N ou A hors borne).
  inv  : I1 l'ordre des opérations : H = E(K, 0) D'ABORD, puis le CTR
             (le chiffré EXISTE avant le GHASH qui le digère), puis
             l'étiquette ;
         I2 le GHASH accumule par APPELS RÉPÉTÉS à tls13-17 (l'itération
             de la § 6.4 : Y ← (Y ⊕ X) • H, bloc de 16 o par bloc —
             l'AAD bourré, le chiffré bourré, les DEUX longueurs en
             BITS u64 gros-boutistes) ;
         I3 le compteur : u32 GROS-BOUTISTE incrémenté depuis 2 (J0 = 1
             porte l'étiquette) — le rendement de compteur (2^32
             blocs) est hors d'atteinte par P4 (2^14 = 1024 blocs) ;
         I4 le temps constant : hérité de tls13-16/17 (les briques sont
             sans branche — la longueur N est publique, le XOR du clair
             est un flot de données) ;
         I5 AUCUNE entrée IAT, AUCUN site syscall (charte § 7) ; les
             transitoires (J0, H, l'accumulateur GHASH, le bloc
             compteur) sur la PILE (charte § 6) ; aucun registre non
             volatil détruit ; NOP, 0x90 (charte § 8).
