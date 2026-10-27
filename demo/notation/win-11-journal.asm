; win-11-journal · bloc démo · spec win-11:R1 · bloc carte d40011
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x1e00, taille 512 octets
; Dépendances : IAT kernel32#2 : GetModuleFileNameA, CreateFileA, WriteFile (commune), FlushFileBuffers, GetLastError ; blocs libc-01/03/04 ; état .data (handle, tampons) ; NOM_FICHIER .rdata
; Notation explicite générée par outils/auteur.py depuis brouillons/win-11-journal.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 468 o · padding : 44 o (NOP)
; Étiquettes résolues : .ouvrir=0x1e30, .balaye=0x1e56, .trouve=0x1e6c, .pose_nom=0x1e6f, .composer=0x1ed3, .crlf=0x1f0b, .ecrire=0x1f16, .conv16=0x1f51, .b16=0x1f55, .pas_fleche=0x1f6a, .pose16=0x1f73, .fin16=0x1f7e, .echec_ouv=0x1fa4, .echec_ecr=0x1fb6, .fin=0x1fc6
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x1e19 + 0x7 + 0x1a68 = 0x3888
;   0x1e32 + 0x7 + 0x1ad7 = 0x3910
;   0x1e3f + 0x6 + 0x103b = 0x2e80
;   0x1e4d + 0x7 + 0x1abc = 0x3910
;   0x1e6f + 0x7 + 0x1a9a = 0x3910
;   0x1e79 + 0x7 + 0x114c = 0x2fcc
;   0x1e8b + 0x7 + 0x1a7e = 0x3910
;   0x1eb9 + 0x6 + 0xfc9 = 0x2e88
;   0x1ec9 + 0x7 + 0x19b8 = 0x3888
;   0x1ed3 + 0x7 + 0x19b6 = 0x3890
;   0x1f16 + 0x7 + 0x196b = 0x3888
;   0x1f23 + 0x7 + 0x1b16 = 0x3a40
;   0x1f33 + 0x6 + 0x17f = 0x20b8
;   0x1f3d + 0x7 + 0x1944 = 0x3888
;   0x1f44 + 0x6 + 0xf46 = 0x2e90
;   0x1fab + 0x7 + 0x18d6 = 0x3888
;   0x1fbd + 0x7 + 0x18c4 = 0x3888
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
mov rbx, qword ptr [rip + 0x1a68]
test rbx, rbx
je 0x1e30
cmp rbx, -1
je 0x1e30
jmp 0x1ed3
xor ecx, ecx
lea rdx, [rip + 0x1ad7]
mov r8d, 280
call qword ptr [rip + 0x103b]
test eax, eax
je 0x1fa4
lea rcx, [rip + 0x1abc]
mov edx, eax
test rdx, rdx
je 0x1e6f
dec rdx
cmp byte ptr [rcx + rdx], 0x5C
je 0x1e6c
cmp byte ptr [rcx + rdx], 0x2F
je 0x1e6c
jmp 0x1e56
inc rdx
lea rcx, [rip + 0x1a9a]
add rcx, rdx
lea rdx, [rip + 0x114c]
mov r8d, 17
call 0x1100
lea rcx, [rip + 0x1a7e]
mov edx, 4
mov r8d, 1
xor r9d, r9d
mov dword ptr [rsp + 0x20], 2
mov dword ptr [rsp + 0x28], 0x80
mov qword ptr [rsp + 0x30], 0
call qword ptr [rip + 0xfc9]
cmp rax, -1
je 0x1fa4
mov qword ptr [rip + 0x19b8], rax
mov rbx, rax
lea rbx, [rip + 0x19b6]
cmp r14d, 2
je 0x1f51
mov rcx, rbx
mov rdx, r12
mov r8, r13
call 0x1100
cmp r14d, 1
jne 0x1f0b
mov ecx, r15d
lea rdx, [rbx + r13]
call 0x1280
mov rcx, rbx
call 0x1200
mov r13, rax
mov word ptr [rbx + r13], 0x0A0D
add r13, 2
mov rcx, qword ptr [rip + 0x196b]
mov rdx, rbx
mov r8, r13
lea r9, [rip + 0x1b16]
mov qword ptr [rsp + 0x20], 0
call qword ptr [rip + 0x17f]
test eax, eax
je 0x1fb6
mov rcx, qword ptr [rip + 0x1944]
call qword ptr [rip + 0xf46]
mov eax, 1
jmp 0x1fc6
xor ecx, ecx
xor edx, edx
cmp rcx, r13
jae 0x1f7e
movzx eax, word ptr [r12 + rcx*2]
cmp eax, 0x2192
jne 0x1f6a
mov al, 0x3E
jmp 0x1f73
cmp eax, 0x100
jb 0x1f73
mov al, 0x2D
mov byte ptr [rbx + rdx], al
inc rcx
inc rdx
jmp 0x1f55
mov r13, rdx
cmp r13, 2
jb 0x1f0b
cmp byte ptr [rbx + r13 - 2], 0x0D
jne 0x1f0b
cmp byte ptr [rbx + r13 - 1], 0x0A
je 0x1f16
jmp 0x1f0b
mov rax, 0xFFFFFFFFFFFFFFFF
mov qword ptr [rip + 0x18d6], rax
xor eax, eax
jmp 0x1fc6
mov rax, 0xFFFFFFFFFFFFFFFF
mov qword ptr [rip + 0x18c4], rax
xor eax, eax
add rsp, 0x50
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
