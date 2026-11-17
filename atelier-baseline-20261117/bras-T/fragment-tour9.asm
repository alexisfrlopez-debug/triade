```
    ; Sauvegarde des registres non volatils (D7/D35)
    push rbp
    push rbx
    push r12
    push r13
    push r14
    push r15

    ; LE CADRE : sub rsp, 0xc0 AVANT les préconditions
    sub rsp, 0xc0
    ; Espace d'ombre pour les appelés (32o) à rsp+0x00
    ; Contexte SHA (112o) à rsp+0x40
    ; Créneau octets lus (32o) à rsp+0xB0

    ; Préconditions (P1, P2, P3, P4)
    mov r15, rcx      ; r15 = offset
    mov r14, rdx      ; r14 = length
    mov r13, r8       ; r13 = sortie

    ; E1 : session fermée (P1)
    lea rbx, [rip + 0x9ba9]
    cmp qword ptr [rbx + 528], -1
    je .erreur_session

    ; E2 : gamme hors bornes (P3)
    mov rax, rcx
    add rax, rdx
    jc .erreur_hors_bornes
    cmp rax, qword ptr [rbx + 520]
    ja .erreur_hors_bornes

    ; E3 : sortie inutilisable (P4)
    test r13, r13
    jz .erreur_entree

    ; Cas particulier : gamme vide (Q3)
    test r14, r14
    jz .vide

    ; Initialisation tls13-01 (Q2, I1)
    ; Le contexte SHA est déjà à rsp+0x40
    mov rcx, rsp
    add rcx, 0x40
    call tls13_01     ; tls13-01 initialise le contexte sur [rcx]

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
    call tls13_03     ; tls13-03 absorbe les données

    ; Mise à jour des compteurs
    add r15, r12
    sub r14, r12
    jnz .boucle_fenetre

    ; Finalisation tls13-04 (Q2, I1)
    mov rcx, rsp
    add rcx, 0x40     ; Pointeur vers le contexte SHA
    call tls13_04     ; tls13-04 écrit le condensé dans [rcx]

    ; Copie du résultat dans la sortie (Q1)
    mov rsi, rsp
    add rsi, 0x40     ; condensé généré
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
    call qword ptr [rip + IAT_GetLastError]
    mov rax, -6       ; E4
    ; Le condensé n'est pas écrit (sortie intacte, Q1 préservé)
    jmp .fin

.vide:
    ; Cas vide : écrire le vecteur FIPS (Q3)
    mov rdi, r13      ; destination
    mov rsi, vecteur_vide ; source (e3b0c442...)
    mov rcx, 32
    rep movsb
    xor rax, rax      ; Q4
    jmp .fin

.fin:
    ; Restauration des registres non volatils (D7/D35)
    add rsp, 0xc0
    pop r15
    pop r14
