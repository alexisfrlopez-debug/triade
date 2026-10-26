; ajout d'une ligne au journal : ecran (EDIT) PUIS fichier (win-11 mode 2, Latin-1)
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
mov rcx, rbx
mov rdx, r12
mov r8d, 2
call JOURNAL_FICHIER
xor eax, eax
add rsp, 0x28
pop r12
pop rbx
ret
