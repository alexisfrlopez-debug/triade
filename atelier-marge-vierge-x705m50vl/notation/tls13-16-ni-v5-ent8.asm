; tls13-16-ni-v5-ent8 · LE CORPS AESENC DES HUIT BLOCS ENTRELACÉS AUX HUIT CALENDRIERS INDÉPENDANTS (x705m50vl, la vague 12)
; LE LEVIER NOMMÉ DE V4 : l'indépendance d'adressage, PAS la précalculée — HUIT calendriers de
; clés aux adresses INDÉPENDANTES (un registre de base PAR flot : rbx · rdi · rsi · rbp · r12-r15),
; les corps aesenc des HUIT blocs ENTRELACÉS par tour : à chaque tour, la lecture rk du flot j (de
; SA base propre) précède IMMÉDIATEMENT l'aesenc du flot j, les sept autres paires exécutent
; pendant sa latence — le masquage nommé de l'instruction au double de v4 ; le mode d'adressage
; [base + rax + déplacement] — le déplacement plié au mode, aucun add, aucune table
; LA FAUTE DE LA PASSE MORTE NOMMÉE : le corps précédent chargeait TOUTES les clés de tour
; de la SEULE base rbx (huit calendriers déclarés, UN vécu) — le vice relevé à la reprise,
; le corps réécrit aux HUIT bases, la vérification différentielle par flot le juge
; LE CONTRAT DÉRIVÉ DU FLUX V2 (R4) : ABI msx64 — rcx = clés : LE TABLEAU DES HUIT POINTEURS de
; calendriers, rdx = entrées, r8 = sorties, r9 = N blocs (1..256) ; LE BLOC i AU CALENDRIER
; (i mod 8) — les groupes complets EN TÊTE (le flot j prend les blocs 8g+j), la QUEUE de
; (N mod 8) blocs au calendrier [t] (le bloc 8G+t ↔ calendrier t) ; rax = 0 au retour ; LA BORNE
; N ≤ 256 fail-closed : rax = -2, RIEN chiffré hors borne ; les registres xmm0-xmm8 (tous
; volatils), AUCUN appel — les bases d'entrée/sortie gardées aux volatils rdx/r8 (la discipline
; de l'inline v4)
; Copie de laboratoire à la marge VIERGE 0xE800 — L'ÉCART AU PLAN NOMMÉ : le plan gelé posait
; ent8 à 0xE400 ; le corps entrelacé k=8 (≈1,2 Ko) NE TIENT PAS dans la fenêtre 0x200 — posé à
; 0xE800, la cause mesurée (le compte d'octets assemblés), le plan demeuré gelé
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
mov rbx, qword ptr [rcx]
mov rdi, qword ptr [rcx + 8]
mov rsi, qword ptr [rcx + 0x10]
mov rbp, qword ptr [rcx + 0x18]
mov r12, qword ptr [rcx + 0x20]
mov r13, qword ptr [rcx + 0x28]
mov r14, qword ptr [rcx + 0x30]
mov r15, qword ptr [rcx + 0x38]
mov rcx, r9
shr ecx, 3
mov r10d, r9d
and r10d, 7
xor eax, eax
test ecx, ecx
jz .queue
.boucle:
movdqu xmm0, xmmword ptr [rdx + rax]
movdqu xmm1, xmmword ptr [rdx + rax + 16]
movdqu xmm2, xmmword ptr [rdx + rax + 32]
movdqu xmm3, xmmword ptr [rdx + rax + 48]
movdqu xmm4, xmmword ptr [rdx + rax + 64]
movdqu xmm5, xmmword ptr [rdx + rax + 80]
movdqu xmm6, xmmword ptr [rdx + rax + 96]
movdqu xmm7, xmmword ptr [rdx + rax + 112]
movdqu xmm8, xmmword ptr [rbx]
pxor xmm0, xmm8
movdqu xmm8, xmmword ptr [rdi]
pxor xmm1, xmm8
movdqu xmm8, xmmword ptr [rsi]
pxor xmm2, xmm8
movdqu xmm8, xmmword ptr [rbp]
pxor xmm3, xmm8
movdqu xmm8, xmmword ptr [r12]
pxor xmm4, xmm8
movdqu xmm8, xmmword ptr [r13]
pxor xmm5, xmm8
movdqu xmm8, xmmword ptr [r14]
pxor xmm6, xmm8
movdqu xmm8, xmmword ptr [r15]
pxor xmm7, xmm8
movdqu xmm8, xmmword ptr [rbx + 0x10]
aesenc xmm0, xmm8
movdqu xmm8, xmmword ptr [rdi + 0x10]
aesenc xmm1, xmm8
movdqu xmm8, xmmword ptr [rsi + 0x10]
aesenc xmm2, xmm8
movdqu xmm8, xmmword ptr [rbp + 0x10]
aesenc xmm3, xmm8
movdqu xmm8, xmmword ptr [r12 + 0x10]
aesenc xmm4, xmm8
movdqu xmm8, xmmword ptr [r13 + 0x10]
aesenc xmm5, xmm8
movdqu xmm8, xmmword ptr [r14 + 0x10]
aesenc xmm6, xmm8
movdqu xmm8, xmmword ptr [r15 + 0x10]
aesenc xmm7, xmm8
movdqu xmm8, xmmword ptr [rbx + 0x20]
aesenc xmm0, xmm8
movdqu xmm8, xmmword ptr [rdi + 0x20]
aesenc xmm1, xmm8
movdqu xmm8, xmmword ptr [rsi + 0x20]
aesenc xmm2, xmm8
movdqu xmm8, xmmword ptr [rbp + 0x20]
aesenc xmm3, xmm8
movdqu xmm8, xmmword ptr [r12 + 0x20]
aesenc xmm4, xmm8
movdqu xmm8, xmmword ptr [r13 + 0x20]
aesenc xmm5, xmm8
movdqu xmm8, xmmword ptr [r14 + 0x20]
aesenc xmm6, xmm8
movdqu xmm8, xmmword ptr [r15 + 0x20]
aesenc xmm7, xmm8
movdqu xmm8, xmmword ptr [rbx + 0x30]
aesenc xmm0, xmm8
movdqu xmm8, xmmword ptr [rdi + 0x30]
aesenc xmm1, xmm8
movdqu xmm8, xmmword ptr [rsi + 0x30]
aesenc xmm2, xmm8
movdqu xmm8, xmmword ptr [rbp + 0x30]
aesenc xmm3, xmm8
movdqu xmm8, xmmword ptr [r12 + 0x30]
aesenc xmm4, xmm8
movdqu xmm8, xmmword ptr [r13 + 0x30]
aesenc xmm5, xmm8
movdqu xmm8, xmmword ptr [r14 + 0x30]
aesenc xmm6, xmm8
movdqu xmm8, xmmword ptr [r15 + 0x30]
aesenc xmm7, xmm8
movdqu xmm8, xmmword ptr [rbx + 0x40]
aesenc xmm0, xmm8
movdqu xmm8, xmmword ptr [rdi + 0x40]
aesenc xmm1, xmm8
movdqu xmm8, xmmword ptr [rsi + 0x40]
aesenc xmm2, xmm8
movdqu xmm8, xmmword ptr [rbp + 0x40]
aesenc xmm3, xmm8
movdqu xmm8, xmmword ptr [r12 + 0x40]
aesenc xmm4, xmm8
movdqu xmm8, xmmword ptr [r13 + 0x40]
aesenc xmm5, xmm8
movdqu xmm8, xmmword ptr [r14 + 0x40]
aesenc xmm6, xmm8
movdqu xmm8, xmmword ptr [r15 + 0x40]
aesenc xmm7, xmm8
movdqu xmm8, xmmword ptr [rbx + 0x50]
aesenc xmm0, xmm8
movdqu xmm8, xmmword ptr [rdi + 0x50]
aesenc xmm1, xmm8
movdqu xmm8, xmmword ptr [rsi + 0x50]
aesenc xmm2, xmm8
movdqu xmm8, xmmword ptr [rbp + 0x50]
aesenc xmm3, xmm8
movdqu xmm8, xmmword ptr [r12 + 0x50]
aesenc xmm4, xmm8
movdqu xmm8, xmmword ptr [r13 + 0x50]
aesenc xmm5, xmm8
movdqu xmm8, xmmword ptr [r14 + 0x50]
aesenc xmm6, xmm8
movdqu xmm8, xmmword ptr [r15 + 0x50]
aesenc xmm7, xmm8
movdqu xmm8, xmmword ptr [rbx + 0x60]
aesenc xmm0, xmm8
movdqu xmm8, xmmword ptr [rdi + 0x60]
aesenc xmm1, xmm8
movdqu xmm8, xmmword ptr [rsi + 0x60]
aesenc xmm2, xmm8
movdqu xmm8, xmmword ptr [rbp + 0x60]
aesenc xmm3, xmm8
movdqu xmm8, xmmword ptr [r12 + 0x60]
aesenc xmm4, xmm8
movdqu xmm8, xmmword ptr [r13 + 0x60]
aesenc xmm5, xmm8
movdqu xmm8, xmmword ptr [r14 + 0x60]
aesenc xmm6, xmm8
movdqu xmm8, xmmword ptr [r15 + 0x60]
aesenc xmm7, xmm8
movdqu xmm8, xmmword ptr [rbx + 0x70]
aesenc xmm0, xmm8
movdqu xmm8, xmmword ptr [rdi + 0x70]
aesenc xmm1, xmm8
movdqu xmm8, xmmword ptr [rsi + 0x70]
aesenc xmm2, xmm8
movdqu xmm8, xmmword ptr [rbp + 0x70]
aesenc xmm3, xmm8
movdqu xmm8, xmmword ptr [r12 + 0x70]
aesenc xmm4, xmm8
movdqu xmm8, xmmword ptr [r13 + 0x70]
aesenc xmm5, xmm8
movdqu xmm8, xmmword ptr [r14 + 0x70]
aesenc xmm6, xmm8
movdqu xmm8, xmmword ptr [r15 + 0x70]
aesenc xmm7, xmm8
movdqu xmm8, xmmword ptr [rbx + 0x80]
aesenc xmm0, xmm8
movdqu xmm8, xmmword ptr [rdi + 0x80]
aesenc xmm1, xmm8
movdqu xmm8, xmmword ptr [rsi + 0x80]
aesenc xmm2, xmm8
movdqu xmm8, xmmword ptr [rbp + 0x80]
aesenc xmm3, xmm8
movdqu xmm8, xmmword ptr [r12 + 0x80]
aesenc xmm4, xmm8
movdqu xmm8, xmmword ptr [r13 + 0x80]
aesenc xmm5, xmm8
movdqu xmm8, xmmword ptr [r14 + 0x80]
aesenc xmm6, xmm8
movdqu xmm8, xmmword ptr [r15 + 0x80]
aesenc xmm7, xmm8
movdqu xmm8, xmmword ptr [rbx + 0x90]
aesenc xmm0, xmm8
movdqu xmm8, xmmword ptr [rdi + 0x90]
aesenc xmm1, xmm8
movdqu xmm8, xmmword ptr [rsi + 0x90]
aesenc xmm2, xmm8
movdqu xmm8, xmmword ptr [rbp + 0x90]
aesenc xmm3, xmm8
movdqu xmm8, xmmword ptr [r12 + 0x90]
aesenc xmm4, xmm8
movdqu xmm8, xmmword ptr [r13 + 0x90]
aesenc xmm5, xmm8
movdqu xmm8, xmmword ptr [r14 + 0x90]
aesenc xmm6, xmm8
movdqu xmm8, xmmword ptr [r15 + 0x90]
aesenc xmm7, xmm8
movdqu xmm8, xmmword ptr [rbx + 0xa0]
aesenclast xmm0, xmm8
movdqu xmm8, xmmword ptr [rdi + 0xa0]
aesenclast xmm1, xmm8
movdqu xmm8, xmmword ptr [rsi + 0xa0]
aesenclast xmm2, xmm8
movdqu xmm8, xmmword ptr [rbp + 0xa0]
aesenclast xmm3, xmm8
movdqu xmm8, xmmword ptr [r12 + 0xa0]
aesenclast xmm4, xmm8
movdqu xmm8, xmmword ptr [r13 + 0xa0]
aesenclast xmm5, xmm8
movdqu xmm8, xmmword ptr [r14 + 0xa0]
aesenclast xmm6, xmm8
movdqu xmm8, xmmword ptr [r15 + 0xa0]
aesenclast xmm7, xmm8
movdqu xmmword ptr [r8 + rax], xmm0
movdqu xmmword ptr [r8 + rax + 16], xmm1
movdqu xmmword ptr [r8 + rax + 32], xmm2
movdqu xmmword ptr [r8 + rax + 48], xmm3
movdqu xmmword ptr [r8 + rax + 64], xmm4
movdqu xmmword ptr [r8 + rax + 80], xmm5
movdqu xmmword ptr [r8 + rax + 96], xmm6
movdqu xmmword ptr [r8 + rax + 112], xmm7
add rax, 128
dec ecx
jnz .boucle
.queue:
test r10d, r10d
jz .fin
xor ecx, ecx
.queue_boucle:
mov rbx, qword ptr [r11 + rcx*8]
movdqu xmm0, xmmword ptr [rdx + rax]
movdqu xmm8, xmmword ptr [rbx]
pxor xmm0, xmm8
movdqu xmm8, xmmword ptr [rbx + 0x10]
aesenc xmm0, xmm8
movdqu xmm8, xmmword ptr [rbx + 0x20]
aesenc xmm0, xmm8
movdqu xmm8, xmmword ptr [rbx + 0x30]
aesenc xmm0, xmm8
movdqu xmm8, xmmword ptr [rbx + 0x40]
aesenc xmm0, xmm8
movdqu xmm8, xmmword ptr [rbx + 0x50]
aesenc xmm0, xmm8
movdqu xmm8, xmmword ptr [rbx + 0x60]
aesenc xmm0, xmm8
movdqu xmm8, xmmword ptr [rbx + 0x70]
aesenc xmm0, xmm8
movdqu xmm8, xmmword ptr [rbx + 0x80]
aesenc xmm0, xmm8
movdqu xmm8, xmmword ptr [rbx + 0x90]
aesenc xmm0, xmm8
movdqu xmm8, xmmword ptr [rbx + 0xa0]
aesenclast xmm0, xmm8
movdqu xmmword ptr [r8 + rax], xmm0
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
