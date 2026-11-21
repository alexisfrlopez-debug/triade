; ghash-pclmulqdq-karatsuba · LE COULOIR GHASH EN PCLMULQDQ (réduction Karatsuba
; 3× pclmulqdq pour le produit 128×128, la réduction par décalages d'alg9) ·
; contrat tls13-17:R1 TENU (R4) : rcx = Z sortie, rdx = X, r8 = Y, rax = 0,
; X/Y INTACTS, commutatif, le chevauchement Z∈{X,Y} permis (la sortie posée à
; la FIN, les lectures AVANT) ; LE DOMAINE dérivé et vérifié : Xi = N_X
; (l'entier gros-boutiste par pshufb inverse), Hkey = twist(N_Y) = N_Y·x mod
; P̃ (le twist SANS BRANCHE : psllq par qword + le carry inter-qword par
; psrlq63/pslldq8/por + la retenue du bit 127 par pcmpgtd/pand/pxor sur la
; constante C = 0xC200000000000000||1) ; le sel Karatsuba HK = qs(Hkey)⊕Hkey ;
; la réduction alg9 PAR DÉCALAGES (psllq/psrlq/pslldq/psrldq — AUCUN clmul) ;
; LE DISPATCH HISSÉ : r10 = le verdict de SESSION (le bit 0 = PCLMULQDQ,
; la sonde-session sonde UNE fois pour tous les corridors) — r10&1 = 0 → LE
; REPLI au scellé GPR (jmp à la copie du scellé, JAMAIS un chemin mort) ;
; aucune donnée secrète ne touche une branche ni une adresse (le seul jcc
; porte sur r10 PUBLIC) ; les instructions à latence variable (div, idiv)
; ABSENTES par construction
; Copie de laboratoire à la marge VIERGE 0xD200 — le scellé (slot 0xDFC0)
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
pshufd xmm2, xmm1, 0x4e
pxor xmm2, xmm1
movdqa xmm3, xmm0
pshufd xmm5, xmm0, 0x4e
pxor xmm5, xmm0
pclmulqdq xmm0, xmm1, 0x00
pclmulqdq xmm3, xmm1, 0x11
pclmulqdq xmm5, xmm2, 0x00
pxor xmm5, xmm0
pxor xmm5, xmm3
movdqa xmm4, xmm5
psrldq xmm5, 8
pslldq xmm4, 8
pxor xmm3, xmm5
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
pxor xmm3, xmm5
movdqa xmm4, xmm0
psrlq xmm0, 1
pxor xmm3, xmm4
pxor xmm4, xmm0
psrlq xmm0, 5
pxor xmm0, xmm4
psrlq xmm0, 1
pxor xmm0, xmm3
pshufb xmm0, xmm7
movdqu [rcx], xmm0
xor rax, rax
add rsp, 0x28
ret
.repli:
add rsp, 0x28
jmp 0xdfc0
