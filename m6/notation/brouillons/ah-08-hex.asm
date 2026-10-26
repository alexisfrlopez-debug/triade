; ah-08-hex · brouillon étiqueté — spec ah-08:R1, bloc carte d40008
; 32 octets binaires -> 64 caractères hexa minuscules (alphabet sha256sum)
; FEUILLE : 0 octet de pile, aucun non-volatil, r8 = base de table (I2)
; r9 curse destination ; source jamais écrite, dst limité à 64 o (Q2)
@R_HEXCHARS = 0x2100
lea r8, [rip + @R_HEXCHARS]
xor ecx, ecx
mov r9, rsi
.boucle:
movzx eax, byte ptr [rdi + rcx]
mov edx, eax
shr eax, 4
and edx, 0xF
movzx eax, byte ptr [r8 + rax]
movzx edx, byte ptr [r8 + rdx]
mov byte ptr [r9], al
mov byte ptr [r9 + 1], dl
add r9, 2
add ecx, 1
cmp ecx, 32
jb .boucle
mov rax, rsi
ret
