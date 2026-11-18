.intel_syntax noprefix
.global shim_strlen
shim_strlen:
    push rdi
    push rsi
    sub rsp, 8
    mov rdi, rcx
    lea rax, [rip+cible_strlen]
    mov rax, [rax]
    call rax
    add rsp, 8
    pop rsi
    pop rdi
    ret
cible_strlen:
    .quad 0
