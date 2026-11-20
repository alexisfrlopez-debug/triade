; tls13-16-ni-v4-creux · LE CREUX DE CALIBRATION : le squelette de la porteuse
; nue SANS cryptographie (aucun aesenc, aucun appel) — le plancher de l'enveloppe
; mesuré : les poussées, la pose des non-volatils, la boucle de comptage et
; l'épilogue ; la cellule creux@64/creux@256 isole le coût FIXE F' de la
; porteuse (la décomposition de l'enveloppe au rapport)
; ABI msx64 (rcx, rdx, r8, r9 = N blocs — ignorés sauf r9)
; Copie de laboratoire à la marge VIERGE 0xF400 — le scellé INTACT
push r12
push r13
push r14
push r15
test r9, r9
jz .fin
mov r12, rcx
mov r13, rdx
mov r14, r8
mov r15, r9
.boucle:
dec r15
jnz .boucle
.fin:
xor eax, eax
pop r15
pop r14
pop r13
pop r12
ret
