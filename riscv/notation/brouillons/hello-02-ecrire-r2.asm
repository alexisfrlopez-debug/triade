; hello-02-ecrire-r2 · brouillon étiqueté — spec hello-02:R2 (le FICHIER
; CANONIQUE vit à unix/I/ — l'instance RV64 le CHARGE, aucune copie), bloc
; carte f71001. L'interface d'écriture du corpus : un appel unique au service
; d'écriture du profil (I4), le verdict BRUT propagé (Q1), feuille pure (I2).
; SysV x86-64 : rdi/rsi/rdx, sys_write 1 — psABI RV64 : a0/a1/a2, ecall
; a7 = 64 (asm-generic — la table x86-64 est REFUSÉE nommément : la parité
; est SÉMANTIQUE, jamais lexicale, fiche § 4).
@SYS_WRITE = 0x40
addi a7, zero, @SYS_WRITE
ecall
ret
