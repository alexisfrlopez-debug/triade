; http-04-chercher · bloc recherche d'en-tête · spec http-04:R1 · bloc carte e50004
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x4f40, taille 320 octets
; Dépendances : blocs http-01 @0x4C00, http-03 @0x4D80 ; comparaison insensible à la casse (unique du domaine)
; Notation explicite générée par outils/auteur.py depuis brouillons/http-04-chercher.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 252 o · padding : 68 o (NOP)
; Étiquettes résolues : .boucle=0x4f65, .cmp_nom=0x4fbb, .pas_min1=0x4fda, .pas_min2=0x4fea, .trouve=0x4ff5, .suivante=0x501c, .absent=0x5021, .invalide=0x5028, .fin=0x502d
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
mov r14, qword ptr [rsp + 0xA0]
xor r15d, r15d
mov rcx, rbx
mov rdx, rbp
mov r8, r15
call 0x4c00
test rax, rax
jne 0x5028
mov r15, r8
test rdx, rdx
je 0x5021
mov r10, r8
sub r10, rdx
sub r10, 2
lea rcx, [rbx + r10]
lea r8, [rsp + 0x20]
call 0x4e80
test rax, rax
jne 0x5028
mov rax, qword ptr [rsp + 0x20]
mov rdx, qword ptr [rsp + 0x28]
cmp rdx, r13
jne 0x501c
xor r11d, r11d
cmp r11, r13
jae 0x4ff5
movzx r9d, byte ptr [rax + r11]
movzx r10d, byte ptr [r12 + r11]
cmp r9, 0x61
jb 0x4fda
cmp r9, 0x7A
ja 0x4fda
sub r9, 0x20
cmp r10, 0x61
jb 0x4fea
cmp r10, 0x7A
ja 0x4fea
sub r10, 0x20
cmp r9, r10
jne 0x501c
add r11, 1
jmp 0x4fbb
mov rax, qword ptr [rsp + 0x20]
mov qword ptr [r14], rax
mov rax, qword ptr [rsp + 0x28]
mov qword ptr [r14 + 8], rax
mov rax, qword ptr [rsp + 0x30]
mov qword ptr [r14 + 16], rax
mov rax, qword ptr [rsp + 0x38]
mov qword ptr [r14 + 24], rax
xor eax, eax
jmp 0x502d
jmp 0x4f65
mov eax, 1
jmp 0x502d
mov eax, 2
add rsp, 0x48
pop r15
pop r14
pop r13
pop r12
pop rbp
pop rbx
ret
