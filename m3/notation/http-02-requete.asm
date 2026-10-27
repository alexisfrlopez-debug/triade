; http-02-requete · bloc ligne de requête · spec http-02:R1 · bloc carte e50002
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x4c80, taille 512 octets
; Dépendances : table des méthodes .rdata (8 entrées + terminateur) ; feuille
; Notation explicite générée par outils/auteur.py depuis brouillons/http-02-requete.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 457 o · padding : 55 o (NOP)
; Étiquettes résolues : .s1_boucle=0x4c9d, .s1_test=0x4ca7, .s1_trouve=0x4cb1, .s2_boucle=0x4cc3, .s2_test=0x4ccd, .s2_trouve=0x4cd7, .ver10=0x4d5d, .ver11=0x4d64, .methode=0x4d69, .mtab=0x4d70, .mcmp=0x4d8a, .msuiv=0x4da0, .mtrouve=0x4da6, .structure=0x4e25, .version_ko=0x4e2e, .cible_ko=0x4e37, .minconnu=0x4e40
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x4c86 + 0x7 - 0x245d = 0x2830
;   0x4d69 + 0x7 - 0x2960 = 0x2410
;   0x4da6 + 0x7 - 0x299d = 0x2410
push rbx
push r12
mov r11, r8
lea rax, [rip - 0x245d]
mov r12d, 0x2830
sub rax, r12
mov r12, rax
xor eax, eax
jmp 0x4ca7
cmp byte ptr [rcx + rax], 0x20
je 0x4cb1
add rax, 1
cmp rax, rdx
jb 0x4c9d
jmp 0x4e25
test rax, rax
je 0x4e25
mov r9, rax
lea rax, [r9 + 1]
jmp 0x4ccd
cmp byte ptr [rcx + rax], 0x20
je 0x4cd7
add rax, 1
cmp rax, rdx
jb 0x4cc3
jmp 0x4e25
mov r8, rax
shl rdx, 16
or r8, rdx
mov rax, r8
and eax, 0xFFFF
sub rax, r9
sub rax, 1
test rax, rax
je 0x4e37
cmp rax, 0x800
ja 0x4e37
mov r10, r8
and r10d, 0xFFFF
mov rax, r8
shr rax, 16
and eax, 0xFFFF
sub rax, r10
sub rax, 1
test rax, rax
je 0x4e25
cmp rax, 8
jne 0x4e2e
mov rax, qword ptr [rcx + r10 + 1]
movabs rdx, 0x302E312F50545448
cmp rax, rdx
je 0x4d5d
movabs rdx, 0x312E312F50545448
cmp rax, rdx
je 0x4d64
jmp 0x4e2e
bts r8, 32
jmp 0x4d69
bts r8, 33
lea rax, [rip - 0x2960]
mov rdx, qword ptr [rax + 8]
test rdx, rdx
je 0x4e40
cmp rdx, r9
jne 0x4da0
mov edx, dword ptr [rax]
add rdx, r12
mov r10, rcx
movzx ebx, byte ptr [rdx]
test bl, bl
je 0x4da6
cmp bl, byte ptr [r10]
jne 0x4da0
add rdx, 1
add r10, 1
jmp 0x4d8a
add rax, 16
jmp 0x4d70
lea rdx, [rip - 0x299d]
sub rax, rdx
shr rax, 4
add rax, 1
mov qword ptr [r11 + 8], rcx
mov qword ptr [r11 + 16], r9
lea rdx, [rcx + r9 + 1]
mov qword ptr [r11 + 24], rdx
mov rdx, r8
and edx, 0xFFFF
sub rdx, r9
sub rdx, 1
mov qword ptr [r11 + 32], rdx
mov rdx, r8
and edx, 0xFFFF
lea rdx, [rcx + rdx + 1]
mov qword ptr [r11 + 40], rdx
mov rdx, r8
shr rdx, 16
and edx, 0xFFFF
mov r10, r8
and r10d, 0xFFFF
sub rdx, r10
sub rdx, 1
mov qword ptr [r11 + 48], rdx
mov dword ptr [r11], eax
mov rdx, r8
shr rdx, 32
mov dword ptr [r11 + 4], edx
xor eax, eax
pop r12
pop rbx
ret
mov eax, 2
pop r12
pop rbx
ret
mov eax, 3
pop r12
pop rbx
ret
mov eax, 4
pop r12
pop rbx
ret
mov eax, 1
pop r12
pop rbx
ret
