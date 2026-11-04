; hello-03-sortir-r2 · bloc terminaison (interface du corpus) · spec hello-03:R2 · bloc carte f71002
; Profil : riscv64-linux-elf64 · ABI psABI (LP64) · slot RVA 0x1040, taille 64 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/hello-03-sortir-r2.asm
; (outil d'arithmétique d'adresses de l'auteur — l'ASSEMBLEUR MAISON outils/as_rv64.py assemble,
; capstone 5.0.7 juge unique du round-trip, sa graphie est canonique)
; Code : 12 o (3 instructions × 4 o — taille fixe, garde anti-C) · padding : 52 o (NOP canonique addi x0, x0, 0)
; Symboles (vérifiés par build_corpus.py contre layout.py — leçon C1) : @SYS_EXIT_GROUP=0x5e
addi a7, zero, 0x5e
ecall
ebreak
