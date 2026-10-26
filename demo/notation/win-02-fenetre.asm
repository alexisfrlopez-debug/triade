; win-02-fenetre · bloc démo · spec win-02:R2 · bloc carte d40002
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x1440, taille 384 octets
; Dépendances : IAT user32 : RegisterClassExW, CreateWindowExW, LoadCursorW, MessageBoxW ; IAT kernel32 : GetModuleHandleW, GetLastError ; bloc win-11 (trace) ; procédure @0x1640 ; chaînes UTF-16 + ASCII trace
; Notation explicite générée par outils/auteur.py depuis brouillons/win-02-fenetre.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 364 o · padding : 20 o (NOP)
; Étiquettes résolues : .echec=0x1560, .fin=0x159e
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x144d + 0x7 + 0x1a54 = 0x2ea8
;   0x1473 + 0x7 + 0x1c6 = 0x1640
;   0x1488 + 0x6 + 0xc72 = 0x2100
;   0x14a4 + 0x6 + 0x139e = 0x2848
;   0x14be + 0x7 + 0x14fb = 0x29c0
;   0x14d4 + 0x6 + 0x1326 = 0x2800
;   0x14e4 + 0x7 + 0x14d5 = 0x29c0
;   0x14eb + 0x7 + 0x14e6 = 0x29d8
;   0x1538 + 0x6 + 0x12ca = 0x2808
;   0x1543 + 0x7 + 0x2316 = 0x3860
;   0x154a + 0x7 + 0x197f = 0x2ed0
;   0x1560 + 0x6 + 0x1932 = 0x2e98
;   0x1569 + 0x7 + 0x197c = 0x2eec
;   0x1582 + 0x7 + 0x14cb = 0x2a54
;   0x1589 + 0x7 + 0x1448 = 0x29d8
;   0x1596 + 0x6 + 0x12cc = 0x2868
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x70
lea rcx, [rip + 0x1a54]
mov edx, 40
xor r8d, r8d
call 0x1e00
lea rbx, [rsp + 0x20]
mov dword ptr [rbx], 0x50
mov dword ptr [rbx + 4], 3
lea rax, [rip + 0x1c6]
mov qword ptr [rbx + 8], rax
mov qword ptr [rbx + 16], 0
xor ecx, ecx
call qword ptr [rip + 0xc72]
mov r12, rax
mov qword ptr [rbx + 24], r12
mov qword ptr [rbx + 32], 0
xor ecx, ecx
mov edx, 0x7F00
call qword ptr [rip + 0x139e]
mov qword ptr [rbx + 40], rax
mov qword ptr [rbx + 48], 16
mov qword ptr [rbx + 56], 0
lea rax, [rip + 0x14fb]
mov qword ptr [rbx + 64], rax
mov qword ptr [rbx + 72], 0
mov rcx, rbx
call qword ptr [rip + 0x1326]
test eax, eax
je 0x1560
xor ecx, ecx
lea rdx, [rip + 0x14d5]
lea r8, [rip + 0x14e6]
mov r9d, 0x10CF0000
mov dword ptr [rsp + 0x20], 0x80000000
mov dword ptr [rsp + 0x28], 0x80000000
mov dword ptr [rsp + 0x30], 780
mov dword ptr [rsp + 0x38], 560
mov qword ptr [rsp + 0x40], 0
mov qword ptr [rsp + 0x48], 0
mov qword ptr [rsp + 0x50], r12
mov qword ptr [rsp + 0x58], 0
call qword ptr [rip + 0x12ca]
test rax, rax
je 0x1560
mov qword ptr [rip + 0x2316], rax
lea rcx, [rip + 0x197f]
mov edx, 28
xor r8d, r8d
call 0x1e00
jmp 0x159e
call qword ptr [rip + 0x1932]
mov r9d, eax
lea rcx, [rip + 0x197c]
mov edx, 36
mov r8d, 1
call 0x1e00
xor ecx, ecx
lea rdx, [rip + 0x14cb]
lea r8, [rip + 0x1448]
mov r9d, 0x10
call qword ptr [rip + 0x12cc]
xor eax, eax
add rsp, 0x70
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
