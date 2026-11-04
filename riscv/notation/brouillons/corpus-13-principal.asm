; corpus-13-principal · brouillon étiqueté — spec corpus-13:R1 (le FICHIER
; CANONIQUE vit à unix/I/), bloc carte f71013. LE RITUEL DE PARITÉ :
; lancer l'auto-test (libc-08 — les 21 vecteurs dorés du patrimoine,
; exécutés ici par l'instance RV64 des MÊMES contrats), journaliser le
; verdict par tcp-11, terminer au code du verdict par sortir (Q3 : deux
; sites, 0 ou 1, la valeur N tranche — Q2 : le verdict TOUJOURS rendu).
; _start (e_entry 0x1C40, RELATIF — ET_DYN/PIE) : [sp] = argc, sp ≡ 0
; mod 16, AUCUN registre garanti à l'entrée ; le corps ne touche JAMAIS sp
; (I4 : jal ne pousse rien, ra porte le lien — et le rituel ne revient
; jamais : sortir termine).
; LES DEUX ANCRES DU CORPUS (le modèle sr-04 généralisé — chaque fenêtre
; déclarée en I3, la portée imm12 contraint sa place) :
;   paire 1 @ 0x1C40 : s1 = base + 0 (LES .rodata 0x140-0x580 — les
;     vecteurs dorés, les chaînes du rituel, le staging, la table R10) ;
;   paire 2 @ 0x1C48 : s2 = base + 0x3400 (LA FENÊTRE .bss CENTRALE — la
;     leçon imm12 du chantier : la base 0x3000 mettrait le verrou 0x3800 à
;     +0x800 = 2048, hors plage de UN ; au centre : le curseur à -0x400,
;     l'arène à -0x3C0, le verrou à +0x400, tout dans ±2047).
; s1/s2 sont NON VOLATILS psABI : les appelés les préservent, le corpus
; entier vit sur ces DEUX fenêtres. N qui traverse vit en s0 (D150 :
; non volatil — les appelés le sauvegardent s'ils l'utilisent).
@A_AUTOTEST = 0x1340
@A_JOURNAL = 0x1840
@A_SORTIR = 0x1040
@J_PREF = 0x280
@L_PREF = 18
@J_SUFF = 0x2A0
@L_SUFF = 10
@ANCRE_RODATA = 0x1C40
@ANCRE_BSS_CORPUS = 0x1C48
auipc s1, @ANCRE_RODATA_HI
addi s1, s1, @ANCRE_RODATA_LO
auipc s2, @ANCRE_BSS_CORPUS_HI
addi s2, s2, @ANCRE_BSS_CORPUS_LO
jal @A_AUTOTEST
mv s0, a0
addi a0, s1, @J_PREF
addi a1, zero, @L_PREF
mv a2, s0
addi a3, s1, @J_SUFF
addi a4, zero, @L_SUFF
jal @A_JOURNAL
addi t0, zero, 0x15
bne s0, t0, .ko
addi a0, zero, 0
j .fin
.ko:
addi a0, zero, 1
.fin:
jal @A_SORTIR
