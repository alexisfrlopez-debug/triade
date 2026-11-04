; hello-02-ecrire-r2 · bloc écriture du flux (interface du corpus) · spec hello-02:R2 · bloc carte f71001
; Profil : riscv64-linux-elf64 · ABI psABI (LP64) · slot RVA 0x1000, taille 64 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/hello-02-ecrire-r2.asm
; (outil d'arithmétique d'adresses de l'auteur — l'ASSEMBLEUR MAISON outils/as_rv64.py assemble,
; capstone 5.0.7 juge unique du round-trip, sa graphie est canonique)
; Code : 12 o (3 instructions × 4 o — taille fixe, garde anti-C) · padding : 52 o (NOP canonique addi x0, x0, 0)
; Symboles (vérifiés par build_corpus.py contre layout.py — leçon C1) : @SYS_WRITE=0x40
addi a7, zero, 0x40
ecall
ret
