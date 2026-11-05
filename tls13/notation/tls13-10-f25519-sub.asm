; tls13-10-f25519-sub · bloc f25519 soustraction réduite (a + 2p − b, miroir av-08) · spec tls13-10:R1 · bloc carte h100010
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0xca00, taille 320 octets
; Domaine : tls13 (M9, l'ère 1.0.0) · Dépendances : tls13-12 (UNE passe — I2) ; les membres de 2p en IMMÉDIATS re-dérivés du plan (I1, l'erratum consigné) ; la chaîne sub/sbb SUR LE SCRATCH, l'emprunt sortant VERROU fail-closed (Q3 : rax = -1 NOMMÉ, RIEN écrit) ; AUCUN déplacement RIP
; Notation explicite générée par outils/auteur.py depuis brouillons/tls13-10-f25519-sub.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 252 o · padding : 68 o (NOP, 0x90)
; Étiquettes résolues : .emprunt=0xcaf0
; Appels directs (l'adresse scellée du plan — I1) : call 0xcfc0
sub rsp, 0x48
mov rax, qword ptr [rcx]
movabs r11, 0x7ffffffffffda
add rax, r11
mov qword ptr [rsp + 0x20], rax
mov rax, qword ptr [rcx + 8]
movabs r11, 0x7ffffffffffff
add rax, r11
mov qword ptr [rsp + 0x28], rax
mov rax, qword ptr [rcx + 16]
movabs r11, 0x7ffffffffffff
add rax, r11
mov qword ptr [rsp + 0x30], rax
mov rax, qword ptr [rcx + 24]
movabs r11, 0x7ffffffffffff
add rax, r11
mov qword ptr [rsp + 0x38], rax
mov rax, qword ptr [rcx + 32]
movabs r11, 0xfffffffffffff
add rax, r11
mov qword ptr [rsp + 0x40], rax
mov rax, qword ptr [rsp + 0x20]
sub rax, qword ptr [rdx]
mov qword ptr [rsp + 0x20], rax
mov rax, qword ptr [rsp + 0x28]
sbb rax, qword ptr [rdx + 8]
mov qword ptr [rsp + 0x28], rax
mov rax, qword ptr [rsp + 0x30]
sbb rax, qword ptr [rdx + 16]
mov qword ptr [rsp + 0x30], rax
mov rax, qword ptr [rsp + 0x38]
sbb rax, qword ptr [rdx + 24]
mov qword ptr [rsp + 0x38], rax
mov rax, qword ptr [rsp + 0x40]
sbb rax, qword ptr [rdx + 32]
mov qword ptr [rsp + 0x40], rax
jc 0xcaf0
mov rax, qword ptr [rsp + 0x20]
mov qword ptr [rcx], rax
mov rax, qword ptr [rsp + 0x28]
mov qword ptr [rcx + 8], rax
mov rax, qword ptr [rsp + 0x30]
mov qword ptr [rcx + 16], rax
mov rax, qword ptr [rsp + 0x38]
mov qword ptr [rcx + 24], rax
mov rax, qword ptr [rsp + 0x40]
mov qword ptr [rcx + 32], rax
call 0xcfc0
xor eax, eax
add rsp, 0x48
ret
mov rax, -1
add rsp, 0x48
ret
