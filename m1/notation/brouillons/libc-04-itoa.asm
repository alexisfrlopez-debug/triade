push rbx
mov rbx, rdx
lea r8, [rbx + 11]
mov byte ptr [r8], 0
mov eax, ecx
.boucle:
mov r9d, 10
xor edx, edx
div r9d
add dl, 48
dec r8
mov byte ptr [r8], dl
test eax, eax
jne .boucle
xor ecx, ecx
.compact:
mov al, byte ptr [r8 + rcx]
mov byte ptr [rbx + rcx], al
test al, al
je .fin
inc rcx
jmp .compact
.fin:
mov rax, rbx
pop rbx
ret
