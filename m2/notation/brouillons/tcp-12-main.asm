; tcp-12-main · brouillon · orchestration serveur — point d'entrée echo.exe · tcp-12:R1 · c30013
; porte R10 (sommes + version) AVANT tout effet réseau, puis init, bannière,
; boucle d'acceptation (thread par connexion), sorties 0/1/2 par ExitProcess
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x60
lea rax, [rip + ANCRE]
mov r14, rax
sub r14, 0x2610
lea rbx, [rip + TAB_SUM]
.verif:
mov edx, dword ptr [rbx]
mov r13d, dword ptr [rbx + 4]
test r13d, r13d
je .verif_ok
mov r12, r14
add r12, rdx
xor eax, eax
xor ecx, ecx
.somme:
add rax, qword ptr [r12 + rcx]
add rcx, 8
cmp rcx, r13
jb .somme
cmp rax, qword ptr [rbx + 8]
jne .integrite_ko
add rbx, 16
jmp .verif
.verif_ok:
mov rax, qword ptr [rip + VERSION]
cmp rax, 0x30000
jb .integrite_ko
mov ecx, -11
call qword ptr [rip + IAT_GSH]
mov qword ptr [rip + STDOUT], rax
mov ecx, -10
call qword ptr [rip + IAT_GSH]
mov qword ptr [rip + STDIN], rax
lea rcx, [rip + CS]
call qword ptr [rip + IAT_ICS]
lea rcx, [rip + MSG_BANNIERE]
mov edx, 47
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call TCP_JOURNAL
call TCP_INIT
test rax, rax
je .erreur_reseau
mov qword ptr [rip + LISTEN], rax
lea rcx, [rip + CONSOLE]
xor edx, edx
call TCP_SPAWN
test rax, rax
je .erreur_reseau
mov rcx, rax
call qword ptr [rip + IAT_CH]
.boucle:
mov rcx, qword ptr [rip + LISTEN]
call TCP_ACCEPT
mov r12, rax
test rax, rax
js .accept_echec
lea rcx, [rip + MSG_CONNEXION]
mov edx, 19
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call TCP_JOURNAL
lea rcx, [rip + CONN]
mov rdx, r12
call TCP_SPAWN
test rax, rax
je .erreur_reseau
mov rcx, rax
call qword ptr [rip + IAT_CH]
jmp .boucle
.accept_echec:
cmp qword ptr [rip + QUIT], 0
jne .arret
.erreur_reseau:
lea rcx, [rip + MSG_ERREUR]
mov edx, 21
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call TCP_JOURNAL
mov ecx, 2
call EXIT
.arret:
lea rcx, [rip + MSG_ARRET]
mov edx, 6
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call TCP_JOURNAL
xor ecx, ecx
call EXIT
.integrite_ko:
mov ecx, -11
call qword ptr [rip + IAT_GSH]
mov rcx, rax
lea rdx, [rip + MSG_KO]
mov r8d, 33
call WRITE
mov ecx, 1
call EXIT
