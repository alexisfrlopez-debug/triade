; su-02-hex64 · brouillon étiqueté — spec su-02:R1, bloc carte f60002
; feuille pure : rdi = valeur, rsi = destination (16 o inscriptibles) ;
; 16 itérations, décalage 60 → 0 (I3) ; table HEXCHARS lue en rip (I1) ;
; r8 = table, r9 = indice, rcx = décalage — registres de travail volatils.
@HEXCHARS = 0x180
lea r8, [rip + @HEXCHARS]
xor r9d, r9d
mov ecx, 60
.boucle:
mov rax, rdi
shr rax, cl
and eax, 0xf
movzx rax, byte ptr [r8 + rax]
mov byte ptr [rsi + r9], al
inc r9d
sub ecx, 4
cmp r9d, 16
jne .boucle
ret
