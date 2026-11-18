.intel_syntax noprefix
.global tramp
tramp:
    mov r11, r9
    mov r9, rcx
    mov r10, r8
    mov r8, rdx
    mov rdx, rsi
    mov rcx, rdi
    sub rsp, 0x38
    mov [rsp+0x20], r10
    mov [rsp+0x28], r11
    lea rax, [rip+cible]
    mov rax, [rax]
    call rax
    add rsp, 0x38
    ret
cible:
    .quad 0
