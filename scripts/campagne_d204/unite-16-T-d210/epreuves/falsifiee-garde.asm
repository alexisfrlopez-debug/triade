; falsifiee-garde · bloc la saisie : la garde non ré-armée (LE MUTANT de la falsification) · spec loupe-16:R1 · bloc carte i110016
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x6240, taille 704 octets
; Domaine : loupe (M10, le TGN « Loupe ») · Dépendances : LE MUTANT de la falsification V5 : la garde de loupe-18 non ré-armée à l'écriture — le scénario Alt+F4 échoue
; Notation explicite générée par outils/auteur.py depuis brouillons/falsifiee-garde.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 648 o · padding : 56 o (NOP, 0x90)
; Étiquettes résolues : .ouverte=0x627e, .caractere=0x62ab, .chiffres=0x62bb, .neuf=0x62e0, .valeur=0x62e3, .engager=0x62fe, .legitime=0x6347, .balaye=0x635b, .absente=0x636e, .remplace=0x638a, .saturee=0x6390, .apres=0x63a6, .avance=0x63dc, .lignes=0x63f4, .cap=0x63fe, .recadre=0x6416, .amorce=0x6424, .plancher=0x6441, .vmax=0x6443, .borne=0x644b, .visible=0x6467, .silence=0x647c, .echec=0x6480, .fin=0x648e, .message=0x649c, .copie=0x64a7, .pose=0x64b9
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x6250 + 0x7 + 0x7da9 = 0xe000
;   0x6257 + 0x7 + 0x81a2 = 0xe400
;   0x6268 + 0x7 - 0x3ed4 = 0x239b
;   0x6331 + 0x7 - 0x3fa9 = 0x238f
;   0x6347 + 0x7 + 0x8152 = 0xe4a0
;   0x6390 + 0x7 - 0x3e77 = 0x2520
;   0x63e3 + 0x7 + 0x9a06 = 0xfdf0
;   0x6472 + 0x6 - 0x32d8 = 0x31a0
;   0x649c + 0x7 + 0x7f5d = 0xe400
;   0x64b9 + 0x7 + 0x7f40 = 0xe400
; Appels directs (l'adresse du plan — I1) : call 0x649c, call 0x649c, call 0x649c, call 0x4240, call qword ptr [rip - 0x32d8]
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x20
mov r12, rcx
lea rbx, [rip + 0x7da9]
lea r13, [rip + 0x81a2]
cmp qword ptr [rbx + 528], -1
jne 0x627e
lea r10, [rip - 0x3ed4]
call 0x649c
push -4
pop rax
nop
nop
jmp 0x648e
mov r14, qword ptr [rbx + 544]
cmp r8d, 0x08
jne 0x62ab
cmp dword ptr [r13 + 4], 0
je 0x647c
mov dword ptr [r13 + 4], 0
mov dword ptr [r13 + 8], 0
jmp 0x647c
mov eax, r8d
cmp eax, 0x61
jb 0x62bb
cmp eax, 0x66
ja 0x62bb
sub eax, 0x20
cmp eax, 0x30
jb 0x647c
cmp eax, 0x39
jbe 0x62e0
cmp eax, 0x41
jb 0x647c
cmp eax, 0x46
ja 0x647c
sub eax, 0x37
jmp 0x62e3
sub eax, 0x30
mov r15d, eax
cmp dword ptr [r13 + 4], 0
jne 0x62fe
mov dword ptr [r13 + 4], 1
mov dword ptr [r13 + 8], r15d
jmp 0x647c
mov r10d, dword ptr [r13 + 8]
mov dword ptr [r13 + 4], 0
mov dword ptr [r13 + 8], 0
mov eax, r10d
shl eax, 4
or eax, r15d
movzx r15d, al
mov eax, dword ptr [rbx + 552]
add rax, qword ptr [rbx + 536]
cmp r14, rax
jb 0x6347
lea r10, [rip - 0x3fa9]
call 0x649c
push -3
pop rax
nop
nop
jmp 0x648e
lea rdx, [rip + 0x8152]
mov r10d, dword ptr [rdx + 4096]
xor r8d, r8d
mov r9, rdx
cmp r8d, r10d
jae 0x636e
cmp qword ptr [r9], r14
je 0x638a
add r9, 16
inc r8d
jmp 0x635b
cmp r10d, 256
jae 0x6390
mov qword ptr [r9], r14
mov byte ptr [r9 + 8], r15b
inc r10d
mov dword ptr [rdx + 4096], r10d
jmp 0x63a6
mov byte ptr [r9 + 8], r15b
jmp 0x63a6
lea r10, [rip - 0x3e77]
call 0x649c
push -3
pop rax
nop
nop
jmp 0x648e
mov rax, r14
sub rax, qword ptr [rbx + 536]
lea rdx, [rbx + 568]
mov byte ptr [rdx + rax], r15b
mov dword ptr [rbx + 556], 1
nop
nop
inc r14
mov rax, qword ptr [rbx + 520]
dec rax
cmp r14, rax
jb 0x63dc
mov r14, rax
mov qword ptr [rbx + 544], r14
lea rax, [rip + 0x9a06]
mov eax, dword ptr [rax + 8]
sub eax, 3
jns 0x63f4
xor eax, eax
cmp eax, 24
jbe 0x63fe
mov eax, 24
shl rax, 4
mov rdx, qword ptr [rbx + 536]
add rax, rdx
cmp r14, rdx
jb 0x6416
cmp r14, rax
jb 0x6467
mov rcx, r14
sub rcx, 176
jns 0x6424
xor ecx, ecx
and rcx, -16
mov rax, qword ptr [rbx + 520]
sub rax, 384
jbe 0x6441
add rax, 15
and rax, -16
jmp 0x6443
xor eax, eax
cmp rcx, rax
jbe 0x644b
mov rcx, rax
cmp rcx, qword ptr [rbx + 536]
je 0x6467
mov r15, rcx
call 0x4240
test eax, eax
jnz 0x6480
mov qword ptr [rbx + 536], r15
mov rcx, r12
xor edx, edx
mov r8d, 1
call qword ptr [rip - 0x32d8]
xor eax, eax
jmp 0x648e
xor eax, eax
jmp 0x648e
add rsp, 0x20
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
add rsp, 0x20
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
lea r11, [rip + 0x7f5d]
add r11, 12
mov al, byte ptr [r10]
mov byte ptr [r11], al
test al, al
jz 0x64b9
inc r10
inc r11
jmp 0x64a7
lea r11, [rip + 0x7f40]
mov dword ptr [r11], 3
ret
