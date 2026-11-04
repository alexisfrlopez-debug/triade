; libc-06-zone-reset-r2 · bloc réinitialisation de zone · spec libc-06:R2 · bloc carte f71008
; Profil : riscv64-linux-elf64 · ABI psABI (LP64) · slot RVA 0x1280, taille 64 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/libc-06-zone-reset-r2.asm
; (outil d'arithmétique d'adresses de l'auteur — l'ASSEMBLEUR MAISON outils/as_rv64.py assemble,
; capstone 5.0.7 juge unique du round-trip, sa graphie est canonique)
; Code : 8 o (2 instructions × 4 o — taille fixe, garde anti-C) · padding : 56 o (NOP canonique addi x0, x0, 0)
; Symboles (vérifiés par build_corpus.py contre layout.py — leçon C1) : @CURSEUR_REL=-0x400
sd zero, -0x400(s2)
ret
