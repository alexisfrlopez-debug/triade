; libc-06-zone-reset-r2 · bloc réinitialisation de zone (libc-06:R2) · spec libc-06:R2 · bloc carte f61008
; Profil : x86-64-linux-elf64 · ABI SysV · slot RVA 0x1280, taille 64 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/libc-06-zone-reset-r2.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 15 o · padding : 49 o (NOP)
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x1280 + 0x7 + 0x1d79 = 0x3000 (@CURSEUR)
; Symboles (vérifiés par build_m6.py contre layout.py) : @CURSEUR=0x3000
lea r8, [rip + 0x1d79]
mov qword ptr [r8], 0
ret
