    ; Repositionnement du pointeur fichier (I4)
    mov rcx, rdi      ; hFile
    mov rdx, r15      ; lpDistanceToMove
    mov r8, NULL      ; lpNewFilePointer
    mov r9, NULL      ; lp_dw
    call SetFilePointerEx
    test rax, rax
    jz .erreur_systeme

    ; Lecture de la fenêtre (I3)
;; — SUITE DU FRAGMENT (le site GetLastError) —
.erreur_systeme:
    ; E4 : GetLastError, sortie intacte (I4, I5)
    call GetLastError
    mov rax, -6       ; E4
