; libc-01-memcpy-r2 · bloc copie mémoire (libc-01:R2) · spec libc-01:R2 · bloc carte f61003
; Profil : x86-64-linux-elf64 · ABI SysV · slot RVA 0x1080, taille 64 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/libc-01-memcpy-r2.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 9 o · padding : 55 o (NOP)
mov rax, rdi
mov rcx, rdx
rep movsb byte ptr [rdi], byte ptr [rsi]
ret
