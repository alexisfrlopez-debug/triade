; journal fichier : trace terrain D36 — lazy-init (chemin a cote de l'exe) + append
; modes : 0 = ligne ASCII, 1 = prefixe ASCII + valeur decimale, 2 = UTF-16 -> Latin-1
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x50
mov r12, rcx
mov r13, rdx
mov r14d, r8d
mov r15d, r9d
mov rbx, qword ptr [rip + JOURNAL_HANDLE]
test rbx, rbx
je .ouvrir
cmp rbx, -1
je .ouvrir
jmp .composer
.ouvrir:
xor ecx, ecx
lea rdx, [rip + BUF_CHEMIN]
mov r8d, 280
call qword ptr [rip + IAT_GMFA]
test eax, eax
je .echec_ouv
lea rcx, [rip + BUF_CHEMIN]
mov edx, eax
.balaye:
test rdx, rdx
je .pose_nom
dec rdx
cmp byte ptr [rcx + rdx], 0x5C
je .trouve
cmp byte ptr [rcx + rdx], 0x2F
je .trouve
jmp .balaye
.trouve:
inc rdx
.pose_nom:
lea rcx, [rip + BUF_CHEMIN]
add rcx, rdx
lea rdx, [rip + NOM_FICHIER]
mov r8d, 17
call MEMCPY
lea rcx, [rip + BUF_CHEMIN]
mov edx, 4
mov r8d, 1
xor r9d, r9d
mov dword ptr [rsp + 0x20], 2
mov dword ptr [rsp + 0x28], 0x80
mov qword ptr [rsp + 0x30], 0
call qword ptr [rip + IAT_CREATEFILE]
cmp rax, -1
je .echec_ouv
mov qword ptr [rip + JOURNAL_HANDLE], rax
mov rbx, rax
.composer:
lea rbx, [rip + BUF_CONV]
cmp r14d, 2
je .conv16
mov rcx, rbx
mov rdx, r12
mov r8, r13
call MEMCPY
cmp r14d, 1
jne .crlf
mov ecx, r15d
lea rdx, [rbx + r13]
call ITOA
mov rcx, rbx
call STRLEN
mov r13, rax
.crlf:
mov word ptr [rbx + r13], 0x0A0D
add r13, 2
.ecrire:
mov rcx, qword ptr [rip + JOURNAL_HANDLE]
mov rdx, rbx
mov r8, r13
lea r9, [rip + SCRATCH_ECRIT]
mov qword ptr [rsp + 0x20], 0
call qword ptr [rip + IAT_WF]
test eax, eax
je .echec_ecr
mov rcx, qword ptr [rip + JOURNAL_HANDLE]
call qword ptr [rip + IAT_FLUSH]
mov eax, 1
jmp .fin
.conv16:
xor ecx, ecx
xor edx, edx
.b16:
cmp rcx, r13
jae .fin16
movzx eax, word ptr [r12 + rcx*2]
cmp eax, 0x2192
jne .pas_fleche
mov al, 0x3E
jmp .pose16
.pas_fleche:
cmp eax, 0x100
jb .pose16
mov al, 0x2D
.pose16:
mov byte ptr [rbx + rdx], al
inc rcx
inc rdx
jmp .b16
.fin16:
mov r13, rdx
cmp r13, 2
jb .crlf
cmp byte ptr [rbx + r13 - 2], 0x0D
jne .crlf
cmp byte ptr [rbx + r13 - 1], 0x0A
je .ecrire
jmp .crlf
.echec_ouv:
mov rax, 0xFFFFFFFFFFFFFFFF
mov qword ptr [rip + JOURNAL_HANDLE], rax
xor eax, eax
jmp .fin
.echec_ecr:
mov rax, 0xFFFFFFFFFFFFFFFF
mov qword ptr [rip + JOURNAL_HANDLE], rax
xor eax, eax
.fin:
add rsp, 0x50
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
