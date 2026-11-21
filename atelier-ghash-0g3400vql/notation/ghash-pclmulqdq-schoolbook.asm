; ghash-pclmulqdq-schoolbook · LE COULOIR GHASH EN PCLMULQDQ, LE PRODUIT
; SCHOOLBOOK (4× pclmulqdq : lo⊗lo, hi⊗hi, X.hi⊗H.lo, X.lo⊗H.hi — la mesure
; TRANCHE contre Karatsuba 3×) · le reste IDENTIQUE au karatsuba (le twist,
; le sel inutile ici, la réduction alg9, le dispatch r10, le repli scellé) ;
; contrat tls13-17:R1 TENU (R4) : rcx = Z, rdx = X, r8 = Y, rax = 0, X/Y
; INTACTS, commutatif, chevauchement permis
; Copie de laboratoire à la marge VIERGE 0xD400 — le scellé (slot 0xDFC0)
; INTACT
sub rsp, 0x28
test r10, 1
jz .repli
movabs rax, 0x08090a0b0c0d0e0f
mov qword ptr [rsp], rax
movabs rax, 0x0001020304050607
mov qword ptr [rsp + 8], rax
movdqu xmm7, [rsp]
movabs rax, 0x0000000000000001
mov qword ptr [rsp + 0x10], rax
movabs rax, 0xc200000000000000
mov qword ptr [rsp + 0x18], rax
movdqu xmm0, [rdx]
pshufb xmm0, xmm7
movdqu xmm1, [r8]
pshufb xmm1, xmm7
movdqa xmm4, xmm1
pshufd xmm5, xmm1, 0xff
psllq xmm1, 1
psrlq xmm4, 63
pslldq xmm4, 8
por xmm1, xmm4
pxor xmm6, xmm6
pcmpgtd xmm6, xmm5
movdqu xmm5, [rsp + 0x10]
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
pshufb xmm0, xmm7
movdqu [rcx], xmm0
xor rax, rax
add rsp, 0x28
ret
.repli:
add rsp, 0x28
jmp 0xdfc0
