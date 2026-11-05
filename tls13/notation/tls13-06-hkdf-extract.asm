; tls13-06-hkdf-extract · bloc HKDF-Extract (RFC 5869 § 2.1 : le sel → le PRK) · spec tls13-06:R1 · bloc carte h100006
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0xc5c0, taille 192 octets
; Domaine : tls13 (M9, l'ère 1.0.0) · Dépendances : tls13-05 (l'HMAC appelé UNE fois — le sel devient la clé) ; les 32 zéros du sel vide sur la PILE (I1)
; Notation explicite générée par outils/auteur.py depuis brouillons/tls13-06-hkdf-extract.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 151 o · padding : 41 o (NOP, 0x90)
; Étiquettes résolues : .sel_vide=0xc616, .hmac=0xc621, .refus_nul=0xc639, .refus_vide=0xc642, .fin=0xc649
; Appels directs (l'adresse scellée du plan — I1) : call 0xc3c0
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x50
mov rbx, qword ptr [rsp + 0xa0]
mov r15, r8
mov r14, r9
test rbx, rbx
je 0xc639
test r14, r14
jz 0xc642
mov r13, rdx
mov qword ptr [rsp + 0x28], 0
mov qword ptr [rsp + 0x30], 0
mov qword ptr [rsp + 0x38], 0
mov qword ptr [rsp + 0x40], 0
test r13, r13
jz 0xc616
mov r12, rcx
jmp 0xc621
lea r12, [rsp + 0x28]
mov r13d, 32
mov [rsp + 0x20], rbx
mov rcx, r12
mov rdx, r13
mov r8, r15
mov r9, r14
call 0xc3c0
jmp 0xc649
mov rax, -1
jmp 0xc649
mov rax, -2
add rsp, 0x50
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
