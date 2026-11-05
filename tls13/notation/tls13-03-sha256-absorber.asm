; tls13-03-sha256-absorber · bloc absorption tamponnée (invariance de découpage) · spec tls13-03:R1 · bloc carte h100003
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0xc240, taille 192 octets
; Domaine : tls13 (M9, l'ère 1.0.0) · Dépendances : tls13-02 (la compression au geste même, à l'adresse scellée — I1) ; le tampon passé en second argument
; Notation explicite générée par outils/auteur.py depuis brouillons/tls13-03-sha256-absorber.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 139 o · padding : 53 o (NOP, 0x90)
; Étiquettes résolues : .boucle=0xc258, .court=0xc29f, .fin=0xc2b9
; Appels directs (l'adresse scellée du plan — I1) : call 0xc080
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
test r13, r13
je 0xc2b9
mov r14d, dword ptr [rbx + 96]
mov r15d, 64
sub r15d, r14d
cmp r13, r15
jb 0xc29f
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
call 0xc080
mov dword ptr [rbx + 96], 0
jmp 0xc258
lea rdi, [rbx + r14 + 32]
mov rsi, r12
mov rcx, r13
rep movsb
add dword ptr [rbx + 96], r13d
add qword ptr [rbx + 104], r13
xor r13d, r13d
jmp 0xc258
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
