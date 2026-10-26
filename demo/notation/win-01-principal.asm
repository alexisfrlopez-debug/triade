; win-01-principal · bloc démo · spec win-01:R1 · bloc carte d40001
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x1400, taille 64 octets
; Dépendances : blocs win-02, win-03, io-02 exit @0x1080
; Notation explicite générée par outils/auteur.py depuis brouillons/win-01-principal.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 36 o · padding : 28 o (NOP)
; Étiquettes résolues : .echec=0x141a
sub rsp, 0x28
call 0x1440
test rax, rax
je 0x141a
call 0x15c0
xor ecx, ecx
call 0x1080
mov ecx, 1
call 0x1080
