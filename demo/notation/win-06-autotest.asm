; win-06-autotest · bloc démo · spec win-06:R1 · bloc carte d40006
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x1940, taille 384 octets
; Dépendances : blocs libc-01/02/03/04 ; table R10 + version + ancre .rdata ; fixtures
; Notation explicite générée par outils/auteur.py depuis brouillons/win-06-autotest.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 322 o · padding : 62 o (NOP)
; Étiquettes résolues : .verif=0x1965, .somme=0x197c, .porte_ok=0x199a, .t_memcmp=0x19e5, .t_memcmp_neg=0x1a05, .t_strlen=0x1a26, .t_itoa=0x1a3b, .porte_ko=0x1a6a, .fin=0x1a71, .retour=0x1a74
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x194d + 0x7 + 0xccc = 0x2620
;   0x195e + 0x7 + 0xaeb = 0x2450
;   0x199a + 0x7 + 0xc6f = 0x2610
;   0x19b5 + 0x7 + 0xc74 = 0x2630
;   0x19cc + 0x7 + 0xc5d = 0x2630
;   0x19e5 + 0x7 + 0xc54 = 0x2640
;   0x19ec + 0x7 + 0xc51 = 0x2644
;   0x1a05 + 0x7 + 0xc34 = 0x2640
;   0x1a0c + 0x7 + 0xc35 = 0x2648
;   0x1a26 + 0x7 + 0xc1f = 0x264c
;   0x1a4f + 0x7 + 0xc04 = 0x265a
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x40
lea rax, [rip + 0xccc]
mov r14, rax
sub r14, 0x2620
lea r12, [rip + 0xaeb]
mov edx, dword ptr [r12]
test edx, edx
je 0x199a
mov r13d, dword ptr [r12 + 4]
mov rbx, r14
add rbx, rdx
xor eax, eax
xor ecx, ecx
add rax, qword ptr [rbx + rcx]
add rcx, 8
cmp rcx, r13
jb 0x197c
cmp rax, qword ptr [r12 + 8]
jne 0x1a6a
add r12, 0x10
jmp 0x1965
mov rax, qword ptr [rip + 0xc6f]
cmp rax, 0x30000
jb 0x1a6a
xor r15d, r15d
lea rcx, [rsp + 0x20]
lea rdx, [rip + 0xc74]
mov r8d, 16
call 0x1100
lea rcx, [rsp + 0x20]
lea rdx, [rip + 0xc5d]
mov r8d, 16
call 0x1180
test eax, eax
jne 0x19e5
inc r15d
lea rcx, [rip + 0xc54]
lea rdx, [rip + 0xc51]
mov r8d, 3
call 0x1180
test eax, eax
jne 0x1a05
inc r15d
lea rcx, [rip + 0xc34]
lea rdx, [rip + 0xc35]
mov r8d, 3
call 0x1180
cmp eax, -1
jne 0x1a26
inc r15d
lea rcx, [rip + 0xc1f]
call 0x1200
cmp rax, 13
jne 0x1a3b
inc r15d
mov ecx, 25000
lea rdx, [rsp + 0x30]
call 0x1280
lea rcx, [rsp + 0x30]
lea rdx, [rip + 0xc04]
mov r8d, 5
call 0x1180
test eax, eax
jne 0x1a71
inc r15d
jmp 0x1a71
mov eax, 0xFFFFFFFF
jmp 0x1a74
mov eax, r15d
add rsp, 0x40
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
