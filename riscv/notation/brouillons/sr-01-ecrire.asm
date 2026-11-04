; sr-01-ecrire · brouillon étiqueté — spec sr-01:R1, bloc carte f70001
; Feuille psABI : a0 = fd, a1 = tampon, a2 = longueur ; a7 = numéro de
; syscall (table ASM-GENERIC du jalon — write = 64, PAS 1 : la garde
; anti-table-x86 vit au builder) ; ecall ; a0 = retour BRUT (le -errno du
; noyau au succès près) ; AUCUNE zone rouge (psABI — le piège inverse de
; SysV x86-64), 0 octet de pile, t1 jamais touché.
@SYS_WRITE = 64
addi a7, zero, @SYS_WRITE
ecall
ret
