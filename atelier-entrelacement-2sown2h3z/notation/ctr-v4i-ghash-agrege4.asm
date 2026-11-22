; ctr-v4i-ghash-agrege4 · LE COULOIR DE COMPOSITION ENTRELACÉE CTR v4i ×
; GHASH AGRÉGÉ-4 PAR GROUPES DE QUATRE (2sown2h3z, la vague 15) — LA
; MESURE SUIVANTE nommée à l'Entrée 385 : la projection ~1,6 c/octet@4096
; DOIT devenir une mesure, cible pré-enregistrée ≤ 2,0 c/octet@4096.
; LA STRUCTURE PAR GROUPE DE QUATRE BLOCS :
;   (1) LE CTR v4i : les QUATRE courants de bloc ENTRELACÉS, LE calendrier
;       de clés PARTAGÉ (la lecture rk UNE fois par tour, aesenc ×4 — le
;       masquage nommé de v4, la leçon D249 : les lectures partagées
;       demeurent devant l'indépendance d'adressage) ;
;   (2) LA FENÊTRE GHASH AGRÉGÉE : les QUATRE produits X_j ⊗ H^{N-4g-j}
;       (la table du juge, UNE entrée par bloc — l'entrée i porte H^{N-i},
;       0-based), chaque terme TWISTÉ comme le scellé twiste son entrée Y
;       (le miroir exact du couloir h1mz2sr8s), l'accumulation 256 bits
;       PAR XOR, LA RÉDUCTION alg9 UNIQUE À LA FIN DE TOUT LE MESSAGE
;       (la linéarité de la réduction : la somme NON réduite des N
;       produits se réduit UNE fois — la généralisation nommée de la
;       fenêtre v14, l'algèbre au registre) ;
;   (3) LA FILE (N mod 4) : les blocs de queue au produit simple (le
;       même accumulateur, la même table — aucune réduction intermédiaire).
; LE REPLI : r10 = 0 → LA CHAÎNE SCELLÉE PAR BLOC (l'AES scellé 0xDF00
; par bloc de compteur, le GHASH scellé 0xDFC0 chaîné par bloc — la
; référence intégralement scellée, jamais un chemin mort).
; ABI (msx64) : rcx = calendrier de clés (11×16 o), rdx = blocs de
; compteur (N×16 o), r8 = clair, r9 = chiffré-sortie (N×16 o + LE TAG
; 16 o posé à [r9 + N*16]), r10 = le verdict de session (1 = couloir,
; 0 = repli), r11 = N (1..256) ; LA TABLE des puissances à l'adresse
; FIXE 0x508000 (N×16 o, l'entrée i = H^{N-i}, 0-based — DÉRIVÉE PAR LE
; SCELLÉ, le domaine du juge) ; rax = 0 au retour ; LA BORNE N ≤ 256
; fail-closed : rax = -2, RIEN chiffré hors borne.
; Copie de laboratoire à la marge VIERGE 0xF800 — le scellé AES (slot
; 0xDF00), le scellé GHASH (slot 0xDFC0), les couloirs v13/v14
; (0xE200-0xEA00, 0xF300) INTACTS.
push rbx
push rdi
push rsi
push rbp
push r12
push r13
push r14
push r15
sub rsp, 0x50
test r11, r11
jz .refus
cmp r11, 0x100
ja .refus
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
; L'ACCUMULATEUR 256 bits À ZÉRO (la somme différée de TOUT le message)
pxor xmm14, xmm14
pxor xmm15, xmm15
; les registres de travail
mov rbx, rcx
mov rdi, rdx
mov rsi, r8
mov rbp, r9
mov r12, 0x508000
mov r13, r11
shr r13, 2
xor r14, r14
test r13, r13
jz .queue
; ==== LE GROUPE DE QUATRE : CTR v4i ENTRELACÉ × LA FENÊTRE AGRÉGÉE ====
.groupe:
movdqu xmm0, xmmword ptr [rdi + r14]
movdqu xmm1, xmmword ptr [rdi + r14 + 16]
movdqu xmm2, xmmword ptr [rdi + r14 + 32]
movdqu xmm3, xmmword ptr [rdi + r14 + 48]
movdqu xmm4, xmmword ptr [rbx]
pxor xmm0, xmm4
pxor xmm1, xmm4
pxor xmm2, xmm4
pxor xmm3, xmm4
movdqu xmm4, xmmword ptr [rbx + 0x10]
aesenc xmm0, xmm4
aesenc xmm1, xmm4
aesenc xmm2, xmm4
aesenc xmm3, xmm4
movdqu xmm4, xmmword ptr [rbx + 0x20]
aesenc xmm0, xmm4
aesenc xmm1, xmm4
aesenc xmm2, xmm4
aesenc xmm3, xmm4
movdqu xmm4, xmmword ptr [rbx + 0x30]
aesenc xmm0, xmm4
aesenc xmm1, xmm4
aesenc xmm2, xmm4
aesenc xmm3, xmm4
movdqu xmm4, xmmword ptr [rbx + 0x40]
aesenc xmm0, xmm4
aesenc xmm1, xmm4
aesenc xmm2, xmm4
aesenc xmm3, xmm4
movdqu xmm4, xmmword ptr [rbx + 0x50]
aesenc xmm0, xmm4
aesenc xmm1, xmm4
aesenc xmm2, xmm4
aesenc xmm3, xmm4
movdqu xmm4, xmmword ptr [rbx + 0x60]
aesenc xmm0, xmm4
aesenc xmm1, xmm4
aesenc xmm2, xmm4
aesenc xmm3, xmm4
movdqu xmm4, xmmword ptr [rbx + 0x70]
aesenc xmm0, xmm4
aesenc xmm1, xmm4
aesenc xmm2, xmm4
aesenc xmm3, xmm4
movdqu xmm4, xmmword ptr [rbx + 0x80]
aesenc xmm0, xmm4
aesenc xmm1, xmm4
aesenc xmm2, xmm4
aesenc xmm3, xmm4
movdqu xmm4, xmmword ptr [rbx + 0x90]
aesenc xmm0, xmm4
aesenc xmm1, xmm4
aesenc xmm2, xmm4
aesenc xmm3, xmm4
movdqu xmm4, xmmword ptr [rbx + 0xa0]
aesenclast xmm0, xmm4
aesenclast xmm1, xmm4
aesenclast xmm2, xmm4
aesenclast xmm3, xmm4
; LES CHIFFRÉS (C_j = KS_j ⊕ P_j)
pxor xmm0, xmmword ptr [rsi + r14]
pxor xmm1, xmmword ptr [rsi + r14 + 16]
pxor xmm2, xmmword ptr [rsi + r14 + 32]
pxor xmm3, xmmword ptr [rsi + r14 + 48]
movdqu xmmword ptr [rbp + r14], xmm0
movdqu xmmword ptr [rbp + r14 + 16], xmm1
movdqu xmmword ptr [rbp + r14 + 32], xmm2
movdqu xmmword ptr [rbp + r14 + 48], xmm3
; LA FENÊTRE GHASH : les QUATRE produits (C_j ⊗ table[4g+j]) à l'accumulateur
movdqa xmm8, xmm1
movdqa xmm9, xmm2
movdqa xmm10, xmm3
pshufb xmm0, xmm7
movdqu xmm1, xmmword ptr [r12 + r14]
call .produit256
pxor xmm14, xmm0
pxor xmm15, xmm2
movdqa xmm0, xmm8
pshufb xmm0, xmm7
movdqu xmm1, xmmword ptr [r12 + r14 + 16]
call .produit256
pxor xmm14, xmm0
pxor xmm15, xmm2
movdqa xmm0, xmm9
pshufb xmm0, xmm7
movdqu xmm1, xmmword ptr [r12 + r14 + 32]
call .produit256
pxor xmm14, xmm0
pxor xmm15, xmm2
movdqa xmm0, xmm10
pshufb xmm0, xmm7
movdqu xmm1, xmmword ptr [r12 + r14 + 48]
call .produit256
pxor xmm14, xmm0
pxor xmm15, xmm2
add r14, 64
dec r13
jnz .groupe
; ==== LA FILE (N mod 4) : le produit simple au même accumulateur ====
.queue:
mov r13, r11
and r13, 3
test r13, r13
jz .reduction
.queue_boucle:
movdqu xmm0, xmmword ptr [rdi + r14]
movdqu xmm4, xmmword ptr [rbx]
pxor xmm0, xmm4
movdqu xmm4, xmmword ptr [rbx + 0x10]
aesenc xmm0, xmm4
movdqu xmm4, xmmword ptr [rbx + 0x20]
aesenc xmm0, xmm4
movdqu xmm4, xmmword ptr [rbx + 0x30]
aesenc xmm0, xmm4
movdqu xmm4, xmmword ptr [rbx + 0x40]
aesenc xmm0, xmm4
movdqu xmm4, xmmword ptr [rbx + 0x50]
aesenc xmm0, xmm4
movdqu xmm4, xmmword ptr [rbx + 0x60]
aesenc xmm0, xmm4
movdqu xmm4, xmmword ptr [rbx + 0x70]
aesenc xmm0, xmm4
movdqu xmm4, xmmword ptr [rbx + 0x80]
aesenc xmm0, xmm4
movdqu xmm4, xmmword ptr [rbx + 0x90]
aesenc xmm0, xmm4
movdqu xmm4, xmmword ptr [rbx + 0xa0]
aesenclast xmm0, xmm4
pxor xmm0, xmmword ptr [rsi + r14]
movdqu xmmword ptr [rbp + r14], xmm0
pshufb xmm0, xmm7
movdqu xmm1, xmmword ptr [r12 + r14]
call .produit256
pxor xmm14, xmm0
pxor xmm15, xmm2
add r14, 16
dec r13
jnz .queue_boucle
; ==== LA RÉDUCTION alg9 UNIQUE (la fin du message : UNE fois) ====
.reduction:
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
pshufb xmm0, xmm7
mov rax, r11
shl rax, 4
movdqu xmmword ptr [rbp + rax], xmm0
xor eax, eax
jmp .epilogue
; ==== LE REPLI : LA CHAÎNE SCELLÉE PAR BLOC (r10 = 0) ====
; l'AES scellé 0xDF00 (rcx = clés, rdx = bloc, r8 = sortie) par bloc de
; compteur ; le GHASH scellé 0xDFC0 (rcx = Z, rdx = X, r8 = H, r10 = 0)
; chaîné par bloc — LA RÉFÉRENCE INTÉGRALEMENT SCELLÉE.
.repli:
mov rbx, rcx
mov rdi, rdx
mov rsi, r8
mov rbp, r9
mov r12, 0x508000
mov r13, r11
pxor xmm0, xmm0
movdqu xmmword ptr [rsp + 0x20], xmm0
xor r14, r14
.repli_boucle:
mov rax, r13
shl rax, 4
cmp r14, rax
jae .repli_fin
mov rcx, rbx
lea rdx, qword ptr [rdi + r14]
lea r8, qword ptr [rsp + 0x30]
call 0xDF00
movdqu xmm0, xmmword ptr [rsp + 0x30]
pxor xmm0, xmmword ptr [rsi + r14]
movdqu xmmword ptr [rbp + r14], xmm0
movdqu xmm1, xmmword ptr [rsp + 0x20]
pxor xmm0, xmm1
movdqu xmmword ptr [rsp + 0x40], xmm0
lea rcx, qword ptr [rsp + 0x20]
lea rdx, qword ptr [rsp + 0x40]
mov rax, r13
dec rax
shl rax, 4
lea r8, qword ptr [r12 + rax]
call 0xDFC0
add r14, 16
jmp .repli_boucle
.repli_fin:
movdqu xmm0, xmmword ptr [rsp + 0x20]
mov rax, r13
shl rax, 4
movdqu xmmword ptr [rbp + rax], xmm0
xor eax, eax
jmp .epilogue
; ==== LE PRODUIT 256 bits (xmm0 = X déjà bswapé, xmm1 = H^k BRUT ; la
;      sortie (xmm0:xmm2), xmm2 la moitié haute — LE TWIST de xmm1
;      appliqué comme le scellé twiste son entrée Y, PUIS le schoolbook
;      — LE MIROIR EXACT de h1mz2sr8s) ====
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
.epilogue:
add rsp, 0x50
pop r15
pop r14
pop r13
pop r12
pop rbp
pop rsi
pop rdi
pop rbx
ret
.refus:
mov rax, -2
jmp .epilogue
