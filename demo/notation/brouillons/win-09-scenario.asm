; LA demonstration en un clic : porte, libc, mecanique patch, serveur, client,
; boucle complete (patch en production, rollback), arret propre
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x60
xor ebx, ebx
mov ecx, -11
call qword ptr [rip + IAT_GSH]
mov qword ptr [rip + STDOUT], rax
mov ecx, -10
call qword ptr [rip + IAT_GSH]
mov qword ptr [rip + STDIN], rax
lea rcx, [rip + J_ENTETE]
mov edx, 27
call JOURNAL_GUI
lea rcx, [rip + J_PROTO]
mov edx, 29
call JOURNAL_GUI
call AUTOTEST
mov r12d, eax
cmp eax, 0xFFFFFFFF
jne .porte_ok
lea rcx, [rip + J_PORTE_KO]
mov edx, 24
call JOURNAL_GUI
jmp .fin
.porte_ok:
lea rcx, [rip + J_PORTE_OK]
mov edx, 29
call JOURNAL_GUI
cmp r12d, 4
je .libc_ok
lea rcx, [rip + J_LIBC_KO]
mov edx, 25
call JOURNAL_GUI
jmp .fin
.libc_ok:
lea rcx, [rip + J_LIBC_OK]
mov edx, 29
call JOURNAL_GUI
; D40 : sonde 1/3 — entrée de mécanique (avant le premier appel écho)
lea rcx, [rip + SONDE_1]
mov edx, 17
xor r8d, r8d
call JOURNAL_TRACE
lea rcx, [rsp + 0x30]
lea rdx, [rip + PHRASE]
mov r8d, 14
call ECHO
lea rcx, [rsp + 0x30]
lea rdx, [rip + PHRASE]
mov r8d, 14
call MEMCMP
test eax, eax
jne .defaut
xor ecx, ecx
call TCP_PATCH
test eax, eax
jne .defaut
; D40 : sonde 2/3 — tcp-07 pose complète (retour 0 vérifié), avant l'écho patché
lea rcx, [rip + SONDE_2]
mov edx, 17
xor r8d, r8d
call JOURNAL_TRACE
lea rcx, [rsp + 0x30]
lea rdx, [rip + PHRASE]
mov r8d, 14
call ECHO
lea rcx, [rsp + 0x30]
lea rdx, [rip + PHRASE_MAJ]
mov r8d, 14
call MEMCMP
test eax, eax
jne .defaut
; D40 : sonde 3/3 — écho patché v2 confirmé par memcmp, avant le rollback
lea rcx, [rip + SONDE_3]
mov edx, 12
xor r8d, r8d
call JOURNAL_TRACE
mov ecx, 1
call TCP_PATCH
test eax, eax
jne .defaut
lea rcx, [rsp + 0x30]
lea rdx, [rip + PHRASE]
mov r8d, 14
call ECHO
lea rcx, [rsp + 0x30]
lea rdx, [rip + PHRASE]
mov r8d, 14
call MEMCMP
test eax, eax
jne .defaut
lea rcx, [rip + J_MEC_OK]
mov edx, 32
call JOURNAL_GUI
lea rcx, [rip + SERVEUR]
xor edx, edx
call TCP_SPAWN
test rax, rax
je .defaut
mov rcx, rax
call qword ptr [rip + IAT_CH]
xor r12d, r12d
.attente:
mov eax, dword ptr [rip + DRAPEAU_SRV]
cmp eax, 1
je .srv_pret
cmp eax, 2
je .srv_ko
inc r12d
cmp r12d, 0x20000000
jb .attente
.srv_ko:
lea rcx, [rip + J_SRV_KO]
mov edx, 37
call JOURNAL_GUI
jmp .fin
.srv_pret:
lea rcx, [rip + J_SRV_OK]
mov edx, 34
call JOURNAL_GUI
call CLIENT
test rax, rax
je .reseau_ko
mov rbx, rax
lea rcx, [rip + J_CLI_OK]
mov edx, 19
call JOURNAL_GUI
mov rcx, rbx
lea rdx, [rip + PHRASE]
call ECHANGE
test eax, eax
je .reseau_ko
lea rcx, [rip + J_ECHO_OK]
mov edx, 34
call JOURNAL_GUI
xor ecx, ecx
call TCP_PATCH
test eax, eax
jne .defaut
mov rcx, rbx
lea rdx, [rip + PHRASE_MAJ]
call ECHANGE
test eax, eax
je .reseau_ko
lea rcx, [rip + J_PROD_OK]
mov edx, 34
call JOURNAL_GUI
mov ecx, 1
call TCP_PATCH
test eax, eax
jne .defaut
mov rcx, rbx
lea rdx, [rip + PHRASE]
call ECHANGE
test eax, eax
je .reseau_ko
lea rcx, [rip + J_RB_OK]
mov edx, 37
call JOURNAL_GUI
mov rcx, rbx
call TCP_CLOSE
xor ebx, ebx
mov qword ptr [rip + QUIT], 1
mov rcx, qword ptr [rip + LISTEN]
test rcx, rcx
je .arret_ok
call TCP_CLOSE
.arret_ok:
lea rcx, [rip + J_FINAL]
mov edx, 31
call JOURNAL_GUI
xor eax, eax
jmp .retour
.defaut:
lea rcx, [rip + J_DEF_KO]
mov edx, 32
call JOURNAL_GUI
jmp .fin
.reseau_ko:
lea rcx, [rip + J_RESEAU_KO]
mov edx, 27
call JOURNAL_GUI
.fin:
test rbx, rbx
je .net1
mov rcx, rbx
call TCP_CLOSE
xor ebx, ebx
.net1:
mov qword ptr [rip + QUIT], 1
mov rcx, qword ptr [rip + LISTEN]
test rcx, rcx
je .net2
call TCP_CLOSE
.net2:
xor eax, eax
.retour:
add rsp, 0x60
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
