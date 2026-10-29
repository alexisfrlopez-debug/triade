; http-03-entete · bloc ligne d'en-tête · spec http-03:R1 · bloc carte e50003
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x4e80, taille 192 octets
; Dépendances : feuille pure ; rognage OWS par bornes uniquement
; Notation explicite générée par outils/auteur.py depuis brouillons/http-03-entete.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 159 o · padding : 33 o (NOP)
; Étiquettes résolues : .col_boucle=0x4e87, .col_test=0x4e91, .col_trouve=0x4e9c, .nom_boucle=0x4ea4, .nom_ok=0x4ec0, .rogne_g=0x4ec7, .rogne_avance=0x4edd, .rogne_d=0x4ee3, .rogne_recule=0x4efa, .ecrit=0x4f00, .nom_invalide=0x4f19
mov r11, r8
xor eax, eax
jmp 0x4e91
cmp byte ptr [rcx + rax], 0x3A
je 0x4e9c
add rax, 1
cmp rax, rdx
jb 0x4e87
mov eax, 1
ret
test rax, rax
je 0x4f19
xor r10d, r10d
cmp r10, rax
jae 0x4ec0
movzx r9d, byte ptr [rcx + r10]
cmp r9, 0x20
je 0x4f19
cmp r9, 0x09
je 0x4f19
add r10, 1
jmp 0x4ea4
lea r10, [rax + 1]
mov r9, rdx
cmp r10, r9
jae 0x4ee3
movzx edx, byte ptr [rcx + r10]
cmp dl, 0x20
je 0x4edd
cmp dl, 0x09
je 0x4edd
jmp 0x4ee3
add r10, 1
jmp 0x4ec7
cmp r9, r10
jbe 0x4f00
movzx edx, byte ptr [rcx + r9 - 1]
cmp dl, 0x20
je 0x4efa
cmp dl, 0x09
je 0x4efa
jmp 0x4f00
sub r9, 1
jmp 0x4ee3
mov qword ptr [r11], rcx
mov qword ptr [r11 + 8], rax
lea rdx, [rcx + r10]
mov qword ptr [r11 + 16], rdx
sub r9, r10
mov qword ptr [r11 + 24], r9
xor eax, eax
ret
mov eax, 2
ret
