; libc-06-zone-reset-r2 · brouillon étiqueté — spec libc-06:R2 (le FICHIER
; CANONIQUE vit à unix/I/), bloc carte f71008. La réinitialisation en UNE
; instruction de stockage (Q1 : le curseur vaut 0) ; la seule écriture du
; bloc est le qword curseur (I4) ; l'arène n'est pas nettoyée (I5 — le
; contenu devient indéfini, l'initialisation appartient aux propriétaires).
; Le store du registre zero : sd zero, @CURSEUR_REL(s2) — l'instance x86-64
; porte lea + mov qword 0 ; l'instance RV64 : le store direct (l'ancre
; porte l'adresse, le registre zero porte la valeur).
@CURSEUR_REL = -0x400
sd zero, @CURSEUR_REL(s2)
ret
