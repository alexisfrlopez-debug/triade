    ; Repositionnement du pointeur fichier (I4)
    mov rcx, rdi      ; hFile
    mov rdx, r15      ; lpDistanceToMove
    mov r8, NULL      ; lpNewFilePointer
    mov r9, NULL      ; lp_dw
    call qword ptr [rip + offset_IAT_SetFilePointerEx]
    test rax, rax
    jz .erreur_systeme

    ; Lecture de la fenêtre (I3)
;; — SUITE DU FRAGMENT (le site GetLastError) —
.erreur_systeme:
    ; E4 : GetLastError, sortie intacte (I4, I5)
    call qword ptr [rip + offset_IAT_GetLastError]
    mov rax, -6       ; E4

le geste : substitution des appels directs par des appels indirects via les slots de l'IAT D161.