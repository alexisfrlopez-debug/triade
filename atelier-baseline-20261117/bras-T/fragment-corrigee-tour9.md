```
    ; Initialisation tls13-01 (Q2, I1)
    ; Le contexte SHA est déjà à rsp+0x40
    mov rcx, rsp
    add rcx, 0x40
    call 0xc000       ; Appel direct à l'adresse du plan

.boucle_fenetre:
    ; Calcul de la taille de la fenêtre (I3)
    mov r12, CUMUL_FENETRE
    cmp r14, r12
    cmovb r12, r14   ; r12 = min(r14, CUMUL_FENETRE)
    ; Repositionnement du pointeur fichier (I4)
    mov rcx, qword ptr [rbx + 528] ; hFile depuis la zone d'état
    mov rdx, r15      ; lpDistanceToMove
    mov r8, NULL      ; lpNewFilePointer
    mov r9, NULL      ; lp_dw
    call qword ptr [rip + IAT_SetFilePointerEx]
    test rax, rax
    jz .erreur_systeme

    ; Lecture de la fenêtre (I3)
    mov rcx, qword ptr [rbx + 528] ; hFile depuis la zone d'état
    lea rdx, [rip + 0xbb06]       ; lpBuffer (adresse du tampon statique TAMPON_CUMUL)
    mov r8, r12                   ; nNumberOfBytesToRead
    mov r9, NULL                  ; lpNumberOfBytesRead
    call qword ptr [rip + IAT_ReadFile]
    test rax, rax
    jz .erreur_systeme

    ; Absorption tls13-03 (Q2, I1)
    mov rcx, rsp
    add rcx, 0x40     ; Pointeur vers le contexte SHA
    mov rdx, rsp      ; données
    add rdx, 0xB0     ; Pointeur vers les données lues
    mov r8, r12       ; longueur
    call 0xc240       ; Appel direct à l'adresse du plan

    ; Mise à jour des compteurs
    add r15, r12
    sub r14, r12
    jnz .boucle_fenetre

    ; Finalisation tls13-04 (Q2, I1)
    mov rcx, rsp
    add rcx, 0x40     ; Pointeur vers le contexte SHA
    call 0xc300       ; Appel direct à l'adresse du plan
```
le geste : remplacement des appels récursifs tls13_xx par les appels directs aux adresses du plan d'adressage (0xc000, 0xc240, 0xc300).