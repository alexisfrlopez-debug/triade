; libc-07-memset · bloc remplissage mémoire (memset) · spec libc-07:R1 · bloc carte b20007
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x13c0, taille 128 octets
; Dépendances : bloc feuille ; aucun accès extérieur
; Notation explicite générée par outils/auteur.py depuis brouillons/libc-07-memset.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 21 o · padding : 107 o (NOP)
push rbx
push rdi
mov rbx, rcx
mov rdi, rcx
mov rcx, r8
mov al, dl
rep stosb byte ptr [rdi], al
mov rax, rbx
pop rdi
pop rbx
ret
