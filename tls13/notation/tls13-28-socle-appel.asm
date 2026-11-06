; tls13-28-socle-appel · bloc le socle d'appel (la rotule de transport à rappels) · spec tls13-28:R1 · bloc carte h100028
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x10d00, taille 176 octets
; Domaine : tls13 (M9, l'ère 1.0.0) · Dépendances : LA ROTULE — le seul point du domaine où le calcul touche le monde : UN contexte de DEUX rappels fournis par l'appelant (émettre @ +0/+8, recevoir @ +16/+24), invoqués PAR POINTEUR DEPUIS LE CONTEXTE (I2 : l'appel indirect DÉCLARÉ sur une cible qui est une DONNÉE du contexte n'est NI un import NI un syscall) ; l'opération rdx ∈ {1 émettre, 2 recevoir}, toute autre → -1 ; le verdict du rappel négatif → -7 NOMMÉ (transport en échec) ; aucune copie, aucun tampon (Q4 — l'adaptateur), le zéro de réception est le refus -7 du KIT
; Notation explicite générée par outils/auteur.py depuis brouillons/tls13-28-socle-appel.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 144 o · padding : 32 o (NOP, 0x90)
; Étiquettes résolues : .emettre=0x10d13, .recevoir=0x10d47, .ok=0x10d75, .refus_transport=0x10d78, .refus_nul=0x10d80, .refus_op=0x10d88
; Appels directs (l'adresse scellée du plan — I1) : call r10, call r10
test rcx, rcx
jz 0x10d80
cmp rdx, 1
je 0x10d13
cmp rdx, 2
je 0x10d47
jmp 0x10d88
test r8, r8
jz 0x10d80
mov r10, qword ptr [rcx]
test r10, r10
jz 0x10d80
mov r11, qword ptr [rcx + 8]
sub rsp, 0x28
mov rcx, r11
mov r11, r8
mov r8, r9
mov rdx, r11
call r10
add rsp, 0x28
test eax, eax
jz 0x10d75
mov rax, -7
ret
test r8, r8
jz 0x10d80
mov r10, qword ptr [rcx + 16]
test r10, r10
jz 0x10d80
mov r11, qword ptr [rcx + 24]
sub rsp, 0x28
mov rcx, r11
mov r11, r8
mov r8, r9
mov rdx, r11
call r10
add rsp, 0x28
test eax, eax
jle 0x10d78
ret
xor eax, eax
ret
mov rax, -7
ret
mov rax, -1
ret
mov rax, -1
ret
