; http-12-principal-r2 · bloc orchestration proxy (point d'entrée) · révision du bloc e50012
; Ancêtre : http-12:R1 (D45, scellé 0.4.0 — spec m3/I/http-12-principal.md, citée
; non recopiée T5 ; balise immuable § 9). La révision CÂBLE le routage (Q3) et
; FERME la porte (Q1) — elle ne touche à rien d'autre : l'initialisation est
; l'héritage R1 instruction pour instruction (à la géométrie du plan près).
; pre  : P1 point d'entrée PE — DÉSORMAIS 0x7DC0 (.text3, delta documenté ;
;        l'ancêtre @0x1800 reste embarqué octet pour octet, R7, mort au
;        lancement) ; P2 pile alignée rsp ≡ 8 mod 16 ; P3 .data à l'état image.
; post : Q1 porte R10 RÉVISÉE — marche de TAB_SUM (0x2660) à la BORNE
;        (l'ADRESSE de VERSION, 0x2820 — jamais son contenu avant la fin de
;        marche) : 28 entrées, TOUTE entrée d'rva nul ou de taille nulle est
;        un ÉCHEC (la table est PLEINE : un trou nomme une corruption —
;        fail-closed renforcé, la troncature silencieuse du terminateur M3
;        n'existe plus) ; somme 64 bits des qwords == somme attendue ; puis
;        version >= 0x00040000 (plancher M3, monotonie) ; écart → ligne KO
;        par hello-02, ExitProcess(1), AUCUN appel réseau ;
;        Q2 initialisation HÉRITAGE R1 TEL QUEL (ordre I2 : GSH -11, GSH -10,
;        InitCS, bannière, tcp-01 écoute, thread console tcp-06 sur http-11,
;        handle fermé) ; Q3 boucle : accept ; socket valide → tcp-06 sur
;        SESSION_R2 (0x74C0 — http-10:R2, LE CÂBLAGE, l'unique différence
;        fonctionnelle) avec la socket, handle fermé, boucle ; échec accept :
;        R_QUIT posé → journal « arret », WSACleanup, ExitProcess(0) ; sinon →
;        journal « erreur reseau, arret », ExitProcess(2) ; Q4 héritage : le
;        processus finit TOUJOURS par ExitProcess (0/1/2).
; inv  : I1 IAT GSH/InitCS/ExitProcess/CloseHandle + WSACleanup ; appels
;        directs hello-02 (WRITE), tcp-01 (TCP_INIT), tcp-02 (TCP_ACCEPT),
;        tcp-06 (TCP_SPAWN), tcp-11 (TCP_JOURNAL) ; cibles CODE par lea :
;        CONSOLE (0x5D80) et SESSION_R2 (0x74C0) — JAMAIS 0x5580 (I1 de la
;        spec : le contre-câblage est la falsification nominale de V4) ;
;        I3 la porte précède tout effet ; I4 handles fermés immédiatement ;
;        I5 la porte .text3 garde [0x6000, 0x2000] — le bloc 0x7DC0 est DANS
;        la plage : la porte se garde elle-même (miroir R1 @0x1800, table M3) ;
;        rien stocké sous rsp.
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
mov rax, qword ptr [rip + VERSION]
cmp rax, 0x40000
jb .integrite_ko
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
lea rcx, [rip + SESSION_R2]
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
