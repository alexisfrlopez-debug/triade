; sr-01-ecrire · bloc écriture par appel système · spec sr-01:R1 · bloc carte f70001
; Profil : riscv64-linux-elf64 · ABI psABI (LP64) · slot RVA 0x1000, taille 64 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/sr-01-ecrire.asm
; (outil d'arithmétique d'adresses de l'auteur — l'ASSEMBLEUR MAISON outils/as_rv64.py assemble,
; capstone 5.0.7 juge unique du round-trip, sa graphie est canonique)
; Code : 12 o (3 instructions × 4 o — taille fixe, garde anti-C) · padding : 52 o (NOP canonique addi x0, x0, 0)
; Symboles (vérifiés par build_m7.py contre layout.py — leçon C1) : @SYS_WRITE=0x40
addi a7, zero, 0x40
ecall
ret
