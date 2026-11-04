; libc-07-memset-r2 · bloc remplissage mémoire · spec libc-07:R2 · bloc carte f71009
; Profil : riscv64-linux-elf64 · ABI psABI (LP64) · slot RVA 0x12c0, taille 128 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/libc-07-memset-r2.asm
; (outil d'arithmétique d'adresses de l'auteur — l'ASSEMBLEUR MAISON outils/as_rv64.py assemble,
; capstone 5.0.7 juge unique du round-trip, sa graphie est canonique)
; Code : 28 o (7 instructions × 4 o — taille fixe, garde anti-C) · padding : 100 o (NOP canonique addi x0, x0, 0)
; Étiquettes résolues : .boucle=0x12c4, .fin=0x12d8
; Arithmétique de l'auteur (ancres auipc+addi, décalages B/J relatifs) :
;   0x12c4 -> .fin (0x12d8) : décalage +0x14
;   0x12d4 -> .boucle (0x12c4) : décalage -0x10
mv t0, a0
beqz a2, 0x14
sb a1, 0(t0)
addi t0, t0, 1
addi a2, a2, -1
j -0x10
ret
