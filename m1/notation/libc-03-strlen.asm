; libc-03-strlen · bloc longueur de chaîne (strlen) · spec libc-03:R1 · bloc carte b20003
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x1200, taille 128 octets
; Dépendances : bloc feuille ; aucun accès extérieur
; Notation explicite générée par outils/auteur.py depuis brouillons/libc-03-strlen.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 14 o · padding : 114 o (NOP)
; Étiquettes résolues : .boucle=0x1202, .fin=0x120d
xor eax, eax
cmp byte ptr [rcx + rax], 0
je 0x120d
inc rax
jmp 0x1202
ret
