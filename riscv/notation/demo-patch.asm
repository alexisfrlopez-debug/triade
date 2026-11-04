; demo-patch · bloc démonstrateur du patch fence.i — _start (chantier M7-(c)) · spec demo-patch:R1 · bloc carte f72001
; Profil : riscv64-linux-elf64 · ABI psABI (LP64) · slot RVA 0x2000, taille 2048 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/demo-patch.asm
; (outil d'arithmétique d'adresses de l'auteur — l'ASSEMBLEUR MAISON outils/as_rv64.py assemble,
; capstone 5.0.7 juge unique du round-trip, sa graphie est canonique)
; Code : 764 o (191 instructions × 4 o — taille fixe, garde anti-C) · padding : 1284 o (NOP canonique addi x0, x0, 0)
; Étiquettes résolues : .boucle=0x2020, .dire=0x22c0, .echec=0x22a8, .fa_apply=0x2078, .fa_rollback=0x20e8, .fin_trafic=0x213c, .protger_page=0x22e0, .usage=0x2030
; Arithmétique de l'auteur (ancres auipc+addi, décalages B/J relatifs) :
;   ancre ANCRE_D_RODATA @ 0x2000 : HI=-2 (0xffffe), LO=0 — 0x2000 + -0x2*4096 + 0 == 0x0 (CIBLE_D_RODATA)
;   ancre ANCRE_D_RODATA : LO=0 (paire avec l'auipc @ 0x2000)
;   ancre ANCRE_D_BSS @ 0x2008 : HI=1 (0x1), LO=1016 — 0x2008 + 0x1*4096 + 1016 == 0x3400 (CIBLE_D_BSS)
;   ancre ANCRE_D_BSS : LO=1016 (paire avec l'auipc @ 0x2008)
;   ancre ANCRE_D_ENTREE @ 0x2010 : HI=0 (0x0), LO=-2000 — 0x2010 + 0x0*4096 + -2000 == 0x1840 (CIBLE_D_ENTREE)
;   ancre ANCRE_D_ENTREE : LO=-2000 (paire avec l'auipc @ 0x2010)
;   0x2024 -> .fa_apply (0x2078) : décalage +0x54
;   0x202c -> .fa_rollback (0x20e8) : décalage +0xbc
;   0x2038 -> @A_ITOA (0x1180) : décalage -0xeb8
;   0x2040 -> @A_STRLEN (0x1140) : décalage -0xf00
;   0x2060 -> @A_JOURNAL (0x1840) : décalage -0x820
;   0x2064 -> .echec (0x22a8) : décalage +0x244
;   0x2070 -> .boucle (0x2020) : décalage -0x50
;   0x2074 -> .fin_trafic (0x213c) : décalage +0xc8
;   0x207c -> @A_PATCH (0x1a40) : décalage -0x63c
;   0x2080 -> .echec (0x22a8) : décalage +0x228
;   0x208c -> .echec (0x22a8) : décalage +0x21c
;   0x2098 -> .dire (0x22c0) : décalage +0x228
;   0x20a4 -> .echec (0x22a8) : décalage +0x204
;   0x20b0 -> .dire (0x22c0) : décalage +0x210
;   0x20c8 -> @A_JOURNAL (0x1840) : décalage -0x888
;   0x20d0 -> .echec (0x22a8) : décalage +0x1d8
;   0x20dc -> .dire (0x22c0) : décalage +0x1e4
;   0x20e4 -> .usage (0x2030) : décalage -0xb4
;   0x20ec -> @A_PATCH (0x1a40) : décalage -0x6ac
;   0x20f0 -> .echec (0x22a8) : décalage +0x1b8
;   0x20f8 -> .echec (0x22a8) : décalage +0x1b0
;   0x2104 -> .dire (0x22c0) : décalage +0x1bc
;   0x211c -> @A_JOURNAL (0x1840) : décalage -0x8dc
;   0x2124 -> .echec (0x22a8) : décalage +0x184
;   0x2130 -> .dire (0x22c0) : décalage +0x190
;   0x2138 -> .usage (0x2030) : décalage -0x108
;   0x2144 -> .dire (0x22c0) : décalage +0x17c
;   0x2150 -> .echec (0x22a8) : décalage +0x158
;   0x215c -> .dire (0x22c0) : décalage +0x164
;   0x216c -> .echec (0x22a8) : décalage +0x13c
;   0x2178 -> .dire (0x22c0) : décalage +0x148
;   0x2180 -> .echec (0x22a8) : décalage +0x128
;   0x218c -> .dire (0x22c0) : décalage +0x134
;   0x2194 -> @A_PATCH (0x1a40) : décalage -0x754
;   0x219c -> .echec (0x22a8) : décalage +0x10c
;   0x21a4 -> @A_PATCH (0x1a40) : décalage -0x764
;   0x21ac -> .echec (0x22a8) : décalage +0xfc
;   0x21b8 -> .dire (0x22c0) : décalage +0x108
;   0x21c0 -> @A_PATCH (0x1a40) : décalage -0x780
;   0x21c4 -> .echec (0x22a8) : décalage +0xe4
;   0x21cc -> @A_PATCH (0x1a40) : décalage -0x78c
;   0x21d4 -> .echec (0x22a8) : décalage +0xd4
;   0x21dc -> @A_PATCH (0x1a40) : décalage -0x79c
;   0x21e0 -> .echec (0x22a8) : décalage +0xc8
;   0x21e8 -> @A_PATCH (0x1a40) : décalage -0x7a8
;   0x21f0 -> .echec (0x22a8) : décalage +0xb8
;   0x21fc -> .dire (0x22c0) : décalage +0xc4
;   0x2204 -> .protger_page (0x22e0) : décalage +0xdc
;   0x2214 -> .protger_page (0x22e0) : décalage +0xcc
;   0x221c -> @A_PATCH (0x1a40) : décalage -0x7dc
;   0x2224 -> .echec (0x22a8) : décalage +0x84
;   0x222c -> .protger_page (0x22e0) : décalage +0xb4
;   0x2238 -> .protger_page (0x22e0) : décalage +0xa8
;   0x2244 -> .dire (0x22c0) : décalage +0x7c
;   0x224c -> .protger_page (0x22e0) : décalage +0x94
;   0x2260 -> .protger_page (0x22e0) : décalage +0x80
;   0x2268 -> @A_PATCH (0x1a40) : décalage -0x828
;   0x2270 -> .echec (0x22a8) : décalage +0x38
;   0x2278 -> .protger_page (0x22e0) : décalage +0x68
;   0x2284 -> .protger_page (0x22e0) : décalage +0x5c
;   0x2290 -> .dire (0x22c0) : décalage +0x30
;   0x229c -> .dire (0x22c0) : décalage +0x24
;   0x22a4 -> @A_SORTIR (0x1040) : décalage -0x1264
;   0x22b4 -> @A_ECRIRE (0x1000) : décalage -0x12b4
;   0x22bc -> @A_SORTIR (0x1040) : décalage -0x127c
;   0x22cc -> @A_ECRIRE (0x1000) : décalage -0x12cc
;   0x22d8 -> .echec (0x22a8) : décalage -0x30
;   0x22f4 -> .echec (0x22a8) : décalage -0x4c
; Symboles (vérifiés par demo_patch.py contre layout.py — leçon C1) : @ANCRE_D_BSS=0x2008, @ANCRE_D_ENTREE=0x2010, @ANCRE_D_RODATA=0x2000, @A_ECRIRE=0x1000, @A_ITOA=0x1180, @A_JOURNAL=0x1840, @A_PATCH=0x1a40, @A_SORTIR=0x1040, @A_STRLEN=0x1140, @CROISS_REL=0x540, @ETAT_REL=0x408, @LL_APPLY=0x24, @LL_DORM=0x29, @LL_ECHEC=0xc, @LL_EFFET=0x2b, @LL_FIN=0x26, @LL_PTRAFIC=0x32, @LL_REFABS=0x1a, @LL_REFETAT=0x1d, @LL_REFMODE=0x18, @LL_REFSOM=0x19, @LL_REST=0x2b, @LL_ROLLB=0x27, @LL_TRAMP=0x29, @LL_V1=0x2b, @LL_VERROU=0x25, @LNL=0x1, @LTRAFIC=0x7, @LVERDICT=0x7, @L_APPLY=0x594, @L_DORM=0x6c4, @L_ECHEC=0x7b0, @L_EFFET=0x5e4, @L_FIN=0x788, @L_PTRAFIC=0x664, @L_REFABS=0x750, @L_REFETAT=0x730, @L_REFMODE=0x718, @L_REFSOM=0x76c, @L_REST=0x698, @L_ROLLB=0x610, @L_TRAMP=0x5b8, @L_V1=0x638, @L_VERROU=0x6f0, @NL=0x588, @SAUVEE_REL=0x410, @SCRATCH=0x500, @SYS_MPROTECT=0xe2, @TAB_SOMME=0x548, @TAB_TAILLE=0x544, @TRAFIC=0x580, @VERDICT=0x58c, @VERROU_REL=0x400
auipc s1, 0xffffe
mv s1, s1
auipc s2, 1
addi s2, s2, 0x3f8
auipc s9, 0
addi s9, s9, -0x7d0
mv s7, zero
mv s8, zero
addi t0, zero, 0x190
beq s8, t0, 0x54
addi t0, zero, 0x320
beq s8, t0, 0xbc
mv a0, s8
addi a1, s2, 0x500
jal -0xeb8
addi a0, s2, 0x500
jal -0xf00
addi s10, a0, 8
add s10, s10, s7
addi a0, s1, 0x580
addi a1, zero, 7
mv a2, s8
addi a3, s1, 0x588
addi a4, zero, 1
jal -0x820
bne a0, s10, 0x244
addi s8, s8, 1
addi t0, zero, 0x4b0
blt s8, t0, -0x50
j 0xc8
mv a0, zero
jal -0x63c
bnez a0, 0x228
ld t0, 0x408(s2)
addi t4, zero, 1
bne t0, t4, 0x21c
addi a1, s1, 0x594
addi a2, zero, 0x24
jal 0x228
lwu t0, 0(s9)
ld t4, 0x410(s2)
beq t0, t4, 0x204
addi a1, s1, 0x5b8
addi a2, zero, 0x29
jal 0x210
addi a0, s1, 0x58c
addi a1, zero, 7
addi a2, zero, -1
addi a3, s1, 0x588
addi a4, zero, 1
jal -0x888
addi t0, zero, 0xc
bne a0, t0, 0x1d8
addi a1, s1, 0x5e4
addi a2, zero, 0x2b
jal 0x1e4
addi s7, zero, 4
j -0xb4
addi a0, zero, 1
jal -0x6ac
bnez a0, 0x1b8
ld t0, 0x408(s2)
bnez t0, 0x1b0
addi a1, s1, 0x610
addi a2, zero, 0x27
jal 0x1bc
addi a0, s1, 0x58c
addi a1, zero, 7
addi a2, zero, -1
addi a3, s1, 0x588
addi a4, zero, 1
jal -0x8dc
addi t0, zero, 8
bne a0, t0, 0x184
addi a1, s1, 0x638
addi a2, zero, 0x2b
jal 0x190
mv s7, zero
j -0x108
addi a1, s1, 0x664
addi a2, zero, 0x32
jal 0x17c
lwu t0, 0(s9)
ld t4, 0x410(s2)
bne t0, t4, 0x158
addi a1, s1, 0x698
addi a2, zero, 0x2b
jal 0x164
lwu t0, 0x540(s9)
lui t4, 0x100
addi t4, t4, 0x73
beq t0, t4, 0x13c
addi a1, s1, 0x6c4
addi a2, zero, 0x29
jal 0x148
ld t0, 0x400(s2)
bnez t0, 0x128
addi a1, s1, 0x6f0
addi a2, zero, 0x25
jal 0x134
addi a0, zero, 2
jal -0x754
addi t0, zero, 1
bne a0, t0, 0x10c
addi a0, zero, -1
jal -0x764
addi t0, zero, 1
bne a0, t0, 0xfc
addi a1, s1, 0x718
addi a2, zero, 0x18
jal 0x108
mv a0, zero
jal -0x780
bnez a0, 0xe4
mv a0, zero
jal -0x78c
addi t0, zero, 4
bne a0, t0, 0xd4
addi a0, zero, 1
jal -0x79c
bnez a0, 0xc8
addi a0, zero, 1
jal -0x7a8
addi t0, zero, 4
bne a0, t0, 0xb8
addi a1, s1, 0x730
addi a2, zero, 0x1d
jal 0xc4
addi a2, zero, 3
jal 0xdc
lwu s11, 0x544(s1)
sw zero, 0x544(s1)
addi a2, zero, 1
jal 0xcc
mv a0, zero
jal -0x7dc
addi t0, zero, 2
bne a0, t0, 0x84
addi a2, zero, 3
jal 0xb4
sw s11, 0x544(s1)
addi a2, zero, 1
jal 0xa8
addi a1, s1, 0x750
addi a2, zero, 0x1a
jal 0x7c
addi a2, zero, 3
jal 0x94
ld s5, 0x548(s1)
addi t0, s5, 1
sd t0, 0x548(s1)
addi a2, zero, 1
jal 0x80
mv a0, zero
jal -0x828
addi t0, zero, 3
bne a0, t0, 0x38
addi a2, zero, 3
jal 0x68
sd s5, 0x548(s1)
addi a2, zero, 1
jal 0x5c
addi a1, s1, 0x76c
addi a2, zero, 0x19
jal 0x30
addi a1, s1, 0x788
addi a2, zero, 0x26
jal 0x24
mv a0, zero
jal -0x1264
addi a0, zero, 1
addi a1, s1, 0x7b0
addi a2, zero, 0xc
jal -0x12b4
addi a0, zero, 1
jal -0x127c
addi sp, sp, -0x10
sd ra, 0(sp)
addi a0, zero, 1
jal -0x12cc
ld ra, 0(sp)
addi sp, sp, 0x10
bltz a0, -0x30
ret
mv a0, s1
addi a1, zero, 1
slli a1, a1, 0xc
addi a7, zero, 0xe2
ecall
bltz a0, -0x4c
ret
