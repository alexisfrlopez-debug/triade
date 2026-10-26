; libc-01-memcpy · bloc copie mémoire (memcpy) · spec libc-01:R1 · bloc carte b20001
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x1100, taille 128 octets
; Dépendances : bloc feuille ; aucun accès extérieur
; Notation explicite générée par outils/auteur.py depuis brouillons/libc-01-memcpy.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 19 o · padding : 109 o (NOP)
push rdi
push rsi
mov rax, rcx
mov rdi, rcx
mov rsi, rdx
mov rcx, r8
rep movsb byte ptr [rdi], byte ptr [rsi]
pop rsi
pop rdi
ret
