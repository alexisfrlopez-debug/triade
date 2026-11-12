; shani-02-comprimer · brouillon étiqueté — spec shani-02:R1, bloc préfiguré g210002
; LA COMPRESSION FIPS § 6.2.2 PAR LES INSTRUCTIONS SHA-NI — le contrat de
; tls13-02 À LA LETTRE (R4) : rcx = le contexte, rdx = le bloc de 64 o,
; H[0..7] := l'état après compression, rax = 0. Le corps DÉROULÉ en 16
; phases (I3 : ZÉRO saut — le temps constant par construction, le contrôle
; structurel du vérificateur le constatera).
;
; LA STRUCTURE (éprouvée à la main AVANT la notation —
; epreuve_compression_shani.py : 100/100 au juge Python, les QUATRE
; vecteurs FIPS verts, le corpus aux bords vert) :
;   - l'état en ping-pong xmm1/xmm2, la mise en page de travail
;     (F,E,B,A)/(H,G,D,C) — les paires renversées par pshufd 0xB1/0x1B,
;     assemblées par punpcklqdq ;
;   - le cur (W+K) TOUJOURS en xmm0 — l'opérande IMPLICITE de sha256rnds2
;     (les sommes des deux constantes et des deux mots du message dans
;     [63:0], la paire haute extraite par pshufd 0x0E) ;
;   - les groupes A/B/C/D = xmm3..6 (le brut JAMAIS additionné de K — pas
;     de conflit brut/cur, le calendrier lit le brut), le grattoir xmm7 ;
;   - le cycle de quatre phases : msg1 sur le mourant, le W[t-7] par
;     palignr sur la COPIE du plus récent, msg2 chaîné ;
;   - xmm6/xmm7 NON VOLATILS msx64 : sauvés/restaurés sur la pile (I4) —
;     le budget des six volatifs ne suffit pas, le septième et le
;     huitième y vivent LOUÉS, rendus INTACTS ;
;   - la table K : CELLE DU SCELLÉ @0x2F00, seize groupes alignés lus par
;     movdqa (I2) ; le masque BE @0x2800 (chaque dword renversé).
;
; L'ALIGNEMENT : entrée ≡ 8 (mod 16) après l'appel ; sub 0x48 (72) →
; ≡ 0 (mod 16) aux movdqa ; 0x40 de crémaillère (xmm6, xmm7, ABEF sauvé,
; CDGH sauvé) + 8 de rattrapage.
sub rsp, 0x48
movdqa [rsp], xmm6
movdqa [rsp + 0x10], xmm7
; l'état scellé lu du contexte : (A,B,C,D) et (E,F,G,H)
movdqu xmm3, [rcx]
movdqu xmm1, [rcx + 16]
; la mise en page de travail : STATE0 = (F,E,B,A), STATE1 = (H,G,D,C)
pshufd xmm4, xmm3, 0xb1
pshufd xmm5, xmm1, 0xb1
punpcklqdq xmm5, xmm4
movdqa xmm2, xmm5
pshufd xmm3, xmm3, 0x1b
pshufd xmm1, xmm1, 0x1b
punpcklqdq xmm1, xmm3
movdqa [rsp + 0x20], xmm2
movdqa [rsp + 0x30], xmm1
; le bloc : quatre groupes BE par le masque
movdqu xmm3, [rdx]
movdqu xmm4, [rdx + 16]
movdqu xmm5, [rdx + 32]
movdqu xmm6, [rdx + 48]
pshufb xmm3, [rip + MASQUE]
pshufb xmm4, [rip + MASQUE]
pshufb xmm5, [rip + MASQUE]
pshufb xmm6, [rip + MASQUE]
; --- phase 0 : rounds 0-3, groupe 0 en A, le calendrier du groupe 4 ---
movdqa xmm0, [rip + K_G0]
paddd xmm0, xmm3
sha256rnds2 xmm1, xmm2
pshufd xmm0, xmm0, 0x0e
sha256rnds2 xmm2, xmm1
sha256msg1 xmm3, xmm4
movdqa xmm7, xmm6
palignr xmm7, xmm5, 4
paddd xmm3, xmm7
sha256msg2 xmm3, xmm6
; --- phase 1 : rounds 4-7, groupe 1 en B, le calendrier du groupe 5 ---
movdqa xmm0, [rip + K_G1]
paddd xmm0, xmm4
sha256rnds2 xmm1, xmm2
pshufd xmm0, xmm0, 0x0e
sha256rnds2 xmm2, xmm1
sha256msg1 xmm4, xmm5
movdqa xmm7, xmm3
palignr xmm7, xmm6, 4
paddd xmm4, xmm7
sha256msg2 xmm4, xmm3
; --- phase 2 : rounds 8-11, groupe 2 en C, le calendrier du groupe 6 ---
movdqa xmm0, [rip + K_G2]
paddd xmm0, xmm5
sha256rnds2 xmm1, xmm2
pshufd xmm0, xmm0, 0x0e
sha256rnds2 xmm2, xmm1
sha256msg1 xmm5, xmm6
movdqa xmm7, xmm4
palignr xmm7, xmm3, 4
paddd xmm5, xmm7
sha256msg2 xmm5, xmm4
; --- phase 3 : rounds 12-15, groupe 3 en D, le calendrier du groupe 7 ---
movdqa xmm0, [rip + K_G3]
paddd xmm0, xmm6
sha256rnds2 xmm1, xmm2
pshufd xmm0, xmm0, 0x0e
sha256rnds2 xmm2, xmm1
sha256msg1 xmm6, xmm3
movdqa xmm7, xmm5
palignr xmm7, xmm4, 4
paddd xmm6, xmm7
sha256msg2 xmm6, xmm5
; --- phase 4 : rounds 16-19, groupe 4 en A, le calendrier du groupe 8 ---
movdqa xmm0, [rip + K_G4]
paddd xmm0, xmm3
sha256rnds2 xmm1, xmm2
pshufd xmm0, xmm0, 0x0e
sha256rnds2 xmm2, xmm1
sha256msg1 xmm3, xmm4
movdqa xmm7, xmm6
palignr xmm7, xmm5, 4
paddd xmm3, xmm7
sha256msg2 xmm3, xmm6
; --- phase 5 : rounds 20-23, groupe 5 en B, le calendrier du groupe 9 ---
movdqa xmm0, [rip + K_G5]
paddd xmm0, xmm4
sha256rnds2 xmm1, xmm2
pshufd xmm0, xmm0, 0x0e
sha256rnds2 xmm2, xmm1
sha256msg1 xmm4, xmm5
movdqa xmm7, xmm3
palignr xmm7, xmm6, 4
paddd xmm4, xmm7
sha256msg2 xmm4, xmm3
; --- phase 6 : rounds 24-27, groupe 6 en C, le calendrier du groupe 10 ---
movdqa xmm0, [rip + K_G6]
paddd xmm0, xmm5
sha256rnds2 xmm1, xmm2
pshufd xmm0, xmm0, 0x0e
sha256rnds2 xmm2, xmm1
sha256msg1 xmm5, xmm6
movdqa xmm7, xmm4
palignr xmm7, xmm3, 4
paddd xmm5, xmm7
sha256msg2 xmm5, xmm4
; --- phase 7 : rounds 28-31, groupe 7 en D, le calendrier du groupe 11 ---
movdqa xmm0, [rip + K_G7]
paddd xmm0, xmm6
sha256rnds2 xmm1, xmm2
pshufd xmm0, xmm0, 0x0e
sha256rnds2 xmm2, xmm1
sha256msg1 xmm6, xmm3
movdqa xmm7, xmm5
palignr xmm7, xmm4, 4
paddd xmm6, xmm7
sha256msg2 xmm6, xmm5
; --- phase 8 : rounds 32-35, groupe 8 en A, le calendrier du groupe 12 ---
movdqa xmm0, [rip + K_G8]
paddd xmm0, xmm3
sha256rnds2 xmm1, xmm2
pshufd xmm0, xmm0, 0x0e
sha256rnds2 xmm2, xmm1
sha256msg1 xmm3, xmm4
movdqa xmm7, xmm6
palignr xmm7, xmm5, 4
paddd xmm3, xmm7
sha256msg2 xmm3, xmm6
; --- phase 9 : rounds 36-39, groupe 9 en B, le calendrier du groupe 13 ---
movdqa xmm0, [rip + K_G9]
paddd xmm0, xmm4
sha256rnds2 xmm1, xmm2
pshufd xmm0, xmm0, 0x0e
sha256rnds2 xmm2, xmm1
sha256msg1 xmm4, xmm5
movdqa xmm7, xmm3
palignr xmm7, xmm6, 4
paddd xmm4, xmm7
sha256msg2 xmm4, xmm3
; --- phase 10 : rounds 40-43, groupe 10 en C, le calendrier du groupe 14 ---
movdqa xmm0, [rip + K_G10]
paddd xmm0, xmm5
sha256rnds2 xmm1, xmm2
pshufd xmm0, xmm0, 0x0e
sha256rnds2 xmm2, xmm1
sha256msg1 xmm5, xmm6
movdqa xmm7, xmm4
palignr xmm7, xmm3, 4
paddd xmm5, xmm7
sha256msg2 xmm5, xmm4
; --- phase 11 : rounds 44-47, groupe 11 en D, le calendrier du groupe 15 ---
movdqa xmm0, [rip + K_G11]
paddd xmm0, xmm6
sha256rnds2 xmm1, xmm2
pshufd xmm0, xmm0, 0x0e
sha256rnds2 xmm2, xmm1
sha256msg1 xmm6, xmm3
movdqa xmm7, xmm5
palignr xmm7, xmm4, 4
paddd xmm6, xmm7
sha256msg2 xmm6, xmm5
; --- phase 12 : rounds 48-51, groupe 12 en A (le calendrier est ÉPUISÉ) ---
movdqa xmm0, [rip + K_G12]
paddd xmm0, xmm3
sha256rnds2 xmm1, xmm2
pshufd xmm0, xmm0, 0x0e
sha256rnds2 xmm2, xmm1
; --- phase 13 : rounds 52-55, groupe 13 en B ---
movdqa xmm0, [rip + K_G13]
paddd xmm0, xmm4
sha256rnds2 xmm1, xmm2
pshufd xmm0, xmm0, 0x0e
sha256rnds2 xmm2, xmm1
; --- phase 14 : rounds 56-59, groupe 14 en C ---
movdqa xmm0, [rip + K_G14]
paddd xmm0, xmm5
sha256rnds2 xmm1, xmm2
pshufd xmm0, xmm0, 0x0e
sha256rnds2 xmm2, xmm1
; --- phase 15 : rounds 60-63, groupe 15 en D ---
movdqa xmm0, [rip + K_G15]
paddd xmm0, xmm6
sha256rnds2 xmm1, xmm2
pshufd xmm0, xmm0, 0x0e
sha256rnds2 xmm2, xmm1
; la sortie : l'état final + l'initial (la double addition FIPS), remis
; en (A..H) au contexte — H[0..7] SEULS (Q2 : tampon, remplissage et
; total INTACTS)
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
