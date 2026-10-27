; le fil ouvrier : porte R10, libc, T1 (demo M2), T2 (proxy M3), T3 (envoi
; Drive), verdict final — chaque test est INDEPENDANT (un KO n'arrete pas
; les suivants : le constat veut TOUT le tableau) ; TOUTES les traces
; passent par win-05 scelle (entree trace, mode 0/1) ; l'ordre T1->T2->T3
; est un invariant (le port 25000 est partage, l'envoi vient en dernier)
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x20
; --- en-tete : banniere + date du run (TAMPON_AFF, 24 o, sup-21) ---
lea rcx, [rip + S00]
mov edx, LEN_S00
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
lea rcx, [rip + TAMPON_AFF]
mov edx, 24
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
; --- porte R10 + libc (win-06 scelle) : -1 = arret immediat, 4 = vert ---
call AUTOTEST
mov r15d, eax          ; le verdict survit aux traces (eax meurt a chaque appel)
cmp eax, 0xFFFFFFFF
jne .porte_ok
lea rcx, [rip + S02B]
mov edx, LEN_S02B
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
lea rcx, [rip + S91]
mov edx, LEN_S91
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
xor eax, eax
jmp .fin
.porte_ok:
lea rcx, [rip + S02A]
mov edx, LEN_S02A
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
cmp r15d, 4
je .libc_ok
lea rcx, [rip + S03B]
mov edx, LEN_S03B
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
lea rcx, [rip + S91]
mov edx, LEN_S91
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
xor eax, eax
jmp .fin
.libc_ok:
lea rcx, [rip + S03A]
mov edx, LEN_S03A
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
; --- T1, T2, T3 dans l'ordre (I1/I2) ---
call TEST_DEMO
mov r12d, eax
call TEST_PROXY
mov r13d, eax
call TEST_ENVOI
mov r14d, eax
; --- verdict final : les trois retours, jamais une impression ---
test r12d, r12d
je .echec
test r13d, r13d
je .echec
test r14d, r14d
je .echec
lea rcx, [rip + S90]
mov edx, LEN_S90
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
mov eax, 1
jmp .fin
.echec:
lea rcx, [rip + S91]
mov edx, LEN_S91
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
xor eax, eax
.fin:
add rsp, 0x20
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
