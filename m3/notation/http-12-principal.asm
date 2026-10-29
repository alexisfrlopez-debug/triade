; http-12-principal · bloc orchestration proxy (point d'entrée) · spec http-12:R1 · bloc carte e50012
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x1800, taille 1152 octets
; Dépendances : IAT kernel32 GSH, InitCS, CloseHandle, ExitProcess ; IAT ws2_32 WSACleanup ; blocs tcp-01/02/06/11, http-10, http-11, io-02 write ; table R10 + version .rdata ; état .data
; Notation explicite générée par outils/auteur.py depuis brouillons/http-12-principal.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 438 o · padding : 714 o (NOP)
; Étiquettes résolues : .verif=0x1825, .somme=0x183e, .entree_suivante=0x1855, .verif_ok=0x185b, .boucle=0x18ef, .accept_echec=0x1922, .erreur_reseau=0x192c, .arret=0x195a, .integrite_ko=0x198b
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x180d + 0x7 + 0x101c = 0x2830
;   0x181e + 0x7 + 0xe3b = 0x2660
;   0x185b + 0x7 + 0xfbe = 0x2820
;   0x1873 + 0x6 + 0x837 = 0x20b0
;   0x1879 + 0x7 + 0x1f80 = 0x3800
;   0x1885 + 0x6 + 0x825 = 0x20b0
;   0x188b + 0x7 + 0x1f76 = 0x3808
;   0x1892 + 0x7 + 0x1f97 = 0x3830
;   0x1899 + 0x6 + 0x839 = 0x20d8
;   0x189f + 0x7 + 0xf9a = 0x2840
;   0x18cc + 0x7 + 0x1f3d = 0x3810
;   0x18d3 + 0x7 + 0x44a6 = 0x5d80
;   0x18e9 + 0x6 + 0x809 = 0x20f8
;   0x18ef + 0x7 + 0x1f1a = 0x3810
;   0x1903 + 0x7 + 0x3c76 = 0x5580
;   0x191a + 0x6 + 0x7d8 = 0x20f8
;   0x1922 + 0x8 + 0x1eee = 0x3818
;   0x192c + 0x7 + 0xfbd = 0x28f0
;   0x1954 + 0x6 + 0x766 = 0x20c0
;   0x195a + 0x7 + 0xf5f = 0x28c0
;   0x197d + 0x6 + 0x9c5 = 0x2348
;   0x1985 + 0x6 + 0x735 = 0x20c0
;   0x1990 + 0x6 + 0x71a = 0x20b0
;   0x1999 + 0x7 + 0xf70 = 0x2910
;   0x19b0 + 0x6 + 0x70a = 0x20c0
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x60
lea rax, [rip + 0x101c]
mov r14, rax
sub r14, 0x2830
lea rbx, [rip + 0xe3b]
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
jne 0x198b
add rbx, 16
jmp 0x1825
mov rax, qword ptr [rip + 0xfbe]
cmp rax, 0x40000
jb 0x198b
mov ecx, -11
call qword ptr [rip + 0x837]
mov qword ptr [rip + 0x1f80], rax
mov ecx, -10
call qword ptr [rip + 0x825]
mov qword ptr [rip + 0x1f76], rax
lea rcx, [rip + 0x1f97]
call qword ptr [rip + 0x839]
lea rcx, [rip + 0xf9a]
mov edx, 40
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call 0x4b00
call 0x4000
test rax, rax
je 0x192c
mov qword ptr [rip + 0x1f3d], rax
lea rcx, [rip + 0x44a6]
xor edx, edx
call 0x4300
test rax, rax
je 0x192c
mov rcx, rax
call qword ptr [rip + 0x809]
mov rcx, qword ptr [rip + 0x1f1a]
call 0x4100
mov r12, rax
test rax, rax
js 0x1922
lea rcx, [rip + 0x3c76]
mov rdx, r12
call 0x4300
test rax, rax
je 0x192c
mov rcx, rax
call qword ptr [rip + 0x7d8]
jmp 0x18ef
cmp qword ptr [rip + 0x1eee], 0
jne 0x195a
lea rcx, [rip + 0xfbd]
mov edx, 22
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call 0x4b00
mov ecx, 2
call qword ptr [rip + 0x766]
lea rcx, [rip + 0xf5f]
mov edx, 7
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call 0x4b00
call qword ptr [rip + 0x9c5]
xor ecx, ecx
call qword ptr [rip + 0x735]
mov ecx, -11
call qword ptr [rip + 0x71a]
mov rcx, rax
lea rdx, [rip + 0xf70]
mov r8d, 33
call 0x1040
mov ecx, 1
call qword ptr [rip + 0x70a]
