; hello-03-sortir-r2 · bloc sortir — interface du corpus (hello-03:R2) · spec hello-03:R2 · bloc carte f61002
; Profil : x86-64-linux-elf64 · ABI SysV · slot RVA 0x1040, taille 64 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/hello-03-sortir-r2.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 9 o · padding : 55 o (NOP)
; Symboles (vérifiés par build_m6.py contre layout.py) : @SYS_EXIT_GROUP=0xe7
mov eax, 0xe7
syscall
ud2
