; tls-04-poignee · bloc poignée de main cliente (boucle ISC) · spec tls-04:R1 · bloc carte g70004
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x62c0, taille 768 octets
; Dépendances : boucle ISC bornée 16 allers ; IAT secur32 InitializeSecurityContextW ; tls-01/02/03
; Notation explicite générée par outils/auteur.py depuis brouillons/tls-04-poignee.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 544 o · padding : 224 o (NOP)
; Étiquettes résolues : .boucle=0x62e3, .premier=0x633a, .sans_entree=0x6358, .continuer=0x63d4, .incomplet=0x63f3, .recevoir=0x6402, .etabli=0x643a, .emettre=0x6450, .boucle_envoi=0x6459, .emis=0x6491, .succes=0x649e, .interminable=0x64b4, .hors_borne=0x64bb, .emission_rompue=0x64c2, .reception_rompue=0x64c9, .echec_nomme=0x64d0, .echec=0x64d0
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x63aa + 0x6 - 0x39a0 = 0x2a10
sub rsp, 0xB8
mov qword ptr [rsp + 0x60], rcx
mov word ptr [rcx + 0x38], 0
mov qword ptr [rsp + 0x68], 0
mov dword ptr [rsp + 0x58], 0
mov rax, [rsp + 0x60]
movzx ecx, word ptr [rax + 0x38]
cmp ecx, 16
jae 0x64b4
inc word ptr [rax + 0x38]
xor ecx, ecx
lea rdx, [rax + 0x260]
mov r8d, 16384
lea r9, [rsp + 0x90]
call 0x6180
cmp qword ptr [rsp + 0x68], 0
je 0x633a
mov rax, [rsp + 0x60]
xor ecx, ecx
lea rdx, [rax + 0x4260]
mov r8, [rsp + 0x68]
lea r9, [rsp + 0x70]
call 0x6180
mov rax, [rsp + 0x60]
mov rcx, rax
xor edx, edx
xor r11d, r11d
cmp qword ptr [rsp + 0x68], 0
jz 0x6358
lea rdx, [rax + 0x10]
lea r11, [rsp + 0x70]
mov [rsp + 0x30], r11
mov r8, [rax + 0x28]
mov r9d, 0xC01C
mov qword ptr [rsp + 0x20], 0
mov qword ptr [rsp + 0x28], 0
mov qword ptr [rsp + 0x38], 0
lea rax, [rax + 0x10]
mov [rsp + 0x40], rax
lea rax, [rsp + 0x90]
mov [rsp + 0x48], rax
lea rax, [rsp + 0x58]
mov [rsp + 0x50], rax
mov dword ptr [rsp + 0x58], 0
call qword ptr [rip - 0x39a0]
movsxd rcx, eax
call 0x6080
mov r10, [rsp + 0x60]
mov dword ptr [r10 + 0x34], edx
test eax, eax
jz 0x643a
cmp eax, 1
je 0x63d4
cmp eax, 2
je 0x63f3
jmp 0x64d0
mov qword ptr [rsp + 0x68], 0
mov qword ptr [rsp + 0x28], 0
mov eax, [rsp + 0xA0]
test eax, eax
jnz 0x6450
jmp 0x6402
cmp qword ptr [rsp + 0x68], 16384
jae 0x64bb
mov rdx, [rsp + 0x60]
mov rcx, [rdx + 0x20]
lea rdx, [rdx + 0x4260]
add rdx, [rsp + 0x68]
mov r8d, 16384
sub r8, [rsp + 0x68]
call 0x4140
test rax, rax
jle 0x64c9
add qword ptr [rsp + 0x68], rax
jmp 0x62e3
mov qword ptr [rsp + 0x28], 1
mov eax, [rsp + 0xA0]
test eax, eax
jnz 0x6450
jmp 0x649e
mov qword ptr [rsp + 0x20], 0
mov eax, [rsp + 0xA0]
mov r8, [rsp + 0x20]
sub rax, r8
jz 0x6491
mov rdx, [rsp + 0x60]
mov rcx, [rdx + 0x20]
lea rdx, [rdx + 0x260]
add rdx, r8
mov r8, rax
call 0x4180
test rax, rax
jle 0x64c2
add qword ptr [rsp + 0x20], rax
jmp 0x6459
cmp qword ptr [rsp + 0x28], 0
jne 0x649e
jmp 0x6402
mov rax, [rsp + 0x60]
mov dword ptr [rax + 0x30], 0
xor eax, eax
add rsp, 0xB8
ret
mov eax, 5
jmp 0x64d0
mov eax, 5
jmp 0x64d0
mov eax, 5
jmp 0x64d0
mov eax, 5
jmp 0x64d0
mov rdx, [rsp + 0x60]
mov [rdx + 0x30], eax
add rsp, 0xB8
ret
