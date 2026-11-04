; libc-08-autotest-r3 · bloc auto-test de la mini-libc (21 vecteurs dorés) · spec libc-08:R3 · bloc carte f71010
; Profil : riscv64-linux-elf64 · ABI psABI (LP64) · slot RVA 0x1340, taille 1280 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/libc-08-autotest-r3.asm
; (outil d'arithmétique d'adresses de l'auteur — l'ASSEMBLEUR MAISON outils/as_rv64.py assemble,
; capstone 5.0.7 juge unique du round-trip, sa graphie est canonique)
; Code : 1056 o (264 instructions × 4 o — taille fixe, garde anti-C) · padding : 224 o (NOP canonique addi x0, x0, 0)
; Étiquettes résolues : .emis=0x1730, .f1=0x137c, .f10=0x14ac, .f11=0x14e4, .f12=0x14f4, .f13=0x1508, .f14=0x151c, .f15=0x1540, .f16=0x1564, .f17=0x158c, .f18=0x15b0, .f19=0x15e8, .f2=0x1398, .f20=0x1620, .f21=0x1668, .f3=0x13b0, .f4=0x13c4, .f5=0x13dc, .f6=0x13f8, .f7=0x1414, .f8=0x142c, .f9=0x1464, .ko=0x171c
; Arithmétique de l'auteur (ancres auipc+addi, décalages B/J relatifs) :
;   0x1364 -> @A_ZONE_ALLOC (0x1200) : décalage -0x164
;   0x136c -> .f1 (0x137c) : décalage +0x10
;   0x1374 -> .f1 (0x137c) : décalage +0x8
;   0x1384 -> @A_ZONE_ALLOC (0x1200) : décalage -0x184
;   0x1390 -> .f2 (0x1398) : décalage +0x8
;   0x1398 -> @A_ZONE_RESET (0x1280) : décalage -0x118
;   0x13a4 -> @A_ZONE_ALLOC (0x1200) : décalage -0x1a4
;   0x13a8 -> .f3 (0x13b0) : décalage +0x8
;   0x13b8 -> @A_ZONE_ALLOC (0x1200) : décalage -0x1b8
;   0x13bc -> .f4 (0x13c4) : décalage +0x8
;   0x13d0 -> @A_MEMCMP (0x10c0) : décalage -0x310
;   0x13d4 -> .f5 (0x13dc) : décalage +0x8
;   0x13e8 -> @A_MEMCMP (0x10c0) : décalage -0x328
;   0x13f0 -> .f6 (0x13f8) : décalage +0x8
;   0x1404 -> @A_MEMCMP (0x10c0) : décalage -0x344
;   0x140c -> .f7 (0x1414) : décalage +0x8
;   0x1420 -> @A_MEMCMP (0x10c0) : décalage -0x360
;   0x1424 -> .f8 (0x142c) : décalage +0x8
;   0x1434 -> @A_ZONE_ALLOC (0x1200) : décalage -0x234
;   0x1448 -> @A_MEMCPY (0x1080) : décalage -0x3c8
;   0x1458 -> @A_MEMCMP (0x10c0) : décalage -0x398
;   0x145c -> .f9 (0x1464) : décalage +0x8
;   0x146c -> @A_ZONE_ALLOC (0x1200) : décalage -0x26c
;   0x1480 -> @A_MEMCPY (0x1080) : décalage -0x400
;   0x1490 -> @A_MEMCPY (0x1080) : décalage -0x410
;   0x14a0 -> @A_MEMCMP (0x10c0) : décalage -0x3e0
;   0x14a4 -> .f10 (0x14ac) : décalage +0x8
;   0x14b4 -> @A_ZONE_ALLOC (0x1200) : décalage -0x2b4
;   0x14c8 -> @A_MEMCPY (0x1080) : décalage -0x448
;   0x14d8 -> @A_MEMCMP (0x10c0) : décalage -0x418
;   0x14dc -> .f11 (0x14e4) : décalage +0x8
;   0x14e8 -> @A_STRLEN (0x1140) : décalage -0x3a8
;   0x14ec -> .f12 (0x14f4) : décalage +0x8
;   0x14f8 -> @A_STRLEN (0x1140) : décalage -0x3b8
;   0x1500 -> .f13 (0x1508) : décalage +0x8
;   0x150c -> @A_STRLEN (0x1140) : décalage -0x3cc
;   0x1514 -> .f14 (0x151c) : décalage +0x8
;   0x1524 -> @A_ITOA (0x1180) : décalage -0x3a4
;   0x1534 -> @A_MEMCMP (0x10c0) : décalage -0x474
;   0x1538 -> .f15 (0x1540) : décalage +0x8
;   0x1548 -> @A_ITOA (0x1180) : décalage -0x3c8
;   0x1558 -> @A_MEMCMP (0x10c0) : décalage -0x498
;   0x155c -> .f16 (0x1564) : décalage +0x8
;   0x1570 -> @A_ITOA (0x1180) : décalage -0x3f0
;   0x1580 -> @A_MEMCMP (0x10c0) : décalage -0x4c0
;   0x1584 -> .f17 (0x158c) : décalage +0x8
;   0x1594 -> @A_ITOA (0x1180) : décalage -0x414
;   0x15a4 -> @A_MEMCMP (0x10c0) : décalage -0x4e4
;   0x15a8 -> .f18 (0x15b0) : décalage +0x8
;   0x15b8 -> @A_ZONE_ALLOC (0x1200) : décalage -0x3b8
;   0x15cc -> @A_MEMSET (0x12c0) : décalage -0x30c
;   0x15dc -> @A_MEMCMP (0x10c0) : décalage -0x51c
;   0x15e0 -> .f19 (0x15e8) : décalage +0x8
;   0x15f0 -> @A_ZONE_ALLOC (0x1200) : décalage -0x3f0
;   0x1604 -> @A_MEMSET (0x12c0) : décalage -0x344
;   0x1614 -> @A_MEMCMP (0x10c0) : décalage -0x554
;   0x1618 -> .f20 (0x1620) : décalage +0x8
;   0x1628 -> @A_ZONE_ALLOC (0x1200) : décalage -0x428
;   0x163c -> @A_MEMCPY (0x1080) : décalage -0x5bc
;   0x164c -> @A_MEMSET (0x12c0) : décalage -0x38c
;   0x165c -> @A_MEMCMP (0x10c0) : décalage -0x59c
;   0x1660 -> .f21 (0x1668) : décalage +0x8
;   0x1670 -> @A_ZONE_ALLOC (0x1200) : décalage -0x470
;   0x1688 -> @A_MEMCPY (0x1080) : décalage -0x608
;   0x1698 -> @A_ITOA (0x1180) : décalage -0x518
;   0x16a0 -> @A_STRLEN (0x1140) : décalage -0x560
;   0x16b8 -> @A_MEMCPY (0x1080) : décalage -0x638
;   0x16c8 -> @A_MEMCPY (0x1080) : décalage -0x648
;   0x16d8 -> @A_ITOA (0x1180) : décalage -0x558
;   0x16e0 -> @A_STRLEN (0x1140) : décalage -0x5a0
;   0x16f8 -> @A_MEMCPY (0x1080) : décalage -0x678
;   0x1700 -> .ko (0x171c) : décalage +0x1c
;   0x1710 -> @A_MEMCPY (0x1080) : décalage -0x690
;   0x1718 -> .emis (0x1730) : décalage +0x18
;   0x1728 -> @A_MEMCPY (0x1080) : décalage -0x6a8
;   0x173c -> @A_ECRIRE (0x1000) : décalage -0x73c
; Symboles (vérifiés par build_corpus.py contre layout.py — leçon C1) : @A_ECRIRE=0x1000, @A_ITOA=0x1180, @A_MEMCMP=0x10c0, @A_MEMCPY=0x1080, @A_MEMSET=0x12c0, @A_STRLEN=0x1140, @A_ZONE_ALLOC=0x1200, @A_ZONE_RESET=0x1280, @FF33=0x1b8, @I0=0x218, @I123=0x230, @I7=0x240, @IMAX=0x220, @KO=0x270, @MOTIF16=0x160, @MOTIF33=0x180, @OK=0x268, @PREFIXE=0x250, @SA=0x140, @SB=0x148, @SC=0x150, @SD=0x158, @SENT16=0x170, @SLASH=0x248, @S_33=0x1f0, @S_TRIADE=0x1e8, @S_VIDE=0x1e0, @ZERO16=0x1a8
addi sp, sp, -0x40
sd ra, 0(sp)
sd s0, 8(sp)
sd s7, 0x10(sp)
sd s4, 0x18(sp)
sd s5, 0x20(sp)
mv s0, zero
addi a0, zero, 0x10
addi a1, zero, 8
jal -0x164
mv s7, a0
beqz a0, 0x10
andi t0, a0, 7
bnez t0, 8
addi s0, s0, 1
addi a0, zero, 0x10
addi a1, zero, 8
jal -0x184
sub t0, a0, s7
addi t2, zero, 0x10
bltu t0, t2, 8
addi s0, s0, 1
jal -0x118
addi a0, zero, 0x10
addi a1, zero, 8
jal -0x1a4
bne a0, s7, 8
addi s0, s0, 1
addi a0, zero, 0x7d0
addi a1, zero, 8
jal -0x1b8
bnez a0, 8
addi s0, s0, 1
addi a0, s1, 0x140
addi a1, s1, 0x148
addi a2, zero, 6
jal -0x310
bnez a0, 8
addi s0, s0, 1
addi a0, s1, 0x140
addi a1, s1, 0x150
addi a2, zero, 6
jal -0x328
addi t0, zero, -1
bne a0, t0, 8
addi s0, s0, 1
addi a0, s1, 0x150
addi a1, s1, 0x140
addi a2, zero, 6
jal -0x344
addi t0, zero, 1
bne a0, t0, 8
addi s0, s0, 1
addi a0, s1, 0x140
addi a1, s1, 0x158
addi a2, zero, 3
jal -0x360
bnez a0, 8
addi s0, s0, 1
addi a0, zero, 0x10
addi a1, zero, 8
jal -0x234
mv s7, a0
mv a0, s7
addi a1, s1, 0x160
addi a2, zero, 0x10
jal -0x3c8
mv a0, s7
addi a1, s1, 0x160
addi a2, zero, 0x10
jal -0x398
bnez a0, 8
addi s0, s0, 1
addi a0, zero, 0x10
addi a1, zero, 8
jal -0x26c
mv s7, a0
mv a0, s7
addi a1, s1, 0x170
addi a2, zero, 0x10
jal -0x400
mv a0, s7
addi a1, s1, 0x170
mv a2, zero
jal -0x410
mv a0, s7
addi a1, s1, 0x170
addi a2, zero, 0x10
jal -0x3e0
bnez a0, 8
addi s0, s0, 1
addi a0, zero, 0x30
addi a1, zero, 8
jal -0x2b4
mv s7, a0
mv a0, s7
addi a1, s1, 0x180
addi a2, zero, 0x21
jal -0x448
mv a0, s7
addi a1, s1, 0x180
addi a2, zero, 0x21
jal -0x418
bnez a0, 8
addi s0, s0, 1
addi a0, s1, 0x1e0
jal -0x3a8
bnez a0, 8
addi s0, s0, 1
addi a0, s1, 0x1e8
jal -0x3b8
addi t0, zero, 6
bne a0, t0, 8
addi s0, s0, 1
addi a0, s1, 0x1f0
jal -0x3cc
addi t0, zero, 0x21
bne a0, t0, 8
addi s0, s0, 1
mv a0, zero
addi a1, sp, 0x28
jal -0x3a4
addi a0, sp, 0x28
addi a1, s1, 0x218
addi a2, zero, 2
jal -0x474
bnez a0, 8
addi s0, s0, 1
addi a0, zero, -1
addi a1, sp, 0x28
jal -0x3c8
addi a0, sp, 0x28
addi a1, s1, 0x220
addi a2, zero, 0xb
jal -0x498
bnez a0, 8
addi s0, s0, 1
lui a0, 0x49960
addi a0, a0, 0x2d2
addi a1, sp, 0x28
jal -0x3f0
addi a0, sp, 0x28
addi a1, s1, 0x230
addi a2, zero, 0xb
jal -0x4c0
bnez a0, 8
addi s0, s0, 1
addi a0, zero, 7
addi a1, sp, 0x28
jal -0x414
addi a0, sp, 0x28
addi a1, s1, 0x240
addi a2, zero, 2
jal -0x4e4
bnez a0, 8
addi s0, s0, 1
addi a0, zero, 0x10
addi a1, zero, 8
jal -0x3b8
mv s7, a0
mv a0, s7
mv a1, zero
addi a2, zero, 0x10
jal -0x30c
mv a0, s7
addi a1, s1, 0x1a8
addi a2, zero, 0x10
jal -0x51c
bnez a0, 8
addi s0, s0, 1
addi a0, zero, 0x30
addi a1, zero, 8
jal -0x3f0
mv s7, a0
mv a0, s7
addi a1, zero, 0xff
addi a2, zero, 0x21
jal -0x344
mv a0, s7
addi a1, s1, 0x1b8
addi a2, zero, 0x21
jal -0x554
bnez a0, 8
addi s0, s0, 1
addi a0, zero, 0x10
addi a1, zero, 8
jal -0x428
mv s7, a0
mv a0, s7
addi a1, s1, 0x170
addi a2, zero, 0x10
jal -0x5bc
mv a0, s7
addi a1, zero, 0xff
mv a2, zero
jal -0x38c
mv a0, s7
addi a1, s1, 0x170
addi a2, zero, 0x10
jal -0x59c
bnez a0, 8
addi s0, s0, 1
addi a0, zero, 0x40
addi a1, zero, 8
jal -0x470
mv s4, a0
mv s5, zero
mv a0, s4
addi a1, s1, 0x250
addi a2, zero, 0x15
jal -0x608
addi s5, s5, 0x15
mv a0, s0
addi a1, sp, 0x28
jal -0x518
addi a0, sp, 0x28
jal -0x560
mv t0, a0
add a0, s4, s5
addi a1, sp, 0x28
mv a2, t0
add s5, s5, t0
jal -0x638
add a0, s4, s5
addi a1, s1, 0x248
addi a2, zero, 1
jal -0x648
addi s5, s5, 1
addi a0, zero, 0x15
addi a1, sp, 0x28
jal -0x558
addi a0, sp, 0x28
jal -0x5a0
mv t0, a0
add a0, s4, s5
addi a1, sp, 0x28
mv a2, t0
add s5, s5, t0
jal -0x678
addi t0, zero, 0x15
bne s0, t0, 0x1c
add a0, s4, s5
addi a1, s1, 0x268
addi a2, zero, 4
jal -0x690
addi s5, s5, 4
j 0x18
add a0, s4, s5
addi a1, s1, 0x270
addi a2, zero, 4
jal -0x6a8
addi s5, s5, 4
addi a0, zero, 1
mv a1, s4
mv a2, s5
jal -0x73c
mv a0, s0
ld ra, 0(sp)
ld s0, 8(sp)
ld s7, 0x10(sp)
ld s4, 0x18(sp)
ld s5, 0x20(sp)
addi sp, sp, 0x40
ret
