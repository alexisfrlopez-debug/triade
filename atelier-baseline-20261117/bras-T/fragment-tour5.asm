    push r13
    push r14
    push r15

    ; Préconditions (P1, P2, P3, P4)
    mov r15, rcx      ; r15 = offset
    mov r14, rdx      ; r14 = length
    mov r13, r8       ; r13 = sortie

    ; E1 : session fermée (P1)
    test rdi, rdi
    jz .erreur_session

    ; E2 : gamme hors bornes (P3)
    ; (Supposition : la taille du fichier est accessible via un registre/mémoire externe non spécifié ici)
    ; cmp r15, [taille_fichier]  ; hypothétique
    ; jg .erreur_hors_bornes
    ; add r14, r15
    ; cmp r14, [taille_fichier]
    ; jg .erreur_hors_bornes

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
