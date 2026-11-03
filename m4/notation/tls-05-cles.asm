; tls-05-cles · bloc cycle de vie des handles · spec tls-05:R2 · bloc carte g70005
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x65c0, taille 384 octets
; Dépendances : IAT secur32 AcquireCredentialsHandleW / FreeCredentialsHandle / DeleteSecurityContext ; compensation exacte ; SCH_CREDENTIALS explicite dwVersion=5 dwFlags=0 (P3/R2, D140) ; cadre aux offsets documentés (layout.CADRE_*, arrêt D81)
; Notation explicite générée par outils/auteur.py depuis brouillons/tls-05-cles.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 325 o · padding : 59 o (NOP)
; Étiquettes résolues : .fin_liberer=0x6608, .acquerir=0x660d, .fin_acquerir=0x66be, .detruire=0x66c6, .fin_detruire=0x66fa, .refus=0x66ff
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x65e2 + 0x6 - 0x3be0 = 0x2a08
;   0x6685 + 0x7 - 0x3a8c = 0x2c00
;   0x6695 + 0x6 - 0x3c9b = 0x2a00
;   0x66d3 + 0x6 - 0x3cc1 = 0x2a18
cmp ecx, 3
jae 0x66ff
test ecx, ecx
jz 0x660d
cmp ecx, 1
je 0x66c6
sub rsp, 0x28
mov qword ptr [rsp + 0x20], rdx
mov rcx, rdx
call qword ptr [rip - 0x3be0]
movsxd rcx, eax
call 0x6080
mov rdx, [rsp + 0x20]
test eax, eax
jnz 0x6608
mov qword ptr [rdx], 0
mov qword ptr [rdx + 8], 0
add rsp, 0x28
ret
sub rsp, 0x98
mov qword ptr [rsp + 0x90], rdx
xor eax, eax
mov [rsp + 0x48], rax
mov [rsp + 0x50], rax
mov [rsp + 0x58], rax
mov [rsp + 0x60], rax
mov [rsp + 0x68], rax
mov [rsp + 0x70], rax
mov [rsp + 0x78], rax
mov [rsp + 0x80], rax
mov [rsp + 0x88], rax
mov dword ptr [rsp + 0x48], 5
mov qword ptr [rsp + 0x28], 0
mov qword ptr [rsp + 0x30], 0
mov [rsp + 0x38], rdx
mov qword ptr [rsp + 0x40], 0
lea rax, [rsp + 0x48]
mov [rsp + 0x20], rax
xor ecx, ecx
lea rdx, [rip - 0x3a8c]
mov r8d, 2
xor r9d, r9d
call qword ptr [rip - 0x3c9b]
movsxd rcx, eax
call 0x6080
mov rdx, [rsp + 0x90]
test eax, eax
jz 0x66be
mov qword ptr [rdx], 0
mov qword ptr [rdx + 8], 0
add rsp, 0x98
ret
sub rsp, 0x28
mov qword ptr [rsp + 0x20], rdx
lea rcx, [rdx + 0x10]
call qword ptr [rip - 0x3cc1]
movsxd rcx, eax
call 0x6080
mov rdx, [rsp + 0x20]
test eax, eax
jnz 0x66fa
mov qword ptr [rdx + 0x10], 0
mov qword ptr [rdx + 0x18], 0
add rsp, 0x28
ret
mov eax, 6
ret
