.intel_syntax noprefix
.global dummy_msx64
dummy_msx64:
    mov rax, [rsp+0x28]     ; arg6 (caractere) au slot d'entree
    mov rbx, [rsp+0x30]     ; hmm entry: ret@0, shadow@8..27, arg5@0x28, arg6@0x30
    ret
