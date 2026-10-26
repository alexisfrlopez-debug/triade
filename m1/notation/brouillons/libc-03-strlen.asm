xor eax, eax
.boucle:
cmp byte ptr [rcx + rax], 0
je .fin
inc rax
jmp .boucle
.fin:
ret
