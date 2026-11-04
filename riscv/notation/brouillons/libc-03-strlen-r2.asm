; libc-03-strlen-r2 · brouillon étiqueté — spec libc-03:R2 (le FICHIER
; CANONIQUE vit à unix/I/), bloc carte f71005. La longueur jusqu'au premier
; octet nul (Q1), la lecture s'arrête strictement au premier nul (I4), la
; chaîne inchangée (Q2). Feuille pure (I1). Le marcheur part de a0 (t0),
; la longueur rendue par différence (sub) — a0, le retour psABI (a0 porte
; encore l'origine : seul t0 a marché).
mv t0, a0
.boucle:
lbu t2, 0(t0)
beqz t2, .fin
addi t0, t0, 1
j .boucle
.fin:
sub a0, t0, a0
ret
