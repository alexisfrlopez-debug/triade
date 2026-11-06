; sys-05-emission · bloc l'émission du transport — le send AFD par syscall direct, TOTALE ou refus -7 · spec sys-05:R2 · bloc carte g90005
; Révision 2 (07/11/2026, le recoup du run 1 de la sonde sys-05 — Entrée 185) :
;   le WSABUF passe de « packé » 12 o (buf à +4) à CANONIQUE 16 o (buf à +8,
;   le padding d'alignement 4 o) — le noyau lisait buf à +8 : l'adresse
;   folle, STATUS_ACCESS_VIOLATION 0xC0000005, le -6 des cinq runs NOMMÉ ;
;   le MÊME encode (48 89 7c 24 68, 5 o) — le slot ne bouge pas d'un octet.
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0xa540, taille 384 octets
; Dépendances : sys-02 PUIS sys-01 (IOCTL_AFD_SEND) — TOTALE ou refus -7 (Q2) ; AUCUNE copie de la charge (I2) ; le fixture .text6 NOM_DEVICEIOCTL cité par déplacement (T5)
; Notation explicite générée par outils/auteur.py depuis brouillons/sys-05-emission.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 289 o · padding : 95 o (NOP)
; Étiquettes résolues : .emission_partielle=0xa61c, .status_nonnul=0xa62a, .status_iosb=0xa636, .resolution_echouee=0xa643, .epilogue=0xa64d, .span_invalide=0xa659
; Déplacements RIP (cible = adresse + taille + disp) :
;   0xa569 + 0x7 + 0x6750 = 0x10cc0
test r8, r8
je 0xa659
test r9, r9
je 0xa659
push rbx
push rbp
push rdi
push rsi
sub rsp, 0x88
mov rbp, rcx
mov rbx, rdx
mov rdi, r8
mov rsi, r9
lea rcx, [rip + 0x6750]
mov edx, 21
mov r8, rbp
call 0xa040
test rax, rax
js 0xa643
mov dword ptr [rsp + 0x60], esi
mov qword ptr [rsp + 0x68], rdi
lea r10, [rsp + 0x60]
mov qword ptr [rsp + 0x70], r10
mov dword ptr [rsp + 0x78], 1
mov dword ptr [rsp + 0x7C], 0
mov dword ptr [rsp + 0x80], 0
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
call 0xa000
test eax, eax
jne 0xa62a
cmp dword ptr [rsp + 0x50], 0
jne 0xa636
cmp qword ptr [rsp + 0x58], rsi
jne 0xa61c
xor eax, eax
add rsp, 0x88
pop rsi
pop rdi
pop rbp
pop rbx
ret
mov rdx, qword ptr [rsp + 0x58]
mov rax, -7
jmp 0xa64d
mov rdx, rax
mov rax, -6
jmp 0xa64d
mov edx, dword ptr [rsp + 0x50]
mov rax, -6
jmp 0xa64d
mov rdx, rax
mov rax, -1
add rsp, 0x88
pop rsi
pop rdi
pop rbp
pop rbx
ret
mov rax, -5
ret
