; demo-patch · brouillon étiqueté — LE DÉMONSTRATEUR du chantier M7-(c) :
; LA SÉQUENCE scratch+fence.i DÉMONTRÉE EN EXÉCUTION sous qemu, la bascule
; PENDANT le trafic (le modèle unix/demo_patch.py, porté en INVITÉ — sous
; qemu-user le scénario vit DANS l'invité : le démonstrateur est _start).
; LE CONTRAT (écrit-avant-code ; l'instrument du chantier, pas un artefact
; de la lignée — le modèle demo_patch.py du jalon M6, jamais une carte) :
;   (a) LE TRAFIC EN SESSION : 1 200 usages de l'ENTRÉE du journal (0x1840,
;       la CIBLE du patch) ; l'apply ENTRE les usages 399 et 400, le rollback
;       entre 799 et 800 ; le verdict de CHAQUE usage contrôlé SUR PLACE
;       (la longueur rendue == 8 + len(itoa(i)) + la marque) ; JAMAIS une
;       interruption — l'usage suit la bascule sans la voir ;
;   (b) L'EFFET AU GESTE MÊME : sous v2 l'entrée appelée rend « j2: verdict »
;       (12 o — LE PATCH EST EFFECTIF), au retour la ligne sans marque (8 o) ;
;       la bascule du mot d'entrée constatée (le mot != l'original sauvegardé) ;
;   (c) LE RETOUR À L'ÉTAT IMAGE : l'entrée revenue à l'octet près (==
;       ENTREE_SAUVEE), le remplaçant DORMANT (la croissance ≠ la réserve
;       ebreak), le verrou rendu un-pour-un ;
;   (d) LES REFUS NOMMÉS : mode invalide 1 (2 et -1), états incohérents 4
;       (apply x2, rollback x2), staging absent 2 et somme divergente 3 —
;       les DEUX DERNIERS par mutation IN-GUEST de la table R10 : le
;       démonstrateur OUVRE la page R par mprotect (LE MÊME SERVICE que le
;       bloc — page sans code, RW sans bit X : D39 ne s'y applique pas),
;       mute, REFERME, éprouve, RESTAURE — chaque geste nommé ;
;   FRONTIÈRES NOMMÉES : code 5 (le service refuse) n'est pas productible
;       sous qemu-user de façon naturelle (l'hôte accorde RWX sur mapping
;       privé) — la branche vit fail-closed dans le bloc (bltz → refus5) ;
;       la concurrence réelle est HORS périmètre (fiche § 5 : le corpus M7
;       est mono-fil, portée de fence.i = le cœur courant) ; le DEP falsifié
;       (0x7→0x3) est une épreuve HOST-SIDE (le mutant du FICHIER, un run
;       séparé — SIGSEGV attendu) ; la FLUX-cohérence octet pour octet est
;       constatée par l'ORACLE host-side (la transcription EST la pièce —
;       il n'y a AUCUN détournement de canal, D153 ne s'applique pas : la
;       narration et les émissions vivent sur le MÊME flux, la pièce entière).
; LES FENÊTRES (le modèle sr-04, la leçon imm12 D156) : s1 = base+0 (les
;       chaînes + la table R10), s2 = base+0x3400 (la fenêtre .bss CENTRALE
;       — état +0x408, sauvegarde +0x410, verrou +0x400, scratch +0x500),
;       s9 = base+0x1840 (l'INSPECTION — l'entrée à +0, la croissance à
;       +0x540). s3 demeure à tcp-07 SEUL (D156 : dédié par rôle) ; t4
;       n'est touché par AUCUN bloc (fiche § 2).
; LES REGISTRES DU DÉMONSTRATEUR (D150 — l'état traverse en non volatil ;
;       les blocs appelés sauvegardent et restaurent les leurs) : s7 = le
;       drapeau v2 (0 = v1, 4 = la marque — le drapeau PORTE la longueur,
;       l'attendu = 8 + t + s7), s8 = i (le compteur du trafic), s11/s5 =
;       les sauvegardes de la table (taille/somme) pour les refus.
; _start (e_entry 0x2000, RELATIF — ET_DYN/PIE) : sp ≡ 0 mod 16 à l'entrée
;       (qemu aligne) ; le corps ne touche JAMAIS sp, AUCUN cadre (toute la
;       vie dans les non volatils — le scratch itoa vit en .bss) ; la pile
;       des appelés descend SOUS sp, jamais au-dessus (psABI : AUCUNE zone
;       rouge) ; la terminaison par sortir (jamais de ret — le rituel ne
;       revient pas).
@A_ECRIRE = 0x1000
@A_SORTIR = 0x1040
@A_STRLEN = 0x1140
@A_ITOA = 0x1180
@A_JOURNAL = 0x1840
@A_PATCH = 0x1A40
@SYS_MPROTECT = 226
@TRAFIC = 0x580
@LTRAFIC = 7
@NL = 0x588
@LNL = 1
@VERDICT = 0x58C
@LVERDICT = 7
@L_APPLY = 0x594
@LL_APPLY = 36
@L_TRAMP = 0x5B8
@LL_TRAMP = 41
@L_EFFET = 0x5E4
@LL_EFFET = 43
@L_ROLLB = 0x610
@LL_ROLLB = 39
@L_V1 = 0x638
@LL_V1 = 43
@L_PTRAFIC = 0x664
@LL_PTRAFIC = 50
@L_REST = 0x698
@LL_REST = 43
@L_DORM = 0x6C4
@LL_DORM = 41
@L_VERROU = 0x6F0
@LL_VERROU = 37
@L_REFMODE = 0x718
@LL_REFMODE = 24
@L_REFETAT = 0x730
@LL_REFETAT = 29
@L_REFABS = 0x750
@LL_REFABS = 26
@L_REFSOM = 0x76C
@LL_REFSOM = 25
@L_FIN = 0x788
@LL_FIN = 38
@L_ECHEC = 0x7B0
@LL_ECHEC = 12
@TAB_TAILLE = 0x544
@TAB_SOMME = 0x548
@VERROU_REL = 0x400
@ETAT_REL = 0x408
@SAUVEE_REL = 0x410
@SCRATCH = 0x500
@CROISS_REL = 0x540
@ANCRE_D_RODATA = 0x2000
@ANCRE_D_BSS = 0x2008
@ANCRE_D_ENTREE = 0x2010
auipc s1, @ANCRE_D_RODATA_HI
addi s1, s1, @ANCRE_D_RODATA_LO
auipc s2, @ANCRE_D_BSS_HI
addi s2, s2, @ANCRE_D_BSS_LO
auipc s9, @ANCRE_D_ENTREE_HI
addi s9, s9, @ANCRE_D_ENTREE_LO
addi s7, zero, 0
addi s8, zero, 0
.boucle:
addi t0, zero, 400
beq s8, t0, .fa_apply
addi t0, zero, 800
beq s8, t0, .fa_rollback
.usage:
mv a0, s8
addi a1, s2, @SCRATCH
jal @A_ITOA
addi a0, s2, @SCRATCH
jal @A_STRLEN
addi s10, a0, 8
add s10, s10, s7
addi a0, s1, @TRAFIC
addi a1, zero, @LTRAFIC
mv a2, s8
addi a3, s1, @NL
addi a4, zero, @LNL
jal @A_JOURNAL
bne a0, s10, .echec
addi s8, s8, 1
addi t0, zero, 1200
blt s8, t0, .boucle
j .fin_trafic
.fa_apply:
addi a0, zero, 0
jal @A_PATCH
bnez a0, .echec
ld t0, @ETAT_REL(s2)
addi t4, zero, 1
bne t0, t4, .echec
addi a1, s1, @L_APPLY
addi a2, zero, @LL_APPLY
jal .dire
lwu t0, 0(s9)
ld t4, @SAUVEE_REL(s2)
beq t0, t4, .echec
addi a1, s1, @L_TRAMP
addi a2, zero, @LL_TRAMP
jal .dire
addi a0, s1, @VERDICT
addi a1, zero, @LVERDICT
addi a2, zero, -1
addi a3, s1, @NL
addi a4, zero, @LNL
jal @A_JOURNAL
addi t0, zero, 12
bne a0, t0, .echec
addi a1, s1, @L_EFFET
addi a2, zero, @LL_EFFET
jal .dire
addi s7, zero, 4
j .usage
.fa_rollback:
addi a0, zero, 1
jal @A_PATCH
bnez a0, .echec
ld t0, @ETAT_REL(s2)
bnez t0, .echec
addi a1, s1, @L_ROLLB
addi a2, zero, @LL_ROLLB
jal .dire
addi a0, s1, @VERDICT
addi a1, zero, @LVERDICT
addi a2, zero, -1
addi a3, s1, @NL
addi a4, zero, @LNL
jal @A_JOURNAL
addi t0, zero, 8
bne a0, t0, .echec
addi a1, s1, @L_V1
addi a2, zero, @LL_V1
jal .dire
addi s7, zero, 0
j .usage
.fin_trafic:
addi a1, s1, @L_PTRAFIC
addi a2, zero, @LL_PTRAFIC
jal .dire
lwu t0, 0(s9)
ld t4, @SAUVEE_REL(s2)
bne t0, t4, .echec
addi a1, s1, @L_REST
addi a2, zero, @LL_REST
jal .dire
lwu t0, @CROISS_REL(s9)
lui t4, 0x100
addi t4, t4, 0x73
beq t0, t4, .echec
addi a1, s1, @L_DORM
addi a2, zero, @LL_DORM
jal .dire
ld t0, @VERROU_REL(s2)
bnez t0, .echec
addi a1, s1, @L_VERROU
addi a2, zero, @LL_VERROU
jal .dire
addi a0, zero, 2
jal @A_PATCH
addi t0, zero, 1
bne a0, t0, .echec
addi a0, zero, -1
jal @A_PATCH
addi t0, zero, 1
bne a0, t0, .echec
addi a1, s1, @L_REFMODE
addi a2, zero, @LL_REFMODE
jal .dire
addi a0, zero, 0
jal @A_PATCH
bnez a0, .echec
addi a0, zero, 0
jal @A_PATCH
addi t0, zero, 4
bne a0, t0, .echec
addi a0, zero, 1
jal @A_PATCH
bnez a0, .echec
addi a0, zero, 1
jal @A_PATCH
addi t0, zero, 4
bne a0, t0, .echec
addi a1, s1, @L_REFETAT
addi a2, zero, @LL_REFETAT
jal .dire
addi a2, zero, 3
jal .protger_page
lwu s11, @TAB_TAILLE(s1)
sw zero, @TAB_TAILLE(s1)
addi a2, zero, 1
jal .protger_page
addi a0, zero, 0
jal @A_PATCH
addi t0, zero, 2
bne a0, t0, .echec
addi a2, zero, 3
jal .protger_page
sw s11, @TAB_TAILLE(s1)
addi a2, zero, 1
jal .protger_page
addi a1, s1, @L_REFABS
addi a2, zero, @LL_REFABS
jal .dire
addi a2, zero, 3
jal .protger_page
ld s5, @TAB_SOMME(s1)
addi t0, s5, 1
sd t0, @TAB_SOMME(s1)
addi a2, zero, 1
jal .protger_page
addi a0, zero, 0
jal @A_PATCH
addi t0, zero, 3
bne a0, t0, .echec
addi a2, zero, 3
jal .protger_page
sd s5, @TAB_SOMME(s1)
addi a2, zero, 1
jal .protger_page
addi a1, s1, @L_REFSOM
addi a2, zero, @LL_REFSOM
jal .dire
addi a1, s1, @L_FIN
addi a2, zero, @LL_FIN
jal .dire
addi a0, zero, 0
jal @A_SORTIR
.echec:
addi a0, zero, 1
addi a1, s1, @L_ECHEC
addi a2, zero, @LL_ECHEC
jal @A_ECRIRE
addi a0, zero, 1
jal @A_SORTIR
.dire:
addi sp, sp, -16
sd ra, 0(sp)
addi a0, zero, 1
jal @A_ECRIRE
ld ra, 0(sp)
addi sp, sp, 16
bltz a0, .echec
ret
.protger_page:
mv a0, s1
addi a1, zero, 1
slli a1, a1, 12
addi a7, zero, @SYS_MPROTECT
ecall
bltz a0, .echec
ret
