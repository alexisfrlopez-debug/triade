; ah-03-sortir · brouillon étiqueté — spec ah-03:R1, bloc carte d40003
; terminaison : sys_exit(edi=code) — ne revient jamais (I2 : rien après syscall)
mov eax, 60
syscall
