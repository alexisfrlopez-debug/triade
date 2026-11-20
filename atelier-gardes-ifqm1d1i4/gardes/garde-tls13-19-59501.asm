; garde-tls13-19-59501 · LA GARDE RUNTIME de l'accès movzx r11, byte ptr [rcx + rax]
; l'invariant externe : le contrat de l'appelant (le contexte AEAD) — la zone CTX [0x500000, 0x501000)
; la copie de laboratoire à la marge 0x10000 — le scellé intact (le modèle OPT-01)
mov rdx, rcx
add rdx, rax
; (1) LA FACE BASSE : l'adresse effective AU-DESSUS du plancher
cmp rdx, 5242880
jb .refus_garde
; (2) LA FACE HAUTE : bornée au plafond de la zone
cmp rdx, 5246976
jae .refus_garde
; les deux faces tenues : l'ADMISSION (eax = 0)
xor eax, eax
ret
.refus_garde:
mov eax, -5
ret
