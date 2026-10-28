; tls-06 · émission chiffrée · spec tls-06:R1 · bloc carte g70006
; pre : rcx pointe le cadre de session TLS (offsets documentés layout.CADRE_*)
;       — contexte ÉTABLI par tls-04 (tls-06 n'est appelé qu'après succès de
;       la poignée : phContext @+0x10 vivant), socket serveur connectée
;       @+0x20 (propriétaire tls-08 — jamais fermée ici, I1) ;
;       rdx pointe le span clair à émettre (propriété de http-10:R2 — les
;       octets ne sont JAMAIS modifiés, Q3 : le chiffrement se fait sur la
;       COPIE, dans la zone d'émission du cadre) ;
;       r8 contient la longueur du span (u64, PEUT ÊTRE 0 : un enregistrement
;       vide est légal et n'a AUCUN cas spécial — la boucle est do-while) ;
;       zone d'émission @+0x260 capacité MAX_JETON : en-tête + message
;       maximal + queue (P1 — précondition de l'APPELANT propriétaire du
;       cadre, hors contrat ici)
; post : rax = 0 — le span a été émis INTÉGRALEMENT en enregistrements
;       chiffrés (Q1 : chaque morceau ≤ message maximal NÉGOCIÉ — jamais une
;       constante, charte § 8 ; chaque enregistrement = copie libc-01 vers
;       zone+en-tête, descripteur tls-03 type 1, EncryptMessageW, émission
;       tcp-04 en boucle d'achèvement bornée — modèle http-09 : jamais
;       fermer, toujours finir) ; rax non nul — verdict tls-02 nommé (E1) ou
;       5 « émission rompue » (E2), le cadre porte le verdict @+0x30 et
;       l'HRESULT d'origine @+0x34 ; AUCUN octet clair ne subsiste en zone
;       d'émission à la fin de l'appel (Q2 : sur échec EM le clair copié est
;       DÉTRUIT par memset — le chiffré qui survit à un succès est de la
;       mémoire morte, réutilisée à l'appel suivant)
; inv : I1 aucune fermeture de socket (tls-08 seul propriétaire) ; I2 zéro
;       octet journalisé, clair OU chiffré (charte § 3) ; I3 QueryContext-
;       AttributesW appelé AU PLUS UNE fois par session (P4 : la garde
;       cBuffers @+0x4C — acquis ⟺ non nul ; deux appels = défaut) ; I4
;       aucune écriture hors zone d'émission et cadre (le descripteur vit
;       dans la PILE de travail) ; I5 volatils seuls modifiés — cadre et
;       longueurs sauvegardés dans la pile
; ABI : msx64 — QueryContextAttributesW = 3 arguments registre (phContext
;       cadre+0x10, ulAttribute 4 = SECPKG_ATTR_STREAM_SIZES VÉRIFIÉ À LA
;       SOURCE D84, pBuffer cadre+0x40 : SecPkgContext_StreamSizes 5 × u32
;       {en-tête, queue, message maximal, cBuffers, cbBlockSize}) ;
;       EncryptMessageW = 4 arguments registre (phContext cadre+0x10, fQOP 0,
;       pMessage = descripteur de pile, MessageSeqNo 0) ; tls-03 type 1 = 5e
;       argument à [rsp+0x20] (adresse des tailles — convention cadre
;       contigu : en-tête AVANT le clair, queue APRÈS) ; pile de travail :
;       tailles-arg @rsp+0x20, verdict sauvé @rsp+0x58, cadre @rsp+0x60,
;       span courant @rsp+0x68, restant @rsp+0x70, morceau @rsp+0x78, envoyé
;       @rsp+0x80, total @rsp+0x88, descripteur @rsp+0x90 (64 o) — sub rsp
;       0xE8 aligne la frontière ; libc-01 copie / libc-07 neutralisation /
;       tcp-04 émission = appels de blocs scellés (R7), tls-02 route chaque
;       HRESULT (volatils morts au retour : le cadre est RECHARGÉ de la pile
;       après chaque appel)
sub rsp, 0xE8
mov qword ptr [rsp + 0x60], rcx
mov qword ptr [rsp + 0x68], rdx
mov qword ptr [rsp + 0x70], r8

; --- P4 : tailles de flux acquises UNE fois par session (cBuffers non nul) ---
mov rax, [rsp + 0x60]
cmp dword ptr [rax + 0x4C], 0
jne .tailles
lea rcx, [rax + 0x10]
mov edx, 4
lea r8, [rax + 0x40]
call qword ptr [rip + IAT_QCA]
movsxd rcx, eax
call TLS_VERDICTS
mov r10, [rsp + 0x60]
mov dword ptr [r10 + 0x34], edx
test eax, eax
jz .acquises
; E3 : zéro défensif du bloc tailles (la bibliothèque peut barbouiller en
; échec — tls-05 modèle D82) ; AUCUN enregistrement entamé
mov qword ptr [r10 + 0x40], 0
mov qword ptr [r10 + 0x48], 0
mov dword ptr [r10 + 0x50], 0
jmp .echec
.acquises:
.tailles:

; --- un morceau = UN enregistrement (do-while : longueur 0 → enregistrement vide, P3) ---
.morceau:
mov rax, [rsp + 0x60]
mov r11d, [rax + 0x48]
mov rax, [rsp + 0x70]
cmp rax, r11
jbe .borne
mov rax, r11
.borne:
mov [rsp + 0x78], rax

; copie libc-01 du morceau vers la zone d'émission, APRÈS l'en-tête
mov rax, [rsp + 0x60]
mov ecx, [rax + 0x40]
lea rcx, [rax + rcx + 0x260]
mov rdx, [rsp + 0x68]
mov r8, [rsp + 0x78]
call MEMCPY

; descripteur tls-03 type 1 SUR la copie (le clair référencé vit en zone)
mov rax, [rsp + 0x60]
lea r11, [rax + 0x40]
mov [rsp + 0x20], r11
mov ecx, [rax + 0x40]
lea rdx, [rax + rcx + 0x260]
mov r8, [rsp + 0x78]
lea r9, [rsp + 0x90]
mov ecx, 1
call TLS_JETONS

; EncryptMessageW : chiffrement SUR PLACE dans la zone (le clair de
; l'appelant n'existe que chez l'appelant — Q3)
mov rax, [rsp + 0x60]
lea rcx, [rax + 0x10]
xor edx, edx
lea r8, [rsp + 0x90]
xor r9d, r9d
call qword ptr [rip + IAT_EM]
movsxd rcx, eax
call TLS_VERDICTS
mov r10, [rsp + 0x60]
mov dword ptr [r10 + 0x34], edx
test eax, eax
jnz .em_echec

; total de l'enregistrement : les TROIS cbBuffer APRÈS l'appel (la
; bibliothèque consigne les longueurs produites — leçon D83 (d))
mov eax, [rsp + 0xA0]
mov ecx, [rsp + 0xB0]
add eax, ecx
mov ecx, [rsp + 0xC0]
add eax, ecx
mov [rsp + 0x88], rax
xor eax, eax
mov [rsp + 0x80], rax

; émission tcp-04 en boucle d'achèvement bornée (E2 : jamais sur une
; socket morte — le RESTANT en argument, jamais l'envoyé)
.boucle_envoi:
mov rax, [rsp + 0x88]
mov r8, [rsp + 0x80]
sub rax, r8
jz .emis
mov rdx, [rsp + 0x60]
mov rcx, [rdx + 0x20]
lea rdx, [rdx + 0x260]
add rdx, r8
mov r8, rax
call TCP_SEND
test rax, rax
jle .rompue
add qword ptr [rsp + 0x80], rax
jmp .boucle_envoi

; morceau suivant (le drapeau du sub décide — mov ne touche pas les fanions)
.emis:
mov rax, [rsp + 0x68]
add rax, [rsp + 0x78]
mov [rsp + 0x68], rax
mov rax, [rsp + 0x70]
sub rax, [rsp + 0x78]
mov [rsp + 0x70], rax
jnz .morceau

; Q1 : émission intégrale réussie
mov rax, [rsp + 0x60]
mov dword ptr [rax + 0x30], 0
xor eax, eax
add rsp, 0xE8
ret

; E1 : le verdict est sauvé, le clair copié est DÉTRUIT en zone (Q2 : aucun
; octet clair résiduel), puis l'échec nommé remonte
.em_echec:
mov dword ptr [rsp + 0x58], eax
mov rdx, [rsp + 0x60]
lea rcx, [rdx + 0x260]
mov r8d, [rdx + 0x40]
add r8d, [rdx + 0x44]
mov rax, [rsp + 0x78]
add r8d, eax
xor edx, edx
call MEMSET
mov eax, [rsp + 0x58]
jmp .echec

; E2 : socket morte en cours d'émission — tunnel rompu proprement
.rompue:
mov eax, 5
.echec:
mov rdx, [rsp + 0x60]
mov [rdx + 0x30], eax
add rsp, 0xE8
ret
