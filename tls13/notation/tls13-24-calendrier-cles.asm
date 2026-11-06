; tls13-24-calendrier-cles · bloc le calendrier de clés (RFC 8446 § 7.1, trois étages) · spec tls13-24:R1 · bloc carte h100024
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0xf060, taille 2176 octets
; Domaine : tls13 (M9, l'ère 1.0.0) · Dépendances : bloc ; tls13-06 (l'extrait — UN par étage), tls13-08 (l'étiquette — TOUTES les clés : les libellés aux fixtures R_LIB_* du plan, données PUBLIQUES), tls13-15 (le déploiement des clés de tour), tls13-01 + tls13-04 (le condensé du VIDE — le contexte de « derived » : l'erratum n° 2 sur pièces, Hash du VIDE de 32 o, JAMAIS zéro octet) ; la machine à TROIS étages STRICTS (-3 sur tout saut), le contexte porte (secret courant, étape), les contextes sortis COMPLETS (rk 176 + IV 12 + réserve 4 + séquence u64) ; le hash du transcript est un ARGUMENT (I1 — le principal tient le contexte SHA) ; le calendrier ne hache RIEN
; Notation explicite générée par outils/auteur.py depuis brouillons/tls13-24-calendrier-cles.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 2130 o · padding : 46 o (NOP, 0x90)
; Étiquettes résolues : .etage1=0xf109, .etage2=0xf1c4, .etage3=0xf59f, .refus_propage=0xf88c, .refus_nul=0xf894, .refus_etat=0xf8a3
; Déplacements RIP (cible = adresse + taille + disp) :
;   0xf13a + 0x7 + 0x1a3f = 0x10b80
;   0xf210 + 0x7 + 0x1979 = 0x10b90
;   0xf25d + 0x7 + 0x196c = 0x10bd0
;   0xf2c0 + 0x7 + 0x1911 = 0x10bd8
;   0xf342 + 0x7 + 0x1897 = 0x10be0
;   0xf38f + 0x7 + 0x180a = 0x10ba0
;   0xf3dc + 0x7 + 0x17ed = 0x10bd0
;   0xf446 + 0x7 + 0x178b = 0x10bd8
;   0xf4c8 + 0x7 + 0x1711 = 0x10be0
;   0xf515 + 0x7 + 0x1664 = 0x10b80
;   0xf5e8 + 0x7 + 0x15c1 = 0x10bb0
;   0xf631 + 0x7 + 0x1598 = 0x10bd0
;   0xf694 + 0x7 + 0x153d = 0x10bd8
;   0xf716 + 0x7 + 0x14a3 = 0x10bc0
;   0xf75f + 0x7 + 0x146a = 0x10bd0
;   0xf7c9 + 0x7 + 0x1408 = 0x10bd8
; Appels directs (l'adresse scellée du plan — I1) : call 0xc000, call 0xc300, call 0xc5c0, call 0xc800, call 0xc5c0, call 0xc800, call 0xc800, call 0xdcc0, call 0xc800, call 0xc800, call 0xc800, call 0xc800, call 0xdcc0, call 0xc800, call 0xc800, call 0xc800, call 0xc5c0, call 0xc800, call 0xc800, call 0xdcc0, call 0xc800, call 0xc800, call 0xc800, call 0xdcc0, call 0xc800
sub rsp, 0x188
test rcx, rcx
jz 0xf894
mov qword ptr [rsp + 0x170], rdx
mov qword ptr [rsp + 0x178], rcx
mov qword ptr [rsp + 0x180], r8
mov qword ptr [rsp + 0x40], 0
mov qword ptr [rsp + 0x48], 0
mov qword ptr [rsp + 0x50], 0
mov qword ptr [rsp + 0x58], 0
lea rcx, [rsp + 0xe0]
call 0xc000
test eax, eax
jnz 0xf88c
lea rcx, [rsp + 0xe0]
lea rdx, [rsp + 0x150]
call 0xc300
test eax, eax
jnz 0xf88c
mov r10, qword ptr [rsp + 0x178]
mov r10d, dword ptr [r10 + 32]
cmp r10d, 0
je 0xf109
cmp r10d, 1
je 0xf1c4
cmp r10d, 2
je 0xf59f
jmp 0xf8a3
lea rcx, [rsp + 0x40]
mov edx, 32
lea r8, [rsp + 0x40]
mov r9d, 32
lea r10, [rsp + 0x60]
mov qword ptr [rsp + 0x20], r10
call 0xc5c0
test eax, eax
jnz 0xf88c
lea rcx, [rsp + 0x60]
lea rdx, [rip + 0x1a3f]
mov r8d, 7
lea r9, [rsp + 0x150]
mov qword ptr [rsp + 0x20], 32
mov qword ptr [rsp + 0x28], 32
lea r10, [rsp + 0xa0]
mov qword ptr [rsp + 0x30], r10
call 0xc800
test eax, eax
jnz 0xf88c
mov r10, qword ptr [rsp + 0x178]
mov r11, qword ptr [rsp + 0xa0]
mov qword ptr [r10], r11
mov r11, qword ptr [rsp + 0xa8]
mov qword ptr [r10 + 8], r11
mov r11, qword ptr [rsp + 0xb0]
mov qword ptr [r10 + 16], r11
mov r11, qword ptr [rsp + 0xb8]
mov qword ptr [r10 + 24], r11
mov dword ptr [r10 + 32], 1
xor eax, eax
add rsp, 0x188
ret
cmp qword ptr [rsp + 0x180], 0
je 0xf894
mov rcx, qword ptr [rsp + 0x178]
mov edx, 32
mov r8, qword ptr [rsp + 0x170]
mov r9d, 32
lea r10, [rsp + 0x80]
mov qword ptr [rsp + 0x20], r10
call 0xc5c0
test eax, eax
jnz 0xf88c
lea rcx, [rsp + 0x80]
lea rdx, [rip + 0x1979]
mov r8d, 12
mov r9, qword ptr [rsp + 0x170]
add r9, 32
mov qword ptr [rsp + 0x20], 32
mov qword ptr [rsp + 0x28], 32
lea r10, [rsp + 0xa0]
mov qword ptr [rsp + 0x30], r10
call 0xc800
test eax, eax
jnz 0xf88c
lea rcx, [rsp + 0xa0]
lea rdx, [rip + 0x196c]
mov r8d, 3
lea r9, [rsp + 0x40]
mov qword ptr [rsp + 0x20], 0
mov qword ptr [rsp + 0x28], 16
lea r10, [rsp + 0xc0]
mov qword ptr [rsp + 0x30], r10
call 0xc800
test eax, eax
jnz 0xf88c
lea rcx, [rsp + 0xc0]
mov rdx, qword ptr [rsp + 0x180]
call 0xdcc0
test eax, eax
jnz 0xf88c
lea rcx, [rsp + 0xa0]
lea rdx, [rip + 0x1911]
mov r8d, 2
lea r9, [rsp + 0x40]
mov qword ptr [rsp + 0x20], 0
mov qword ptr [rsp + 0x28], 12
lea r10, [rsp + 0xd0]
mov qword ptr [rsp + 0x30], r10
call 0xc800
test eax, eax
jnz 0xf88c
mov r10, qword ptr [rsp + 0x180]
mov r11, qword ptr [rsp + 0xd0]
mov qword ptr [r10 + 176], r11
mov r11d, dword ptr [rsp + 0xd8]
mov dword ptr [r10 + 184], r11d
mov dword ptr [r10 + 188], 0
mov qword ptr [r10 + 192], 0
lea rcx, [rsp + 0xa0]
lea rdx, [rip + 0x1897]
mov r8d, 8
lea r9, [rsp + 0x40]
mov qword ptr [rsp + 0x20], 0
mov qword ptr [rsp + 0x28], 32
mov r10, qword ptr [rsp + 0x180]
add r10, 400
mov qword ptr [rsp + 0x30], r10
call 0xc800
test eax, eax
jnz 0xf88c
lea rcx, [rsp + 0x80]
lea rdx, [rip + 0x180a]
mov r8d, 12
mov r9, qword ptr [rsp + 0x170]
add r9, 32
mov qword ptr [rsp + 0x20], 32
mov qword ptr [rsp + 0x28], 32
lea r10, [rsp + 0xa0]
mov qword ptr [rsp + 0x30], r10
call 0xc800
test eax, eax
jnz 0xf88c
lea rcx, [rsp + 0xa0]
lea rdx, [rip + 0x17ed]
mov r8d, 3
lea r9, [rsp + 0x40]
mov qword ptr [rsp + 0x20], 0
mov qword ptr [rsp + 0x28], 16
lea r10, [rsp + 0xc0]
mov qword ptr [rsp + 0x30], r10
call 0xc800
test eax, eax
jnz 0xf88c
lea rcx, [rsp + 0xc0]
mov rdx, qword ptr [rsp + 0x180]
add rdx, 200
call 0xdcc0
test eax, eax
jnz 0xf88c
lea rcx, [rsp + 0xa0]
lea rdx, [rip + 0x178b]
mov r8d, 2
lea r9, [rsp + 0x40]
mov qword ptr [rsp + 0x20], 0
mov qword ptr [rsp + 0x28], 12
lea r10, [rsp + 0xd0]
mov qword ptr [rsp + 0x30], r10
call 0xc800
test eax, eax
jnz 0xf88c
mov r10, qword ptr [rsp + 0x180]
mov r11, qword ptr [rsp + 0xd0]
mov qword ptr [r10 + 376], r11
mov r11d, dword ptr [rsp + 0xd8]
mov dword ptr [r10 + 384], r11d
mov dword ptr [r10 + 388], 0
mov qword ptr [r10 + 392], 0
lea rcx, [rsp + 0xa0]
lea rdx, [rip + 0x1711]
mov r8d, 8
lea r9, [rsp + 0x40]
mov qword ptr [rsp + 0x20], 0
mov qword ptr [rsp + 0x28], 32
mov r10, qword ptr [rsp + 0x180]
add r10, 432
mov qword ptr [rsp + 0x30], r10
call 0xc800
test eax, eax
jnz 0xf88c
lea rcx, [rsp + 0x80]
lea rdx, [rip + 0x1664]
mov r8d, 7
lea r9, [rsp + 0x150]
mov qword ptr [rsp + 0x20], 32
mov qword ptr [rsp + 0x28], 32
lea r10, [rsp + 0xa0]
mov qword ptr [rsp + 0x30], r10
call 0xc800
test eax, eax
jnz 0xf88c
mov r10, qword ptr [rsp + 0x178]
mov r11, qword ptr [rsp + 0xa0]
mov qword ptr [r10], r11
mov r11, qword ptr [rsp + 0xa8]
mov qword ptr [r10 + 8], r11
mov r11, qword ptr [rsp + 0xb0]
mov qword ptr [r10 + 16], r11
mov r11, qword ptr [rsp + 0xb8]
mov qword ptr [r10 + 24], r11
mov dword ptr [r10 + 32], 2
xor eax, eax
add rsp, 0x188
ret
cmp qword ptr [rsp + 0x180], 0
je 0xf894
mov rcx, qword ptr [rsp + 0x178]
mov edx, 32
lea r8, [rsp + 0x40]
mov r9d, 32
lea r10, [rsp + 0x80]
mov qword ptr [rsp + 0x20], r10
call 0xc5c0
test eax, eax
jnz 0xf88c
lea rcx, [rsp + 0x80]
lea rdx, [rip + 0x15c1]
mov r8d, 12
mov r9, qword ptr [rsp + 0x170]
mov qword ptr [rsp + 0x20], 32
mov qword ptr [rsp + 0x28], 32
lea r10, [rsp + 0xa0]
mov qword ptr [rsp + 0x30], r10
call 0xc800
test eax, eax
jnz 0xf88c
lea rcx, [rsp + 0xa0]
lea rdx, [rip + 0x1598]
mov r8d, 3
lea r9, [rsp + 0x40]
mov qword ptr [rsp + 0x20], 0
mov qword ptr [rsp + 0x28], 16
lea r10, [rsp + 0xc0]
mov qword ptr [rsp + 0x30], r10
call 0xc800
test eax, eax
jnz 0xf88c
lea rcx, [rsp + 0xc0]
mov rdx, qword ptr [rsp + 0x180]
call 0xdcc0
test eax, eax
jnz 0xf88c
lea rcx, [rsp + 0xa0]
lea rdx, [rip + 0x153d]
mov r8d, 2
lea r9, [rsp + 0x40]
mov qword ptr [rsp + 0x20], 0
mov qword ptr [rsp + 0x28], 12
lea r10, [rsp + 0xd0]
mov qword ptr [rsp + 0x30], r10
call 0xc800
test eax, eax
jnz 0xf88c
mov r10, qword ptr [rsp + 0x180]
mov r11, qword ptr [rsp + 0xd0]
mov qword ptr [r10 + 176], r11
mov r11d, dword ptr [rsp + 0xd8]
mov dword ptr [r10 + 184], r11d
mov dword ptr [r10 + 188], 0
mov qword ptr [r10 + 192], 0
lea rcx, [rsp + 0x80]
lea rdx, [rip + 0x14a3]
mov r8d, 12
mov r9, qword ptr [rsp + 0x170]
mov qword ptr [rsp + 0x20], 32
mov qword ptr [rsp + 0x28], 32
lea r10, [rsp + 0xa0]
mov qword ptr [rsp + 0x30], r10
call 0xc800
test eax, eax
jnz 0xf88c
lea rcx, [rsp + 0xa0]
lea rdx, [rip + 0x146a]
mov r8d, 3
lea r9, [rsp + 0x40]
mov qword ptr [rsp + 0x20], 0
mov qword ptr [rsp + 0x28], 16
lea r10, [rsp + 0xc0]
mov qword ptr [rsp + 0x30], r10
call 0xc800
test eax, eax
jnz 0xf88c
lea rcx, [rsp + 0xc0]
mov rdx, qword ptr [rsp + 0x180]
add rdx, 200
call 0xdcc0
test eax, eax
jnz 0xf88c
lea rcx, [rsp + 0xa0]
lea rdx, [rip + 0x1408]
mov r8d, 2
lea r9, [rsp + 0x40]
mov qword ptr [rsp + 0x20], 0
mov qword ptr [rsp + 0x28], 12
lea r10, [rsp + 0xd0]
mov qword ptr [rsp + 0x30], r10
call 0xc800
test eax, eax
jnz 0xf88c
mov r10, qword ptr [rsp + 0x180]
mov r11, qword ptr [rsp + 0xd0]
mov qword ptr [r10 + 376], r11
mov r11d, dword ptr [rsp + 0xd8]
mov dword ptr [r10 + 384], r11d
mov dword ptr [r10 + 388], 0
mov qword ptr [r10 + 392], 0
mov r10, qword ptr [rsp + 0x178]
mov r11, qword ptr [rsp + 0x80]
mov qword ptr [r10], r11
mov r11, qword ptr [rsp + 0x88]
mov qword ptr [r10 + 8], r11
mov r11, qword ptr [rsp + 0x90]
mov qword ptr [r10 + 16], r11
mov r11, qword ptr [rsp + 0x98]
mov qword ptr [r10 + 24], r11
mov dword ptr [r10 + 32], 3
xor eax, eax
add rsp, 0x188
ret
add rsp, 0x188
ret
mov rax, -1
add rsp, 0x188
ret
mov rax, -3
add rsp, 0x188
ret
