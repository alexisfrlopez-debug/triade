; sup-38 · test T4 — tunnel TLS du proxy M4 (R1, terrain.17) : le critère M4
; « HTTPS en transit ; échec propre sur certificat invalide » atterrit ICI.
; Le superviseur pose le script client terrain_m4.ps1 (fixture RX -> fichier,
; powershell.exe lancé en MODE 0 — la forme absolue « GET https://… »
; n'existe dans aucun client standard), lance proxy.exe 0.5.0-dev.2 avec
; TUYAUX, joue les DEUX moitiés du critère (page 200 + « tunnel chiffre
; etabli » ; 502 étiquetée 34 o OCTET POUR OCTET + « certificat rejete »),
; puis arrête le proxy (« quit »/« arret »/exit 0 — miroir T2). Les pages
; sont comptées, jamais journalisées ; les événements console du proxy
; SONT journalisés (.flux par ligne) — le constat § 8.4 veut sa voix.
; Neuf bits de succès (bannière, code A, page A, évts A, code B, page B
; 502 exacte, évts B, arret, exit) — tous posés = rax 1, sinon 0.
; (rbx = TAMPON_CMD — pages lues ET console du proxy, séquentiellement ;
;  r12 = handle vivant ; r13 = bits ; r14 = verdict (0 par défaut) ;
;  ebp = lignes console ; .ligne/.ligneNum facteurs communs des traces)
push rbx
push r12
push r13
push r14
push r15
push rbp
sub rsp, 0x48
xor r13d, r13d
xor r14d, r14d
xor ebp, ebp
lea rbx, [rip + TAMPON_CMD]
; --- Q1 : le script client posé AVANT tout lancement (P5) ---
lea rcx, [rip + TAMPON_COMPO]
lea rdx, [rip + FIX_PS1]
mov r8d, LEN_FIX_PS1
call MEMCPY
lea rcx, [rip + S40]
mov edx, LEN_S40
call .ligne
lea rcx, [rip + NOM_PS1]
mov edx, 1
mov r8d, LEN_NOM_PS1
mov r9d, LEN_FIX_PS1
call FICHIERS
test eax, eax
jne .script_ok
lea rcx, [rip + S40B]
mov edx, LEN_S40B
call .ligne
jmp .fin
.script_ok:
; --- Q2 : lancement proxy (MODE 1, tuyaux — la voix du proxy captée) ---
lea rcx, [rip + NOM_PROXY]
mov edx, 1
call LANCEUR
test eax, eax
jne .proxy_vit
lea rcx, [rip + S41B]
mov edx, LEN_S41B
call .ligne
lea rcx, [rip + NOM_PS1]
mov edx, 2
mov r8d, LEN_NOM_PS1
xor r9d, r9d
call FICHIERS
jmp .fin
.proxy_vit:
mov r12, qword ptr [rip + HPROC]
mov qword ptr [rip + HPROC_PROXY], r12
lea rcx, [rip + S41A]
mov edx, LEN_S41A
call .ligne
; --- Q3 : bannière (40 o — R7 : l'octet bannière du scellé M3 vit dans le M4) ---
mov eax, 40
call .attendre
test rax, rax
je .banniere_ko
mov rcx, rbx
lea rdx, [rip + FIX_BANNIERE]
mov r8d, 40
call MEMCMP
test eax, eax
jne .banniere_ko
or r13d, 1
lea rcx, [rip + S42A]
mov edx, LEN_S42A
call .ligne
mov rcx, rbx
mov edx, 38
call .flux
jmp .req_a
.banniere_ko:
lea rcx, [rip + S42B]
mov edx, LEN_S42B
call .ligne
mov rcx, rbx
mov edx, dword ptr [rip + LU]
call .flux
jmp .arret
; --- Q4 : requête A — https saine (example.com, script arg a) ---
.req_a:
lea rcx, [rip + CMD_PS_M4A]
call .ps
test rax, rax
je .ps_absent
lea rcx, [rip + S43A]
mov edx, LEN_S43A
mov r9d, dword ptr [rip + CODE_SORTIE]
call .ligneNum
cmp dword ptr [rip + CODE_SORTIE], 0
jne .evt_a
or r13d, 2
lea rcx, [rip + NOM_PAGE_M4A]
xor edx, edx
mov r8d, LEN_NOM_PAGE_M4A
xor r9d, r9d
call FICHIERS
lea rcx, [rip + S44A]
mov edx, LEN_S44A
mov r9d, dword ptr [rip + LU]
call .ligneNum
cmp qword ptr [rip + LU], 12
jb .evt_a
mov rcx, rbx
lea rdx, [rip + FIX_200]
mov r8d, 12
call MEMCMP
test eax, eax
jne .evt_a
or r13d, 4
; --- Q6 : événements A (58 o — la voix du tunnel établi) ---
.evt_a:
mov eax, 58
call .attendre
test rax, rax
je .evt_a_ko
mov rcx, rbx
lea rdx, [rip + FIX_EVT_M4A]
mov r8d, 58
call MEMCMP
test eax, eax
jne .evt_a_ko
or r13d, 8
mov rcx, rbx
mov edx, 18
call .flux
lea rcx, [rbx + 20]
mov edx, 21
call .flux
lea rcx, [rbx + 43]
mov edx, 13
call .flux
jmp .req_b
.evt_a_ko:
mov rcx, rbx
mov edx, dword ptr [rip + LU]
call .flux
; --- Q7 : requête B — certificat invalide (self-signed.badssl.com, arg b) ---
.req_b:
lea rcx, [rip + CMD_PS_M4B]
call .ps
test rax, rax
je .ps_absent
lea rcx, [rip + S45A]
mov edx, LEN_S45A
mov r9d, dword ptr [rip + CODE_SORTIE]
call .ligneNum
cmp dword ptr [rip + CODE_SORTIE], 0
jne .evt_b
or r13d, 16
lea rcx, [rip + NOM_PAGE_M4B]
xor edx, edx
mov r8d, LEN_NOM_PAGE_M4B
xor r9d, r9d
call FICHIERS
lea rcx, [rip + S46A]
mov edx, LEN_S46A
mov r9d, dword ptr [rip + LU]
call .ligneNum
cmp qword ptr [rip + LU], 34
jne .evt_b
mov rcx, rbx
lea rdx, [rip + FIX_502_M4]
mov r8d, 34
call MEMCMP
test eax, eax
jne .evt_b
or r13d, 32
; --- Q8 : événements B (54 o — le certificat nommé) ---
.evt_b:
mov eax, 54
call .attendre
test rax, rax
je .evt_b_ko
mov rcx, rbx
lea rdx, [rip + FIX_EVT_M4B]
mov r8d, 54
call MEMCMP
test eax, eax
jne .evt_b_ko
or r13d, 64
mov rcx, rbx
mov edx, 18
call .flux
lea rcx, [rbx + 20]
mov edx, 17
call .flux
lea rcx, [rbx + 39]
mov edx, 13
call .flux
jmp .arret
.evt_b_ko:
mov rcx, rbx
mov edx, dword ptr [rip + LU]
call .flux
; --- Q9 : arret : "quit\r\n" sur stdin (6 o), "arret\r\n" attendu (7 o) ---
.arret:
mov rcx, qword ptr [rip + TUYAU_IN_WR]
lea rdx, [rip + QUIT]
mov r8d, 6
lea r9, [rip + LU]
mov qword ptr [rsp + 0x20], 0
call qword ptr [rip + IAT_WF]
mov eax, 7
call .attendre
test rax, rax
je .fin_proxy
mov rcx, rbx
lea rdx, [rip + FIX_ARRET]
mov r8d, 7
call MEMCMP
test eax, eax
jne .fin_proxy
or r13d, 128
mov rcx, rbx
mov edx, 5
call .flux
; --- fin du proxy : attente 10 s (timeout -> TerminateProcess), code ---
; (HPROC_PROXY recharge : le global HPROC est mort — chaque .ps l'a ecrase
;  avec le handle du powershell attendu — leçon T2)
.fin_proxy:
mov rcx, qword ptr [rip + HPROC_PROXY]
mov r12, rcx
mov edx, 10000
call qword ptr [rip + IAT_WAIT]
test eax, eax
je .proxy_mort
mov rcx, r12
mov edx, 1
call qword ptr [rip + IAT_TERMINATE]
mov rcx, r12
mov edx, 5000
call qword ptr [rip + IAT_WAIT]
.proxy_mort:
mov rcx, r12
lea rdx, [rip + CODE_SORTIE]
call qword ptr [rip + IAT_EXITCODE]
mov rcx, r12
call qword ptr [rip + IAT_CH]
cmp dword ptr [rip + CODE_SORTIE], 0
jne .verdict
or r13d, 256
; --- Q10 : verdict — les NEUF drapeaux -------------------------------
.verdict:
cmp r13d, 511
je .ok
lea rcx, [rip + S49B]
mov edx, LEN_S49B
call .ligne
jmp .nettoyage
.ok:
lea rcx, [rip + S49A]
mov edx, LEN_S49A
call .ligne
mov r14d, 1
; --- Q11 : nettoyage (tout chemin) : pages + script supprimés, tuyaux fermés ---
.nettoyage:
lea rcx, [rip + NOM_PAGE_M4A]
mov edx, 2
mov r8d, LEN_NOM_PAGE_M4A
xor r9d, r9d
call FICHIERS
lea rcx, [rip + NOM_PAGE_M4B]
mov edx, 2
mov r8d, LEN_NOM_PAGE_M4B
xor r9d, r9d
call FICHIERS
lea rcx, [rip + NOM_PS1]
mov edx, 2
mov r8d, LEN_NOM_PS1
xor r9d, r9d
call FICHIERS
mov rcx, qword ptr [rip + TUYAU_IN_WR]
call qword ptr [rip + IAT_CH]
mov rcx, qword ptr [rip + TUYAU_OUT_RD]
call qword ptr [rip + IAT_CH]
mov eax, r14d
jmp .fin
; --- chemins d'echec courts ---
.ps_absent:
lea rcx, [rip + S43B]
mov edx, LEN_S43B
call .ligne
jmp .arret
; --- sous-routines ---------------------------------------------------------
; .ligne : rcx = chaîne, edx = longueur -> trace mode 0 (facteur commun)
.ligne:
sub rsp, 8
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
add rsp, 8
ret
; .ligneNum : rcx = chaîne, edx = longueur, r9d = valeur -> trace mode 1
.ligneNum:
sub rsp, 8
mov r8d, 1
call JOURNAL_TRACE
add rsp, 8
ret
; .attendre : eax = N octets attendus sur stdout du proxy -> rax = N | 0
; (frame : ombre+args des appels [rsp..0x2F], r15 sauve [rsp+0x38], N [rsp+0x40])
.attendre:
push rax
push r15
sub rsp, 0x38
mov r15d, 300
.att_boucle:
mov rcx, qword ptr [rip + TUYAU_OUT_RD]
xor edx, edx
xor r8d, r8d
xor r9d, r9d
lea rax, [rip + DISPO]
mov qword ptr [rsp + 0x20], rax
mov qword ptr [rsp + 0x28], 0
call qword ptr [rip + IAT_PEEKPIPE]
test eax, eax
je .att_suite
mov rax, qword ptr [rsp + 0x40]
cmp qword ptr [rip + DISPO], rax
jb .att_suite
mov rcx, qword ptr [rip + TUYAU_OUT_RD]
lea rdx, [rip + TAMPON_CMD]
mov r8, rax
lea r9, [rip + LU]
mov qword ptr [rsp + 0x20], 0
call qword ptr [rip + IAT_RF]
mov rax, qword ptr [rsp + 0x40]
jmp .att_fin
.att_suite:
mov ecx, 50
call qword ptr [rip + IAT_SLEEP]
dec r15d
jne .att_boucle
xor eax, eax
.att_fin:
add rsp, 0x38
pop r15
add rsp, 8
ret
; .ps : rcx = cmdline -> eax = 1 (ZF=1) | 0 (ZF=0) ; CODE_SORTIE pose
; (miroir .curl T2 — attente 45 s : le script porte son propre ReceiveTimeout
;  30 s, la marge couvre le lancement powershell + la poignée TLS Schannel)
; (D98 : 0x28 = ombre ABI x64 — même faute que .curl, même correctif)
.ps:
sub rsp, 0x28
xor edx, edx
call LANCEUR
test eax, eax
je .ps_fin
mov r12, qword ptr [rip + HPROC]
mov rcx, r12
mov edx, 45000
call qword ptr [rip + IAT_WAIT]
mov rcx, r12
lea rdx, [rip + CODE_SORTIE]
call qword ptr [rip + IAT_EXITCODE]
mov rcx, r12
call qword ptr [rip + IAT_CH]
mov eax, 1
.ps_fin:
add rsp, 0x28
ret
; .flux : rcx = ptr, edx = longueur -> ligne embarquee au journal (mode 0)
.flux:
sub rsp, 8
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
inc ebp
add rsp, 8
ret
.fin:
add rsp, 0x48
pop rbp
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
