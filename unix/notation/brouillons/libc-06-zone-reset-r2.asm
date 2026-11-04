; libc-06-zone-reset-r2 · brouillon étiqueté — spec libc-06:R2, bloc carte f61008
; La réinitialisation en UNE instruction de store : le curseur (au plan de
; l'image — frag-loc : 0x3000 au corpus, 0x3000 chez m1, la MÊME géométrie)
; remis à zéro, rien d'autre (I4 — la seule écriture du bloc). La valeur de
; retour n'est pas une donnée du contrat (Q2). Relatif RIP : l'image est
; PIE, le déplacement est un lien-temps.
@CURSEUR = 0x3000
lea r8, [rip + @CURSEUR]
mov qword ptr [r8], 0
ret
