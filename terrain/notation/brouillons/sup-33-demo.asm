; T1 : rejouer la demo M2 sans main humaine — lancer demo.exe, trouver SA
; fenetre (classe TRIADE_demo), cliquer SON bouton (BM_CLICK, pas de
; coordonnees — la geometrie appartient a la demo), attendre le marqueur
; final du journal (un EVENEMENT borne, pas une duree), fermer proprement,
; verifier (exit 0, 17 lignes, 31 derniers octets = fixture) et embarquer
; les preuves brutes (le constat 8.4 veut l'integralite) ; le balayage
; CRLF est UNE sous-routine partagee par le comptage et l'embarquement
push rbx
push r12
push r13
push r14
push r15
push rbp
sub rsp, 0x48
; --- lancement demo.exe (mode 0, muet) ---
lea rcx, [rip + NOM_DEMO]
xor edx, edx
call LANCEUR
test eax, eax
je .absent
lea rcx, [rip + S10]
mov edx, LEN_S10
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
mov r12, qword ptr [rip + HPROC]
lea rbx, [rip + TAMPON_CMD]
; --- fenetre : FindWindowW(NULL, "TRIADE_demo"), 200 x 50 ms ---
mov r15d, 200
.boucle_fen:
xor ecx, ecx
lea rdx, [rip + CLASSE_DEMO]
call qword ptr [rip + IAT_FINDWINDOW]
test rax, rax
jne .fen_ok
mov ecx, 50
call qword ptr [rip + IAT_SLEEP]
dec r15d
jne .boucle_fen
lea rcx, [rip + S11B]
mov edx, LEN_S11B
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
jmp .tuer_ko
.fen_ok:
mov r14, rax
mov qword ptr [rip + HWND_DEMO], rax
lea rcx, [rip + S11A]
mov edx, LEN_S11A
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
; --- bouton : FindWindowExW(fen, 0, "BUTTON", 0) ---
mov rcx, r14
xor edx, edx
lea r8, [rip + CLASSE_BOUTON]
xor r9d, r9d
call qword ptr [rip + IAT_FINDWINDOWEX]
test rax, rax
je .clic_ko
; --- clic : BM_CLICK par SendMessageTimeoutW (SMTO_ABORTIFHUNG, 90 s) ---
mov rcx, rax
mov edx, 0xF5
xor r8d, r8d
xor r9d, r9d
mov dword ptr [rsp + 0x20], 2
mov dword ptr [rsp + 0x28], 90000
lea rax, [rsp + 0x38]
mov qword ptr [rsp + 0x30], rax
call qword ptr [rip + IAT_SENDMSGTIMEOUT]
test eax, eax
je .clic_ko
lea rcx, [rip + S12A]
mov edx, LEN_S12A
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
jmp .sondage
.clic_ko:
lea rcx, [rip + S12B]
mov edx, LEN_S12B
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
.tuer_ko:
mov rcx, r12
mov edx, 1
call qword ptr [rip + IAT_TERMINATE]
mov rcx, r12
mov edx, 5000
call qword ptr [rip + IAT_WAIT]
mov rcx, r12
call qword ptr [rip + IAT_CH]
xor eax, eax
jmp .fin
; --- sondage du journal : 150 x 200 ms, marqueur = 31 derniers octets ---
.sondage:
mov r15d, 150
.boucle_sond:
call .lire_journal
test rax, rax
je .pas_encore
cmp rax, 31
jb .pas_encore
lea rcx, [rip + TAMPON_CMD]
add rcx, rax
sub rcx, 31
lea rdx, [rip + FIX_FINAL_DEMO]
mov r8d, 31
call MEMCMP
test eax, eax
je .fermeture
.pas_encore:
mov ecx, 200
call qword ptr [rip + IAT_SLEEP]
dec r15d
jne .boucle_sond
; --- fermeture : WM_CLOSE 10 s, attente, code de sortie, handle ferme ---
.fermeture:
mov rcx, r14
mov edx, 0x10
xor r8d, r8d
xor r9d, r9d
mov dword ptr [rsp + 0x20], 2
mov dword ptr [rsp + 0x28], 10000
lea rax, [rsp + 0x38]
mov qword ptr [rsp + 0x30], rax
call qword ptr [rip + IAT_SENDMSGTIMEOUT]
mov rcx, r12
mov edx, 10000
call qword ptr [rip + IAT_WAIT]
mov rcx, r12
lea rdx, [rip + CODE_SORTIE]
call qword ptr [rip + IAT_EXITCODE]
mov rcx, r12
call qword ptr [rip + IAT_CH]
lea rcx, [rip + S13]
mov edx, LEN_S13
mov r8d, 1
mov r9d, dword ptr [rip + CODE_SORTIE]
call JOURNAL_TRACE
; --- relecture finale + comptage des lignes (CRLF) ---
call .lire_journal
xor r13d, r13d
xor ecx, ecx
.compte:
call .fin_ligne
test rdx, rdx
je .compte_fin
inc r13d
lea rcx, [rax + 2]
cmp rcx, qword ptr [rip + LU]
jb .compte
.compte_fin:
lea rcx, [rip + S14]
mov edx, LEN_S14
mov r8d, 1
mov r9d, r13d
call JOURNAL_TRACE
; --- embarquement : chaque ligne via l'entree trace (mode 0) ---
xor r15d, r15d
.embarque:
cmp r15, qword ptr [rip + LU]
jae .verdict
mov rcx, r15
call .fin_ligne
mov r14, r15
mov r15, rax
lea rbp, [rax + rdx]
lea rcx, [rbx + r14]
mov rdx, r15
sub rdx, r14
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
mov r15, rbp
jmp .embarque
; --- verdict : exit 0 ET 17 lignes ET 31 derniers octets == fixture ---
.verdict:
cmp r13d, 17
jne .ko
cmp dword ptr [rip + CODE_SORTIE], 0
jne .ko
mov rax, qword ptr [rip + LU]
cmp rax, 31
jb .ko
lea rcx, [rip + TAMPON_CMD]
add rcx, rax
sub rcx, 31
lea rdx, [rip + FIX_FINAL_DEMO]
mov r8d, 31
call MEMCMP
test eax, eax
jne .ko
lea rcx, [rip + S15A]
mov edx, LEN_S15A
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
lea rcx, [rip + S16A]
mov edx, LEN_S16A
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
mov eax, 1
jmp .fin
.ko:
lea rcx, [rip + S15B]
mov edx, LEN_S15B
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
lea rcx, [rip + S16B]
mov edx, LEN_S16B
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
xor eax, eax
jmp .fin
.absent:
lea rcx, [rip + S10B]
mov edx, LEN_S10B
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
xor eax, eax
.fin:
add rsp, 0x48
pop rbp
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
; --- lecture du journal de la demo (sup-36, chemin repertoire) -> rax = LU ---
.lire_journal:
sub rsp, 8
lea rcx, [rip + NOM_JOURNAL_DEMO]
xor edx, edx
mov r8d, LEN_NOM_JOURNAL_DEMO
xor r9d, r9d
call FICHIERS
add rsp, 8
ret
; --- fin de ligne : rcx = offset -> rax = fin (hors CRLF), rdx = 2|0 ---
.fin_ligne:
xor edx, edx
mov rax, qword ptr [rip + LU]
.fboucle:
cmp rcx, rax
jae .fret
cmp byte ptr [rbx + rcx], 0x0D
jne .fsuite
lea r9, [rcx + 1]
cmp r9, rax
jae .fret
cmp byte ptr [rbx + r9], 0x0A
jne .fsuite
mov rax, rcx
mov edx, 2
.fret:
ret
.fsuite:
inc rcx
jmp .fboucle
