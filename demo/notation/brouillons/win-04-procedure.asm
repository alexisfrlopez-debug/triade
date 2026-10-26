; procedure de fenetre : controles (fail-closed D36), taille RECT.right corrigee, clic unique
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x50
mov rbx, rcx
mov r12, rdx
mov r13, r8
mov r14, r9
cmp edx, 1
je .creer
cmp edx, 5
je .taille
cmp edx, 0x111
je .commande
cmp edx, 0x10
je .fermer
cmp edx, 2
je .detruire
jmp .defaut
.creer:
xor ecx, ecx
call qword ptr [rip + IAT_GMH]
mov r15, rax
xor ecx, ecx
lea rdx, [rip + CLASSE_EDIT]
lea r8, [rip + CHAINE_VIDE]
mov r9d, 0x50200844
mov dword ptr [rsp + 0x20], 8
mov dword ptr [rsp + 0x28], 8
mov dword ptr [rsp + 0x30], 716
mov dword ptr [rsp + 0x38], 380
mov qword ptr [rsp + 0x40], rbx
mov qword ptr [rsp + 0x48], 0
mov qword ptr [rsp + 0x50], r15
mov qword ptr [rsp + 0x58], 0
call qword ptr [rip + IAT_CREATEWINDOW]
mov qword ptr [rip + HWND_JOURNAL], rax
test rax, rax
jne .edit_ok
call qword ptr [rip + IAT_GLE]
mov r9d, eax
lea rcx, [rip + LKO_EDIT]
mov edx, LEN_LKO_EDIT
mov r8d, 1
call JOURNAL_TRACE
mov rax, 0xFFFFFFFFFFFFFFFF
jmp .sortie
.edit_ok:
xor ecx, ecx
lea rdx, [rip + CLASSE_BOUTON]
lea r8, [rip + TXT_BOUTON]
mov r9d, 0x50000001
mov dword ptr [rsp + 0x20], 8
mov dword ptr [rsp + 0x28], 396
mov dword ptr [rsp + 0x30], 716
mov dword ptr [rsp + 0x38], 36
mov qword ptr [rsp + 0x40], rbx
mov qword ptr [rsp + 0x48], 1
mov qword ptr [rsp + 0x50], r15
mov qword ptr [rsp + 0x58], 0
call qword ptr [rip + IAT_CREATEWINDOW]
mov qword ptr [rip + HWND_BOUTON], rax
test rax, rax
jne .bouton_ok
call qword ptr [rip + IAT_GLE]
mov r9d, eax
lea rcx, [rip + LKO_BOUTON]
mov edx, LEN_LKO_BOUTON
mov r8d, 1
call JOURNAL_TRACE
mov rax, 0xFFFFFFFFFFFFFFFF
jmp .sortie
.bouton_ok:
mov ecx, 17
call qword ptr [rip + IAT_GETSTOCK]
mov r12, rax
mov rcx, qword ptr [rip + HWND_JOURNAL]
mov edx, 0x30
mov r8, r12
mov r9d, 1
call qword ptr [rip + IAT_SENDMESSAGE]
mov rcx, qword ptr [rip + HWND_BOUTON]
mov edx, 0x30
mov r8, r12
mov r9d, 1
call qword ptr [rip + IAT_SENDMESSAGE]
lea rcx, [rip + L02]
mov edx, LEN_L02
xor r8d, r8d
call JOURNAL_TRACE
xor eax, eax
jmp .sortie
.taille:
mov rcx, rbx
lea rdx, [rsp + 0x20]
call qword ptr [rip + IAT_GETCLIENTRECT]
mov r10d, dword ptr [rsp + 0x28]
mov r11d, dword ptr [rsp + 0x2C]
mov rcx, qword ptr [rip + HWND_JOURNAL]
mov edx, 8
mov r8d, 8
mov r9d, r10d
sub r9d, 16
mov dword ptr [rsp + 0x20], r11d
sub dword ptr [rsp + 0x20], 56
mov dword ptr [rsp + 0x28], 1
call qword ptr [rip + IAT_MOVEWINDOW]
mov r12d, eax
mov rcx, qword ptr [rip + HWND_BOUTON]
mov edx, 8
mov r8d, r11d
sub r8d, 44
mov r9d, r10d
sub r9d, 16
mov dword ptr [rsp + 0x20], 36
mov dword ptr [rsp + 0x28], 1
call qword ptr [rip + IAT_MOVEWINDOW]
mov r13d, eax
lea rcx, [rip + L4C]
mov edx, LEN_L4C
mov r8d, 1
mov r9d, r12d
call JOURNAL_TRACE
lea rcx, [rip + L4D]
mov edx, LEN_L4D
mov r8d, 1
mov r9d, r13d
call JOURNAL_TRACE
xor eax, eax
jmp .sortie
.commande:
cmp r13d, 1
jne .zero
cmp qword ptr [rip + DRAPEAU_WORKER], 0
jne .zero
mov qword ptr [rip + DRAPEAU_WORKER], 1
lea rcx, [rip + L03]
mov edx, LEN_L03
xor r8d, r8d
call JOURNAL_TRACE
mov rcx, qword ptr [rip + HWND_BOUTON]
xor edx, edx
call qword ptr [rip + IAT_ENABLEWINDOW]
lea rcx, [rip + SCENARIO]
xor edx, edx
call TCP_SPAWN
test rax, rax
jne .thread_ok
call qword ptr [rip + IAT_GLE]
mov r9d, eax
lea rcx, [rip + LKO_SPAWN]
mov edx, LEN_LKO_SPAWN
mov r8d, 1
call JOURNAL_TRACE
mov qword ptr [rip + DRAPEAU_WORKER], 0
mov rcx, qword ptr [rip + HWND_BOUTON]
mov edx, 1
call qword ptr [rip + IAT_ENABLEWINDOW]
jmp .zero
.thread_ok:
mov rcx, rax
call qword ptr [rip + IAT_CH]
.zero:
xor eax, eax
jmp .sortie
.fermer:
mov rcx, rbx
call qword ptr [rip + IAT_DESTROYWINDOW]
xor eax, eax
jmp .sortie
.detruire:
xor ecx, ecx
call qword ptr [rip + IAT_POSTQUIT]
xor eax, eax
jmp .sortie
.defaut:
mov rcx, rbx
mov rdx, r12
mov r8, r13
mov r9, r14
call qword ptr [rip + IAT_DEFWNDPROC]
.sortie:
add rsp, 0x50
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
