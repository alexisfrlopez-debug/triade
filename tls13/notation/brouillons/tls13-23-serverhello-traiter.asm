; tls13-23-serverhello-traiter · brouillon étiqueté — spec tls13-23:R1, bloc carte h100023
; LE VERDICT SUR LA RÉPONSE — la marche BORNÉE du message (le type de poignée
; 2, la longueur u24, le corps) : chaque champ CONFRONTÉ à l'attendu du
; jalon, chaque divergence un REFUS NOMMÉ (le domaine ne s'adapte JAMAIS en
; silence). L'issue EST le secret partagé : la key_share x25519 du serveur
; croisée avec la clé privée du client par tls13-13.
; L'ERRATUM n° 2 (troisième pièce, sur pièces) : la garde de P2 « ≥ 94 : 4 +
; 90 » compte l'en-tête DEUX FOIS — le ServerHello minimal du RFC 8448 § 3
; fait 90 o (4 + 86 — la construction re-jouée de verifier_specs_m9a § 4 :
; version 2 + aléa 32 + écho 1 + suite 2 [SANS longueur — ServerHello] +
; compression 1 + extensions-len 2 + extensions 46) : la garde est rdx ≥ 90.
; LES CONFRONTATIONS DANS L'ORDRE DU CORPS (Q1, chacune NOMMÉE) : le type
; de poignée == 2 (-1) ; la version héritage == 0x0303 (-1) ; l'aléa != LA
; VALEUR MAGIQUE HelloRetryRequest — la constante du plan au fixture R_HRR,
; la comparaison par OU cumulatif des QUATRE quads, le test À LA FIN (I2 :
; la discipline demeure — même sur un refus nommé) — l'ÉGALER est le -5
; NOMMÉ « HelloRetryRequest : le chantier futur nommé » (RFC 8446 § 4.1.3 :
; la demande de nouvelle offre est un refus propre, jamais une seconde
; offre silencieuse) ; l'écho session_id VIDE (-1) ; LA suite == 0x1301
; (-5 : LA NÉGOCIATION REFUSÉE — le serveur a choisi autre chose, charte
; § 1) ; la compression nulle (-1) ; LA MARCHE DES EXTENSIONS BORNÉE (I1 :
; chaque lecture précédée du contrôle de reste — l'en-tête tronquée → -1,
; le corps tronqué → -1) : supported_versions PRÉSENTE == 0x0304 (-5),
; key_share PRÉSENTE, groupe x25519 0x001d, 32 octets (-5 — une seconde
; key_share → -1), les extensions INCONNUES IGNORÉES (RFC 8446 § 4.1.3 : la
; règle DU PROTOCOLE, pas une tolérance du domaine), l'épuisement exact du
; message (le u24 + 4 == la longueur disponible, -1).
; Q2 : l'issue tls13-13(clé privée, clé publique du serveur) → le secret
; partagé à r9 — APRÈS le dernier refus possible : la clé privée n'est
; JAMAIS touchée sur un message refusé. Q3 le message et la clé privée
; INTACTS ; rax = 0 (ou le verdict NOMMÉ).
; Le message ne TOUCHE PAS au transcript (I3 — le principal absorbe, la
; même séparation que tls13-22).
; LE CADRE NOMMÉ (0x38) : l'ombre des appelés [rsp+0x00..0x20), les
; drapeaux (bit 0 key_share, bit 1 supported_versions) @ +0x20, le pointeur
; de la clé publique du serveur @ +0x28, l'etype sauvegardée @ +0x30 ;
; l'entrée ≡ 8 → 8−0x38 ≡ 0 (mod 16) à l'appel.
; rcx = le message ServerHello (90 o MINIMUM) · rdx = la longueur
; disponible (≥ 90) · r8 = la clé privée x25519 du client (32 o — BRUTE : le
; clamp est l'affaire de tls13-13) · r9 = la sortie : le secret partagé
; (32 o) · I4 AUCUNE entrée IAT, AUCUN site syscall (charte § 7) ; aucun
; état détenu (§ 6) ; aucun registre non volatil détruit ; NOP, 0x90 (§ 8).
sub rsp, 0x38
test rcx, rcx
jz .refus_nul
test r8, r8
jz .refus_nul
test r9, r9
jz .refus_nul
cmp rdx, 90
jb .refus_taille
cmp byte ptr [rcx], 2
jne .refus_type
movzx r10d, byte ptr [rcx + 1]
shl r10d, 16
movzx r11d, byte ptr [rcx + 2]
shl r11d, 8
or r10d, r11d
movzx r11d, byte ptr [rcx + 3]
or r10d, r11d
cmp r10, 86
jb .refus_taille
lea r11, [r10 + 4]
cmp r11, rdx
jne .refus_type
cmp word ptr [rcx + 4], 0x303
jne .refus_type
; l'aléa ≠ la valeur magique HRR (I2 : le OU cumulatif, le test À LA FIN)
lea r11, [rip + HRR]
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
jz .refus_hrr
cmp byte ptr [rcx + 38], 0
jne .refus_type
movzx eax, word ptr [rcx + 39]
xchg al, ah
cmp eax, 0x1301
jne .refus_negociation
cmp byte ptr [rcx + 41], 0
jne .refus_type
; la région déclarée des extensions DOIT épuiser le corps exactement
; (l'u16 GROS-BOUTISTE @ +42 == rdx − 44 : le message doit s'épuiser exactement)
movzx eax, word ptr [rcx + 42]
xchg al, ah
mov r10, rax
mov r11, rdx
sub r11, 44
cmp r10, r11
jne .refus_type
; LA MARCHE DES EXTENSIONS : le curseur r10 @ +44, la fin r11 == rcx + rdx
; (l'épuisement exact déjà confronté), les drapeaux en pile
mov qword ptr [rsp + 0x20], 0
lea r10, [rcx + 44]
lea r11, [rcx + rdx]
.marche:
cmp r10, r11
jae .marche_fin
mov rax, r11
sub rax, r10
cmp rax, 4
jb .refus_type
movzx eax, word ptr [r10]
xchg al, ah
mov qword ptr [rsp + 0x30], rax
movzx eax, word ptr [r10 + 2]
xchg al, ah
mov rcx, r11
sub rcx, r10
sub rcx, 4
cmp rax, rcx
ja .refus_type
cmp qword ptr [rsp + 0x30], 0x33
jne .pas_ks
bt qword ptr [rsp + 0x20], 0
jc .refus_type
cmp rax, 36
jne .refus_negociation
movzx ecx, word ptr [r10 + 4]
xchg cl, ch
cmp ecx, 0x1d
jne .refus_negociation
movzx ecx, word ptr [r10 + 6]
xchg cl, ch
cmp ecx, 0x20
jne .refus_negociation
lea rcx, [r10 + 8]
mov qword ptr [rsp + 0x28], rcx
or qword ptr [rsp + 0x20], 1
jmp .marche_avance
.pas_ks:
cmp qword ptr [rsp + 0x30], 0x2b
jne .marche_avance
bt qword ptr [rsp + 0x20], 1
jc .refus_type
cmp rax, 2
jne .refus_negociation
movzx ecx, word ptr [r10 + 4]
xchg cl, ch
cmp ecx, 0x304
jne .refus_negociation
or qword ptr [rsp + 0x20], 2
.marche_avance:
lea r10, [r10 + rax + 4]
jmp .marche
.marche_fin:
cmp qword ptr [rsp + 0x20], 3
jne .refus_negociation
; Q2 : tls13-13(la clé privée, la clé publique du serveur) — le secret
; partagé à r9, la clé privée n'est JAMAIS touchée avant ce point
mov rcx, r9
mov rdx, r8
mov r8, qword ptr [rsp + 0x28]
call TLS13
add rsp, 0x38
ret
.refus_hrr:
mov rax, -5
add rsp, 0x38
ret
.refus_negociation:
mov rax, -5
add rsp, 0x38
ret
.refus_nul:
mov rax, -1
add rsp, 0x38
ret
.refus_type:
mov rax, -1
add rsp, 0x38
ret
.refus_taille:
mov rax, -2
add rsp, 0x38
ret
