; tcp-11-journal-r2 · brouillon étiqueté — spec tcp-11:R2 (le FICHIER
; CANONIQUE vit à unix/I/), bloc carte f71011. LA LIGNE DE JOURNAL sous
; verrou : la composition dans le cadre privé (I2 : AUCUNE allocation
; d'arène — pile privée), UNE seule écriture de la composition exacte
; (Q1), le verdict BRUT du service propagé (Q2), le verrou pris puis rendu
; SUR TOUT CHEMIN (Q3 — l'échec d'écriture ne laisse JAMAIS le verrou pris).
; Les CINQ arguments en registres (I4 : l'ABI psABI porte cinq arguments
; sans pile — l'instance Windows loge le 5e en pile) : a0 préfixe, a1
; longueur, a2 valeur (sentinelle 0xFFFFFFFF = pas de champ), a3 suffixe,
; a4 longueur du suffixe.
; LE VERROU DU PROFIL (I1) : le qword du plan, atomique amoswap.d (l'extension
; A — le portage RV64 du lock xchg), attente passive PAR LA BOUCLE (le
; profil n'a pas d'instruction pause — la réessai est l'attente), jamais de
; service système ; la restitution est un sd simple (comme le mov simple de
; l'instance x86-64 — le corpus est mono-fil, fiche § 5).
; D150 : ce qui traverse les appels vit en non volatil sauvegardé :
; s0 = préfixe, s7 = longueur courante, s4 = valeur, s5 = suffixe,
; s6 = longueur du suffixe. t1 : jamais touché (fiche § 2).
; Le cadre 0x80 : [0]=ra [8]=s0 [16]=s7 [24]=s4 [32]=s5 [40]=s6, la ligne
; (64 o) à sp+0x30, la décimale de travail (12 o) à sp+0x70, pad —
; TOUT dans le cadre alloué (psABI : AUCUNE zone rouge).
@A_MEMCPY = 0x1080
@A_ITOA = 0x1180
@A_STRLEN = 0x1140
@A_ECRIRE = 0x1000
@VERROU_REL = 0x400
@SENTINELLE = 0xFFFFFFFF
addi sp, sp, -0x80
sd ra, 0(sp)
sd s0, 8(sp)
sd s7, 16(sp)
sd s4, 24(sp)
sd s5, 32(sp)
sd s6, 40(sp)
mv s0, a0
mv s7, a1
mv s4, a2
mv s5, a3
mv s6, a4
.reattendre:
addi t0, zero, 1
addi t2, s2, @VERROU_REL
amoswap.d t3, t0, (t2)
bnez t3, .reattendre
; — la composition (la ligne à sp+0x30, dans le cadre)
addi a0, sp, 0x30
mv a1, s0
mv a2, s7
jal @A_MEMCPY
; le champ numérique ? (le sentinelle u32 — masqué puis confronté)
slli t0, s4, 32
srli t0, t0, 32
addi t2, zero, -1
srli t2, t2, 32
bne t0, t2, .avec_champ
j .sans_champ
.avec_champ:
mv a0, s4
addi a1, sp, 0x70
jal @A_ITOA
addi a0, sp, 0x70
jal @A_STRLEN
mv t0, a0
addi a0, sp, 0x30
add a0, a0, s7
addi a1, sp, 0x70
mv a2, t0
add s7, s7, t0
jal @A_MEMCPY
.sans_champ:
; le suffixe
addi a0, sp, 0x30
add a0, a0, s7
mv a1, s5
mv a2, s6
jal @A_MEMCPY
add s7, s7, s6
; — l'émission UNIQUE (Q1) : fd 1, la ligne, la longueur totale
addi a0, zero, 1
addi a1, sp, 0x30
mv a2, s7
jal @A_ECRIRE
; la restitution du verrou (Q3 : après l'écriture, sur tout chemin —
; le verdict brut dans a0 traverse le sd et l'épilogue)
sd zero, @VERROU_REL(s2)
ld ra, 0(sp)
ld s0, 8(sp)
ld s7, 16(sp)
ld s4, 24(sp)
ld s5, 32(sp)
ld s6, 40(sp)
addi sp, sp, 0x80
ret
