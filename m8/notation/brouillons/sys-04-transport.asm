; sys-04-transport · le transport établi · spec sys-04:R1 · bloc carte g90004
; LE socket natif par AFD, SANS ws2_32 (I1 : AUCUN IAT — la surface de
; hook que M8 a nommée est contournée). L'ORCHESTRATEUR de la séquence
; MESURÉE mswsock (Q2/I6 : jamais une invention) : le handle SYNCHRONE
; d'abord (NtCreateFile sur \Device\Afd\Endpoint, le EA AfdOpenPacketXX),
; le bind IMPLICITE WILDCARD ensuite (le noyau DÉDUIT l'adresse source,
; I3 : le domaine ne décide RIEN de la source), le connect ENFIN (le
; sockaddr distant du kit, boutisme réseau, I4 : LU, jamais interprété).
; Les constantes au plan d'adressage (m8/layout.py, source unique — T5) ;
; l'instrument verifier_specs_m9d.py les re-dérive, le harnais re-vérifie.
; TROIS résolutions au geste même (Q3 : « NtDeviceIoControlFile » résolu
; DEUX FOIS — chaque geste résout, charte § 6) ; le SSN traverse en rax
; jusqu'au site syscall (P1 de sys-01). Le handle naît dans la variable
; LOCALE du bloc ([rsp+0x58] — le PHANDLE passé au noyau) et n'est posé
; à [P3] qu'au succès des TROIS gestes (Q4 : au -6 le handle n'est PAS
; posé — aucune possession partielle ; I8 : la fermeture est AU KIT).
; Le cadre 0x110 (3 pushes + 0x110 ≡ 0 mod 16 aux sites d'appel) :
; l'ombre 0x20, les SEPT arguments de pile du create (0x38), le handle
; local, les TROIS IOSB (0x30), l'OBJECT_ATTRIBUTES (0x30),
; l'UNICODE_STRING (0x10), l'AFD_CONNECT (0x28), la sortie de bind
; (0x10) — zones mortes au retour (I2 : aucun état, charte § 6).
push rbx
push rbp
push rdi
sub rsp, 0x110
mov rbp, rcx
mov rdi, rdx
mov rbx, r8
; Q3 geste 1 : résoudre « NtCreateFile » AU GESTE MÊME (sys-02 — jamais
; un numéro en cache, charte § 6) ; I5 : un échec = AUCUN syscall émis
lea rcx, [rip + NOM_CREATEFILE]
mov edx, 11
mov r8, rbp
call SYS02
test rax, rax
js .resolution_echouee
; I2/I3 : l'UNICODE_STRING de pile pointe le fixture-device .text6 (T5 :
; CITÉ par déplacement — Length 40 SANS le NUL, MaximumLength 42 AVEC,
; l'ERRATUM DE L'INSTRUMENT corrigé sur pièces AVANT la notation)
mov word ptr [rsp + 0xC0], 40
mov word ptr [rsp + 0xC2], 42
lea r10, [rip + DEVICE]
mov qword ptr [rsp + 0xC8], r10
; I2 : l'OBJECT_ATTRIBUTES de pile (Length 0x30, RootDirectory 0,
; Attributes OBJ_CASE_INSENSITIVE 0x40, ni descripteur ni QoS — Q2)
mov dword ptr [rsp + 0x90], 0x30
mov qword ptr [rsp + 0x98], 0
lea r10, [rsp + 0xC0]
mov qword ptr [rsp + 0xA0], r10
mov dword ptr [rsp + 0xA8], 0x40
mov qword ptr [rsp + 0xB0], 0
mov qword ptr [rsp + 0xB8], 0
; Q2 : les ONZE arguments dans l'ordre NT — quatre en registres, SEPT à
; [rsp+0x20]+ (l'ombre du cadre est AUSSI la pile du syscall — sys-01
; six octets, le noyau lit [rsp+0x28] au site, le charme du trombone) ;
; le PHANDLE est la LOCALE du bloc, JAMAIS P3 (Q4) ; le DesiredAccess en
; edx : l'imm32 est ZÉRO-ÉTENDU (mov edx — jamais mov rdx dont le C7
; SIGNERAIT l'extension, 0xC0140000 a le bit 31 posé, la leçon du
; round-trip : le harnais l'a attrapé AVANT le noyau)
lea rcx, [rsp + 0x58]
mov edx, 0xC0140000
lea r8, [rsp + 0x90]
lea r9, [rsp + 0x60]
mov qword ptr [rsp + 0x20], 0
mov qword ptr [rsp + 0x28], 0
mov qword ptr [rsp + 0x30], 3
mov qword ptr [rsp + 0x38], 1
mov qword ptr [rsp + 0x40], 0x20
lea r10, [rip + EA]
mov qword ptr [rsp + 0x48], r10
mov qword ptr [rsp + 0x50], 54
call SYS01
; Q4 : le NTSTATUS n'est JAMAIS muet — 0 NOMMÉ, sinon -6 le brut en
; rdx ; la divergence rax/IOSB.Status est -6 (le noyau ne parle pas
; deux fois) ; le PREMIER STATUS non nul arrête la marche (I6)
test eax, eax
jne .status_nonnul
cmp dword ptr [rsp + 0x60], 0
jne .status_iosb_create
; Q3 geste 2 : résoudre « NtDeviceIoControlFile » AU GESTE MÊME (la
; PREMIÈRE des DEUX résolutions du nom — chaque geste résout)
lea rcx, [rip + NOM_DEVICEIOCTL]
mov edx, 21
mov r8, rbp
call SYS02
test rax, rax
js .resolution_echouee
; Q2/I3 : les DIX arguments du BIND — le handle né du create, le
; fixture-bind WILDCARD CITÉ par déplacement (flags 2 : le noyau
; DÉDUIT), la sortie 16 o dans le cadre du bloc (I2)
mov rcx, qword ptr [rsp + 0x58]
xor edx, edx
xor r8d, r8d
xor r9d, r9d
lea r10, [rsp + 0x70]
mov qword ptr [rsp + 0x20], r10
mov qword ptr [rsp + 0x28], 0x12003
lea r10, [rip + BIND]
mov qword ptr [rsp + 0x30], r10
mov qword ptr [rsp + 0x38], 0x14
lea r10, [rsp + 0xF8]
mov qword ptr [rsp + 0x40], r10
mov qword ptr [rsp + 0x48], 0x10
call SYS01
test eax, eax
jne .status_nonnul
cmp dword ptr [rsp + 0x70], 0
jne .status_iosb_bind
; Q3 geste 3 : résoudre « NtDeviceIoControlFile » ENCORE (chaque geste
; résout — JAMAIS le numéro du geste précédent, charte § 6)
lea rcx, [rip + NOM_DEVICEIOCTL]
mov edx, 21
mov r8, rbp
call SYS02
test rax, rax
js .resolution_echouee
; I2/I4 : l'AFD_CONNECT_JOIN_INFO_TL de pile (40 o) — SanActive 0 (+7
; NUL), RootEndpoint 0, ConnectEndpoint 0 (la MESURE : les zéros SONT
; acceptés), le sockaddr du kit COPIÉ à +24 SANS INTERPRÉTATION (le
; domaine ne valide ni le port ni l'adresse : le noyau connecte)
mov qword ptr [rsp + 0xD0], 0
mov qword ptr [rsp + 0xD8], 0
mov qword ptr [rsp + 0xE0], 0
mov r10, qword ptr [rdi]
mov qword ptr [rsp + 0xE8], r10
mov r10, qword ptr [rdi + 8]
mov qword ptr [rsp + 0xF0], r10
; Q2 : les DIX arguments du CONNECT — sortie NULL (la réponse est le
; IOSB ; la poignée EST ÉTABLIE au retour : le handle synchrone attend
; le three-way handshake)
mov rcx, qword ptr [rsp + 0x58]
xor edx, edx
xor r8d, r8d
xor r9d, r9d
lea r10, [rsp + 0x80]
mov qword ptr [rsp + 0x20], r10
mov qword ptr [rsp + 0x28], 0x12007
lea r10, [rsp + 0xD0]
mov qword ptr [rsp + 0x30], r10
mov qword ptr [rsp + 0x38], 0x28
mov qword ptr [rsp + 0x40], 0
mov qword ptr [rsp + 0x48], 0
call SYS01
test eax, eax
jne .status_nonnul
cmp dword ptr [rsp + 0x80], 0
jne .status_iosb_connect
; Q1 : les TROIS gestes ont rendu 0 — le handle est posé à [P3] ICI
; seulement (la donnée du kit, I8 : le bloc ne le ferme jamais)
mov r10, qword ptr [rsp + 0x58]
mov qword ptr [rbx], r10
xor eax, eax
add rsp, 0x110
pop rdi
pop rbp
pop rbx
ret
; Q4 : -6 le STATUS brut consigné en rdx (nommé, jamais muet)
.status_nonnul:
mov rdx, rax
mov rax, -6
jmp .epilogue
.status_iosb_create:
mov edx, dword ptr [rsp + 0x60]
mov rax, -6
jmp .epilogue
.status_iosb_bind:
mov edx, dword ptr [rsp + 0x70]
mov rax, -6
jmp .epilogue
.status_iosb_connect:
mov edx, dword ptr [rsp + 0x80]
mov rax, -6
jmp .epilogue
; Q4 : -1 LA CAUSE en rdx (le verdict du résolveur, nommé) — AUCUN
; syscall émis pour CE geste (I5 : la marche s'arrête NOMMÉMENT)
.resolution_echouee:
mov rdx, rax
mov rax, -1
.epilogue:
add rsp, 0x110
pop rdi
pop rbp
pop rbx
ret
