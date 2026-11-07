; loupe-09-ecran · bloc l'écran : WinMain + LA PROCÉDURE + la vitrine (l'entrée du domaine) · spec loupe-09:R1 · bloc carte i110009
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x5c00, taille 896 octets
; Domaine : loupe (M10, le TGN « Loupe ») · Dépendances : WinMain + LA PROCÉDURE (le bloc DERNIER du tassement : la table de routage s'étendra au chantier (d)) ; IAT kernel32 : GetModuleHandleW, GetCommandLineW, ExitProcess ; IAT user32 : RegisterClassExW, CreateWindowExW, ShowWindow, LoadCursorW, MessageBoxW (l'explication fatale E1/E2, D36) ; win-03 LA BOUCLE HÉRITÉE PAR LA CARTE (l'adresse scellée démo @0x15C0, R7 — ses déplacements visent l'IAT démo @0x2818/0x2820/0x2828) ; loupe-01 (la session née à la ligne de commande lue À LA MAIN) ; loupe-10/11/12/14 (les blocs routés) ; l'image PI (D33 : aucune adresse absolue — la procédure par lea rip) ; les zones DÉCLARÉES avant la première goutte (I1)
; Notation explicite générée par outils/auteur.py depuis brouillons/loupe-09-ecran.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 874 o · padding : 22 o (NOP, 0x90)
; Étiquettes résolues : .programme_cote=0x5c21, .programme_nu=0x5c33, .programme_apres=0x5c45, .chemin_pre=0x5c53, .refus_gen=0x5c79, .sans_chemin=0x5c85, .suite_vitrine=0x5c85, .vitrine_impossible=0x5da4, .procedure=0x5dcb, .r_peinture=0x5e19, .r_defilement=0x5e2d, .r_commande=0x5e4a, .r_aller=0x5e5b, .r_suivant=0x5e7a, .r_caractere=0x5e99, .r_caractere_libre=0x5ec2, .r_libre_suivant=0x5ed0, .r_libre_aller=0x5eec, .r_defaut=0x5f08, .r_retour=0x5f1a, .monter=0x5f24, .monter_fin=0x5f40, .message=0x5f41, .message_copie=0x5f4c, .message_fin=0x5f5c
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x5c0e + 0x6 - 0x380c = 0x2408
;   0x5c6b + 0x7 - 0x388c = 0x23e6
;   0x5c79 + 0x7 - 0x38a8 = 0x23d8
;   0x5c85 + 0x7 + 0x13f = 0x5dcb
;   0x5cc9 + 0x6 - 0x3807 = 0x24c8
;   0x5cef + 0x7 - 0x36f6 = 0x2600
;   0x5d0f + 0x6 - 0x38c5 = 0x2450
;   0x5d60 + 0x7 - 0x3767 = 0x2600
;   0x5d67 + 0x7 - 0x375a = 0x2614
;   0x5d74 + 0x6 - 0x3922 = 0x2458
;   0x5d7f + 0x7 + 0xa05a = 0xfde0
;   0x5d91 + 0x6 - 0x3937 = 0x2460
;   0x5d9e + 0x6 - 0x3994 = 0x2410
;   0x5da6 + 0x7 - 0x375d = 0x2650
;   0x5dad + 0x7 - 0x37a0 = 0x2614
;   0x5dba + 0x6 - 0x38e8 = 0x24d8
;   0x5dc5 + 0x6 - 0x39bb = 0x2410
;   0x5e99 + 0x7 + 0x8560 = 0xe400
;   0x5f14 + 0x6 - 0x3a9a = 0x2480
;   0x5f28 + 0x7 + 0x84d1 = 0xe400
;   0x5f34 + 0x7 - 0x3b63 = 0x23d8
;   0x5f41 + 0x7 + 0x84b8 = 0xe400
;   0x5f5c + 0x7 + 0x849d = 0xe400
; Appels directs (l'adresse du plan — I1) : call qword ptr [rip - 0x380c], call 0x4080, call 0x5f41, call 0x5f41, call qword ptr [rip - 0x3807], call qword ptr [rip - 0x38c5], call qword ptr [rip - 0x3922], call qword ptr [rip - 0x3937], call 0x15c0, call qword ptr [rip - 0x3994], call qword ptr [rip - 0x38e8], call qword ptr [rip - 0x39bb], call 0x4b00, call 0x5f24, call 0x5180, call 0x5f24, call 0x5400, call 0x5f24, call 0x5800, call 0x5f24, call 0x5400, call 0x5f24, call 0x5800, call 0x5f24, call 0x5400, call 0x5f24, call qword ptr [rip - 0x3a9a], call 0x5f41
push rdi
push rsi
push r12
sub rsp, 0xb0
mov r12, rcx
call qword ptr [rip - 0x380c]
mov rdx, rax
cmp word ptr [rdx], 0x22
jne 0x5c33
add rdx, 2
movzx eax, word ptr [rdx]
test eax, eax
jz 0x5c85
cmp eax, 0x22
je 0x5c45
add rdx, 2
jmp 0x5c21
movzx eax, word ptr [rdx]
test eax, eax
jz 0x5c85
cmp eax, 0x20
je 0x5c45
add rdx, 2
jmp 0x5c33
movzx eax, word ptr [rdx]
cmp eax, 0x20
jne 0x5c53
add rdx, 2
jmp 0x5c45
movzx eax, word ptr [rdx]
test eax, eax
jz 0x5c85
mov rcx, rdx
call 0x4080
test eax, eax
jns 0x5c85
cmp eax, -2
jne 0x5c79
lea rsi, [rip - 0x388c]
call 0x5f41
jmp 0x5c85
lea rsi, [rip - 0x38a8]
call 0x5f41
lea rax, [rip + 0x13f]
mov qword ptr [rsp + 0x68], rax
mov dword ptr [rsp + 0x60], 80
mov dword ptr [rsp + 0x64], 0
mov dword ptr [rsp + 0x70], 0
mov dword ptr [rsp + 0x74], 0
mov qword ptr [rsp + 0x78], r12
mov qword ptr [rsp + 0x80], 0
xor ecx, ecx
mov edx, 32512
call qword ptr [rip - 0x3807]
mov qword ptr [rsp + 0x88], rax
mov qword ptr [rsp + 0x90], 5
mov qword ptr [rsp + 0x98], 0
lea rax, [rip - 0x36f6]
mov qword ptr [rsp + 0xa0], rax
mov qword ptr [rsp + 0xa8], 0
lea rcx, [rsp + 0x60]
call qword ptr [rip - 0x38c5]
test eax, eax
jz 0x5da4
mov eax, 0x80000000
mov qword ptr [rsp + 0x20], rax
mov qword ptr [rsp + 0x28], rax
mov qword ptr [rsp + 0x30], 640
mov qword ptr [rsp + 0x38], 480
mov qword ptr [rsp + 0x40], 0
mov qword ptr [rsp + 0x48], 0
mov qword ptr [rsp + 0x50], r12
mov qword ptr [rsp + 0x58], 0
xor ecx, ecx
lea rdx, [rip - 0x3767]
lea r8, [rip - 0x375a]
mov r9d, 0x00ef0000
call qword ptr [rip - 0x3922]
test rax, rax
jz 0x5da4
lea rcx, [rip + 0xa05a]
mov qword ptr [rcx], rax
mov rcx, rax
mov edx, 5
call qword ptr [rip - 0x3937]
call 0x15c0
xor ecx, ecx
call qword ptr [rip - 0x3994]
xor ecx, ecx
lea rdx, [rip - 0x375d]
lea r8, [rip - 0x37a0]
mov r9d, 0x10
call qword ptr [rip - 0x38e8]
mov ecx, 1
call qword ptr [rip - 0x39bb]
push rbx
push rdi
push rsi
push r12
sub rsp, 0x28
mov r12, rcx
mov rbx, rdx
mov rsi, r8
mov rdi, r9
cmp rbx, 0x0f
je 0x5e19
cmp rbx, 5
je 0x5e2d
cmp rbx, 0x115
je 0x5e2d
cmp rbx, 0x20a
je 0x5e2d
cmp rbx, 0x100
je 0x5e4a
cmp rbx, 0x102
je 0x5e99
jmp 0x5f08
mov rcx, r12
call 0x4b00
call 0x5f24
xor eax, eax
jmp 0x5f1a
mov rcx, r12
mov rdx, rbx
mov r8, rsi
mov r9, rdi
call 0x5180
call 0x5f24
xor eax, eax
jmp 0x5f1a
cmp rsi, 0x74
je 0x5e5b
cmp rsi, 0x72
je 0x5e7a
jmp 0x5f08
mov rcx, r12
mov edx, 0x100
mov r8, rsi
mov r9, rdi
call 0x5400
call 0x5f24
xor eax, eax
jmp 0x5f1a
mov rcx, r12
mov edx, 0x100
mov r8, rsi
mov r9, rdi
call 0x5800
call 0x5f24
xor eax, eax
jmp 0x5f1a
lea rax, [rip + 0x8560]
mov eax, dword ptr [rax]
test eax, eax
jz 0x5ec2
mov rcx, r12
mov edx, 0x102
mov r8, rsi
mov r9, rdi
call 0x5400
call 0x5f24
xor eax, eax
jmp 0x5f1a
cmp rsi, 0x06
je 0x5ed0
cmp rsi, 0x07
je 0x5eec
jmp 0x5f08
mov rcx, r12
mov edx, 0x102
mov r8, rsi
mov r9, rdi
call 0x5800
call 0x5f24
xor eax, eax
jmp 0x5f1a
mov rcx, r12
mov edx, 0x102
mov r8, rsi
mov r9, rdi
call 0x5400
call 0x5f24
xor eax, eax
jmp 0x5f1a
mov rcx, r12
mov rdx, rbx
mov r8, rsi
mov r9, rdi
call qword ptr [rip - 0x3a9a]
add rsp, 0x28
pop r12
pop rsi
pop rdi
pop rbx
ret
test eax, eax
jns 0x5f40
lea rdx, [rip + 0x84d1]
cmp dword ptr [rdx], 0
jne 0x5f40
lea rsi, [rip - 0x3b63]
call 0x5f41
ret
lea rdi, [rip + 0x84b8]
add rdi, 12
mov al, byte ptr [rsi]
mov byte ptr [rdi], al
test al, al
jz 0x5f5c
inc rsi
inc rdi
jmp 0x5f4c
lea rax, [rip + 0x849d]
mov dword ptr [rax], 3
ret
