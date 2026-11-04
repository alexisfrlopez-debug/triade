; libc-07-memset-r2 · bloc remplissage mémoire (libc-07:R2) · spec libc-07:R2 · bloc carte f61009
; Profil : x86-64-linux-elf64 · ABI SysV · slot RVA 0x12c0, taille 128 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/libc-07-memset-r2.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 15 o · padding : 113 o (NOP)
mov r10, rdi
mov rcx, rdx
mov al, sil
rep stosb byte ptr [rdi], al
mov rax, r10
ret
