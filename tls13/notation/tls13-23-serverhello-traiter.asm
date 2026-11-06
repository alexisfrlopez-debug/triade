; tls13-23-serverhello-traiter · bloc le ServerHello traité (les refus nommés, le secret partagé) · spec tls13-23:R1 · bloc carte h100023
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0xee20, taille 576 octets
; Domaine : tls13 (M9, l'ère 1.0.0) · Dépendances : bloc ; tls13-13 (UNE composition — le secret partagé, APRÈS le dernier refus possible : la clé privée n'est JAMAIS touchée sur un message refusé — Q3) ; LA MARCHE BORNÉE (I1 : chaque lecture précédée du contrôle de reste), chaque confrontation NOMMÉE dans l'ordre du corps (le type 2, la version 0x0303, l'aléa ≠ la valeur magique HRR au fixture R_HRR par OU cumulatif — I2, l'écho session_id vide, LA SUITE 0x1301 → -5 la négociation refusée, la compression nulle, supported_versions 0x0304 PRÉSENTE, key_share x25519 32 o PRÉSENTE, les extensions inconnues IGNORÉES — la règle du protocole, l'épuisement exact) ; le message ne TOUCHE PAS au transcript (I3)
; Notation explicite générée par outils/auteur.py depuis brouillons/tls13-23-serverhello-traiter.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 532 o · padding : 44 o (NOP, 0x90)
; Étiquettes résolues : .marche=0xef1f, .pas_ks=0xefa5, .marche_avance=0xefd1, .marche_fin=0xefdb, .refus_hrr=0xeff8, .refus_negociation=0xf004, .refus_nul=0xf010, .refus_type=0xf01c, .refus_taille=0xf028
; Déplacements RIP (cible = adresse + taille + disp) :
;   0xee92 + 0x7 + 0x1d57 = 0x10bf0
; Appels directs (l'adresse scellée du plan — I1) : call 0xd100
sub rsp, 0x38
test rcx, rcx
jz 0xf010
test r8, r8
jz 0xf010
test r9, r9
jz 0xf010
cmp rdx, 90
jb 0xf028
cmp byte ptr [rcx], 2
jne 0xf01c
movzx r10d, byte ptr [rcx + 1]
shl r10d, 16
movzx r11d, byte ptr [rcx + 2]
shl r11d, 8
or r10d, r11d
movzx r11d, byte ptr [rcx + 3]
or r10d, r11d
cmp r10, 86
jb 0xf028
lea r11, [r10 + 4]
cmp r11, rdx
jne 0xf01c
cmp word ptr [rcx + 4], 0x303
jne 0xf01c
lea r11, [rip + 0x1d57]
xor r10d, r10d
mov rax, qword ptr [rcx + 6]
xor rax, qword ptr [r11]
or r10, rax
mov rax, qword ptr [rcx + 14]
xor rax, qword ptr [r11 + 8]
or r10, rax
mov rax, qword ptr [rcx + 22]
xor rax, qword ptr [r11 + 16]
or r10, rax
mov rax, qword ptr [rcx + 30]
xor rax, qword ptr [r11 + 24]
or r10, rax
test r10, r10
jz 0xeff8
cmp byte ptr [rcx + 38], 0
jne 0xf01c
movzx eax, word ptr [rcx + 39]
xchg al, ah
cmp eax, 0x1301
jne 0xf004
cmp byte ptr [rcx + 41], 0
jne 0xf01c
movzx eax, word ptr [rcx + 42]
xchg al, ah
mov r10, rax
mov r11, rdx
sub r11, 44
cmp r10, r11
jne 0xf01c
mov qword ptr [rsp + 0x20], 0
lea r10, [rcx + 44]
lea r11, [rcx + rdx]
cmp r10, r11
jae 0xefdb
mov rax, r11
sub rax, r10
cmp rax, 4
jb 0xf01c
movzx eax, word ptr [r10]
xchg al, ah
mov qword ptr [rsp + 0x30], rax
movzx eax, word ptr [r10 + 2]
xchg al, ah
mov rcx, r11
sub rcx, r10
sub rcx, 4
cmp rax, rcx
ja 0xf01c
cmp qword ptr [rsp + 0x30], 0x33
jne 0xefa5
bt qword ptr [rsp + 0x20], 0
jc 0xf01c
cmp rax, 36
jne 0xf004
movzx ecx, word ptr [r10 + 4]
xchg cl, ch
cmp ecx, 0x1d
jne 0xf004
movzx ecx, word ptr [r10 + 6]
xchg cl, ch
cmp ecx, 0x20
jne 0xf004
lea rcx, [r10 + 8]
mov qword ptr [rsp + 0x28], rcx
or qword ptr [rsp + 0x20], 1
jmp 0xefd1
cmp qword ptr [rsp + 0x30], 0x2b
jne 0xefd1
bt qword ptr [rsp + 0x20], 1
jc 0xf01c
cmp rax, 2
jne 0xf004
movzx ecx, word ptr [r10 + 4]
xchg cl, ch
cmp ecx, 0x304
jne 0xf004
or qword ptr [rsp + 0x20], 2
lea r10, [r10 + rax + 4]
jmp 0xef1f
cmp qword ptr [rsp + 0x20], 3
jne 0xf004
mov rcx, r9
mov rdx, r8
mov r8, qword ptr [rsp + 0x28]
call 0xd100
add rsp, 0x38
ret
mov rax, -5
add rsp, 0x38
ret
mov rax, -5
add rsp, 0x38
ret
mov rax, -1
add rsp, 0x38
ret
mov rax, -1
add rsp, 0x38
ret
mov rax, -2
add rsp, 0x38
ret
