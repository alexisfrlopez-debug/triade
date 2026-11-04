; libc-01-memcpy-r2 · bloc copie mémoire · spec libc-01:R2 · bloc carte f71003
; Profil : riscv64-linux-elf64 · ABI psABI (LP64) · slot RVA 0x1080, taille 64 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/libc-01-memcpy-r2.asm
; (outil d'arithmétique d'adresses de l'auteur — l'ASSEMBLEUR MAISON outils/as_rv64.py assemble,
; capstone 5.0.7 juge unique du round-trip, sa graphie est canonique)
; Code : 32 o (8 instructions × 4 o — taille fixe, garde anti-C) · padding : 32 o (NOP canonique addi x0, x0, 0)
; Étiquettes résolues : .boucle=0x1080, .fin=0x109c
; Arithmétique de l'auteur (ancres auipc+addi, décalages B/J relatifs) :
;   0x1080 -> .fin (0x109c) : décalage +0x1c
;   0x1098 -> .boucle (0x1080) : décalage -0x18
beqz a2, 0x1c
lbu t3, 0(a1)
sb t3, 0(a0)
addi a1, a1, 1
addi a0, a0, 1
addi a2, a2, -1
j -0x18
ret
