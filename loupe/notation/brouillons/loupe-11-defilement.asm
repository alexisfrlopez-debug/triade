; loupe-11 · défilement : la molette et l'ascenseur · LA RÉVISION R2 (l'Entrée 207 — l'AUDIT D'ABI du build a
; NOMMÉ L'AXE : le cadre 5 pushes + 0x38 laissait la pile ≡8 AU call — le VRAI
; user32 (SSE) peut fautter là où l'émulation passe ; 0x38 → 0x40, la pile alignée
; 16 — la convention, jamais la pièce)
; LE PAS (Q1) : SB_LIGNE_HAUT/BAS = ±16 o (une ligne) ; SB_PAGE_HAUT/BAS =
; ±352 o (22 lignes — la grille moins les deux de repère) ; SB_POIGNEE/
; SB_POIGNEE_COURSE = la position demandée × 16 (GetScrollInfo au
; SIF_TRACKPOS — l'ascenseur parle en LIGNES, le cadre en octets) ;
; WM_MOUSEWHEEL = −(delta/120) × 48 o (TROIS lignes par cran, le delta
; signé — le cran avant remonte, la convention Win32).
; LA BORNE (Q2) : vue' = clamp(vue ± pas) dans [0, vue_max] — vue_max =
; aligne16_sup(max(0, taille − 384)) : LA DERNIÈRE fenêtre montre le
; DERNIER octet ; les fichiers ≤ 384 o ne défilent pas (vue = 0 — le clamp
; fait le repli, la molette au bout ne relit rien).
; LE GESTE (Q3) : vue' == vue → RIEN (l'OS au bout reste calme — les
; appels comptés) ; sinon LOUPE-02 LA PREMIÈRE (la lecture au décalage
; AVANT l'engagement : le refus système relayé laisse la vue inchangée,
; le geste abandonné proprement — le miroir de E1), puis la vue COMMITÉE,
; l'ascenseur TOUJOURS synchrone (SetScrollInfo min 0 · max vue_max/16 ·
; page les lignes visibles · pos vue'/16 — I3 : jamais une position
; affichée divergente du cadre), InvalidateRect.
; WM_SIZE (Q4) : les lignes visibles recalculées de lParam (cy /
; ligne_h — LES MÉTRIQUES DE LOUPE-10 ; la garde ligne_h nulle : la
; police pas encore mesurée, lignes = 0 — JAMAIS une division par zéro),
; l'ascenseur remis, l'écran invalidé — aucune ligne fantôme.
; E1 : GetScrollInfo en échec → -6 (GetLastError consigné), le geste de
; poignée ABANDONNÉ proprement (vue inchangée, l'ascenseur non touché).
; SANS SESSION (Q5) : rax = 0 SANS AUCUN effet. Le clamp PRÉCÈDE la
; lecture (I2 : jamais une lecture hors fichier) ; l'alignement 16
; inviolable (I1) ; le curseur, le journal, les empreintes INTACTS (I4).
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x40
mov r14, rcx
lea rbx, [rip + CADRE]
cmp qword ptr [rbx + 528], -1
je .sans_session
mov r15, rdx
; — vue_max = aligne16_sup(max(0, taille − 384)) : LA DERNIÈRE FENÊTRE —
mov rax, qword ptr [rbx + 520]
sub rax, 384
jbe .vmax_zero
add rax, 15
and rax, -16
jmp .vmax_fin
.vmax_zero:
xor eax, eax
.vmax_fin:
mov r13, rax
; — le message —
cmp r15, 5
je .taille
cmp r15, 0x115
je .vscroll
cmp r15, 0x20a
je .molette
xor eax, eax
jmp .sortie
; ============================ WM_SIZE (Q4) ====================================
.taille:
mov eax, r9d
shr eax, 16
lea rdx, [rip + METRIQUES]
mov ecx, dword ptr [rdx + 4]
test ecx, ecx
jz .taille_zero
xor edx, edx
div ecx
jmp .taille_pose
.taille_zero:
xor eax, eax
.taille_pose:
lea rdx, [rip + METRIQUES]
mov dword ptr [rdx + 8], eax
jmp .ascenseur_remis
; ============================ WM_VSCROLL (Q1) =================================
.vscroll:
mov eax, r8d
and eax, 0xffff
cmp eax, 0
je .pas_ligne_haut
cmp eax, 1
je .pas_ligne_bas
cmp eax, 2
je .pas_page_haut
cmp eax, 3
je .pas_page_bas
cmp eax, 4
je .poignee
cmp eax, 5
je .poignee
xor eax, eax
jmp .sortie
.pas_ligne_haut:
mov r12d, -16
jmp .pas_applique
.pas_ligne_bas:
mov r12d, 16
jmp .pas_applique
.pas_page_haut:
mov r12d, -352
jmp .pas_applique
.pas_page_bas:
mov r12d, 352
jmp .pas_applique
.poignee:
mov dword ptr [rsp], 28
mov dword ptr [rsp + 4], 0x10
mov dword ptr [rsp + 8], 0
mov dword ptr [rsp + 12], 0
mov dword ptr [rsp + 16], 0
mov dword ptr [rsp + 20], 0
mov dword ptr [rsp + 24], 0
mov rcx, r14
mov edx, 1
mov r8, rsp
call qword ptr [rip + IAT_GETSCROLLINFO]
test eax, eax
jz .refus_gsi
mov eax, dword ptr [rsp + 24]
shl eax, 4
mov r12, rax
jmp .borne
.pas_applique:
movsxd r12, r12d
add r12, qword ptr [rbx + 536]
; — LA BORNE (Q2) : le clamp —
.borne:
cmp r12, 0
jge .borne_haut
xor r12d, r12d
.borne_haut:
cmp r12, r13
jbe .borne_fin
mov r12, r13
.borne_fin:
; ============================ LE GESTE (Q3) ===================================
mov rax, qword ptr [rbx + 536]
cmp r12, rax
je .rien
mov rcx, r12
call LOUPE02
test eax, eax
jnz .sortie
mov qword ptr [rbx + 536], r12
; ============================ L'ASCENSEUR REMIS (I3) ==========================
.ascenseur_remis:
mov dword ptr [rsp], 28
mov dword ptr [rsp + 4], 7
mov dword ptr [rsp + 8], 0
mov rax, r13
shr rax, 4
mov dword ptr [rsp + 12], eax
lea rax, [rip + METRIQUES]
mov eax, dword ptr [rax + 8]
mov dword ptr [rsp + 16], eax
mov rax, qword ptr [rbx + 536]
shr rax, 4
mov dword ptr [rsp + 20], eax
mov dword ptr [rsp + 24], 0
mov rcx, r14
mov edx, 1
mov r8, rsp
mov r9d, 1
call qword ptr [rip + IAT_SETSCROLLINFO]
mov rcx, r14
xor edx, edx
mov r8d, 1
call qword ptr [rip + IAT_INVALIDATERECT]
xor eax, eax
jmp .sortie
; ============================ WM_MOUSEWHEEL (Q1) ==============================
.molette:
mov eax, r8d
shr eax, 16
movsx eax, ax
mov ecx, 120
cdq
idiv ecx
imul eax, eax, 48
neg eax
movsxd r12, eax
add r12, qword ptr [rbx + 536]
jmp .borne
; ============================ LES REPLIS NOMMÉS ===============================
.rien:
xor eax, eax
jmp .sortie
.sans_session:
xor eax, eax
jmp .sortie
.refus_gsi:
call qword ptr [rip + IAT_GETLASTERROR]
mov eax, -6
.sortie:
add rsp, 0x40
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
