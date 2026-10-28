; tls-04 · poignée de main cliente · spec tls-04:R1 · bloc carte g70004
; pre : rcx pointe le cadre de session TLS (offsets documentés layout.CADRE_*)
;       — credentials ACQUIS par tls-05 (op 0), contexte à zéro, socket
;       serveur connectée par tcp-13 (P3 : vierge de tout octet échangé),
;       nom cible UTF-16 déjà traduit par tls-01 (pointeur @+0x28, I4)
; post : rax = 0 — contexte ÉTABLI (Q1 : handle écrit PAR ISC via
;       phNewContext @+0x10, prêt pour tls-06/07 ; nombre d'allers-retours
;       consigné @+0x38 en u16) ; rax non nul — verdict tls-02 (Q2 : le cadre
;       porte verdict @+0x30 ET HRESULT d'origine @+0x34 ; le contexte reste
;       dans l'état où la bibliothèque l'a laissé — I3 : la compensation
;       des handles appartient à tls-05/tls-08, JAMAIS ici)
; inv : I1 boucle bornée MAX_ALLERS = 16 — au-delà verdict 5 « poignée
;       interminable » (E5 : elle se termine TOUJOURS) ; I2 zéro octet de
;       jeton journalisé (aucune console ici — les états nommés vivent en
;       tls-08) ; I3 AUCUNE fermeture de socket, AUCUNE libération de
;       handle — seule entrée IAT : InitializeSecurityContextW (tcp-03/04
;       sont des appels de blocs, pas d'IAT nouvelles) ; I4 nom lu tel quel
;       (traduction tls-01 jamais refaite) ; I5 volatils seuls modifiés —
;       cadre et longueurs sauvegardés dans la PILE de travail
; ABI : msx64 — InitializeSecurityContextW = 11 arguments (4 registres +
;       7 pile, sub rsp 0xB8 aligne la frontière) ; fContextReq = 0xC01C
;       (layout.ISC_REQUETES — STREAM pour tls-03:1/tls-06/07, JAMAIS
;       MANUAL_CRED_VALIDATION [charte § 2] ni ALLOCATE_MEMORY [les jetons
;       vivent dans le cadre, pas en mémoire de bibliothèque]) ;
;       TargetDataRep 0 (Schannel l'ignore) ; pile de travail : envoyé
;       @rsp+0x20 / destination @rsp+0x28 (morts comme arguments Reserved1/
;       TargetDataRep après l'appel — réutilisés par la boucle d'émission
;       après coup), pfContextAttr @rsp+0x58 réécrit 0 avant chaque appel
;       (aucun état résiduel), cadre @rsp+0x60, longueur entrée @rsp+0x68,
;       descripteurs ENTRÉE @rsp+0x70 / SORTIE @rsp+0x90 (tls-03 type 0 —
;       reconstruits à chaque tour) ; le jeton produit vit en zone ÉMISSION
;       (capacité MAX_JETON, ISC met à jour cbBuffer), le jeton serveur
;       s'accumule en zone RÉCEPTION (capacité restante — garde E2 AVANT
;       toute réception complémentaire, avant tout appel SSPI)
sub rsp, 0xB8
mov qword ptr [rsp + 0x60], rcx
mov word ptr [rcx + 0x38], 0
mov qword ptr [rsp + 0x68], 0
mov dword ptr [rsp + 0x58], 0

; --- une itération = UN aller-retour : garde E5, descripteurs, ISC, verdict ---
.boucle:
mov rax, [rsp + 0x60]
movzx ecx, word ptr [rax + 0x38]
cmp ecx, 16
jae .interminable
inc word ptr [rax + 0x38]
; descripteur SORTIE (jeton client à produire — capacité MAX_JETON)
xor ecx, ecx
lea rdx, [rax + 0x260]
mov r8d, 16384
lea r9, [rsp + 0x90]
call TLS_JETONS
; descripteur ENTRÉE (jeton serveur accumulé) — absent au PREMIER appel (Q4)
cmp qword ptr [rsp + 0x68], 0
je .premier
mov rax, [rsp + 0x60]
xor ecx, ecx
lea rdx, [rax + 0x4260]
mov r8, [rsp + 0x68]
lea r9, [rsp + 0x70]
call TLS_JETONS

; --- InitializeSecurityContextW : 11 arguments (4 registres + 7 pile) ---
; r11 porte le défaut pInput NULL (jamais eax — rax est le CADRE, il sert
; encore à phContext puis à phNewContext : un volatile ne s'écrase pas
; entre deux usages sans être rechargé — le differentiel l'a nommé)
.premier:
mov rax, [rsp + 0x60]
mov rcx, rax
xor edx, edx
xor r11d, r11d
cmp qword ptr [rsp + 0x68], 0
jz .sans_entree
lea rdx, [rax + 0x10]
lea r11, [rsp + 0x70]
.sans_entree:
mov [rsp + 0x30], r11
mov r8, [rax + 0x28]
mov r9d, 0xC01C
mov qword ptr [rsp + 0x20], 0
mov qword ptr [rsp + 0x28], 0
mov qword ptr [rsp + 0x38], 0
lea rax, [rax + 0x10]
mov [rsp + 0x40], rax
lea rax, [rsp + 0x90]
mov [rsp + 0x48], rax
lea rax, [rsp + 0x58]
mov [rsp + 0x50], rax
mov dword ptr [rsp + 0x58], 0
call qword ptr [rip + IAT_ISC]
movsxd rcx, eax
call TLS_VERDICTS
mov r10, [rsp + 0x60]
mov dword ptr [r10 + 0x34], edx
test eax, eax
jz .etabli
cmp eax, 1
je .continuer
cmp eax, 2
je .incomplet
jmp .echec_nomme

; --- verdict 1 : CONTINUE_NEEDED — l'entrée est consommée, l'aller continue ---
.continuer:
mov qword ptr [rsp + 0x68], 0
mov qword ptr [rsp + 0x28], 0
mov eax, [rsp + 0xA0]
test eax, eax
jnz .emettre
jmp .recevoir

; --- verdict 2 : INCOMPLETE — recevoir davantage (garde E2 AVANT réception) ---
.incomplet:
cmp qword ptr [rsp + 0x68], 16384
jae .hors_borne

; --- réception : UN tcp-03 par tour, accumulation au sommet (Q3, E4) ---
.recevoir:
mov rdx, [rsp + 0x60]
mov rcx, [rdx + 0x20]
lea rdx, [rdx + 0x4260]
add rdx, [rsp + 0x68]
mov r8d, 16384
sub r8, [rsp + 0x68]
call TCP_RECV
test rax, rax
jle .reception_rompue
add qword ptr [rsp + 0x68], rax
jmp .boucle

; --- verdict 0 : SEC_E_OK — contexte ÉTABLI (jeton final émis si produit) ---
.etabli:
mov qword ptr [rsp + 0x28], 1
mov eax, [rsp + 0xA0]
test eax, eax
jnz .emettre
jmp .succes

; --- émission intégrale du jeton produit (boucle d'achèvement bornée, E3) ---
; r8 porte l'ENVOYÉ pour l'adresse (zone + envoyé) puis RESTANT pour tcp-04
; (la longueur de l'appel — jamais l'envoyé : c'est le restant qui décrémente)
.emettre:
mov qword ptr [rsp + 0x20], 0
.boucle_envoi:
mov eax, [rsp + 0xA0]
mov r8, [rsp + 0x20]
sub rax, r8
jz .emis
mov rdx, [rsp + 0x60]
mov rcx, [rdx + 0x20]
lea rdx, [rdx + 0x260]
add rdx, r8
mov r8, rax
call TCP_SEND
test rax, rax
jle .emission_rompue
add qword ptr [rsp + 0x20], rax
jmp .boucle_envoi
.emis:
cmp qword ptr [rsp + 0x28], 0
jne .succes
jmp .recevoir

; --- fins : succès, échecs nommés (Q2/E1) et système (E2..E5) ---
.succes:
mov rax, [rsp + 0x60]
mov dword ptr [rax + 0x30], 0
xor eax, eax
add rsp, 0xB8
ret
.interminable:
mov eax, 5
jmp .echec
.hors_borne:
mov eax, 5
jmp .echec
.emission_rompue:
mov eax, 5
jmp .echec
.reception_rompue:
mov eax, 5
jmp .echec
.echec_nomme:
.echec:
mov rdx, [rsp + 0x60]
mov [rdx + 0x30], eax
add rsp, 0xB8
ret
