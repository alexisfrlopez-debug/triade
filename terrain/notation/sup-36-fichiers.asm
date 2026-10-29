; sup-36-fichiers · bloc terrain · spec sup-36:R1 · bloc carte f60036
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x4e00, taille 448 octets
; Dépendances : IAT kernel32#2 : CreateFileA ; IAT kernel32#1 : ReadFile, WriteFile, CloseHandle ; IAT kernel32#3 : DeleteFileA ; blocs libc-01/03 ; état .data (DIR_LONG, LU) ; BUF_CHEMIN/TAMPON_CMD
; Notation explicite générée par outils/auteur.py depuis brouillons/sup-36-fichiers.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 424 o · padding : 24 o (NOP)
; Étiquettes résolues : .balaye=0x4e39, .pose_dir=0x4e4a, .dir_pret=0x4e51, .lire=0x4ea4, .absent=0x4f1a, .ecrire=0x4f1e, .supprimer=0x4f8d, .fin=0x4f9a
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x4e19 + 0x8 - 0x12b9 = 0x3b68
;   0x4e23 + 0x7 - 0x151a = 0x3910
;   0x4e32 + 0x7 - 0x1529 = 0x3910
;   0x4e4a + 0x7 - 0x12e9 = 0x3b68
;   0x4e51 + 0x7 - 0x12f0 = 0x3b68
;   0x4e58 + 0x7 - 0x110f = 0x3d50
;   0x4e5f + 0x7 - 0x1556 = 0x3910
;   0x4e6e + 0x7 - 0x1125 = 0x3d50
;   0x4e75 + 0x7 - 0x1314 = 0x3b68
;   0x4ea4 + 0x7 - 0x115b = 0x3d50
;   0x4ed0 + 0x6 - 0x204e = 0x2e88
;   0x4ee2 + 0x7 - 0x1199 = 0x3d50
;   0x4eef + 0x7 - 0x139e = 0x3b58
;   0x4eff + 0x6 - 0x2e15 = 0x20f0
;   0x4f08 + 0x6 - 0x2e16 = 0x20f8
;   0x4f0e + 0x7 - 0x13bd = 0x3b58
;   0x4f1e + 0x7 - 0x11d5 = 0x3d50
;   0x4f4a + 0x6 - 0x20c8 = 0x2e88
;   0x4f5c + 0x7 - 0x1e63 = 0x3100
;   0x4f66 + 0x7 - 0x1415 = 0x3b58
;   0x4f76 + 0x6 - 0x2ec4 = 0x20b8
;   0x4f82 + 0x6 - 0x2e90 = 0x20f8
;   0x4f8d + 0x7 - 0x1244 = 0x3d50
;   0x4f94 + 0x6 - 0x2c6a = 0x2330
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x40
mov rbx, rcx
mov r12d, edx
mov r13, r8
mov r14d, r9d
cmp qword ptr [rip - 0x12b9], 0
jne 0x4e51
lea rcx, [rip - 0x151a]
call 0x1200
mov rcx, rax
lea rdx, [rip - 0x1529]
test rcx, rcx
je 0x4e4a
cmp byte ptr [rdx + rcx - 1], 0x5C
je 0x4e4a
dec rcx
jmp 0x4e39
mov qword ptr [rip - 0x12e9], rcx
mov r8, qword ptr [rip - 0x12f0]
lea rcx, [rip - 0x110f]
lea rdx, [rip - 0x1556]
call 0x1100
mov r8, r13
lea rcx, [rip - 0x1125]
add rcx, qword ptr [rip - 0x1314]
mov rdx, rbx
call 0x1100
test r12d, r12d
je 0x4ea4
cmp r12d, 1
je 0x4f1e
cmp r12d, 2
je 0x4f8d
xor eax, eax
jmp 0x4f9a
lea rcx, [rip - 0x115b]
mov edx, 0x80000000
xor r8d, r8d
xor r9d, r9d
mov dword ptr [rsp + 0x20], 3
mov qword ptr [rsp + 0x28], 0
mov qword ptr [rsp + 0x30], 0
call qword ptr [rip - 0x204e]
cmp rax, -1
je 0x4f1a
mov r15, rax
mov rcx, r15
lea rdx, [rip - 0x1199]
mov r8d, 640
lea r9, [rip - 0x139e]
mov qword ptr [rsp + 0x20], 0
call qword ptr [rip - 0x2e15]
mov rcx, r15
call qword ptr [rip - 0x2e16]
mov rax, qword ptr [rip - 0x13bd]
jmp 0x4f9a
xor eax, eax
jmp 0x4f9a
lea rcx, [rip - 0x11d5]
mov edx, 0x40000000
xor r8d, r8d
xor r9d, r9d
mov dword ptr [rsp + 0x20], 2
mov qword ptr [rsp + 0x28], 0
mov qword ptr [rsp + 0x30], 0
call qword ptr [rip - 0x20c8]
cmp rax, -1
je 0x4f1a
mov r15, rax
mov rcx, r15
lea rdx, [rip - 0x1e63]
mov r8, r14
lea r9, [rip - 0x1415]
mov qword ptr [rsp + 0x20], 0
call qword ptr [rip - 0x2ec4]
mov r13d, eax
mov rcx, r15
call qword ptr [rip - 0x2e90]
mov eax, r13d
jmp 0x4f9a
lea rcx, [rip - 0x1244]
call qword ptr [rip - 0x2c6a]
add rsp, 0x40
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
