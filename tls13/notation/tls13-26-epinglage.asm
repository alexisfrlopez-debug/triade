; tls13-26-epinglage · bloc l'épinglage du certificat (la comparaison, jamais la croyance) · spec tls13-26:R1 · bloc carte h100026
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0xf9e0, taille 320 octets
; Domaine : tls13 (M9, l'ère 1.0.0) · Dépendances : bloc ; tls13-01, tls13-03, tls13-04 (le hachage — un contexte de PILE local, I2) ; la décision de confiance : SHA-256(DER) CONFRONTÉ à l'empreinte par OU cumulatif des 32 différences (I1 : TEMPS CONSTANT — la discipline demeure sur une donnée de confiance), conforme → 0, divergent → -6 NOMMÉ (épinglage divergent — la session MEURT sans autres formes)
; Notation explicite générée par outils/auteur.py depuis brouillons/tls13-26-epinglage.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 285 o · padding : 35 o (NOP, 0x90)
; Étiquettes résolues : .conforme=0xfacd, .refus_propage=0xfad7, .refus_nul=0xfadf, .refus_taille=0xfaee
; Appels directs (l'adresse scellée du plan — I1) : call 0xc000, call 0xc240, call 0xc300
sub rsp, 0xc8
test rcx, rcx
jz 0xfadf
test r8, r8
jz 0xfadf
test rdx, rdx
jz 0xfaee
movabs r10, 0x2000000000000000
cmp rdx, r10
ja 0xfaee
mov qword ptr [rsp + 0xb0], rcx
mov qword ptr [rsp + 0xb8], rdx
mov qword ptr [rsp + 0xc0], r8
lea rcx, [rsp + 0x20]
call 0xc000
test eax, eax
jnz 0xfad7
lea rcx, [rsp + 0x20]
mov rdx, qword ptr [rsp + 0xb0]
mov r8, qword ptr [rsp + 0xb8]
call 0xc240
test eax, eax
jnz 0xfad7
lea rcx, [rsp + 0x20]
lea rdx, [rsp + 0x90]
call 0xc300
test eax, eax
jnz 0xfad7
mov r8, qword ptr [rsp + 0xc0]
xor r10d, r10d
mov r11, qword ptr [r8]
xor r11, qword ptr [rsp + 0x90]
or r10, r11
mov r11, qword ptr [r8 + 8]
xor r11, qword ptr [rsp + 0x98]
or r10, r11
mov r11, qword ptr [r8 + 16]
xor r11, qword ptr [rsp + 0xa0]
or r10, r11
mov r11, qword ptr [r8 + 24]
xor r11, qword ptr [rsp + 0xa8]
or r10, r11
test r10, r10
jz 0xfacd
mov rax, -6
add rsp, 0xc8
ret
xor eax, eax
add rsp, 0xc8
ret
add rsp, 0xc8
ret
mov rax, -1
add rsp, 0xc8
ret
mov rax, -2
add rsp, 0xc8
ret
