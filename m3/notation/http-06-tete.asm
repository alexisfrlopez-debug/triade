; http-06-tete · bloc détection de fin de tête · spec http-06:R2 · bloc carte e50006
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x5140, taille 192 octets
; Dépendances : feuille pure ; propriétaire de MAX_TETE 8192 ; rejet LF isolé
; Notation explicite générée par outils/auteur.py depuis brouillons/http-06-tete.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 122 o · padding : 70 o (NOP)
; Étiquettes résolues : .boucle=0x5142, .lf=0x5153, .excessive=0x5193, .suite=0x5199, .isole=0x519f, .fin_boucle=0x51a5, .incomplet=0x51b4
xor eax, eax
cmp rax, rdx
jae 0x51a5
cmp byte ptr [rcx + rax], 0x0A
je 0x5153
add rax, 1
jmp 0x5142
test rax, rax
je 0x519f
cmp byte ptr [rcx + rax - 1], 0x0D
jne 0x519f
lea r9, [rax + 1]
cmp r9, rdx
jae 0x5199
cmp byte ptr [rcx + rax + 1], 0x0D
jne 0x5199
lea r9, [rax + 2]
cmp r9, rdx
jae 0x5199
cmp byte ptr [rcx + rax + 2], 0x0A
jne 0x5199
lea r9, [rax + 3]
cmp r9, 0x2000
ja 0x5193
lea rdx, [rax + 3]
xor eax, eax
ret
mov eax, 2
ret
add rax, 1
jmp 0x5142
mov eax, 3
ret
cmp rdx, 0x2000
jbe 0x51b4
mov eax, 2
ret
mov eax, 1
ret
