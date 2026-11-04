; sr-03-verdict · bloc verdict d'erreur syscall · spec sr-03:R1 · bloc carte f70003
; Profil : riscv64-linux-elf64 · ABI psABI (LP64) · slot RVA 0x10c0, taille 128 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/sr-03-verdict.asm
; (outil d'arithmétique d'adresses de l'auteur — l'ASSEMBLEUR MAISON outils/as_rv64.py assemble,
; capstone 5.0.7 juge unique du round-trip, sa graphie est canonique)
; Code : 52 o (13 instructions × 4 o — taille fixe, garde anti-C) · padding : 76 o (NOP canonique addi x0, x0, 0)
; Étiquettes résolues : .boucle=0x10cc, .fatal=0x10ec, .trouve=0x10e4
; Arithmétique de l'auteur (ancres auipc+addi, décalages B/J relatifs) :
;   0x10cc -> .fatal (0x10ec) : décalage +0x20
;   0x10d4 -> .trouve (0x10e4) : décalage +0x10
;   0x10e0 -> .boucle (0x10cc) : décalage -0x14
; Symboles (vérifiés par build_m7.py contre layout.py — leçon C1) : @ENTREES=0x144, @ERRNOS=0x140
neg a0, a0
lw t0, 0x140(s1)
addi t4, s1, 0x144
beqz t0, 0x20
lw t2, 0(t4)
beq t2, a0, 0x10
addi t4, t4, 8
addi t0, t0, -1
j -0x14
lw a0, 4(t4)
ret
addi a0, zero, 6
ret
