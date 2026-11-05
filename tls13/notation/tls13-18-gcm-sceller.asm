; tls13-18-gcm-sceller · bloc GCM sceller (SP 800-38D § 7.1 — CTR + étiquette) · spec tls13-18:R1 · bloc carte h100018
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0xe080, taille 1152 octets
; Domaine : tls13 (M9, l'ère 1.0.0) · Dépendances : tls13-16 (H = E(K,0) D'ABORD, les compteurs du CTR, E(K, J0)) + tls13-17 (CHAQUE bloc du GHASH — I2) ; J0 FIGÉ, CB la COPIE qui mute (inc32 u32 GROS-BOUTISTE par bswap — I3) ; le cadre 0xE8 : l'ombre + J0/CB/H/Y/X/ks + les pointeurs (I5 — tout sur la PILE) ; les refus -1/-2 NOMMÉS (Q3)
; Notation explicite générée par outils/auteur.py depuis brouillons/tls13-18-gcm-sceller.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 1076 o · padding : 76 o (NOP, 0x90)
; Étiquettes résolues : .aad_indifferent=0xe0df, .ctr=0xe1a5, .flot_pret=0xe1f8, .ctr_fin=0xe24c, .gh_aad=0xe27e, .gh_aad_plein=0xe2b2, .gh_aad_copie=0xe2b9, .gh_aad_octet=0xe2bc, .gh_aad_avance=0xe2d9, .gh_aad_fin=0xe32b, .gh_ct=0xe34b, .gh_ct_plein=0xe37f, .gh_ct_copie=0xe386, .gh_ct_octet=0xe389, .gh_ct_avance=0xe3a6, .gh_ct_fin=0xe3f8, .refus_nul=0xe496, .refus_taille=0xe4a5
; Appels directs (l'adresse scellée du plan — I1) : call 0xdf00, call 0xdf00, call 0xdfc0, call 0xdfc0, call 0xdfc0, call 0xdf00
sub rsp, 0xe8
test rcx, rcx
jz 0xe496
test rdx, rdx
jz 0xe496
test r8, r8
jz 0xe496
cmp r9, 0x4000
ja 0xe4a5
mov rax, qword ptr [rsp + 0x118]
cmp rax, 0x4000
ja 0xe4a5
cmp qword ptr [rsp + 0x118], 0
je 0xe0df
mov rax, qword ptr [rsp + 0x110]
test rax, rax
jz 0xe496
mov r10, qword ptr [rsp + 0x120]
test r10, r10
jz 0xe496
mov r11, qword ptr [rsp + 0x128]
test r11, r11
jz 0xe496
mov qword ptr [rsp + 0x80], rcx
mov qword ptr [rsp + 0x88], r8
mov qword ptr [rsp + 0x90], r10
mov qword ptr [rsp + 0xa8], r11
mov qword ptr [rsp + 0xb8], r9
mov rax, qword ptr [rsp + 0x118]
mov qword ptr [rsp + 0xc0], rax
mov rax, qword ptr [rdx]
mov qword ptr [rsp + 0x20], rax
mov eax, dword ptr [rdx + 8]
mov dword ptr [rsp + 0x28], eax
mov dword ptr [rsp + 0x2c], 0x01000000
mov rax, qword ptr [rsp + 0x20]
mov qword ptr [rsp + 0x30], rax
mov rax, qword ptr [rsp + 0x28]
mov qword ptr [rsp + 0x38], rax
mov qword ptr [rsp + 0x60], 0
mov qword ptr [rsp + 0x68], 0
mov rcx, qword ptr [rsp + 0x80]
lea rdx, [rsp + 0x60]
lea r8, [rsp + 0x40]
call 0xdf00
mov qword ptr [rsp + 0x98], 0
mov qword ptr [rsp + 0xb0], 0
mov rax, qword ptr [rsp + 0xb8]
cmp qword ptr [rsp + 0x98], rax
jae 0xe24c
cmp qword ptr [rsp + 0xb0], 0
jne 0xe1f8
mov eax, dword ptr [rsp + 0x3c]
bswap eax
add eax, 1
bswap eax
mov dword ptr [rsp + 0x3c], eax
mov rcx, qword ptr [rsp + 0x80]
lea rdx, [rsp + 0x30]
lea r8, [rsp + 0x70]
call 0xdf00
mov qword ptr [rsp + 0xb0], 16
mov rax, qword ptr [rsp + 0x88]
add rax, qword ptr [rsp + 0x98]
movzx edx, byte ptr [rax]
mov rcx, 16
sub rcx, qword ptr [rsp + 0xb0]
movzx r10, byte ptr [rsp + rcx + 0x70]
xor edx, r10d
mov rax, qword ptr [rsp + 0x90]
add rax, qword ptr [rsp + 0x98]
mov byte ptr [rax], dl
add qword ptr [rsp + 0x98], 1
sub qword ptr [rsp + 0xb0], 1
jmp 0xe1a5
mov qword ptr [rsp + 0x50], 0
mov qword ptr [rsp + 0x58], 0
mov rax, qword ptr [rsp + 0x110]
mov qword ptr [rsp + 0x98], rax
mov rax, qword ptr [rsp + 0xc0]
mov qword ptr [rsp + 0xa0], rax
cmp qword ptr [rsp + 0xa0], 0
je 0xe32b
mov qword ptr [rsp + 0x60], 0
mov qword ptr [rsp + 0x68], 0
mov rax, qword ptr [rsp + 0xa0]
cmp rax, 16
jae 0xe2b2
mov rcx, rax
jmp 0xe2b9
mov rcx, 16
xor r10d, r10d
cmp r10, rcx
jae 0xe2d9
mov rax, qword ptr [rsp + 0x98]
movzx r11, byte ptr [rax + r10]
mov byte ptr [rsp + r10 + 0x60], r11b
add r10, 1
jmp 0xe2bc
mov rax, qword ptr [rsp + 0x98]
add rax, rcx
mov qword ptr [rsp + 0x98], rax
sub qword ptr [rsp + 0xa0], rcx
mov rdx, qword ptr [rsp + 0x50]
xor rdx, qword ptr [rsp + 0x60]
mov qword ptr [rsp + 0x60], rdx
mov rdx, qword ptr [rsp + 0x58]
xor rdx, qword ptr [rsp + 0x68]
mov qword ptr [rsp + 0x68], rdx
lea rcx, [rsp + 0x50]
lea rdx, [rsp + 0x60]
lea r8, [rsp + 0x40]
call 0xdfc0
jmp 0xe27e
mov rax, qword ptr [rsp + 0x90]
mov qword ptr [rsp + 0x98], rax
mov rax, qword ptr [rsp + 0xb8]
mov qword ptr [rsp + 0xa0], rax
cmp qword ptr [rsp + 0xa0], 0
je 0xe3f8
mov qword ptr [rsp + 0x60], 0
mov qword ptr [rsp + 0x68], 0
mov rax, qword ptr [rsp + 0xa0]
cmp rax, 16
jae 0xe37f
mov rcx, rax
jmp 0xe386
mov rcx, 16
xor r10d, r10d
cmp r10, rcx
jae 0xe3a6
mov rax, qword ptr [rsp + 0x98]
movzx r11, byte ptr [rax + r10]
mov byte ptr [rsp + r10 + 0x60], r11b
add r10, 1
jmp 0xe389
mov rax, qword ptr [rsp + 0x98]
add rax, rcx
mov qword ptr [rsp + 0x98], rax
sub qword ptr [rsp + 0xa0], rcx
mov rdx, qword ptr [rsp + 0x50]
xor rdx, qword ptr [rsp + 0x60]
mov qword ptr [rsp + 0x60], rdx
mov rdx, qword ptr [rsp + 0x58]
xor rdx, qword ptr [rsp + 0x68]
mov qword ptr [rsp + 0x68], rdx
lea rcx, [rsp + 0x50]
lea rdx, [rsp + 0x60]
lea r8, [rsp + 0x40]
call 0xdfc0
jmp 0xe34b
mov rax, qword ptr [rsp + 0xc0]
shl rax, 3
bswap rax
mov qword ptr [rsp + 0x60], rax
mov rax, qword ptr [rsp + 0xb8]
shl rax, 3
bswap rax
mov qword ptr [rsp + 0x68], rax
mov rdx, qword ptr [rsp + 0x50]
xor rdx, qword ptr [rsp + 0x60]
mov qword ptr [rsp + 0x60], rdx
mov rdx, qword ptr [rsp + 0x58]
xor rdx, qword ptr [rsp + 0x68]
mov qword ptr [rsp + 0x68], rdx
lea rcx, [rsp + 0x50]
lea rdx, [rsp + 0x60]
lea r8, [rsp + 0x40]
call 0xdfc0
mov rcx, qword ptr [rsp + 0x80]
lea rdx, [rsp + 0x20]
lea r8, [rsp + 0x70]
call 0xdf00
mov rax, qword ptr [rsp + 0x70]
xor rax, qword ptr [rsp + 0x50]
mov rdx, qword ptr [rsp + 0x78]
xor rdx, qword ptr [rsp + 0x58]
mov rcx, qword ptr [rsp + 0xa8]
mov qword ptr [rcx], rax
mov qword ptr [rcx + 8], rdx
xor eax, eax
add rsp, 0xe8
ret
mov rax, -1
add rsp, 0xe8
ret
mov rax, -2
add rsp, 0xe8
ret
