tls13-14 · X25519 : la clé publique · révision 1
Intention : le couple du ClientHello — la clé publique =
X25519(clé privée, 9) : le clamp et l'échelle par tls13-13, le point de
base u = 9 (la constante 32 octets little-endian du plan d'adressage, la
fixture PUBLIQUE du domaine — RFC 7748 § 6.1 : « the base point is
u = 9 »). Le bloc EST le geste du couple : le principal appelle UNE fois,
la clé publique naît avant le premier octet du ClientHello.
Contrat :
  pre  : P1 rcx = la sortie (32 o — la clé publique sérialisée) ;
         P2 rdx = la clé privée (32 o, BRUTE — le clamp est l'affaire
             de tls13-13) ;
         P3 la pile alignée 16, l'ombre 0x20 fournie.
  post : Q1 la sortie = X25519(privée, 9) — les vecteurs RFC 7748 § 6.1
             (les scalaires privés d'Alice et de Bob rendent LES clés
             publiques consignées) ET le transfert RFC 8448 (le
             key_share du ClientHello du transcript enregistré : la
             clé du fixture rendue octet pour octet) ;
         Q2 la clé privée INTACTE ; Q3 rax = 0.
  inv  : I1 UNE composition : tls13-13 (l'échelle au point de base — le
             point 9 est une DONNÉE PUBLIQUE du plan d'adressage, jamais
             un octet de code) ;
         I2 le sans-branche, l'absence d'état et la réentrance
             HÉRITENT de tls13-13 par composition (chartes § 3/§ 6) ;
         I3 AUCUNE entrée IAT, AUCUN site syscall (charte § 7) ;
         I4 aucun registre non volatil détruit ; NOP, 0x90 (charte § 8).
