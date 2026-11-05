; tls13-15-aes128-cles-tour · bloc AES-128 le déploiement des clés de tour (FIPS 197 § 5.2) · spec tls13-15:R1 · bloc carte h100015
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0xdcc0, taille 576 octets
; Domaine : tls13 (M9, l'ère 1.0.0) · Dépendances : bloc feuille de la famille aead ; l'ARRÊT AES-NI — AESKEYGENASSIST le SubWord/RotWord MATÉRIEL, la disposition DÉRIVÉE DE L'OBSERVATION (le mot d'AES-128 au dword 3 → pshufd 0xFF — la sonde du labo, derive_aead.py), les DIX Rcon en IMMÉDIATS, la recette préfixe-XOR ⊕ t CONTRE-PROUVÉE sur C.1 ; les dix tours DÉROULÉS — AUCUN saut, AUCUN déplacement RIP
; Notation explicite générée par outils/auteur.py depuis brouillons/tls13-15-aes128-cles-tour.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 520 o · padding : 56 o (NOP, 0x90)
movdqu xmm0, xmmword ptr [rcx]
movdqu xmmword ptr [rdx], xmm0
aeskeygenassist xmm1, xmm0, 0x01
pshufd xmm1, xmm1, 0xff
movdqa xmm2, xmm0
pslldq xmm2, 4
pxor xmm2, xmm0
movdqa xmm3, xmm2
pslldq xmm3, 8
pxor xmm2, xmm3
pxor xmm2, xmm1
movdqa xmm0, xmm2
movdqu xmmword ptr [rdx + 0x10], xmm2
aeskeygenassist xmm1, xmm0, 0x02
pshufd xmm1, xmm1, 0xff
movdqa xmm2, xmm0
pslldq xmm2, 4
pxor xmm2, xmm0
movdqa xmm3, xmm2
pslldq xmm3, 8
pxor xmm2, xmm3
pxor xmm2, xmm1
movdqa xmm0, xmm2
movdqu xmmword ptr [rdx + 0x20], xmm2
aeskeygenassist xmm1, xmm0, 0x04
pshufd xmm1, xmm1, 0xff
movdqa xmm2, xmm0
pslldq xmm2, 4
pxor xmm2, xmm0
movdqa xmm3, xmm2
pslldq xmm3, 8
pxor xmm2, xmm3
pxor xmm2, xmm1
movdqa xmm0, xmm2
movdqu xmmword ptr [rdx + 0x30], xmm2
aeskeygenassist xmm1, xmm0, 0x08
pshufd xmm1, xmm1, 0xff
movdqa xmm2, xmm0
pslldq xmm2, 4
pxor xmm2, xmm0
movdqa xmm3, xmm2
pslldq xmm3, 8
pxor xmm2, xmm3
pxor xmm2, xmm1
movdqa xmm0, xmm2
movdqu xmmword ptr [rdx + 0x40], xmm2
aeskeygenassist xmm1, xmm0, 0x10
pshufd xmm1, xmm1, 0xff
movdqa xmm2, xmm0
pslldq xmm2, 4
pxor xmm2, xmm0
movdqa xmm3, xmm2
pslldq xmm3, 8
pxor xmm2, xmm3
pxor xmm2, xmm1
movdqa xmm0, xmm2
movdqu xmmword ptr [rdx + 0x50], xmm2
aeskeygenassist xmm1, xmm0, 0x20
pshufd xmm1, xmm1, 0xff
movdqa xmm2, xmm0
pslldq xmm2, 4
pxor xmm2, xmm0
movdqa xmm3, xmm2
pslldq xmm3, 8
pxor xmm2, xmm3
pxor xmm2, xmm1
movdqa xmm0, xmm2
movdqu xmmword ptr [rdx + 0x60], xmm2
aeskeygenassist xmm1, xmm0, 0x40
pshufd xmm1, xmm1, 0xff
movdqa xmm2, xmm0
pslldq xmm2, 4
pxor xmm2, xmm0
movdqa xmm3, xmm2
pslldq xmm3, 8
pxor xmm2, xmm3
pxor xmm2, xmm1
movdqa xmm0, xmm2
movdqu xmmword ptr [rdx + 0x70], xmm2
aeskeygenassist xmm1, xmm0, 0x80
pshufd xmm1, xmm1, 0xff
movdqa xmm2, xmm0
pslldq xmm2, 4
pxor xmm2, xmm0
movdqa xmm3, xmm2
pslldq xmm3, 8
pxor xmm2, xmm3
pxor xmm2, xmm1
movdqa xmm0, xmm2
movdqu xmmword ptr [rdx + 0x80], xmm2
aeskeygenassist xmm1, xmm0, 0x1b
pshufd xmm1, xmm1, 0xff
movdqa xmm2, xmm0
pslldq xmm2, 4
pxor xmm2, xmm0
movdqa xmm3, xmm2
pslldq xmm3, 8
pxor xmm2, xmm3
pxor xmm2, xmm1
movdqa xmm0, xmm2
movdqu xmmword ptr [rdx + 0x90], xmm2
aeskeygenassist xmm1, xmm0, 0x36
pshufd xmm1, xmm1, 0xff
movdqa xmm2, xmm0
pslldq xmm2, 4
pxor xmm2, xmm0
movdqa xmm3, xmm2
pslldq xmm3, 8
pxor xmm2, xmm3
pxor xmm2, xmm1
movdqa xmm0, xmm2
movdqu xmmword ptr [rdx + 0xa0], xmm2
xor eax, eax
ret
