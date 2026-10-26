; tcp-11-journal · brouillon · ligne de journal sérialisée · tcp-11:R1 · c30011
; (rcx préfixe, rdx lg, r8d valeur|0xFFFFFFFF, r9 suffixe, [pile] lg suffixe) -> BOOL
; composition dans le cadre privé (pile), émission sous section critique
push rbx
push r12
push r13
push r14
push r15
mov rbx, qword ptr [rsp + 0x50]
sub rsp, 0x80
mov r12, rcx
mov r13, rdx
mov r14, r8
mov r15, r9
lea rcx, [rip + CS]
call qword ptr [rip + IAT_ECS]
lea rcx, [rsp + 0x40]
mov rdx, r12
mov r8, r13
call MEMCPY
lea rax, [rsp + 0x40]
add rax, r13
cmp r14d, 0xFFFFFFFF
je .sans_champ
mov ecx, r14d
mov rdx, rax
call ITOA
mov rcx, rax
call STRLEN
add r13, rax
.sans_champ:
lea rax, [rsp + 0x40]
add rax, r13
mov rcx, rax
mov rdx, r15
mov r8, rbx
call MEMCPY
add r13, rbx
mov rcx, qword ptr [rip + STDOUT]
lea rdx, [rsp + 0x40]
mov r8, r13
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call WRITE
mov r12, rax
lea rcx, [rip + CS]
call qword ptr [rip + IAT_LCS]
mov rax, r12
add rsp, 0x80
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
