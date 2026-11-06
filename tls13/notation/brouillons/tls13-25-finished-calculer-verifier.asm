; tls13-25-finished-calculer-verifier · brouillon étiqueté — spec tls13-25:R1, bloc carte h100025
; LA PREUVE DE POSSESSION DES CLÉS — verify_data = HMAC(clé_Finished, hash
; du transcript) (RFC 8446 § 4.4.4 : le Finished EST le HMAC du transcript —
; la preuve de possession n'est jamais une parole, charte § 4). DEUX modes
; NOMMÉS sur r9 : CALCULER (0 — le nôtre, à émettre : la sortie = le
; verify_data, rax = 0) et VÉRIFIER (1 — celui du serveur, à confronter :
; le REÇU confronté, conforme → 0, divergent → -4 NOMMÉ la cryptographie
; divergente, la session MEURT, charte § 5).
; UNE COMPOSITION (I1) : tls13-05 (l'HMAC — le Finished n'est RIEN d'autre)
; — la clé (32 o) devient la clé HMAC telle quelle, le hash (32 o) le
; message, la sortie (32 o) le verify_data.
; LE MODE VÉRIFIER (Q2) : le reçu CONFRONTÉ par OU cumulatif des 32
; différences — QUATRE quads accumulés en UN seul registre, LE test À LA
; FIN (le miroir exact de la discipline du verdict AEAD tls13-19 : AUCUN
; court-circuit — la comparaison d'un secret ne s'arrête JAMAIS au premier
; octet différent) ; le reçu n'est JAMAIS modifié (le condensé calculé vit
; en pile, le reçu lu tel quel) ; divergent → rax = -4 NOMMÉ.
; Le mode est une donnée PUBLIQUE de contrôle (I2 — le branch sur r9 est
; licite : les branches de CONTRÔLE sur des arguments publics ne sont pas
; des branches de donnée secrète, la charte § 3 nomme la frontière).
; LE CADRE NOMMÉ (0x68) : l'ombre [rsp+0x00..0x20), le 5e arg de 05 (la
; sortie) @ +0x20, la clé sauvée @ +0x28, le hash sauvé @ +0x30, le reçu
; sauvé @ +0x38, le condensé calculé (32 o) @ +0x40, le mode sauvé @ +0x60
; (r9 est VOLATIL à l'appel — le mode survit en pile) ; l'entrée ≡ 8 →
; 8−0x68 ≡ 0 (mod 16) à l'appel.
; rcx = la clé Finished (32 o — l'étage 2 de tls13-24, la DIRECTION
; correspond à l'ÉMETTEUR du message) · rdx = le hash du transcript (32 o —
; au point de coupe NOMMÉ : serveur CH..Certificate/CertificateVerify,
; client CH..le Finished serveur) · r8 = le pointeur 32 o (CALCULER : la
; SORTIE ; VÉRIFIER : le REÇU) · r9 = le mode (0/1, toute autre valeur →
; -1) · Q3 la clé et le hash INTACTS · I3 AUCUNE entrée IAT, AUCUN site
; syscall (charte § 7) ; aucun état détenu (§ 6) ; aucun registre non
; volatil détruit ; NOP, 0x90 (charte § 8).
sub rsp, 0x68
test rcx, rcx
jz .refus_nul
test rdx, rdx
jz .refus_nul
test r8, r8
jz .refus_nul
cmp r9, 1
ja .refus_mode
mov qword ptr [rsp + 0x28], rcx
mov qword ptr [rsp + 0x30], rdx
mov qword ptr [rsp + 0x38], r8
mov qword ptr [rsp + 0x60], r9
; la sortie de l'HMAC : mode CALCULER → le pointeur de l'appelant ; mode
; VÉRIFIER → le condensé LOCAL (le reçu n'est JAMAIS modifié — Q2)
cmp r9, 1
je .mode_verifier
mov qword ptr [rsp + 0x20], r8
jmp .hmac
.mode_verifier:
lea r10, [rsp + 0x40]
mov qword ptr [rsp + 0x20], r10
.hmac:
mov rcx, qword ptr [rsp + 0x28]
mov edx, 32
mov r8, qword ptr [rsp + 0x30]
mov r9d, 32
call TLS05
test eax, eax
jnz .refus_propage
cmp qword ptr [rsp + 0x60], 1
je .verifier
jmp .fin_calculer
.verifier:
; LE VERDICT : le OU cumulatif des QUATRE quads, le test À LA FIN
mov r8, qword ptr [rsp + 0x38]
xor r10d, r10d
mov r11, qword ptr [r8]
xor r11, qword ptr [rsp + 0x40]
or r10, r11
mov r11, qword ptr [r8 + 8]
xor r11, qword ptr [rsp + 0x48]
or r10, r11
mov r11, qword ptr [r8 + 16]
xor r11, qword ptr [rsp + 0x50]
or r10, r11
mov r11, qword ptr [r8 + 24]
xor r11, qword ptr [rsp + 0x58]
or r10, r11
test r10, r10
jz .conforme
mov rax, -4
add rsp, 0x68
ret
.conforme:
xor eax, eax
add rsp, 0x68
ret
.fin_calculer:
xor eax, eax
add rsp, 0x68
ret
.refus_propage:
add rsp, 0x68
ret
.refus_nul:
mov rax, -1
add rsp, 0x68
ret
.refus_mode:
mov rax, -1
add rsp, 0x68
ret
