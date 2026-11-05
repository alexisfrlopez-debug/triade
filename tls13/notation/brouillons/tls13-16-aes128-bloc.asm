; tls13-16-aes128-bloc · brouillon étiqueté — spec tls13-16:R1, bloc carte h100016
; AES-128 : LE CHIFFREMENT D'UN BLOC — LE bloc de 16 octets : pxor RK[0],
; NEUF tours AESENC (RK[1..9]), le tour final AESENCLAST (RK[10], sans
; MixColumns) — l'arrêt AES-NI de tls13-15 poursuivi. Le chiffrement GCM
; est TOUJOURS le chiffrement DIRECT : le compteur est re-chiffré pour
; produire le flot, l'ouverture re-chiffre les compteurs (SP 800-38D § 6)
; — LA BRIQUE D'INVERSION N'EXISTE PAS DANS LE DOMAINE (l'intention le
; nomme : AES n'apparaît qu'en sens unique, l'InvCipher et ses tables
; inverses jamais).
; LA SÉMANTIQUE — CONTRE-PROUVÉE PAR LE LABO sur l'émulation AVANT la
; notation (derive_aead.py, le juge est le code) : AESENC =
; MixColumns(ShiftRows(SubBytes(état))) ⊕ clé, AESENCLAST sans
; MixColumns ; LA COMPOSITION pxor + 9×AESENC + AESENCLAST rend
; EXACTEMENT le vecteur FIPS 197 appendice C.1 (69c4e0d8… — la
; composition blanche a été jouée sur l'émulateur AVANT d'être écrite
; ici). Les clés de tour arrivent par MOYENS NON ALIGNÉS (movdqu — le
; contrat P1 ne promet PAS l'alignement de rcx, la forme mémoire directe
; d'aesenc l'exigerait : le chargement explicite est le choix SANS
; précondition cachée), le registre-form aesenc suit.
; rcx = les clés de tour (176 o — le produit de tls13-15) · rdx = le
; bloc d'entrée (16 o) · r8 = le bloc de sortie (16 o — peut chevaucher
; rdx : le bloc charge AVANT d'écrire, P3) · Q1 la sortie = AES-128
; (chiffrement, clés, entrée) — FIPS 197 C.1 (clé 000102…0f, entrée
; 00112233…ff → 69c4e0d86a7b0430d8cdb78070b4c55a) ET SP 800-38A F.1.1
; (les QUATRE blocs ECB-AES128) · Q2 les clés de tour et l'entrée
; INTACTES · Q3 rax = 0.
; I1 le flot : dix tours TOUJOURS exécutés, aucune branche du bloc — la
; propriété est GRATUITE PAR CONSTRUCTION (la spec la constate : l'entrée
; du CTR est publique, le flot produit est secret, l'instruction
; matérielle ne branche pas) ; I2 AUCUNE entrée IAT, AUCUN site syscall
; (charte § 7) ; aucun état détenu (charte § 6) ; I3 aucun registre non
; volatil détruit ; NOP, 0x90 (charte § 8).
; 0 push + AUCUN cadre (bloc FEUILLE — la convention tls13-01/12 : la
; pile ne porte RIEN) ; AUCUN déplacement RIP — tout vit en xmm.
movdqu xmm0, xmmword ptr [rdx]
movdqu xmm1, xmmword ptr [rcx]
pxor xmm0, xmm1
movdqu xmm1, xmmword ptr [rcx + 0x10]
aesenc xmm0, xmm1
movdqu xmm1, xmmword ptr [rcx + 0x20]
aesenc xmm0, xmm1
movdqu xmm1, xmmword ptr [rcx + 0x30]
aesenc xmm0, xmm1
movdqu xmm1, xmmword ptr [rcx + 0x40]
aesenc xmm0, xmm1
movdqu xmm1, xmmword ptr [rcx + 0x50]
aesenc xmm0, xmm1
movdqu xmm1, xmmword ptr [rcx + 0x60]
aesenc xmm0, xmm1
movdqu xmm1, xmmword ptr [rcx + 0x70]
aesenc xmm0, xmm1
movdqu xmm1, xmmword ptr [rcx + 0x80]
aesenc xmm0, xmm1
movdqu xmm1, xmmword ptr [rcx + 0x90]
aesenc xmm0, xmm1
movdqu xmm1, xmmword ptr [rcx + 0xa0]
aesenclast xmm0, xmm1
movdqu xmmword ptr [r8], xmm0
xor eax, eax
ret
