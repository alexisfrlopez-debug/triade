xor eax, eax
test r8, r8
je .zero
push rdi
push rsi
mov rdi, rcx
mov rsi, rdx
mov rcx, r8
repe cmpsb byte ptr [rsi], byte ptr [rdi]
je .egal
movzx r10d, byte ptr [rdi - 1]
movzx r11d, byte ptr [rsi - 1]
cmp r10d, r11d
ja .sup
mov eax, -1
jmp .fin
.egal:
xor eax, eax
jmp .fin
.sup:
mov eax, 1
.fin:
pop rsi
pop rdi
ret
.zero:
ret
