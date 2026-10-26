; win-06-autotest · bloc démo · spec win-06:R1 · bloc carte d40006
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x1ac0, taille 384 octets
; Dépendances : blocs libc-01/02/03/04 ; table R10 + version + ancre .rdata ; fixtures
; Notation explicite générée par outils/auteur.py depuis brouillons/win-06-autotest.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 322 o · padding : 62 o (NOP)
; Étiquettes résolues : .verif=0x1ae5, .somme=0x1afc, .porte_ok=0x1b1a, .t_memcmp=0x1b65, .t_memcmp_neg=0x1b85, .t_strlen=0x1ba6, .t_itoa=0x1bbb, .porte_ko=0x1bea, .fin=0x1bf1, .retour=0x1bf4
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x1acd + 0x7 + 0xb4c = 0x2620
;   0x1ade + 0x7 + 0x96b = 0x2450
;   0x1b1a + 0x7 + 0xb07 = 0x2628
;   0x1b35 + 0x7 + 0xaf4 = 0x2630
;   0x1b4c + 0x7 + 0xadd = 0x2630
;   0x1b65 + 0x7 + 0xad4 = 0x2640
;   0x1b6c + 0x7 + 0xad1 = 0x2644
;   0x1b85 + 0x7 + 0xab4 = 0x2640
;   0x1b8c + 0x7 + 0xab5 = 0x2648
;   0x1ba6 + 0x7 + 0xa9f = 0x264c
;   0x1bcf + 0x7 + 0xa84 = 0x265a
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x40
lea rax, [rip + 0xb4c]
mov r14, rax
sub r14, 0x2620
lea r12, [rip + 0x96b]
mov edx, dword ptr [r12]
test edx, edx
je 0x1b1a
mov r13d, dword ptr [r12 + 4]
mov rbx, r14
add rbx, rdx
xor eax, eax
xor ecx, ecx
add rax, qword ptr [rbx + rcx]
add rcx, 8
cmp rcx, r13
jb 0x1afc
cmp rax, qword ptr [r12 + 8]
jne 0x1bea
add r12, 0x10
jmp 0x1ae5
mov rax, qword ptr [rip + 0xb07]
cmp rax, 0x30000
jb 0x1bea
xor r15d, r15d
lea rcx, [rsp + 0x20]
lea rdx, [rip + 0xaf4]
mov r8d, 16
call 0x1100
lea rcx, [rsp + 0x20]
lea rdx, [rip + 0xadd]
mov r8d, 16
call 0x1180
test eax, eax
jne 0x1b65
inc r15d
lea rcx, [rip + 0xad4]
lea rdx, [rip + 0xad1]
mov r8d, 3
call 0x1180
test eax, eax
jne 0x1b85
inc r15d
lea rcx, [rip + 0xab4]
lea rdx, [rip + 0xab5]
mov r8d, 3
call 0x1180
cmp eax, -1
jne 0x1ba6
inc r15d
lea rcx, [rip + 0xa9f]
call 0x1200
cmp rax, 13
jne 0x1bbb
inc r15d
mov ecx, 25000
lea rdx, [rsp + 0x30]
call 0x1280
lea rcx, [rsp + 0x30]
lea rdx, [rip + 0xa84]
mov r8d, 5
call 0x1180
test eax, eax
jne 0x1bf1
inc r15d
jmp 0x1bf1
mov eax, 0xFFFFFFFF
jmp 0x1bf4
mov eax, r15d
add rsp, 0x40
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
