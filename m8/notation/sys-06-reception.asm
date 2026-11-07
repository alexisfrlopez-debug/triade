; sys-06-reception · bloc la réception du transport — le recv AFD bloquant, le zéro est LA DEMI-FIN -7 · spec sys-06:R3 · bloc carte g90006
; Révision 3 (07/11/2026, l'erratum n° 10 — LE TERRAIN A JUGÉ LA MESURE) :
;   le run de la sonde sys-06 (Entrée 191) a lu LE CODE EXACT de la
;   première lecture réelle : -6, STATUS_INVALID_PARAMETER (0xC000000D),
;   DÉTERMINISTE (trois lectures identiques — dont la capacité 1 et le
;   délai 2 s ; le compas étalonné, l'offre sys-05 VERT au même geste) ;
;   l'A/B des notations nomme le coupable au CHAMP : le VRAI afd.sys
;   (Win11 26300) REFUSE le bit 0x20 dans AfdFlags — l'erratum de lecture
;   de la révision 2 (la mesure WinDbg citée) est RÉFUTÉ PAR LE TERRAIN :
;   TDI_RECEIVE_NORMAL (0x20) RETOURNE au champ TdiFlags, AfdFlags = 0 —
;   le MÊME encode (mov dword, 8 o), le slot ne bouge pas d'un octet.
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0xa6c0, taille 384 octets
; Dépendances : sys-02 PUIS sys-01 (IOCTL_AFD_RECEIVE bloquant) — LE ZÉRO EST LA DEMI-FIN -7 (Q2) ; le noyau ÉCRIT chez le kit (I2) ; TdiFlags 0x20 LE TERRAIN (l'erratum n° 10) ; le fixture .text6 NOM_DEVICEIOCTL cité par déplacement (T5)
; Notation explicite générée par outils/auteur.py depuis brouillons/sys-06-reception.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 287 o · padding : 97 o (NOP)
; Étiquettes résolues : .demi_fin=0xa79d, .status_nonnul=0xa7a8, .status_iosb=0xa7b4, .resolution_echouee=0xa7c1, .epilogue=0xa7cb, .span_invalide=0xa7d7
; Déplacements RIP (cible = adresse + taille + disp) :
;   0xa6e9 + 0x7 + 0x65d0 = 0x10cc0
test r8, r8
je 0xa7d7
test r9, r9
je 0xa7d7
push rbx
push rbp
push rdi
push rsi
sub rsp, 0x88
mov rbp, rcx
mov rbx, rdx
mov rdi, r8
mov rsi, r9
lea rcx, [rip + 0x65d0]
mov edx, 21
mov r8, rbp
call 0xa040
test rax, rax
js 0xa7c1
mov dword ptr [rsp + 0x60], esi
mov qword ptr [rsp + 0x68], rdi
lea r10, [rsp + 0x60]
mov qword ptr [rsp + 0x70], r10
mov dword ptr [rsp + 0x78], 1
mov dword ptr [rsp + 0x7C], 0
mov dword ptr [rsp + 0x80], 0x20
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
call 0xa000
test eax, eax
jne 0xa7a8
cmp dword ptr [rsp + 0x50], 0
jne 0xa7b4
mov rax, qword ptr [rsp + 0x58]
test rax, rax
jz 0xa79d
add rsp, 0x88
pop rsi
pop rdi
pop rbp
pop rbx
ret
xor edx, edx
mov rax, -7
jmp 0xa7cb
mov rdx, rax
mov rax, -6
jmp 0xa7cb
mov edx, dword ptr [rsp + 0x50]
mov rax, -6
jmp 0xa7cb
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
