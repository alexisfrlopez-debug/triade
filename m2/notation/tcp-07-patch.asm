; tcp-07-patch · bloc moteur de patch à chaud · spec tcp-07:R1 · bloc carte c30007
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x4400, taille 512 octets
; Dépendances : IAT kernel32 : VirtualProtect ; bloc libc-01 memcpy @0x1100 ; données : echo @0x4600, croissance @0x4680, staging, table, état .data
; Notation explicite générée par outils/auteur.py depuis brouillons/tcp-07-patch.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 389 o · padding : 123 o (NOP)
; Étiquettes résolues : .somme=0x4451, .protection_tardive=0x44eb, .rollback=0x44f5, .protger=0x4531, .mode_invalide=0x4556, .rien=0x455d, .integrite=0x4564, .incoherent=0x456b, .protection=0x4572, .fin=0x4577
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x4416 + 0x7 - 0xbfd = 0x3820
;   0x441d + 0x7 + 0x1dc = 0x4600
;   0x4436 + 0x7 - 0x1fe9 = 0x2454
;   0x4446 + 0x7 - 0x207d = 0x23d0
;   0x445e + 0x7 - 0x200d = 0x2458
;   0x4484 + 0x7 - 0xc63 = 0x3828
;   0x448b + 0x7 + 0x1ee = 0x4680
;   0x4492 + 0x7 - 0x20c9 = 0x23d0
;   0x44a1 + 0x7 + 0x1d8 = 0x4680
;   0x44d5 + 0xb - 0xcc0 = 0x3820
;   0x4509 + 0x7 - 0xce8 = 0x3828
;   0x451e + 0xb - 0xd09 = 0x3820
;   0x454b + 0x6 - 0x2481 = 0x20d0
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x40
cmp ecx, 1
ja 0x4556
mov rax, qword ptr [rip - 0xbfd]
lea r15, [rip + 0x1dc]
test ecx, ecx
jne 0x44f5
cmp rax, 1
je 0x456b
mov r12d, dword ptr [rip - 0x1fe9]
test r12d, r12d
je 0x455d
lea rbx, [rip - 0x207d]
xor eax, eax
xor ecx, ecx
add rax, qword ptr [rbx + rcx]
add rcx, 8
cmp rcx, r12
jb 0x4451
mov r13, qword ptr [rip - 0x200d]
cmp rax, r13
jne 0x4564
mov r8d, 4
call 0x4531
test eax, eax
je 0x4572
mov rax, qword ptr [r15]
mov qword ptr [rip - 0xc63], rax
lea rcx, [rip + 0x1ee]
lea rdx, [rip - 0x20c9]
mov r8, r12
call 0x1100
lea rax, [rip + 0x1d8]
sub rax, r15
sub rax, 5
mov r11d, 0x909090
shl r11, 40
shl rax, 8
or r11, rax
or r11, 0xE9
mov qword ptr [r15], r11
mov r8d, 0x20
call 0x4531
mov qword ptr [rip - 0xcc0], 1
test eax, eax
je 0x44eb
xor eax, eax
jmp 0x4577
mov eax, 5
jmp 0x4577
test rax, rax
je 0x456b
mov r8d, 4
call 0x4531
test eax, eax
je 0x4572
mov rdx, qword ptr [rip - 0xce8]
mov qword ptr [r15], rdx
mov r8d, 0x20
call 0x4531
mov qword ptr [rip - 0xd09], 0
test eax, eax
je 0x44eb
xor eax, eax
jmp 0x4577
sub rsp, 8
mov rcx, r15
and rcx, 0xfffffffffffff000
mov rdx, 0x700
lea r9, [rsp + 0x38]
call qword ptr [rip - 0x2481]
add rsp, 8
ret
mov eax, 1
jmp 0x4577
mov eax, 2
jmp 0x4577
mov eax, 3
jmp 0x4577
mov eax, 4
jmp 0x4577
mov eax, 5
add rsp, 0x40
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
