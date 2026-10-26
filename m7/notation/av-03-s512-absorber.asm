; av-03-s512-absorber · bloc absorption tamponnée · spec av-03:R1 · bloc carte d50003
; Profil : x86-64-linux-elf64 · ABI SysV · slot RVA 0x1680, taille 256 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/av-03-s512-absorber.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 146 o · padding : 110 o (NOP)
; Étiquettes résolues : .boucle=0x1692, .court=0x16e1, .fin=0x1701
; Symboles (vérifiés par build_sceau.py contre layout.py) : @A_COMPRIMER=0x1200
push rbx
push r12
push r13
push r14
push r15
mov rbx, rdi
mov r12, rsi
mov r13, rdx
test r13, r13
je 0x1701
mov r14d, dword ptr [rbx + 0xc0]
mov r15d, 0x80
sub r15d, r14d
cmp r13, r15
jb 0x16e1
lea rdi, [rbx + r14 + 0x40]
mov rsi, r12
mov rcx, r15
rep movsb byte ptr [rdi], byte ptr [rsi]
add dword ptr [rbx + 0xc0], r15d
add qword ptr [rbx + 0xc8], r15
sub r13, r15
add r12, r15
mov rdi, rbx
call 0x1200
mov dword ptr [rbx + 0xc0], 0
jmp 0x1692
lea rdi, [rbx + r14 + 0x40]
mov rsi, r12
mov rcx, r13
rep movsb byte ptr [rdi], byte ptr [rsi]
add dword ptr [rbx + 0xc0], r13d
add qword ptr [rbx + 0xc8], r13
xor r13d, r13d
jmp 0x1692
mov rax, qword ptr [rbx + 0xc8]
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
