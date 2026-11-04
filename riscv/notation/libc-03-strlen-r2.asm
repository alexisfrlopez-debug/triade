; libc-03-strlen-r2 · bloc longueur de chaîne · spec libc-03:R2 · bloc carte f71005
; Profil : riscv64-linux-elf64 · ABI psABI (LP64) · slot RVA 0x1140, taille 64 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/libc-03-strlen-r2.asm
; (outil d'arithmétique d'adresses de l'auteur — l'ASSEMBLEUR MAISON outils/as_rv64.py assemble,
; capstone 5.0.7 juge unique du round-trip, sa graphie est canonique)
; Code : 28 o (7 instructions × 4 o — taille fixe, garde anti-C) · padding : 36 o (NOP canonique addi x0, x0, 0)
; Étiquettes résolues : .boucle=0x1144, .fin=0x1154
; Arithmétique de l'auteur (ancres auipc+addi, décalages B/J relatifs) :
;   0x1148 -> .fin (0x1154) : décalage +0xc
;   0x1150 -> .boucle (0x1144) : décalage -0xc
mv t0, a0
lbu t2, 0(t0)
beqz t2, 0xc
addi t0, t0, 1
j -0xc
sub a0, t0, a0
ret
