; libc-03-strlen-r2 · brouillon étiqueté — spec libc-03:R2, bloc carte f61005
; La feuille la plus courte du patrimoine : chaîne nommée (frag-con : SysV —
; rdi ; msx64 — rcx). Le compteur vit en rax (le retour même, Q1), la
; lecture s'arrête strictement au premier octet nul (I4), aucun registre
; non volatil touché, pile équilibrée sans jamais l'avoir déplacée (I2).
xor eax, eax
.boucle:
cmp byte ptr [rdi + rax], 0
je .fin
inc rax
jmp .boucle
.fin:
ret
