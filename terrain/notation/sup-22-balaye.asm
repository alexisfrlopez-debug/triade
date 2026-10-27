; sup-22-balaye · bloc terrain · spec sup-22:R1 · bloc carte f60022
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x1d40, taille 192 octets
; Dépendances : blocs libc-02 memcmp, libc-01 memcpy — pur, aucun état .data
; Notation explicite générée par outils/auteur.py depuis brouillons/sup-22-balaye.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 175 o · padding : 17 o (NOP)
; Étiquettes résolues : .boucle=0x1d6b, .absent=0x1d88, .trouve=0x1d8c, .scan=0x1d95, .copie_prete=0x1da8, .plein=0x1dc0, .copie=0x1dc3, .fin=0x1dde
push rbx
push rbp
push r12
push r13
push r14
push r15
push r11
sub rsp, 0x10
mov rbx, rcx
mov r12, rdx
mov r13, r8
mov r14, r9
mov r15, qword ptr [rsp + 0x70]
mov rbp, qword ptr [rsp + 0x78]
cmp r12, r14
jb 0x1d88
mov rcx, rbx
mov rdx, r13
mov r8, r14
call 0x1180
test eax, eax
je 0x1d8c
inc rbx
dec r12
cmp r12, r14
jae 0x1d6b
xor eax, eax
jmp 0x1dde
add rbx, r14
sub r12, r14
xor r8d, r8d
cmp r8, r12
jae 0x1da8
mov al, byte ptr [rbx + r8]
cmp al, r15b
je 0x1da8
inc r8
jmp 0x1d95
mov rax, qword ptr [rsp + 0x80]
cmp r8, rax
jb 0x1dc0
dec rax
mov r8, rax
xor r12d, r12d
jmp 0x1dc3
mov r12, r8
mov qword ptr [rsp], r8
mov rcx, rbp
mov rdx, rbx
call 0x1100
mov rax, qword ptr [rsp]
mov byte ptr [rbp + rax], 0
mov rax, r12
add rsp, 0x10
pop r11
pop r15
pop r14
pop r13
pop r12
pop rbp
pop rbx
ret
