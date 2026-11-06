; tls13-20-enregistrement-proteger · brouillon étiqueté — spec tls13-20:R1, bloc carte h100020
; LA COUCHE ENREGISTREMENT — PROTÉGER (RFC 8446 § 5.2) : le texte interne
; = charge || type (BOURRE LONGUEUR ZÉRO : le choix minimal, la
; possibilité de bourre d'opacité est un CHANTIER FUTUR nommé), le nonce
; = IV statique ⊕ numéro de séquence (le u64 GROS-BOUTISTE posé sur les
; HUIT derniers octets du IV — RFC 8446 § 5.3), l'AAD = l'en-tête
; COMPLÈTE de l'enregistrement émis (23 opaque, 0x0303 héritage, N+17 en
; u16 GROS-BOUTISTE — CINQ octets FIXES), le tout scellé par tls13-18.
; L'enregistrement protégé est TOUJOURS de type opaque 23 — le type réel
; vit DANS le chiffré.
; L'ORDRE NOMMÉ (Q1) : le nonce consommé EST la séquence courante, PUIS
; la séquence du contexte est INCRÉMENTÉE — l'incrémentation SUIT le
; scellement, UN ÉCHEC N'AVANCE JAMAIS LA SÉQUENCE (le -3 propagé ne
; bouge rien : l'en-tête reste LOCALE, la sortie demeure VIERGE — le
; fail-closed de la famille : le refus n'écrit RIEN).
; LE CADRE NOMMÉ (0x4078) : l'ombre de l'appelé [rsp+0x00..0x20), les
; QUATRE args de pile de tls13-18 [rsp+0x20..0x40 : l'AAD, 5, le chiffré,
; l'étiquette], le nonce local [rsp+0x40..0x4C), l'en-tête LOCALE
; [rsp+0x50..0x55) — le fail-closed l'exige : copiée à la sortie APRÈS le
; succès seulement, la sortie P5 [rsp+0x58] et le contexte [rsp+0x60]
; SAUVÉS (rax/rcx volatiles à l'appel), le texte interne [rsp+0x68..0x4069)
; — la charge recopiée PUIS le type au DERNIER octet (I1) ; la pile du
; domaine dimensionnée par l'appelant (jusqu'à 2^14+1 : le sous-cadre
; est NOMMÉ) ; l'entrée ≡ 8 → 8−0x4078 ≡ 0 (mod 16) à l'appel.
; LE VERDICT -3 NOMMÉ (Q3) : le verdict PROPAGÉ de tls13-18 — N = 2^14
; (LA borne P4 de la charge) porte le texte interne à 2^14+1, HORS la
; borne de la brique (N ≤ 2^14) : le maximal du protocole est REFUSÉ par
; la composition, la fragmentation est à l'APPELANT (RFC 8446 § 5.1 —
; l'émission effective est bornée à 2^14−1, la brique fait foi).
; rcx = le contexte (200 o : clés de tour @+0 [176], IV @+176 [12],
; réserve @+188 [4], séquence u64 @+192 [8] — la disposition DÉCLARÉE
; par la spec, le contexte POSÉ par tls13-24 au geste qui l'a dérivé) ·
; rdx = le type de contenu RÉEL (1 o : 22 poignée, 21 alerte, 23 données
; — il DEVIENT le dernier octet du texte interne, une VALEUR pas un
; pointeur : AUCUN test de nul) · r8 = la charge (N octets — indifférente
; si N = 0 : le couple longueur/pointeur, jamais le pointeur seul) ·
; r9 = N (0 ≤ N ≤ 2^14 — TLSPlaintext.length, verdict -2 au-delà) ·
; [rsp+0x28] = la sortie (5+N+17 o : l'en-tête puis le chiffré) · Q2 la
; charge INTACTE, le contexte réécrit SUR SA SÉQUENCE SEULE · Q3 rax = 0.
; I1 UNE composition tls13-18 · I2 le nonce : le IV COPIÉ en local, la
; séquence XORée GROS-BOUTISTE sur les octets 4..11 — le contexte
; JAMAIS réécrit sur son IV · I3 le temps constant hérité de 18 (la
; longueur N publique, le contenu jamais) · I4 AUCUNE entrée IAT, AUCUN
; site syscall (charte § 7) ; aucune écriture hors du contexte pointé et
; de la sortie ; aucun registre non volatil détruit ; NOP, 0x90 (charte § 8).
sub rsp, 0x4078
test rcx, rcx
jz .refus_nul
cmp r9, 0x4000
ja .refus_taille
mov rax, qword ptr [rsp + 0x40a0]
test rax, rax
jz .refus_nul
test r9, r9
je .charge_indifferente
test r8, r8
jz .refus_nul
.charge_indifferente:
mov byte ptr [rsp + 0x50], 23
mov byte ptr [rsp + 0x51], 3
mov byte ptr [rsp + 0x52], 3
lea r10, [r9 + 17]
mov byte ptr [rsp + 0x54], r10b
shr r10, 8
mov byte ptr [rsp + 0x53], r10b
mov r11, qword ptr [rcx + 176]
mov qword ptr [rsp + 0x40], r11
mov r11d, dword ptr [rcx + 184]
mov dword ptr [rsp + 0x48], r11d
mov r11, qword ptr [rcx + 192]
bswap r11
xor qword ptr [rsp + 0x44], r11
xor r10d, r10d
.copie:
cmp r10, r9
jae .copie_fin
mov r11, r8
add r11, r10
movzx r11d, byte ptr [r11]
mov byte ptr [rsp + r10 + 0x68], r11b
add r10, 1
jmp .copie
.copie_fin:
mov byte ptr [rsp + r9 + 0x68], dl
mov qword ptr [rsp + 0x58], rax
mov qword ptr [rsp + 0x60], rcx
lea r10, [rsp + 0x50]
mov qword ptr [rsp + 0x20], r10
mov qword ptr [rsp + 0x28], 5
lea r10, [rax + 5]
mov qword ptr [rsp + 0x30], r10
lea r10, [rax + r9 + 6]
mov qword ptr [rsp + 0x38], r10
lea rdx, [rsp + 0x40]
lea r8, [rsp + 0x68]
lea r9, [r9 + 1]
call TLS18
test eax, eax
jnz .refus_propage
mov rcx, qword ptr [rsp + 0x60]
mov r10, qword ptr [rsp + 0x58]
mov al, byte ptr [rsp + 0x50]
mov byte ptr [r10], al
mov al, byte ptr [rsp + 0x51]
mov byte ptr [r10 + 1], al
mov al, byte ptr [rsp + 0x52]
mov byte ptr [r10 + 2], al
mov al, byte ptr [rsp + 0x53]
mov byte ptr [r10 + 3], al
mov al, byte ptr [rsp + 0x54]
mov byte ptr [r10 + 4], al
add qword ptr [rcx + 192], 1
xor eax, eax
add rsp, 0x4078
ret
.refus_propage:
mov rax, -3
add rsp, 0x4078
ret
.refus_nul:
mov rax, -1
add rsp, 0x4078
ret
.refus_taille:
mov rax, -2
add rsp, 0x4078
ret
