; tls13-16-ni-v5-ent4 · LE CORPS AESENC DES QUATRE BLOCS ENTRELACÉS AUX QUATRE CALENDRIERS INDÉPENDANTS (x705m50vl, la vague 12)
; LE LEVIER NOMMÉ DE V4 : l'indépendance d'adressage, PAS la précalculée — QUATRE calendriers de
; clés aux adresses INDÉPENDANTES (un registre de base PAR flot : rbx · rdi · rsi · rbp), les corps
; aesenc des QUATRE blocs ENTRELACÉS par tour : à chaque tour, la lecture rk du flot j (de SA base
; propre) précède IMMÉDIATEMENT l'aesenc du flot j, les trois autres paires exécutent pendant sa
; latence — le masquage nommé de l'instruction ; le mode d'adressage [base + rax + déplacement] —
; le déplacement plié au mode, aucun add, aucune table (la leçon v3-table : la précalcule n'est
; pas le levier)
; LE CONTRAT DÉRIVÉ DU FLUX V2 (R4 — le patch à contrat stable) : ABI msx64 — rcx = clés : LE
; TABLEAU DES QUATRE POINTEURS de calendriers (les adresses indépendantes du rig), rdx = entrées,
; r8 = sorties, r9 = N blocs (1..256) ; LE BLOC i CHIFFRÉ AU CALENDRIER (i mod 4) — les groupes
; complets EN TÊTE (le flot j prend les blocs 4g+j), la QUEUE de (N mod 4) blocs au calendrier
; [t] (le bloc 4G+t ↔ calendrier t) ; rax = 0 au retour ; LA BORNE N ≤ 256 fail-closed : rax = -2,
; RIEN chiffré hors borne ; les registres xmm0-xmm4 (tous volatils), AUCUN appel (l'inline de v4)
; Copie de laboratoire à la marge VIERGE 0xE200 — le scellé (slot 0xDF00) INTACT
push rbx
push rdi
push rsi
push rbp
push r12
push r13
push r14
push r15
test r9, r9
jz .fin
cmp r9, 0x100
ja .refus
mov r11, rcx
mov r12, rdx
mov r13, r8
mov r14, r9
mov rbx, qword ptr [rcx]
mov rdi, qword ptr [rcx + 8]
mov rsi, qword ptr [rcx + 0x10]
mov rbp, qword ptr [rcx + 0x18]
mov rcx, r14
shr ecx, 2
mov r10d, r14d
and r10d, 3
xor eax, eax
test ecx, ecx
jz .queue
.boucle:
movdqu xmm0, xmmword ptr [r12 + rax]
movdqu xmm1, xmmword ptr [r12 + rax + 16]
movdqu xmm2, xmmword ptr [r12 + rax + 32]
movdqu xmm3, xmmword ptr [r12 + rax + 48]
movdqu xmm4, xmmword ptr [rbx]
pxor xmm0, xmm4
movdqu xmm4, xmmword ptr [rdi]
pxor xmm1, xmm4
movdqu xmm4, xmmword ptr [rsi]
pxor xmm2, xmm4
movdqu xmm4, xmmword ptr [rbp]
pxor xmm3, xmm4
movdqu xmm4, xmmword ptr [rbx + 0x10]
aesenc xmm0, xmm4
movdqu xmm4, xmmword ptr [rdi + 0x10]
aesenc xmm1, xmm4
movdqu xmm4, xmmword ptr [rsi + 0x10]
aesenc xmm2, xmm4
movdqu xmm4, xmmword ptr [rbp + 0x10]
aesenc xmm3, xmm4
movdqu xmm4, xmmword ptr [rbx + 0x20]
aesenc xmm0, xmm4
movdqu xmm4, xmmword ptr [rdi + 0x20]
aesenc xmm1, xmm4
movdqu xmm4, xmmword ptr [rsi + 0x20]
aesenc xmm2, xmm4
movdqu xmm4, xmmword ptr [rbp + 0x20]
aesenc xmm3, xmm4
movdqu xmm4, xmmword ptr [rbx + 0x30]
aesenc xmm0, xmm4
movdqu xmm4, xmmword ptr [rdi + 0x30]
aesenc xmm1, xmm4
movdqu xmm4, xmmword ptr [rsi + 0x30]
aesenc xmm2, xmm4
movdqu xmm4, xmmword ptr [rbp + 0x30]
aesenc xmm3, xmm4
movdqu xmm4, xmmword ptr [rbx + 0x40]
aesenc xmm0, xmm4
movdqu xmm4, xmmword ptr [rdi + 0x40]
aesenc xmm1, xmm4
movdqu xmm4, xmmword ptr [rsi + 0x40]
aesenc xmm2, xmm4
movdqu xmm4, xmmword ptr [rbp + 0x40]
aesenc xmm3, xmm4
movdqu xmm4, xmmword ptr [rbx + 0x50]
aesenc xmm0, xmm4
movdqu xmm4, xmmword ptr [rdi + 0x50]
aesenc xmm1, xmm4
movdqu xmm4, xmmword ptr [rsi + 0x50]
aesenc xmm2, xmm4
movdqu xmm4, xmmword ptr [rbp + 0x50]
aesenc xmm3, xmm4
movdqu xmm4, xmmword ptr [rbx + 0x60]
aesenc xmm0, xmm4
movdqu xmm4, xmmword ptr [rdi + 0x60]
aesenc xmm1, xmm4
movdqu xmm4, xmmword ptr [rsi + 0x60]
aesenc xmm2, xmm4
movdqu xmm4, xmmword ptr [rbp + 0x60]
aesenc xmm3, xmm4
movdqu xmm4, xmmword ptr [rbx + 0x70]
aesenc xmm0, xmm4
movdqu xmm4, xmmword ptr [rdi + 0x70]
aesenc xmm1, xmm4
movdqu xmm4, xmmword ptr [rsi + 0x70]
aesenc xmm2, xmm4
movdqu xmm4, xmmword ptr [rbp + 0x70]
aesenc xmm3, xmm4
movdqu xmm4, xmmword ptr [rbx + 0x80]
aesenc xmm0, xmm4
movdqu xmm4, xmmword ptr [rdi + 0x80]
aesenc xmm1, xmm4
movdqu xmm4, xmmword ptr [rsi + 0x80]
aesenc xmm2, xmm4
movdqu xmm4, xmmword ptr [rbp + 0x80]
aesenc xmm3, xmm4
movdqu xmm4, xmmword ptr [rbx + 0x90]
aesenc xmm0, xmm4
movdqu xmm4, xmmword ptr [rdi + 0x90]
aesenc xmm1, xmm4
movdqu xmm4, xmmword ptr [rsi + 0x90]
aesenc xmm2, xmm4
movdqu xmm4, xmmword ptr [rbp + 0x90]
aesenc xmm3, xmm4
movdqu xmm4, xmmword ptr [rbx + 0xa0]
aesenclast xmm0, xmm4
movdqu xmm4, xmmword ptr [rdi + 0xa0]
aesenclast xmm1, xmm4
movdqu xmm4, xmmword ptr [rsi + 0xa0]
aesenclast xmm2, xmm4
movdqu xmm4, xmmword ptr [rbp + 0xa0]
aesenclast xmm3, xmm4
movdqu xmmword ptr [r13 + rax], xmm0
movdqu xmmword ptr [r13 + rax + 16], xmm1
movdqu xmmword ptr [r13 + rax + 32], xmm2
movdqu xmmword ptr [r13 + rax + 48], xmm3
add rax, 64
dec ecx
jnz .boucle
.queue:
test r10d, r10d
jz .fin
xor ecx, ecx
.queue_boucle:
mov rbx, qword ptr [r11 + rcx*8]
movdqu xmm0, xmmword ptr [r12 + rax]
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
movdqu xmmword ptr [r13 + rax], xmm0
add rax, 16
inc ecx
cmp ecx, r10d
jb .queue_boucle
.fin:
xor eax, eax
.epilogue:
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
