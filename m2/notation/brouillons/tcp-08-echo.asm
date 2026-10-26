; tcp-08-echo v1 · brouillon · transformation identité · (rcx dst, rdx src, r8 n) -> rax n
; spec tcp-08:R1 · c30008 · entrée 0x4600 alignée 16 : 8 premiers octets trampolinables
; FEUILLE : aucun appel, aucun push, volatils uniquement (I1/I2)
mov rax, r8
test r8, r8
je .fin
xor r9, r9
.boucle:
mov r10b, byte ptr [rdx + r9]
mov byte ptr [rcx + r9], r10b
inc r9
cmp r9, r8
jb .boucle
.fin:
ret
