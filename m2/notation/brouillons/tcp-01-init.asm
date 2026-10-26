; tcp-01-init · brouillon (étiquettes + symboles, résolu par outils/auteur.py)
; (rcx vide) -> rax = socket d'écoute | 0 · spec tcp-01:R1 · c30001
; sockaddr et WSADATA dans le cadre (pile privée, I3/Q4)
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x210
mov dword ptr [rsp + 0x20], 0xA8610002
mov dword ptr [rsp + 0x24], 0
mov qword ptr [rsp + 0x28], 0
mov ecx, 0x202
lea rdx, [rsp + 0x30]
call qword ptr [rip + IAT_WSASTARTUP]
test eax, eax
jne .echec
mov ecx, 2
mov edx, 1
mov r8d, 6
call qword ptr [rip + IAT_SOCKET]
cmp rax, -1
je .echec_wsa
mov rbx, rax
mov rcx, rbx
lea rdx, [rsp + 0x20]
mov r8d, 16
call qword ptr [rip + IAT_BIND]
test eax, eax
jne .echec_sock
mov rcx, rbx
mov edx, 8
call qword ptr [rip + IAT_LISTEN]
test eax, eax
jne .echec_sock
mov rax, rbx
jmp .fin
.echec_sock:
mov rcx, rbx
call qword ptr [rip + IAT_CLOSESOCK]
.echec_wsa:
call qword ptr [rip + IAT_WSACLEANUP]
.echec:
xor eax, eax
.fin:
add rsp, 0x210
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
