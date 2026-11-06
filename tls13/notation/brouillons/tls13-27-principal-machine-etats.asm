; tls13-27-principal-machine-etats · brouillon étiqueté — spec tls13-27:R1, bloc carte h100027
; L'ORCHESTRATION — le client TLS 1.3 ENTIER comme machine d'états sur UN
; contexte (17 520 o, la disposition DÉCLARÉE par la spec P1 : le transcript
; [contexte SHA, 112 o] @ +0 ; le calendrier [48 o] @ +112 ; la clé privée
; x25519 [32 o] @ +160 ; la clé publique [32 o] @ +192 ; l'émission POIGNÉE
; [200 o] @ +224 ; la réception POIGNÉE [200 o] @ +424 ; l'émission
; APPLICATION [200 o] @ +624 ; la réception APPLICATION [200 o] @ +824 ; la
; clé Finished client [32 o] @ +1024 ; la clé Finished serveur [32 o] @
; +1056 ; l'empreinte attendue [32 o] @ +1088 ; l'état u32 @ +1120 ; le
; remplissage de réassemblage u32 @ +1124 ; le pointeur socle u64 @ +1128 ;
; le tampon de réassemblage [2^14 o] @ +1136).
; LA TABLE DES ÉVÉNEMENTS (Q1 — les états : 0 VIERGE, 1 CH ÉMIS, 2 POIGNÉE
; ÉTABLIE [des points de contrôle internes], 3 CONNECTÉ, 4 CLOS, 5 MORT ;
; tout événement hors de sa ligne : verdict -3 NOMMÉ, la machine ne devine
; JAMAIS l'intention de l'appelant) :
;   É1 OUVRIR (r8 = le pointeur socle, r9 = le pointeur des 96 o : aléa 32
;      + clé privée 32 + empreinte 32 — le kit fournit TOUT) : le couple
;      x25519 (tls13-14), le calendrier ÉTAGE 1 (tls13-24 — l'étape 0 →
;      early/derived, la machine dérivée AVANT l'offre : le calendrier est
;      la fondation), le CH composé (tls13-22) et ABSORBÉ (charte § 4 : le
;      transcript AVANT tout — l'ordre d'émission), l'enregistrement en
;      clair cadrée (5 o : type 22, 0x0303, 114 — l'en-tête de L'OFFRE DU
;      JALON, erratum n° 2 : l'émission est NOTRE offre minimale scellée)
;      et ÉMISE au socle ; l'état 1 ; LA BOUCLE DE LECTURE : le ServerHello
;      (l'enregistrement en clair type 22, la lecture bloquante au socle
;      BOUCLE jusqu'à l'enregistrement entier) → tls13-23 (le secret
;      partagé), ABSORBÉ, la copie du transcript finalisée (I2 : la COPIE,
;      l'original continue de vivre — RFC 8446 § 7.1 exige le hash COURANT)
;      → l'étage 2 du calendrier (les contextes POIGNÉE et les clés
;      Finished posés au contexte session) ; l'état 2 ; les enregistrements
;      PROTÉGÉS (tls13-21, réception POIGNÉE) : la charge DÉPOSÉE au tampon
;      de réassemblage @ +1136 + remplissage (la borne NOMMÉE : un message
;      de poignée reçu > 2^14 est le verdict -2), LA MARCHE DES MESSAGES
;      INTERNES : chaque message complet ABSORBÉ AVANT tout traitement
;      (charte § 4) ; au Certificate (0x0b) : l'extraction de la PREMIÈRE
;      entrée de la certificate_list (le u24 lu — le DÉTROIT nommé de
;      tls13-26) puis l'ÉPINGLAGE (tls13-26, l'empreinte @ +1088) ; le
;      CertificateVerify (0x0f) ABSORBÉ sans vérification cryptographique
;      (le chantier futur nommé de tls13-26 : la confiance a tranché à
;      l'épinglage — le domaine le NOMME, il ne le cache pas) ; au Finished
;      serveur (0x14) : LA COUPE du hash AVANT l'absorption (le point de
;      coupe NOMMÉ § 4.4.4 : CH..Certificate/CertificateVerify — la copie
;      finalisée, PUIS le message absorbé), tls13-25 VÉRIFIER (la clé
;      Finished serveur @ +1056, mode 1), l'étage 3 du calendrier (les
;      contextes APPLICATION @ +624), PUIS le Finished client CALCULÉ
;      (tls13-25, la clé @ +1024, mode 0, sur le transcript clos), le
;      message composé (14 00 00 20 || verify_data) et ABSORBÉ, scellé
;      (tls13-20, émission POIGNÉE @ +224, type interne 22) et ÉMIS —
;      L'ÉTAT 3 (CONNECTÉ), rax = 0 ;
;   É2 ÉMETTRE (r8 = la charge, r9 = N ≤ 2^14 — les gardes de tls13-20
;      propagées nommées) : tls13-20 (émission APPLICATION @ +624, type
;      23), l'enregistrement ÉMISE au socle ; rax = 0 ;
;   É3 RECEVOIR (r8 = le tampon, r9 = la capacité — elle DOIT couvrir
;      l'enregistrement entier [5 + L ≤ 5 + 2^14 + 17] : la machine lit
;      l'enregistrement DANS le tampon de l'appelant puis restitue la
;      charge AU DÉBUT du même tampon — la restitution n'a lieu qu'après
;      le déverrouillage, l'écrasement est licite et NOMMÉ) : tls13-21
;      (réception APPLICATION @ +824) ; un type interne 21 : si
;      close_notify (01 00) → l'état 4, rax = 0 (la fin PROPRE, la charge
;      vide) ; une autre alerne → l'état 5, rax = -3 NOMMÉ (le couple
;      niveau/description laissé au tampon pour le témoin du kit :
;      l'information CONSIGNÉE, jamais muette) ; un type interne 22/23 :
;      la charge restituée, rax = la LONGUEUR rendue ; un type inconnu :
;      l'état 5, rax = -3 ;
;   É4 FERMER (états 3 ou 4) : le close_notify composé (2 o : 01 00 — RFC
;      8446 § 6.1), scellé (tls13-20, émission APPLICATION, type interne
;      21) et ÉMIS ; l'état 4 ; rax = 0.
; LA DISCIPLINE D'ÉCHEC (Q2) : tout verdict négatif des briques est
; PROPAGÉ NOMMÉ (-4/-5/-6/-7 tels quels, les -1/-2/-3 des gardes aussi) ;
; l'état passe à 5 (MORT) et AUCUN octet applicatif n'est jamais rendu
; après (tout événement sur l'état 5 : -3) ; le close_notify de É4
; n'est atteint que sur le chemin propre — un échec n'ÉMET RIEN (le
; protocole N'EXIGE rien d'un client qui vient de constater l'échec).
; Les compositions DÉCLARÉES (I1 — LA LISTE EST FERMÉE) : tls13-14, 22,
; 23, 24 (×3 étages), 25 (×2 modes), 26, 20 (×2), 21 (×2), 03 (le
; transcript), 04 (les coupes du hash sur la COPIE) et LE SOCLE tls13-28
; pour TOUTE entrée/sortie — la machine n'appelle rien d'autre : AUCUNE
; entrée IAT, AUCUN site syscall (charte § 7 — l'oracle structurel le
; constatera sur LE PLUS GRAND bloc comme sur la plus petite brique).
; I3 le temps constant : les branches de la machine portent sur l'ÉTAT et
; les LONGUEURS (publiques) ; les secrets ne traversent que les briques
; qui les protègent (charte § 3 héritée par composition).
; LE CADRE NOMMÉ (0x43C8) : l'ombre [rsp+0x00..0x20), l'arg de pile des
; appelés @ +0x20, le contexte session sauvé @ +0x28, got @ +0x40,
; remplissage @ +0x48, marche @ +0x50, le total 5+L @ +0x58, le type
; interne @ +0x60, le type de message @ +0x68, la longueur de message @
; +0x70, l'arg d'événement sauvé @ +0x78, LE TAMPON D'ENREGISTREMENT
; [16 416 o = 5 + 2^14 + 16] @ +0x80, l'entrée d'étage 2 (64) @ +0x40A0,
; la sortie d'étage 2 (464) @ +0x40E0, la copie du transcript (112) @
; +0x42B0, le hash de coupe CH..CV (32) @ +0x4320, le hash clos CH..FinS
; (32) @ +0x4340, le verify_data client (32) @ +0x4360, le message
; Finished (36+) / close_notify et son scellé (64) @ +0x4380 ; l'entrée
; ≡ 8 → 8−0x43C8 ≡ 0 (mod 16) à CHAQUE appel — la zone morte profonde du
; harnais vivra sous le cadre (0x43C8 + 0x4078 des briques imbriquées).
; rcx = le contexte session (17 520 o) · rdx = l'ÉVÉNEMENT · r8 =
; l'argument (pointeur) · r9 = sa longueur (ou la capacité) · I4 AUCUN
; état détenu hors du contexte pointé (charte § 6) ; aucun registre non
; volatil détruit ; NOP, 0x90 (charte § 8).
test rcx, rcx
jz .refus_contexte_nul
cmp rdx, 1
je .ouvrir_ligne
cmp rdx, 2
je .emettre_ligne
cmp rdx, 3
je .recevoir_ligne
cmp rdx, 4
je .fermer_ligne
jmp .refus_pre_etat
; ------------------------------------------------------------------ OUVRIR
.ouvrir_ligne:
cmp dword ptr [rcx + 1120], 0
jne .refus_pre_etat
test r8, r8
jz .refus_pre_nul
test r9, r9
jz .refus_pre_nul
sub rsp, 0x43c8
mov qword ptr [rsp + 0x28], rcx
mov qword ptr [rsp + 0x38], r9
; le pointeur socle posé au contexte (@ +1128) : TOUTE entrée/sortie passe par lui
mov qword ptr [rcx + 1128], r8
; LE TRANSCRIPT INITIALISÉ (tls13-01 — la session naît VIERGE : le contexte
; SHA posé des H0, le hachage partira de l'état initial ; l'absorption suit
; dans l'ordre D'ÉMISSION — charte § 4 ; l'init est le geste de la machine :
; le kit fournit le CSPRG, le couple et la confiance, JAMAIS le transcript)
mov rcx, qword ptr [rsp + 0x28]
call TLS01
test eax, eax
jnz .mort
; l'empreinte attendue : kit+64 → contexte+1088 (la donnée de confiance du kit)
; la clé privée x25519 : kit+32 → contexte+160 (la disposition de la spec P1)
lea r10, [r9 + 32]
lea r11, [rcx + 160]
mov rax, qword ptr [r10]
mov qword ptr [r11], rax
mov rax, qword ptr [r10 + 8]
mov qword ptr [r11 + 8], rax
mov rax, qword ptr [r10 + 16]
mov qword ptr [r11 + 16], rax
mov rax, qword ptr [r10 + 24]
mov qword ptr [r11 + 24], rax
lea r10, [r9 + 64]
lea r11, [rcx + 1088]
mov rax, qword ptr [r10]
mov qword ptr [r11], rax
mov rax, qword ptr [r10 + 8]
mov qword ptr [r11 + 8], rax
mov rax, qword ptr [r10 + 16]
mov qword ptr [r11 + 16], rax
mov rax, qword ptr [r10 + 24]
mov qword ptr [r11 + 24], rax
; le calendrier ÉTAGE 1 : l'étape 0 → early/derived (la fondation AVANT l'offre)
mov rcx, qword ptr [rsp + 0x28]
add rcx, 112
xor edx, edx
xor r8d, r8d
call TLS24
test eax, eax
jnz .mort
; LE COUPLE x25519 : tls13-14(sortie = clé publique @ +192, privée du kit
; sauvé — r9 est VOLATIL, l'appel à tls13-24 l'a clobberé : LA FAUTE du
; premier jet, nommée par le crash)
mov rcx, qword ptr [rsp + 0x28]
add rcx, 192
mov rdx, qword ptr [rsp + 0x38]
add rdx, 32
call TLS14
test eax, eax
jnz .mort
; LE CH COMPOSÉ : tls13-22(aléa du kit sauvé, clé publique, tampon+5, 114)
mov rcx, qword ptr [rsp + 0x38]
mov rdx, qword ptr [rsp + 0x28]
add rdx, 192
lea r8, [rsp + 0x80]
add r8, 5
mov r9d, 114
call TLS22
test eax, eax
jnz .mort
; l'en-tête en clair : type 22, version héritage 0x0303, longueur 114
; (5 o : 16 03 03 00 76 — l'u16 GROS-BOUTISTE)
lea r10, [rsp + 0x80]
mov dword ptr [r10], 0x30316
mov byte ptr [r10 + 4], 0x76
; le CH ABSORBÉ (l'ordre d'émission — charte § 4)
mov rcx, qword ptr [rsp + 0x28]
lea rdx, [rsp + 0x85]
mov r8d, 114
call TLS03
test eax, eax
jnz .mort
; ÉMIS au socle (119 o : 5 + 114)
mov rcx, qword ptr [rsp + 0x28]
mov rcx, qword ptr [rcx + 1128]
mov edx, 1
lea r8, [rsp + 0x80]
mov r9d, 119
call TLS28
test eax, eax
jnz .mort
; l'état 1 (CH ÉMIS — un point de contrôle interne)
mov r10, qword ptr [rsp + 0x28]
mov dword ptr [r10 + 1120], 1
; LA BOUCLE DE LECTURE — le ServerHello (en clair type 22)
mov qword ptr [rsp + 0x40], 0
.sh_tete:
mov rax, qword ptr [rsp + 0x40]
cmp rax, 5
jae .sh_tete_fin
mov rcx, qword ptr [rsp + 0x28]
mov rcx, qword ptr [rcx + 1128]
mov edx, 2
lea r8, [rsp + 0x80]
add r8, qword ptr [rsp + 0x40]
mov r9, 5
sub r9, qword ptr [rsp + 0x40]
call TLS28
test eax, eax
jle .mort
add qword ptr [rsp + 0x40], rax
jmp .sh_tete
.sh_tete_fin:
lea r10, [rsp + 0x80]
cmp byte ptr [r10], 22
jne .refus_etat_mort
movzx eax, word ptr [r10 + 3]
xchg al, ah
cmp rax, 16400
ja .refus_taille_mort
lea rax, [rax + 5]
mov qword ptr [rsp + 0x58], rax
.sh_corps:
mov rax, qword ptr [rsp + 0x40]
cmp rax, qword ptr [rsp + 0x58]
jae .sh_corps_fin
mov rcx, qword ptr [rsp + 0x28]
mov rcx, qword ptr [rcx + 1128]
mov edx, 2
lea r8, [rsp + 0x80]
add r8, qword ptr [rsp + 0x40]
mov r9, qword ptr [rsp + 0x58]
sub r9, qword ptr [rsp + 0x40]
call TLS28
test eax, eax
jle .mort
add qword ptr [rsp + 0x40], rax
jmp .sh_corps
.sh_corps_fin:
; TLS13-23 : le ServerHello traité → le secret partagé (l'entrée d'étage 2
; @ +0 : le calendrier consommera shared || hash)
mov r8, qword ptr [rsp + 0x28]
add r8, 160
lea rcx, [rsp + 0x80]
add rcx, 5
mov rdx, qword ptr [rsp + 0x58]
sub rdx, 5
lea r9, [rsp + 0x40a0]
call TLS23
test eax, eax
jnz .mort
; le SH ABSORBÉ (le message complet)
mov rcx, qword ptr [rsp + 0x28]
lea rdx, [rsp + 0x85]
mov r8, qword ptr [rsp + 0x58]
sub r8, 5
call TLS03
test eax, eax
jnz .mort
; la COPIE du transcript finalisée → le hash CH..SH (I2 : la copie)
mov rsi, qword ptr [rsp + 0x28]
lea rdi, [rsp + 0x42b0]
mov ecx, 14
cld
rep movsq
lea rcx, [rsp + 0x42b0]
lea rdx, [rsp + 0x40a0]
add rdx, 32
call TLS04
test eax, eax
jnz .mort
; L'ÉTAGE 2 : l'entrée shared || hash (64 o), la sortie (464 o)
mov rcx, qword ptr [rsp + 0x28]
add rcx, 112
lea rdx, [rsp + 0x40a0]
lea r8, [rsp + 0x40e0]
call TLS24
test eax, eax
jnz .mort
; les sorties recopiées au contexte : émission POIGNÉE @ +224 (200 o),
; réception POIGNÉE @ +424 (200 o), clé Finished client @ +1024 (32),
; clé Finished serveur @ +1056 (32) — les contextes sortis COMPLETS
lea rsi, [rsp + 0x40e0]
mov rdi, qword ptr [rsp + 0x28]
add rdi, 224
mov ecx, 25
rep movsq
lea rsi, [rsp + 0x40e0]
add rsi, 200
mov rdi, qword ptr [rsp + 0x28]
add rdi, 424
mov ecx, 25
rep movsq
lea rsi, [rsp + 0x40e0]
add rsi, 400
mov rdi, qword ptr [rsp + 0x28]
add rdi, 1024
mov ecx, 4
rep movsq
lea rsi, [rsp + 0x40e0]
add rsi, 432
mov rdi, qword ptr [rsp + 0x28]
add rdi, 1056
mov ecx, 4
rep movsq
; l'état 2 (POIGNÉE ÉTABLIE)
mov r10, qword ptr [rsp + 0x28]
mov dword ptr [r10 + 1120], 2
; LA BOUCLE PROTÉGÉE — les enregistrements opaques jusqu'au Finished
mov qword ptr [rsp + 0x48], 0
.protege:
mov qword ptr [rsp + 0x40], 0
mov qword ptr [rsp + 0x50], 0
.pr_tete:
mov rax, qword ptr [rsp + 0x40]
cmp rax, 5
jae .pr_tete_fin
mov rcx, qword ptr [rsp + 0x28]
mov rcx, qword ptr [rcx + 1128]
mov edx, 2
lea r8, [rsp + 0x80]
add r8, qword ptr [rsp + 0x40]
mov r9, 5
sub r9, qword ptr [rsp + 0x40]
call TLS28
test eax, eax
jle .mort
add qword ptr [rsp + 0x40], rax
jmp .pr_tete
.pr_tete_fin:
lea r10, [rsp + 0x80]
cmp byte ptr [r10], 23
jne .refus_etat_mort
movzx eax, word ptr [r10 + 3]
xchg al, ah
cmp rax, 16400
ja .refus_taille_mort
lea r11, [rax - 17]
add r11, qword ptr [rsp + 0x48]
cmp r11, 16384
ja .refus_taille_mort
lea rax, [rax + 5]
mov qword ptr [rsp + 0x58], rax
.pr_corps:
mov rax, qword ptr [rsp + 0x40]
cmp rax, qword ptr [rsp + 0x58]
jae .pr_corps_fin
mov rcx, qword ptr [rsp + 0x28]
mov rcx, qword ptr [rcx + 1128]
mov edx, 2
lea r8, [rsp + 0x80]
add r8, qword ptr [rsp + 0x40]
mov r9, qword ptr [rsp + 0x58]
sub r9, qword ptr [rsp + 0x40]
call TLS28
test eax, eax
jle .mort
add qword ptr [rsp + 0x40], rax
jmp .pr_corps
.pr_corps_fin:
; TLS13-21 : déprotéger — la charge DÉPOSÉE au tampon de réassemblage
mov rcx, qword ptr [rsp + 0x28]
add rcx, 424
lea rdx, [rsp + 0x80]
mov r8, qword ptr [rsp + 0x58]
mov r9, qword ptr [rsp + 0x28]
add r9, 1136
add r9, qword ptr [rsp + 0x48]
lea r10, [rsp + 0x60]
mov qword ptr [rsp + 0x20], r10
call TLS21
test eax, eax
jnz .mort
cmp byte ptr [rsp + 0x60], 22
jne .refus_etat_mort
mov rax, qword ptr [rsp + 0x58]
sub rax, 22
add qword ptr [rsp + 0x48], rax
; LA MARCHE DES MESSAGES INTERNES (le réassemblage)
.marche:
mov rax, qword ptr [rsp + 0x48]
sub rax, qword ptr [rsp + 0x50]
cmp rax, 4
jb .protege
mov r10, qword ptr [rsp + 0x28]
add r10, 1136
add r10, qword ptr [rsp + 0x50]
movzx eax, byte ptr [r10 + 1]
shl rax, 16
movzx r11d, byte ptr [r10 + 2]
shl r11, 8
or rax, r11
movzx r11d, byte ptr [r10 + 3]
or rax, r11
mov qword ptr [rsp + 0x70], rax
lea r11, [rax + 4]
mov rcx, qword ptr [rsp + 0x48]
sub rcx, qword ptr [rsp + 0x50]
cmp r11, rcx
ja .protege
movzx r11d, byte ptr [r10]
mov qword ptr [rsp + 0x68], r11
cmp r11d, 0x14
jne .absorbe
; LE FINISHED SERVEUR : LA COUPE du hash AVANT l'absorption (§ 4.4.4 :
; CH..Certificate/CertificateVerify — la copie finalisée d'abord)
mov rsi, qword ptr [rsp + 0x28]
lea rdi, [rsp + 0x42b0]
mov ecx, 14
rep movsq
lea rcx, [rsp + 0x42b0]
lea rdx, [rsp + 0x4320]
call TLS04
test eax, eax
jnz .mort
.absorbe:
; le message ABSORBÉ AVANT tout traitement (charte § 4)
mov rcx, qword ptr [rsp + 0x28]
mov r10, qword ptr [rsp + 0x28]
add r10, 1136
add r10, qword ptr [rsp + 0x50]
mov rdx, r10
mov r8, qword ptr [rsp + 0x70]
add r8, 4
call TLS03
test eax, eax
jnz .mort
; LE DISPATCH du type de message
mov rax, qword ptr [rsp + 0x68]
cmp rax, 0xb
je .cert
cmp rax, 0x14
je .fin_serveur
jmp .marche_avance
.cert:
; l'extraction de la PREMIÈRE entrée : le u24 lu (corps : u8 contexte,
; u24 liste, u24 entrée — le DÉTROIT nommé de tls13-26), la borne d'abord
mov r10, qword ptr [rsp + 0x28]
add r10, 1136
add r10, qword ptr [rsp + 0x50]
movzx eax, byte ptr [r10 + 8]
shl rax, 16
movzx r11d, byte ptr [r10 + 9]
shl r11, 8
or rax, r11
movzx r11d, byte ptr [r10 + 10]
or rax, r11
mov r11, qword ptr [rsp + 0x70]
sub r11, 7
cmp rax, r11
ja .refus_taille_mort
mov rcx, r10
add rcx, 11
mov rdx, rax
mov r8, qword ptr [rsp + 0x28]
add r8, 1088
call TLS26
test eax, eax
jnz .mort
jmp .marche_avance
.fin_serveur:
; la longueur du corps == 32 (le verify_data)
cmp qword ptr [rsp + 0x70], 32
jne .refus_taille_mort
; TLS13-25 VÉRIFIER (clé Finished serveur @ +1056, hash CH..CV, mode 1)
mov rcx, qword ptr [rsp + 0x28]
add rcx, 1056
lea rdx, [rsp + 0x4320]
mov r8, qword ptr [rsp + 0x28]
add r8, 1136
add r8, qword ptr [rsp + 0x50]
add r8, 4
mov r9d, 1
call TLS25
test eax, eax
jnz .mort
; la COPIE finalisée → le hash CH..Fin serveur (le message déjà absorbé)
mov rsi, qword ptr [rsp + 0x28]
lea rdi, [rsp + 0x42b0]
mov ecx, 14
rep movsq
lea rcx, [rsp + 0x42b0]
lea rdx, [rsp + 0x4340]
call TLS04
test eax, eax
jnz .mort
; L'ÉTAGE 3 : les contextes d'APPLICATION posés @ +624
mov rcx, qword ptr [rsp + 0x28]
add rcx, 112
lea rdx, [rsp + 0x4340]
mov r8, qword ptr [rsp + 0x28]
add r8, 624
call TLS24
test eax, eax
jnz .mort
; LE FINISHED CLIENT CALCULÉ (clé @ +1024, hash clos, mode 0)
mov rcx, qword ptr [rsp + 0x28]
add rcx, 1024
lea rdx, [rsp + 0x4340]
lea r8, [rsp + 0x4360]
xor r9d, r9d
call TLS25
test eax, eax
jnz .mort
; le message composé : 14 00 00 20 || verify_data (36 o)
lea r10, [rsp + 0x4380]
mov dword ptr [r10], 0x20000014
mov rax, qword ptr [rsp + 0x4360]
mov qword ptr [r10 + 4], rax
mov rax, qword ptr [rsp + 0x4368]
mov qword ptr [r10 + 12], rax
mov rax, qword ptr [rsp + 0x4370]
mov qword ptr [r10 + 20], rax
mov rax, qword ptr [rsp + 0x4378]
mov qword ptr [r10 + 28], rax
; le message ABSORBÉ
mov rcx, qword ptr [rsp + 0x28]
lea rdx, [rsp + 0x4380]
mov r8d, 36
call TLS03
test eax, eax
jnz .mort
; SCELLÉ (tls13-20, émission POIGNÉE @ +224, type interne 22)
mov rcx, qword ptr [rsp + 0x28]
add rcx, 224
mov edx, 22
lea r8, [rsp + 0x4380]
mov r9d, 36
lea r10, [rsp + 0x80]
mov qword ptr [rsp + 0x20], r10
call TLS20
test eax, eax
jnz .mort
; ÉMIS au socle (58 o)
mov rcx, qword ptr [rsp + 0x28]
mov rcx, qword ptr [rcx + 1128]
mov edx, 1
lea r8, [rsp + 0x80]
mov r9d, 58
call TLS28
test eax, eax
jnz .mort
; L'ÉTAT 3 (CONNECTÉ), rax = 0
mov r10, qword ptr [rsp + 0x28]
mov dword ptr [r10 + 1120], 3
xor eax, eax
add rsp, 0x43c8
ret
.marche_avance:
mov rax, qword ptr [rsp + 0x70]
add rax, 4
add qword ptr [rsp + 0x50], rax
jmp .marche
; ------------------------------------------------------------------ ÉMETTRE
.emettre_ligne:
cmp dword ptr [rcx + 1120], 3
jne .refus_pre_etat
sub rsp, 0x43c8
mov qword ptr [rsp + 0x28], rcx
mov qword ptr [rsp + 0x38], r9
mov qword ptr [rsp + 0x78], r8
mov qword ptr [rsp + 0x40], r9
; tls13-20 (émission APPLICATION @ +624, type 23) — les gardes de 20
; propagées nommées (les pointeurs, N ≤ 2^14, la fragmentation à l'appelant)
mov rcx, qword ptr [rsp + 0x28]
add rcx, 624
mov edx, 23
mov r8, qword ptr [rsp + 0x78]
mov r9, qword ptr [rsp + 0x40]
lea r10, [rsp + 0x80]
mov qword ptr [rsp + 0x20], r10
call TLS20
test eax, eax
jnz .mort
mov rcx, qword ptr [rsp + 0x28]
mov rcx, qword ptr [rcx + 1128]
mov edx, 1
lea r8, [rsp + 0x80]
mov r9, qword ptr [rsp + 0x40]
add r9, 22
call TLS28
test eax, eax
jnz .mort
xor eax, eax
add rsp, 0x43c8
ret
; ------------------------------------------------------------------ RECEVOIR
.recevoir_ligne:
cmp dword ptr [rcx + 1120], 3
jne .refus_pre_etat
test r8, r8
jz .refus_pre_nul
cmp r9, 5
jb .refus_pre_taille
sub rsp, 0x43c8
mov qword ptr [rsp + 0x28], rcx
mov qword ptr [rsp + 0x38], r9
mov qword ptr [rsp + 0x78], r8
mov qword ptr [rsp + 0x40], r9
mov qword ptr [rsp + 0x48], 0
.rc_tete:
mov rax, qword ptr [rsp + 0x48]
cmp rax, 5
jae .rc_tete_fin
mov rcx, qword ptr [rsp + 0x28]
mov rcx, qword ptr [rcx + 1128]
mov edx, 2
mov r8, qword ptr [rsp + 0x78]
add r8, qword ptr [rsp + 0x48]
mov r9, 5
sub r9, qword ptr [rsp + 0x48]
call TLS28
test eax, eax
jle .mort
add qword ptr [rsp + 0x48], rax
jmp .rc_tete
.rc_tete_fin:
mov r10, qword ptr [rsp + 0x78]
movzx eax, word ptr [r10 + 3]
xchg al, ah
lea rax, [rax + 5]
cmp rax, qword ptr [rsp + 0x40]
ja .refus_taille_mort
mov qword ptr [rsp + 0x58], rax
mov qword ptr [rsp + 0x40], 5
.rc_corps:
mov rax, qword ptr [rsp + 0x40]
cmp rax, qword ptr [rsp + 0x58]
jae .rc_corps_fin
mov rcx, qword ptr [rsp + 0x28]
mov rcx, qword ptr [rcx + 1128]
mov edx, 2
mov r8, qword ptr [rsp + 0x78]
add r8, qword ptr [rsp + 0x40]
mov r9, qword ptr [rsp + 0x58]
sub r9, qword ptr [rsp + 0x40]
call TLS28
test eax, eax
jle .mort
add qword ptr [rsp + 0x40], rax
jmp .rc_corps
.rc_corps_fin:
; tls13-21 (réception APPLICATION @ +824) — la charge AU DÉBUT du même
; tampon (l'écrasement NOMMÉ : la restitution n'a lieu qu'après le
; déverrouillage, 21 lit l'enregistrement AVANT d'écrire)
mov rcx, qword ptr [rsp + 0x28]
add rcx, 824
mov rdx, qword ptr [rsp + 0x78]
mov r8, qword ptr [rsp + 0x58]
mov r9, qword ptr [rsp + 0x78]
lea r10, [rsp + 0x60]
mov qword ptr [rsp + 0x20], r10
call TLS21
test eax, eax
jnz .mort
movzx eax, byte ptr [rsp + 0x60]
cmp eax, 21
je .rc_alerte
cmp eax, 22
je .rc_restituer
cmp eax, 23
je .rc_restituer
jmp .refus_etat_mort
.rc_restituer:
mov rax, qword ptr [rsp + 0x58]
sub rax, 22
add rsp, 0x43c8
ret
.rc_alerte:
; si close_notify (01 00 — la charge de 2 o au début du tampon) → l'état 4 ;
; une autre alerne → l'état 5, rax = -3 NOMMÉ (le couple laissé au tampon
; pour le témoin du kit : l'information CONSIGNÉE, jamais muette)
cmp qword ptr [rsp + 0x58], 24
jne .rc_alerte_morte
mov r10, qword ptr [rsp + 0x78]
cmp word ptr [r10], 1
jne .rc_alerte_morte
mov r10, qword ptr [rsp + 0x28]
mov dword ptr [r10 + 1120], 4
xor eax, eax
add rsp, 0x43c8
ret
.rc_alerte_morte:
mov r10, qword ptr [rsp + 0x28]
mov dword ptr [r10 + 1120], 5
mov eax, -3
add rsp, 0x43c8
ret
; ------------------------------------------------------------------ FERMER
.fermer_ligne:
cmp dword ptr [rcx + 1120], 3
je .fermer_ok
cmp dword ptr [rcx + 1120], 4
je .fermer_ok
jmp .refus_pre_etat
.fermer_ok:
sub rsp, 0x43c8
mov qword ptr [rsp + 0x28], rcx
mov qword ptr [rsp + 0x38], r9
; le close_notify composé (2 o : 01 00 — RFC 8446 § 6.1)
lea r10, [rsp + 0x4380]
mov word ptr [r10], 1
; scellé (tls13-20, émission APPLICATION @ +624, type interne 21)
mov rcx, qword ptr [rsp + 0x28]
add rcx, 624
mov edx, 21
lea r8, [rsp + 0x4380]
mov r9d, 2
lea r10, [rsp + 0x80]
mov qword ptr [rsp + 0x20], r10
call TLS20
test eax, eax
jnz .mort
; émis au socle (24 o)
mov rcx, qword ptr [rsp + 0x28]
mov rcx, qword ptr [rcx + 1128]
mov edx, 1
lea r8, [rsp + 0x80]
mov r9d, 24
call TLS28
test eax, eax
jnz .mort
mov r10, qword ptr [rsp + 0x28]
mov dword ptr [r10 + 1120], 4
xor eax, eax
add rsp, 0x43c8
ret
; ------------------------------------------------------------- LES CHEMINS
.mort:
; tout verdict négatif : l'état passe à 5 (MORT), le verdict PROPAGÉ (rax)
mov r10, qword ptr [rsp + 0x28]
mov dword ptr [r10 + 1120], 5
add rsp, 0x43c8
ret
.refus_etat_mort:
mov eax, -3
jmp .mort
.refus_taille_mort:
mov eax, -2
jmp .mort
.refus_pre_etat:
mov dword ptr [rcx + 1120], 5
mov rax, -3
ret
.refus_pre_nul:
mov dword ptr [rcx + 1120], 5
mov rax, -1
ret
.refus_pre_taille:
mov dword ptr [rcx + 1120], 5
mov rax, -2
ret
.refus_contexte_nul:
; le contexte lui-même nul : l'état est inatteignable, le verdict seul rendu
mov rax, -1
ret
