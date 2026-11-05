; tls13-19-gcm-ouvrir · brouillon étiqueté — spec tls13-19:R1, bloc carte h100019
; GCM : OUVRIR — l'inverse EXACT de tls13-18, AVEC LA DISCIPLINE DU
; VERDICT : l'étiquette est RECALCULÉE sur le chiffré reçu et CONFRONTÉE
; AVANT TOUTE restitution (RFC 8446 § 5.2 : l'enregistrement entier doit
; être authentifié avant de rendre un octet — jamais l'inverse). LA
; CONFRONTATION TEMPS CONSTANT (I1) : le OU cumulatif des 16 différences
; octet par octet accumulées en UN SEUL drapeau — AUCUN court-circuit
; (un arrêt précoce serait une fuite), le branch final se prononce sur
; LE drapeau, jamais sur un octet isolé.
; L'ORDRE (I2) : H, le GHASH (sur le CHIFFRÉ REÇU), la confrontation,
; PUIS le CTR — LA RESTITUTION EST LA DERNIÈRE OPÉRATION du bloc : si
; l'étiquette diffère, rax = -4 NOMMÉ (cryptographie divergente — la
; table des SEPT verdicts du domaine, fail-closed) et la sortie clair
; demeure INTACTE : AUCUN octet restitué.
; rcx = les clés de tour (176 o) · rdx = le nonce (12 o) · r8 = le
; chiffré reçu (N octets) · r9 = N (0 ≤ N ≤ 2^14) · [rsp+0x28] = l'AAD
; (A octets) · [rsp+0x30] = A (0 ≤ A ≤ 2^14) · [rsp+0x38] = l'étiquette
; REÇUE (16 o) · [rsp+0x40] = la sortie clair (N o — ÉCRITE SEULEMENT
; SI l'étiquette est CONFORME, P8) · Q1 l'étiquette recalculée (la même
; recette que tls13-18 — H, le GHASH du chiffré, E(K, J0) ⊕ GHASH)
; confrontée : si elle DIFFÈRE, rax = -4 et la sortie INTACTE · Q2 si
; CONFORME : la sortie = le clair (le CTR du chiffré — LA BRIQUE
; D'INVERSION AES N'EXISTE PAS : tls13-16 re-chiffre les compteurs) ;
; rax = 0 · Q3 le chiffré reçu, l'AAD et l'étiquette reçue INTACTS · Q4
; LA PREUVE : les vecteurs de tls13-18 en sens inverse (les Test Cases
; McGrew–Viega ouverts) ET LA FALSIFICATION INVITÉE — chaque octet du
; chiffré muté → -4, chaque octet de l'étiquette muté → -4 (la garde
; constatée sur pièces, mutation par mutation).
; LE CADRE (0xE8 — le miroir EXACT de tls13-18 : l'ombre, J0 [0x20]
; FIGÉ, CB [0x30] la copie qui mute, H [0x40], Y [0x50], X [0x60], ks
; [0x70], les pointeurs et comptes ; les transitoires sur la PILE, I3) ;
; la confrontation boucle sur l'INDICE PUBLIC (16 itérations TOUJOURS,
; le corps sans branche), le drapeau vit en r10 D'UN BOUT À L'AUTRE
; (aucun appel dans la boucle) ; la restitution CTR ne commence qu'après
; le verdict — LA SORTIE NE PEUT PAS ÊTRE ÉCRITE AVANT.
; COMPOSITION DÉCLARÉE : tls13-16 (H, E(K, J0), les compteurs du CTR) ;
; tls17 (chaque bloc du GHASH). AUCUN déplacement RIP ; AUCUNE entrée
; IAT, AUCUN site syscall (charte § 7) ; aucun registre non volatil
; détruit (I4) ; NOP, 0x90 (charte § 8).
sub rsp, 0xe8
test rcx, rcx
jz .refus_nul
test rdx, rdx
jz .refus_nul
test r8, r8
jz .refus_nul
cmp r9, 0x4000
ja .refus_taille
mov rax, qword ptr [rsp + 0x118]
cmp rax, 0x4000
ja .refus_taille
cmp qword ptr [rsp + 0x118], 0
je .aad_indifferent
mov rax, qword ptr [rsp + 0x110]
test rax, rax
jz .refus_nul
.aad_indifferent:
mov r10, qword ptr [rsp + 0x120]
test r10, r10
jz .refus_nul
mov r11, qword ptr [rsp + 0x128]
test r11, r11
jz .refus_nul
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
call TLS16
mov qword ptr [rsp + 0x50], 0
mov qword ptr [rsp + 0x58], 0
mov rax, qword ptr [rsp + 0x110]
mov qword ptr [rsp + 0x98], rax
mov rax, qword ptr [rsp + 0xc0]
mov qword ptr [rsp + 0xa0], rax
.gh_aad:
cmp qword ptr [rsp + 0xa0], 0
je .gh_aad_fin
mov qword ptr [rsp + 0x60], 0
mov qword ptr [rsp + 0x68], 0
mov rax, qword ptr [rsp + 0xa0]
cmp rax, 16
jae .gh_aad_plein
mov rcx, rax
jmp .gh_aad_copie
.gh_aad_plein:
mov rcx, 16
.gh_aad_copie:
xor r10d, r10d
.gh_aad_octet:
cmp r10, rcx
jae .gh_aad_avance
mov rax, qword ptr [rsp + 0x98]
movzx r11, byte ptr [rax + r10]
mov byte ptr [rsp + r10 + 0x60], r11b
add r10, 1
jmp .gh_aad_octet
.gh_aad_avance:
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
call TLS17
jmp .gh_aad
.gh_aad_fin:
mov rax, qword ptr [rsp + 0x90]
mov qword ptr [rsp + 0x98], rax
mov rax, qword ptr [rsp + 0xb8]
mov qword ptr [rsp + 0xa0], rax
.gh_ct:
cmp qword ptr [rsp + 0xa0], 0
je .gh_ct_fin
mov qword ptr [rsp + 0x60], 0
mov qword ptr [rsp + 0x68], 0
mov rax, qword ptr [rsp + 0xa0]
cmp rax, 16
jae .gh_ct_plein
mov rcx, rax
jmp .gh_ct_copie
.gh_ct_plein:
mov rcx, 16
.gh_ct_copie:
xor r10d, r10d
.gh_ct_octet:
cmp r10, rcx
jae .gh_ct_avance
mov rax, qword ptr [rsp + 0x98]
movzx r11, byte ptr [rax + r10]
mov byte ptr [rsp + r10 + 0x60], r11b
add r10, 1
jmp .gh_ct_octet
.gh_ct_avance:
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
call TLS17
jmp .gh_ct
.gh_ct_fin:
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
call TLS17
mov rcx, qword ptr [rsp + 0x80]
lea rdx, [rsp + 0x20]
lea r8, [rsp + 0x70]
call TLS16
mov rax, qword ptr [rsp + 0x70]
xor rax, qword ptr [rsp + 0x50]
mov rdx, qword ptr [rsp + 0x78]
xor rdx, qword ptr [rsp + 0x58]
mov qword ptr [rsp + 0x70], rax
mov qword ptr [rsp + 0x78], rdx
mov qword ptr [rsp + 0xb0], 0
xor r10d, r10d
.conf:
mov rax, qword ptr [rsp + 0xb0]
movzx rdx, byte ptr [rsp + rax + 0x70]
mov rcx, qword ptr [rsp + 0xa8]
movzx r11, byte ptr [rcx + rax]
xor rdx, r11
or r10, rdx
add qword ptr [rsp + 0xb0], 1
cmp qword ptr [rsp + 0xb0], 16
jb .conf
test r10, r10
jnz .divergente
mov qword ptr [rsp + 0x98], 0
mov qword ptr [rsp + 0xb0], 0
.ctr:
mov rax, qword ptr [rsp + 0xb8]
cmp qword ptr [rsp + 0x98], rax
jae .ctr_fin
cmp qword ptr [rsp + 0xb0], 0
jne .flot_pret
mov eax, dword ptr [rsp + 0x3c]
bswap eax
add eax, 1
bswap eax
mov dword ptr [rsp + 0x3c], eax
mov rcx, qword ptr [rsp + 0x80]
lea rdx, [rsp + 0x30]
lea r8, [rsp + 0x70]
call TLS16
mov qword ptr [rsp + 0xb0], 16
.flot_pret:
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
jmp .ctr
.ctr_fin:
xor eax, eax
add rsp, 0xe8
ret
.divergente:
mov rax, -4
add rsp, 0xe8
ret
.refus_nul:
mov rax, -1
add rsp, 0xe8
ret
.refus_taille:
mov rax, -2
add rsp, 0xe8
ret
