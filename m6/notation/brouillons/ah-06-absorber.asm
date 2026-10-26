; ah-06-absorber · brouillon étiqueté — spec ah-06:R1, bloc carte d40006
; absorption tamponnée : absorber(ctx=rdi, source=rsi, n=rdx) → rax = total
; invariance de découpage : le tampon de 64 o vit DANS le contexte (ah-04..07)
; 5 pushes (40 o) : pile 16-alignée aux points d'appel — pas de sous-cadre
push rbx
push r12
push r13
push r14
push r15
mov rbx, rdi
mov r12, rsi
mov r13, rdx
.boucle:
test r13, r13
je .fin
mov r14d, dword ptr [rbx + 96]
mov r15d, 64
sub r15d, r14d
cmp r13, r15
jb .court
; journal 20 : égalité stricte (n == espace restant) → chemin PLEIN : copier,
; remplissage=64, comprimer, reset — jbe laissait remplissage=64 SANS
; compression (violation Q1/Q2) : ah-07 recevait un tampon plein et
; déclenchait rep stosb avec ecx = -1 (segfault sur tout multiple de 64).
lea rdi, [rbx + r14 + 32]
mov rsi, r12
mov rcx, r15
rep movsb
add dword ptr [rbx + 96], r15d
add qword ptr [rbx + 104], r15
sub r13, r15
add r12, r15
mov rdi, rbx
call 0x1200
mov dword ptr [rbx + 96], 0
jmp .boucle
.court:
lea rdi, [rbx + r14 + 32]
mov rsi, r12
mov rcx, r13
rep movsb
add dword ptr [rbx + 96], r13d
add qword ptr [rbx + 104], r13
xor r13d, r13d
jmp .boucle
.fin:
mov rax, qword ptr [rbx + 104]
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
