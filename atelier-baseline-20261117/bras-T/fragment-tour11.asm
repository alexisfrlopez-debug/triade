    ; Lecture de la fenêtre (I3)
    mov rcx, qword ptr [rbx + 528] ; hFile depuis la zone d'état
    lea rdx, [rip + 0xbb06]       ; lpBuffer (adresse du tampon statique TAMPON_CUMUL)
    mov r8, r12                   ; nNumberOfBytesToRead
    mov r9, NULL                  ; lpNumberOfBytesRead
    call qword ptr [rip + IAT_ReadFile]
    test rax, rax
    jz .erreur_systeme

