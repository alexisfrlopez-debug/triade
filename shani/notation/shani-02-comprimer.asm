; shani-02-comprimer · bloc compression SHA-256 SHA-NI d'un bloc de 64 o · spec shani-02:R1 · bloc carte g210002 (PRÉFIGURÉ — la variante n'est PAS dans la carte : charte § 3, le scellage appartient au développeur)
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0xd080, taille 896 octets
; Domaine : shani (la variante SHA-NI, D205 — JAMAIS SCELLÉE) · Dépendances : bloc feuille ; LE MÊME CONTRAT que tls13-02 (R4) — la compression FIPS § 6.2.2 par sha256rnds2/msg1/msg2 ; le corps DÉROULÉ en 16 phases (I3 : zéro saut) ; le masque BE @R_MASQUE et les SEIZE groupes K du scellé (@R_K+16·g) cités par déplacement RIP (I2) ; xmm6/7 sauvés sur la pile (I4)
; Notation explicite générée par outils/auteur.py depuis brouillons/shani-02-comprimer.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 856 o · padding : 40 o (NOP, 0x90)
; Déplacements RIP (cible = adresse + taille + disp) :
;   0xd0d7 + 0x9 - 0xa8e0 = 0x2800
;   0xd0e0 + 0x9 - 0xa8e9 = 0x2800
;   0xd0e9 + 0x9 - 0xa8f2 = 0x2800
;   0xd0f2 + 0x9 - 0xa8fb = 0x2800
;   0xd0fb + 0x8 - 0xa203 = 0x2f00
;   0xd12a + 0x8 - 0xa222 = 0x2f10
;   0xd159 + 0x8 - 0xa241 = 0x2f20
;   0xd188 + 0x8 - 0xa260 = 0x2f30
;   0xd1b7 + 0x8 - 0xa27f = 0x2f40
;   0xd1e6 + 0x8 - 0xa29e = 0x2f50
;   0xd215 + 0x8 - 0xa2bd = 0x2f60
;   0xd244 + 0x8 - 0xa2dc = 0x2f70
;   0xd273 + 0x8 - 0xa2fb = 0x2f80
;   0xd2a2 + 0x8 - 0xa31a = 0x2f90
;   0xd2d1 + 0x8 - 0xa339 = 0x2fa0
;   0xd300 + 0x8 - 0xa358 = 0x2fb0
;   0xd32f + 0x8 - 0xa377 = 0x2fc0
;   0xd348 + 0x8 - 0xa380 = 0x2fd0
;   0xd361 + 0x8 - 0xa389 = 0x2fe0
;   0xd37a + 0x8 - 0xa392 = 0x2ff0
sub rsp, 0x48
movdqa [rsp], xmm6
movdqa [rsp + 0x10], xmm7
movdqu xmm3, [rcx]
movdqu xmm1, [rcx + 16]
pshufd xmm4, xmm3, 0xb1
pshufd xmm5, xmm1, 0xb1
punpcklqdq xmm5, xmm4
movdqa xmm2, xmm5
pshufd xmm3, xmm3, 0x1b
pshufd xmm1, xmm1, 0x1b
punpcklqdq xmm1, xmm3
movdqa [rsp + 0x20], xmm2
movdqa [rsp + 0x30], xmm1
movdqu xmm3, [rdx]
movdqu xmm4, [rdx + 16]
movdqu xmm5, [rdx + 32]
movdqu xmm6, [rdx + 48]
pshufb xmm3, [rip - 0xa8e0]
pshufb xmm4, [rip - 0xa8e9]
pshufb xmm5, [rip - 0xa8f2]
pshufb xmm6, [rip - 0xa8fb]
movdqa xmm0, [rip - 0xa203]
paddd xmm0, xmm3
sha256rnds2 xmm1, xmm2
pshufd xmm0, xmm0, 0x0e
sha256rnds2 xmm2, xmm1
sha256msg1 xmm3, xmm4
movdqa xmm7, xmm6
palignr xmm7, xmm5, 4
paddd xmm3, xmm7
sha256msg2 xmm3, xmm6
movdqa xmm0, [rip - 0xa222]
paddd xmm0, xmm4
sha256rnds2 xmm1, xmm2
pshufd xmm0, xmm0, 0x0e
sha256rnds2 xmm2, xmm1
sha256msg1 xmm4, xmm5
movdqa xmm7, xmm3
palignr xmm7, xmm6, 4
paddd xmm4, xmm7
sha256msg2 xmm4, xmm3
movdqa xmm0, [rip - 0xa241]
paddd xmm0, xmm5
sha256rnds2 xmm1, xmm2
pshufd xmm0, xmm0, 0x0e
sha256rnds2 xmm2, xmm1
sha256msg1 xmm5, xmm6
movdqa xmm7, xmm4
palignr xmm7, xmm3, 4
paddd xmm5, xmm7
sha256msg2 xmm5, xmm4
movdqa xmm0, [rip - 0xa260]
paddd xmm0, xmm6
sha256rnds2 xmm1, xmm2
pshufd xmm0, xmm0, 0x0e
sha256rnds2 xmm2, xmm1
sha256msg1 xmm6, xmm3
movdqa xmm7, xmm5
palignr xmm7, xmm4, 4
paddd xmm6, xmm7
sha256msg2 xmm6, xmm5
movdqa xmm0, [rip - 0xa27f]
paddd xmm0, xmm3
sha256rnds2 xmm1, xmm2
pshufd xmm0, xmm0, 0x0e
sha256rnds2 xmm2, xmm1
sha256msg1 xmm3, xmm4
movdqa xmm7, xmm6
palignr xmm7, xmm5, 4
paddd xmm3, xmm7
sha256msg2 xmm3, xmm6
movdqa xmm0, [rip - 0xa29e]
paddd xmm0, xmm4
sha256rnds2 xmm1, xmm2
pshufd xmm0, xmm0, 0x0e
sha256rnds2 xmm2, xmm1
sha256msg1 xmm4, xmm5
movdqa xmm7, xmm3
palignr xmm7, xmm6, 4
paddd xmm4, xmm7
sha256msg2 xmm4, xmm3
movdqa xmm0, [rip - 0xa2bd]
paddd xmm0, xmm5
sha256rnds2 xmm1, xmm2
pshufd xmm0, xmm0, 0x0e
sha256rnds2 xmm2, xmm1
sha256msg1 xmm5, xmm6
movdqa xmm7, xmm4
palignr xmm7, xmm3, 4
paddd xmm5, xmm7
sha256msg2 xmm5, xmm4
movdqa xmm0, [rip - 0xa2dc]
paddd xmm0, xmm6
sha256rnds2 xmm1, xmm2
pshufd xmm0, xmm0, 0x0e
sha256rnds2 xmm2, xmm1
sha256msg1 xmm6, xmm3
movdqa xmm7, xmm5
palignr xmm7, xmm4, 4
paddd xmm6, xmm7
sha256msg2 xmm6, xmm5
movdqa xmm0, [rip - 0xa2fb]
paddd xmm0, xmm3
sha256rnds2 xmm1, xmm2
pshufd xmm0, xmm0, 0x0e
sha256rnds2 xmm2, xmm1
sha256msg1 xmm3, xmm4
movdqa xmm7, xmm6
palignr xmm7, xmm5, 4
paddd xmm3, xmm7
sha256msg2 xmm3, xmm6
movdqa xmm0, [rip - 0xa31a]
paddd xmm0, xmm4
sha256rnds2 xmm1, xmm2
pshufd xmm0, xmm0, 0x0e
sha256rnds2 xmm2, xmm1
sha256msg1 xmm4, xmm5
movdqa xmm7, xmm3
palignr xmm7, xmm6, 4
paddd xmm4, xmm7
sha256msg2 xmm4, xmm3
movdqa xmm0, [rip - 0xa339]
paddd xmm0, xmm5
sha256rnds2 xmm1, xmm2
pshufd xmm0, xmm0, 0x0e
sha256rnds2 xmm2, xmm1
sha256msg1 xmm5, xmm6
movdqa xmm7, xmm4
palignr xmm7, xmm3, 4
paddd xmm5, xmm7
sha256msg2 xmm5, xmm4
movdqa xmm0, [rip - 0xa358]
paddd xmm0, xmm6
sha256rnds2 xmm1, xmm2
pshufd xmm0, xmm0, 0x0e
sha256rnds2 xmm2, xmm1
sha256msg1 xmm6, xmm3
movdqa xmm7, xmm5
palignr xmm7, xmm4, 4
paddd xmm6, xmm7
sha256msg2 xmm6, xmm5
movdqa xmm0, [rip - 0xa377]
paddd xmm0, xmm3
sha256rnds2 xmm1, xmm2
pshufd xmm0, xmm0, 0x0e
sha256rnds2 xmm2, xmm1
movdqa xmm0, [rip - 0xa380]
paddd xmm0, xmm4
sha256rnds2 xmm1, xmm2
pshufd xmm0, xmm0, 0x0e
sha256rnds2 xmm2, xmm1
movdqa xmm0, [rip - 0xa389]
paddd xmm0, xmm5
sha256rnds2 xmm1, xmm2
pshufd xmm0, xmm0, 0x0e
sha256rnds2 xmm2, xmm1
movdqa xmm0, [rip - 0xa392]
paddd xmm0, xmm6
sha256rnds2 xmm1, xmm2
pshufd xmm0, xmm0, 0x0e
sha256rnds2 xmm2, xmm1
movdqa xmm0, [rsp + 0x20]
paddd xmm2, xmm0
movdqa xmm0, [rsp + 0x30]
paddd xmm1, xmm0
pshufd xmm0, xmm2, 0x1b
pshufd xmm2, xmm1, 0x1b
movdqa xmm1, xmm0
punpckhqdq xmm0, xmm2
punpcklqdq xmm1, xmm2
movdqu [rcx], xmm1
movdqu [rcx + 16], xmm0
movdqa xmm6, [rsp]
movdqa xmm7, [rsp + 0x10]
add rsp, 0x48
xor eax, eax
ret
