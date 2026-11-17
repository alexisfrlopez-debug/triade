.boucle_fenetre:
    ; Calcul de la taille de la fenêtre (I3)
    mov r12, CUMUL_FENETRE
    cmp r14, r12
    cmovb r12, r14   ; r12 = min(r14, CUMUL_FENETRE)

le geste : remplacer `cmova` par `cmovb` pour calculer le minimum.