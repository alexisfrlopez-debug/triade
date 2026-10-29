; http-01-ligne · bloc itérateur de ligne CRLF · spec http-01:R1 · bloc carte e50001
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x4c00, taille 128 octets
; Dépendances : feuille pure ; aucun accès extérieur (propriétaire T5 du balayage)
; Notation explicite générée par outils/auteur.py depuis brouillons/http-01-ligne.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 58 o · padding : 70 o (NOP)
; Étiquettes résolues : .boucle=0x4c05, .test=0x4c09, .incomplet=0x4c34
mov rax, r8
jmp 0x4c09
add rax, 1
cmp rax, rdx
jae 0x4c34
cmp byte ptr [rcx + rax], 0x0D
jne 0x4c05
lea r9, [rax + 1]
cmp r9, rdx
jae 0x4c34
cmp byte ptr [rcx + r9], 0x0A
jne 0x4c05
lea r9, [rax + 2]
sub rax, r8
mov rdx, rax
mov r8, r9
xor eax, eax
ret
mov eax, 1
ret
