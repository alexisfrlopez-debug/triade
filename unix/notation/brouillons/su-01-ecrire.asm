; su-01-ecrire · brouillon étiqueté — spec su-01:R1, bloc carte f60001
; feuille sys : rax = 1 (sys_write) exclusivement (I1) ; l'instruction
; syscall détruit rcx/r11 (I2) ; aucun push, 0 octet de pile (feuille).
mov eax, 1
syscall
ret
