; sys-02-resolveur · bloc résolveur SSN (l'EAT de ntdll lue, le motif vérifié) · spec sys-02:R1 · bloc carte g90002
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0xa040, taille 320 octets
; Dépendances : memcmp libc-02 (b20002, l'héritage scellé M1 — le seul appel direct DÉCLARÉ)
; Notation explicite générée par outils/auteur.py depuis brouillons/sys-02-resolveur.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 293 o · padding : 27 o (NOP)
; Étiquettes résolues : .boucle=0xa0b8, .suivant=0xa12f, .nom_absent=0xa135, .stub_divergent=0xa141, .span_invalide=0xa14d, .pas_module=0xa155, .eat_absente=0xa15d
test rcx, rcx
je 0xa14d
test rdx, rdx
je 0xa14d
mov r11d, dword ptr [r8 + 0x3C]
cmp r11d, 0x40
jb 0xa155
cmp r11d, 0x400
ja 0xa155
lea r9, [r8 + r11]
cmp dword ptr [r9], 0x4550
jne 0xa155
mov r10d, dword ptr [r9 + 0x88]
test r10d, r10d
jz 0xa15d
lea r10, [r8 + r10]
sub rsp, 0x48
mov qword ptr [rsp + 0x20], rcx
mov qword ptr [rsp + 0x28], rdx
mov qword ptr [rsp + 0x30], r8
mov qword ptr [rsp + 0x38], r10
mov r9d, dword ptr [r10 + 0x20]
lea r9, [r8 + r9]
mov r10d, dword ptr [r10 + 0x18]
xor eax, eax
cmp rax, r10
jae 0xa135
mov r11d, dword ptr [r9 + rax*4]
add r11, qword ptr [rsp + 0x30]
mov rdx, qword ptr [rsp + 0x20]
mov r8, qword ptr [rsp + 0x28]
push rax
push r10
push r9
sub rsp, 0x28
mov rcx, r11
call 0x1180
add rsp, 0x28
pop r9
pop r10
test eax, eax
pop rax
jne 0xa12f
mov rdx, qword ptr [rsp + 0x38]
mov r11d, dword ptr [rdx + 0x24]
mov rdx, qword ptr [rsp + 0x30]
lea r11, [rdx + r11]
movzx ecx, word ptr [r11 + rax*2]
mov rdx, qword ptr [rsp + 0x38]
mov r11d, dword ptr [rdx + 0x1C]
mov rdx, qword ptr [rsp + 0x30]
lea r11, [rdx + r11]
mov r11d, dword ptr [r11 + rcx*4]
lea rdx, [rdx + r11]
cmp dword ptr [rdx], 0xB8D18B4C
jne 0xa141
mov eax, dword ptr [rdx + 4]
add rsp, 0x48
ret
add rax, 1
jmp 0xa0b8
mov rax, -1
add rsp, 0x48
ret
mov rax, -4
add rsp, 0x48
ret
mov rax, -5
ret
mov rax, -2
ret
mov rax, -3
ret
