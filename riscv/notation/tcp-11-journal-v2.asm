; tcp-11-journal-v2 · bloc journal v2 — le remplaçant (staging, POUR la croissance) · spec tcp-11:R2-v2 · bloc carte f71991
; Profil : riscv64-linux-elf64 · ABI psABI (LP64) · slot RVA 0x1d80, taille 640 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/tcp-11-journal-v2.asm
; (outil d'arithmétique d'adresses de l'auteur — l'ASSEMBLEUR MAISON outils/as_rv64.py assemble,
; capstone 5.0.7 juge unique du round-trip, sa graphie est canonique)
; Code : 248 o (62 instructions × 4 o — taille fixe, garde anti-C) · padding : 392 o (NOP canonique addi x0, x0, 0)
; Étiquettes résolues : .avec_champ=0x1dfc, .reattendre=0x1db0, .sans_champ=0x1e2c
; Arithmétique de l'auteur (ancres auipc+addi, décalages B/J relatifs) :
;   0x1dbc -> .reattendre (0x1db0) : décalage -0xc
;   0x1dcc -> @A_MEMCPY (0x1080) : décalage -0xd4c
;   0x1ddc -> @A_MEMCPY (0x1080) : décalage -0xd5c
;   0x1df4 -> .avec_champ (0x1dfc) : décalage +0x8
;   0x1df8 -> .sans_champ (0x1e2c) : décalage +0x34
;   0x1e04 -> @A_ITOA (0x1180) : décalage -0xc84
;   0x1e0c -> @A_STRLEN (0x1140) : décalage -0xccc
;   0x1e28 -> @A_MEMCPY (0x1080) : décalage -0xda8
;   0x1e3c -> @A_MEMCPY (0x1080) : décalage -0xdbc
;   0x1e50 -> @A_ECRIRE (0x1000) : décalage -0xe50
; Symboles (vérifiés par build_corpus.py contre layout.py — leçon C1) : @A_ECRIRE=0x1000, @A_ITOA=0x1180, @A_MEMCPY=0x1080, @A_STRLEN=0x1140, @J2_MARK=0x2b0, @SENTINELLE=0xffffffff, @VERROU_REL=0x400
addi sp, sp, -0x80
sd ra, 0(sp)
sd s0, 8(sp)
sd s7, 0x10(sp)
sd s4, 0x18(sp)
sd s5, 0x20(sp)
sd s6, 0x28(sp)
mv s0, a0
mv s7, a1
mv s4, a2
mv s5, a3
mv s6, a4
addi t0, zero, 1
addi t2, s2, 0x400
amoswap.d t3, t0, (t2)
bnez t3, -0xc
addi a0, sp, 0x30
addi a1, s1, 0x2b0
addi a2, zero, 4
jal -0xd4c
addi a0, sp, 0x34
mv a1, s0
mv a2, s7
jal -0xd5c
addi s7, s7, 4
slli t0, s4, 0x20
srli t0, t0, 0x20
addi t2, zero, -1
srli t2, t2, 0x20
bne t0, t2, 8
j 0x34
mv a0, s4
addi a1, sp, 0x74
jal -0xc84
addi a0, sp, 0x74
jal -0xccc
mv t0, a0
addi a0, sp, 0x30
add a0, a0, s7
addi a1, sp, 0x74
mv a2, t0
add s7, s7, t0
jal -0xda8
addi a0, sp, 0x30
add a0, a0, s7
mv a1, s5
mv a2, s6
jal -0xdbc
add s7, s7, s6
addi a0, zero, 1
addi a1, sp, 0x30
mv a2, s7
jal -0xe50
sd zero, 0x400(s2)
ld ra, 0(sp)
ld s0, 8(sp)
ld s7, 0x10(sp)
ld s4, 0x18(sp)
ld s5, 0x20(sp)
ld s6, 0x28(sp)
addi sp, sp, 0x80
ret
