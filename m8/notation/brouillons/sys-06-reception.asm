; sys-06-reception · la réception du transport · spec sys-06:R3 · bloc carte g90006
; Révision 3 (l'erratum n° 10 — LE TERRAIN A JUGÉ LA MESURE, la sonde
;   sys-06 Entrée 191) : le VRAI noyau REFUSE le bit 0x20 dans AfdFlags
;   (STATUS_INVALID_PARAMETER, trois lectures identiques) — TDI_RECEIVE_
;   NORMAL (0x20) RETOURNE au champ TdiFlags (la littérature avait raison
;   du placement), AfdFlags = 0 ; le MÊME encode, le slot intact.
; Révision 2 (l'erratum n° 9, le miroir de la sonde sys-05 — Entrée 185) :
;   le WSABUF canonique 16 o (buf à +8), JAMAIS un « packé » de 12 o.
; LE GESTE DE RÉCEPTION du socle socket : IOCTL_AFD_RECEIVE par syscall
; direct, la lecture BLOQUANTE sur le handle SYNCHRONE (posé par sys-04 —
; Q1 : le syscall ATTEND les données, jamais un compte nul silencieux).
; LE ZÉRO EST LA DEMI-FIN (Q2) : une lecture qui rend zéro octet (le pair
; a fermé proprement) est LE REFUS -7 NOMMÉ (rdx = 0), jamais un succès
; masqué — l'ÉVÉNEMENT TRANSPORT que le kit tranche. AUCUNE COPIE (I2) :
; le noyau ÉCRIT DIRECTEMENT chez l'appelant (le WSABUF pointe LE TAMPON
; DU KIT, P3 traverse) ; I8 : le reçu est INTÈGRE (le bloc ne touche
; JAMAIS les octets écrits par le noyau). L'ERRATUM n° 10 (LE TERRAIN A
; JUGÉ LA MESURE — le modèle libc-02 tenu) : TDI_RECEIVE_NORMAL (0x20)
; vit au champ TdiFlags (+16) — LE TERRAIN l'a tranché (la sonde
; sys-06, Entrée 191 : le VRAI noyau REFUSE le 0x20 posé en AfdFlags —
; STATUS_INVALID_PARAMETER, trois fois ; la révision 2 avait suivi la
; mesure WinDbg citée, le noyau réel a le dernier mot) ; les
; constantes au plan (m8/layout.py — T5), le harnais re-vérifie. La garde
; d'abord : -5 le span invalide (P3/P4 nuls — aucun syscall) ; le cadre
; 0x88 comme sys-05 (l'ombre, SIX arguments de pile, l'IOSB, le WSABUF,
; l'AFD_RECV_INFO — zones mortes au retour, I7 : AUCUN état, aucun reste
; de lecture : ce que le noyau n'a pas livré appartient à SA file).
test r8, r8
je .span_invalide
test r9, r9
je .span_invalide
push rbx
push rbp
push rdi
push rsi
sub rsp, 0x88
mov rbp, rcx
mov rbx, rdx
mov rdi, r8
mov rsi, r9
; I3 : le SSN résolu AU GESTE MÊME (sys-02, jamais un cache — charte § 6)
; ; I5 : un échec = AUCUN syscall émis
lea rcx, [rip + NOM_DEVICEIOCTL]
mov edx, 21
mov r8, rbp
call SYS02
test rax, rax
js .resolution_echouee
; Q3/I2 : le WSABUF (12 o) porte LA CAPACITÉ et LE TAMPON DU KIT ;
; l'AFD_RECV_INFO (24 o) : BufferArray le WSABUF de pile, BufferCount 1,
; AfdFlags = 0, TdiFlags = TDI_RECEIVE_NORMAL 0x20 (L'ERRATUM n° 10 :
; LE TERRAIN A JUGÉ — le VRAI noyau refuse le 0x20 en AfdFlags, le
; QUATRIÈME champ le porte, le placement de la littérature)
mov dword ptr [rsp + 0x60], esi
mov qword ptr [rsp + 0x68], rdi
lea r10, [rsp + 0x60]
mov qword ptr [rsp + 0x70], r10
mov dword ptr [rsp + 0x78], 1
mov dword ptr [rsp + 0x7C], 0
mov dword ptr [rsp + 0x80], 0x20
; Q4 : les DIX arguments NT dans l'ordre — handle, Event NULL (le handle
; synchrone : le syscall ATTEND), ApcRoutine NULL, ApcContext NULL,
; l'IOSB de pile, l'IOCTL du plan, l'AFD_RECV_INFO de pile, 24, NULL, 0
mov rcx, rbx
xor edx, edx
xor r8d, r8d
xor r9d, r9d
lea r10, [rsp + 0x50]
mov qword ptr [rsp + 0x20], r10
mov qword ptr [rsp + 0x28], 0x12017
lea r10, [rsp + 0x70]
mov qword ptr [rsp + 0x30], r10
mov qword ptr [rsp + 0x38], 0x18
mov qword ptr [rsp + 0x40], 0
mov qword ptr [rsp + 0x48], 0
call SYS01
; Q5 : -6 le STATUS brut consigné en rdx (p. ex. STATUS_CONNECTION_RESET :
; le pair a coupé BRUTALEMENT — le STATUS le NOMME), -6 la divergence
; iosb (le noyau ne parle pas deux fois)
test eax, eax
jne .status_nonnul
cmp dword ptr [rsp + 0x50], 0
jne .status_iosb
; Q1 : n = le compte du IOSB (Information), n ≥ 1 au succès ; Q2 : LE
; ZÉRO EST LA DEMI-FIN — le refus -7 NOMMÉ, rdx consigne le compte nul
mov rax, qword ptr [rsp + 0x58]
test rax, rax
jz .demi_fin
; n rendu (le tampon du kit contient les n octets du noyau — I8 : le
; bloc ne les a JAMAIS touchés) ; la pile rendue propre au retour
add rsp, 0x88
pop rsi
pop rdi
pop rbp
pop rbx
ret
.demi_fin:
xor edx, edx
mov rax, -7
jmp .epilogue
.status_nonnul:
mov rdx, rax
mov rax, -6
jmp .epilogue
.status_iosb:
mov edx, dword ptr [rsp + 0x50]
mov rax, -6
jmp .epilogue
.resolution_echouee:
mov rdx, rax
mov rax, -1
.epilogue:
add rsp, 0x88
pop rsi
pop rdi
pop rbp
pop rbx
ret
; Q5 : -5 le span invalide, AUCUN syscall émis (la garde d'abord)
.span_invalide:
mov rax, -5
ret
