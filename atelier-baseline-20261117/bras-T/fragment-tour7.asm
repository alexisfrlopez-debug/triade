    ; Lecture de la fenêtre (I3)
    mov rcx, qword ptr [rbx + 528] ; hFile depuis la zone d'état
    mov rdx, rsp      ; lpBuffer
    add rdx, 0xB0     ; Décalage pour le tampon après le contexte SHA (rsp+0x40) et l'ombre (rsp+0x00)
    mov r8, r12       ; nNumberOfBytesToRead
    mov r9, NULL      ; lpNumberOfBytesRead
    call qword ptr [rip + IAT_ReadFile]
    test rax, rax
    jz .erreur_systeme
