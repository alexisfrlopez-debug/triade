; tcp-12-main · bloc orchestration serveur (point d'entrée) · spec tcp-12:R1 · bloc carte c30013
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x1800, taille 2048 octets
; Dépendances : IAT kernel32 : GSH, InitCS, CloseHandle, ExitProcess ; blocs tcp-01/02/06/11, io-01 write, io-02 exit ; table R10 + version .rdata ; état .data
; Notation explicite générée par outils/auteur.py depuis brouillons/tcp-12-main.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 468 o · padding : 1580 o (NOP)
; Étiquettes résolues : .verif=0x1825, .somme=0x183e, .entree_suivante=0x1855, .verif_ok=0x185b, .boucle=0x18f3, .accept_echec=0x1949, .erreur_reseau=0x1953, .arret=0x1980, .integrite_ko=0x19aa
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x180d + 0x7 + 0xdfc = 0x2610
;   0x181e + 0x7 + 0xc2b = 0x2450
;   0x185b + 0x7 + 0xd9e = 0x2600
;   0x1873 + 0x6 + 0x837 = 0x20b0
;   0x1879 + 0x7 + 0x1f80 = 0x3800
;   0x1885 + 0x6 + 0x825 = 0x20b0
;   0x188b + 0x7 + 0x1f76 = 0x3808
;   0x1892 + 0x7 + 0x1f97 = 0x3830
;   0x1899 + 0x6 + 0x839 = 0x20d8
;   0x189f + 0x7 + 0xd7a = 0x2620
;   0x18d0 + 0x7 + 0x1f39 = 0x3810
;   0x18d7 + 0x7 + 0x30a2 = 0x4980
;   0x18ed + 0x6 + 0x805 = 0x20f8
;   0x18f3 + 0x7 + 0x1f16 = 0x3810
;   0x1907 + 0x7 + 0xd42 = 0x2650
;   0x192a + 0x7 + 0x2ecf = 0x4800
;   0x1941 + 0x6 + 0x7b1 = 0x20f8
;   0x1949 + 0x8 + 0x1ec7 = 0x3818
;   0x1953 + 0x7 + 0xd96 = 0x26f0
;   0x1980 + 0x7 + 0xd61 = 0x26e8
;   0x19af + 0x6 + 0x6fb = 0x20b0
;   0x19b8 + 0x7 + 0xd49 = 0x2708
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
test edx, edx
je 0x185b
mov r13d, dword ptr [rbx + 4]
test r13d, r13d
je 0x1855
mov r12, r14
add r12, rdx
xor eax, eax
xor ecx, ecx
add rax, qword ptr [r12 + rcx]
add rcx, 8
cmp rcx, r13
jb 0x183e
cmp rax, qword ptr [rbx + 8]
jne 0x19aa
add rbx, 16
jmp 0x1825
mov rax, qword ptr [rip + 0xd9e]
cmp rax, 0x30000
jb 0x19aa
mov ecx, -11
call qword ptr [rip + 0x837]
mov qword ptr [rip + 0x1f80], rax
mov ecx, -10
call qword ptr [rip + 0x825]
mov qword ptr [rip + 0x1f76], rax
lea rcx, [rip + 0x1f97]
call qword ptr [rip + 0x839]
lea rcx, [rip + 0xd7a]
mov edx, 47
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call 0x4b00
call 0x4000
test rax, rax
je 0x1953
mov qword ptr [rip + 0x1f39], rax
lea rcx, [rip + 0x30a2]
xor edx, edx
call 0x4300
test rax, rax
je 0x1953
mov rcx, rax
call qword ptr [rip + 0x805]
mov rcx, qword ptr [rip + 0x1f16]
call 0x4100
mov r12, rax
test rax, rax
js 0x1949
lea rcx, [rip + 0xd42]
mov edx, 20
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call 0x4b00
lea rcx, [rip + 0x2ecf]
mov rdx, r12
call 0x4300
test rax, rax
je 0x1953
mov rcx, rax
call qword ptr [rip + 0x7b1]
jmp 0x18f3
cmp qword ptr [rip + 0x1ec7], 0
jne 0x1980
lea rcx, [rip + 0xd96]
mov edx, 22
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call 0x4b00
mov ecx, 2
call 0x1080
lea rcx, [rip + 0xd61]
mov edx, 7
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call 0x4b00
xor ecx, ecx
call 0x1080
mov ecx, -11
call qword ptr [rip + 0x6fb]
mov rcx, rax
lea rdx, [rip + 0xd49]
mov r8d, 33
call 0x1040
mov ecx, 1
call 0x1080
