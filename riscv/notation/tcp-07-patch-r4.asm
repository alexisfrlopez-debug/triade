; tcp-07-patch-r4 · bloc moteur de patch (mprotect asm-generic 226, fence.i) · spec tcp-07:R4 · bloc carte f71012
; Profil : riscv64-linux-elf64 · ABI psABI (LP64) · slot RVA 0x1a40, taille 512 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/tcp-07-patch-r4.asm
; (outil d'arithmétique d'adresses de l'auteur — l'ASSEMBLEUR MAISON outils/as_rv64.py assemble,
; capstone 5.0.7 juge unique du round-trip, sa graphie est canonique)
; Code : 396 o (99 instructions × 4 o — taille fixe, garde anti-C) · padding : 116 o (NOP canonique addi x0, x0, 0)
; Étiquettes résolues : .applique=0x1a98, .fin=0x1b94, .protger=0x1ba4, .refus1=0x1b68, .refus2=0x1b70, .refus3=0x1b78, .refus4=0x1b80, .refus5=0x1b88, .restauration_echouee=0x1b90, .somme=0x1ab8
; Arithmétique de l'auteur (ancres auipc+addi, décalages B/J relatifs) :
;   0x1a50 -> .refus1 (0x1b68) : décalage +0x118
;   ancre ANCRE_ENTREE @ 0x1a54 : HI=0 (0x0), LO=-532 — 0x1a54 + 0x0*4096 + -532 == 0x1840 (CIBLE_ENTREE)
;   ancre ANCRE_ENTREE : LO=-532 (paire avec l'auipc @ 0x1a54)
;   0x1a5c -> .applique (0x1a98) : décalage +0x3c
;   0x1a64 -> .refus4 (0x1b80) : décalage +0x11c
;   0x1a6c -> .protger (0x1ba4) : décalage +0x138
;   0x1a70 -> .refus5 (0x1b88) : décalage +0x118
;   0x1a84 -> .protger (0x1ba4) : décalage +0x120
;   0x1a8c -> .restauration_echouee (0x1b90) : décalage +0x104
;   0x1a94 -> .fin (0x1b94) : décalage +0x100
;   0x1aa0 -> .refus4 (0x1b80) : décalage +0xe0
;   0x1aa8 -> .refus2 (0x1b70) : décalage +0xc8
;   0x1ac8 -> .somme (0x1ab8) : décalage -0x10
;   0x1ad0 -> .refus3 (0x1b78) : décalage +0xa8
;   0x1ad8 -> .protger (0x1ba4) : décalage +0xcc
;   0x1adc -> .refus5 (0x1b88) : décalage +0xac
;   0x1af4 -> @A_MEMCPY (0x1080) : décalage -0xa74
;   0x1b50 -> .protger (0x1ba4) : décalage +0x54
;   0x1b5c -> .restauration_echouee (0x1b90) : décalage +0x34
;   0x1b64 -> .fin (0x1b94) : décalage +0x30
;   0x1b6c -> .fin (0x1b94) : décalage +0x28
;   0x1b74 -> .fin (0x1b94) : décalage +0x20
;   0x1b7c -> .fin (0x1b94) : décalage +0x18
;   0x1b84 -> .fin (0x1b94) : décalage +0x10
;   0x1b8c -> .fin (0x1b94) : décalage +0x8
; Symboles (vérifiés par build_corpus.py contre layout.py — leçon C1) : @ANCRE_ENTREE=0x1a54, @A_MEMCPY=0x1080, @CROISSANCE_REL=0x540, @ENTREE_SAUVEE_REL=0x410, @ETAT_REL=0x408, @PROT_RWX=0x7, @PROT_RX=0x5, @SOMME_SUM=0x548, @STAGING=0x300, @SYS_MPROTECT=0xe2, @TAILLE_SUM=0x544
addi sp, sp, -0x10
sd ra, 0(sp)
sd s3, 8(sp)
addi t0, zero, 1
bltu t0, a0, 0x118
auipc s3, 0
addi s3, s3, -0x214
beqz a0, 0x3c
ld t0, 0x408(s2)
beqz t0, 0x11c
addi a0, zero, 7
jal 0x138
bltz a0, 0x118
ld t2, 0x410(s2)
sw t2, 0(s3)
fence.i
addi a0, zero, 5
jal 0x120
sd zero, 0x408(s2)
bltz a0, 0x104
mv a0, zero
j 0x100
ld t0, 0x408(s2)
addi t2, zero, 1
beq t0, t2, 0xe0
lw t0, 0x544(s1)
beqz t0, 0xc8
addi t2, s1, 0x300
mv t3, zero
mv t4, zero
add t5, t2, t3
ld t6, 0(t5)
add t4, t4, t6
addi t3, t3, 8
bltu t3, t0, -0x10
ld t6, 0x548(s1)
bne t4, t6, 0xa8
addi a0, zero, 7
jal 0xcc
bltz a0, 0xac
lwu t5, 0(s3)
sd t5, 0x410(s2)
addi a0, s3, 0x540
addi a1, s1, 0x300
lw a2, 0x544(s1)
jal -0xa74
fence rw, rw
addi t2, s3, 0x540
sub t2, t2, s3
srli t3, t2, 1
andi t3, t3, 0x3ff
slli t3, t3, 0x15
srli t4, t2, 0xb
andi t4, t4, 1
slli t4, t4, 0x14
srli t5, t2, 0xc
andi t5, t5, 0xff
slli t5, t5, 0xc
srli t6, t2, 0x14
andi t6, t6, 1
slli t6, t6, 0x1f
or t3, t3, t4
or t3, t3, t5
or t3, t3, t6
ori t3, t3, 0x6f
sw t3, 0(s3)
fence.i
addi a0, zero, 5
jal 0x54
addi t0, zero, 1
sd t0, 0x408(s2)
bltz a0, 0x34
mv a0, zero
j 0x30
addi a0, zero, 1
j 0x28
addi a0, zero, 2
j 0x20
addi a0, zero, 3
j 0x18
addi a0, zero, 4
j 0x10
addi a0, zero, 5
j 8
addi a0, zero, 5
ld ra, 0(sp)
ld s3, 8(sp)
addi sp, sp, 0x10
ret
srli t0, s3, 0xc
slli t0, t0, 0xc
mv t2, a0
mv a0, t0
addi a1, zero, 1
slli a1, a1, 0xc
mv a2, t2
addi a7, zero, 0xe2
ecall
ret
