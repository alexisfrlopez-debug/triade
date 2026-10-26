; tcp-02-accept · brouillon · (rcx = socket écoute) -> rax = cliente | -1 · tcp-02:R1 · c30002
sub rsp, 0x28
xor edx, edx
xor r8d, r8d
call qword ptr [rip + IAT_ACCEPT]
add rsp, 0x28
ret
