; tls13-25-finished-calculer-verifier · bloc le Finished calculé/vérifié (le HMAC du transcript, § 4.4.4) · spec tls13-25:R1 · bloc carte h100025
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0xf8e0, taille 256 octets
; Domaine : tls13 (M9, l'ère 1.0.0) · Dépendances : bloc ; tls13-05 (UNE composition — l'HMAC, le Finished n'est RIEN d'autre — I1) ; DEUX modes NOMMÉS sur r9 (0 calculer, 1 vérifier, toute autre valeur → -1) ; le mode VÉRIFIER : le reçu CONFRONTÉ par OU cumulatif des 32 différences (I2 : AUCUN court-circuit — la discipline du verdict AEAD), conforme → 0, divergent → -4 NOMMÉ ; le mode est une donnée PUBLIQUE de contrôle (le branch licite)
; Notation explicite générée par outils/auteur.py depuis brouillons/tls13-25-finished-calculer-verifier.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 239 o · padding : 17 o (NOP, 0x90)
; Étiquettes résolues : .mode_verifier=0xf92a, .hmac=0xf934, .verifier=0xf95c, .conforme=0xf9a4, .fin_calculer=0xf9ab, .refus_propage=0xf9b2, .refus_nul=0xf9b7, .refus_mode=0xf9c3
; Appels directs (l'adresse scellée du plan — I1) : call 0xc3c0
sub rsp, 0x68
test rcx, rcx
jz 0xf9b7
test rdx, rdx
jz 0xf9b7
test r8, r8
jz 0xf9b7
cmp r9, 1
ja 0xf9c3
mov qword ptr [rsp + 0x28], rcx
mov qword ptr [rsp + 0x30], rdx
mov qword ptr [rsp + 0x38], r8
mov qword ptr [rsp + 0x60], r9
cmp r9, 1
je 0xf92a
mov qword ptr [rsp + 0x20], r8
jmp 0xf934
lea r10, [rsp + 0x40]
mov qword ptr [rsp + 0x20], r10
mov rcx, qword ptr [rsp + 0x28]
mov edx, 32
mov r8, qword ptr [rsp + 0x30]
mov r9d, 32
call 0xc3c0
test eax, eax
jnz 0xf9b2
cmp qword ptr [rsp + 0x60], 1
je 0xf95c
jmp 0xf9ab
mov r8, qword ptr [rsp + 0x38]
xor r10d, r10d
mov r11, qword ptr [r8]
xor r11, qword ptr [rsp + 0x40]
or r10, r11
mov r11, qword ptr [r8 + 8]
xor r11, qword ptr [rsp + 0x48]
or r10, r11
mov r11, qword ptr [r8 + 16]
xor r11, qword ptr [rsp + 0x50]
or r10, r11
mov r11, qword ptr [r8 + 24]
xor r11, qword ptr [rsp + 0x58]
or r10, r11
test r10, r10
jz 0xf9a4
mov rax, -4
add rsp, 0x68
ret
xor eax, eax
add rsp, 0x68
ret
xor eax, eax
add rsp, 0x68
ret
add rsp, 0x68
ret
mov rax, -1
add rsp, 0x68
ret
mov rax, -1
add rsp, 0x68
ret
