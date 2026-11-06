; tls13-26-epinglage · brouillon étiqueté — spec tls13-26:R1, bloc carte h100026
; LA DÉCISION DE CONFIANCE DU JALON — une COMPARAISON, jamais une croyance :
; le SHA-256 des octets DER du certificat de l'entité, confronté à
; L'EMPREINTE ÉPINGLÉE fournie par l'appelant (la donnée du kit). L'analyse
; X.509 complète (la chaîne, les extensions, la révocation, la vérification
; de signature du CertificateVerify) est un CHANTIER FUTUR NOMMÉ — le jalon
; compare et NOMME la frontière : il ne fait pas confiance en silence.
; Le certificat (le DER) est EXTRAIT par le principal tls13-27 (le DÉTROIT
; est nommé : la lecture du u24 de la première entrée de la certificate_list
; est le geste du principal, jamais de la brique — P1).
; LE CADRE NOMMÉ (0xC8) : l'ombre des appelés [rsp+0x00..0x20), le contexte
; SHA de PILE (112 o) @ +0x20 [I2 : un contexte de PILE local — le bloc ne
; détient RIEN], le condensé (32 o) @ +0x90, le certificat sauvé @ +0xB0,
; N sauvé @ +0xB8, l'empreinte sauvée @ +0xC0 ; l'entrée ≡ 8 → 8−0xC8 ≡ 0
; (mod 16) aux appels.
; LES COMPOSITIONS (I2) : tls13-01 (l'initialisation du contexte de pile),
; tls13-03 (l'absorption du DER — le contexte en premier argument, les
; données en second, N en troisième : l'ABI ah), tls13-04 (la finalisation
; — le condensé GROS-BOUTISTE extrait en pile).
; LA COMPARAISON TEMPS CONSTANT (I1) : le OU cumulatif des 32 différences —
; QUATRE quads accumulés en UN seul registre, LE test À LA FIN (le miroir
; exact de la discipline du verdict AEAD tls13-19 : aucune comparaison ne
; s'arrête au premier octet différent — l'empreinte est une donnée de
; CONFIANCE, la discipline demeure) ; conforme → rax = 0, divergent →
; rax = -6 NOMMÉ (épinglage divergent — la session MEURT sans autres
; formes, charte § 5 : le certificat offert n'est pas celui qu'on attendait).
; rcx = le certificat (les octets DER de l'entité, N o) · rdx = N (1 ≤ N ≤
; 2^61) · r8 = l'empreinte attendue (32 o) · Q2 le certificat et l'empreinte
; INTACTS · I3 AUCUNE entrée IAT, AUCUN site syscall (charte § 7) ; aucun
; état détenu (§ 6) ; aucun registre non volatil détruit ; NOP, 0x90 (§ 8).
sub rsp, 0xc8
test rcx, rcx
jz .refus_nul
test r8, r8
jz .refus_nul
test rdx, rdx
jz .refus_taille
movabs r10, 0x2000000000000000
cmp rdx, r10
ja .refus_taille
mov qword ptr [rsp + 0xb0], rcx
mov qword ptr [rsp + 0xb8], rdx
mov qword ptr [rsp + 0xc0], r8
; le hachage : le contexte de PILE (I2), l'ABI ah (01/03/04)
lea rcx, [rsp + 0x20]
call TLS01
test eax, eax
jnz .refus_propage
lea rcx, [rsp + 0x20]
mov rdx, qword ptr [rsp + 0xb0]
mov r8, qword ptr [rsp + 0xb8]
call TLS03
test eax, eax
jnz .refus_propage
lea rcx, [rsp + 0x20]
lea rdx, [rsp + 0x90]
call TLS04
test eax, eax
jnz .refus_propage
; la comparaison TEMPS CONSTANT : le OU cumulatif des QUATRE quads, le
; test À LA FIN (I1 — aucune comparaison ne s'arrête au premier octet)
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
jz .conforme
mov rax, -6
add rsp, 0xc8
ret
.conforme:
xor eax, eax
add rsp, 0xc8
ret
.refus_propage:
add rsp, 0xc8
ret
.refus_nul:
mov rax, -1
add rsp, 0xc8
ret
.refus_taille:
mov rax, -2
add rsp, 0xc8
ret
