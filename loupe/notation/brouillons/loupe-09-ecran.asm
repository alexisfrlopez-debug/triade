; loupe-09 · écran : la vitrine entière et la disposition déclarée · spec loupe-09:R1
; WinMain (Q1) : LA LIGNE DE COMMANDE LUE À LA MAIN par GetCommandLineW —
; le programme sauté (guillemets honorés : « "… » » ou le premier blanc),
; les blancs passés, le reste EST le chemin — aucun shell32, aucune
; dépendance, GetKeyState jamais (les codes de contrôle 0x06/0x07 vivent
; par WM_CHAR — Ctrl+F ouvre CHERCHER, Ctrl+G ouvre ALLER) ; chemin cité
; → loupe-01 : la session naît AVANT la vitrine (les WM_SIZE de la
; création trouvent la session vivante), le refus nommé monte à la barre
; (-2 → « fichier introuvable », l'autre → « refus système ») et la
; vitrine s'ouvre VIDE VRAIE — l'état nommé, jamais la mort ; chemin
; absent → la vitrine s'ouvre, l'usage à la barre (peint par loupe-10).
; LA CLASSE (Q2) : WNDCLASSEXW SUR LA PILE (jamais en .data) —
; lpfnWndProc = LA PROCÉDURE (lea rip : l'image PI, D33 — le hInstance
; vient de l'ABI de l'entrée, GetModuleHandleW attend son geste), le
; curseur flèche (LoadCursorW IDC_ARROW), le pinceau COLOR_WINDOW+1,
; la classe « LoupeHexa » et le titre UTF-16 du plan ; puis
; CreateWindowExW (STYLE_FENETRE — l'ascenseur inclus — 640×480,
; CW_USEDEFAULT), HWND_PRINCIPAL posé à SA zone (I1 : les trois zones
; déclarées avant la première goutte), ShowWindow(SW_SHOW).
; E1/E2 : RegisterClassExW ou CreateWindowExW nuls → MessageBoxW
; (MB_ICONERROR, l'explication fatale du plan) PUIS ExitProcess(1) —
; la vitrine impossible s'explique PUIS meurt (D36 : jamais silencieux).
; LA BOUCLE (Q4) : win-03 HÉRITÉE PAR LA CARTE — l'adresse scellée démo
; 0x15C0, R7 : les octets de demo.exe 0.3.0, ses déplacements visent
; l'IAT démo @0x2818/0x2820/0x2828 ; le retour propre ExitProcess(0)
; (Q5 — le bloc ne rend jamais, ExitProcess est le dernier appel).
; LA PROCÉDURE (Q3, D38 — les quatre arguments aux NON-VOLATILS avant
; tout appel) : WM_PAINT → loupe-10 ; WM_SIZE/WM_VSCROLL/WM_MOUSEWHEEL
; → loupe-11 (les quatre passés) ; WM_KEYDOWN : F5 → loupe-12, F3 →
; loupe-14 ; WM_CHAR : la saisie active → loupe-12 (le gestionnaire
; partagé), 0x06 → loupe-14, 0x07 → loupe-12, le reste → DefWindowProcW
; (loupe-16 au chantier (d) — la table s'y étendra, révision nommée) ;
; TOUT LE RESTE → DefWindowProcW (son rax retourné tel quel) ; TOUT
; verdict négatif des blocs routés monte à la barre (.monter : le -6
; générique « refus système » SI aucun message ne vit déjà — jamais un
; refus muet, jamais un crash, I4) ; les messages traités rendent 0.
; AUCUNE goutte de peinture hors WM_PAINT (I3) ; l'IAT fermée du bloc
; (GetCommandLineW, LoadCursorW, RegisterClassExW, CreateWindowExW,
; ShowWindow, MessageBoxW, ExitProcess, DefWindowProcW) ; NOP, 0x90.
push rdi
push rsi
push r12
sub rsp, 0xb0
mov r12, rcx
; ==================== LA LIGNE DE COMMANDE LUE À LA MAIN (Q1) =================
call qword ptr [rip + IAT_GETCOMMANDLINEW]
mov rdx, rax
cmp word ptr [rdx], 0x22
jne .programme_nu
add rdx, 2
.programme_cote:
movzx eax, word ptr [rdx]
test eax, eax
jz .sans_chemin
cmp eax, 0x22
je .programme_apres
add rdx, 2
jmp .programme_cote
.programme_nu:
movzx eax, word ptr [rdx]
test eax, eax
jz .sans_chemin
cmp eax, 0x20
je .programme_apres
add rdx, 2
jmp .programme_nu
.programme_apres:
movzx eax, word ptr [rdx]
cmp eax, 0x20
jne .chemin_pre
add rdx, 2
jmp .programme_apres
.chemin_pre:
movzx eax, word ptr [rdx]
test eax, eax
jz .sans_chemin
mov rcx, rdx
call LOUPE01
test eax, eax
jns .suite_vitrine
cmp eax, -2
jne .refus_gen
lea rsi, [rip + L_ABSENT]
call .message
jmp .suite_vitrine
.refus_gen:
lea rsi, [rip + L_SYSTEME]
call .message
.sans_chemin:
.suite_vitrine:
; ==================== LA CLASSE (Q2 — WNDCLASSEXW sur la pile) ================
lea rax, [.procedure]
mov qword ptr [rsp + 0x68], rax
mov dword ptr [rsp + 0x60], 80
mov dword ptr [rsp + 0x64], 0
mov dword ptr [rsp + 0x70], 0
mov dword ptr [rsp + 0x74], 0
mov qword ptr [rsp + 0x78], r12
mov qword ptr [rsp + 0x80], 0
xor ecx, ecx
mov edx, 32512
call qword ptr [rip + IAT_LOADCURSORW]
mov qword ptr [rsp + 0x88], rax
mov qword ptr [rsp + 0x90], 5
mov qword ptr [rsp + 0x98], 0
lea rax, [rip + CLASSE]
mov qword ptr [rsp + 0xa0], rax
mov qword ptr [rsp + 0xa8], 0
lea rcx, [rsp + 0x60]
call qword ptr [rip + IAT_REGISTERCLASSEXW]
test eax, eax
jz .vitrine_impossible
; ==================== LA VITRINE (Q2 — 640×480, l'ascenseur) ==================
mov eax, 0x80000000
mov qword ptr [rsp + 0x20], rax
mov qword ptr [rsp + 0x28], rax
mov qword ptr [rsp + 0x30], 640
mov qword ptr [rsp + 0x38], 480
mov qword ptr [rsp + 0x40], 0
mov qword ptr [rsp + 0x48], 0
mov qword ptr [rsp + 0x50], r12
mov qword ptr [rsp + 0x58], 0
xor ecx, ecx
lea rdx, [rip + CLASSE]
lea r8, [rip + TITRE]
mov r9d, 0x00ef0000
call qword ptr [rip + IAT_CREATEWINDOWEXW]
test rax, rax
jz .vitrine_impossible
lea rcx, [rip + HWND]
mov qword ptr [rcx], rax
mov rcx, rax
mov edx, 5
call qword ptr [rip + IAT_SHOWWINDOW]
; ==================== LA BOUCLE HÉRITÉE (Q4 — win-03 PAR LA CARTE) ============
call WIN03
xor ecx, ecx
call qword ptr [rip + IAT_EXITPROCESS]
; ==================== E1/E2 : l'explication fatale puis la mort ==============
.vitrine_impossible:
xor ecx, ecx
lea rdx, [rip + ERREUR]
lea r8, [rip + TITRE]
mov r9d, 0x10
call qword ptr [rip + IAT_MESSAGEBOXW]
mov ecx, 1
call qword ptr [rip + IAT_EXITPROCESS]
; ==================== LA PROCÉDURE (Q3 — le callback msx64) ===================
.procedure:
push rbx
push rdi
push rsi
push r12
sub rsp, 0x28
mov r12, rcx
mov rbx, rdx
mov rsi, r8
mov rdi, r9
cmp rbx, 0x0f
je .r_peinture
cmp rbx, 5
je .r_defilement
cmp rbx, 0x115
je .r_defilement
cmp rbx, 0x20a
je .r_defilement
cmp rbx, 0x100
je .r_commande
cmp rbx, 0x102
je .r_caractere
jmp .r_defaut
.r_peinture:
mov rcx, r12
call LOUPE10
call .monter
xor eax, eax
jmp .r_retour
.r_defilement:
mov rcx, r12
mov rdx, rbx
mov r8, rsi
mov r9, rdi
call LOUPE11
call .monter
xor eax, eax
jmp .r_retour
.r_commande:
cmp rsi, 0x74
je .r_aller
cmp rsi, 0x72
je .r_suivant
jmp .r_defaut
.r_aller:
mov rcx, r12
mov edx, 0x100
mov r8, rsi
mov r9, rdi
call LOUPE12
call .monter
xor eax, eax
jmp .r_retour
.r_suivant:
mov rcx, r12
mov edx, 0x100
mov r8, rsi
mov r9, rdi
call LOUPE14
call .monter
xor eax, eax
jmp .r_retour
.r_caractere:
lea rax, [rip + SAISIE]
mov eax, dword ptr [rax]
test eax, eax
jz .r_caractere_libre
mov rcx, r12
mov edx, 0x102
mov r8, rsi
mov r9, rdi
call LOUPE12
call .monter
xor eax, eax
jmp .r_retour
.r_caractere_libre:
cmp rsi, 0x06
je .r_libre_suivant
cmp rsi, 0x07
je .r_libre_aller
jmp .r_defaut
.r_libre_suivant:
mov rcx, r12
mov edx, 0x102
mov r8, rsi
mov r9, rdi
call LOUPE14
call .monter
xor eax, eax
jmp .r_retour
.r_libre_aller:
mov rcx, r12
mov edx, 0x102
mov r8, rsi
mov r9, rdi
call LOUPE12
call .monter
xor eax, eax
jmp .r_retour
.r_defaut:
mov rcx, r12
mov rdx, rbx
mov r8, rsi
mov r9, rdi
call qword ptr [rip + IAT_DEFWINDOWPROCW]
.r_retour:
add rsp, 0x28
pop r12
pop rsi
pop rdi
pop rbx
ret
; ==================== LES SOUS-ROUTINES LOCALES ===============================
.monter:
test eax, eax
jns .monter_fin
lea rdx, [rip + SAISIE]
cmp dword ptr [rdx], 0
jne .monter_fin
lea rsi, [rip + L_SYSTEME]
call .message
.monter_fin:
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
