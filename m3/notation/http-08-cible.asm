; http-08-cible · bloc cible (forme) · spec http-08:R1 · bloc carte e50008
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x5380, taille 320 octets
; Dépendances : feuille pure ; fixture « / » .rdata (chemin par défaut)
; Notation explicite générée par outils/auteur.py depuis brouillons/http-08-cible.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 241 o · padding : 79 o (NOP)
; Étiquettes résolues : .absolu_boucle=0x53ae, .absolu_delim=0x53c9, .absolu_defaut=0x53d1, .absolu_zone=0x53de, .pas_absolu=0x53f6, .pas_origine=0x540d, .sch_boucle=0x540f, .sch_deux_points=0x5420, .refuse=0x543d, .autorite=0x5443, .ecrit=0x5455, .autorite_vide=0x546b
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x53d1 + 0x7 - 0x2f08 = 0x24d0
cmp r8d, 8
je 0x5443
cmp rdx, 7
jb 0x53f6
cmp dword ptr [rcx], 0x70747468
jne 0x53f6
cmp word ptr [rcx + 4], 0x2F3A
jne 0x53f6
cmp byte ptr [rcx + 6], 0x2F
jne 0x53f6
lea rax, [rcx + 7]
lea r10, [rcx + rdx]
cmp rax, r10
jae 0x53d1
movzx r11d, byte ptr [rax]
cmp r11, 0x2F
je 0x53c9
cmp r11, 0x3F
je 0x53d1
add rax, 1
jmp 0x53ae
mov r8, rax
sub r10, rax
jmp 0x53de
lea r8, [rip - 0x2f08]
mov r10d, 1
lea rdx, [rcx + 7]
sub rax, rdx
test rax, rax
je 0x546b
mov r11d, 1
jmp 0x5455
cmp byte ptr [rcx], 0x2F
jne 0x540d
mov r11d, 2
mov r8, rcx
mov r10, rdx
xor edx, edx
xor eax, eax
jmp 0x5455
xor eax, eax
cmp rax, rdx
jae 0x543d
cmp byte ptr [rcx + rax], 0x3A
je 0x5420
add rax, 1
jmp 0x540f
lea r10, [rax + 2]
cmp r10, rdx
jae 0x543d
cmp byte ptr [rcx + rax + 1], 0x2F
jne 0x543d
cmp byte ptr [rcx + rax + 2], 0x2F
jne 0x543d
mov eax, 3
ret
mov eax, 1
ret
mov r11d, 3
mov rax, rdx
mov rdx, rcx
xor r8d, r8d
xor r10d, r10d
mov dword ptr [r9], r11d
mov qword ptr [r9 + 8], rdx
mov qword ptr [r9 + 16], rax
mov qword ptr [r9 + 24], r8
mov qword ptr [r9 + 32], r10
xor eax, eax
ret
mov eax, 2
ret
