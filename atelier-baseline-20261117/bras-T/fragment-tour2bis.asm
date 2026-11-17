    ; Repositionnement du pointeur fichier (I4)
    mov rcx, rdi      ; hFile
    mov rdx, r15      ; lpDistanceToMove
    mov r8, NULL      ; lpNewFilePointer
    mov r9, NULL      ; lp_dw
    call SetFilePointerEx
    test rax, rax
    jz .erreur_systeme

    ; Lecture de la fenêtre (I3)
    mov rcx, rdi      ; hFile
    mov rdx, rsp      ; lpBuffer
    add rdx, 112      ; Décalage pour le tampon après le contexte SHA
    mov r8, r12       ; nNumberOfBytesToRead
    mov r9, NULL      ; lpNumberOfBytesRead
    call ReadFile
    test rax, rax
    jz .erreur_systeme

    ; Absorption tls13-03 (Q2, I1)
    mov rcx, rsp      ; contexte SHA
    mov rdx, rsp      ; données
    add rdx, 112      ; Décalage pour le tampon après le contexte SHA
    mov r8, r12       ; longueur
    call tls13_03     ; tls13-03 absorbe les données

    ; Mise à jour des compteurs
    add r15, r12
    sub r14, r12
    jnz .boucle_fenetre

    ; Finalisation tls13-04 (Q2, I1)
    mov rcx, rsp      ; contexte SHA
    call tls13_04     ; tls13-04 écrit le condensé dans [rcx]

    ; Copie du résultat dans la sortie (Q1)
    mov rsi, rsp      ; condensé généré
    mov rdi, r13      ; destination
    mov rcx, 32       ; 32o
    rep movsb

    ; Succès (Q4)
    xor rax, rax      ; rax = 0
    jmp .fin

.erreur_session:
    mov rax, -4       ; E1
    jmp .fin

.erreur_hors_bornes:
    mov rax, -3       ; E2
    jmp .fin

.erreur_entree:
    mov rax, -5       ; E3
    jmp .fin

.erreur_systeme:
    ; E4 : GetLastError, sortie intacte (I4, I5)
    call GetLastError
    mov rax, -6       ; E4
