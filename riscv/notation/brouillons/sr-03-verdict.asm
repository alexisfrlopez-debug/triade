; sr-03-verdict · brouillon étiqueté — spec sr-03:R1, bloc carte f70003
; Feuille pure : a0 = retour BRUT du syscall (négatif, plage [-4095, -1]) ;
; errno = -a0 ; balayage EXHAUSTIF de la table ERRNOS (le nombre borne) ;
; errno dans la table → a0 = verdict ; hors table → a0 = 6 (VERDICT_FATAL,
; fail-closed). PRÉCONDITION : s1 = base (posée par sr-04). t1 JAMAIS
; touché (le porteur du brut) : t0/t2/t4 suffisent. Le succès n'est JAMAIS
; consulté ici : a0 dans [0, 4095] se constate par PLAGE chez l'appelant.
@ERRNOS = 0x140
@ENTREES = 0x144
neg a0, a0
lw t0, @ERRNOS(s1)
addi t4, s1, @ENTREES
.boucle:
beqz t0, .fatal
lw t2, 0(t4)
beq t2, a0, .trouve
addi t4, t4, 8
addi t0, t0, -1
j .boucle
.trouve:
lw a0, 4(t4)
ret
.fatal:
addi a0, zero, 6
ret
