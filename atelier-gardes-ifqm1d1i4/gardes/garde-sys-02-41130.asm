; garde-sys-02-41130 · LA GARDE RUNTIME de l'accès mov r9d, dword ptr [r10 + 0x20]
; l'invariant externe : l'OS (le tampon de l'appel système) — la zone OS [0x500000, 0x501000)
; la copie de laboratoire à la marge 0x10000 — le scellé intact (le modèle OPT-01)
mov rax, r10
add rax, 32
; (1) LA FACE BASSE : l'adresse effective AU-DESSUS du plancher
cmp rax, 5242880
jb .refus_garde
; (2) LA FACE HAUTE : bornée au plafond de la zone
cmp rax, 5246976
jae .refus_garde
; les deux faces tenues : l'ADMISSION (eax = 0)
xor eax, eax
ret
.refus_garde:
mov eax, -5
ret
