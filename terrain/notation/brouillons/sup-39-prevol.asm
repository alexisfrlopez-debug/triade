; le prevol (R1, terrain.18, D101) : AVANT l'extraction du kit, deux sondes
; bornees journalisent leurs preuves — (1) taskkill.exe /f /IM proxy.exe
; /IM demo.exe tue les orphelins d'un run anterieur (un proxy.exe survivant
; VERROUILLE le fichier proxy.exe a re-poser et tient le port 25000 ; un
; demo.exe survivant ferait mentir FindWindowW — le reflexe ETAPE 0 du
; protocole, devenu automatique ; codes bruts au journal : 0 = orphelins
; tues, 128 = introuvables = etat PROPRE, autre = refus) ; (2) curl.exe -s
; --max-time 20 -o NUL https://example.com/ sonde l'AMONT DIRECT, sans
; proxy (code 0 = reseau vivant, 6/7/28 = DNS/connexion/timeout — le run
; 17-D est mort de l'amont, pas du code : l'ETAPE 0 BIS, devenue
; automatique). Les DEUX codes partent au journal (S08/S09, mode numerique
; r8=1 — miroir S13/S22/S47) et ne TOUCHENT JAMAIS le verdict : le prevol
; est une EVIDENCE, pas un juge (miroir du temoin D99 : resultat ignore).
; Mode 0 partout (aucun tuyau, aucun heritage : les sondes vivent et
; meurent seules) ; mort attendue par WaitForSingleObject borne (30000 ms,
; zero gel — curl s'autolimite a 20) ; handle ferme sur tout chemin (zero
; fuite) ; lancement impossible = ligne sautee, JAMAIS un crash (un run
; prive de prevol vaut mieux qu'un run mort au prevol). RAX = 0 sur tout
; chemin : sup-09:R4 l'appelle et l'ignore.
sub rsp, 0x28
; --- sonde 1 : orphelins (taskkill, AVANT l'extraction — I5) ---
lea rcx, [rip + CMD_TASKKILL]
xor edx, edx
call LANCEUR
test eax, eax
je .sans_taskkill
call .attendre
lea rcx, [rip + S08]
mov edx, LEN_S08
call .ligne
.sans_taskkill:
; --- sonde 2 : reseau amont (curl direct, sans proxy) ---
lea rcx, [rip + CMD_CURL_AMONT]
xor edx, edx
call LANCEUR
test eax, eax
je .fin
call .attendre
lea rcx, [rip + S09]
mov edx, LEN_S09
call .ligne
.fin:
xor eax, eax
add rsp, 0x28
ret
; --- .ligne : journalise (ligne rcx, longueur edx) + code CODE_SORTIE en
; numerique — relais vers win-05 scelle (jmp terminal : la trace rend la
; main a l'appelant du prevol, la pile du prevol reste la sienne) ---
.ligne:
mov r8d, 1
mov r9d, dword ptr [rip + CODE_SORTIE]
jmp JOURNAL_TRACE
; --- .attendre : mort bornee du dernier processus lance (HPROC), code lu
; a CODE_SORTIE, handle ferme — zero gel (charte § 1), zero fuite (§ 2) ---
.attendre:
sub rsp, 0x28
mov rcx, qword ptr [rip + HPROC]
mov edx, 30000
call qword ptr [rip + IAT_WAIT]
mov rcx, qword ptr [rip + HPROC]
lea rdx, [rip + CODE_SORTIE]
call qword ptr [rip + IAT_EXITCODE]
mov rcx, qword ptr [rip + HPROC]
call qword ptr [rip + IAT_CH]
add rsp, 0x28
ret
