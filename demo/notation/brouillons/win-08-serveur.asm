; thread serveur : tcp-01, publication R_LISTEN, boucle accept -> spawn tcp-09
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x30
call TCP_INIT
test rax, rax
je .echec
mov qword ptr [rip + LISTEN], rax
mov qword ptr [rip + DRAPEAU_SRV], 1
.boucle:
mov rcx, qword ptr [rip + LISTEN]
call TCP_ACCEPT
test rax, rax
js .fin
mov r12, rax
lea rcx, [rip + CONN]
mov rdx, r12
call TCP_SPAWN
test rax, rax
je .fin
mov rcx, rax
call qword ptr [rip + IAT_CH]
jmp .boucle
.echec:
mov qword ptr [rip + DRAPEAU_SRV], 2
lea rcx, [rip + J_SRV_KO]
mov edx, 37
call JOURNAL_GUI
xor eax, eax
.fin:
add rsp, 0x30
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
