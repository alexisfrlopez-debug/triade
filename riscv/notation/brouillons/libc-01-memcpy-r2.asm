; libc-01-memcpy-r2 · brouillon étiqueté — spec libc-01:R2 (le FICHIER
; CANONIQUE vit à unix/I/), bloc carte f71003. La brique de déplacement :
; feuille PURE (I1 : aucun appel, aucun accès système), la copie octet par
; octet en avant (Q1), n = 0 : aucun octet écrit (I4), src inchangé (Q3),
; dst rendu (Q2 — a0, le registre de retour psABI).
; L'instance x86-64 : rep movsb (UNE instruction) ; l'instance RV64 : la
; boucle explicite — l'OBSERVABLE (les octets déplacés) est invariant, la
; notation est le choix du profil.
.boucle:
beqz a2, .fin
lbu t3, 0(a1)
sb t3, 0(a0)
addi a1, a1, 1
addi a0, a0, 1
addi a2, a2, -1
j .boucle
.fin:
ret
