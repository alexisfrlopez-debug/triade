; tls13-18-gcm-sceller · brouillon étiqueté — spec tls13-18:R1, bloc carte h100018
; GCM : SCELLER — le mode authentifié SP 800-38D § 7.1 : le compteur
; J0 = nonce || 0^31 || 1 (le nonce de 12 o — RFC 8446 § 5.3, GCM_NONCE
; du plan) ; le chiffrage CTR (les blocs de compteur 2, 3, 4… chiffrés
; par tls13-16, XOR au clair) ; l'étiquette : GHASH sur AAD || bourre au
; 16 || chiffré || bourre au 16 || [longueur(AAD) en BITS]64 ||
; [longueur(chiffré) en BITS]64 (les u64 GROS-BOUTISTES), puis
; l'étiquette = E(K, J0) ⊕ GHASH — avec H = E(K, 0^128), calculé au
; geste même, JAMAIS détenu (charte § 6 : aucun état hors la pile).
; L'ORDRE DES OPÉRATIONS (I1) : H D'ABORD, PUIS LE CTR (le chiffré
; EXISTE avant le GHASH qui le digère), PUIS l'étiquette ; le GHASH
; accumule par APPELS RÉPÉTÉS à tls13-17 — l'itération de la § 6.4 :
; Y ← (Y ⊕ X) • H, bloc de 16 o par bloc (I2), l'AAD et le chiffré
; zéro-bourrés au dernier bloc, les DEUX longueurs en bits u64
; gros-boutistes ; LE COMPTEUR (I3) : inc32 — le u32 GROS-BOUTISTE de
; CB incrémenté depuis 2 (bswap/add/bswap, l'arithmétique exacte de la
; norme § 6.2), J0 FIGÉ dans son logement (le bloc compteur CB en est
; une COPIE qui mute : l'étiquette relit J0 INTACT), le rendement de
; compteur (2^32 blocs) est hors d'atteinte par P4 (2^14 = 1024 blocs —
; la contre-preuve du labo).
; rcx = les clés de tour (176 o — le produit de tls13-15) · rdx = le
; nonce (12 o) · r8 = le clair (N octets) · r9 = N (0 ≤ N ≤ 2^14 — la
; borne de la couche enregistrement : le GCM tolère 2^39 bits, le
; protocole TLS n'émet jamais plus de 2^14 par enregistrement, la brique
; prend la borne du protocole) · [rsp+0x28] = l'AAD (A octets) ·
; [rsp+0x30] = A (0 ≤ A ≤ 2^14) · [rsp+0x38] = la sortie chiffrée (N o) ·
; [rsp+0x40] = la sortie étiquette (16 o) · Q1 le chiffré = CTR(K,
; nonce, clair) et l'étiquette = le tag GCM — les Test Cases 1..6 de
; McGrew–Viega (CAVP) ET le TRANSFERT RFC 8448 (les enregistrements du
; transcript, octet pour octet, par les clés du calendrier) · Q2 le
; clair, l'AAD et le nonce INTACTS · Q3 rax = 0, ou -1/-2 NOMMÉS
; (pointeurs nuls ; N ou A hors borne — les SEPT verdicts de la table,
; jamais un échec muet).
; LE CADRE (0xE8 = 232 o, entrée ≡ 8 → 8−232 ≡ 0 (mod 16) au point
; d'appel) : l'ombre msx64 0x20 POUR LES APPELS à TLS16/TLS17 (la
; convention de la famille), les transitoires SUR LA PILE (I5 — J0
; [0x20], CB [0x30], H [0x40], Y [0x50], X [0x60], ks [0x70], puis les
; pointeurs et comptes) ; la copie OCTET PAR OCTET du clair au chiffré
; (alias-safe : chaque octet lu AVANT d'être écrit) ; les longueurs N et
; A sont PUBLIQUES (les branches de contrôle et de boucle ne lisent
; JAMAIS une donnée secrète — I4 : le temps constant hérité de
; tls13-16/17, la longueur seule mène la danse).
; COMPOSITION DÉCLARÉE (I2) : tls13-16 aux appels H, CTR et E(K, J0) ;
; tls13-17 à CHAQUE bloc du GHASH. AUCUN déplacement RIP ; AUCUNE entrée
; IAT, AUCUN site syscall (charte § 7) ; aucun registre non volatil
; détruit ; NOP, 0x90 (charte § 8).
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
call TLS16
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
jmp .ctr
.ctr_fin:
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
mov rcx, qword ptr [rsp + 0xa8]
mov qword ptr [rcx], rax
mov qword ptr [rcx + 8], rdx
xor eax, eax
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
