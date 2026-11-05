; tls13-13-x25519-echelle · brouillon étiqueté — spec tls13-13:R1, bloc carte h100013
; X25519 : L'ÉCHELLE DE MONTGOMERY (RFC 7748 § 5) — LA fonction du domaine.
; 255 itérations (les bits 254 → 0 du scalaire CLAMPÉ), la permutation
; conditionnelle cswap à chaque itération, l'inversion finale
; x2 · z2^(p−2). Le miroir win de l'arithmétique des contrats av-05..11
; (M7), RE-COMPOSÉE pour la coordonnée seule : les opérateurs tls13-09..12,
; la représentation membres radix 2^51 — et LA DISCIPLINE SANS BRANCHE DE
; DONNÉES sur le scalaire (charte § 3 : le scalaire EST la clé privée).
; rcx = la sortie (32 o accessibles en écriture — le résultat SÉRIALISÉ
; little-endian, le bit 255 nul : la valeur < p) · rdx = le scalaire (32 o
; BRUT — le clamp RFC 7748 [octet 0 &= 248 ; octet 31 &= 127 puis |= 64]
; est FAIT PAR LE BLOC dans une COPIE LOCALE, une opération PUBLIQUE sur
; la clé — P2) · r8 = le point u (32 o — le bit 255 est MASQUÉ par le bloc
; dans la copie locale : RFC 7748 § 5 le décodage de la coordonnée, les
; valeurs NON CANONIQUES ≡ réduites mod p par l'arithmétique même — P3) ·
; Q1 la sortie = X25519(scalaire, u) — les vecteurs RFC 7748 § 5.2/§ 6.1
; et LE TRANSFERT RFC 8448 · Q2 le scalaire et u INTACTS (les copies
; locales seules vivent) · Q3 rax = 0.
; LE SANS-BRANCHE NOMMÉ (I1) : le bit du scalaire est extrait par
; décalage en registre, la permutation cswap est un XOR MASQUÉ membre à
; membre (le masque 0/−1 diffusé du drapeau par sar — RFC 7748 § 5 exige
; un échange en temps constant, le miroir exact de la recette officielle) ;
; AUCUNE instruction de branch ne lit le scalaire ni les intermédiaires ;
; les 255 itérations s'exécutent TOUJOURS. LA RECETTE RFC 7748 § 5 À
; CHAQUE ITÉRATION (I2) : A = x2+z2, B = x2−z2, AA = A², BB = B², E =
; AA−BB, C = x3+z3, D = x3−z3, DA = D·A, CB = C·B, x3 = (DA+CB)², z3 =
; x1·(DA−CB)², x2 = AA·BB, z2 = E·(AA+a24·E) — 4 add + 4 sub + 10 mul =
; 18 appels PAR ITÉRATION (ERRATUM I5 consigné AVANT la notation :
; « entre 4 et 6 opérations » — la recette I2 fait foi, le compte par
; code) ; a24 = 121665 en REPRÉSENTATION MEMBRES posée UNE fois sur la
; pile (la constante du plan d'adressage, X25519_A24).
; LES ÉTATS DE L'ÉCHELLE (I3) — x1, x2, z2, x3, z3, a24 et les QUATRE
; transitoires S1..S4 vivent sur la PILE (LA DIVERGENCE NOMMÉE sur le
; miroir av-11 : le M7 tenait ses zones en .bss à adresse fixe, la charte
; § 6 l'INTERDIT — tout est pile, le bloc est réentrant par construction)
; ; le sous-cadre réel 0x210 (la spec écrit « ≈ 0x300 » — la mesure
; s'incline, la consignation porte le nombre) + K copie du scalaire,
; U copie masquée du point, E copie de l'exposant (32 o chacun).
; L'INVERSION FINALE (I4) : z2^(p−2) par carré-et-multiplie de GAUCHE à
; DROITE sur l'exposant FIXE p − 2 — 255 itérations bornées, l'exposant
; copié depuis LE FIXTURE R_EXP_INV du plan (la constante PUBLIQUE, miroir
; av-11 : le M7 la tenait en .rodata, le M9 la tient au fixture .text6 —
; l'ARRÊT consigné au plan d'adressage) ; les zéros de tête coûtent des
; carrés de 1, exacts et inoffensifs ; LA BRANCHE du bit porte sur
; L'EXPOSANT PUBLIC, jamais sur un secret (255 carrés + 253
; multiplications = 508 appels ∈ [255, 510] — I5) ; PUIS x2 · z2^(p−2) et
; la SÉRIALISATION 32 o little-endian (la mini-passe de retenues — le
; retour ×19 du membre 4 est IMPOSSIBLE : la valeur < p, le théorème —
; puis les QUATRE quads, les décalages 0/13/38/25/12 en miroir exact du
; décodage, le miroir win d'av-05 renversé).
; COMPOSITION DÉCLARÉE (I5) : tls13-09/10/11 — TOUJOURS réduits en sortie
; (l'invariant de la famille : les entrées de l'échelle respirent sous
; 2^52 membres, < p valeurs). AUCUNE entrée IAT, AUCUN site syscall
; (charte § 7) ; AUCUN état détenu (charte § 6) ; les non-volatils rdi
; (la sortie), rbx (le compteur), rbp (le drapeau) retenus par pushes ;
; NOP, 0x90 (charte § 8). LES DÉPLACEMENTS RIP : le SEUL du bloc est le
; fixture EXP_INV (I4 — les constantes vivent au plan, jamais en octets
; de code).
; 3 pushes (24 o) : entrée ≡ 8 → 8−24 ≡ 0 (mod 16) aux points d'appel ;
; sub rsp, 0x210 (528 o ≡ 0 mod 16) : [rsp+0x00..0x1f] l'ombre msx64 des
; appels · x1 @+0x20 · x2 @+0x48 · z2 @+0x70 · x3 @+0x98 · z3 @+0xc0 ·
; a24 @+0xe8 · S1 @+0x110 · S2 @+0x138 · S3 @+0x160 · S4 @+0x188 ·
; le scalaire clampé @+0x1b0 · le point u masqué @+0x1d0 · l'exposant
; p−2 @+0x1f0 (32 o chacun — la frontière 0x210 est tenue).
push rdi
push rbx
push rbp
sub rsp, 0x210
mov rdi, rcx
; --- le scalaire : la COPIE LOCALE + le clamp RFC 7748 (P2 — public) ---------
mov rax, qword ptr [rdx]
movabs r11, 0xfffffffffffffff8
and rax, r11
mov qword ptr [rsp + 0x1b0], rax
mov rax, qword ptr [rdx + 8]
mov qword ptr [rsp + 0x1b8], rax
mov rax, qword ptr [rdx + 16]
mov qword ptr [rsp + 0x1c0], rax
mov rax, qword ptr [rdx + 24]
movabs r11, 0x7fffffffffffffff
and rax, r11
movabs r11, 0x4000000000000000
or rax, r11
mov qword ptr [rsp + 0x1c8], rax
; --- le point u : la COPIE LOCALE + le masque du bit 255 (P3) ----------------
mov rax, qword ptr [r8]
mov qword ptr [rsp + 0x1d0], rax
mov rax, qword ptr [r8 + 8]
mov qword ptr [rsp + 0x1d8], rax
mov rax, qword ptr [r8 + 16]
mov qword ptr [rsp + 0x1e0], rax
mov rax, qword ptr [r8 + 24]
movabs r11, 0x7fffffffffffffff
and rax, r11
mov qword ptr [rsp + 0x1e8], rax
; --- l'exposant p−2 : la copie du FIXTURE R_EXP_INV (I4) ----------------------
lea r11, [rip + EXP_INV]
mov rax, qword ptr [r11]
mov qword ptr [rsp + 0x1f0], rax
mov rax, qword ptr [r11 + 8]
mov qword ptr [rsp + 0x1f8], rax
mov rax, qword ptr [r11 + 16]
mov qword ptr [rsp + 0x200], rax
mov rax, qword ptr [r11 + 24]
mov qword ptr [rsp + 0x208], rax
; --- le décodage du point u → x1 (le miroir win d'av-05 : 0/13/38/25/12) ------
movabs r11, 0x7ffffffffffff
mov rax, qword ptr [rsp + 0x1d0]
and rax, r11
mov qword ptr [rsp + 0x20], rax
mov rax, qword ptr [rsp + 0x1d0]
shr rax, 51
mov rdx, qword ptr [rsp + 0x1d8]
shl rdx, 13
or rax, rdx
and rax, r11
mov qword ptr [rsp + 0x28], rax
mov rax, qword ptr [rsp + 0x1d8]
shr rax, 38
mov rdx, qword ptr [rsp + 0x1e0]
shl rdx, 26
or rax, rdx
and rax, r11
mov qword ptr [rsp + 0x30], rax
mov rax, qword ptr [rsp + 0x1e0]
shr rax, 25
mov rdx, qword ptr [rsp + 0x1e8]
shl rdx, 39
or rax, rdx
and rax, r11
mov qword ptr [rsp + 0x38], rax
mov rax, qword ptr [rsp + 0x1e8]
shr rax, 12
and rax, r11
mov qword ptr [rsp + 0x40], rax
; --- l'initialisation de l'échelle (RFC 7748 § 5 : x2=1, z2=0, x3=u, z3=1) ---
mov qword ptr [rsp + 0x48], 1
mov qword ptr [rsp + 0x50], 0
mov qword ptr [rsp + 0x58], 0
mov qword ptr [rsp + 0x60], 0
mov qword ptr [rsp + 0x68], 0
mov qword ptr [rsp + 0x70], 0
mov qword ptr [rsp + 0x78], 0
mov qword ptr [rsp + 0x80], 0
mov qword ptr [rsp + 0x88], 0
mov qword ptr [rsp + 0x90], 0
mov qword ptr [rsp + 0xc0], 1
mov qword ptr [rsp + 0xc8], 0
mov qword ptr [rsp + 0xd0], 0
mov qword ptr [rsp + 0xd8], 0
mov qword ptr [rsp + 0xe0], 0
; a24 en représentation membres : [121665, 0, 0, 0, 0] — le plan X25519_A24
mov qword ptr [rsp + 0xe8], 121665
mov qword ptr [rsp + 0xf0], 0
mov qword ptr [rsp + 0xf8], 0
mov qword ptr [rsp + 0x100], 0
mov qword ptr [rsp + 0x108], 0
; x3 = x1 (la copie des cinq membres)
mov rax, qword ptr [rsp + 0x20]
mov qword ptr [rsp + 0x98], rax
mov rax, qword ptr [rsp + 0x28]
mov qword ptr [rsp + 0xa0], rax
mov rax, qword ptr [rsp + 0x30]
mov qword ptr [rsp + 0xa8], rax
mov rax, qword ptr [rsp + 0x38]
mov qword ptr [rsp + 0xb0], rax
mov rax, qword ptr [rsp + 0x40]
mov qword ptr [rsp + 0xb8], rax
; --- LA BOUCLE : t = 254 → 0 (255 itérations TOUJOURS exécutées) -------------
mov rbx, 254
xor ebp, ebp
.boucle:
; le bit k_t : extrait par décalage en registre (I1 — JAMAIS une branche)
mov rax, rbx
shr rax, 3
movzx eax, byte ptr [rsp + rax + 0x1b0]
mov rcx, rbx
and rcx, 7
shr rax, cl
and eax, 1
mov r11d, eax                   ; k_t PRÉSERVÉ — rax est le scratch du cswap
; swap ^= k_t ; le masque 0/−1 diffusé par sar (I1 — RFC 7748 § 5)
xor ebp, eax
mov r10, rbp
shl r10, 63
sar r10, 63
; LE CSWAP : (x2,z2) ↔ (x3,z3), dix membres XOR MASQUÉS (I1)
mov rax, qword ptr [rsp + 0x48]
xor rax, qword ptr [rsp + 0x98]
and rax, r10
xor qword ptr [rsp + 0x48], rax
xor qword ptr [rsp + 0x98], rax
mov rax, qword ptr [rsp + 0x50]
xor rax, qword ptr [rsp + 0xa0]
and rax, r10
xor qword ptr [rsp + 0x50], rax
xor qword ptr [rsp + 0xa0], rax
mov rax, qword ptr [rsp + 0x58]
xor rax, qword ptr [rsp + 0xa8]
and rax, r10
xor qword ptr [rsp + 0x58], rax
xor qword ptr [rsp + 0xa8], rax
mov rax, qword ptr [rsp + 0x60]
xor rax, qword ptr [rsp + 0xb0]
and rax, r10
xor qword ptr [rsp + 0x60], rax
xor qword ptr [rsp + 0xb0], rax
mov rax, qword ptr [rsp + 0x68]
xor rax, qword ptr [rsp + 0xb8]
and rax, r10
xor qword ptr [rsp + 0x68], rax
xor qword ptr [rsp + 0xb8], rax
mov rax, qword ptr [rsp + 0x70]
xor rax, qword ptr [rsp + 0xc0]
and rax, r10
xor qword ptr [rsp + 0x70], rax
xor qword ptr [rsp + 0xc0], rax
mov rax, qword ptr [rsp + 0x78]
xor rax, qword ptr [rsp + 0xc8]
and rax, r10
xor qword ptr [rsp + 0x78], rax
xor qword ptr [rsp + 0xc8], rax
mov rax, qword ptr [rsp + 0x80]
xor rax, qword ptr [rsp + 0xd0]
and rax, r10
xor qword ptr [rsp + 0x80], rax
xor qword ptr [rsp + 0xd0], rax
mov rax, qword ptr [rsp + 0x88]
xor rax, qword ptr [rsp + 0xd8]
and rax, r10
xor qword ptr [rsp + 0x88], rax
xor qword ptr [rsp + 0xd8], rax
mov rax, qword ptr [rsp + 0x90]
xor rax, qword ptr [rsp + 0xe0]
and rax, r10
xor qword ptr [rsp + 0x90], rax
xor qword ptr [rsp + 0xe0], rax
mov ebp, r11d                   ; swap = k_t (le bit PRÉSERVÉ, jamais le scratch)
; --- LA RECETTE §5 (I2) : B = x2 − z2 (S1 ← la copie de x2) -------------------
mov rax, qword ptr [rsp + 0x48]
mov qword ptr [rsp + 0x110], rax
mov rax, qword ptr [rsp + 0x50]
mov qword ptr [rsp + 0x118], rax
mov rax, qword ptr [rsp + 0x58]
mov qword ptr [rsp + 0x120], rax
mov rax, qword ptr [rsp + 0x60]
mov qword ptr [rsp + 0x128], rax
mov rax, qword ptr [rsp + 0x68]
mov qword ptr [rsp + 0x130], rax
lea rcx, [rsp + 0x110]
lea rdx, [rsp + 0x70]
call TLS10
; A = x2 + z2 → x2 EN PLACE (l'original vit dans S1)
lea rcx, [rsp + 0x48]
lea rdx, [rsp + 0x70]
call TLS09
; D = x3 − z3 (S2 ← la copie de x3)
mov rax, qword ptr [rsp + 0x98]
mov qword ptr [rsp + 0x138], rax
mov rax, qword ptr [rsp + 0xa0]
mov qword ptr [rsp + 0x140], rax
mov rax, qword ptr [rsp + 0xa8]
mov qword ptr [rsp + 0x148], rax
mov rax, qword ptr [rsp + 0xb0]
mov qword ptr [rsp + 0x150], rax
mov rax, qword ptr [rsp + 0xb8]
mov qword ptr [rsp + 0x158], rax
lea rcx, [rsp + 0x138]
lea rdx, [rsp + 0xc0]
call TLS10
; C = x3 + z3 → x3 EN PLACE (l'original vit dans S2)
lea rcx, [rsp + 0x98]
lea rdx, [rsp + 0xc0]
call TLS09
; DA = D·A (S2 détruit — A survit en second)
lea rcx, [rsp + 0x138]
lea rdx, [rsp + 0x48]
call TLS11
; CB = C·B (x3 détruit — B survit en S1)
lea rcx, [rsp + 0x98]
lea rdx, [rsp + 0x110]
call TLS11
; AA = A² (S3 ← la copie de A : DA est fait, A n'a plus que AA)
mov rax, qword ptr [rsp + 0x48]
mov qword ptr [rsp + 0x160], rax
mov rax, qword ptr [rsp + 0x50]
mov qword ptr [rsp + 0x168], rax
mov rax, qword ptr [rsp + 0x58]
mov qword ptr [rsp + 0x170], rax
mov rax, qword ptr [rsp + 0x60]
mov qword ptr [rsp + 0x178], rax
mov rax, qword ptr [rsp + 0x68]
mov qword ptr [rsp + 0x180], rax
lea rcx, [rsp + 0x160]
lea rdx, [rsp + 0x160]
call TLS11
; BB = B² (S1 détruit — B n'a plus que BB)
lea rcx, [rsp + 0x110]
lea rdx, [rsp + 0x110]
call TLS11
; x2' = AA·BB : x2 ← la COPIE de AA (A est mort — DA est fait ; AA a TROIS
; consommateurs destructifs [x2', E, AA+AE] : la copie x2 sert au produit,
; S3 garde l'original pour E, S4 prendra la sienne pour le sommet)
mov rax, qword ptr [rsp + 0x160]
mov qword ptr [rsp + 0x48], rax
mov rax, qword ptr [rsp + 0x168]
mov qword ptr [rsp + 0x50], rax
mov rax, qword ptr [rsp + 0x170]
mov qword ptr [rsp + 0x58], rax
mov rax, qword ptr [rsp + 0x178]
mov qword ptr [rsp + 0x60], rax
mov rax, qword ptr [rsp + 0x180]
mov qword ptr [rsp + 0x68], rax
lea rcx, [rsp + 0x48]
lea rdx, [rsp + 0x110]
call TLS11
; S4 ← la copie de AA (le TROISIÈME consommateur : AA+AE, le dernier vivant)
mov rax, qword ptr [rsp + 0x160]
mov qword ptr [rsp + 0x188], rax
mov rax, qword ptr [rsp + 0x168]
mov qword ptr [rsp + 0x190], rax
mov rax, qword ptr [rsp + 0x170]
mov qword ptr [rsp + 0x198], rax
mov rax, qword ptr [rsp + 0x178]
mov qword ptr [rsp + 0x1a0], rax
mov rax, qword ptr [rsp + 0x180]
mov qword ptr [rsp + 0x1a8], rax
; E = AA − BB (S3 = AA détruit — le deuxième consommateur)
lea rcx, [rsp + 0x160]
lea rdx, [rsp + 0x110]
call TLS10
; AE = a24·E (S1 ← la copie de E ; a24 survit en second)
mov rax, qword ptr [rsp + 0x160]
mov qword ptr [rsp + 0x110], rax
mov rax, qword ptr [rsp + 0x168]
mov qword ptr [rsp + 0x118], rax
mov rax, qword ptr [rsp + 0x170]
mov qword ptr [rsp + 0x120], rax
mov rax, qword ptr [rsp + 0x178]
mov qword ptr [rsp + 0x128], rax
mov rax, qword ptr [rsp + 0x180]
mov qword ptr [rsp + 0x130], rax
lea rcx, [rsp + 0x110]
lea rdx, [rsp + 0xe8]
call TLS11
; AA + AE (S4 = AA détruit — le dernier consommateur)
lea rcx, [rsp + 0x188]
lea rdx, [rsp + 0x110]
call TLS09
; z2' = E·(AA+AE) (z2 ← la copie de E — le logement était libre)
mov rax, qword ptr [rsp + 0x160]
mov qword ptr [rsp + 0x70], rax
mov rax, qword ptr [rsp + 0x168]
mov qword ptr [rsp + 0x78], rax
mov rax, qword ptr [rsp + 0x170]
mov qword ptr [rsp + 0x80], rax
mov rax, qword ptr [rsp + 0x178]
mov qword ptr [rsp + 0x88], rax
mov rax, qword ptr [rsp + 0x180]
mov qword ptr [rsp + 0x90], rax
lea rcx, [rsp + 0x70]
lea rdx, [rsp + 0x188]
call TLS11
; DA − CB (S1 ← la copie de DA — DA a DEUX consommateurs)
mov rax, qword ptr [rsp + 0x138]
mov qword ptr [rsp + 0x110], rax
mov rax, qword ptr [rsp + 0x140]
mov qword ptr [rsp + 0x118], rax
mov rax, qword ptr [rsp + 0x148]
mov qword ptr [rsp + 0x120], rax
mov rax, qword ptr [rsp + 0x150]
mov qword ptr [rsp + 0x128], rax
mov rax, qword ptr [rsp + 0x158]
mov qword ptr [rsp + 0x130], rax
lea rcx, [rsp + 0x110]
lea rdx, [rsp + 0x98]
call TLS10
; (DA−CB)²
lea rcx, [rsp + 0x110]
lea rdx, [rsp + 0x110]
call TLS11
; z3' = x1·(DA−CB)² (z3 ← la copie de x1 — x1 SURVIT en second, TOUJOURS)
mov rax, qword ptr [rsp + 0x20]
mov qword ptr [rsp + 0xc0], rax
mov rax, qword ptr [rsp + 0x28]
mov qword ptr [rsp + 0xc8], rax
mov rax, qword ptr [rsp + 0x30]
mov qword ptr [rsp + 0xd0], rax
mov rax, qword ptr [rsp + 0x38]
mov qword ptr [rsp + 0xd8], rax
mov rax, qword ptr [rsp + 0x40]
mov qword ptr [rsp + 0xe0], rax
lea rcx, [rsp + 0xc0]
lea rdx, [rsp + 0x110]
call TLS11
; DA + CB (S2 = DA détruit, x3 = CB détruit — les derniers)
lea rcx, [rsp + 0x138]
lea rdx, [rsp + 0x98]
call TLS09
; x3' = (DA+CB)²
lea rcx, [rsp + 0x138]
lea rdx, [rsp + 0x138]
call TLS11
; le commit de x3' (x3 ← S2 — le logement CB est mort)
mov rax, qword ptr [rsp + 0x138]
mov qword ptr [rsp + 0x98], rax
mov rax, qword ptr [rsp + 0x140]
mov qword ptr [rsp + 0xa0], rax
mov rax, qword ptr [rsp + 0x148]
mov qword ptr [rsp + 0xa8], rax
mov rax, qword ptr [rsp + 0x150]
mov qword ptr [rsp + 0xb0], rax
mov rax, qword ptr [rsp + 0x158]
mov qword ptr [rsp + 0xb8], rax
dec rbx
jns .boucle
; --- LE CSWAP FINAL (RFC 7748 § 5 : la dernière permutation drapeautée) ------
mov r10, rbp
shl r10, 63
sar r10, 63
mov rax, qword ptr [rsp + 0x48]
xor rax, qword ptr [rsp + 0x98]
and rax, r10
xor qword ptr [rsp + 0x48], rax
xor qword ptr [rsp + 0x98], rax
mov rax, qword ptr [rsp + 0x50]
xor rax, qword ptr [rsp + 0xa0]
and rax, r10
xor qword ptr [rsp + 0x50], rax
xor qword ptr [rsp + 0xa0], rax
mov rax, qword ptr [rsp + 0x58]
xor rax, qword ptr [rsp + 0xa8]
and rax, r10
xor qword ptr [rsp + 0x58], rax
xor qword ptr [rsp + 0xa8], rax
mov rax, qword ptr [rsp + 0x60]
xor rax, qword ptr [rsp + 0xb0]
and rax, r10
xor qword ptr [rsp + 0x60], rax
xor qword ptr [rsp + 0xb0], rax
mov rax, qword ptr [rsp + 0x68]
xor rax, qword ptr [rsp + 0xb8]
and rax, r10
xor qword ptr [rsp + 0x68], rax
xor qword ptr [rsp + 0xb8], rax
mov rax, qword ptr [rsp + 0x70]
xor rax, qword ptr [rsp + 0xc0]
and rax, r10
xor qword ptr [rsp + 0x70], rax
xor qword ptr [rsp + 0xc0], rax
mov rax, qword ptr [rsp + 0x78]
xor rax, qword ptr [rsp + 0xc8]
and rax, r10
xor qword ptr [rsp + 0x78], rax
xor qword ptr [rsp + 0xc8], rax
mov rax, qword ptr [rsp + 0x80]
xor rax, qword ptr [rsp + 0xd0]
and rax, r10
xor qword ptr [rsp + 0x80], rax
xor qword ptr [rsp + 0xd0], rax
mov rax, qword ptr [rsp + 0x88]
xor rax, qword ptr [rsp + 0xd8]
and rax, r10
xor qword ptr [rsp + 0x88], rax
xor qword ptr [rsp + 0xd8], rax
mov rax, qword ptr [rsp + 0x90]
xor rax, qword ptr [rsp + 0xe0]
and rax, r10
xor qword ptr [rsp + 0x90], rax
xor qword ptr [rsp + 0xe0], rax
; --- L'INVERSION z2^(p−2) : 255 bornées, l'exposant PUBLIC (I4) ---------------
mov rax, qword ptr [rsp + 0x70]
mov qword ptr [rsp + 0x110], rax
mov rax, qword ptr [rsp + 0x78]
mov qword ptr [rsp + 0x118], rax
mov rax, qword ptr [rsp + 0x80]
mov qword ptr [rsp + 0x120], rax
mov rax, qword ptr [rsp + 0x88]
mov qword ptr [rsp + 0x128], rax
mov rax, qword ptr [rsp + 0x90]
mov qword ptr [rsp + 0x130], rax
mov qword ptr [rsp + 0x138], 1
mov qword ptr [rsp + 0x140], 0
mov qword ptr [rsp + 0x148], 0
mov qword ptr [rsp + 0x150], 0
mov qword ptr [rsp + 0x158], 0
mov rbx, 254
.inv_boucle:
lea rcx, [rsp + 0x138]
lea rdx, [rsp + 0x138]
call TLS11
mov rax, rbx
shr rax, 3
movzx eax, byte ptr [rsp + rax + 0x1f0]
mov rcx, rbx
and rcx, 7
shr rax, cl
test eax, 1
jz .inv_saut
lea rcx, [rsp + 0x138]
lea rdx, [rsp + 0x110]
call TLS11
.inv_saut:
dec rbx
jns .inv_boucle
; x = x2 · z2^(p−2) → x2 EN PLACE
lea rcx, [rsp + 0x48]
lea rdx, [rsp + 0x138]
call TLS11
; --- LA SÉRIALISATION : la mini-passe puis les QUATRE quads (P1) -------------
movabs r11, 0x7ffffffffffff
mov rax, qword ptr [rsp + 0x48]
mov rdx, rax
shr rdx, 51
and rax, r11
mov qword ptr [rsp + 0x48], rax
add qword ptr [rsp + 0x50], rdx
mov rax, qword ptr [rsp + 0x50]
mov rdx, rax
shr rdx, 51
and rax, r11
mov qword ptr [rsp + 0x50], rax
add qword ptr [rsp + 0x58], rdx
mov rax, qword ptr [rsp + 0x58]
mov rdx, rax
shr rdx, 51
and rax, r11
mov qword ptr [rsp + 0x58], rax
add qword ptr [rsp + 0x60], rdx
mov rax, qword ptr [rsp + 0x60]
mov rdx, rax
shr rdx, 51
and rax, r11
mov qword ptr [rsp + 0x60], rax
add qword ptr [rsp + 0x68], rdx
; les QUATRE quads (les décalages en miroir du décodage — le retour ×19
; du membre 4 est IMPOSSIBLE : la valeur < p, le théorème)
mov rax, qword ptr [rsp + 0x50]
shl rax, 51
add rax, qword ptr [rsp + 0x48]
mov qword ptr [rdi], rax
mov rax, qword ptr [rsp + 0x50]
shr rax, 13
mov rdx, qword ptr [rsp + 0x58]
shl rdx, 38
add rax, rdx
mov qword ptr [rdi + 8], rax
mov rax, qword ptr [rsp + 0x58]
shr rax, 26
mov rdx, qword ptr [rsp + 0x60]
shl rdx, 25
add rax, rdx
mov qword ptr [rdi + 16], rax
mov rax, qword ptr [rsp + 0x60]
shr rax, 39
mov rdx, qword ptr [rsp + 0x68]
shl rdx, 12
add rax, rdx
mov qword ptr [rdi + 24], rax
xor eax, eax
add rsp, 0x210
pop rbp
pop rbx
pop rdi
ret
