; tcp-11-journal-v2 · brouillon étiqueté — LE REMPLAÇANT (staging, POUR la
; croissance 0x1D80 — PAS un bloc placé : la spec est tcp-11:R2, la marque
; « j2: » est le seule différence, fiche de la lignée). Assemblé pour
; 0x1D80 : ses décalages internes (B/J, ancre) y sont résolus — la cible du
; patch y sera copiée par tcp-07 au chantier (c).
; La composition porte la marque d'abord (4 octets), le préfixe à +4 :
; running = 4 + longueur du préfixe. Le cadre 0x80 : la ligne (68 o
; disponibles) à sp+0x30, la décimale à sp+0x74, pad — tout dans le cadre.
@A_MEMCPY = 0x1080
@A_ITOA = 0x1180
@A_STRLEN = 0x1140
@A_ECRIRE = 0x1000
@J2_MARK = 0x2B0
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
; — la marque d'abord (le remplaçant se signale)
addi a0, sp, 0x30
addi a1, s1, @J2_MARK
addi a2, zero, 4
jal @A_MEMCPY
; le préfixe à +4
addi a0, sp, 0x34
mv a1, s0
mv a2, s7
jal @A_MEMCPY
addi s7, s7, 4
; le champ numérique ?
slli t0, s4, 32
srli t0, t0, 32
addi t2, zero, -1
srli t2, t2, 32
bne t0, t2, .avec_champ
j .sans_champ
.avec_champ:
mv a0, s4
addi a1, sp, 0x74
jal @A_ITOA
addi a0, sp, 0x74
jal @A_STRLEN
mv t0, a0
addi a0, sp, 0x30
add a0, a0, s7
addi a1, sp, 0x74
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
; — l'émission unique
addi a0, zero, 1
addi a1, sp, 0x30
mv a2, s7
jal @A_ECRIRE
; la restitution du verrou
sd zero, @VERROU_REL(s2)
ld ra, 0(sp)
ld s0, 8(sp)
ld s7, 16(sp)
ld s4, 24(sp)
ld s5, 32(sp)
ld s6, 40(sp)
addi sp, sp, 0x80
ret
