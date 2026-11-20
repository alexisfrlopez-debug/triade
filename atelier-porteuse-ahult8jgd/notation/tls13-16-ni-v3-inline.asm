; tls13-16-ni-v3-inline · L'INLINING DU BLOC NI : le corps aesenc POSÉ DANS LA
; BOUCLE — plus AUCUN appel : l'économie du stub (4,1 cycles/appel mesurés au v2),
; la perte de l'isolement du bloc scellé NOMMÉE (le corps n'est plus une brique
; interchangeable — le prix de la vitesse) ; LE POINTEUR AVANCE PAR LE MODE
; D'ADRESSAGE [r13 + rax*8] : l'indice rax compte en QUADS (8 o), 2 par bloc —
; aucun add de pointeur, aucune table : l'adresse EST le mode d'adressage
; LE DÉROULAGE k=4 : les QUATRE blocs partagent la clé de tour CHARGÉE UNE FOIS
; (movdqu xmm4 par tour, 4 aesenc servis — la lecture RK payée 1 fois par 4 blocs)
; ABI msx64 (rcx = clés, rdx = entrées, r8 = sorties, r9 = N blocs) — le contrat
; du flux v2 INTACT ; les registres xmm0-xmm4 (TOUS volatils) ; le reste N mod 4
; à la boucle k=1 de tête (le cas général tenu) ; le repli au scellé tls13-16
; (copie 0xC400) au décalage quad [r13 + rbx*8] (rbx NON-VOLATIL : survit à
; l'appelé) ; le sondage CPUID UNE fois par flot
; Copie de laboratoire à la marge VIERGE 0xD800 — le scellé (slot 0xDF00) INTACT
push rbx
push rbp
push r12
push r13
push r14
push r15
sub rsp, 0x28
test r9, r9
jz .fin
mov r12, rcx
mov r13, rdx
mov r14, r8
mov r15, r9
mov eax, 1
xor ecx, ecx
cpuid
test ecx, 0x2000000
jz .repli_boucle
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
jmp .fin
.repli_boucle:
mov rbp, r15
xor ebx, ebx
.boucle_repli:
mov rcx, r12
lea rdx, [r13 + rbx*8]
lea r8, [r14 + rbx*8]
call 0xc400
lea rbx, [rbx + 2]
dec rbp
jnz .boucle_repli
.fin:
xor eax, eax
add rsp, 0x28
pop r15
pop r14
pop r13
pop r12
pop rbp
pop rbx
ret
