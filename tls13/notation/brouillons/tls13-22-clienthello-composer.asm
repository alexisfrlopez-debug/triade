; tls13-22-clienthello-composer · brouillon étiqueté — spec tls13-22:R1, bloc carte h100022
; LE PREMIER MESSAGE — l'offre du client en 114 octets FIXES (la longueur est
; une CONSTANTE du plan d'adressage, vérifiée par construction au harnais :
; la construction re-jouée de verifier_specs_m9a § 4, le fixture aléa/clé
; aux offsets déclarés — l'ERRATUM n° 2 de l'arbre I : l'égalité octet pour
; octet AVEC LE ClientHello de 196 o du RFC 8448 § 3 est IMPOSSIBLE PAR
; CONSTRUCTION, le jalon propose l'offre MINIMALE scellée, charte § 1 :
; LA suite seule — le domaine ne propose JAMAIS ce qu'il ne prouve pas).
; LA COMPOSITION PAR OCTETS FIXES (I1) : chaque champ écrit à son offset
; constant, les valeurs protocolaires en IMMÉDIATS DU PLAN (T5 — jamais
; recopiées d'écriture : SUITE 0x1301, GROUPE 0x001d, VERSION_HÉRITAGE
; 0x0303, VERSION_TLS13 0x0304, EXT_SUPPORTED_VERSIONS 0x002b,
; EXT_SUPPORTED_GROUPS 0x000a, EXT_SIG_ALGS 0x000d, EXT_KEY_SHARE 0x0033,
; SIG_ALGOS 0x0804/0x0401 — le harnais V1 recoupe chacun au plan) ;
; l'aléa copié de rcx @ +6..37 (QUATRE quads), la clé publique copiée de
; rdx @ +82..113 (QUATRE quads) — le fixture du RFC 8448 § 3 à leur place.
; AUCUNE branche de données, AUCUNE construction variable (I1) : les QUATRE
; seuls sauts sont les gardes des pointeurs et de la capacité — le message
; est FIXE, il n'y a RIEN à négocier.
; Le message ne TOUCHE PAS au transcript (I2 — le compositeur compose, la
; machine d'états tls13-27 chronique : la séparation est nommée).
; rcx = l'aléa (32 o — la sortie du CSPRG de l'appelant) · rdx = la clé
; publique x25519 (32 o — le produit de tls13-14) · r8 = la sortie (114 o)
; · r9 = la capacité offerte (≥ 114, verdict -2) · Q2 l'aléa et la clé
; INTACTS · Q3 rax = 0 · I4 AUCUNE entrée IAT, AUCUN site syscall (charte
; § 7) ; aucun état détenu (§ 6) ; aucun registre non volatil détruit ;
; NOP, 0x90 (charte § 8).
; Le cadre : AUCUN (bloc feuille — aucun appel, aucune pile locale, l'ombre
; n'est jamais touchée) ; l'entrée ≡ 8 (mod 16) inchangée.
test rcx, rcx
jz .refus_nul
test rdx, rdx
jz .refus_nul
test r8, r8
jz .refus_nul
cmp r9, 114
jb .refus_taille
; l'en-tête de poignée : type 1, longueur u24 = 110 (0x00006e) GROS-BOUTISTE
mov dword ptr [r8], 0x6e000001
; version héritage 0x0303 (le plan : VERSION_HERITAGE)
mov word ptr [r8 + 4], 0x303
; l'aléa @ +6 (QUATRE quads, la source INTACTE — Q2)
mov r10, qword ptr [rcx]
mov qword ptr [r8 + 6], r10
mov r10, qword ptr [rcx + 8]
mov qword ptr [r8 + 14], r10
mov r10, qword ptr [rcx + 16]
mov qword ptr [r8 + 22], r10
mov r10, qword ptr [rcx + 24]
mov qword ptr [r8 + 30], r10
; session_id héritage VIDE @ +38, cipher_suites len 2 @ +39, LA suite 0x1301 @ +41
mov byte ptr [r8 + 38], 0
mov dword ptr [r8 + 39], 0x1130200
; compression len 1 @ +43, méthode nulle @ +44
mov word ptr [r8 + 43], 1
; extensions len 67 @ +45
mov word ptr [r8 + 45], 0x4300
; supported_versions @ +47 : type 0x002b, len 3, liste 2, 0x0304
mov dword ptr [r8 + 47], 0x3002b00
mov byte ptr [r8 + 51], 2
mov word ptr [r8 + 52], 0x403
; supported_groups @ +54 : type 0x000a, len 4, liste 2, x25519 0x001d
mov dword ptr [r8 + 54], 0x4000a00
mov dword ptr [r8 + 58], 0x1d000200
; signature_algorithms @ +62 : type 0x000d, len 6, liste 4, 0x0804, 0x0401
mov dword ptr [r8 + 62], 0x6000d00
mov dword ptr [r8 + 66], 0x4080400
mov word ptr [r8 + 70], 0x104
; key_share @ +72 : type 0x0033, len 38, client_shares 36, groupe 0x001d,
; klen 32 — la clé publique suit @ +82 (QUATRE quads, la source INTACTE)
mov dword ptr [r8 + 72], 0x26003300
mov dword ptr [r8 + 76], 0x1d002400
mov word ptr [r8 + 80], 0x2000
mov r10, qword ptr [rdx]
mov qword ptr [r8 + 82], r10
mov r10, qword ptr [rdx + 8]
mov qword ptr [r8 + 90], r10
mov r10, qword ptr [rdx + 16]
mov qword ptr [r8 + 98], r10
mov r10, qword ptr [rdx + 24]
mov qword ptr [r8 + 106], r10
xor eax, eax
ret
.refus_nul:
mov rax, -1
ret
.refus_taille:
mov rax, -2
ret
