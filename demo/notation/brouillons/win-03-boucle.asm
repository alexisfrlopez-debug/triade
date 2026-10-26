; pompage des messages jusqu'a WM_QUIT (0) ou erreur (-1)
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x50
lea rbx, [rsp + 0x20]
.boucle:
mov rcx, rbx
xor edx, edx
xor r8d, r8d
xor r9d, r9d
call qword ptr [rip + IAT_GETMESSAGE]
test eax, eax
jle .fin
mov rcx, rbx
call qword ptr [rip + IAT_TRANSLATE]
mov rcx, rbx
call qword ptr [rip + IAT_DISPATCH]
jmp .boucle
.fin:
xor eax, eax
add rsp, 0x50
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
