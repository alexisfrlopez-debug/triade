; tcp-03-recv · brouillon · (rcx sock, rdx tampon, r8 cap) -> rax = n | 0 | -1 · tcp-03:R1 · c30003
sub rsp, 0x28
xor r9d, r9d
call qword ptr [rip + IAT_RECV]
add rsp, 0x28
ret
