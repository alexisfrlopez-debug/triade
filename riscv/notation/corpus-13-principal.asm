; corpus-13-principal · bloc orchestration du corpus paritaire — _start · spec corpus-13:R1 · bloc carte f71013
; Profil : riscv64-linux-elf64 · ABI psABI (LP64) · slot RVA 0x1c40, taille 320 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/corpus-13-principal.asm
; (outil d'arithmétique d'adresses de l'auteur — l'ASSEMBLEUR MAISON outils/as_rv64.py assemble,
; capstone 5.0.7 juge unique du round-trip, sa graphie est canonique)
; Code : 72 o (18 instructions × 4 o — taille fixe, garde anti-C) · padding : 248 o (NOP canonique addi x0, x0, 0)
; Étiquettes résolues : .fin=0x1c84, .ko=0x1c80
; Arithmétique de l'auteur (ancres auipc+addi, décalages B/J relatifs) :
;   ancre ANCRE_RODATA @ 0x1c40 : HI=-2 (0xffffe), LO=960 — 0x1c40 + -0x2*4096 + 960 == 0x0 (CIBLE_RODATA)
;   ancre ANCRE_RODATA : LO=960 (paire avec l'auipc @ 0x1c40)
;   ancre ANCRE_BSS_CORPUS @ 0x1c48 : HI=1 (0x1), LO=1976 — 0x1c48 + 0x1*4096 + 1976 == 0x3400 (CIBLE_BSS_CORPUS)
;   ancre ANCRE_BSS_CORPUS : LO=1976 (paire avec l'auipc @ 0x1c48)
;   0x1c50 -> @A_AUTOTEST (0x1340) : décalage -0x910
;   0x1c6c -> @A_JOURNAL (0x1840) : décalage -0x42c
;   0x1c74 -> .ko (0x1c80) : décalage +0xc
;   0x1c7c -> .fin (0x1c84) : décalage +0x8
;   0x1c84 -> @A_SORTIR (0x1040) : décalage -0xc44
; Symboles (vérifiés par build_corpus.py contre layout.py — leçon C1) : @ANCRE_BSS_CORPUS=0x1c48, @ANCRE_RODATA=0x1c40, @A_AUTOTEST=0x1340, @A_JOURNAL=0x1840, @A_SORTIR=0x1040, @J_PREF=0x280, @J_SUFF=0x2a0, @L_PREF=0x12, @L_SUFF=0xa
auipc s1, 0xffffe
addi s1, s1, 0x3c0
auipc s2, 1
addi s2, s2, 0x7b8
jal -0x910
mv s0, a0
addi a0, s1, 0x280
addi a1, zero, 0x12
mv a2, s0
addi a3, s1, 0x2a0
addi a4, zero, 0xa
jal -0x42c
addi t0, zero, 0x15
bne s0, t0, 0xc
mv a0, zero
j 8
addi a0, zero, 1
jal -0xc44
