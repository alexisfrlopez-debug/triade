; tcp-09-conn · brouillon · thread par connexion · (rcx socket cliente) · tcp-09:R1 · c30009
; boucle recv -> écho (bloc patchable 0x4600) -> send complet -> journal ; fin propre
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x460
mov rbx, rcx
.boucle:
mov rcx, rbx
lea rdx, [rsp + 0x30]
mov r8d, 1024
call TCP_RECV
test rax, rax
jle .fin
mov r12, rax
lea rcx, [rsp + 0x30]
lea rdx, [rsp + 0x30]
mov r8, r12
call ECHO
lea rcx, [rip + MSG_ECHO]
mov edx, 5
mov r8d, r12d
lea r9, [rip + MSG_CRLF]
mov qword ptr [rsp + 0x20], 2
call TCP_JOURNAL
xor r13, r13
.envoyer:
mov rcx, rbx
lea rdx, [rsp + 0x30]
add rdx, r13
mov r8, r12
sub r8, r13
call TCP_SEND
test rax, rax
jle .fin
add r13, rax
cmp r13, r12
jb .envoyer
jmp .boucle
.fin:
mov rcx, rbx
call TCP_CLOSE
lea rcx, [rip + MSG_FIN]
mov edx, 15
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call TCP_JOURNAL
add rsp, 0x460
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
