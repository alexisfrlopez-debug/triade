; libc-05-zone-alloc-r2 · bloc allocateur par zone · spec libc-05:R2 · bloc carte f71007
; Profil : riscv64-linux-elf64 · ABI psABI (LP64) · slot RVA 0x1200, taille 128 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/libc-05-zone-alloc-r2.asm
; (outil d'arithmétique d'adresses de l'auteur — l'ASSEMBLEUR MAISON outils/as_rv64.py assemble,
; capstone 5.0.7 juge unique du round-trip, sa graphie est canonique)
; Code : 84 o (21 instructions × 4 o — taille fixe, garde anti-C) · padding : 44 o (NOP canonique addi x0, x0, 0)
; Étiquettes résolues : .echec=0x124c
; Arithmétique de l'auteur (ancres auipc+addi, décalages B/J relatifs) :
;   0x1204 -> .echec (0x124c) : décalage +0x48
;   0x1208 -> .echec (0x124c) : décalage +0x44
;   0x1214 -> .echec (0x124c) : décalage +0x38
;   0x121c -> .echec (0x124c) : décalage +0x30
;   0x1238 -> .echec (0x124c) : décalage +0x14
; Symboles (vérifiés par build_corpus.py contre layout.py — leçon C1) : @ARENE_REL=-0x3c0, @ARENE_TAILLE=0x7c0, @CURSEUR_REL=-0x400
addi t3, zero, 0x7c0
bltu t3, a0, 0x48
beqz a1, 0x44
addi t4, a1, -1
and t5, t4, a1
bnez t5, 0x38
addi t3, zero, 0x40
bltu t3, a1, 0x30
ld t0, -0x400(s2)
add t2, t0, t4
not t6, t4
and t2, t2, t6
add t5, t2, a0
addi t3, zero, 0x7c0
bltu t3, t5, 0x14
sd t5, -0x400(s2)
addi a0, s2, -0x3c0
add a0, a0, t2
ret
mv a0, zero
ret
