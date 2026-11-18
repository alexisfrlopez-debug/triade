.intel_syntax noprefix
.global dummy_msx64
dummy_msx64:
    mov rax, [rsp+0x28]
    add rax, [rsp+0x30]
    ret
