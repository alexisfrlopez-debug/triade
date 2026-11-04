; sr-04-principal · bloc orchestration sonde · spec sr-04:R1 · bloc carte f70004
; Profil : riscv64-linux-elf64 · ABI psABI (LP64) · slot RVA 0x1140, taille 640 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/sr-04-principal.asm
; (outil d'arithmétique d'adresses de l'auteur — l'ASSEMBLEUR MAISON outils/as_rv64.py assemble,
; capstone 5.0.7 juge unique du round-trip, sa graphie est canonique)
; Code : 372 o (93 instructions × 4 o — taille fixe, garde anti-C) · padding : 268 o (NOP canonique addi x0, x0, 0)
; Étiquettes résolues : .echec=0x11e4, .emit=0x1218, .fatal=0x11fc
; Arithmétique de l'auteur (ancres auipc+addi, décalages B/J relatifs) :
;   ancre ANCRE_BASE @ 0x1140 : HI=-1 (0xfffff), LO=-320 — 0x1140 + -0x1*4096 + -320 == 0x0 (CIBLE_BASE)
;   ancre ANCRE_BASE : LO=-320 (paire avec l'auipc @ 0x1140)
;   ancre ANCRE_BSS @ 0x1148 : HI=1 (0x1), LO=-328 — 0x1148 + 0x1*4096 + -328 == 0x2000 (CIBLE_BSS)
;   ancre ANCRE_BSS : LO=-328 (paire avec l'auipc @ 0x1148)
;   0x1158 -> @A_HEX64 (0x1040) : décalage -0x118
;   0x1168 -> @A_ECRIRE (0x1000) : décalage -0x168
;   0x116c -> .echec (0x11e4) : décalage +0x78
;   0x117c -> @A_ECRIRE (0x1000) : décalage -0x17c
;   0x1180 -> .echec (0x11e4) : décalage +0x64
;   0x1190 -> @A_ECRIRE (0x1000) : décalage -0x190
;   0x1194 -> .echec (0x11e4) : décalage +0x50
;   0x11a4 -> @A_ECRIRE (0x1000) : décalage -0x1a4
;   0x11b0 -> .emit (0x1218) : décalage +0x68
;   0x11c0 -> @A_ECRIRE (0x1000) : décalage -0x1c0
;   0x11cc -> .emit (0x1218) : décalage +0x4c
;   0x11d4 -> .fatal (0x11fc) : décalage +0x28
;   0x11e4 -> @A_VERDICT (0x10c0) : décalage -0x124
;   0x11ec -> .fatal (0x11fc) : décalage +0x10
;   0x1208 -> @A_ECRIRE (0x1000) : décalage -0x208
;   0x122c -> @A_ECRIRE (0x1000) : décalage -0x22c
;   0x1230 -> .echec (0x11e4) : décalage -0x4c
;   0x1238 -> @A_VERDICT (0x10c0) : décalage -0x178
;   0x1244 -> @A_HEX64 (0x1040) : décalage -0x204
;   0x1250 -> @A_HEX64 (0x1040) : décalage -0x210
;   0x1260 -> @A_ECRIRE (0x1000) : décalage -0x260
;   0x1264 -> .echec (0x11e4) : décalage -0x80
;   0x1274 -> @A_ECRIRE (0x1000) : décalage -0x274
;   0x1278 -> .echec (0x11e4) : décalage -0x94
;   0x1288 -> @A_ECRIRE (0x1000) : décalage -0x288
;   0x128c -> .echec (0x11e4) : décalage -0xa8
;   0x129c -> @A_ECRIRE (0x1000) : décalage -0x29c
;   0x12a0 -> .echec (0x11e4) : décalage -0xbc
; Symboles (vérifiés par build_m7.py contre layout.py — leçon C1) : @ANCRE_BASE=0x1140, @ANCRE_BSS=0x1148, @A_ECRIRE=0x1000, @A_HEX64=0x1040, @A_VERDICT=0x10c0, @EXIT_GROUP=0x5e, @L_BASE=0xf, @L_FATAL=0x25, @L_FIN=0x1, @L_P1=0x19, @L_P2=0x1a, @L_VERD=0xb, @MSG_BASE=0x1c0, @MSG_FATAL=0x260, @MSG_FIN=0x240, @MSG_P1=0x1e0, @MSG_P2=0x200, @MSG_VERD=0x220
auipc s1, 0xfffff
addi s1, s1, -0x140
auipc s2, 1
addi s2, s2, -0x148
mv a0, s1
mv a1, s2
jal -0x118
addi a0, zero, 1
addi a1, s1, 0x1c0
addi a2, zero, 0xf
jal -0x168
bltz a0, 0x78
addi a0, zero, 1
mv a1, s2
addi a2, zero, 0x10
jal -0x17c
bltz a0, 0x64
addi a0, zero, 1
addi a1, s1, 0x240
addi a2, zero, 1
jal -0x190
bltz a0, 0x50
addi a0, zero, -1
addi a1, s1, 0x1c0
addi a2, zero, 0xf
jal -0x1a4
addi a1, zero, 0x1e0
addi a2, zero, 0x19
jal 0x68
addi a0, zero, 1
addi a1, zero, 1
addi a2, zero, 0x1a
jal -0x1c0
addi a1, zero, 0x200
addi a2, zero, 0x1a
jal 0x4c
addi t0, zero, 6
beq a0, t0, 0x28
mv a0, zero
addi a7, zero, 0x5e
ecall
jal -0x124
addi t0, zero, 6
beq a0, t0, 0x10
mv a0, zero
addi a7, zero, 0x5e
ecall
addi a0, zero, 1
addi a1, s1, 0x260
addi a2, zero, 0x25
jal -0x208
addi a0, zero, 6
addi a7, zero, 0x5e
ecall
addi sp, sp, -0x10
sd ra, 0(sp)
mv t1, a0
add a1, a1, s1
addi a0, zero, 1
jal -0x22c
bltz a0, -0x4c
mv a0, t1
jal -0x178
sw a0, 0x20(s2)
addi a1, s2, 0x10
jal -0x204
mv a0, t1
mv a1, s2
jal -0x210
addi a0, zero, 1
mv a1, s2
addi a2, zero, 0x10
jal -0x260
bltz a0, -0x80
addi a0, zero, 1
addi a1, s1, 0x220
addi a2, zero, 0xb
jal -0x274
bltz a0, -0x94
addi a0, zero, 1
addi a1, s2, 0x10
addi a2, zero, 0x10
jal -0x288
bltz a0, -0xa8
addi a0, zero, 1
addi a1, s1, 0x240
addi a2, zero, 1
jal -0x29c
bltz a0, -0xbc
lw a0, 0x20(s2)
ld ra, 0(sp)
addi sp, sp, 0x10
ret
