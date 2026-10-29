; http-04-chercher · brouillon · premier en-tête nommé · http-04:R1 · e50004
; L'unique comparaison insensible à la casse du domaine http (I3 — A-Z versus
; a-z, 0x20 d'écart) vit ICI et nulle part ailleurs ; l'analyse passe par
; http-01 (itération T5) et http-03 (parsing) — aucun autre appel, aucun IAT ;
; la zone d'accueil (32 o, celle de http-03) n'est écrite qu'en cas de trouve
; (Q1-Q3 : copie depuis la zone locale APRÈS le verdict — jamais d'écriture
; partielle sur les chemins absent/invalide).
; entrée : rcx = bloc d'en-têtes, rdx = longueur, r8 = nom cherché, r9 = longueur
;          nom (> 0), [arg5] = zone 32 o
; sortie : rax = 0 trouvé (zone remplie) / 1 absent / 2 tête invalide
push rbx
push rbp
push r12
push r13
push r14
push r15
sub rsp, 0x48
mov rbx, rcx
mov rbp, rdx
mov r12, r8
mov r13, r9
; arg5 (zone d'accueil) : loge msx64 [entrée+0x28] — 6 push + sub 0x48
; = 0x78 de prologue, donc [rsp+0xA0] après prologue
mov r14, qword ptr [rsp + 0xA0]
xor r15d, r15d
.boucle:
mov rcx, rbx
mov rdx, rbp
mov r8, r15
call HTTP_LIGNE
test rax, rax
jne .invalide
mov r15, r8
test rdx, rdx
je .absent
mov r10, r8
sub r10, rdx
sub r10, 2
lea rcx, [rbx + r10]
lea r8, [rsp + 0x20]
call HTTP_ENTETE
test rax, rax
jne .invalide
mov rax, qword ptr [rsp + 0x20]
mov rdx, qword ptr [rsp + 0x28]
cmp rdx, r13
jne .suivante
xor r11d, r11d
.cmp_nom:
cmp r11, r13
jae .trouve
movzx r9d, byte ptr [rax + r11]
movzx r10d, byte ptr [r12 + r11]
cmp r9, 0x61
jb .pas_min1
cmp r9, 0x7A
ja .pas_min1
sub r9, 0x20
.pas_min1:
cmp r10, 0x61
jb .pas_min2
cmp r10, 0x7A
ja .pas_min2
sub r10, 0x20
.pas_min2:
cmp r9, r10
jne .suivante
add r11, 1
jmp .cmp_nom
.trouve:
mov rax, qword ptr [rsp + 0x20]
mov qword ptr [r14], rax
mov rax, qword ptr [rsp + 0x28]
mov qword ptr [r14 + 8], rax
mov rax, qword ptr [rsp + 0x30]
mov qword ptr [r14 + 16], rax
mov rax, qword ptr [rsp + 0x38]
mov qword ptr [r14 + 24], rax
xor eax, eax
jmp .fin
.suivante:
jmp .boucle
.absent:
mov eax, 1
jmp .fin
.invalide:
mov eax, 2
.fin:
add rsp, 0x48
pop r15
pop r14
pop r13
pop r12
pop rbp
pop rbx
ret
