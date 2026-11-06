; tls13-21-enregistrement-deproteger · brouillon étiqueté — spec tls13-21:R1, bloc carte h100021
; LA COUCHE ENREGISTREMENT — DÉPROTÉGER : l'inverse exact (RFC 8446 § 5.2).
; L'en-tête CONFRONTÉE AVANT TOUT (I2 : les verdicts -1/-2 précèdent le -4) :
; le type doit être 23 (le protégé est TOUJOURS opaque — verdict -1 NOMMÉ
; sur divergence), la longueur DÉCLARÉE par l'en-tête == L (verdict -2 :
; l'enregistrement doit s'épuiser exactement, aucun octet traînant), la
; version héritage est IGNORÉE (RFC 8446 § 5.1 : « MUST be ignored for all
; purposes » — la spec ne promet pas ce que le protocole n'exige pas ; les
; octets version reçus restent couverts par l'AAD : la mutation → le -4,
; la cryptographie attrape ce que la logique ignore) ; les bornes
; structurelles (le minimum P2 : L ≥ 18 — au minimum le type interne et
; l'étiquette ; le total ≥ 5+18 ; la borne de la brique : L ≤ 2^14+16) —
; verdict -2 NOMMÉ, la famille de l'épuisement exact.
; L'AAD = l'en-tête REÇUE TELLE QUELLE (RFC 8446 § 5.2 : l'authentification
; couvre les octets REÇUS), le nonce = IV ⊕ séquence (I2 : le IV copié en
; local, la séquence XORée GROS-BOUTISTE sur les octets 4..11 — le
; contexte JAMAIS réécrit sur son IV), tls13-19 rend le verdict.
; LA RESTITUTION EST LA DERNIÈRE OPÉRATION (I2) : le -4 de 19 → rax = -4
; NOMMÉ, la sortie charge et le type demeurent INTACTS (AUCUN octet
; restitué après un échec — charte § 5), la séquence N'EST PAS
; incrémentée (l'échec ne bouge RIEN) ; le succès : la charge (L−17 o)
; copiée du tampon local, le TYPE (le DERNIER octet du texte interne)
; écrit à P5, la séquence INCRÉMENTÉE.
; L'ANTI-REJOUE DU PROTOCOLE (Q5) : une désynchronisation de séquence
; (rejoue, perte) est une étiquette qui ne colle PAS — la cryptographie
; tranche, le bloc n'interroge jamais : un enregistrement consommé
; REJOUÉ → -4 par la séquence avancée.
; LE CADRE NOMMÉ (0x4078) : l'ombre de l'appelé [rsp+0x00..0x20), les
; QUATRE args de pile de tls13-19 [rsp+0x20..0x40 : l'AAD = l'en-tête
; reçue, 5, l'étiquette reçue, le tampon local], le nonce local
; [rsp+0x40..0x4C), l'enregistrement [rsp+0x50], le type P5 [rsp+0x58],
; la charge P4 [rsp+0x60], le contexte [rsp+0x68] SAUVÉS (rdx/rcx/rax/r9
; volatiles à l'appel), le texte interne [rsp+0x70..0x4070) — déverrouillé
; dans le LOCAL puis la charge copiée (le DERNIER octet est le TYPE, la
; sortie P4 n'a que L−17 o : le tampon local est NOMMÉ) ; l'entrée ≡ 8 →
; 8−0x4078 ≡ 0 (mod 16) à l'appel.
; rcx = le contexte (200 o — la même disposition que tls13-20) · rdx =
; l'enregistrement reçu (5+L octets) · r8 = la longueur totale (5+L) ·
; r9 = la sortie charge (L−17 o) · [rsp+0x28] = le type restitué (1 o) ·
; Q4 l'enregistrement reçu INTACT.
; I1 UNE composition tls13-19 · I3 le temps constant hérité (19 compare
; sans court-circuit) · I4 AUCUNE entrée IAT, AUCUN site syscall (charte
; § 7) ; aucune écriture hors du contexte, de la sortie et du type ;
; aucun registre non volatil détruit ; NOP, 0x90 (charte § 8).
sub rsp, 0x4078
test rcx, rcx
jz .refus_nul
test rdx, rdx
jz .refus_nul
test r9, r9
jz .refus_nul
mov rax, qword ptr [rsp + 0x40a0]
test rax, rax
jz .refus_nul
cmp r8, 23
jb .refus_taille
cmp byte ptr [rdx], 23
jne .refus_type
movzx r10d, byte ptr [rdx + 3]
shl r10d, 8
movzx r11d, byte ptr [rdx + 4]
or r10d, r11d
lea r11, [r8 - 5]
cmp r10, r11
jne .refus_taille
cmp r10, 18
jb .refus_taille
cmp r10, 16400
ja .refus_taille
mov r11, qword ptr [rcx + 176]
mov qword ptr [rsp + 0x40], r11
mov r11d, dword ptr [rcx + 184]
mov dword ptr [rsp + 0x48], r11d
mov r11, qword ptr [rcx + 192]
bswap r11
xor qword ptr [rsp + 0x44], r11
mov qword ptr [rsp + 0x50], rdx
mov qword ptr [rsp + 0x58], rax
mov qword ptr [rsp + 0x60], r9
mov qword ptr [rsp + 0x68], rcx
lea r10, [rdx + r8 - 16]
mov qword ptr [rsp + 0x30], r10
lea r10, [rsp + 0x70]
mov qword ptr [rsp + 0x38], r10
lea r9, [r8 - 21]
lea r8, [rdx + 5]
lea rdx, [rsp + 0x40]
mov r10, qword ptr [rsp + 0x50]
mov qword ptr [rsp + 0x20], r10
mov qword ptr [rsp + 0x28], 5
call TLS19
test eax, eax
jnz .refus_divergente
mov r10, qword ptr [rsp + 0x50]
movzx r11d, byte ptr [r10 + 3]
shl r11d, 8
movzx eax, byte ptr [r10 + 4]
or r11d, eax
sub r11d, 16
mov r10, r11
sub r10, 1
mov al, byte ptr [rsp + r10 + 0x70]
mov r10, qword ptr [rsp + 0x58]
mov byte ptr [r10], al
mov r10, qword ptr [rsp + 0x60]
lea r11, [r11 - 1]
xor eax, eax
.copie:
cmp rax, r11
jae .copie_fin
movzx edx, byte ptr [rsp + rax + 0x70]
mov byte ptr [r10 + rax], dl
add rax, 1
jmp .copie
.copie_fin:
mov rcx, qword ptr [rsp + 0x68]
add qword ptr [rcx + 192], 1
xor eax, eax
add rsp, 0x4078
ret
.refus_divergente:
mov rax, -4
add rsp, 0x4078
ret
.refus_nul:
mov rax, -1
add rsp, 0x4078
ret
.refus_type:
mov rax, -1
add rsp, 0x4078
ret
.refus_taille:
mov rax, -2
add rsp, 0x4078
ret
