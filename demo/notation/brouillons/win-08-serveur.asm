; thread serveur : tcp-01, publication R_LISTEN, boucle accept -> spawn tcp-09
; D42 : sondes S1/S2 autour d'accept/spawn — instrumentation TEMPORAIRE (R3)
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x30
call TCP_INIT
test rax, rax
je .echec
mov qword ptr [rip + LISTEN], rax
mov qword ptr [rip + DRAPEAU_SRV], 1
.boucle:
mov rcx, qword ptr [rip + LISTEN]
call TCP_ACCEPT
test rax, rax
js .fin
mov r12, rax
; D42 : sonde S1 — connexion acceptee (retour >= 0 verifie), avant le spawn
lea rcx, [rip + SONDE_S1]
mov edx, 12
xor r8d, r8d
call JOURNAL_TRACE
lea rcx, [rip + CONN]
mov rdx, r12
call TCP_SPAWN
test rax, rax
je .fin
mov r13, rax
; D42 : sonde S2 — fil d'echo lance (handle non nul verifie, sauve en r13
; car les volatils meurent a tout appel), avant CloseHandle + nouvel accept
lea rcx, [rip + SONDE_S2]
mov edx, 17
xor r8d, r8d
call JOURNAL_TRACE
mov rcx, r13
call qword ptr [rip + IAT_CH]
jmp .boucle
.echec:
mov qword ptr [rip + DRAPEAU_SRV], 2
lea rcx, [rip + J_SRV_KO]
mov edx, 37
call JOURNAL_GUI
xor eax, eax
.fin:
add rsp, 0x30
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
