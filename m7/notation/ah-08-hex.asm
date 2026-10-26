; ah-08-hex · bloc encodage hexadécimal · spec ah-08:R1 · bloc carte d40008
; Profil : x86-64-linux-elf64 · ABI SysV · slot RVA 0x1600, taille 128 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/ah-08-hex.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 57 o · padding : 71 o (NOP)
; Étiquettes résolues : .boucle=0x160c
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x1600 + 0x7 + 0xaf9 = 0x2100 (@R_HEXCHARS)
; Symboles (vérifiés par build_ah.py contre layout.py) : @R_HEXCHARS=0x2100
lea r8, [rip + 0xaf9]
xor ecx, ecx
mov r9, rsi
movzx eax, byte ptr [rdi + rcx]
mov edx, eax
shr eax, 4
and edx, 0xf
movzx eax, byte ptr [r8 + rax]
movzx edx, byte ptr [r8 + rdx]
mov byte ptr [r9], al
mov byte ptr [r9 + 1], dl
add r9, 2
add ecx, 1
cmp ecx, 0x20
jb 0x160c
mov rax, rsi
ret
