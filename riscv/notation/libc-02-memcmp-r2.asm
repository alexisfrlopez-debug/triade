; libc-02-memcmp-r2 · bloc comparaison mémoire normalisée · spec libc-02:R2 · bloc carte f71004
; Profil : riscv64-linux-elf64 · ABI psABI (LP64) · slot RVA 0x10c0, taille 128 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/libc-02-memcmp-r2.asm
; (outil d'arithmétique d'adresses de l'auteur — l'ASSEMBLEUR MAISON outils/as_rv64.py assemble,
; capstone 5.0.7 juge unique du round-trip, sa graphie est canonique)
; Code : 60 o (15 instructions × 4 o — taille fixe, garde anti-C) · padding : 68 o (NOP canonique addi x0, x0, 0)
; Étiquettes résolues : .avance=0x10e4, .boucle=0x10c0, .moins=0x10dc, .zero=0x10f4
; Arithmétique de l'auteur (ancres auipc+addi, décalages B/J relatifs) :
;   0x10c0 -> .zero (0x10f4) : décalage +0x34
;   0x10cc -> .moins (0x10dc) : décalage +0x10
;   0x10d0 -> .avance (0x10e4) : décalage +0x14
;   0x10f0 -> .boucle (0x10c0) : décalage -0x30
beqz a2, 0x34
lbu t2, 0(a0)
lbu t3, 0(a1)
bltu t2, t3, 0x10
beq t2, t3, 0x14
addi a0, zero, 1
ret
addi a0, zero, -1
ret
addi a0, a0, 1
addi a1, a1, 1
addi a2, a2, -1
j -0x30
mv a0, zero
ret
