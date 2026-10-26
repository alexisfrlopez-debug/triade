; ah-02-lire · brouillon étiqueté — spec ah-02:R1, bloc carte d40002
; lecture par appel système : sys_read(edi=fd, rsi=tampon, edx=capacité)
; un appel, un verdict : rax = octets lus (0 = EOF) ou -errno
xor eax, eax
syscall
ret
