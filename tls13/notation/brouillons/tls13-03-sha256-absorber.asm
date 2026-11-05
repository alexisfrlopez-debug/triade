; tls13-03-sha256-absorber · brouillon étiqueté — spec tls13-03:R1, bloc carte h100003
; l'absorption tamponnée (l'invariance de découpage) — miroir win de ah-06
; (M6) : hacher(a puis b) == hacher(ab), le découpage de l'appelant n'est
; JAMAIS une entrée de la fonction. Le chemin PLEIN sur l'ÉGALITÉ STRICTE
; (journal 20 de la lignée : jbe laissait remplissage=64 sans compression).
; rcx = le contexte · rdx = les données · r8 = N (0 légal : ne fait rien)
; rax = 0 (Q4). DIVERGENCES NOMMÉES d'avec ah-06 : les arguments msx64, le
; verdict 0 en retour (ah-06 rendait le total), et l'appel DIRECT à TLS02 à
; l'adresse scellée du plan (I1) AVEC le tampon en second argument (P2 de
; tls13-02 : le bloc est un argument, jamais le tampon relu implicitement).
; 7 pushes (56 o) : entrée ≡ 8 → 8−56 ≡ 0 (mod 16) aux points d'appel ;
; sub rsp, 0x20 : L'OMBRE msx64 fournie à TLS02 (P3 de tls13-02).
push rbx
push r12
push r13
push r14
push r15
push rdi
push rsi
sub rsp, 0x20
mov rbx, rcx
mov r12, rdx
mov r13, r8
.boucle:
test r13, r13
je .fin
mov r14d, dword ptr [rbx + 96]
mov r15d, 64
sub r15d, r14d
cmp r13, r15
jb .court
lea rdi, [rbx + r14 + 32]
mov rsi, r12
mov rcx, r15
rep movsb
add dword ptr [rbx + 96], r15d
add qword ptr [rbx + 104], r15
sub r13, r15
add r12, r15
mov rcx, rbx
lea rdx, [rbx + 32]
call TLS02
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
xor eax, eax
add rsp, 0x20
pop rsi
pop rdi
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
