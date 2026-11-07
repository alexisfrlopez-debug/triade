; sys-06-reception · bloc la réception du transport — le recv AFD bloquant, le zéro est LA DEMI-FIN -7 · spec sys-06:R2 · bloc carte g90006
; Révision 2 (07/11/2026, l'erratum n° 9 — le miroir exact de la sonde
;   sys-05, Entrée 185) : le WSABUF passe de « packé » 12 o (buf à +4) à
;   CANONIQUE 16 o (buf à +8, le padding d'alignement 4 o) — le noyau
;   lit buf à +8 : à la réception il ÉCRIRAIT chez l'adresse folle, le
;   miroir de la mesure 0xC0000005 ; le MÊME encode (48 89 7c 24 68,
;   5 o) — le slot ne bouge pas d'un octet.
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0xa6c0, taille 384 octets
; Dépendances : sys-02 PUIS sys-01 (IOCTL_AFD_RECEIVE bloquant) — LE ZÉRO EST LA DEMI-FIN -7 (Q2) ; le noyau ÉCRIT chez le kit (I2) ; AfdFlags 0x20 LA MESURE (l'erratum) ; le fixture .text6 NOM_DEVICEIOCTL cité par déplacement (T5)
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
mov dword ptr [rsp + 0x7C], 0x20
mov dword ptr [rsp + 0x80], 0
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
