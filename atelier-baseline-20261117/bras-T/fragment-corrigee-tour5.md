    push r13
    push r14
    push r15

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
    sub rsp, 112      ; Espace pour le contexte SHA (112o)
    call tls13_01     ; tls13-01 initialise le contexte sur rsp

.boucle_fenetre:
le geste : remplacer le test `test rdi, rdi` par la lecture de la session dans la zone d'état et la vérification de la condition de dépassement de la taille du fichier.