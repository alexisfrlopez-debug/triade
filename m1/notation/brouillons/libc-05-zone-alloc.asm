cmp rcx, 0x7C0
ja .invalide
test rdx, rdx
je .invalide
lea r9, [rdx - 1]
test r9, rdx
jne .invalide
cmp rdx, 64
ja .invalide
lea r8, [rip + CURSEUR]
mov rax, qword ptr [r8]
lea r10, [rip + ARENE]
add rax, r9
not r9
and rax, r9
add r10, rax
add rax, rcx
cmp rax, 0x7C0
ja .invalide
mov qword ptr [r8], rax
mov rax, r10
ret
.invalide:
xor eax, eax
ret
