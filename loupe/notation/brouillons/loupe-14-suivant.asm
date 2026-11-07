; loupe-14 · suivant : l'occurrence suivante au fichier, la FIN nommée · spec loupe-14:R1
; LA SAISIE (Q1) : Ctrl+F OUVRE le mode CHERCHER (WM_CHAR 0x06 — LE CODE DE
; CONTRÔLE, la voie WM_CHAR : aucune feuille GetKeyState au plan) ; la
; barre-saisie de loupe-12, LE MODE PARTAGÉ (le tampon, la correction,
; l'échappée idem : RENVOI, jamais réécrit) ; le commit (VK_RETURN, délégué
; par loupe-12) : le compte IMPAIR ou non hexa ou vide ou > 64 chiffres →
; -5 « paires hexa attendues » (E1) ; SINON les paires posées à la zone
; MOTIF (la longueur à +32 — F3 reprend le dernier motif, la re-saisie
; n'est jamais exigée).
; LA RECHERCHE AU FICHIER (Q2) : depuis LE PLANCHER (le commit : le
; curseur ; F3 : le curseur + 1 — le plancher NE RECULE JAMAIS : une
; fenêtre manquée y avance le premier départ non examiné), les fenêtres
; de 64 Kio lues à TAMPON_CUMUL (SetFilePointerEx + ReadFile — le pointeur
; repositionné à CHAQUE fenêtre, Q5 ; la longueur LUE comptée, jamais
; supposée), CHAQUE fenêtre confiée à loupe-13 (le départ relatif = LE
; PLANCHER − le bord de fenêtre, BORNÉ À 0 — la règle de la spec) ;
; TAMPON_CUMUL partagé (I1 : l'exclusion de famille).
; LE RECOUVREMENT (Q3) : la fenêtre suivante commence à bord + 64 Kio −
; (longueur − 1) — l'occurrence À CHEVAL sur la frontière est dans les
; DEUX fenêtres, loupe-13 la trouve dans la seconde : JAMAIS manquée (les
; départs examinés se suivent sans trou ni recouvrement mort : la preuve
; par construction, V2 la juge).
; LA RENCONTRE : le curseur = l'absolue, LA RÈGLE DE RECADRAGE DE
; LOUPE-12 (renvoi — si le curseur sort de la fenêtre visible), loupe-02
; LA PREMIÈRE (le refus relayé, la vue inchangée), InvalidateRect, rax=0.
; LA FIN (Q4) : plus de fenêtre et plus d'occurrence → -1 « plus
; d'occurrence », LE MOTIF DEMEURE (la fin n'efface pas la question).
; E2 sans session → -4 ; E3 le refus de lecture → -6 relayé (GetLastError
; consigné), la recherche STOPPÉE proprement (le départ DEMEURE, rien
; bougé) ; F3 sans motif → -5 « paires hexa attendues » (chercher rien
; n'est pas chercher — le miroir de loupe-13 E1).
; I2 : le motif BORNÉ (≤ 32) ; I3 : la recherche est LECTURE SEULE ;
; I4 : l'IAT fermée (SetFilePointerEx, ReadFile, GetLastError,
; InvalidateRect — la composition loupe-13 PAR LA CARTE) ; NOP, 0x90.
push rbx
push rdi
push rsi
push r12
push r13
push r14
push r15
sub rsp, 0x40
mov r12, rcx
lea rbx, [rip + CADRE]
cmp rdx, 0x100
je .touche
cmp rdx, 0x102
je .caract
xor eax, eax
jmp .sortie
; ============================ F3 : L'OCCURRENCE SUIVANTE =======================
.touche:
cmp r8d, 0x72
jne .rien
cmp qword ptr [rbx + 528], -1
jne .suivant_session
lea rsi, [rip + L_SESSION]
call .message
mov eax, -4
jmp .sortie
.suivant_session:
lea rax, [rip + MOTIF]
mov r14d, dword ptr [rax + 32]
test r14d, r14d
jnz .suivant_motif
lea rsi, [rip + L_PAIRES]
call .message
mov eax, -5
jmp .sortie
.suivant_motif:
mov r15, qword ptr [rbx + 544]
inc r15
jmp .recherche
; ============================ Ctrl+F : LE MODE CHERCHER (Q1, E2) ==============
.caract:
cmp r8d, 0x06
je .ouvrir
cmp r8d, 0x0d
je .commit
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
mov dword ptr [rax], 2
mov dword ptr [rax + 4], 0
mov dword ptr [rax + 8], 0
mov byte ptr [rax + 12], 0
jmp .rien
; ============================ LE COMMIT (mode CHERCHER, E1) ===================
.commit:
cmp qword ptr [rbx + 528], -1
jne .commit_session
lea rsi, [rip + L_SESSION]
call .message
mov eax, -4
jmp .sortie
.commit_session:
lea rsi, [rip + SAISIE]
add rsi, 12
xor r13d, r13d
.commit_scan:
movzx eax, byte ptr [rsi]
test eax, eax
jz .commit_scan_fin
cmp eax, 0x30
jb .commit_mal
cmp eax, 0x39
jbe .commit_suite
cmp eax, 0x41
jb .commit_mal
cmp eax, 0x46
ja .commit_mal
.commit_suite:
inc r13d
inc rsi
jmp .commit_scan
.commit_scan_fin:
test r13d, r13d
jz .commit_mal
test r13d, 1
jnz .commit_mal
cmp r13d, 64
ja .commit_mal
lea rsi, [rip + SAISIE]
add rsi, 12
lea rdi, [rip + MOTIF]
xor ecx, ecx
.commit_pose:
cmp ecx, r13d
jae .commit_pose_fin
movzx eax, byte ptr [rsi]
call .hexval
mov r10b, al
movzx eax, byte ptr [rsi + 1]
call .hexval
shl r10b, 4
or al, r10b
mov byte ptr [rdi], al
add rsi, 2
inc rdi
add ecx, 2
jmp .commit_pose
.commit_pose_fin:
lea rax, [rip + MOTIF]
mov edx, r13d
shr edx, 1
mov dword ptr [rax + 32], edx
mov r14d, edx
mov r15, qword ptr [rbx + 544]
jmp .recherche
.commit_mal:
lea rsi, [rip + L_PAIRES]
call .message
mov eax, -5
jmp .sortie
; ============================ LA RECHERCHE AU FICHIER (Q2) ====================
.recherche:
cmp r15, qword ptr [rbx + 520]
jae .fin_nomme
mov r13, r15
shr r13, 16
shl r13, 16
.fenetre:
mov rax, qword ptr [rbx + 520]
sub rax, r13
jbe .fin_nomme
cmp rax, 65536
jbe .fenetre_len
mov eax, 65536
.fenetre_len:
mov qword ptr [rsp + 0x28], rax
mov rcx, qword ptr [rbx + 528]
mov rdx, r13
xor r8d, r8d
xor r9d, r9d
call qword ptr [rip + IAT_SETFILEPOINTEREX]
test eax, eax
jz .refus_systeme
mov qword ptr [rsp + 0x20], 0
mov qword ptr [rsp + 0x30], 0
mov rcx, qword ptr [rbx + 528]
lea rdx, [rip + CUMUL]
mov r8, qword ptr [rsp + 0x28]
lea r9, [rsp + 0x30]
call qword ptr [rip + IAT_READFILE]
test eax, eax
jz .refus_systeme
lea rcx, [rip + CUMUL]
mov rdx, qword ptr [rsp + 0x30]
lea r8, [rip + MOTIF]
mov r9d, r14d
mov rax, r15
sub rax, r13
jns .fenetre_depart
xor eax, eax
.fenetre_depart:
mov qword ptr [rsp + 0x20], rax
call LOUPE13
cmp eax, 0
jge .trouve
cmp eax, -1
je .fenetre_suivante
jmp .sortie
.trouve:
add rax, r13
jmp .rencontre
.fenetre_suivante:
mov rax, 65536
sub rax, r14
inc rax
add r13, rax
cmp r15, r13
jae .fenetre
mov r15, r13
jmp .fenetre
; ============================ LA RENCONTRE (Q2 — le renvoi à loupe-12) ========
.rencontre:
mov qword ptr [rbx + 544], rax
mov rcx, qword ptr [rbx + 536]
mov rdx, rcx
mov r8d, dword ptr [rbx + 552]
add rdx, r8
cmp rax, rcx
jb .rencontre_recadre
cmp rax, rdx
jb .rencontre_visible
.rencontre_recadre:
mov rcx, rax
sub rcx, 176
jns .rencontre_pos
xor ecx, ecx
.rencontre_pos:
and rcx, -16
mov rax, qword ptr [rbx + 520]
sub rax, 384
jbe .rencontre_vmax0
add rax, 15
and rax, -16
jmp .rencontre_vmaxfin
.rencontre_vmax0:
xor eax, eax
.rencontre_vmaxfin:
cmp rcx, rax
jbe .rencontre_clamp
mov rcx, rax
.rencontre_clamp:
cmp rcx, qword ptr [rbx + 536]
je .rencontre_visible
mov r15, rcx
mov rcx, r15
call LOUPE02
test eax, eax
jnz .refus_lecture
mov qword ptr [rbx + 536], r15
.rencontre_visible:
lea rax, [rip + SAISIE]
mov dword ptr [rax], 0
mov rcx, r12
xor edx, edx
mov r8d, 1
call qword ptr [rip + IAT_INVALIDATERECT]
xor eax, eax
jmp .sortie
; ============================ LES REPLIS NOMMÉS ===============================
.fin_nomme:
lea rsi, [rip + L_FIN]
call .message
mov eax, -1
jmp .sortie
.refus_systeme:
call qword ptr [rip + IAT_GETLASTERROR]
lea rax, [rip + SAISIE]
mov dword ptr [rax], 0
mov eax, -6
jmp .sortie
.refus_lecture:
mov r10d, eax
lea rax, [rip + SAISIE]
mov dword ptr [rax], 0
mov eax, r10d
jmp .sortie
.rien:
xor eax, eax
.sortie:
add rsp, 0x40
pop r15
pop r14
pop r13
pop r12
pop rsi
pop rdi
pop rbx
ret
; ============================ LES SOUS-ROUTINES LOCALES =======================
.hexval:
cmp al, 0x39
jbe .hexval_chiffre
sub al, 0x37
ret
.hexval_chiffre:
sub al, 0x30
ret
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
