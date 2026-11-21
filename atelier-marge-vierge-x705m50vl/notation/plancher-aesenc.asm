; plancher-aesenc · LA SONDE DE DÉBIT PUR DE L'UNITÉ AES (x705m50vl, la vague 12)
; HUIT chaînes aesenc INDÉPENDANTES sur registres SEULS — aucune charge de
; clé, aucune donnée, aucun accès mémoire : le DÉBIT NU de l'unité AES-NI
; (le plancher de port pressure — LA CAUSE MESURÉE si la cible ≤3 c/bloc est
; manquée : le rapport confronte les cycles/bloc mesurés au plancher
; 10 × c/aesenc, jamais un chiffre ajusté)
; ABI msx64 : rcx = le nombre d'itérations (chaque itération avance les HUIT
; chaînes d'un aesenc) ; rax = 0 au retour ; xmm0-xmm8 volatils, aucun appel
; Copie de laboratoire à la marge VIERGE 0xF400 — le scellé INTACT
test rcx, rcx
jz .fin
pxor xmm8, xmm8
.boucle:
aesenc xmm0, xmm8
aesenc xmm1, xmm8
aesenc xmm2, xmm8
aesenc xmm3, xmm8
aesenc xmm4, xmm8
aesenc xmm5, xmm8
aesenc xmm6, xmm8
aesenc xmm7, xmm8
dec rcx
jnz .boucle
.fin:
xor eax, eax
ret
