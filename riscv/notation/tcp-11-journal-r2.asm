; tcp-11-journal-r2 · bloc ligne de journal (verrou tournant amoswap.d) · spec tcp-11:R2 · bloc carte f71011
; Profil : riscv64-linux-elf64 · ABI psABI (LP64) · slot RVA 0x1840, taille 512 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/tcp-11-journal-r2.asm
; (outil d'arithmétique d'adresses de l'auteur — l'ASSEMBLEUR MAISON outils/as_rv64.py assemble,
; capstone 5.0.7 juge unique du round-trip, sa graphie est canonique)
; Code : 228 o (57 instructions × 4 o — taille fixe, garde anti-C) · padding : 284 o (NOP canonique addi x0, x0, 0)
; Étiquettes résolues : .avec_champ=0x18a8, .reattendre=0x1870, .sans_champ=0x18d8
; Arithmétique de l'auteur (ancres auipc+addi, décalages B/J relatifs) :
;   0x187c -> .reattendre (0x1870) : décalage -0xc
;   0x188c -> @A_MEMCPY (0x1080) : décalage -0x80c
;   0x18a0 -> .avec_champ (0x18a8) : décalage +0x8
;   0x18a4 -> .sans_champ (0x18d8) : décalage +0x34
;   0x18b0 -> @A_ITOA (0x1180) : décalage -0x730
;   0x18b8 -> @A_STRLEN (0x1140) : décalage -0x778
;   0x18d4 -> @A_MEMCPY (0x1080) : décalage -0x854
;   0x18e8 -> @A_MEMCPY (0x1080) : décalage -0x868
;   0x18fc -> @A_ECRIRE (0x1000) : décalage -0x8fc
; Symboles (vérifiés par build_corpus.py contre layout.py — leçon C1) : @A_ECRIRE=0x1000, @A_ITOA=0x1180, @A_MEMCPY=0x1080, @A_STRLEN=0x1140, @SENTINELLE=0xffffffff, @VERROU_REL=0x400
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
mv a1, s0
mv a2, s7
jal -0x80c
slli t0, s4, 0x20
srli t0, t0, 0x20
addi t2, zero, -1
srli t2, t2, 0x20
bne t0, t2, 8
j 0x34
mv a0, s4
addi a1, sp, 0x70
jal -0x730
addi a0, sp, 0x70
jal -0x778
mv t0, a0
addi a0, sp, 0x30
add a0, a0, s7
addi a1, sp, 0x70
mv a2, t0
add s7, s7, t0
jal -0x854
addi a0, sp, 0x30
add a0, a0, s7
mv a1, s5
mv a2, s6
jal -0x868
add s7, s7, s6
addi a0, zero, 1
addi a1, sp, 0x30
mv a2, s7
jal -0x8fc
sd zero, 0x400(s2)
ld ra, 0(sp)
ld s0, 8(sp)
ld s7, 0x10(sp)
ld s4, 0x18(sp)
ld s5, 0x20(sp)
ld s6, 0x28(sp)
addi sp, sp, 0x80
ret
