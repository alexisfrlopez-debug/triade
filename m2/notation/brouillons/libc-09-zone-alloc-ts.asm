; libc-09-zone-alloc-ts · brouillon · allocateur par zone thread-safe · libc-09:R1 · c30012
; (rcx taille, rdx alignement) -> rax = ptr | 0 — EnterCS ; libc-05 ; LeaveCS
; (non embarqué dans echo.exe : vérifié par l'oracle sur image synthétique)
sub rsp, 0x28
mov r10, rcx
mov r11, rdx
lea rcx, [rip + CS]
call qword ptr [rip + IAT_ECS]
mov rcx, r10
mov rdx, r11
call ZONE_ALLOC
mov r10, rax
lea rcx, [rip + CS]
call qword ptr [rip + IAT_LCS]
mov rax, r10
add rsp, 0x28
ret
