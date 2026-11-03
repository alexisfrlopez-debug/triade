; http-12-principal-r3 · orchestration du proxy — la CLI et la porte M5 · spec http-12:R3 · bloc carte g80003
; Intention : l'orchestrateur scellé lance encore http-10:R2 @0x74C0 (la
; session 0.5.1, qui ne connaît pas le relèvement) et ne sait ni lire une
; ligne de commande ni garder la couche M5. La révision câble la boucle
; d'acceptation sur http-10:R3 @0x81C0 (la session révisée), ARME la
; politique --relever-https à partir des arguments, porte avec elle la
; porte R10 .text4 (marche aux bornes, miroir D95) et nomme la politique
; au journal (« relever-https arme ») quand elle est armée — le processus
; ne démarre JAMAIS en silence avec un drapeau mal orthographié.
; Ancêtre : http-12:R2 (D95, embarquée 0.5.1 @0x7DC0 — spécification m4/I/,
; citée non recopiée T5 ; balise immuable § 9). RENUMÉROTATION (verdict v8) :
; l'intention de D136 disait « http-12:R2 » ; le nom est PRIS par le câblage
; D95 — la révision CLI est http-12:R3, ancêtre http-12:R2.
; pre  : P1 point d'entrée PE — DÉSORMAIS 0x8BC0 (.text4, delta documenté ;
;        les ancêtres @0x7DC0 et @0x1800 restent embarqués octet pour octet,
;        R7, morts au lancement) ; P2 pile alignée rsp ≡ 8 mod 16 ; P3 .data
;        à l'état image (handles nuls, drapeaux nuls, R_POLITIQUE = 0, CS non
;        initialisée).
; post : Q1 porte héritée (28 entrées, fail-closed) ; Q1bis porte M5 (UNE
;        entrée, fail-closed, même contrat) ; Q1ter version >= 0x00040000 ;
;        Q2 LA CLI (GetCommandLineW, refus nommé ExitProcess 3, politique
;        écrite AVANT toute initialisation) ; Q3 initialisation héritée +
;        la ligne de politique entre bannière et écoute ; Q4 la boucle
;        lance http-10:R3 (0x81C0) — l'unique différence fonctionnelle ;
;        Q5 ExitProcess (0 arrêt, 1 intégrité, 2 erreur structurale, 3 refus CLI).
; inv  : I1 IAT GetStdHandle/InitializeCriticalSection/ExitProcess/CloseHandle
;        + GetCommandLineW (LA seule entrée nouvelle) + WSACleanup ; cibles
;        de CODE par lea : http-11 @0x5D80 et http-10:R3 @0x81C0 — JAMAIS
;        0x74C0 ni 0x5580 ; I2 l'ordre d'initialisation est un invariant
;        (D42) — la ligne de politique s'insère entre la bannière et
;        l'écoute ; I3 la porte précède TOUT autre effet ; I4 handles
;        fermés immédiatement ; I5 la couche .text4 gardée par SA PROPRE
;        entrée (la porte se garde elle-même) ; I6 la CLI est lue UNE fois.
; Dépendances : RÉVISION (ancêtre g70011 http-12:R2 embarqué 0.5.1, cité § 9)
; Notation explicite générée par outils/auteur.py depuis brouillons/http-12-principal-r3.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x60
lea rax, [rip + ANCRE]
mov r14, rax
sub r14, 0x2830
lea rbx, [rip + TAB_SUM]
lea r15, [rip + VERSION]
.verif:
cmp rbx, r15
jae .verif_ok
mov edx, dword ptr [rbx]
test edx, edx
je .integrite_ko
mov r13d, dword ptr [rbx + 4]
test r13d, r13d
je .integrite_ko
mov r12, r14
add r12, rdx
xor eax, eax
xor ecx, ecx
.somme:
add rax, qword ptr [r12 + rcx]
add rcx, 8
cmp rcx, r13
jb .somme
cmp rax, qword ptr [rbx + 8]
jne .integrite_ko
add rbx, 16
jmp .verif
.verif_ok:
; Q1bis — la PORTE M5 (miroir D95, même contrat que la marche héritée) :
; UNE entrée (0x8000, 0x2000, somme .text4) de TAB_SUM_M5 à SA BORNE,
; fail-closed sur entrée trouée, la porte se garde elle-même (le bloc
; 0x8C80 est DANS la plage) ; la MÊME boucle est rejouée (aucun état
; caché) : le premier exit atterrit sur VERSION, le second sur BORNE_M5
lea rax, [rip + BORNE_M5]
cmp rbx, rax
je .porte_m5_ok
lea rbx, [rip + TAB_SUM_M5]
lea r15, [rip + BORNE_M5]
jmp .verif
.porte_m5_ok:
mov rax, qword ptr [rip + VERSION]
cmp rax, 0x40000
jb .integrite_ko
; Q2 — LA CLI NAÎT : GetCommandLineW (IAT M5, I1 — LA seule entrée
; nouvelle), l'argument 0 sauté (guillemets ou séparateurs), chaque
; argument suivant comparé BYTE-EXACT (UTF-16, casse sensible) à la
; fixture L"--relever-https" : égal → R_POLITIQUE (.data) = 1 — l'état
; écrit AVANT toute initialisation (l'ordonnanceur n'a pas commencé) ;
; TOUT autre argument non vide → REFUS NOMMÉ (« TRIADE M5 : argument
; inconnu, arret », ExitProcess 3, AUCUN appel réseau, AUCUNE
; initialisation — E4 : le refus est un ÉTAT consigné, jamais un
; démarrage au mieux) ; la commande vide ne nomme rien : R_POLITIQUE
; reste 0 (le chemin scellé)
call qword ptr [rip + IAT_GCLW]
mov r12, rax
cmp word ptr [r12], 0x22
jne .cmd_arg0
; Q2 — arg0 entre guillemets : le saut court à la guillemet FERMANTE
; (un chemin cité contient des espaces — c'est sa raison d'être : « C:
; \Program Files\… ») ; ligne finie sans fermante → .cmd_fin (la commande
; ne nomme rien, R_POLITIQUE reste 0)
.cmd_quote:
add r12, 2
cmp word ptr [r12], 0
je .cmd_fin
cmp word ptr [r12], 0x22
jne .cmd_quote
jmp .cmd_apres_arg0
.cmd_arg0:
cmp word ptr [r12], 0
je .cmd_fin
cmp word ptr [r12], 0x22
je .cmd_apres_arg0
cmp word ptr [r12], 0x20
je .cmd_suivant
cmp word ptr [r12], 0x09
je .cmd_suivant
add r12, 2
jmp .cmd_arg0
.cmd_apres_arg0:
add r12, 2
.cmd_suivant:
cmp word ptr [r12], 0
je .cmd_fin
cmp word ptr [r12], 0x20
je .cmd_sep
cmp word ptr [r12], 0x09
je .cmd_sep
lea r13, [rip + CMD_RELEVER]
xor r14d, r14d
.cmd_cmp:
movzx eax, word ptr [r12 + r14*2]
cmp ax, word ptr [r13 + r14*2]
jne .cmd_inconnu
add r14d, 1
cmp r14d, 15
jb .cmd_cmp
movzx eax, word ptr [r12 + 30]
test eax, eax
je .cmd_relever
cmp ax, 0x20
je .cmd_relever
cmp ax, 0x09
je .cmd_relever
.cmd_inconnu:
; E4 — le refus NOMMÉ par hello-02 (GSH propre, miroir .integrite_ko —
; JAMAIS tcp-11 : sa P5 exige la section critique .data INITIALISÉE et le
; handle stdout consigné, or E4 précède TOUTE initialisation — un appel
; avant l'état serait une faute de contrat) ; AUCUNE initialisation n'a
; eu lieu (I3 : la CLI AVANT tout effet réseau), AUCUN appel réseau
mov ecx, -11
call qword ptr [rip + IAT_GSH]
mov rcx, rax
lea rdx, [rip + TXT_CMD_KO]
mov r8d, 37
call WRITE
mov ecx, 3
call qword ptr [rip + IAT_EP]
.cmd_relever:
mov qword ptr [rip + POLITIQUE], 1
add r12, 30
jmp .cmd_suivant
.cmd_sep:
add r12, 2
jmp .cmd_suivant
.cmd_fin:
; Q3 — l'initialisation est l'héritage R1/R2 TEL QUEL (ordre I2)
mov ecx, -11
call qword ptr [rip + IAT_GSH]
mov qword ptr [rip + STDOUT], rax
mov ecx, -10
call qword ptr [rip + IAT_GSH]
mov qword ptr [rip + STDIN], rax
lea rcx, [rip + CS]
call qword ptr [rip + IAT_ICS]
lea rcx, [rip + MSG_BANNIERE]
mov edx, 40
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call TCP_JOURNAL
; I2/Q3 — SI R_POLITIQUE == 1 : la ligne console de l'état nommé
; (« relever-https arme »), UNE fois, AVANT toute écoute
cmp qword ptr [rip + POLITIQUE], 1
jne .sans_politique
lea rcx, [rip + TXT_POLITIQUE]
mov edx, 20
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call TCP_JOURNAL
.sans_politique:
call TCP_INIT
test rax, rax
je .erreur_reseau
mov qword ptr [rip + LISTEN], rax
lea rcx, [rip + CONSOLE]
xor edx, edx
call TCP_SPAWN
test rax, rax
je .erreur_reseau
mov rcx, rax
call qword ptr [rip + IAT_CH]
.boucle:
mov rcx, qword ptr [rip + LISTEN]
call TCP_ACCEPT
mov r12, rax
test rax, rax
js .accept_echec
lea rcx, [rip + SESSION_R3]
mov rdx, r12
call TCP_SPAWN
test rax, rax
je .erreur_reseau
mov rcx, rax
call qword ptr [rip + IAT_CH]
jmp .boucle
.accept_echec:
cmp qword ptr [rip + QUIT], 0
jne .arret
.erreur_reseau:
lea rcx, [rip + MSG_ERREUR]
mov edx, 22
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call TCP_JOURNAL
mov ecx, 2
call qword ptr [rip + IAT_EP]
.arret:
lea rcx, [rip + MSG_ARRET]
mov edx, 7
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call TCP_JOURNAL
call qword ptr [rip + IAT_WSACLEANUP]
xor ecx, ecx
call qword ptr [rip + IAT_EP]
.integrite_ko:
mov ecx, -11
call qword ptr [rip + IAT_GSH]
mov rcx, rax
lea rdx, [rip + MSG_KO]
mov r8d, 33
call WRITE
mov ecx, 1
call qword ptr [rip + IAT_EP]
