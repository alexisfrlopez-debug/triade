; classe TRIADE + fenetre principale visible ; echec explique (MessageBoxW + trace fichier D36)
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x70
lea rcx, [rip + L00]
mov edx, LEN_L00
xor r8d, r8d
call JOURNAL_FICHIER
lea rbx, [rsp + 0x20]
mov dword ptr [rbx], 0x50
mov dword ptr [rbx + 4], 3
lea rax, [rip + PROCEDURE]
mov qword ptr [rbx + 8], rax
mov qword ptr [rbx + 16], 0
xor ecx, ecx
call qword ptr [rip + IAT_GMH]
mov r12, rax
mov qword ptr [rbx + 24], r12
mov qword ptr [rbx + 32], 0
xor ecx, ecx
mov edx, 0x7F00
call qword ptr [rip + IAT_LOADCURSOR]
mov qword ptr [rbx + 40], rax
mov qword ptr [rbx + 48], 16
mov qword ptr [rbx + 56], 0
lea rax, [rip + CLASSE]
mov qword ptr [rbx + 64], rax
mov qword ptr [rbx + 72], 0
mov rcx, rbx
call qword ptr [rip + IAT_REGISTERCLASSEX]
test eax, eax
je .echec
xor ecx, ecx
lea rdx, [rip + CLASSE]
lea r8, [rip + TITRE]
mov r9d, 0x10CF0000
mov dword ptr [rsp + 0x20], 0x80000000
mov dword ptr [rsp + 0x28], 0x80000000
mov dword ptr [rsp + 0x30], 780
mov dword ptr [rsp + 0x38], 560
mov qword ptr [rsp + 0x40], 0
mov qword ptr [rsp + 0x48], 0
mov qword ptr [rsp + 0x50], r12
mov qword ptr [rsp + 0x58], 0
call qword ptr [rip + IAT_CREATEWINDOW]
test rax, rax
je .echec
mov qword ptr [rip + HWND_PRINCIPAL], rax
lea rcx, [rip + L01]
mov edx, LEN_L01
xor r8d, r8d
call JOURNAL_FICHIER
jmp .fin
.echec:
call qword ptr [rip + IAT_GLE]
mov r9d, eax
lea rcx, [rip + LKO_GUI]
mov edx, LEN_LKO_GUI
mov r8d, 1
call JOURNAL_FICHIER
xor ecx, ecx
lea rdx, [rip + MSG_ECHEC_GUI]
lea r8, [rip + TITRE]
mov r9d, 0x10
call qword ptr [rip + IAT_MESSAGEBOX]
xor eax, eax
.fin:
add rsp, 0x70
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
