; loupe-12 · aller : la saisie hexadécimale à la barre, le refus nommé · spec loupe-12:R1
; L'OUVERTURE (Q1) : WM_KEYDOWN F5 ou WM_CHAR 0x07 (Ctrl+G — LE CODE DE
; CONTRÔLE, la voie WM_CHAR : aucune feuille GetKeyState au plan, l'état
; du clavier ne se sonde pas, le caractère ctrl-G EST le message) → mode
; ALLER, le tampon vide, la barre « ALLER (hexa) : » (peinte par loupe-10,
; le seul peintre) ; SANS SESSION (E3) → -4, la barre nomme « aucun
; fichier ouvert ».
; LA FRAPPE (Q2) : le gestionnaire PARTAGÉ (le RENVOI de loupe-14 : le
; tampon, la correction, l'échappée idem, jamais réécrit) : chiffre hexa →
; accumulé MAJUSCULE, au plus 8 chiffres en ALLER / 64 en CHERCHER (le 9e
; IGNORÉ proprement) ; VK_SUPPR retire le dernier ; VK_ECHAP annule TOUT
; proprement (mode = 0, rien arrivé) ; un message affiché (mode MESSAGE)
; est ACQUITTÉ par toute frappe.
; LE COMMIT ALLER (Q3) : le tampon VIDE ou non hexa → -5 « saisie mal
; formée » (E1) ; la valeur ≥ taille → -3 « hors bornes » (E2 — JAMAIS un
; saut silencieux) ; SINON le curseur = la valeur ET LA RÈGLE DE
; RECADRAGE : le curseur sorti de la fenêtre visible → vue =
; min(recadre(curseur), vue_max) — LA RÈGLE EXÉCUTABLE DU PLAN (la ligne
; active posée à la 12e, le bord sinon), loupe-02 LA PREMIÈRE (le refus
; système relayé, la vue inchangée — le miroir de loupe-11), mode = 0,
; InvalidateRect — LE SAUT EXACT.
; LE COMMIT CHERCHER (mode 2) : DÉLÉGUÉ à loupe-14 (hwnd, WM_CHAR,
; VK_RETURN) — le verdict relayé TEL QUEL.
; I1 : la barre n'est PAS un contrôle (aucun EDIT enfant — les frappes
; reviennent par la procédure) ; I2 : le tampon de vue, le journal, les
; empreintes INTACTS ; I3 : le curseur BORNÉ [0, taille−1] ; I4 :
; InvalidateRect la seule feuille IAT du bloc (le plan d'adressage fait
; foi — la barre est peinte par loupe-10) ; NOP, 0x90.
; LE MODE DU GESTE (c) : le champ porte QUATRE valeurs — 0 RIEN · 1 ALLER
; · 2 CHERCHER · 3 MESSAGE (aucune saisie + le refus nommé au tampon —
; le « mode = 0 » des E1/E3 se lit LA SAISIE FERMÉE : la barre nomme, la
; saisie n'écoute plus).
push rbx
push rdi
push rsi
push r12
push r13
push r14
push r15
sub rsp, 0x30
mov r12, rcx
lea rbx, [rip + CADRE]
cmp rdx, 0x100
je .touche
cmp rdx, 0x102
je .caract
xor eax, eax
jmp .sortie
; ============================ L'OUVERTURE (Q1, E3) ============================
.touche:
cmp r8d, 0x74
jne .rien
jmp .ouvrir
.caract:
cmp r8d, 0x07
je .ouvrir
lea rax, [rip + SAISIE]
mov eax, dword ptr [rax]
test eax, eax
jz .rien
cmp eax, 3
je .acquitter
cmp r8d, 0x0d
je .commit
cmp r8d, 0x1b
je .echappe
lea r14, [rip + SAISIE]
add r14, 12
xor r13d, r13d
.longueur:
cmp byte ptr [r14 + r13], 0
je .longueur_fin
inc r13d
cmp r13d, 79
jb .longueur
.longueur_fin:
cmp r8d, 0x08
je .corrige
mov eax, r8d
cmp eax, 0x61
jb .chiffre_maj
cmp eax, 0x66
ja .chiffre_maj
sub eax, 0x20
.chiffre_maj:
cmp eax, 0x30
jb .rien
cmp eax, 0x39
jbe .chiffre_hex
cmp eax, 0x41
jb .rien
cmp eax, 0x46
ja .rien
.chiffre_hex:
lea rdx, [rip + SAISIE]
mov edx, dword ptr [rdx]
cmp edx, 1
jne .borne_chercher
mov r15d, 8
jmp .borne_mode
.borne_chercher:
mov r15d, 64
.borne_mode:
cmp r13d, r15d
jae .rien
mov byte ptr [r14 + r13], al
mov byte ptr [r14 + r13 + 1], 0
jmp .rien
.corrige:
test r13d, r13d
jz .rien
mov byte ptr [r14 + r13 - 1], 0
jmp .rien
.echappe:
lea rax, [rip + SAISIE]
mov dword ptr [rax], 0
jmp .rien
.acquitter:
lea rax, [rip + SAISIE]
mov dword ptr [rax], 0
jmp .rien
.ouvrir:
cmp qword ptr [rbx + 528], -1
jne .ouvrir_session
lea rsi, [rip + L_SESSION]
call .message
mov eax, -4
jmp .sortie
.ouvrir_session:
lea rax, [rip + SAISIE]
mov dword ptr [rax], 1
mov dword ptr [rax + 4], 0
mov dword ptr [rax + 8], 0
mov byte ptr [rax + 12], 0
jmp .rien
; ============================ LE COMMIT (Q3) ==================================
.commit:
lea rax, [rip + SAISIE]
mov eax, dword ptr [rax]
cmp eax, 2
je .commit_chercher
lea rsi, [rip + SAISIE]
add rsi, 12
xor r10d, r10d
xor r11d, r11d
.commit_scan:
movzx eax, byte ptr [rsi]
test eax, eax
jz .commit_scan_fin
cmp eax, 0x30
jb .commit_mal
cmp eax, 0x39
jbe .commit_chiffre
cmp eax, 0x41
jb .commit_mal
cmp eax, 0x46
ja .commit_mal
sub eax, 0x37
jmp .commit_accumule
.commit_chiffre:
sub eax, 0x30
.commit_accumule:
shl r10, 4
add r10, rax
inc r11d
inc rsi
jmp .commit_scan
.commit_scan_fin:
test r11d, r11d
jz .commit_mal
cmp r10, qword ptr [rbx + 520]
jae .commit_hors
mov qword ptr [rbx + 544], r10
mov rax, qword ptr [rbx + 536]
mov rcx, rax
mov edx, dword ptr [rbx + 552]
add rcx, rdx
cmp r10, rax
jb .commit_recadre
cmp r10, rcx
jb .commit_visible
.commit_recadre:
mov rcx, r10
sub rcx, 176
jns .recadre_pos
xor ecx, ecx
.recadre_pos:
and rcx, -16
mov rax, qword ptr [rbx + 520]
sub rax, 384
jbe .recadre_vmax_zero
add rax, 15
and rax, -16
jmp .recadre_vmax_fin
.recadre_vmax_zero:
xor eax, eax
.recadre_vmax_fin:
cmp rcx, rax
jbe .recadre_fin
mov rcx, rax
.recadre_fin:
cmp rcx, qword ptr [rbx + 536]
je .commit_visible
mov r15, rcx
mov rcx, r15
call LOUPE02
test eax, eax
jnz .commit_echec
mov qword ptr [rbx + 536], r15
.commit_visible:
lea rax, [rip + SAISIE]
mov dword ptr [rax], 0
mov rcx, r12
xor edx, edx
mov r8d, 1
call qword ptr [rip + IAT_INVALIDATERECT]
xor eax, eax
jmp .sortie
.commit_mal:
lea rsi, [rip + L_MALFORMEE]
call .message
mov eax, -5
jmp .sortie
.commit_hors:
lea rsi, [rip + L_HORSBORNES]
call .message
mov eax, -3
jmp .sortie
.commit_echec:
mov r10d, eax
lea rax, [rip + SAISIE]
mov dword ptr [rax], 0
mov eax, r10d
jmp .sortie
.commit_chercher:
mov rcx, r12
mov edx, 0x102
mov r8d, 0x0d
xor r9d, r9d
call LOUPE14
jmp .sortie
; ============================ LES REPLIS ======================================
.rien:
xor eax, eax
.sortie:
add rsp, 0x30
pop r15
pop r14
pop r13
pop r12
pop rsi
pop rdi
pop rbx
ret
; ============================ LE MESSAGE À LA BARRE ===========================
.message:
lea rdi, [rip + SAISIE]
add rdi, 12
.message_copie:
mov al, byte ptr [rsi]
mov byte ptr [rdi], al
test al, al
jz .message_fin
inc rsi
inc rdi
jmp .message_copie
.message_fin:
lea rax, [rip + SAISIE]
mov dword ptr [rax], 3
ret
