; libc-04-itoa-r3 · brouillon étiqueté — spec libc-04:R3 (le FICHIER
; CANONIQUE vit à unix/I/), bloc carte f71006. La conversion décimale u32 :
; Q1 la représentation sans zéro non significatif, NUL-terminée ; Q2 le
; premier chiffre à l'offset 0 (la génération en place PUIS le compactage —
; l'espace de travail entre le NUL et +11 est non spécifié, Q4 : aucune
; écriture hors du tampon de douze octets) ; Q3 le tampon rendu ; I4 la
; valeur 0 produit « 0 » (la boucle do-while génère AU MOINS un chiffre).
; La valeur est masquée u32 (slli/srli 32 — le portage du « mov eax, edi »
; de l'instance x86-64, qui zéro-étend par l'écriture 32 bits) ; la division
; par 10 explicite (D21 : aucune magie multiplicative) : remu/divu —
; l'extension M du profil.
; L'ordre : remu PUIS divu (les deux lisent l'ANCIEN v — le divu l'écrit
; après, la séquence est sûre).
slli t0, a0, 32
srli t0, t0, 32
addi t2, a1, 11
addi t4, zero, 10
sb zero, 0(t2)
.genere:
remu t3, t0, t4
divu t0, t0, t4
addi t3, t3, 0x30
addi t2, t2, -1
sb t3, 0(t2)
bnez t0, .genere
; le compactage : de t2 (premier chiffre) vers a1 (offset 0)
mv t5, a1
.compacte:
lbu t3, 0(t2)
sb t3, 0(t5)
beqz t3, .fin
addi t2, t2, 1
addi t5, t5, 1
j .compacte
.fin:
mv a0, a1
ret
