; loupe-08-ligne × bras T — la notation de campagne D210 (l'unité 02)
; LA CONSTRUCTION PAR LA RIG : spec → notation → correctif 1 (SYNTAXE : la table
;   au plan R_HEX par le lea, les formes ptr) → oracle-depuis-I → correctifs
;   2-6 (le faisceau STRUCTUREL : le plan VOLATIL — les sept registres rax, rcx,
;   rdx, r8, r9, r10, r11, aucun push, la pile jamais touchée ; les deux espaces ;
;   le lea UNE fois ; l'extraction par les deux nibbles ; Q4 rax remis) — 100 %
;   log-api au journal-tokens-d210.jsonl ; le geste MÉCANIQUE du labo nommé :
;   la remappe bijective r12/r13/r14/r15 → r8/rdx/r9d/rax (la phase 1) et la
;   normalisation de largeur cmp r9d, rdx → edx (la classe registre 32/64).
; slot RVA 0x49C0, taille 320 octets · ABI msx64 · AUCUNE entrée IAT (la feuille
;   pure) · la table hexa « 0123456789ABCDEF » du plan (R_HEX 0x2050, lea + HEX)

; --- Constantes et étiquettes locales ---

; --- Début du code ---

    ; --- Vérifications préalables (E1, E2, E3) ---
    test rcx, rcx                    ; P1 : rcx est-il nul ?
    jz .erreur_entree                 ; Si oui, E3
    test r8, r8                      ; P3 : r8 est-il nul ?
    jz .erreur_entree                 ; Si oui, E3
    cmp rdx, 1                       ; P2 : longueur < 1 ?
    jl .erreur_entree                 ; Si oui, E1
    cmp rdx, 16                      ; P2 : longueur > 16 ?
    jg .erreur_entree                 ; Si oui, E2

    ; --- le plan volatile : rcx la source, rdx la longueur, r8 le curseur, r10 le décalage, r11 la table, rax/r9 le chantier ---
    ; --- Initialisation des registres et pointeurs ---
    mov r10, r9                      ; r10 = décalage (pour écriture)
    lea r11, [rip + HEX]          ; r11 = LA TABLE, posée UNE SEULE FOIS

    ; --- Écriture du décalage hexadécimal (8 chiffres, grand-boutiste) ---
    mov r9d, 8                       ; Compteur pour 8 chiffres hex
.writedec_loop:
    mov rax, r10                     ; Copie du décalage
    shr rax, 28                      ; Extraction du NIBBLE HAUT (grand-boutiste)
    and rax, 0xF                     ; Masque pour le chiffre
    mov al, [r11 + rax]             ; Conversion avec la table
    mov [r8], al                    ; Écriture du caractère hex
    inc r8                          ; Avancer dans la sortie
    shl r10, 4                       ; Décalage du décalage pour le prochain chiffre
    dec r9d                          ; Décrémenter le compteur
    jnz .writedec_loop               ; Boucler si 8 chiffres pas écrits

    ; --- Écriture de l'espacement initial ---
    mov word ptr [r8], 0x2020       ; Deux espaces
    add r8, 2

    ; --- Écriture des 16 groupes hexadécimaux (HH) ---
    xor r9d, r9d                    ; r9 = l'indice 0..15
.writ_hex_loop:
    ; Écriture du premier octet du groupe (si disponible)
    cmp r9d, edx                    ; Comparer l'indice et la longueur
    jae .write_group_space         ; Si indice >= longueur, sauter à l'écriture d'espace
    movzx eax, byte ptr [rcx + r9]  ; Lire l'octet source (rcx)
    mov r10d, eax                   ; Sauver l'octet source (r10)
    shr eax, 4                      ; Extraction du premier chiffre
    and r10d, 0xF                   ; Extraction du second chiffre
    movzx eax, byte ptr [r11 + rax] ; Conversion du premier chiffre
    movzx r10d, byte ptr [r11 + r10] ; Conversion du second chiffre
    mov [r8], al                    ; Écrire les deux caractères hex
    mov [r8 + 1], r10b
    jmp .after_group_write
.write_group_space:
    mov word ptr [r8], 0x2020       ; Deux espaces pour le groupe manquant
.after_group_write:
    add r8, 2                       ; Avancer dans la sortie

    ; Gestion de l'espace médian double
    inc r9d                         ; Incrémenter le compteur de groupes
    cmp r9d, 16                     ; Si 16 groupes écrits, finir
    jae .write_hex_done
    cmp r9d, 8                      ; Est-ce le 9ème groupe ?
    jne .write_single_space         ; Non, écrire un espace simple
    mov word ptr [r8], 0x2020       ; Oui, écrire un double espace
    add r8, 2
    jmp .next_hex_group
.write_single_space:
    mov byte ptr [r8], 0x20        ; Écrire un espace simple
    inc r8
.next_hex_group:
    jmp .writ_hex_loop               ; Boucler pour le prochain groupe

.write_hex_done:
    ; --- Écriture de l'espacement final et du miroir ASCII ---
    mov word ptr [r8], 0x2020       ; Deux espaces
    add r8, 2

    ; --- Écriture du miroir ASCII (16 caractères) ---
    xor r9d, r9d                    ; r9 = l'indice 0..15
.writ_ascii_loop:
    cmp r9d, edx                    ; Comparer le compteur et la longueur
    jae .write_ascii_space         ; Si compteur >= longueur, sauter à l'écriture d'espace
    movzx eax, byte ptr [rcx + r9]  ; Lecture de la source (rcx)
    cmp al, 0x20                     ; Caractère imprimable ?
    jl .write_dot                   ; Non, écrire un point
    cmp al, 0x7E                    ; Caractère imprimable ?
    jg .write_dot                   ; Non, écrire un point
    mov [r8], al                    ; Oui, écrire le caractère
    jmp .after_ascii_write
.write_dot:
    mov byte ptr [r8], 0x2E        ; Écrire le point de remplacement
.after_ascii_write:
    inc r9d                         ; Incrémenter le compteur de caractères
    jmp .next_ascii_char
.write_ascii_space:
    mov byte ptr [r8], 0x20        ; Écrire un espace pour le caractère manquant
    inc r9d                         ; l'indice s'incrémente AUSSI au chemin absent (le geste de la rig, tour 7)
    jmp .next_ascii_char
.next_ascii_char:
    inc r8                          ; Avancer dans la sortie
    cmp r9d, 16                     ; Boucler si 16 caractères pas écrits
    jb .writ_ascii_loop

    ; --- Écriture du NUL final et retour ---
    mov byte ptr [r8], 0            ; NUL final
    xor eax, eax                    ; rax = 0 au retour (Q4)
    ret
.erreur_entree:
    mov rax, -5                      ; Code d'erreur -5
    ret                              ; Rien écrit dans la sortie
