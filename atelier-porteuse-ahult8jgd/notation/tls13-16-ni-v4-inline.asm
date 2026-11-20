; tls13-16-ni-v4-inline · LA PORTEUSE NUE INLINÉE : le verdict CPUID remonté à
; l'appelant (une fois par session — l'éléphant nommé : ~2 500 cycles par flot
; au bac virtualisé) ; le corps aesenc POSÉ DANS LA BOUCLE — plus AUCUN appel :
; l'économie du stub mesurée (la marginale 4,45 c/bloc contre 7,16 à l'appel)
; la perte de l'isolement NOMMÉE (le corps n'est plus une brique interchangeable
; — le prix de la vitesse) ; LE POINTEUR AU MODE D'ADRESSAGE [r13 + rax*8]
; (rax compte en QUADS, 2 par bloc — aucun add, aucune table, aucune pose)
; LE DÉROULAGE k=4 : les QUATRE blocs partagent la clé de tour CHARGÉE UNE FOIS
; (movdqu xmm4 par tour, 4 aesenc servis — la lecture RK payée 1 fois par 4)
; ABI msx64 (rcx = clés, rdx = entrées, r8 = sorties, r9 = N blocs) — le
; contrat du flux v2 INTACT (N quelconque) ; les registres xmm0-xmm4 (tous
; volatils) ; le reste N mod 4 à la boucle k=1 de tête ; AUCUN appel : aucune
; ombre de pile, les QUATRE poussées de non-volatils seules
; Copie de laboratoire à la marge VIERGE 0xDE00 — le scellé (slot 0xDF00)
; INTACT
push r12
push r13
push r14
push r15
test r9, r9
jz .fin
mov r12, rcx
mov r13, rdx
mov r14, r8
mov r15, r9
mov rcx, r15
and rcx, 3
xor eax, eax
test rcx, rcx
jz .prep4
.boucle_reste:
movdqu xmm0, xmmword ptr [r13 + rax*8]
movdqu xmm4, xmmword ptr [r12]
pxor xmm0, xmm4
movdqu xmm4, xmmword ptr [r12 + 0x10]
aesenc xmm0, xmm4
movdqu xmm4, xmmword ptr [r12 + 0x20]
aesenc xmm0, xmm4
movdqu xmm4, xmmword ptr [r12 + 0x30]
aesenc xmm0, xmm4
movdqu xmm4, xmmword ptr [r12 + 0x40]
aesenc xmm0, xmm4
movdqu xmm4, xmmword ptr [r12 + 0x50]
aesenc xmm0, xmm4
movdqu xmm4, xmmword ptr [r12 + 0x60]
aesenc xmm0, xmm4
movdqu xmm4, xmmword ptr [r12 + 0x70]
aesenc xmm0, xmm4
movdqu xmm4, xmmword ptr [r12 + 0x80]
aesenc xmm0, xmm4
movdqu xmm4, xmmword ptr [r12 + 0x90]
aesenc xmm0, xmm4
movdqu xmm4, xmmword ptr [r12 + 0xa0]
aesenclast xmm0, xmm4
movdqu xmmword ptr [r14 + rax*8], xmm0
lea rax, [rax + 2]
dec rcx
jnz .boucle_reste
.prep4:
mov rcx, r15
shr rcx, 2
test rcx, rcx
jz .fin
.boucle_ni:
movdqu xmm0, xmmword ptr [r13 + rax*8]
movdqu xmm1, xmmword ptr [r13 + rax*8 + 16]
movdqu xmm2, xmmword ptr [r13 + rax*8 + 32]
movdqu xmm3, xmmword ptr [r13 + rax*8 + 48]
movdqu xmm4, xmmword ptr [r12]
pxor xmm0, xmm4
pxor xmm1, xmm4
pxor xmm2, xmm4
pxor xmm3, xmm4
movdqu xmm4, xmmword ptr [r12 + 0x10]
aesenc xmm0, xmm4
aesenc xmm1, xmm4
aesenc xmm2, xmm4
aesenc xmm3, xmm4
movdqu xmm4, xmmword ptr [r12 + 0x20]
aesenc xmm0, xmm4
aesenc xmm1, xmm4
aesenc xmm2, xmm4
aesenc xmm3, xmm4
movdqu xmm4, xmmword ptr [r12 + 0x30]
aesenc xmm0, xmm4
aesenc xmm1, xmm4
aesenc xmm2, xmm4
aesenc xmm3, xmm4
movdqu xmm4, xmmword ptr [r12 + 0x40]
aesenc xmm0, xmm4
aesenc xmm1, xmm4
aesenc xmm2, xmm4
aesenc xmm3, xmm4
movdqu xmm4, xmmword ptr [r12 + 0x50]
aesenc xmm0, xmm4
aesenc xmm1, xmm4
aesenc xmm2, xmm4
aesenc xmm3, xmm4
movdqu xmm4, xmmword ptr [r12 + 0x60]
aesenc xmm0, xmm4
aesenc xmm1, xmm4
aesenc xmm2, xmm4
aesenc xmm3, xmm4
movdqu xmm4, xmmword ptr [r12 + 0x70]
aesenc xmm0, xmm4
aesenc xmm1, xmm4
aesenc xmm2, xmm4
aesenc xmm3, xmm4
movdqu xmm4, xmmword ptr [r12 + 0x80]
aesenc xmm0, xmm4
aesenc xmm1, xmm4
aesenc xmm2, xmm4
aesenc xmm3, xmm4
movdqu xmm4, xmmword ptr [r12 + 0x90]
aesenc xmm0, xmm4
aesenc xmm1, xmm4
aesenc xmm2, xmm4
aesenc xmm3, xmm4
movdqu xmm4, xmmword ptr [r12 + 0xa0]
aesenclast xmm0, xmm4
aesenclast xmm1, xmm4
aesenclast xmm2, xmm4
aesenclast xmm3, xmm4
movdqu xmmword ptr [r14 + rax*8], xmm0
movdqu xmmword ptr [r14 + rax*8 + 16], xmm1
movdqu xmmword ptr [r14 + rax*8 + 32], xmm2
movdqu xmmword ptr [r14 + rax*8 + 48], xmm3
lea rax, [rax + 8]
dec rcx
jnz .boucle_ni
.fin:
xor eax, eax
pop r15
pop r14
pop r13
pop r12
ret
