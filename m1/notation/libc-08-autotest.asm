; libc-08-autotest · bloc auto-test de la mini-libc (point d'entrée) · spec libc-08:R1 · bloc carte b20008
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x1800, taille 2048 octets
; Dépendances : blocs libc-01…07, io-01 write @0x1040, io-02 exit @0x1080, IAT[0] GetStdHandle
; Notation explicite générée par outils/auteur.py depuis brouillons/libc-08-autotest.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 977 o · padding : 1071 o (NOP)
; Étiquettes résolues : .v1ko=0x1840, .v2ko=0x185b, .v3ko=0x1877, .v4ko=0x188e, .v5ko=0x18ae, .v6ko=0x18cf, .v7ko=0x18f0, .v8ko=0x1910, .v9ko=0x1953, .v10ko=0x19a8, .v11ko=0x19eb, .v12ko=0x19ff, .v13ko=0x1a14, .v14ko=0x1a29, .v15ko=0x1a53, .v16ko=0x1a80, .v17ko=0x1aad, .v18ko=0x1ada, .ko=0x1b93, .verdict=0x1b9a, .ko_sortie=0x1bc7, .fin=0x1bcc
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x1815 + 0x6 + 0x895 = 0x20b0
;   0x188e + 0x7 + 0x76b = 0x2000
;   0x1895 + 0x7 + 0x76c = 0x2008
;   0x18ae + 0x7 + 0x74b = 0x2000
;   0x18b5 + 0x7 + 0x754 = 0x2010
;   0x18cf + 0x7 + 0x73a = 0x2010
;   0x18d6 + 0x7 + 0x723 = 0x2000
;   0x18f0 + 0x7 + 0x721 = 0x2018
;   0x18f7 + 0x7 + 0x702 = 0x2000
;   0x1925 + 0x7 + 0x7b4 = 0x20e0
;   0x193a + 0x7 + 0x79f = 0x20e0
;   0x1968 + 0x7 + 0x781 = 0x20f0
;   0x197d + 0x7 + 0x75c = 0x20e0
;   0x198f + 0x7 + 0x75a = 0x20f0
;   0x19bd + 0x7 + 0x73c = 0x2100
;   0x19d2 + 0x7 + 0x727 = 0x2100
;   0x19eb + 0x7 + 0x776 = 0x2168
;   0x19ff + 0x7 + 0x76a = 0x2170
;   0x1a14 + 0x7 + 0x75d = 0x2178
;   0x1a3a + 0x7 + 0x75f = 0x21a0
;   0x1a67 + 0x7 + 0x73a = 0x21a8
;   0x1a94 + 0x7 + 0x71d = 0x21b8
;   0x1ac1 + 0x7 + 0x700 = 0x21c8
;   0x1af5 + 0x7 + 0x6d4 = 0x21d0
;   0x1b3d + 0x7 + 0x6ac = 0x21f0
;   0x1b8a + 0x7 + 0x667 = 0x21f8
;   0x1b93 + 0x7 + 0x666 = 0x2200
sub rsp, 0x40
push rbx
push r12
push r13
push r14
push r15
xor r15, r15
mov ecx, -11
call qword ptr [rip + 0x895]
mov r13, rax
mov ecx, 16
mov edx, 8
call 0x1300
test rax, rax
je 0x1840
mov r14, rax
test rax, 7
jne 0x1840
inc r15
mov ecx, 16
mov edx, 8
call 0x1300
sub rax, r14
cmp rax, 16
jb 0x185b
inc r15
call 0x1380
mov ecx, 16
mov edx, 8
call 0x1300
cmp rax, r14
jne 0x1877
inc r15
mov ecx, 0x7D0
mov edx, 8
call 0x1300
test rax, rax
jne 0x188e
inc r15
lea rcx, [rip + 0x76b]
lea rdx, [rip + 0x76c]
mov r8d, 6
call 0x1180
test eax, eax
jne 0x18ae
inc r15
lea rcx, [rip + 0x74b]
lea rdx, [rip + 0x754]
mov r8d, 6
call 0x1180
cmp eax, -1
jne 0x18cf
inc r15
lea rcx, [rip + 0x73a]
lea rdx, [rip + 0x723]
mov r8d, 6
call 0x1180
cmp eax, 1
jne 0x18f0
inc r15
lea rcx, [rip + 0x721]
lea rdx, [rip + 0x702]
mov r8d, 3
call 0x1180
test eax, eax
jne 0x1910
inc r15
mov ecx, 16
mov edx, 8
call 0x1300
mov r14, rax
mov rcx, r14
lea rdx, [rip + 0x7b4]
mov r8d, 16
call 0x1100
mov rcx, r14
lea rdx, [rip + 0x79f]
mov r8d, 16
call 0x1180
test eax, eax
jne 0x1953
inc r15
mov ecx, 16
mov edx, 8
call 0x1300
mov r14, rax
mov rcx, r14
lea rdx, [rip + 0x781]
mov r8d, 16
call 0x1100
mov rcx, r14
lea rdx, [rip + 0x75c]
xor r8d, r8d
call 0x1100
mov rcx, r14
lea rdx, [rip + 0x75a]
mov r8d, 16
call 0x1180
test eax, eax
jne 0x19a8
inc r15
mov ecx, 48
mov edx, 8
call 0x1300
mov r14, rax
mov rcx, r14
lea rdx, [rip + 0x73c]
mov r8d, 33
call 0x1100
mov rcx, r14
lea rdx, [rip + 0x727]
mov r8d, 33
call 0x1180
test eax, eax
jne 0x19eb
inc r15
lea rcx, [rip + 0x776]
call 0x1200
test rax, rax
jne 0x19ff
inc r15
lea rcx, [rip + 0x76a]
call 0x1200
cmp rax, 6
jne 0x1a14
inc r15
lea rcx, [rip + 0x75d]
call 0x1200
cmp rax, 33
jne 0x1a29
inc r15
xor ecx, ecx
lea rdx, [rsp + 0x30]
call 0x1280
lea rcx, [rsp + 0x30]
lea rdx, [rip + 0x75f]
mov r8d, 2
call 0x1180
test eax, eax
jne 0x1a53
inc r15
mov ecx, 0xFFFFFFFF
lea rdx, [rsp + 0x30]
call 0x1280
lea rcx, [rsp + 0x30]
lea rdx, [rip + 0x73a]
mov r8d, 11
call 0x1180
test eax, eax
jne 0x1a80
inc r15
mov ecx, 1234567890
lea rdx, [rsp + 0x30]
call 0x1280
lea rcx, [rsp + 0x30]
lea rdx, [rip + 0x71d]
mov r8d, 11
call 0x1180
test eax, eax
jne 0x1aad
inc r15
mov ecx, 7
lea rdx, [rsp + 0x30]
call 0x1280
lea rcx, [rsp + 0x30]
lea rdx, [rip + 0x700]
mov r8d, 2
call 0x1180
test eax, eax
jne 0x1ada
inc r15
mov ecx, 64
mov edx, 8
call 0x1300
mov rbx, rax
mov r12d, 21
mov rcx, rbx
lea rdx, [rip + 0x6d4]
mov r8d, 21
call 0x1100
mov ecx, r15d
lea rdx, [rsp + 0x30]
call 0x1280
lea rcx, [rsp + 0x30]
call 0x1200
mov r14, rax
mov rcx, rbx
add rcx, r12
lea rdx, [rsp + 0x30]
mov r8, r14
call 0x1100
add r12, r14
mov rcx, rbx
add rcx, r12
lea rdx, [rip + 0x6ac]
mov r8d, 1
call 0x1100
inc r12
mov ecx, 18
lea rdx, [rsp + 0x30]
call 0x1280
lea rcx, [rsp + 0x30]
call 0x1200
mov r14, rax
mov rcx, rbx
add rcx, r12
lea rdx, [rsp + 0x30]
mov r8, r14
call 0x1100
add r12, r14
cmp r15, 18
jne 0x1b93
lea rdx, [rip + 0x667]
jmp 0x1b9a
lea rdx, [rip + 0x666]
mov rcx, rbx
add rcx, r12
mov r8d, 5
call 0x1100
add r12, 5
mov rcx, r13
mov rdx, rbx
mov r8, r12
call 0x1040
cmp r15, 18
jne 0x1bc7
xor ecx, ecx
jmp 0x1bcc
mov ecx, 1
call 0x1080
