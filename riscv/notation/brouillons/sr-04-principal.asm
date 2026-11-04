; sr-04-principal · brouillon étiqueté — spec sr-04:R1, bloc carte f70004
; _start (e_entry 0x1140, RELATIF à la base — ET_DYN/PIE) : [sp] = argc…,
; sp ≡ 0 mod 16, AUCUN registre garanti à l'entrée (ra non initialisé —
; le corps ne touche JAMAIS sp ; jal ne pousse rien, le lien vit dans ra).
; LES DEUX ANCRES (le portage RV64 du lea rip lié-temps soustrait) :
;   paire 1 @ 0x1140 : auipc s1, HI ; addi s1, s1, LO → s1 = base
;     (CIBLE 0x0 — l'ancre traversante des .rodata, non-volatil psABI,
;      le portage de rbx ; les déplacements imm12 atteignent 0x140-0x2xx) ;
;   paire 2 @ 0x1148 : auipc s2, HI ; addi s2, s2, LO → s2 = base + 0x2000
;     (la FENÊTRE .bss — le tampon vit au-delà de portée imm12 depuis la
;      base : l'ancre le porte ; déplacements relatifs 0/+16/+32).
; t1 = registre de travail interne du projet (fiche § 2 — le portage de
; r10/r11) : porte le a0 brut à travers sr-02/sr-03 (qui le respectent par
; contrat). Le sous-programme local .emit (déclaré I1) émet la ligne d'une
; sonde et rend le verdict : entrée a0 = résultat brut, a1 = RVA du
; préfixe, a2 = longueur, s1/s2 = ancres ; a1/a2 sont consommés AVANT le
; premier jal (ils meurent au premier) ; le verdict vit au tampon [s2+32]
; (la mémoire traverse les appels et les syscalls — les volatils non) ;
; le cadre de .emit SAUVE ra (jal écrase le lien — call poussait, jal ne
; pousse pas) : addi sp,sp,-16 ; sd ra,0(sp) … ld ra,0(sp) ; addi sp,sp,16
; — appariés, sp ≡ 0 mod 16 en tous points d'appel psABI.
; émissions vérifiées (I6) : a0 < 0 → .echec (canal de constat atteint) ;
; sondes volontaires NON vérifiées sur place : leur a0 négatif est le
; PAYLOAD, il passe par .emit → sr-03 (jamais au hasard).
; syscalls : exit_group ASM-GENERIC (94 — PAS 231 : garde anti-table-x86),
; trois sites (nominal 0, canal-mort 0, fatal 6) ; les write passent TOUS
; par sr-01.
@A_ECRIRE = 0x1000
@A_HEX64 = 0x1040
@A_VERDICT = 0x10C0
@MSG_BASE = 0x1C0
@L_BASE = 15
@MSG_P1 = 0x1E0
@L_P1 = 25
@MSG_P2 = 0x200
@L_P2 = 26
@MSG_VERD = 0x220
@L_VERD = 11
@MSG_FIN = 0x240
@L_FIN = 1
@MSG_FATAL = 0x260
@L_FATAL = 37
@ANCRE_BASE = 0x1140
@ANCRE_BSS = 0x1148
@EXIT_GROUP = 94
auipc s1, @ANCRE_BASE_HI
addi s1, s1, @ANCRE_BASE_LO
auipc s2, @ANCRE_BSS_HI
addi s2, s2, @ANCRE_BSS_LO
addi a0, s1, 0
addi a1, s2, 0
jal @A_HEX64
addi a0, zero, 1
addi a1, s1, @MSG_BASE
addi a2, zero, @L_BASE
jal @A_ECRIRE
bltz a0, .echec
addi a0, zero, 1
addi a1, s2, 0
addi a2, zero, 16
jal @A_ECRIRE
bltz a0, .echec
addi a0, zero, 1
addi a1, s1, @MSG_FIN
addi a2, zero, @L_FIN
jal @A_ECRIRE
bltz a0, .echec
addi a0, zero, -1
addi a1, s1, @MSG_BASE
addi a2, zero, @L_BASE
jal @A_ECRIRE
addi a1, zero, @MSG_P1
addi a2, zero, @L_P1
jal .emit
addi a0, zero, 1
addi a1, zero, 1
addi a2, zero, @L_P2
jal @A_ECRIRE
addi a1, zero, @MSG_P2
addi a2, zero, @L_P2
jal .emit
addi t0, zero, 6
beq a0, t0, .fatal
addi a0, zero, 0
addi a7, zero, @EXIT_GROUP
ecall
.echec:
jal @A_VERDICT
addi t0, zero, 6
beq a0, t0, .fatal
addi a0, zero, 0
addi a7, zero, @EXIT_GROUP
ecall
.fatal:
addi a0, zero, 1
addi a1, s1, @MSG_FATAL
addi a2, zero, @L_FATAL
jal @A_ECRIRE
addi a0, zero, 6
addi a7, zero, @EXIT_GROUP
ecall
.emit:
addi sp, sp, -16
sd ra, 0(sp)
addi t1, a0, 0
add a1, a1, s1
addi a0, zero, 1
jal @A_ECRIRE
bltz a0, .echec
addi a0, t1, 0
jal @A_VERDICT
sw a0, 32(s2)
addi a1, s2, 16
jal @A_HEX64
addi a0, t1, 0
addi a1, s2, 0
jal @A_HEX64
addi a0, zero, 1
addi a1, s2, 0
addi a2, zero, 16
jal @A_ECRIRE
bltz a0, .echec
addi a0, zero, 1
addi a1, s1, @MSG_VERD
addi a2, zero, @L_VERD
jal @A_ECRIRE
bltz a0, .echec
addi a0, zero, 1
addi a1, s2, 16
addi a2, zero, 16
jal @A_ECRIRE
bltz a0, .echec
addi a0, zero, 1
addi a1, s1, @MSG_FIN
addi a2, zero, @L_FIN
jal @A_ECRIRE
bltz a0, .echec
lw a0, 32(s2)
ld ra, 0(sp)
addi sp, sp, 16
ret
