; tcp-05-close · brouillon · (rcx socket) -> propagation du int ws2_32 · tcp-05:R1 · c30005
sub rsp, 0x28
call qword ptr [rip + IAT_CLOSESOCK]
add rsp, 0x28
ret
