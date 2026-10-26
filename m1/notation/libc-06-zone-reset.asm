; libc-06-zone-reset · bloc réinitialisation de zone · spec libc-06:R1 · bloc carte b20006
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x1380, taille 64 octets
; Dépendances : données : curseur @0x3000
; Notation explicite générée par outils/auteur.py depuis brouillons/libc-06-zone-reset.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 15 o · padding : 49 o (NOP)
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x1380 + 0x7 + 0x1c79 = 0x3000
lea r8, [rip + 0x1c79]
mov qword ptr [r8], 0
ret
