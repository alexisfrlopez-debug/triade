; envoie la phrase (13 o), recoit 13 o, verifie contre l'attendu (memcmp scelle)
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x40
mov rbx, rcx
mov r12, rdx
xor r13d, r13d
.envoi:
mov rcx, rbx
lea rdx, [rip + PHRASE]
add rdx, r13
mov r8d, 14
sub r8d, r13d
call qword ptr [rip + IAT_SEND]
cmp rax, 0
jle .echec
add r13, rax
cmp r13, 14
jb .envoi
xor r13d, r13d
.recep:
mov rcx, rbx
lea rdx, [rsp + 0x20]
add rdx, r13
mov r8d, 14
sub r8d, r13d
call qword ptr [rip + IAT_RECV]
cmp rax, 0
jle .echec
add r13, rax
cmp r13, 14
jb .recep
lea rcx, [rsp + 0x20]
mov rdx, r12
mov r8d, 14
call MEMCMP
test eax, eax
jne .echec
mov eax, 1
jmp .fin
.echec:
xor eax, eax
.fin:
add rsp, 0x40
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
