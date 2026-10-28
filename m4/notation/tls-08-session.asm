; tls-08-session · bloc session TLS cliente (orchestration) · spec tls-08:R1 · bloc carte g70008
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x6d40, taille 1536 octets
; Dépendances : orchestration TLS cliente ; tls-01..07, tcp-13, tcp-03/04/05 ; compensation intégrale constatée par comptage
; Notation explicite générée par outils/auteur.py depuis brouillons/tls-08-session.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 740 o · padding : 796 o (NOP)
; Étiquettes résolues : .relais=0x6e3a, .chambre=0x6e53, .recevoir=0x6e67, .decrypter=0x6ea3, .span=0x6edf, .envoi=0x6ef6, .apres_pompe=0x6f43, .cible=0x6f5a, .zone_pleine=0x6f64, .succes=0x6f6e, .echec=0x6f78, .poignee_echec=0x6f7e, .compensation=0x6fac, .pas_contexte=0x6fd8, .pas_credentials=0x7003, .fin=0x7018
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x6de5 + 0x7 - 0x418c = 0x2c60
;   0x6f87 + 0x7 - 0x430e = 0x2c80
sub rsp, 0xE8
mov qword ptr [rsp + 0x60], rcx
mov qword ptr [rsp + 0x68], rdx
mov qword ptr [rcx + 0x20], 0
mov qword ptr [rcx], 0
mov qword ptr [rcx + 0x10], 0
mov r11, [rsp + 0x68]
mov rcx, [r11]
mov rdx, [r11 + 0x08]
movzx r8d, word ptr [r11 + 0x10]
call 0x4400
test rax, rax
jz 0x6f5a
mov r10, [rsp + 0x60]
mov [r10 + 0x20], rax
mov r11, [rsp + 0x68]
mov rcx, [r11]
mov rdx, [r11 + 0x08]
mov r10, [rsp + 0x60]
lea r8, [r10 + 0x60]
call 0x6000
test eax, eax
jnz 0x6f5a
mov r10, [rsp + 0x60]
lea rax, [r10 + 0x60]
mov [r10 + 0x28], rax
xor ecx, ecx
mov rdx, [rsp + 0x60]
call 0x65c0
test eax, eax
jnz 0x6f78
mov rcx, [rsp + 0x60]
call 0x62c0
test eax, eax
jnz 0x6f7e
lea rcx, [rip - 0x418c]
mov edx, 23
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call 0x4b00
mov r11, [rsp + 0x68]
mov rcx, [rsp + 0x60]
mov rdx, [r11 + 0x18]
mov r8, [r11 + 0x20]
call 0x6740
test eax, eax
jnz 0x6f78
mov r10, [rsp + 0x60]
mov word ptr [r10 + 0x3A], 0
mov word ptr [r10 + 0x3C], 0
mov r10, [rsp + 0x60]
movzx eax, word ptr [r10 + 0x3A]
test eax, eax
jnz 0x6e53
mov word ptr [r10 + 0x3C], 0
xor eax, eax
jmp 0x6e67
movzx ecx, word ptr [r10 + 0x3C]
add rax, rcx
cmp rax, 0x8000
jae 0x6f64
mov r10, [rsp + 0x60]
mov rcx, [r10 + 0x20]
lea rdx, [r10 + 0x4260]
add rdx, rax
mov r8, 0x8000
sub r8, rax
call 0x4140
test rax, rax
jle 0x6f6e
mov r10, [rsp + 0x60]
movzx ecx, word ptr [r10 + 0x3A]
add ecx, eax
mov word ptr [r10 + 0x3A], cx
mov r10, [rsp + 0x60]
mov rcx, r10
lea rdx, [r10 + 0x4260]
movzx r8d, word ptr [r10 + 0x3A]
lea r9, [rsp + 0x80]
call 0x6a40
test eax, eax
jz 0x6edf
cmp eax, 4
je 0x6f6e
cmp eax, 2
je 0x6e3a
jmp 0x6f78
mov qword ptr [rsp + 0x90], 0
cmp qword ptr [rsp + 0x88], 0
je 0x6f43
mov r11, [rsp + 0x68]
mov rcx, [r11 + 0x28]
mov rdx, [rsp + 0x80]
add rdx, [rsp + 0x90]
mov r8, [rsp + 0x88]
sub r8, [rsp + 0x90]
call 0x4180
test rax, rax
jle 0x6f6e
add qword ptr [rsp + 0x90], rax
mov rax, [rsp + 0x90]
cmp rax, [rsp + 0x88]
jb 0x6ef6
mov r10, [rsp + 0x60]
movzx eax, word ptr [r10 + 0x3A]
test eax, eax
jnz 0x6ea3
jmp 0x6e3a
mov dword ptr [rsp + 0x58], 7
jmp 0x6fac
mov dword ptr [rsp + 0x58], 5
jmp 0x6fac
mov dword ptr [rsp + 0x58], 0
jmp 0x6fac
mov [rsp + 0x58], eax
jmp 0x6fac
mov [rsp + 0x58], eax
cmp eax, 3
jne 0x6fac
lea rcx, [rip - 0x430e]
mov edx, 19
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call 0x4b00
jmp 0x6fac
mov r10, [rsp + 0x60]
cmp qword ptr [r10 + 0x10], 0
je 0x6fd8
mov ecx, 1
mov rdx, r10
call 0x65c0
test eax, eax
jz 0x6fd8
mov ecx, 1
mov rdx, [rsp + 0x60]
call 0x65c0
mov r10, [rsp + 0x60]
cmp qword ptr [r10], 0
je 0x7003
mov ecx, 2
mov rdx, r10
call 0x65c0
test eax, eax
jz 0x7003
mov ecx, 2
mov rdx, [rsp + 0x60]
call 0x65c0
mov r10, [rsp + 0x60]
cmp qword ptr [r10 + 0x20], 0
je 0x7018
mov rcx, [r10 + 0x20]
call 0x41c0
mov eax, [rsp + 0x58]
add rsp, 0xE8
ret
