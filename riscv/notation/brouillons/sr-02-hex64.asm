; sr-02-hex64 · brouillon étiqueté — spec sr-02:R1, bloc carte f70002
; Feuille pure : a0 = valeur (BRUTE — un a0 négatif se formate en son
; complément à deux), a1 = destination 16 o (le curseur avance — registre
; de travail). PRÉCONDITION : s1 = base (posée par sr-04 — le bloc lit
; l'ancre, il ne la pose pas) ; l'accès HEXCHARS vit en [s1 + 0x180].
; t1 JAMAIS touché (le porteur du brut chez sr-04 — fiche § 2) :
; t0/t3/t4 suffisent. 16 itérations, décalage 60, 56, …, 0.
@HEXCHARS = 0x180
addi t0, zero, 60
addi t4, s1, @HEXCHARS
.boucle:
srl t3, a0, t0
andi t3, t3, 0xf
add t3, t3, t4
lbu t3, 0(t3)
sb t3, 0(a1)
addi a1, a1, 1
addi t0, t0, -4
bgez t0, .boucle
ret
