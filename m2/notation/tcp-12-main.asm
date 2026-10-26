; tcp-12-main · bloc orchestration serveur (point d'entrée) · spec tcp-12:R1 · bloc carte c30013
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x1800, taille 2048 octets
; Dépendances : IAT kernel32 : GSH, InitCS, CloseHandle, ExitProcess ; blocs tcp-01/02/06/11, io-01 write, io-02 exit ; table R10 + version .rdata ; état .data
; Notation explicite générée par outils/auteur.py depuis brouillons/tcp-12-main.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 464 o · padding : 1584 o (NOP)
; Étiquettes résolues : .verif=0x1825, .somme=0x183a, .verif_ok=0x1857, .boucle=0x18ef, .accept_echec=0x1945, .erreur_reseau=0x194f, .arret=0x197c, .integrite_ko=0x19a6
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x180d + 0x7 + 0xdfc = 0x2610
;   0x181e + 0x7 + 0xc2b = 0x2450
;   0x1857 + 0x7 + 0xda2 = 0x2600
;   0x186f + 0x6 + 0x83b = 0x20b0
;   0x1875 + 0x7 + 0x1f84 = 0x3800
;   0x1881 + 0x6 + 0x829 = 0x20b0
;   0x1887 + 0x7 + 0x1f7a = 0x3808
;   0x188e + 0x7 + 0x1f9b = 0x3830
;   0x1895 + 0x6 + 0x83d = 0x20d8
;   0x189b + 0x7 + 0xd7e = 0x2620
;   0x18cc + 0x7 + 0x1f3d = 0x3810
;   0x18d3 + 0x7 + 0x30a6 = 0x4980
;   0x18e9 + 0x6 + 0x809 = 0x20f8
;   0x18ef + 0x7 + 0x1f1a = 0x3810
;   0x1903 + 0x7 + 0xd46 = 0x2650
;   0x1926 + 0x7 + 0x2ed3 = 0x4800
;   0x193d + 0x6 + 0x7b5 = 0x20f8
;   0x1945 + 0x8 + 0x1ecb = 0x3818
;   0x194f + 0x7 + 0xd9a = 0x26f0
;   0x197c + 0x7 + 0xd65 = 0x26e8
;   0x19ab + 0x6 + 0x6ff = 0x20b0
;   0x19b4 + 0x7 + 0xd4d = 0x2708
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x60
lea rax, [rip + 0xdfc]
mov r14, rax
sub r14, 0x2610
lea rbx, [rip + 0xc2b]
mov edx, dword ptr [rbx]
mov r13d, dword ptr [rbx + 4]
test r13d, r13d
je 0x1857
mov r12, r14
add r12, rdx
xor eax, eax
xor ecx, ecx
add rax, qword ptr [r12 + rcx]
add rcx, 8
cmp rcx, r13
jb 0x183a
cmp rax, qword ptr [rbx + 8]
jne 0x19a6
add rbx, 16
jmp 0x1825
mov rax, qword ptr [rip + 0xda2]
cmp rax, 0x30000
jb 0x19a6
mov ecx, -11
call qword ptr [rip + 0x83b]
mov qword ptr [rip + 0x1f84], rax
mov ecx, -10
call qword ptr [rip + 0x829]
mov qword ptr [rip + 0x1f7a], rax
lea rcx, [rip + 0x1f9b]
call qword ptr [rip + 0x83d]
lea rcx, [rip + 0xd7e]
mov edx, 47
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call 0x4b00
call 0x4000
test rax, rax
je 0x194f
mov qword ptr [rip + 0x1f3d], rax
lea rcx, [rip + 0x30a6]
xor edx, edx
call 0x4300
test rax, rax
je 0x194f
mov rcx, rax
call qword ptr [rip + 0x809]
mov rcx, qword ptr [rip + 0x1f1a]
call 0x4100
mov r12, rax
test rax, rax
js 0x1945
lea rcx, [rip + 0xd46]
mov edx, 19
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call 0x4b00
lea rcx, [rip + 0x2ed3]
mov rdx, r12
call 0x4300
test rax, rax
je 0x194f
mov rcx, rax
call qword ptr [rip + 0x7b5]
jmp 0x18ef
cmp qword ptr [rip + 0x1ecb], 0
jne 0x197c
lea rcx, [rip + 0xd9a]
mov edx, 21
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call 0x4b00
mov ecx, 2
call 0x1080
lea rcx, [rip + 0xd65]
mov edx, 6
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call 0x4b00
xor ecx, ecx
call 0x1080
mov ecx, -11
call qword ptr [rip + 0x6ff]
mov rcx, rax
lea rdx, [rip + 0xd4d]
mov r8d, 33
call 0x1040
mov ecx, 1
call 0x1080
