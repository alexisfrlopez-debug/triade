; libc-05-zone-alloc-r2 · bloc allocateur par zone (libc-05:R2) · spec libc-05:R2 · bloc carte f61007
; Profil : x86-64-linux-elf64 · ABI SysV · slot RVA 0x1200, taille 128 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/libc-05-zone-alloc-r2.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 79 o · padding : 49 o (NOP)
; Étiquettes résolues : .echec=0x124c
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x121d + 0x7 + 0x1ddc = 0x3000 (@CURSEUR)
;   0x1230 + 0x7 + 0x1e09 = 0x3040 (@ARENE)
; Symboles (vérifiés par build_m6.py contre layout.py) : @ARENE=0x3040, @ARENE_TAILLE=0x7c0, @CURSEUR=0x3000
cmp rdi, 0x7c0
ja 0x124c
test rsi, rsi
je 0x124c
lea r9, [rsi - 1]
test r9, rsi
jne 0x124c
cmp rsi, 0x40
ja 0x124c
lea r8, [rip + 0x1ddc]
mov rax, qword ptr [r8]
add rax, r9
not r9
and rax, r9
lea r10, [rip + 0x1e09]
add r10, rax
add rax, rdi
cmp rax, 0x7c0
ja 0x124c
mov qword ptr [r8], rax
mov rax, r10
ret
xor eax, eax
ret
