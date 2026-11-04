; libc-04-itoa-r3 · bloc conversion décimale u32 · spec libc-04:R3 · bloc carte f71006
; Profil : riscv64-linux-elf64 · ABI psABI (LP64) · slot RVA 0x1180, taille 128 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/libc-04-itoa-r3.asm
; (outil d'arithmétique d'adresses de l'auteur — l'ASSEMBLEUR MAISON outils/as_rv64.py assemble,
; capstone 5.0.7 juge unique du round-trip, sa graphie est canonique)
; Code : 80 o (20 instructions × 4 o — taille fixe, garde anti-C) · padding : 48 o (NOP canonique addi x0, x0, 0)
; Étiquettes résolues : .compacte=0x11b0, .fin=0x11c8, .genere=0x1194
; Arithmétique de l'auteur (ancres auipc+addi, décalages B/J relatifs) :
;   0x11a8 -> .genere (0x1194) : décalage -0x14
;   0x11b8 -> .fin (0x11c8) : décalage +0x10
;   0x11c4 -> .compacte (0x11b0) : décalage -0x14
slli t0, a0, 0x20
srli t0, t0, 0x20
addi t2, a1, 0xb
addi t4, zero, 0xa
sb zero, 0(t2)
remu t3, t0, t4
divu t0, t0, t4
addi t3, t3, 0x30
addi t2, t2, -1
sb t3, 0(t2)
bnez t0, -0x14
mv t5, a1
lbu t3, 0(t2)
sb t3, 0(t5)
beqz t3, 0x10
addi t2, t2, 1
addi t5, t5, 1
j -0x14
mv a0, a1
ret
