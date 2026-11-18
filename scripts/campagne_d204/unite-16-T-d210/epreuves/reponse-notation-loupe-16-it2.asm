```asm
; E1 session
    cmp qword [rbx + 528], -1
    jne .attente
    mov byte [r13 + 12], 'S' ; barre
    mov eax, -4
    jmp .epilogue

.attente:
    ; Q5 VK_SUPPR (0x08)
    cmp dil, 0x08
    jne .premier_chiffre
    ; E2 la cellule fantôme
    mov eax, [rbx + 552] ; remplissage
    mov ecx, [rbx + 544] ; curseur
    add eax, [rbx + 536] ; vue
    cmp ecx, eax
    jb .sauvegarde_octet
    mov byte [r13 + 12], 'F' ; barre
    mov eax, -3
    jmp .epilogue

.premier_chiffre:
    ; Q1 le premier chiffre
    cmp dil, '0'
    jb .attente
    cmp dil, '9'
    jbe .sauvegarde_premier
    cmp dil, 'a'
    jb .attente
    cmp dil, 'f'
    ja .attente
    sub dil, 20h ; a-f -> A-F

.sauvegarde_premier:
    mov r10d, eax ; SAUVE le premier
    jmp .attente

.second_chiffre:
    ; Q2 le second
    cmp dil, '0'
    jb .sauvegarde_octet
    cmp dil, '9'
    jbe .sauvegarde_octet
    cmp dil, 'A'
    jb .sauvegarde_octet
    cmp dil, 'F'
    ja .sauvegarde_octet
    sub dil, 20h ; A-F

.sauvegarde_octet:
    ; l'attente CONSOMMÉE avant tout contrôle
    mov eax, r10d ; le premier
    shl eax, 4
    or al, dil ; l'octet
    mov r15b, al ; l'octet

.sauvegarde_octet_suite:
    ; Q3 tampon[curseur − vue] = l'octet
    mov rdx, [rbx + 544] ; curseur
    sub rdx, [rbx + 536] ; vue
    mov [r13 + rdx], r15b ; tampon

    ; Q4 sale = 1, refus_quitter = 0, curseur +1 clampé à taille − 1
    mov byte [rbx + 556], 1 ; sale
    mov byte [rbx + 560], 0 ; refus_quitter
    mov eax, [rbx + 520] ; taille
    dec eax
    inc dword [rbx + 544] ; curseur +1
    cmp dword [rbx + 544], eax
    cmova dword [rbx + 544], eax ; clampé

    ; LA VUE SUIT
    ; V = lignes@METRIQUES+8 − 3 clampé [0, 24]
    mov rcx, [r12] ; HWND
    call qword ptr [rip + IAT_GETLINECOUNT]
    movsxd rax, eax
    lea rax, [rax - 3]
    xor edx, edx
    cmp rax, 24
    cmovbe rax, rdx
    movsxd rdx, eax ; V
    ; la vitrine [vue, vue + 16·V)
    ; si le curseur est dehors, la nouvelle vue = aligne16_inf(curseur − 176)
    ; clampée à aligne16_sup(taille − 384)
    mov eax, [rbx + 544] ; curseur
    cmp eax, [rbx + 536] ; vue
    jb .curseur_dedans
    cmp eax, [rbx + 536] ; vue
    jge .curseur_dehors
.curseur_dedans:
    cmp eax, [rbx + 536] ; vue
    jl .curseur_dehors
    add eax, rdx ; V
    cmp eax, [rbx + 536] ; vue
    jg .curseur_dehors
    jmp .vue_inchangee

.curseur_dehors:
    mov ecx, eax ; curseur
    sub ecx, 176
    and ecx, 0xFFFFFFF0 ; aligne16_inf
    mov eax, [rbx + 520] ; taille
    sub eax, 384
    and eax, 0xFFFFFFF0 ; aligne16_sup
    cmp ecx, eax
    cmova ecx, eax
    cmp ecx, [rbx + 536] ; vue
    je .vue_inchangee
    mov r15d, ecx ; la SAUVE
    mov eax, 1
    mov ecx, r15d ; la nouvelle vue
    call LOUPE02
    test eax, eax
    jnz .s InvalidateRect ; sortie SANS la poser
    mov [rbx + 536], r15d ; la vue du cadre la reçoit

.vue_inchangee:
    ; InvalidateRect (rcx = HWND, rdx = 0, r8d = 1)
    mov rcx, [r12] ; HWND
    xor edx, edx
    mov r8d, 1
    call qword ptr [rip + IAT_INVALIDATERECT]

.epilogue:
    ; l'épilogue rend tout non-volatil poussé
    pop r15
    pop r14
    pop r13
    pop rbx
    pop r12
    ret
```