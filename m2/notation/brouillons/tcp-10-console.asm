; tcp-10-console · brouillon · thread console · () · tcp-10:R1 · c30010
; lit stdin : patch / rollback / quit ; inconnu -> journal ; fin de flux -> retour
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x70
.boucle:
mov rcx, qword ptr [rip + STDIN]
lea rdx, [rsp + 0x30]
mov r8d, 64
lea r9, [rsp + 0x28]
mov qword ptr [rsp + 0x20], 0
call qword ptr [rip + IAT_READFILE]
test eax, eax
je .sortie
mov r12, qword ptr [rsp + 0x28]
cmp r12, 7
jne .pas_patch
lea rcx, [rsp + 0x30]
lea rdx, [rip + CMD_PATCH]
mov r8d, 7
call MEMCMP
test eax, eax
jne .pas_patch
xor ecx, ecx
call TCP_PATCH
test eax, eax
jne .refus
lea rcx, [rip + MSG_PATCH_OK]
mov edx, 29
jmp .journal_statique
.refus:
lea rcx, [rip + MSG_REFUS]
mov edx, 18
.journal_statique:
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call TCP_JOURNAL
jmp .boucle
.pas_patch:
cmp r12, 10
jne .pas_rollback
lea rcx, [rsp + 0x30]
lea rdx, [rip + CMD_RB]
mov r8d, 10
call MEMCMP
test eax, eax
jne .pas_rollback
mov ecx, 1
call TCP_PATCH
test eax, eax
jne .refus
lea rcx, [rip + MSG_RB_OK]
mov edx, 27
jmp .journal_statique
.pas_rollback:
cmp r12, 6
jne .inconnue
lea rcx, [rsp + 0x30]
lea rdx, [rip + CMD_QUIT]
mov r8d, 6
call MEMCMP
test eax, eax
jne .inconnue
mov qword ptr [rip + QUIT], 1
mov rcx, qword ptr [rip + LISTEN]
call TCP_CLOSE
jmp .sortie
.inconnue:
lea rcx, [rip + MSG_INCONNU]
mov edx, 19
jmp .journal_statique
.sortie:
add rsp, 0x70
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
