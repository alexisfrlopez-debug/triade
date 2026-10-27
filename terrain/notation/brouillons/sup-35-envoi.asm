; T3 : fermer la boucle du constat — le journal part DANS le dossier test du
; Drive SANS intervention : lecture de terrain_jetons.bin (annexe hors
; depot, interdit 11), rafraichissement OAuth par curl.exe (requete
; composee par le formatteur a marqueurs), extraction du jeton (sup-22),
; session resumable (POST meta, URL dans les en-tetes -D), televersement
; (PUT --data-binary @journal), verification par code de sortie ; la voie
; est EXACTEMENT celle de drive_sync.py ; aucun secret au journal (I1),
; BUF_CHEMIN jamais recompose (I2), TAMPON_JETON cycle sequentiel (I3)
push rbx
push r12
push r13
push r14
push r15
push rbp
sub rsp, 0x48
lea rbx, [rip + TAMPON_COMPO]
; --- S30 : annonce, puis lecture des jetons (annexe) ---
lea rcx, [rip + S30]
mov edx, LEN_S30
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
lea rcx, [rip + NOM_JETONS]
xor edx, edx
mov r8d, LEN_NOM_JETONS
xor r9d, r9d
call FICHIERS
test rax, rax
je .jetons_absents
; recopier les jetons vers TAMPON_JETON (le FICHIERS lit dans TAMPON_CMD)
lea rcx, [rip + TAMPON_JETON]
lea rdx, [rip + TAMPON_CMD]
mov r8, rax
call MEMCPY
; --- requete OAuth : formatteur a marqueurs -> zone composition ---
xor ebp, ebp
lea r15, [rip + GABARIT_OAUTH]
call .gab
lea rcx, [rip + NOM_REQ]
mov edx, 1
mov r8d, LEN_NOM_REQ
mov r9d, ebp
call FICHIERS
lea rcx, [rip + S32]
mov edx, LEN_S32
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
; --- curl jeton : cmdline composee, lancement, attente 35 s, code ---
xor ebp, ebp
lea r15, [rip + GABARIT_JETON]
call .gab
mov rcx, rbx
xor edx, edx
call LANCEUR
test eax, eax
je .jeton_ko
mov r12, qword ptr [rip + HPROC]
mov rcx, r12
mov edx, 35000
call qword ptr [rip + IAT_WAIT]
mov rcx, r12
lea rdx, [rip + CODE_SORTIE]
call qword ptr [rip + IAT_EXITCODE]
mov rcx, r12
call qword ptr [rip + IAT_CH]
cmp dword ptr [rip + CODE_SORTIE], 0
jne .jeton_ko
; --- reponse OAuth : lire, extraire le jeton (sup-22, etiquette -> valeur) ---
lea rcx, [rip + NOM_JETON_JSON]
xor edx, edx
mov r8d, LEN_NOM_JETON_JSON
xor r9d, r9d
call FICHIERS
test rax, rax
je .jeton_ko
lea rcx, [rip + TAMPON_CMD]
mov rdx, rax
lea r8, [rip + ETIQ_TOKEN]
mov r9d, LEN_ETIQ_TOKEN
mov dword ptr [rsp + 0x20], 0x22
lea rax, [rip + TAMPON_JETON]
mov qword ptr [rsp + 0x28], rax
mov qword ptr [rsp + 0x30], 480
call BALAYEUR
test rax, rax
je .jeton_ko
lea rcx, [rip + S33A]
mov edx, LEN_S33A
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
; --- metadonnees : nom du run + dossier test, posees par le formatteur ---
xor ebp, ebp
lea r15, [rip + GABARIT_META]
call .gab
lea rcx, [rip + NOM_META]
mov edx, 1
mov r8d, LEN_NOM_META
mov r9d, ebp
call FICHIERS
; --- curl session : en-tetes -D terrain_session.txt, attente 35 s, code ---
xor ebp, ebp
lea r15, [rip + GABARIT_SESSION]
call .gab
mov rcx, rbx
xor edx, edx
call LANCEUR
test eax, eax
je .session_ko
mov r12, qword ptr [rip + HPROC]
mov rcx, r12
mov edx, 35000
call qword ptr [rip + IAT_WAIT]
mov rcx, r12
lea rdx, [rip + CODE_SORTIE]
call qword ptr [rip + IAT_EXITCODE]
mov rcx, r12
call qword ptr [rip + IAT_CH]
cmp dword ptr [rip + CODE_SORTIE], 0
jne .session_ko
; --- en-tetes : lire, extraire l'URL de session (arret au CR) ---
lea rcx, [rip + NOM_SESSION]
xor edx, edx
mov r8d, LEN_NOM_SESSION
xor r9d, r9d
call FICHIERS
test rax, rax
je .session_ko
lea rcx, [rip + TAMPON_CMD]
mov rdx, rax
lea r8, [rip + ETIQ_LOCATION]
mov r9d, LEN_ETIQ_LOCATION
mov dword ptr [rsp + 0x20], 0x0D
lea rax, [rip + TAMPON_JETON]
mov qword ptr [rsp + 0x28], rax
mov qword ptr [rsp + 0x30], 480
call BALAYEUR
test rax, rax
je .session_ko
lea rcx, [rip + S34A]
mov edx, LEN_S34A
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
; --- televersement : PUT --data-binary @journal (BUF_CHEMIN, I2) ---
xor ebp, ebp
lea r15, [rip + GABARIT_PUT]
call .gab
mov rcx, rbx
xor edx, edx
call LANCEUR
test eax, eax
je .envoi_ko
mov r12, qword ptr [rip + HPROC]
mov rcx, r12
mov edx, 130000
call qword ptr [rip + IAT_WAIT]
mov rcx, r12
lea rdx, [rip + CODE_SORTIE]
call qword ptr [rip + IAT_EXITCODE]
mov rcx, r12
call qword ptr [rip + IAT_CH]
cmp dword ptr [rip + CODE_SORTIE], 0
jne .envoi_ko
lea rcx, [rip + S35A]
mov edx, LEN_S35A
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
lea rcx, [rip + S36A]
mov edx, LEN_S36A
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
mov r14d, 1
jmp .nettoyage
; --- chemins d'echec : ligne KO honnete, verdict KO, nettoyage JAMAIS saute ---
.envoi_ko:
lea rcx, [rip + S35B]
mov edx, LEN_S35B
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
jmp .ko
.jeton_ko:
lea rcx, [rip + S33B]
mov edx, LEN_S33B
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
jmp .ko
.session_ko:
lea rcx, [rip + S34B]
mov edx, LEN_S34B
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
jmp .ko
.jetons_absents:
lea rcx, [rip + S31]
mov edx, LEN_S31
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
.ko:
lea rcx, [rip + S36B]
mov edx, LEN_S36B
xor r8d, r8d
xor r9d, r9d
call JOURNAL_TRACE
xor r14d, r14d
; --- nettoyage : les 5 temporaires contigus (zone donnees 2), un a un ---
.nettoyage:
lea r15, [rip + NOM_REQ]
mov r13d, 5
.nettoie:
mov rcx, r15
mov edx, 2
xor r8d, r8d
.compte_nom:
cmp byte ptr [rcx + r8], 0
je .nom_len
inc r8
jmp .compte_nom
.nom_len:
inc r8
mov r12, r8
xor r9d, r9d
call FICHIERS
add r15, r12
dec r13d
jne .nettoie
mov eax, r14d
jmp .fin
; --- formatteur a marqueurs : 0x01..0x08 -> champ, autre -> octet litteral ---
.gab:
sub rsp, 8
.gab_boucle:
movzx eax, byte ptr [r15]
test eax, eax
je .gab_fin
cmp eax, 8
ja .gab_literal
dec eax
call .champ
call .append
inc r15
jmp .gab_boucle
.gab_literal:
mov byte ptr [rbx + rbp], al
inc rbp
inc r15
jmp .gab_boucle
.gab_fin:
mov byte ptr [rbx + rbp], 0
add rsp, 8
ret
; .champ : eax = 0..7 -> rdx = ptr, r8d = longueur (sans NUL)
; 0..2 = champs 0..2 de TAMPON_JETON (cid, secret, refresh) ;
; 3 = TAMPON_NOM (marqueur \x04) ; 4 = DOSSIER_TEST (\x05) ;
; 5 = BUF_CHEMIN (\x06) ; 6 = TAMPON_JETON (\x07, jeton/URL extraits) ;
; 7 = 4e champ de TAMPON_JETON (\x08, uri des jetons)
.champ:
cmp eax, 3
jae .champ_special
lea rcx, [rip + TAMPON_JETON]
.teste:
test eax, eax
je .champ_ptr
.avance:
cmp byte ptr [rcx], 0
je .nul
inc rcx
jmp .avance
.nul:
inc rcx
dec eax
jmp .teste
.champ_special:
cmp eax, 3
je .champ_nom
cmp eax, 4
je .champ_dossier
cmp eax, 5
je .champ_chemin
cmp eax, 6
je .champ_jeton
mov eax, 3
lea rcx, [rip + TAMPON_JETON]
jmp .teste
.champ_jeton:
lea rdx, [rip + TAMPON_JETON]
jmp .champ_len
.champ_nom:
lea rdx, [rip + TAMPON_NOM]
jmp .champ_len
.champ_dossier:
lea rdx, [rip + DOSSIER_TEST]
jmp .champ_len
.champ_chemin:
lea rdx, [rip + BUF_CHEMIN]
.champ_len:
xor r8d, r8d
.compte:
cmp byte ptr [rdx + r8], 0
je .champ_fin
inc r8
jmp .compte
.champ_ptr:
mov rdx, rcx
jmp .champ_len
.champ_fin:
ret
; .append : rdx = source, r8d = longueur -> [rbx+rbp...], rbp avance
.append:
mov rcx, rbx
add rcx, rbp
push r8
call MEMCPY
pop r8
add rbp, r8
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
