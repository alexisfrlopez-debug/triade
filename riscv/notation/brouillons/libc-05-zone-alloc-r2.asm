; libc-05-zone-alloc-r2 · brouillon étiqueté — spec libc-05:R2 (le FICHIER
; CANONIQUE vit à unix/I/), bloc carte f71007. L'allocateur par avancement
; de curseur : Q1 le pointeur aligné sur la demande, borne basse = l'ancien
; curseur aligné ; Q2 le curseur avance de la taille ; Q3 l'échec propre
; (rax = 0, curseur inchangé — le refus précède TOUTE écriture du curseur) ;
; Q4 taille 0 : pointeur valide. I3 : la SEULE écriture est le qword curseur.
; Les validations (P1) : taille <= arène, alignement non nul, puissance de
; deux, <= 64 — dans cet ordre, l'échec nommé AVANT toute lecture du curseur.
; LA FENÊTRE .bss : l'ancre s2 = base + 0x3400 (LE CENTRE de la zone — la
; leçon imm12 du chantier : la base 0x3000 mettrait le verrou à +0x800,
; hors plage de UN). Le curseur vit à s2-0x400, l'arène à s2-0x3C0.
@CURSEUR_REL = -0x400
@ARENE_REL = -0x3C0
@ARENE_TAILLE = 0x7C0
addi t3, zero, @ARENE_TAILLE
bltu t3, a0, .echec
beqz a1, .echec
addi t4, a1, -1
and t5, t4, a1
bnez t5, .echec
addi t3, zero, 0x40
bltu t3, a1, .echec
; la borne alignée : (curseur + align-1) & ~(align-1)
ld t0, @CURSEUR_REL(s2)
add t2, t0, t4
not t6, t4
and t2, t2, t6
; le débordement : borne + taille > arène → échec AVANT la écriture
add t5, t2, a0
addi t3, zero, @ARENE_TAILLE
bltu t3, t5, .echec
sd t5, @CURSEUR_REL(s2)
; le pointeur : arène + borne (l'arène est alignée 64 en absolu — frag-loc)
addi a0, s2, @ARENE_REL
add a0, a0, t2
ret
.echec:
addi a0, zero, 0
ret
