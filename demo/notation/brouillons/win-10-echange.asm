; envoie la phrase (13 o), recoit 13 o, verifie contre l'attendu (memcmp scelle)
; D42 : sondes 4/5 — émission/réception complètes, instrumentation TEMPORAIRE
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x40
mov rbx, rcx
mov r12, rdx
xor r13d, r13d
.envoi:
mov rcx, rbx
lea rdx, [rip + PHRASE]
add rdx, r13
mov r8d, 14
sub r8d, r13d
call qword ptr [rip + IAT_SEND]
cmp rax, 0
jle .echec
add r13, rax
cmp r13, 14
jb .envoi
; D42 : sonde 4 — boucle d'emission complete (14 o partis), avant reception
lea rcx, [rip + SONDE_4]
mov edx, 16
xor r8d, r8d
call JOURNAL_TRACE
xor r13d, r13d
.recep:
mov rcx, rbx
lea rdx, [rsp + 0x20]
add rdx, r13
mov r8d, 14
sub r8d, r13d
call qword ptr [rip + IAT_RECV]
cmp rax, 0
jle .echec
add r13, rax
cmp r13, 14
jb .recep
; D42 : sonde 5 — boucle de reception complete (14 o recus), avant memcmp
; (rbx/r12/r13 survivent : win-05 preserve ; tampon [rsp+0x20] hors de portee)
lea rcx, [rip + SONDE_5]
mov edx, 14
xor r8d, r8d
call JOURNAL_TRACE
lea rcx, [rsp + 0x20]
mov rdx, r12
mov r8d, 14
call MEMCMP
test eax, eax
jne .echec
mov eax, 1
jmp .fin
.echec:
xor eax, eax
.fin:
add rsp, 0x40
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
