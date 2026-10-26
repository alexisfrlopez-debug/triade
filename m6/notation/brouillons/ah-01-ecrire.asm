; ah-01-ecrire · brouillon étiqueté — spec ah-01:R1, bloc carte d40001
; écriture par appel système : sys_write(edi=fd, rsi=tampon, edx=n)
; interface noyau : nr dans rax, retour rax (négatif = -errno), rcx/r11 détruits
mov eax, 1
syscall
ret
