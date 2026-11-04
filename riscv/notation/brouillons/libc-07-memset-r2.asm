; libc-07-memset-r2 · brouillon étiqueté — spec libc-07:R2 (le FICHIER
; CANONIQUE vit à unix/I/), bloc carte f71009. Le remplissage : Q1 les n
; octets égaux à la valeur, Q3 au-delà de dst+n jamais écrit, I4 n = 0 :
; aucun octet. Feuille pure (I1). La valeur est 8 bits significatifs (P2) —
; sb ne porte que l'octet bas de a1 (l'ABI a déjà la valeur dans a1, le
; sb la tronque : aucune préparation nécessaire).
; L'instance x86-64 : rep stosb ; l'instance RV64 : la boucle explicite —
; l'OBSERVABLE (la région remplie) est invariant.
; a0 (dst) n'est JAMAIS modifié — le marcheur vit en t0 (initialisé AVANT la
; boucle) : le retour est dst par survivors (Q2 : la valeur de retour
; contient dst). n = 0 : le beqz sort immédiatement, AUCUN octet (I4).
mv t0, a0
.boucle:
beqz a2, .fin
sb a1, 0(t0)
addi t0, t0, 1
addi a2, a2, -1
j .boucle
.fin:
ret
