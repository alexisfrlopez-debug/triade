; sys-01-emetteur · bloc émetteur syscall (le trombone ABI, six octets) · spec sys-01:R1 · bloc carte g90001
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0xa000, taille 64 octets
; Dépendances : bloc feuille ; le site syscall est l'unique interaction (aucun IAT, aucun appel)
; Notation explicite générée par outils/auteur.py depuis brouillons/sys-01-emetteur.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 6 o · padding : 58 o (NOP)
mov r10, rcx
syscall
ret
