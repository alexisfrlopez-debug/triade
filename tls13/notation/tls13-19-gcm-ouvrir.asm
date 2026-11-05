; tls13-19-gcm-ouvrir · bloc GCM ouvrir (le verdict AVANT la restitution, fail-closed) · spec tls13-19:R1 · bloc carte h100019
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0xe500, taille 1216 octets
; Domaine : tls13 (M9, l'ère 1.0.0) · Dépendances : tls13-16 + tls13-17 (la même recette que 18 sur le chiffré REÇU) ; LA DISCIPLINE DU VERDICT — la confrontation TEMPS CONSTANT (I1 : le OU cumulatif des 16 différences en UN seul drapeau, AUCUN court-circuit, le branch sur LE drapeau), PUIS le CTR : LA RESTITUTION EST LA DERNIÈRE OPÉRATION (I2) ; l'étiquette divergente → rax = -4 NOMMÉ, la sortie INTACTE
; Notation explicite générée par outils/auteur.py depuis brouillons/tls13-19-gcm-ouvrir.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 1163 o · padding : 53 o (NOP, 0x90)
; Étiquettes résolues : .aad_indifferent=0xe55f, .gh_aad=0xe63f, .gh_aad_plein=0xe673, .gh_aad_copie=0xe67a, .gh_aad_octet=0xe67d, .gh_aad_avance=0xe69a, .gh_aad_fin=0xe6ec, .gh_ct=0xe70c, .gh_ct_plein=0xe740, .gh_ct_copie=0xe747, .gh_ct_octet=0xe74a, .gh_ct_avance=0xe767, .gh_ct_fin=0xe7b9, .conf=0xe857, .ctr=0xe8ad, .flot_pret=0xe900, .ctr_fin=0xe954, .divergente=0xe95e, .refus_nul=0xe96d, .refus_taille=0xe97c
; Appels directs (l'adresse scellée du plan — I1) : call 0xdf00, call 0xdfc0, call 0xdfc0, call 0xdfc0, call 0xdf00, call 0xdf00
sub rsp, 0xe8
test rcx, rcx
jz 0xe96d
test rdx, rdx
jz 0xe96d
test r8, r8
jz 0xe96d
cmp r9, 0x4000
ja 0xe97c
mov rax, qword ptr [rsp + 0x118]
cmp rax, 0x4000
ja 0xe97c
cmp qword ptr [rsp + 0x118], 0
je 0xe55f
mov rax, qword ptr [rsp + 0x110]
test rax, rax
jz 0xe96d
mov r10, qword ptr [rsp + 0x120]
test r10, r10
jz 0xe96d
mov r11, qword ptr [rsp + 0x128]
test r11, r11
jz 0xe96d
mov qword ptr [rsp + 0x80], rcx
mov qword ptr [rsp + 0x88], r11
mov qword ptr [rsp + 0x90], r8
mov qword ptr [rsp + 0xa8], r10
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
mov qword ptr [rsp + 0x50], 0
mov qword ptr [rsp + 0x58], 0
mov rax, qword ptr [rsp + 0x110]
mov qword ptr [rsp + 0x98], rax
mov rax, qword ptr [rsp + 0xc0]
mov qword ptr [rsp + 0xa0], rax
cmp qword ptr [rsp + 0xa0], 0
je 0xe6ec
mov qword ptr [rsp + 0x60], 0
mov qword ptr [rsp + 0x68], 0
mov rax, qword ptr [rsp + 0xa0]
cmp rax, 16
jae 0xe673
mov rcx, rax
jmp 0xe67a
mov rcx, 16
xor r10d, r10d
cmp r10, rcx
jae 0xe69a
mov rax, qword ptr [rsp + 0x98]
movzx r11, byte ptr [rax + r10]
mov byte ptr [rsp + r10 + 0x60], r11b
add r10, 1
jmp 0xe67d
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
jmp 0xe63f
mov rax, qword ptr [rsp + 0x90]
mov qword ptr [rsp + 0x98], rax
mov rax, qword ptr [rsp + 0xb8]
mov qword ptr [rsp + 0xa0], rax
cmp qword ptr [rsp + 0xa0], 0
je 0xe7b9
mov qword ptr [rsp + 0x60], 0
mov qword ptr [rsp + 0x68], 0
mov rax, qword ptr [rsp + 0xa0]
cmp rax, 16
jae 0xe740
mov rcx, rax
jmp 0xe747
mov rcx, 16
xor r10d, r10d
cmp r10, rcx
jae 0xe767
mov rax, qword ptr [rsp + 0x98]
movzx r11, byte ptr [rax + r10]
mov byte ptr [rsp + r10 + 0x60], r11b
add r10, 1
jmp 0xe74a
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
jmp 0xe70c
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
mov qword ptr [rsp + 0x70], rax
mov qword ptr [rsp + 0x78], rdx
mov qword ptr [rsp + 0xb0], 0
xor r10d, r10d
mov rax, qword ptr [rsp + 0xb0]
movzx rdx, byte ptr [rsp + rax + 0x70]
mov rcx, qword ptr [rsp + 0xa8]
movzx r11, byte ptr [rcx + rax]
xor rdx, r11
or r10, rdx
add qword ptr [rsp + 0xb0], 1
cmp qword ptr [rsp + 0xb0], 16
jb 0xe857
test r10, r10
jnz 0xe95e
mov qword ptr [rsp + 0x98], 0
mov qword ptr [rsp + 0xb0], 0
mov rax, qword ptr [rsp + 0xb8]
cmp qword ptr [rsp + 0x98], rax
jae 0xe954
cmp qword ptr [rsp + 0xb0], 0
jne 0xe900
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
mov rax, qword ptr [rsp + 0x90]
add rax, qword ptr [rsp + 0x98]
movzx edx, byte ptr [rax]
mov rcx, 16
sub rcx, qword ptr [rsp + 0xb0]
movzx r10, byte ptr [rsp + rcx + 0x70]
xor edx, r10d
mov rax, qword ptr [rsp + 0x88]
add rax, qword ptr [rsp + 0x98]
mov byte ptr [rax], dl
add qword ptr [rsp + 0x98], 1
sub qword ptr [rsp + 0xb0], 1
jmp 0xe8ad
xor eax, eax
add rsp, 0xe8
ret
mov rax, -4
add rsp, 0xe8
ret
mov rax, -1
add rsp, 0xe8
ret
mov rax, -2
add rsp, 0xe8
ret
