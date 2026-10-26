; tcp-06-spawn · brouillon · (rcx proc, rdx arg) -> rax = handle | 0 · tcp-06:R1 · c30006
sub rsp, 0x38
mov r8, rcx
mov r9, rdx
xor ecx, ecx
xor edx, edx
mov qword ptr [rsp + 0x20], 0
mov qword ptr [rsp + 0x28], 0
call qword ptr [rip + IAT_CREATETHREAD]
add rsp, 0x38
ret
