push rdi
push rsi
mov rax, rcx
mov rdi, rcx
mov rsi, rdx
mov rcx, r8
rep movsb byte ptr [rdi], byte ptr [rsi]
pop rsi
pop rdi
ret
