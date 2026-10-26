; win-02-fenetre · bloc démo · spec win-02:R1 · bloc carte d40002
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x1440, taille 320 octets
; Dépendances : IAT user32 : RegisterClassExW, CreateWindowExW, LoadCursorW, MessageBoxW ; IAT kernel32 : GetModuleHandleW ; procédure @0x15E0 ; chaînes UTF-16
; Notation explicite générée par outils/auteur.py depuis brouillons/win-02-fenetre.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 288 o · padding : 32 o (NOP)
; Étiquettes résolues : .echec=0x1534, .fin=0x1552
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x145f + 0x7 + 0x19a = 0x1600
;   0x1474 + 0x6 + 0xc86 = 0x2100
;   0x1490 + 0x6 + 0x13b2 = 0x2848
;   0x14aa + 0x7 + 0x150f = 0x29c0
;   0x14c0 + 0x6 + 0x133a = 0x2800
;   0x14cc + 0x7 + 0x14ed = 0x29c0
;   0x14d3 + 0x7 + 0x14fe = 0x29d8
;   0x1520 + 0x6 + 0x12e2 = 0x2808
;   0x152b + 0x7 + 0x232e = 0x3860
;   0x1536 + 0x7 + 0x1517 = 0x2a54
;   0x153d + 0x7 + 0x1494 = 0x29d8
;   0x154a + 0x6 + 0x1318 = 0x2868
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x70
lea rbx, [rsp + 0x20]
mov dword ptr [rbx], 0x50
mov dword ptr [rbx + 4], 3
lea rax, [rip + 0x19a]
mov qword ptr [rbx + 8], rax
mov qword ptr [rbx + 16], 0
xor ecx, ecx
call qword ptr [rip + 0xc86]
mov r12, rax
mov qword ptr [rbx + 24], r12
mov qword ptr [rbx + 32], 0
xor ecx, ecx
mov edx, 0x7F00
call qword ptr [rip + 0x13b2]
mov qword ptr [rbx + 40], rax
mov qword ptr [rbx + 48], 16
mov qword ptr [rbx + 56], 0
lea rax, [rip + 0x150f]
mov qword ptr [rbx + 64], rax
mov qword ptr [rbx + 72], 0
mov rcx, rbx
call qword ptr [rip + 0x133a]
test eax, eax
je 0x1534
xor ecx, ecx
lea rdx, [rip + 0x14ed]
lea r8, [rip + 0x14fe]
mov r9d, 0x10CF0000
mov dword ptr [rsp + 0x20], 0x80000000
mov dword ptr [rsp + 0x28], 0x80000000
mov dword ptr [rsp + 0x30], 780
mov dword ptr [rsp + 0x38], 560
mov qword ptr [rsp + 0x40], 0
mov qword ptr [rsp + 0x48], 0
mov qword ptr [rsp + 0x50], r12
mov qword ptr [rsp + 0x58], 0
call qword ptr [rip + 0x12e2]
test rax, rax
je 0x1534
mov qword ptr [rip + 0x232e], rax
jmp 0x1552
xor ecx, ecx
lea rdx, [rip + 0x1517]
lea r8, [rip + 0x1494]
mov r9d, 0x10
call qword ptr [rip + 0x1318]
xor eax, eax
add rsp, 0x70
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
