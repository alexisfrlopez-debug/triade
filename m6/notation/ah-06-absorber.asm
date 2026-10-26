; ah-06-absorber · bloc absorption tamponnée · spec ah-06:R1 · bloc carte d40006
; Profil : x86-64-linux-elf64 · ABI SysV · slot RVA 0x1400, taille 256 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/ah-06-absorber.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 125 o · padding : 131 o (NOP)
; Étiquettes résolues : .boucle=0x1412, .court=0x1455, .fin=0x146f
push rbx
push r12
push r13
push r14
push r15
mov rbx, rdi
mov r12, rsi
mov r13, rdx
test r13, r13
je 0x146f
mov r14d, dword ptr [rbx + 0x60]
mov r15d, 0x40
sub r15d, r14d
cmp r13, r15
jb 0x1455
lea rdi, [rbx + r14 + 0x20]
mov rsi, r12
mov rcx, r15
rep movsb byte ptr [rdi], byte ptr [rsi]
add dword ptr [rbx + 0x60], r15d
add qword ptr [rbx + 0x68], r15
sub r13, r15
add r12, r15
mov rdi, rbx
call 0x1200
mov dword ptr [rbx + 0x60], 0
jmp 0x1412
lea rdi, [rbx + r14 + 0x20]
mov rsi, r12
mov rcx, r13
rep movsb byte ptr [rdi], byte ptr [rsi]
add dword ptr [rbx + 0x60], r13d
add qword ptr [rbx + 0x68], r13
xor r13d, r13d
jmp 0x1412
mov rax, qword ptr [rbx + 0x68]
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
