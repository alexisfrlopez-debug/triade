; ajout d'une ligne UTF-16 au journal (EDIT) : EM_SETSEL(-1,-1) + EM_REPLACESEL
push rbx
push r12
sub rsp, 0x28
mov rbx, rcx
mov r12, rdx
mov rcx, qword ptr [rip + HWND_JOURNAL]
mov edx, 0xB1
mov r8, 0xFFFFFFFFFFFFFFFF
mov r9, 0xFFFFFFFFFFFFFFFF
call qword ptr [rip + IAT_SENDMESSAGE]
mov rcx, qword ptr [rip + HWND_JOURNAL]
mov edx, 0xC2
mov r8d, 1
mov r9, rbx
call qword ptr [rip + IAT_SENDMESSAGE]
xor eax, eax
add rsp, 0x28
pop r12
pop rbx
ret
