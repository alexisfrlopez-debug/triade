; hello-03-sortir-r2 · brouillon étiqueté — spec hello-03:R2 (le FICHIER
; CANONIQUE vit à unix/I/), bloc carte f71002. La terminaison du corpus :
; l'appel ne revient jamais (Q1) ; l'inaccessible défensif SUIT l'appel
; (I1 : ebreak — l'équivalent exact du rôle ud2 des profils x86-64, fiche
; § 7 : la garde défensive, fail-closed). Aucun ret JAMAIS (V3 de la spec).
; SysV : sys_exit_group 231 — psABI RV64 : ecall a7 = 94 (asm-generic).
@SYS_EXIT_GROUP = 0x5E
addi a7, zero, @SYS_EXIT_GROUP
ecall
ebreak
