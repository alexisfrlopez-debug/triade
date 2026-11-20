; garde-loupe-06-18474 · LA GARDE RUNTIME de l'accès mov r11d, dword ptr [rbx + 0xc]
; l'invariant externe : le champ du plan (le CADRE, 960 o — le layout) — la zone CADRE [0xe000, 0xe3c0)
; la copie de laboratoire à la marge 0x10000 — le scellé intact (le modèle OPT-01)
mov rax, rbx
add rax, 12
; (1) LA FACE BASSE : l'adresse effective AU-DESSUS du plancher
cmp rax, 57344
jb .refus_garde
; (2) LA FACE HAUTE : bornée au plafond de la zone
cmp rax, 58304
jae .refus_garde
; les deux faces tenues : l'ADMISSION (eax = 0)
xor eax, eax
ret
.refus_garde:
mov eax, -5
ret
