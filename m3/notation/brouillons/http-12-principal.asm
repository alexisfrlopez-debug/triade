; http-12-principal · brouillon · orchestration du proxy — point d'entrée de
; proxy.exe · http-12:R1 · e50012
; porte R10 AVANT tout effet (I3) : table d'intégrité (sommes 64 bits des
; qwords par bloc scellé embarqué) + version >= 0x00040000 (plancher M3),
; échec -> ligne « integrite KO » par hello-02 puis ExitProcess(1), AUCUN
; appel réseau ; init DANS L'ORDRE CONTRACTUEL (I2 — leçon D42) : handles,
; section critique EN TÊTE, bannière, écoute, console ; boucle d'acceptation :
; chaque connexion reçoit son thread session http-10 (le journal « connexion
; entrante » est délégué à http-10:Q6) ; WSACleanup sur le chemin propre
; uniquement (Q4) ; sorties 0/1/2 par ExitProcess (Q4).
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x60
; --- porte R10 : base d'image par ancre RIP-relative ---
lea rax, [rip + ANCRE]
mov r14, rax
sub r14, 0x2830
lea rbx, [rip + TAB_SUM]
.verif:
mov edx, dword ptr [rbx]
test edx, edx
je .verif_ok
mov r13d, dword ptr [rbx + 4]
test r13d, r13d
je .entree_suivante
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
.entree_suivante:
add rbx, 16
jmp .verif
.verif_ok:
mov rax, qword ptr [rip + VERSION]
cmp rax, 0x40000
jb .integrite_ko
; --- initialisation dans l'ordre (I2 : handle -> CS -> bannière -> écoute -> console)
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
; --- boucle d'acceptation : thread session par connexion ---
.boucle:
mov rcx, qword ptr [rip + LISTEN]
call TCP_ACCEPT
mov r12, rax
test rax, rax
js .accept_echec
lea rcx, [rip + SESSION]
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
