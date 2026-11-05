; tls13-17-ghash-multiplication · brouillon étiqueté — spec tls13-17:R1, bloc carte h100017
; GHASH : LA MULTIPLICATION GF(2^128) — la marche de l'algorithme 1 de
; SP 800-38D § 6.3, MOT POUR MOT : Z ← 0, V ← Y ; pour chaque bit de X
; (du premier au dernier de la chaîne) : si le bit est à 1, Z ← Z ⊕ V ;
; V est décalé d'un bit vers la fin, le bit sortant (le bit 0 de l'octet
; 15) déclenche le repli V ← V ⊕ R. SANS TABLE PAR DONNÉE (la table de
; Shoup indexée par les octets de H est la faille classique que la
; charte § 3 interdit : la marche est lente ET constante — le choix
; minimal auditable) ; la frontière I5 nommée : PCLMULQDQ est un
; CHANTIER FUTUR d'optimisation — mesuré, pas supposé (le miroir R11 de
; av-09) ; la marche binaire est la transcription EXACTE de la norme.
; LE DOMAINE GROS-BOUTISTE PAR BSWAP — LA SECONDE FAUTE nommée par la
; sonde du geste (la preuve corrige la notation, ENCORE : la première
; écriture tenait la chaîne en DEUX u64 little-endian et la sonde l'a
; renversée trente fois sur trente ; la contre-preuve du labo avait
; nommé la première lecture du repli en 0xE1<<56 — la correction
; d'alors s'était arrêtée à l'IMMÉDIAT, la REPRÉSENTATION restait
; fausse : le bit 63 de la voie basse n'est PAS le premier bit de la
; chaîne, le bit 0 de la voie haute n'est PAS le sortant) : la chaîne
; de 16 octets est l'entier GROS-BOUTISTE B = (h << 64) | l — h =
; bswap des octets 0..7 (la voie HAUTE : l'octet 0 AU SOMMET, son bit
; de poids fort = LE PREMIER BIT DE LA CHAÎNE), l = bswap des octets
; 8..15 (la voie BASSE : l'octet 15 AU FOND, son bit de poids faible =
; LE SORTANT) ; L'EXTRACTION (shld h, l, 1 pose CF à l'ancien bit 63
; de la voie haute = le bit courant) : le sbb LE CAPTURE AVANT que le
; shl de la voie basse n'écrase le drapeau — l'ordre shld/sbb/shl est
; LE geste de l'extraction ; LE DÉCALAGE de V vers la fin = le décalage
; À DROITE de B (shrd l, h, 1 puis shr h, 1), le sortant = l'ancien bit
; 0 de la voie basse (le CF du shrd, capturé au SECOND sbb avant le
; shr) ; LE REPLI R = 0xE1||0^120 (le plan, GCM_R — PUBLIQUE) : l'octet
; 0 de la chaîne vit au SOMMET de la voie haute — l'immédiat
; 0xE1 << 56, la voie basse de R est NULLE.
; LE SANS-BRANCHE DE DONNÉES (I1) : le bit courant de X devient un
; MASQUE 0/−1 par sbb rdx, rdx (la diffusion arithmétique du drapeau —
; le même geste que le gel de tls13-12), la sélection
; Z ← Z ⊕ (V ET masque) PAR ET LOGIQUE ; LE REPLI sans branche lui
; aussi (I2) : le sortant devient masque par le second sbb, le repli
; PAR ET LOGIQUE — AUCUNE instruction de branch ne lit X, Y ni V, les
; 128 itérations s'exécutent TOUJOURS (le SEUL saut du bloc est la
; boucle sur le COMPTEUR public).
; rcx = la sortie Z (16 o) · rdx = X (16 o) · r8 = Y (16 o — les trois
; zones peuvent se chevaucher : le bloc charge X et Y AVANT d'écrire,
; P3) · Q1 Z = X • Y — l'oracle différentiel (les paires du harnais)
; ET les vecteurs GCM en bout en bout (tls13-18/19 : la valeur de H et
; les étiquettes des Test Cases McGrew–Viega) ; la commutativité
; vérifiée aux DEUX ordres (Q1) · Q2 X et Y INTACTS · Q3 rax = 0.
; 0 push + sub rsp, 0x28 (40 o de locaux : z_h, z_l, le compteur, R —
; + la marge et l'alignement : entrée ≡ 8 → 8−40 ≡ 0 (mod 16)) ; I3 les
; transitoires en registres et sur la pile (charte § 6 — aucun état
; détenu) ; I4 AUCUN déplacement RIP (la constante R du plan en
; IMMÉDIAT, le miroir du bloc autoporteur) ; AUCUNE entrée IAT, AUCUN
; site syscall (charte § 7) ; aucun registre non volatil détruit ; NOP,
; 0x90 (charte § 8).
sub rsp, 0x28
mov rax, qword ptr [rdx]
bswap rax
mov r9, qword ptr [rdx + 8]
bswap r9
mov r10, qword ptr [r8]
bswap r10
mov r11, qword ptr [r8 + 8]
bswap r11
mov qword ptr [rsp], 0
mov qword ptr [rsp + 8], 0
mov qword ptr [rsp + 0x10], 128
movabs rdx, 0xe100000000000000
mov qword ptr [rsp + 0x18], rdx
.boucle:
shld rax, r9, 1
sbb rdx, rdx
shl r9, 1
mov r8, r10
and r8, rdx
xor qword ptr [rsp], r8
mov r8, r11
and r8, rdx
xor qword ptr [rsp + 8], r8
shrd r11, r10, 1
sbb rdx, rdx
shr r10, 1
mov r8, qword ptr [rsp + 0x18]
and r8, rdx
xor r10, r8
sub qword ptr [rsp + 0x10], 1
jnz .boucle
mov rax, qword ptr [rsp]
bswap rax
mov qword ptr [rcx], rax
mov rax, qword ptr [rsp + 8]
bswap rax
mov qword ptr [rcx + 8], rax
xor eax, eax
add rsp, 0x28
ret
