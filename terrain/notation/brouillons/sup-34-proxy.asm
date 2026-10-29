; T2 : le run terrain que M3 attend — curl traverse le proxy (http simple
; puis https CONNECT), la voix du PROXY est captee par tuyaux et verifiee
; par memcmp EXACT (banniere, evenements, arret), les pages recues sont
; COMPTEES jamais journalisees (discipline M3), le flux capture est embarque
; brut ; TOUT echec apres le lancement coule vers le chemin .arret commun
; (quit quand meme, attente bornee, verdict par 9 drapeaux) — zero gel,
; zero fuite, un seul demontage
push rbx
push r12
push r13
push r14
push r15
push rbp
sub rsp, 0x48
xor r13d, r13d
xor ebp, ebp
; --- lancement proxy.exe (mode 1 : tuyaux) ---
lea rcx, [rip + NOM_PROXY]
mov edx, 1
call LANCEUR
test eax, eax
je .proxy_absent
mov r12, qword ptr [rip + HPROC]
mov qword ptr [rip + HPROC_PROXY], r12
; (le handle proxy survit aux curls : chaque .curl ecrase le global HPROC)
lea rbx, [rip + TAMPON_CMD]
lea rcx, [rip + S20]
mov edx, LEN_S20
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
; --- banniere : 40 octets exacts (sondage borne 15 s) ---
mov eax, 40
call .attendre
test rax, rax
je .banniere_timeout
mov rcx, rbx
lea rdx, [rip + FIX_BANNIERE]
mov r8d, 40
call MEMCMP
test eax, eax
jne .banniere_ko
or r13d, 1
lea rcx, [rip + S21A]
mov edx, LEN_S21A
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
mov rcx, rbx
mov edx, 38
call .flux
jmp .curl_http
.banniere_ko:
lea rcx, [rip + S21B]
mov edx, LEN_S21B
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
mov rcx, rbx
mov edx, dword ptr [rip + LU]
call .flux
jmp .arret
.banniere_timeout:
lea rcx, [rip + S21B]
mov edx, LEN_S21B
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
jmp .arret
; --- curl http : lancement, attente 25 s, code, page comptee ---
.curl_http:
lea rcx, [rip + CMD_CURL_HTTP]
call .curl
je .curl_absent
lea rcx, [rip + S22A]
mov edx, LEN_S22A
mov r8d, 1
mov r9d, dword ptr [rip + CODE_SORTIE]
call JOURNAL_TRACE
cmp dword ptr [rip + CODE_SORTIE], 0
jne .page_http
or r13d, 2
.page_http:
lea rcx, [rip + NOM_PAGE_HTTP]
xor edx, edx
mov r8d, LEN_NOM_PAGE_HTTP
xor r9d, r9d
call FICHIERS
lea rcx, [rip + S23]
mov edx, LEN_S23
mov r8d, 1
mov r9d, dword ptr [rip + LU]
call JOURNAL_TRACE
cmp qword ptr [rip + LU], 0
je .evt_http
or r13d, 4
; --- evenements http : 35 octets exacts, embarques en 2 lignes ---
.evt_http:
mov eax, 35
call .attendre
test rax, rax
je .curl_https
mov rcx, rbx
lea rdx, [rip + FIX_EVT_HTTP]
mov r8d, 35
call MEMCMP
test eax, eax
jne .ev_http_ko
or r13d, 8
mov rcx, rbx
mov edx, 18
call .flux
lea rcx, [rbx + 20]
mov edx, 13
call .flux
jmp .curl_https
.ev_http_ko:
mov rcx, rbx
mov edx, dword ptr [rip + LU]
call .flux
; --- curl https : meme discipline (tunnel) ---
.curl_https:
lea rcx, [rip + CMD_CURL_HTTPS]
call .curl
je .curl_absent
lea rcx, [rip + S24]
mov edx, LEN_S24
mov r8d, 1
mov r9d, dword ptr [rip + CODE_SORTIE]
call JOURNAL_TRACE
cmp dword ptr [rip + CODE_SORTIE], 0
jne .page_https
or r13d, 16
.page_https:
lea rcx, [rip + NOM_PAGE_HTTPS]
xor edx, edx
mov r8d, LEN_NOM_PAGE_HTTPS
xor r9d, r9d
call FICHIERS
lea rcx, [rip + S25]
mov edx, LEN_S25
mov r8d, 1
mov r9d, dword ptr [rip + LU]
call JOURNAL_TRACE
cmp qword ptr [rip + LU], 0
je .evt_https
or r13d, 32
; --- evenements https : 43 octets exacts, embarques en 3 lignes ---
.evt_https:
mov eax, 43
call .attendre
test rax, rax
je .arret
mov rcx, rbx
lea rdx, [rip + FIX_EVT_HTTPS]
mov r8d, 43
call MEMCMP
test eax, eax
jne .ev_https_ko
or r13d, 64
mov rcx, rbx
mov edx, 18
call .flux
lea rcx, [rbx + 20]
mov edx, 6
call .flux
lea rcx, [rbx + 28]
mov edx, 13
call .flux
jmp .arret
.ev_https_ko:
mov rcx, rbx
mov edx, dword ptr [rip + LU]
call .flux
; --- arret : "quit\r\n" sur stdin (6 o), "arret\r\n" attendu (7 o) ---
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
; (HPROC_PROXY recharge : le global HPROC est mort — chaque .curl l'a ecrase
;  avec le handle du curl attendu ; attendre un handle deja ferme =
;  WAIT_FAILED systematique, fuite du handle proxy et exit code fautif)
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
jne .ligne_count
or r13d, 256
.ligne_count:
lea rcx, [rip + S26]
mov edx, LEN_S26
mov r8d, 1
mov r9d, ebp
call JOURNAL_TRACE
; --- verdict : les 9 drapeaux (banniere, codes, pages, evenements, arret, exit) ---
cmp r13d, 511
je .ok
lea rcx, [rip + S27B]
mov edx, LEN_S27B
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
lea rcx, [rip + S28B]
mov edx, LEN_S28B
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
xor r14d, r14d
jmp .nettoyage
.ok:
lea rcx, [rip + S27A]
mov edx, LEN_S27A
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
lea rcx, [rip + S28A]
mov edx, LEN_S28A
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
mov r14d, 1
; --- nettoyage (tout chemin) : pages supprimees, tuyaux parent fermes ---
.nettoyage:
lea rcx, [rip + NOM_PAGE_HTTP]
mov edx, 2
mov r8d, LEN_NOM_PAGE_HTTP
xor r9d, r9d
call FICHIERS
lea rcx, [rip + NOM_PAGE_HTTPS]
mov edx, 2
mov r8d, LEN_NOM_PAGE_HTTPS
xor r9d, r9d
call FICHIERS
mov rcx, qword ptr [rip + TUYAU_IN_WR]
call qword ptr [rip + IAT_CH]
mov rcx, qword ptr [rip + TUYAU_OUT_RD]
call qword ptr [rip + IAT_CH]
mov eax, r14d
jmp .fin
; --- chemins d'echec courts ---
.curl_absent:
lea rcx, [rip + S22B]
mov edx, LEN_S22B
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
jmp .arret
.proxy_absent:
lea rcx, [rip + S20B]
mov edx, LEN_S20B
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
xor eax, eax
jmp .fin
; --- sous-routines ---------------------------------------------------------
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
; .curl : rcx = cmdline -> eax = 1 (ZF=1) | 0 (ZF=0) ; CODE_SORTIE pose
; (D98 : 0x28 = ombre ABI x64 0x20 + alignement 8 — le 8 nu de la régénération
;  D96 laissait la maison d'arguments rdx de WaitForSingleObject/GetExitCode
;  Process RECOUVRIR l'adresse de retour : mort du superviseur pendant T2,
;  fenêtre fermée, proxy orphelin — terrain16 portait 0x28, miroir exact)
.curl:
sub rsp, 0x28
xor edx, edx
call LANCEUR
test eax, eax
je .curl_fin
mov r12, qword ptr [rip + HPROC]
mov rcx, r12
mov edx, 25000
call qword ptr [rip + IAT_WAIT]
mov rcx, r12
lea rdx, [rip + CODE_SORTIE]
call qword ptr [rip + IAT_EXITCODE]
mov rcx, r12
call qword ptr [rip + IAT_CH]
mov eax, 1
.curl_fin:
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
