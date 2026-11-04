; sr-02-hex64 · bloc formatage hexadécimal u64 · spec sr-02:R1 · bloc carte f70002
; Profil : riscv64-linux-elf64 · ABI psABI (LP64) · slot RVA 0x1040, taille 128 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/sr-02-hex64.asm
; (outil d'arithmétique d'adresses de l'auteur — l'ASSEMBLEUR MAISON outils/as_rv64.py assemble,
; capstone 5.0.7 juge unique du round-trip, sa graphie est canonique)
; Code : 44 o (11 instructions × 4 o — taille fixe, garde anti-C) · padding : 84 o (NOP canonique addi x0, x0, 0)
; Étiquettes résolues : .boucle=0x1048
; Arithmétique de l'auteur (ancres auipc+addi, décalages B/J relatifs) :
;   0x1064 -> .boucle (0x1048) : décalage -0x1c
; Symboles (vérifiés par build_m7.py contre layout.py — leçon C1) : @HEXCHARS=0x180
addi t0, zero, 0x3c
addi t4, s1, 0x180
srl t3, a0, t0
andi t3, t3, 0xf
add t3, t3, t4
lbu t3, 0(t3)
sb t3, 0(a1)
addi a1, a1, 1
addi t0, t0, -4
bgez t0, -0x1c
ret
