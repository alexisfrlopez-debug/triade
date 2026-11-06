; tls13-20-enregistrement-proteger · bloc l'enregistrement protéger (RFC 8446 § 5.2) · spec tls13-20:R1 · bloc carte h100020
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0xe9c0, taille 384 octets
; Domaine : tls13 (M9, l'ère 1.0.0) · Dépendances : bloc ; tls13-18 (UNE composition — le scellement) ; le texte interne charge || type au DERNIER octet (bourre LONGUEUR ZÉRO), le nonce = IV ⊕ séquence GROS-BOUTISTE (I2 : le IV COPIÉ en local, le contexte jamais réécrit), l'AAD = l'en-tête LOCALE (23, 0x0303, N+17 u16 gros-boutiste — copiée à la sortie APRÈS le succès : le -3 propagé n'écrit RIEN) ; l'incrémentation SUIT le scellement (un échec n'avance JAMAIS) ; le cadre 0x4078 : le texte interne jusqu'à 2^14+1 sur la pile ; le verdict -3 = le verdict PROPAGÉ de 18 (N = 2^14 : le texte interne 2^14+1 hors la brique — la fragmentation à l'appelant)
; Notation explicite générée par outils/auteur.py depuis brouillons/tls13-20-enregistrement-proteger.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 349 o · padding : 35 o (NOP, 0x90)
; Étiquettes résolues : .charge_indifferente=0xe9fc, .copie=0xea47, .copie_fin=0xea61, .refus_propage=0xeaf0, .refus_nul=0xeaff, .refus_taille=0xeb0e
; Appels directs (l'adresse scellée du plan — I1) : call 0xe080
sub rsp, 0x4078
test rcx, rcx
jz 0xeaff
cmp r9, 0x4000
ja 0xeb0e
mov rax, qword ptr [rsp + 0x40a0]
test rax, rax
jz 0xeaff
test r9, r9
je 0xe9fc
test r8, r8
jz 0xeaff
mov byte ptr [rsp + 0x50], 23
mov byte ptr [rsp + 0x51], 3
mov byte ptr [rsp + 0x52], 3
lea r10, [r9 + 17]
mov byte ptr [rsp + 0x54], r10b
shr r10, 8
mov byte ptr [rsp + 0x53], r10b
mov r11, qword ptr [rcx + 176]
mov qword ptr [rsp + 0x40], r11
mov r11d, dword ptr [rcx + 184]
mov dword ptr [rsp + 0x48], r11d
mov r11, qword ptr [rcx + 192]
bswap r11
xor qword ptr [rsp + 0x44], r11
xor r10d, r10d
cmp r10, r9
jae 0xea61
mov r11, r8
add r11, r10
movzx r11d, byte ptr [r11]
mov byte ptr [rsp + r10 + 0x68], r11b
add r10, 1
jmp 0xea47
mov byte ptr [rsp + r9 + 0x68], dl
mov qword ptr [rsp + 0x58], rax
mov qword ptr [rsp + 0x60], rcx
lea r10, [rsp + 0x50]
mov qword ptr [rsp + 0x20], r10
mov qword ptr [rsp + 0x28], 5
lea r10, [rax + 5]
mov qword ptr [rsp + 0x30], r10
lea r10, [rax + r9 + 6]
mov qword ptr [rsp + 0x38], r10
lea rdx, [rsp + 0x40]
lea r8, [rsp + 0x68]
lea r9, [r9 + 1]
call 0xe080
test eax, eax
jnz 0xeaf0
mov rcx, qword ptr [rsp + 0x60]
mov r10, qword ptr [rsp + 0x58]
mov al, byte ptr [rsp + 0x50]
mov byte ptr [r10], al
mov al, byte ptr [rsp + 0x51]
mov byte ptr [r10 + 1], al
mov al, byte ptr [rsp + 0x52]
mov byte ptr [r10 + 2], al
mov al, byte ptr [rsp + 0x53]
mov byte ptr [r10 + 3], al
mov al, byte ptr [rsp + 0x54]
mov byte ptr [r10 + 4], al
add qword ptr [rcx + 192], 1
xor eax, eax
add rsp, 0x4078
ret
mov rax, -3
add rsp, 0x4078
ret
mov rax, -1
add rsp, 0x4078
ret
mov rax, -2
add rsp, 0x4078
ret
