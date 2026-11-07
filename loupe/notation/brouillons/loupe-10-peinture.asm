; loupe-10 · peinture : WM_PAINT, l'unique peintre · spec loupe-10:R1
; L'ORDRE DU GESTE : BeginPaint (E1 : le DC nul → -6 SANS EndPaint, RIEN
; peint) → LA POLICE mesurée UNE fois (ANSI_FIXED_FONT, GetTextMetricsW →
; METRIQUES char_w/ligne_h, bit 0 du drapeau ; E2 : l'échec → EndPaint QUAND
; MÊME — le contexte se rend TOUJOURS — puis -6) → GetClientRect À CHAQUE
; peinture (I2 : la fenêtre peut rétrécir ; lignes_affichables = (cy −
; MARGE_Y) / ligne_h, posée à METRIQUES.lignes — l'ascenseur honnête) →
; LA COMPOSITION (l'ECRAN 2320 o remis VIERGE — jamais une ligne fantôme ;
; l'entête 65 o du plan ; la grille par loupe-08, G = min(24,
; ceil(remplissage/16), lignes_affichables − 3) — la barre ANCRÉE AU BAS
; cède sa place, le panneau d'empreintes demeure TOUJOURS visible : LA
; LECTURE DU GESTE (c), l'oracle la juge) → LA PEINTURE (l'entête, la
; grille à MARGE_Y + (i+1)·ligne_h, la barre à cy−2·ligne_h / cy−ligne_h,
; LA CELLULE ACTIVE en inverse EXPLICITE blanc-sur-noir puis restaurée —
; chaque Set rend l'ancienne couleur, aucune couleur par défaut devinée)
; → EndPaint. L'EXPANSION latin-1 octet→mot EXACTE (I4 : jamais un octet
; signé).
; LE CADRE RBP : les sous-routines locales (.chaine/.chemin16/.hex8/
; .hex_octets/.dec/.peindre) partagent le cadre du bloc — chaque local à
; son déplacement RBP STABLE à travers les appels internes ; le 5e
; argument des TextOutW appelés DEPUIS les sous-routines vit à [rsp+0x20]
; dans la zone libre du bas — aucun local n'y vit, jamais un clobber.
; LA BARRE-ÉTAT (la ligne 1, 160 o @ECRAN+2000) : mode MESSAGE → le
; tampon de la saisie (le refus nommé) ; mode ALLER/CHERCHER → le libellé
; du plan + le tampon ; mode RIEN + session → « Loupe 0.1.0-dev.1 - <chemin>
; · <taille> o · curseur 0xNNNNNNNN · MODIFIÉ » (le chemin UTF-16 →
; latin-1, le point hors table ; la taille en DÉCIMAL ; le curseur en 8
; chiffres MAJUSCULES — la table HEX) ; mode RIEN + vide → l'usage.
; LE PANNEAU (la ligne 2, 160 o @ECRAN+2160) : « md5 <32 hex minuscules>
; · sha256 <64 hex minuscules> » + « * » si la marque sale (les empreintes
; du DISQUE — I3) ; « - » sans session. La composition est PURE LECTURE
; d'état (I5) ; rax = 0 (Q4).
; LE CADRE (rbp, après sub rsp, 0x198) : zone libre [rsp,+0x28) · ARGS8
; [rbp-0x178] · PS 0x48 [rbp-0x170] · TM 0x40 [rbp-0x128] · RECT 0x10
; [rbp-0xE8] · x/y [rbp-0xD8/-0xD4] · G [rbp-0xD0] · lignes [rbp-0xCC] ·
; EXPR 0xA0 [rbp-0xC8] · DIGITS [rbp-0x28] (à reculons depuis rbp-8)
push rbx
push rdi
push rsi
push r12
push r13
push r14
push r15
push rbp
mov rbp, rsp
sub rsp, 0x198
mov r14, rcx
lea rbx, [rip + CADRE]
lea r12, [rip + ECRAN]
; ============================ LA PEINTURE S'OUVRE (E1) =======================
mov rcx, r14
lea rdx, [rbp - 0x170]
call qword ptr [rip + IAT_BEGINPAINT]
test rax, rax
jz .refus_begin
mov r13, rax
; ============================ LA POLICE (UNE fois, Q2) =======================
lea rax, [rip + METRIQUES]
test dword ptr [rax + 12], 1
jnz .police_la
mov rcx, 13
call qword ptr [rip + IAT_GETSTOCKOBJECT]
test rax, rax
jz .avorte_police
mov r15, rax
mov rcx, r13
mov rdx, r15
call qword ptr [rip + IAT_SELECTOBJECT]
mov rcx, r13
lea rdx, [rbp - 0x128]
call qword ptr [rip + IAT_GETTEXTMETRICSW]
test eax, eax
jz .avorte_police
lea rcx, [rip + METRIQUES]
mov eax, dword ptr [rbp - 0x128]
mov dword ptr [rcx + 4], eax
mov eax, dword ptr [rbp - 0x114]
mov dword ptr [rcx], eax
or dword ptr [rcx + 12], 1
.police_la:
; ============================ LE CLIENT (à CHAQUE peinture, I2) ==============
mov rcx, r14
lea rdx, [rbp - 0xE8]
call qword ptr [rip + IAT_GETCLIENTRECT]
mov ecx, dword ptr [rbp - 0xDC]
sub ecx, dword ptr [rbp - 0xE4]
sub ecx, 8
jbe .client_zero
lea rdx, [rip + METRIQUES]
mov r9d, dword ptr [rdx + 4]
mov eax, ecx
xor edx, edx
div r9d
jmp .client_div
.client_zero:
xor eax, eax
.client_div:
mov dword ptr [rbp - 0xCC], eax
lea rcx, [rip + METRIQUES]
mov dword ptr [rcx + 8], eax
; ============================ LA COMPOSITION (Q1) ============================
xor eax, eax
.raz:
mov byte ptr [r12 + rax], 0
inc rax
cmp rax, 2320
jb .raz
lea rsi, [rip + ENTETE]
lea rdi, [r12]
mov ecx, 65
.entete_copie:
mov al, byte ptr [rsi]
mov byte ptr [rdi], al
inc rsi
inc rdi
dec ecx
jnz .entete_copie
mov byte ptr [r12 + 65], 0
cmp qword ptr [rbx + 528], -1
je .grille_zero
mov eax, dword ptr [rbx + 552]
test eax, eax
jz .grille_zero
add eax, 15
shr eax, 4
cmp eax, 24
jbe .grille_remplie
mov eax, 24
.grille_remplie:
mov edx, dword ptr [rbp - 0xCC]
sub edx, 3
jle .grille_zero
cmp eax, edx
jbe .grille_G
mov eax, edx
jmp .grille_G
.grille_zero:
xor eax, eax
.grille_G:
mov dword ptr [rbp - 0xD0], eax
xor r15d, r15d
.grille_boucle:
cmp r15d, dword ptr [rbp - 0xD0]
jae .grille_fin
mov r10, r15
shl r10, 4
lea rcx, [rbx + r10 + 568]
mov edx, dword ptr [rbx + 552]
sub edx, r10d
cmp edx, 16
jbe .grille_len
mov edx, 16
.grille_len:
mov r8d, r15d
imul r8d, r8d, 80
lea r8, [r12 + r8 + 80]
mov r9, qword ptr [rbx + 536]
add r9, r10
call LOUPE08
inc r15
jmp .grille_boucle
.grille_fin:
; — la barre-état : la ligne 1 @ECRAN+2000 —
lea rdi, [r12 + 2000]
lea rax, [rip + SAISIE]
mov eax, dword ptr [rax]
cmp eax, 3
je .barre_message
cmp eax, 1
je .barre_aller
cmp eax, 2
je .barre_chercher
cmp qword ptr [rbx + 528], -1
je .barre_usage
lea rsi, [rip + L_BALISE]
call .chaine
lea rsi, [rip + L_TIRET]
call .chaine
mov rsi, rbx
call .chemin16
lea rsi, [rip + L_MID]
call .chaine
mov rax, qword ptr [rbx + 520]
call .dec
lea rsi, [rip + L_OCT]
call .chaine
mov rax, qword ptr [rbx + 544]
call .hex8
cmp dword ptr [rbx + 556], 0
je .barre1_fin
lea rsi, [rip + L_MODIF]
call .chaine
jmp .barre1_fin
.barre_usage:
lea rsi, [rip + L_USAGE]
call .chaine
jmp .barre1_fin
.barre_message:
lea rsi, [rip + SAISIE]
add rsi, 12
call .chaine
jmp .barre1_fin
.barre_aller:
lea rsi, [rip + L_ALLER]
call .chaine
lea rsi, [rip + SAISIE]
add rsi, 12
call .chaine
jmp .barre1_fin
.barre_chercher:
lea rsi, [rip + L_CHERCHER]
call .chaine
lea rsi, [rip + SAISIE]
add rsi, 12
call .chaine
.barre1_fin:
mov byte ptr [rdi], 0
; — LE PANNEAU : la ligne 2 @ECRAN+2160 —
lea rdi, [r12 + 2160]
cmp qword ptr [rbx + 528], -1
je .panneau_vide
lea rsi, [rip + L_MD5]
call .chaine
lea rsi, [rip + EMPREINTES]
mov ecx, 16
lea rdx, [rip + HEXL]
call .hex_octets
lea rsi, [rip + L_SHA]
call .chaine
lea rsi, [rip + EMPREINTES]
add rsi, 16
mov ecx, 32
lea rdx, [rip + HEXL]
call .hex_octets
cmp dword ptr [rbx + 556], 0
je .panneau_fin
lea rsi, [rip + L_AST]
call .chaine
jmp .panneau_fin
.panneau_vide:
lea rsi, [rip + L_VIDE]
call .chaine
.panneau_fin:
mov byte ptr [rdi], 0
; ============================ LA PEINTURE DES LIGNES (Q2) ====================
lea rsi, [r12]
mov edx, 8
call .peindre
xor r15d, r15d
.peint_grille:
cmp r15d, dword ptr [rbp - 0xD0]
jae .peint_grille_fin
mov r8d, r15d
imul r8d, r8d, 80
lea rsi, [r12 + r8 + 80]
lea rcx, [rip + METRIQUES]
mov edx, dword ptr [rcx + 4]
mov eax, r15d
inc eax
imul eax, edx
add eax, 8
mov r10d, eax
add r10d, edx
cmp r10d, dword ptr [rbp - 0xDC]
ja .peint_grille_suivant
mov edx, eax
call .peindre
.peint_grille_suivant:
inc r15
jmp .peint_grille
.peint_grille_fin:
lea rcx, [rip + METRIQUES]
mov edx, dword ptr [rcx + 4]
mov r10d, dword ptr [rbp - 0xDC]
lea r11d, [rdx + rdx]
cmp r10d, r11d
jbe .barre_saute
mov r11d, r10d
sub r11d, edx
sub r11d, edx
lea rsi, [r12 + 2000]
mov edx, r11d
call .peindre
mov r11d, dword ptr [rbp - 0xDC]
lea rcx, [rip + METRIQUES]
mov edx, dword ptr [rcx + 4]
sub r11d, edx
lea rsi, [r12 + 2160]
mov edx, r11d
call .peindre
.barre_saute:
; ============================ LA CELLULE ACTIVE (Q3) =========================
cmp qword ptr [rbx + 528], -1
je .cellule_fin
mov rax, qword ptr [rbx + 544]
sub rax, qword ptr [rbx + 536]
mov ecx, dword ptr [rbx + 552]
cmp rax, rcx
jae .cellule_fin
mov r11, rax
shr r11, 4
mov r10, rax
and r10, 15
cmp r11d, dword ptr [rbp - 0xD0]
jae .cellule_fin
lea rcx, [rip + METRIQUES]
mov edx, dword ptr [rcx]
lea eax, [r10 + r10*2 + 10]
cmp r10d, 8
jb .cellule_col
inc eax
.cellule_col:
imul eax, edx
add eax, 8
mov dword ptr [rbp - 0xD8], eax
mov edx, dword ptr [rcx + 4]
mov r8d, r11d
inc r8d
imul r8d, edx
add r8d, 8
mov dword ptr [rbp - 0xD4], r8d
mov rcx, r13
mov edx, 0x00ffffff
call qword ptr [rip + IAT_SETTEXTCOLOR]
mov rcx, r13
xor edx, edx
call qword ptr [rip + IAT_SETBKCOLOR]
mov r8d, r11d
imul r8d, r8d, 80
lea rsi, [r12 + r8 + 80]
lea r9d, [r10 + r10*2 + 10]
cmp r10d, 8
jb .cellule_pos
inc r9d
.cellule_pos:
add rsi, r9
movzx eax, byte ptr [rsi]
mov word ptr [rbp - 0xC8], ax
movzx eax, byte ptr [rsi + 1]
mov word ptr [rbp - 0xC6], ax
mov rcx, r13
mov edx, dword ptr [rbp - 0xD8]
mov r8d, dword ptr [rbp - 0xD4]
lea r9, [rbp - 0xC8]
mov dword ptr [rsp + 0x20], 2
call qword ptr [rip + IAT_TEXTOUTW]
mov rcx, r13
xor edx, edx
call qword ptr [rip + IAT_SETTEXTCOLOR]
mov rcx, r13
mov edx, 0x00ffffff
call qword ptr [rip + IAT_SETBKCOLOR]
.cellule_fin:
mov rcx, r14
lea rdx, [rbp - 0x170]
call qword ptr [rip + IAT_ENDPAINT]
xor eax, eax
jmp .sortie
.refus_begin:
call qword ptr [rip + IAT_GETLASTERROR]
mov eax, -6
jmp .sortie
.avorte_police:
mov rcx, r14
lea rdx, [rbp - 0x170]
call qword ptr [rip + IAT_ENDPAINT]
call qword ptr [rip + IAT_GETLASTERROR]
mov eax, -6
.sortie:
lea rsp, [rbp]
pop rbp
pop r15
pop r14
pop r13
pop r12
pop rsi
pop rdi
pop rbx
ret
; ============================ LES SOUS-ROUTINES LOCALES ======================
.chaine:
mov al, byte ptr [rsi]
test al, al
jz .chaine_fin
mov byte ptr [rdi], al
inc rsi
inc rdi
jmp .chaine
.chaine_fin:
ret
.chemin16:
movzx eax, word ptr [rsi]
test eax, eax
jz .chemin16_fin
cmp eax, 0xff
ja .chemin16_point
jmp .chemin16_poser
.chemin16_point:
mov al, 0x2e
.chemin16_poser:
mov byte ptr [rdi], al
add rsi, 2
inc rdi
jmp .chemin16
.chemin16_fin:
ret
.hex8:
lea r11, [rip + HEX]
mov r10, rax
mov r9d, 28
.hex8_boucle:
mov rax, r10
mov ecx, r9d
shr rax, cl
and eax, 0xf
movzx eax, byte ptr [r11 + rax]
mov byte ptr [rdi], al
inc rdi
sub r9d, 4
cmp r9d, 0
jge .hex8_boucle
ret
.hex_octets:
movzx eax, byte ptr [rsi]
mov r8d, eax
shr r8d, 4
and eax, 0xf
movzx r8d, byte ptr [rdx + r8]
mov byte ptr [rdi], r8b
inc rdi
movzx r8d, byte ptr [rdx + rax]
mov byte ptr [rdi], r8b
inc rdi
inc rsi
dec ecx
jnz .hex_octets
ret
.dec:
lea r9, [rbp - 8]
xor r11d, r11d
mov r10d, 10
.dec_boucle:
xor edx, edx
div r10
add dl, 0x30
dec r9
mov byte ptr [r9], dl
inc r11d
test rax, rax
jnz .dec_boucle
.dec_copie:
mov al, byte ptr [r9]
mov byte ptr [rdi], al
inc r9
inc rdi
dec r11d
jnz .dec_copie
ret
.peindre:
mov dword ptr [rbp - 0xD4], edx
xor ecx, ecx
.peindre_compte:
cmp byte ptr [rsi + rcx], 0
je .peindre_expanse
inc ecx
jmp .peindre_compte
.peindre_expanse:
xor r8d, r8d
.peindre_goutte:
movzx eax, byte ptr [rsi + r8]
mov word ptr [rbp + r8*2 - 0xC8], ax
inc r8
cmp r8d, ecx
jb .peindre_goutte
mov dword ptr [rbp - 0xD8], ecx
mov rcx, r13
mov edx, 8
mov r8d, dword ptr [rbp - 0xD4]
lea r9, [rbp - 0xC8]
mov eax, dword ptr [rbp - 0xD8]
mov dword ptr [rsp + 0x20], eax
call qword ptr [rip + IAT_TEXTOUTW]
ret
