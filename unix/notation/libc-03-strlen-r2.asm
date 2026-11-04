; libc-03-strlen-r2 · bloc longueur de chaîne (libc-03:R2) · spec libc-03:R2 · bloc carte f61005
; Profil : x86-64-linux-elf64 · ABI SysV · slot RVA 0x1140, taille 64 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/libc-03-strlen-r2.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 14 o · padding : 50 o (NOP)
; Étiquettes résolues : .boucle=0x1142, .fin=0x114d
xor eax, eax
cmp byte ptr [rdi + rax], 0
je 0x114d
inc rax
jmp 0x1142
ret
