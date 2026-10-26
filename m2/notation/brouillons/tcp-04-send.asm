; tcp-04-send · brouillon · (rcx sock, rdx tampon, r8 n) -> rax = k | -1 · tcp-04:R1 · c30004
sub rsp, 0x28
xor r9d, r9d
call qword ptr [rip + IAT_SEND]
add rsp, 0x28
ret
