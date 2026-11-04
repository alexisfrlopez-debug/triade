; libc-02-memcmp-r2 · brouillon étiqueté — spec libc-02:R2 (le FICHIER
; CANONIQUE vit à unix/I/), bloc carte f71004. La comparaison normalisée :
; -1 / 0 / +1 exactement (Q1-Q3), le premier octet divergent tranche (Q4),
; n = 0 → 0 (E1). Feuille pure (I1), les régions jamais écrites (I4).
; L'instance x86-64 : repe cmpsb puis l'examen des octets divergents ;
; l'instance RV64 : la comparaison à chaque pas (bltu/beq — les trois issues
; au site même).
.boucle:
beqz a2, .zero
lbu t2, 0(a0)
lbu t3, 0(a1)
bltu t2, t3, .moins
beq t2, t3, .avance
; supérieur strict : +1 (premier octet divergent, Q2)
addi a0, zero, 1
ret
.moins:
; inférieur strict : -1 (Q1)
addi a0, zero, -1
ret
.avance:
addi a0, a0, 1
addi a1, a1, 1
addi a2, a2, -1
j .boucle
.zero:
addi a0, zero, 0
ret
