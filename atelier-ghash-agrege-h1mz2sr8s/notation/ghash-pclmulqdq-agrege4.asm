; ghash-pclmulqdq-agrege4 · LE COULOIR GHASH AGRÉGÉ QUATRE BLOCS À RÉDUCTION
; DIFFÉRÉE (h1mz2sr8s, la vague 14) : le produit de X1..X4 contre les
; PUISSANCES de H (H⁴, H³, H², H — la table passée par l'appelant au
; domaine du juge), chaque terme TWISTÉ comme le scellé twiste son
; entrée Y (psllq/psrlq/pslldq/por + la retenue mod C — le miroir exact
; du twist schoolbook v13), l'accumulation 256 bits PAR XOR (l'addition du
; corps GF(2^128) est SANS RETENUE), LA RÉDUCTION alg9 UNIQUE à la fin
; (par décalages : AUCUN clmul en réduction, miroir du schoolbook v13),
; le produit SCHOOLBOOK par puissance (4× pclmulqdq — la mesure v13 a
; tranché : 63,39 c contre karatsuba 64,04, l'écart 0,65 c DANS l'IQR).
; LE REPLI : r10 = 0 → QUATRE appels chaînés au scellé 0xdfc0 (le produit
; par bloc — jamais un chemin mort) ; r10 = 1 → le couloir agrégé.
; ABI (l'extension du contrat tls13-17:R1) : rcx = Z (sortie 128 bits),
; rdx = ptr X (QUATRE blocs de 16 octets), r8 = ptr table [H⁴ ‖ H³ ‖ H² ‖ H]
; (64 octets, domaine du juge), r9 = ptr H (la valeur du juge — la voie de
; repli SEULE), r10 = le verdict de session ; rax = 0 en retour ; X, la
; table et H INTACTS ; Z posée à la FIN (chevauchement Z ∈ X permis).
; Copie de laboratoire à la marge VIERGE 0xF300 — le scellé (slot 0xDFC0)
; INTACT ; les marges v13 0xE800/0xEA00 INTACTES.
sub rsp, 0x50
test r10, 1
jz .repli
; LE MIROIR : la table de permutation octet (pshufb) et la constante C
movabs rax, 0x08090a0b0c0d0e0f
mov qword ptr [rsp], rax
movabs rax, 0x0001020304050607
mov qword ptr [rsp + 8], rax
movdqu xmm7, [rsp]
movabs rax, 0x0000000000000001
mov qword ptr [rsp + 0x10], rax
movabs rax, 0xc200000000000000
mov qword ptr [rsp + 0x18], rax
movdqu xmm6, [rsp + 0x10]
; L'ACCUMULATEUR 256 bits À ZÉRO (la somme différée — le XOR ne déborde pas)
pxor xmm14, xmm14
pxor xmm15, xmm15
; ==== LE BLOC 1 : X1 ⊗ H⁴ ====
movdqu xmm0, [rdx]
pshufb xmm0, xmm7
movdqu xmm1, [r8]
call .produit256
pxor xmm14, xmm0
pxor xmm15, xmm2
; ==== LE BLOC 2 : X2 ⊗ H³ ====
movdqu xmm0, [rdx + 0x10]
pshufb xmm0, xmm7
movdqu xmm1, [r8 + 0x10]
call .produit256
pxor xmm14, xmm0
pxor xmm15, xmm2
; ==== LE BLOC 3 : X3 ⊗ H² ====
movdqu xmm0, [rdx + 0x20]
pshufb xmm0, xmm7
movdqu xmm1, [r8 + 0x20]
call .produit256
pxor xmm14, xmm0
pxor xmm15, xmm2
; ==== LE BLOC 4 : X4 ⊗ H ====
movdqu xmm0, [rdx + 0x30]
pshufb xmm0, xmm7
movdqu xmm1, [r8 + 0x30]
call .produit256
pxor xmm14, xmm0
pxor xmm15, xmm2
; ==== LA RÉDUCTION alg9 UNIQUE (différée — UNE fois pour les quatre) ====
movdqa xmm0, xmm14
movdqa xmm2, xmm15
movdqa xmm4, xmm0
movdqa xmm5, xmm0
psllq xmm0, 5
pxor xmm5, xmm0
psllq xmm0, 1
pxor xmm0, xmm5
psllq xmm0, 57
movdqa xmm5, xmm0
pslldq xmm0, 8
psrldq xmm5, 8
pxor xmm0, xmm4
pxor xmm2, xmm5
movdqa xmm4, xmm0
psrlq xmm0, 1
pxor xmm2, xmm4
pxor xmm4, xmm0
psrlq xmm0, 5
pxor xmm0, xmm4
psrlq xmm0, 1
pxor xmm0, xmm2
; LA SORTIE (le miroir octet, Z posée à la fin)
pshufb xmm0, xmm7
movdqu [rcx], xmm0
xor rax, rax
add rsp, 0x50
ret
; ==== LE PRODUIT 256 bits (xmm0 = X déjà bswapé, xmm1 = H^k BRUT ; la
;      sortie (xmm0:xmm2), xmm2 la moitié haute — LE TWIST de xmm1
;      appliqué comme le scellé twiste son entrée Y, PUIS le schoolbook) ====
.produit256:
pshufb xmm1, xmm7
movdqa xmm4, xmm1
pshufd xmm5, xmm1, 0xff
psllq xmm1, 1
psrlq xmm4, 63
pslldq xmm4, 8
por xmm1, xmm4
pxor xmm6, xmm6
pcmpgtd xmm6, xmm5
movdqu xmm5, [rsp + 0x18]
pand xmm6, xmm5
pxor xmm1, xmm6
movdqa xmm2, xmm0
movdqa xmm3, xmm0
movdqa xmm5, xmm0
pclmulqdq xmm0, xmm1, 0x00
pclmulqdq xmm2, xmm1, 0x11
pclmulqdq xmm3, xmm1, 0x01
pclmulqdq xmm5, xmm1, 0x10
pxor xmm3, xmm5
movdqa xmm4, xmm3
psrldq xmm3, 8
pslldq xmm4, 8
pxor xmm2, xmm3
pxor xmm0, xmm4
ret
; ==== LE REPLI : QUATRE appels chaînés au scellé 0xdfc0 (r10 = 0, le
;      produit par bloc : Y1 = X1·H, Yk = (Y(k-1) ⊕ Xk)·H — la chaîne
;      exacte du scellé) ====
.repli:
mov qword ptr [rsp + 0x40], r9
mov r11, rdx
movdqu xmm8, [r11 + 0x10]
movdqu xmm9, [r11 + 0x20]
movdqu xmm10, [r11 + 0x30]
mov rdx, r11
mov r8, qword ptr [rsp + 0x40]
call 0xdfc0
movdqu xmm12, [rcx]
pxor xmm12, xmm8
movdqu [rsp + 0x30], xmm12
mov rdx, rsp
add rdx, 0x30
mov r8, qword ptr [rsp + 0x40]
call 0xdfc0
movdqu xmm12, [rcx]
pxor xmm12, xmm9
movdqu [rsp + 0x30], xmm12
mov rdx, rsp
add rdx, 0x30
mov r8, qword ptr [rsp + 0x40]
call 0xdfc0
movdqu xmm12, [rcx]
pxor xmm12, xmm10
movdqu [rsp + 0x30], xmm12
mov rdx, rsp
add rdx, 0x30
mov r8, qword ptr [rsp + 0x40]
call 0xdfc0
xor rax, rax
add rsp, 0x50
ret