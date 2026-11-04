; hello-02-ecrire-r2 · bloc écrire — interface du corpus (hello-02:R2) · spec hello-02:R2 · bloc carte f61001
; Profil : x86-64-linux-elf64 · ABI SysV · slot RVA 0x1000, taille 64 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/hello-02-ecrire-r2.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 8 o · padding : 56 o (NOP)
; Symboles (vérifiés par build_m6.py contre layout.py) : @SYS_WRITE=0x1
mov eax, 1
syscall
ret
