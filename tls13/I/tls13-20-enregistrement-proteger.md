tls13-20 · l'enregistrement : protéger · révision 1
Intention : la couche enregistrement de TLS 1.3 (RFC 8446 § 5.2) — le
texte interne = charge || type (1 o) || zéros de bourre (LONGUEUR ZÉRO :
le choix minimal, la possibilité de bourre d'opacité du RFC est un
chantier futur nommé) ; le nonce = IV statique ⊕ numéro de séquence (le
u64 GROS-BOUTISTE posé sur les HUIT derniers octets du IV) ; l'AAD =
l'en-tête COMPLÈTE de l'enregistrement émis (type opaque 23, version
héritage 0x0303, longueur = N + 17) ; le tout scellé par tls13-18.
L'enregistrement protégé est TOUJOURS de type opaque 23 — le type réel
vit DANS le chiffré.
Contrat :
  pre  : P1 rcx = le contexte enregistrement (200 o : clés de tour @ +0
             [176 o], IV statique @ +176 [12 o], réserve @ +188 [4 o],
             numéro de séquence u64 @ +192 [8 o] — la disposition
             DÉCLARÉE par la présente spec, l'adresse choisie par
             l'appelant : charte § 6 ; le contexte est POSÉ par
             tls13-24 au geste qui l'a dérivé) ;
         P2 rdx = le type de contenu RÉEL (1 o : 22 poignée, 21 alerte,
             23 données — il DEVIENT le dernier octet du texte interne) ;
         P3 r8 = la charge utile (N octets) ; P4 r9 = N (0 ≤ N ≤ 2^14 —
             RFC 8446 § 5.1 : TLSPlaintext.length ≤ 2^14, verdict -2
             au-delà) ;
         P5 [rsp+0x28] = la sortie (5 + N + 17 o accessibles :
             l'en-tête puis le chiffré) ; la pile alignée 16.
  post : Q1 l'enregistrement ÉMIS : l'en-tête (23, 0x0303, N + 17 en
             u16 GROS-BOUTISTE — 5 o construits par OCTETS FIXES) puis
             le chiffré (N + 1 o de texte interne + 16 o d'étiquette) ;
             le nonce consommé EST la séquence courante, PUIS la
             séquence du contexte est INCRÉMENTÉE (l'ordre est nommé :
             l'incrémentation SUIT le scellement — un échec n'avance
             JAMAIS la séquence) ;
         Q2 la charge utile INTACTE ; le contexte réécrit SUR SA
             SÉQUENCE SEULE ;
         Q3 rax = 0 (ou -1/-2/-3 NOMMÉS : pointeurs nuls, N hors
             borne, le verdict propagé de tls13-18).
  inv  : I1 UNE composition : tls13-18 (le scellement — le texte interne
             assemblé dans UN tampon local de N + 1 o sur la pile
             [jusqu'à 2^14 + 1 : le sous-cadre est NOMMÉ, la pile du
             domaine est dimensionnée par l'appelant], la charge
             recopiée puis le type posé au dernier octet) ;
         I2 le nonce : le IV copié en local, la séquence u64
             gros-boutiste XORée sur les octets 4..11 — le contexte
             n'est JAMAIS réécrit sur son IV ;
         I3 le temps constant : hérité de tls13-18 (la charge est
             secrète ou publique selon l'étage — la propriété couvre
             les deux ; la longueur N est publique) ;
         I4 AUCUNE entrée IAT, AUCUN site syscall (charte § 7) ; aucune
             écriture hors du contexte pointé et de la sortie ; aucun
             registre non volatil détruit ; NOP, 0x90 (charte § 8).
