; tls13-15-aes128-cles-tour · brouillon étiqueté — spec tls13-15:R1, bloc carte h100015
; AES-128 : LE DÉPLOIEMENT DES CLÉS DE TOUR — l'expansion FIPS 197 § 5.2 /
; SP 800-38A : les ONZE clés de tour (176 o) depuis la clé de 16 o, le mot
; w[i] = w[i−4] ⊕ T(w[i−1]) où T = RotWord ∘ SubWord ⊕ Rcon (les deux sens
; COMMUTENT — SubWord(RotWord(w)) == RotWord(SubWord(w)), la notation suit
; le matériel). L'ARRÊT AES-NI NOMMÉ (I1 de la spec) : la transcription se
; fait par AESKEYGENASSIST — le SubWord/RotWord MATÉRIEL, le Rcon en
; immédiat ; la S-box n'est PAS une table logicielle : une table indexée
; par la donnée secrète est la faille que la charte § 3 interdit,
; l'instruction matérielle est temps constant PAR CONSTRUCTION (I2).
; rcx = la clé (16 o) · rdx = la sortie (176 o : RK[0..10], RK[0] EST la
; clé) · Q1 le déploiement conforme FIPS 197 § 5.2 — l'oracle
; différentiel du harnais (les 176 o confrontés à Python sur la clé
; 000102…0f de l'appendice C.1 ET les quatre clés F.1.1) ET À L'USAGE par
; tls13-16 (un déploiement faux rend un chiffrement faux) · Q2 la clé
; INTACTE · Q3 rax = 0.
; LA DISPOSITION D'AESKEYGENASSIST — DÉRIVÉE DE L'OBSERVATION (le juge est
; le code : la sonde du labo a lu la sortie sur pièces, derive_aead.py —
; les candidats de mémoire étaient faux TOUS LES DEUX) :
;   dword0 = SubWord(w1), dword1 = RotWord(SubWord(w1)) ⊕ Rcon,
;   dword2 = SubWord(w3), dword3 = RotWord(SubWord(w3)) ⊕ Rcon —
; LE MOT D'AES-128 (T(w3) = SubWord∘RotWord(w3) ⊕ Rcon) EST LE DWORD 3 :
; la diffusion pshufd 0xFF le porte aux quatre voies (le secours d'AES-
; 192/256 — dword1 — n'est pas lu : le bloc n'existe pas, I1 la propriété
; est structurelle).
; LA RECETTE DU TOUR (contre-prouvée sur C.1 par le labo AVANT la
; notation) : RK'[i] = préfixe-XOR(RK)[i] ⊕ T(w3) — car w'[0] = w0 ⊕ t,
; w'[1] = w1 ⊕ w'[0], … le préfixe-XOR des mots par DEUX décalages
; d'octets pslldq 4 puis 8 (la voie AUDITABLE, dix fois la même) ; les
; DIX Rcon (01 02 04 08 10 20 40 80 1b 36 — x^i dans GF(2^8), DÉRIVÉS
; du plan) sont des IMMÉDIATS de l'instruction — AUCUNE donnée RIP (I1,
; le miroir du choix av-01/av-08 : le bloc autoporteur), les dix tours
; DÉROULÉS : AUCUN saut du bloc entier, la propriété I2 est GRATUITE.
; 0 push + AUCUN cadre (bloc FEUILLE sans appel ni local — la convention
; des feuilles de la famille : tls13-01/12 entrent directement, la pile
; ne porte RIEN, l'alignement d'entrée est celui de l'appelant) ;
; AUCUNE entrée IAT, AUCUN site syscall (charte § 7) ; aucun état détenu
; (charte § 6) ; aucun registre non volatil détruit (I5) ; NOP, 0x90
; (charte § 8).
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
