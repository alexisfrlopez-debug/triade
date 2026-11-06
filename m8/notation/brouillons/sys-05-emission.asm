; sys-05-emission · l'émission du transport · spec sys-05:R2 · bloc carte g90005
; LE GESTE D'ÉMISSION du socle socket : IOCTL_AFD_SEND par syscall direct
; (I1 : AUCUN IAT — le send SANS ws2_32.send, la règle structurelle TENUE).
; LA RÈGLE DU KIT (Q1/Q2) : l'émission est TOTALE ou refusée — le compteur
; du IOSB doit COUVRIR la longueur demandée, un envoi partiel est LE REFUS
; -7 NOMMÉ (rdx = le compte Information consigné), JAMAIS une boucle
; silencieuse (une boucle d'envoi serait une décision de transport que le
; domaine n'a pas). AUCUNE COPIE (I2) : le WSABUF de pile pointe LA CHARGE
; DU KIT (P3 traverse), les octets appartiennent à l'appelant. Les
; constantes au plan (m8/layout.py — T5 : l'IOCTL DÉRIVÉ par la macro
; canonique, jamais un littéral hors plan) ; le harnais re-vérifie.
; La garde d'abord (charte § 5, fail-closed) : le span invalide = -5 AVANT
; tout (P3 nul ou P4 nul — aucun syscall émis) ; PUIS la résolution au
; geste même (I3/I5), PUIS l'émission. Le cadre 0x88 (4 pushes + 0x88 ≡ 0
; mod 16 aux sites) : l'ombre 0x20, les SIX arguments de pile du ioctl
; (0x30), l'IOSB (0x10), le WSABUF (0xC), l'AFD_SEND_INFO (0x18) — zones
; mortes au retour (I7 : le bloc ne détient AUCUN état, chaque émission
; est un geste neuf). rbx le handle, rbp la base, rdi la charge, rsi la
; longueur (I6 : les non-volatils sauvés et rendus).
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
; I3 : le SSN de « NtDeviceIoControlFile » résolu AU GESTE MÊME (sys-02,
; jamais un cache — charte § 6) ; I5 : un échec = AUCUN syscall
lea rcx, [rip + NOM_DEVICEIOCTL]
mov edx, 21
mov r8, rbp
call SYS02
test rax, rax
js .resolution_echouee
; Q3/I2 : le WSABUF (12 o — len u32 + buf ptr, la MESURE p.3) et
; l'AFD_SEND_INFO (24 o) sur la PILE du bloc : BufferArray pointe le
; WSABUF, le WSABUF pointe LA CHARGE DU KIT, BufferCount 1, AfdFlags 0,
; TdiFlags 0 (LA MESURE : aucun drapeau, le Fast I/O du noyau)
mov dword ptr [rsp + 0x60], esi
mov qword ptr [rsp + 0x68], rdi
lea r10, [rsp + 0x60]
mov qword ptr [rsp + 0x70], r10
mov dword ptr [rsp + 0x78], 1
mov dword ptr [rsp + 0x7C], 0
mov dword ptr [rsp + 0x80], 0
; Q4 : les DIX arguments NT dans l'ordre — handle, Event NULL, ApcRoutine
; NULL, ApcContext NULL, l'IOSB de pile, l'IOCTL du plan, l'AFD_SEND_INFO
; de pile, 24, NULL, 0 (aucune sortie attendue : la réponse est le IOSB)
mov rcx, rbx
xor edx, edx
xor r8d, r8d
xor r9d, r9d
lea r10, [rsp + 0x50]
mov qword ptr [rsp + 0x20], r10
mov qword ptr [rsp + 0x28], 0x1201F
lea r10, [rsp + 0x70]
mov qword ptr [rsp + 0x30], r10
mov qword ptr [rsp + 0x38], 0x18
mov qword ptr [rsp + 0x40], 0
mov qword ptr [rsp + 0x48], 0
call SYS01
; Q5 : 0 NOMMÉ ; -6 le STATUS brut en rdx, -6 la divergence iosb (le
; noyau ne parle pas deux fois)
test eax, eax
jne .status_nonnul
cmp dword ptr [rsp + 0x50], 0
jne .status_iosb
; Q1/Q2 : le compteur doit ÉGALEMENT la longueur demandée — TOUT est
; émis ; sinon l'émission PARTIELLE est LE REFUS -7 (le compte en rdx,
; consigné, jamais muet — le kit tranche de la suite)
cmp qword ptr [rsp + 0x58], rsi
jne .emission_partielle
xor eax, eax
add rsp, 0x88
pop rsi
pop rdi
pop rbp
pop rbx
ret
.emission_partielle:
mov rdx, qword ptr [rsp + 0x58]
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
