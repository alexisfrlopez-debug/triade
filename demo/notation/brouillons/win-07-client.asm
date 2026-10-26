; socket + connect 127.0.0.1:25000 (sockaddr sur pile, octets du plan)
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x40
mov dword ptr [rsp + 0x20], 0xA8610002
mov dword ptr [rsp + 0x24], 0x0100007F
mov qword ptr [rsp + 0x28], 0
mov ecx, 2
mov edx, 1
mov r8d, 6
call qword ptr [rip + IAT_SOCKET]
cmp rax, -1
je .echec
mov rbx, rax
mov rcx, rbx
lea rdx, [rsp + 0x20]
mov r8d, 16
call qword ptr [rip + IAT_CONNECT]
test eax, eax
jne .echec_close
mov rax, rbx
jmp .fin
.echec_close:
mov rcx, rbx
call qword ptr [rip + IAT_CLOSESOCK]
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
