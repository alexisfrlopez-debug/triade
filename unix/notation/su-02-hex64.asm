; su-02-hex64 · bloc formatage hexadécimal u64 · spec su-02:R1 · bloc carte f60002
; Profil : x86-64-linux-elf64 · ABI SysV · slot RVA 0x1040, taille 128 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/su-02-hex64.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 46 o · padding : 82 o (NOP)
; Étiquettes résolues : .boucle=0x104f
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x1040 + 0x7 - 0xec7 = 0x180 (@HEXCHARS)
; Symboles (vérifiés par build_m6.py contre layout.py) : @HEXCHARS=0x180
lea r8, [rip - 0xec7]
xor r9d, r9d
mov ecx, 0x3c
mov rax, rdi
shr rax, cl
and eax, 0xf
movzx rax, byte ptr [r8 + rax]
mov byte ptr [rsi + r9], al
inc r9d
sub ecx, 4
cmp r9d, 0x10
jne 0x104f
ret
