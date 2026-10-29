; http-07-autorite · bloc autorité hôte:port · spec http-07:R1 · bloc carte e50007
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x5200, taille 384 octets
; Dépendances : feuille pure ; assistant local .chiffres_port (pile équilibrée)
; Notation explicite générée par outils/auteur.py depuis brouillons/http-07-autorite.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 307 o · padding : 77 o (NOP)
; Étiquettes résolues : .dernier=0x5215, .sans_port=0x5226, .deux_points=0x523a, .crochet=0x525c, .cherche_ferme=0x5263, .ferme=0x5278, .crochet_sans_port=0x52be, .ecrit=0x52d5, .chiffres_port=0x52e3, .chiffres_boucle=0x52f2, .chiffres_ko=0x531e, .hote_vide=0x5321, .port_invalide=0x5327, .crochet_invalide=0x532d
mov r11d, r8d
test rdx, rdx
je 0x5321
cmp byte ptr [rcx], 0x5B
je 0x525c
lea rax, [rdx - 1]
cmp byte ptr [rcx + rax], 0x3A
je 0x523a
test rax, rax
je 0x5226
sub rax, 1
jmp 0x5215
test r11d, r11d
je 0x5327
mov r10d, r11d
mov rax, rdx
jmp 0x52d5
test rax, rax
je 0x5321
lea r8, [rcx + rax + 1]
sub rdx, rax
sub rdx, 1
call 0x52e3
jb 0x5327
jmp 0x52d5
mov rax, 1
cmp rax, rdx
jae 0x532d
cmp byte ptr [rcx + rax], 0x5D
je 0x5278
add rax, 1
jmp 0x5263
sub rax, 1
test rax, rax
je 0x5321
lea r10, [rax + 2]
cmp r10, rdx
jae 0x52be
cmp byte ptr [rcx + r10], 0x3A
jne 0x532d
lea r8, [rcx + rax + 3]
sub rdx, rax
sub rdx, 3
call 0x52e3
jb 0x5327
lea rdx, [rcx + 1]
mov qword ptr [r9], rdx
mov qword ptr [r9 + 8], rax
mov dword ptr [r9 + 16], r10d
xor eax, eax
ret
test r11d, r11d
je 0x5327
lea rdx, [rcx + 1]
mov qword ptr [r9], rdx
mov qword ptr [r9 + 8], rax
mov dword ptr [r9 + 16], r11d
xor eax, eax
ret
mov qword ptr [r9], rcx
mov qword ptr [r9 + 8], rax
mov dword ptr [r9 + 16], r10d
xor eax, eax
ret
push rbx
test rdx, rdx
je 0x531e
cmp rdx, 5
ja 0x531e
xor r10d, r10d
movzx ebx, byte ptr [r8]
sub ebx, 0x30
cmp ebx, 9
ja 0x531e
lea r10, [r10 + r10*4]
add r10, r10
add r10, rbx
add r8, 1
sub rdx, 1
jne 0x52f2
cmp r10d, 0xFFFF
ja 0x531e
clc
pop rbx
ret
stc
pop rbx
ret
mov eax, 1
ret
mov eax, 2
ret
mov eax, 3
ret
