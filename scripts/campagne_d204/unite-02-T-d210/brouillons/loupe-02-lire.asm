; loupe-02-lire × bras T — l'it3 RE-POSÉE (la reprise de l'atelier d210, le 17/11 au soir)
; LA PERTE NOMMÉE : l'it3 vécue périt au recyclage du bac (NOTE-REPRISE-ATELIER.txt) ;
;   le présent re-posé reconstruit LA STRUCTURE DE FAMILLE TELLE QUE CONSIGNÉE à
;   l'Entrée 335 : le cadre par le lea du plan, le décalage sauvé en r12, le
;   remplissage au +552, l'ombre autour des appels, le journal par le lea 0xe4a0 —
;   et PORTE les TROIS FAUTES NOMMÉES de l'it3 (le tour suivant par la rig les guérit) :
;   le compteur ReadFile lit rax (le retour de SetFilePointerEx, pas le remplissage) ;
;   le r9/ombre hors de l'endroit juste ; la destination du recouvrement hors du +568.
; LE DÉBORDEMENT DU SLOT (331 > 320 à l'it1) demeure NOMMÉ — le compactage au tour suivant.
; slot RVA 0x4240, taille 320 octets · ABI msx64 · IAT D161 : SetFilePointerEx, ReadFile, GetLastError
    push rbx
    push r12
    push r13
    push r14
    sub rsp, 0x28
    lea rbx, [rip + CADRE]
    cmp qword ptr [rbx + 528], -1
    je .refus_session
    test rcx, 0xf
    jne .refus_entree
    mov r12, rcx
    cmp r12, qword ptr [rbx + 520]
    jae .refus_bornes
    mov r13, qword ptr [rbx + 520]
    sub r13, r12
    cmp r13, 384
    jbe .rempli
    mov r13d, 384
.rempli:
    mov dword ptr [rbx + 552], r13d
    mov rcx, qword ptr [rbx + 528]
    mov rdx, r12
    xor r8d, r8d
    xor r9d, r9d
    call qword ptr [rip + IAT_SETFILEPOINTEREX]
    test eax, eax
    jz .refus_systeme
    mov rcx, qword ptr [rbx + 528]
    lea rdx, [rbx + 568]
    mov r8, r13
    mov qword ptr [rsp + 0x20], 0
    mov qword ptr [rsp], 0
    lea r9, [rsp + 0x20]
    call qword ptr [rip + IAT_READFILE]
    test eax, eax
    jz .refus_systeme
    lea r14, [rip + JOURNAL]
    xor ecx, ecx
.recouvre:
    cmp ecx, dword ptr [r14 + 4096]
    jae .recouvre_fin
    mov rax, rcx
    shl rax, 4
    mov rdx, qword ptr [r14 + rax]
    cmp rdx, r12
    jb .recouvre_suivant
    mov r8, r12
    add r8, r13
    cmp rdx, r8
    jae .recouvre_suivant
    sub rdx, r12
    mov al, byte ptr [r14 + rax + 8]
    mov byte ptr [rbx + rdx + 568], al
    inc ecx
    jmp .recouvre
.recouvre_suivant:
    inc ecx
    jmp .recouvre
.recouvre_fin:
    xor eax, eax
    jmp .sortie
.refus_session:
    push -4
    pop rax
    nop
    nop
    jmp .sortie
.refus_entree:
    push -5
    pop rax
    nop
    nop
    jmp .sortie
.refus_bornes:
    push -3
    pop rax
    nop
    nop
    jmp .sortie
.refus_systeme:
    call qword ptr [rip + IAT_GETLASTERROR]
    mov dword ptr [rbx + 552], 0
    push -6
    pop rax
    nop
    nop
    jmp .sortie
.sortie:
    add rsp, 0x28
    pop r14
    pop r13
    pop r12
    pop rbx
    ret
