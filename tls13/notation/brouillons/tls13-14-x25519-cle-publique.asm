; tls13-14-x25519-cle-publique · brouillon étiqueté — spec tls13-14:R1, bloc carte h100014
; X25519 : LA CLÉ PUBLIQUE — le couple du ClientHello. La clé publique =
; X25519(clé privée, 9) : le clamp et l'échelle par tls13-13, le point de
; base u = 9 LU AU FIXTURE R_U9 (la constante 32 octets little-endian du
; plan d'adressage — RFC 7748 § 6.1 : « the base point is u = 9 » — LA
; FIXTURE PUBLIQUE DU DOMAINE, jamais un octet de code — I1). Le bloc EST
; le geste du couple : le principal appellera UNE fois, la clé publique
; naîtra avant le premier octet du ClientHello.
; rcx = la sortie (32 o — la clé publique sérialisée) · rdx = la clé
; privée (32 o, BRUTE — le clamp est l'affaire de tls13-13, P2) · Q1 la
; sortie = X25519(privée, 9) — les vecteurs RFC 7748 § 6.1 (les scalaires
; privés d'Alice et de Bob rendent LES clés publiques consignées) ET LE
; TRANSFERT RFC 8448 (le key_share du ClientHello du transcript enregistré
; : la clé du fixture rendue octet pour octet) · Q2 la clé privée INTACTE
; · Q3 rax = 0.
; COMPOSITION DÉCLARÉE (I1) : tls13-13 UNE fois, à l'adresse scellée — le
; point 9 est une DONNÉE PUBLIQUE du plan d'adressage (R_U9, l'ARRÊT .text6
; consigné — miroir D95 : la réserve .rdata M8 est ÉPUISÉE par K[64]).
; Le sans-branche, l'absence d'état et la réentrance HÉRITENT de tls13-13
; par composition (I2 — les chartes § 3/§ 6). LE DÉPLACEMENT RIP UNIQUE :
; le lea du fixture U9 (le SEUL du bloc — tout le reste vit dans les
; registres et la pile de l'appelé). AUCUNE entrée IAT, AUCUN site
; syscall (charte § 7) ; aucun registre non volatil détruit (I4) ; NOP,
; 0x90 (charte § 8).
; 0 push + sub rsp, 0x28 (40 o = l'ombre msx64 0x20 + l'alignement 8 :
; entrée ≡ 8 → 8−40 ≡ 0 (mod 16) au point d'appel) — le bloc est LE
; passe-plat du couple : rcx et rdx traversent, r8 désigne le fixture.
sub rsp, 0x28
lea r8, [rip + U9]
call TLS13
xor eax, eax
add rsp, 0x28
ret
