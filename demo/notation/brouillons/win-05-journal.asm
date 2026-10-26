; miroir universel : ecran (EDIT) PUIS fichier (win-11) — D37
; entree trace    0x5000 : (rcx=ascii, rdx=len, r8d=mode 0/1, r9d=valeur)
; entree scenario 0x5100 : (rcx=utf16 NUL-terminee, rdx=nchars) -> force mode 2
; mode 0/1 : conversion ASCII->UTF-16 dans BUF_MIROIR (+ itoa valeur si 1, CRLF+NUL)
; mode 2    : ptr utf16 tel quel
; envoi commun : EM_SETSEL(-1,-1) + EM_REPLACESEL(1, rbx=texte)
; relais fichier : jmp win-11(ptr originale, len originale, mode, valeur)
.principal:
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x30
mov rbx, rcx
mov r12, rdx
mov r13d, r8d
mov r14d, r9d
mov qword ptr [rsp + 0x20], rdx
mov qword ptr [rsp + 0x28], rcx
lea r15, [rip + BUF_MIROIR]
mov rax, qword ptr [rip + HWND_JOURNAL]
test rax, rax
je .fichier
cmp r13d, 2
je .mode2
xor ecx, ecx
.conv_txt:
cmp rcx, r12
jae .txt_fait
movzx edx, byte ptr [rbx + rcx]
mov word ptr [r15 + rcx*2], dx
inc ecx
jmp .conv_txt
.txt_fait:
mov r12, rcx
cmp r13d, 1
jne .crlf
mov ecx, r14d
lea rdx, [rip + BUF_CONV]
call ITOA
lea rdx, [rip + BUF_CONV]
.conv_val:
movzx eax, byte ptr [rdx]
test eax, eax
je .crlf
mov word ptr [r15 + r12*2], ax
inc rdx
inc r12
jmp .conv_val
.crlf:
mov dword ptr [r15 + r12*2], 0xA000D
mov word ptr [r15 + r12*2 + 4], 0
mov rbx, r15
jmp .envoi
.mode2:
.envoi:
mov rcx, qword ptr [rip + HWND_JOURNAL]
mov edx, 0xB1
mov r8, 0xFFFFFFFFFFFFFFFF
mov r9, 0xFFFFFFFFFFFFFFFF
call qword ptr [rip + IAT_SENDMESSAGE]
mov rcx, qword ptr [rip + HWND_JOURNAL]
mov edx, 0xC2
mov r8d, 1
mov r9, rbx
call qword ptr [rip + IAT_SENDMESSAGE]
.fichier:
mov rcx, qword ptr [rsp + 0x28]
mov rdx, qword ptr [rsp + 0x20]
mov r8d, r13d
mov r9d, r14d
add rsp, 0x30
pop r15
pop r14
pop r13
pop r12
pop rbx
jmp JOURNAL_FICHIER
nop
nop
nop
nop
nop
nop
nop
.scenario:
mov r8d, 2
jmp .principal
