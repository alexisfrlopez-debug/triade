; tls13-02-shani · LE COULOIR SHA-NI DE LA COMPRESSION (fnvan0zes, la vague 11) · spec tls13-02:R1 (LE MÊME CONTRAT — R4)
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0xd300 (la marge VIERGE — AUCUN octet du scellé touché, le modèle OPT-01)
; Domaine : tls13 (M9) · Dépendances : la table K[64] scellée à 0x2f00 (le fixture R_K — LE MÊME, lu, jamais copié)
; LE DISPATCH RUNTIME : CPUID(7,0).EBX[29] (SHA) — le sondage UNE FOIS PAR APPEL ; le REPLI BASELINE : LE SCELLÉ GPR (jmp 0xc080),
; jamais une copie — la machine sans SHA-NI vit le scellé (le contrat par construction).
; L'ALGORITHME : la référence sha256ni_ref.c VÉRIFIÉE (256/256 vecteurs aléatoires, zéro divergence contre le juge) ;
; les lanes RÉSOLUES PAR SONDES (rnds2 : src=(A,B,E,F)@lanes 3,2,1,0, dst=(C,D,G,H), sortie=le nouveau ABEF dans dst ;
; msg1/msg2 : les formules sondées) ; les instructions SHA AUX OCTETS EXPLICITES (keystone ne les porte pas — 0F 38 CB/CC/CD /r,
; l'encodage vérifié as/objdump ET le round-trip capstone).
; LE CONTRAT (tls13-02:R1 À LA LETTRE — R4) : (ptr état, ptr bloc) -> 0, l'état mis à jour par addition (FIPS § 6.2.2),
; silencieux, les non-volatils rendus.
push rbp
mov rbp, rcx
mov r10, rdx
; ---- LE DISPATCH (une fois par appel) -----------------------------------------
xor ecx, ecx
mov eax, 7
cpuid
test ebx, 0x20000000
jz 0xc080
; ---- L'ÉTAT : ABEF/CDGH aux lanes 3,2,1,0 --------------------------------------
movdqu xmm4, xmmword ptr [rbp]
movdqu xmm5, xmmword ptr [rbp + 16]
pshufd xmm1, xmm4, 0xb1
pshufd xmm2, xmm5, 0xb1
movdqa xmm3, xmm2
punpcklqdq xmm2, xmm1
punpckhqdq xmm3, xmm1
movdqa xmm1, xmm2
movdqa xmm2, xmm3
; ---- LES FENÊTRES DU MESSAGE (bswap par dword) ---------------------------------
lea r11, [rip + @MASQUE]
movdqu xmm6, xmmword ptr [r10 + 0]
pshufb xmm6, xmmword ptr [r11]
movdqu xmm7, xmmword ptr [r10 + 16]
pshufb xmm7, xmmword ptr [r11]
movdqu xmm8, xmmword ptr [r10 + 32]
pshufb xmm8, xmmword ptr [r11]
movdqu xmm9, xmmword ptr [r10 + 48]
pshufb xmm9, xmmword ptr [r11]
; ---- LES RONDES 0-15 (les fenêtres d'entrée) -----------------------------------
movdqa xmm0, xmm6
paddd xmm0, xmmword ptr [rip + @K0]
db 0f 38 cb d1 ; sha256rnds2 xmm2, xmm1
pshufd xmm0, xmm0, 0x0e
db 0f 38 cb ca ; sha256rnds2 xmm1, xmm2
movdqa xmm0, xmm7
paddd xmm0, xmmword ptr [rip + @K4]
db 0f 38 cb d1 ; sha256rnds2 xmm2, xmm1
pshufd xmm0, xmm0, 0x0e
db 0f 38 cb ca ; sha256rnds2 xmm1, xmm2
movdqa xmm0, xmm8
paddd xmm0, xmmword ptr [rip + @K8]
db 0f 38 cb d1 ; sha256rnds2 xmm2, xmm1
pshufd xmm0, xmm0, 0x0e
db 0f 38 cb ca ; sha256rnds2 xmm1, xmm2
movdqa xmm0, xmm9
paddd xmm0, xmmword ptr [rip + @K12]
db 0f 38 cb d1 ; sha256rnds2 xmm2, xmm1
pshufd xmm0, xmm0, 0x0e
db 0f 38 cb ca ; sha256rnds2 xmm1, xmm2
; ---- LES GÉNÉRATIONS 0-11 (msg1/alignr/add/msg2 + la paire rnds2) --------------
; la génération 0 : la fenêtre W[16..19]
db 0f 38 cc f7 ; sha256msg1 xmm6, xmm7
movdqa xmm3, xmm9
palignr xmm3, xmm8, 4
paddd xmm6, xmm3
db 41 0f 38 cd f1 ; sha256msg2 xmm6, xmm9
movdqa xmm0, xmm6
paddd xmm0, xmmword ptr [rip + @K16]
db 0f 38 cb d1 ; sha256rnds2 xmm2, xmm1
pshufd xmm0, xmm0, 0x0e
db 0f 38 cb ca ; sha256rnds2 xmm1, xmm2
; la génération 1 : la fenêtre W[20..23]
db 41 0f 38 cc f8 ; sha256msg1 xmm7, xmm8
movdqa xmm3, xmm6
palignr xmm3, xmm9, 4
paddd xmm7, xmm3
db 0f 38 cd fe ; sha256msg2 xmm7, xmm6
movdqa xmm0, xmm7
paddd xmm0, xmmword ptr [rip + @K20]
db 0f 38 cb d1 ; sha256rnds2 xmm2, xmm1
pshufd xmm0, xmm0, 0x0e
db 0f 38 cb ca ; sha256rnds2 xmm1, xmm2
; la génération 2 : la fenêtre W[24..27]
db 45 0f 38 cc c1 ; sha256msg1 xmm8, xmm9
movdqa xmm3, xmm7
palignr xmm3, xmm6, 4
paddd xmm8, xmm3
db 44 0f 38 cd c7 ; sha256msg2 xmm8, xmm7
movdqa xmm0, xmm8
paddd xmm0, xmmword ptr [rip + @K24]
db 0f 38 cb d1 ; sha256rnds2 xmm2, xmm1
pshufd xmm0, xmm0, 0x0e
db 0f 38 cb ca ; sha256rnds2 xmm1, xmm2
; la génération 3 : la fenêtre W[28..31]
db 44 0f 38 cc ce ; sha256msg1 xmm9, xmm6
movdqa xmm3, xmm8
palignr xmm3, xmm7, 4
paddd xmm9, xmm3
db 45 0f 38 cd c8 ; sha256msg2 xmm9, xmm8
movdqa xmm0, xmm9
paddd xmm0, xmmword ptr [rip + @K28]
db 0f 38 cb d1 ; sha256rnds2 xmm2, xmm1
pshufd xmm0, xmm0, 0x0e
db 0f 38 cb ca ; sha256rnds2 xmm1, xmm2
; la génération 4 : la fenêtre W[32..35]
db 0f 38 cc f7 ; sha256msg1 xmm6, xmm7
movdqa xmm3, xmm9
palignr xmm3, xmm8, 4
paddd xmm6, xmm3
db 41 0f 38 cd f1 ; sha256msg2 xmm6, xmm9
movdqa xmm0, xmm6
paddd xmm0, xmmword ptr [rip + @K32]
db 0f 38 cb d1 ; sha256rnds2 xmm2, xmm1
pshufd xmm0, xmm0, 0x0e
db 0f 38 cb ca ; sha256rnds2 xmm1, xmm2
; la génération 5 : la fenêtre W[36..39]
db 41 0f 38 cc f8 ; sha256msg1 xmm7, xmm8
movdqa xmm3, xmm6
palignr xmm3, xmm9, 4
paddd xmm7, xmm3
db 0f 38 cd fe ; sha256msg2 xmm7, xmm6
movdqa xmm0, xmm7
paddd xmm0, xmmword ptr [rip + @K36]
db 0f 38 cb d1 ; sha256rnds2 xmm2, xmm1
pshufd xmm0, xmm0, 0x0e
db 0f 38 cb ca ; sha256rnds2 xmm1, xmm2
; la génération 6 : la fenêtre W[40..43]
db 45 0f 38 cc c1 ; sha256msg1 xmm8, xmm9
movdqa xmm3, xmm7
palignr xmm3, xmm6, 4
paddd xmm8, xmm3
db 44 0f 38 cd c7 ; sha256msg2 xmm8, xmm7
movdqa xmm0, xmm8
paddd xmm0, xmmword ptr [rip + @K40]
db 0f 38 cb d1 ; sha256rnds2 xmm2, xmm1
pshufd xmm0, xmm0, 0x0e
db 0f 38 cb ca ; sha256rnds2 xmm1, xmm2
; la génération 7 : la fenêtre W[44..47]
db 44 0f 38 cc ce ; sha256msg1 xmm9, xmm6
movdqa xmm3, xmm8
palignr xmm3, xmm7, 4
paddd xmm9, xmm3
db 45 0f 38 cd c8 ; sha256msg2 xmm9, xmm8
movdqa xmm0, xmm9
paddd xmm0, xmmword ptr [rip + @K44]
db 0f 38 cb d1 ; sha256rnds2 xmm2, xmm1
pshufd xmm0, xmm0, 0x0e
db 0f 38 cb ca ; sha256rnds2 xmm1, xmm2
; la génération 8 : la fenêtre W[48..51]
db 0f 38 cc f7 ; sha256msg1 xmm6, xmm7
movdqa xmm3, xmm9
palignr xmm3, xmm8, 4
paddd xmm6, xmm3
db 41 0f 38 cd f1 ; sha256msg2 xmm6, xmm9
movdqa xmm0, xmm6
paddd xmm0, xmmword ptr [rip + @K48]
db 0f 38 cb d1 ; sha256rnds2 xmm2, xmm1
pshufd xmm0, xmm0, 0x0e
db 0f 38 cb ca ; sha256rnds2 xmm1, xmm2
; la génération 9 : la fenêtre W[52..55]
db 41 0f 38 cc f8 ; sha256msg1 xmm7, xmm8
movdqa xmm3, xmm6
palignr xmm3, xmm9, 4
paddd xmm7, xmm3
db 0f 38 cd fe ; sha256msg2 xmm7, xmm6
movdqa xmm0, xmm7
paddd xmm0, xmmword ptr [rip + @K52]
db 0f 38 cb d1 ; sha256rnds2 xmm2, xmm1
pshufd xmm0, xmm0, 0x0e
db 0f 38 cb ca ; sha256rnds2 xmm1, xmm2
; la génération 10 : la fenêtre W[56..59]
db 45 0f 38 cc c1 ; sha256msg1 xmm8, xmm9
movdqa xmm3, xmm7
palignr xmm3, xmm6, 4
paddd xmm8, xmm3
db 44 0f 38 cd c7 ; sha256msg2 xmm8, xmm7
movdqa xmm0, xmm8
paddd xmm0, xmmword ptr [rip + @K56]
db 0f 38 cb d1 ; sha256rnds2 xmm2, xmm1
pshufd xmm0, xmm0, 0x0e
db 0f 38 cb ca ; sha256rnds2 xmm1, xmm2
; la génération 11 : la fenêtre W[60..63]
db 44 0f 38 cc ce ; sha256msg1 xmm9, xmm6
movdqa xmm3, xmm8
palignr xmm3, xmm7, 4
paddd xmm9, xmm3
db 45 0f 38 cd c8 ; sha256msg2 xmm9, xmm8
movdqa xmm0, xmm9
paddd xmm0, xmmword ptr [rip + @K60]
db 0f 38 cb d1 ; sha256rnds2 xmm2, xmm1
pshufd xmm0, xmm0, 0x0e
db 0f 38 cb ca ; sha256rnds2 xmm1, xmm2
; ---- LA SOMMATION : l'état += les variables (FIPS § 6.2.2) ---------------------
movdqa xmm3, xmm1
punpckhqdq xmm3, xmm2
pshufd xmm3, xmm3, 0xb1
paddd xmm3, xmm4
movdqu xmmword ptr [rbp], xmm3
movdqa xmm3, xmm1
punpcklqdq xmm3, xmm2
pshufd xmm3, xmm3, 0xb1
paddd xmm3, xmm5
movdqu xmmword ptr [rbp + 16], xmm3
xor eax, eax
pop rbp
ret
; ---- LE MASQUE (bswap par dword : [3,2,1,0, 7,6,5,4, 11,10,9,8, 15,14,13,12]) ---
; ALIGNÉ 16 (pshufb m128 EXIGE l'alignement — la faute nommée et corrigée)
align 16
db 03 02 01 00 07 06 05 04 0b 0a 09 08 0f 0e 0d 0c
