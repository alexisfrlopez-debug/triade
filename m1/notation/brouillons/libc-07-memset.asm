push rbx
push rdi
mov rbx, rcx
mov rdi, rcx
mov rcx, r8
mov al, dl
rep stosb byte ptr [rdi], al
mov rax, rbx
pop rdi
pop rbx
ret
