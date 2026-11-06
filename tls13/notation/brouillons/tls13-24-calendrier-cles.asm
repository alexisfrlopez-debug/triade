; tls13-24-calendrier-cles · brouillon étiqueté — spec tls13-24:R1, bloc carte h100024
; LA MACHINE À DÉRIVER DE LA RFC 8446 § 7.1 — le calendrier à TROIS étages
; (early → handshake → application), chaque étage AVANCÉ PAR UN APPEL : le
; contexte porte le secret courant et L'ÉTAPE (une machine dérivée, charte
; § 6 : l'état est un ARGUMENT pointé, jamais une adresse fixe — l'ordre des
; étages est STRICT, -3 sur tout saut, l'étape 4 n'existe pas : CLOS).
; Chaque étage produit LES CONTEXTES ENREGISTREMENT prêts à l'emploi (clés
; de tour par tls13-15, IV, séquence zéro — les contextes sortis COMPLETS,
; I2 : aucun champ non posé, le récepteur n'initialise rien) et les clés
; Finished — les sorties de la poignée.
; LE CONTEXTE DE « derived » (l'erratum n° 2 sur pièces) : le contexte de
; l'étiquette est le hash du TRANSCRIPT VIDE — Derive-Secret(., "derived",
; "") de la § 7.1 : Hash("") (32 o), l'info imprimée par le RFC 8448 § 3
; fait 49 o, JAMAIS un contexte de zéro octet — le condensé du vide DÉRIVÉ
; PAR LES BRIQUES MÊMES (tls13-01 + tls13-04 au geste, le juge est le
; code) ; les libellés vivent aux fixtures R_LIB_* du plan (I1 : des
; DONNÉES PUBLIQUES, jamais des octets de code).
; L'ÉTAGE 1 (Q1, l'étape doit être 0 — sinon -3 : la machine refuse de
; sauter) : early_secret = Extract(zéros32, zéros32) — la PSK est HORS
; PÉRIMÈTRE (pas de reprise de session au jalon, l'IKM du premier extrait
; est LES ZÉROS, la voie « 0 » du diagramme § 7.1 — chantier futur nommé) ;
; derived_1 = Expand-Label(early, « derived », Hash(vide), 32) ; le
; contexte porte (derived_1, étape 1). La sortie RIEN (P3 : r8 ignoré).
; L'ÉTAGE 2 (Q2, l'étape doit être 1) : l'entrée = le secret partagé
; x25519 [32] || le hash du transcript CH..SH [32] (64 o) ;
; handshake_secret = Extract(derived_1, partagé) ; c_hs = EL(handshake,
; « c hs traffic », hash, 32) ; s_hs = EL(handshake, « s hs traffic »,
; hash, 32) ; PAR DIRECTION : la clé write = EL(secret, « key », vide, 16),
; le IV = EL(secret, « iv », vide, 12), la clé Finished = EL(secret,
; « finished », vide, 32) — les contextes POSÉS (émission client @ +0,
; réception serveur @ +200 : rk 176 par tls13-15, IV 12, réserve 4 zéros,
; séquence u64 0), les clés Finished (@ +400 client, @ +432 serveur) ;
; derived_2 = EL(handshake, « derived », Hash(vide), 32) — le contexte
; porte (derived_2, étape 2).
; L'ÉTAGE 3 (Q3, l'étape doit être 2) : l'entrée = le hash du transcript
; CH..Finished serveur [32] ; master = Extract(derived_2, zéros32) ;
; c_ap = EL(master, « c ap traffic », hash, 32) ; s_ap = EL(master,
; « s ap traffic », hash, 32) ; les contextes d'application POSÉS (clé
; write, IV, séquence 0) ; le contexte porte (master, étape 3 — CLOS).
; Q4 LA PREUVE : LE TRANSFERT RFC 8448 — le transcript enregistré documente
; les secrets par étage : chaque étage rejoué sur les hash du RFC en
; ARGUMENTS rend LES secrets consignés (early 33ad0a1c…, derived
; 6f2615a1…/43de77e0…, handshake 1dc826e9…, c_hs b3eddb12…, s_hs
; b67b7d69…, master 18df0684…, c_ap 9e40646c…, s_ap a11af9f0…), les clés
; write/IV == LES QUATRE CHAÎNES du TRANSFERT_8448, octet pour octet (le
; juge est le code).
; I1 les compositions DÉCLARÉES : tls13-06 (l'extrait — UN par étage),
; tls13-08 (l'étiquette — TOUTES les clés), tls13-15 (le déploiement des
; clés de tour), tls13-01 + tls13-04 (le condensé du vide) ; le calendrier
; ne hache RIEN : le hash du transcript est un ARGUMENT (le principal
; tient le contexte SHA — tls13-27 I3).
; I3 le temps constant : les secrets sont des DONNÉES SECRÈTES (charte
; § 3) — la propriété hérite de tls13-05..08, le calendrier n'ajoute
; AUCUNE branche sur le contenu (l'étape est une donnée publique de
; contrôle).
; LE CADRE NOMMÉ (0x188) : l'ombre [rsp+0x00..0x20), les TROIS args de
; pile de tls13-08 @ +0x20..0x38, les 32 zéros @ +0x40 (le sel/IKM du vide
; ET le contexte vide des libellés « key »/« iv »/« finished »), early
; @ +0x60, le secret d'étage (handshake/master) @ +0x80, le secret de
; direction @ +0xa0, la clé write @ +0xc0, le IV @ +0xd0, le contexte SHA
; du vide (112 o) @ +0xe0, le hash du vide @ +0x150, l'entrée rdx sauvée
; @ +0x170, le contexte rcx sauvé @ +0x178, la sortie r8 sauvée @ +0x180 ;
; l'entrée ≡ 8 → 8−0x188 ≡ 0 (mod 16) aux appels.
; rcx = le contexte calendrier (48 o : secret courant 32 @ +0, étape u32
; @ +32, réserve @ +36) · rdx = l'ENTRÉE de l'étage · r8 = la SORTIE ·
; I4 AUCUNE entrée IAT, AUCUN site syscall (charte § 7) ; aucun état détenu
; hors du contexte pointé (§ 6) ; aucun registre non volatil détruit ;
; NOP, 0x90 (charte § 8).
sub rsp, 0x188
test rcx, rcx
jz .refus_nul
mov qword ptr [rsp + 0x170], rdx
mov qword ptr [rsp + 0x178], rcx
mov qword ptr [rsp + 0x180], r8
; les 32 zéros du vide (la voie « 0 » du diagramme § 7.1)
mov qword ptr [rsp + 0x40], 0
mov qword ptr [rsp + 0x48], 0
mov qword ptr [rsp + 0x50], 0
mov qword ptr [rsp + 0x58], 0
; LE CONDENSÉ DU VIDE dérivé par les briques mêmes (l'erratum n° 2 : le
; contexte de « derived » = Hash(""), 32 o — JAMAIS zéro octet)
lea rcx, [rsp + 0xe0]
call TLS01
test eax, eax
jnz .refus_propage
lea rcx, [rsp + 0xe0]
lea rdx, [rsp + 0x150]
call TLS04
test eax, eax
jnz .refus_propage
; LE DISPATCH : l'étape u32 @ +32 du contexte (la machine ne saute JAMAIS)
mov r10, qword ptr [rsp + 0x178]
mov r10d, dword ptr [r10 + 32]
cmp r10d, 0
je .etage1
cmp r10d, 1
je .etage2
cmp r10d, 2
je .etage3
jmp .refus_etat
; ---------------------------------------------------------------- étage 1
.etage1:
; early_secret = Extract(zéros32, zéros32)
lea rcx, [rsp + 0x40]
mov edx, 32
lea r8, [rsp + 0x40]
mov r9d, 32
lea r10, [rsp + 0x60]
mov qword ptr [rsp + 0x20], r10
call TLS06
test eax, eax
jnz .refus_propage
; derived_1 = EL(early, « derived », Hash(vide), 32)
lea rcx, [rsp + 0x60]
lea rdx, [rip + LIB_DERIVED]
mov r8d, 7
lea r9, [rsp + 0x150]
mov qword ptr [rsp + 0x20], 32
mov qword ptr [rsp + 0x28], 32
lea r10, [rsp + 0xa0]
mov qword ptr [rsp + 0x30], r10
call TLS08
test eax, eax
jnz .refus_propage
; le contexte porte (derived_1, étape 1)
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
; ---------------------------------------------------------------- étage 2
.etage2:
cmp qword ptr [rsp + 0x180], 0
je .refus_nul
; handshake_secret = Extract(derived_1, le secret partagé)
mov rcx, qword ptr [rsp + 0x178]
mov edx, 32
mov r8, qword ptr [rsp + 0x170]
mov r9d, 32
lea r10, [rsp + 0x80]
mov qword ptr [rsp + 0x20], r10
call TLS06
test eax, eax
jnz .refus_propage
; --- la direction CLIENT : c_hs → le contexte @ sortie+0, la clé Fin @ +400
lea rcx, [rsp + 0x80]
lea rdx, [rip + LIB_C_HS]
mov r8d, 12
mov r9, qword ptr [rsp + 0x170]
add r9, 32
mov qword ptr [rsp + 0x20], 32
mov qword ptr [rsp + 0x28], 32
lea r10, [rsp + 0xa0]
mov qword ptr [rsp + 0x30], r10
call TLS08
test eax, eax
jnz .refus_propage
lea rcx, [rsp + 0xa0]
lea rdx, [rip + LIB_KEY]
mov r8d, 3
lea r9, [rsp + 0x40]
mov qword ptr [rsp + 0x20], 0
mov qword ptr [rsp + 0x28], 16
lea r10, [rsp + 0xc0]
mov qword ptr [rsp + 0x30], r10
call TLS08
test eax, eax
jnz .refus_propage
lea rcx, [rsp + 0xc0]
mov rdx, qword ptr [rsp + 0x180]
call TLS15
test eax, eax
jnz .refus_propage
lea rcx, [rsp + 0xa0]
lea rdx, [rip + LIB_IV]
mov r8d, 2
lea r9, [rsp + 0x40]
mov qword ptr [rsp + 0x20], 0
mov qword ptr [rsp + 0x28], 12
lea r10, [rsp + 0xd0]
mov qword ptr [rsp + 0x30], r10
call TLS08
test eax, eax
jnz .refus_propage
mov r10, qword ptr [rsp + 0x180]
mov r11, qword ptr [rsp + 0xd0]
mov qword ptr [r10 + 176], r11
mov r11d, dword ptr [rsp + 0xd8]
mov dword ptr [r10 + 184], r11d
mov dword ptr [r10 + 188], 0
mov qword ptr [r10 + 192], 0
lea rcx, [rsp + 0xa0]
lea rdx, [rip + LIB_FINISHED]
mov r8d, 8
lea r9, [rsp + 0x40]
mov qword ptr [rsp + 0x20], 0
mov qword ptr [rsp + 0x28], 32
mov r10, qword ptr [rsp + 0x180]
add r10, 400
mov qword ptr [rsp + 0x30], r10
call TLS08
test eax, eax
jnz .refus_propage
; --- la direction SERVEUR : s_hs → le contexte @ sortie+200, la clé Fin @ +432
lea rcx, [rsp + 0x80]
lea rdx, [rip + LIB_S_HS]
mov r8d, 12
mov r9, qword ptr [rsp + 0x170]
add r9, 32
mov qword ptr [rsp + 0x20], 32
mov qword ptr [rsp + 0x28], 32
lea r10, [rsp + 0xa0]
mov qword ptr [rsp + 0x30], r10
call TLS08
test eax, eax
jnz .refus_propage
lea rcx, [rsp + 0xa0]
lea rdx, [rip + LIB_KEY]
mov r8d, 3
lea r9, [rsp + 0x40]
mov qword ptr [rsp + 0x20], 0
mov qword ptr [rsp + 0x28], 16
lea r10, [rsp + 0xc0]
mov qword ptr [rsp + 0x30], r10
call TLS08
test eax, eax
jnz .refus_propage
lea rcx, [rsp + 0xc0]
mov rdx, qword ptr [rsp + 0x180]
add rdx, 200
call TLS15
test eax, eax
jnz .refus_propage
lea rcx, [rsp + 0xa0]
lea rdx, [rip + LIB_IV]
mov r8d, 2
lea r9, [rsp + 0x40]
mov qword ptr [rsp + 0x20], 0
mov qword ptr [rsp + 0x28], 12
lea r10, [rsp + 0xd0]
mov qword ptr [rsp + 0x30], r10
call TLS08
test eax, eax
jnz .refus_propage
mov r10, qword ptr [rsp + 0x180]
mov r11, qword ptr [rsp + 0xd0]
mov qword ptr [r10 + 376], r11
mov r11d, dword ptr [rsp + 0xd8]
mov dword ptr [r10 + 384], r11d
mov dword ptr [r10 + 388], 0
mov qword ptr [r10 + 392], 0
lea rcx, [rsp + 0xa0]
lea rdx, [rip + LIB_FINISHED]
mov r8d, 8
lea r9, [rsp + 0x40]
mov qword ptr [rsp + 0x20], 0
mov qword ptr [rsp + 0x28], 32
mov r10, qword ptr [rsp + 0x180]
add r10, 432
mov qword ptr [rsp + 0x30], r10
call TLS08
test eax, eax
jnz .refus_propage
; derived_2 = EL(handshake, « derived », Hash(vide), 32)
lea rcx, [rsp + 0x80]
lea rdx, [rip + LIB_DERIVED]
mov r8d, 7
lea r9, [rsp + 0x150]
mov qword ptr [rsp + 0x20], 32
mov qword ptr [rsp + 0x28], 32
lea r10, [rsp + 0xa0]
mov qword ptr [rsp + 0x30], r10
call TLS08
test eax, eax
jnz .refus_propage
; le contexte porte (derived_2, étape 2)
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
; ---------------------------------------------------------------- étage 3
.etage3:
cmp qword ptr [rsp + 0x180], 0
je .refus_nul
; master = Extract(derived_2, zéros32)
mov rcx, qword ptr [rsp + 0x178]
mov edx, 32
lea r8, [rsp + 0x40]
mov r9d, 32
lea r10, [rsp + 0x80]
mov qword ptr [rsp + 0x20], r10
call TLS06
test eax, eax
jnz .refus_propage
; --- la direction CLIENT : c_ap → le contexte @ sortie+0
lea rcx, [rsp + 0x80]
lea rdx, [rip + LIB_C_AP]
mov r8d, 12
mov r9, qword ptr [rsp + 0x170]
mov qword ptr [rsp + 0x20], 32
mov qword ptr [rsp + 0x28], 32
lea r10, [rsp + 0xa0]
mov qword ptr [rsp + 0x30], r10
call TLS08
test eax, eax
jnz .refus_propage
lea rcx, [rsp + 0xa0]
lea rdx, [rip + LIB_KEY]
mov r8d, 3
lea r9, [rsp + 0x40]
mov qword ptr [rsp + 0x20], 0
mov qword ptr [rsp + 0x28], 16
lea r10, [rsp + 0xc0]
mov qword ptr [rsp + 0x30], r10
call TLS08
test eax, eax
jnz .refus_propage
lea rcx, [rsp + 0xc0]
mov rdx, qword ptr [rsp + 0x180]
call TLS15
test eax, eax
jnz .refus_propage
lea rcx, [rsp + 0xa0]
lea rdx, [rip + LIB_IV]
mov r8d, 2
lea r9, [rsp + 0x40]
mov qword ptr [rsp + 0x20], 0
mov qword ptr [rsp + 0x28], 12
lea r10, [rsp + 0xd0]
mov qword ptr [rsp + 0x30], r10
call TLS08
test eax, eax
jnz .refus_propage
mov r10, qword ptr [rsp + 0x180]
mov r11, qword ptr [rsp + 0xd0]
mov qword ptr [r10 + 176], r11
mov r11d, dword ptr [rsp + 0xd8]
mov dword ptr [r10 + 184], r11d
mov dword ptr [r10 + 188], 0
mov qword ptr [r10 + 192], 0
; --- la direction SERVEUR : s_ap → le contexte @ sortie+200
lea rcx, [rsp + 0x80]
lea rdx, [rip + LIB_S_AP]
mov r8d, 12
mov r9, qword ptr [rsp + 0x170]
mov qword ptr [rsp + 0x20], 32
mov qword ptr [rsp + 0x28], 32
lea r10, [rsp + 0xa0]
mov qword ptr [rsp + 0x30], r10
call TLS08
test eax, eax
jnz .refus_propage
lea rcx, [rsp + 0xa0]
lea rdx, [rip + LIB_KEY]
mov r8d, 3
lea r9, [rsp + 0x40]
mov qword ptr [rsp + 0x20], 0
mov qword ptr [rsp + 0x28], 16
lea r10, [rsp + 0xc0]
mov qword ptr [rsp + 0x30], r10
call TLS08
test eax, eax
jnz .refus_propage
lea rcx, [rsp + 0xc0]
mov rdx, qword ptr [rsp + 0x180]
add rdx, 200
call TLS15
test eax, eax
jnz .refus_propage
lea rcx, [rsp + 0xa0]
lea rdx, [rip + LIB_IV]
mov r8d, 2
lea r9, [rsp + 0x40]
mov qword ptr [rsp + 0x20], 0
mov qword ptr [rsp + 0x28], 12
lea r10, [rsp + 0xd0]
mov qword ptr [rsp + 0x30], r10
call TLS08
test eax, eax
jnz .refus_propage
mov r10, qword ptr [rsp + 0x180]
mov r11, qword ptr [rsp + 0xd0]
mov qword ptr [r10 + 376], r11
mov r11d, dword ptr [rsp + 0xd8]
mov dword ptr [r10 + 384], r11d
mov dword ptr [r10 + 388], 0
mov qword ptr [r10 + 392], 0
; le contexte porte (master, étape 3 — CLOS)
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
; ---------------------------------------------------------------- les refus
.refus_propage:
add rsp, 0x188
ret
.refus_nul:
mov rax, -1
add rsp, 0x188
ret
.refus_etat:
mov rax, -3
add rsp, 0x188
ret
