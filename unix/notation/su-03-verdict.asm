; su-03-verdict · bloc verdict d'erreur syscall · spec su-03:R1 · bloc carte f60003
; Profil : x86-64-linux-elf64 · ABI SysV · slot RVA 0x10c0, taille 128 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/su-03-verdict.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 50 o · padding : 78 o (NOP)
; Étiquettes résolues : .boucle=0x10d5, .fatal=0x10ec, .trouve=0x10e7
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x10c3 + 0x7 - 0xf8a = 0x140 (@ERRNOS)
; Symboles (vérifiés par build_m6.py contre layout.py) : @ERRNOS=0x140
neg rdi
lea r8, [rip - 0xf8a]
mov ecx, dword ptr [r8]
lea r9, [r8 + 4]
test ecx, ecx
je 0x10ec
cmp edi, dword ptr [r9]
je 0x10e7
add r9, 8
sub ecx, 1
test ecx, ecx
je 0x10ec
jmp 0x10d5
mov eax, dword ptr [r9 + 4]
ret
mov eax, 6
ret
