; libc-08-autotest-r3 · brouillon étiqueté — spec libc-08:R3 (le FICHIER
; CANONIQUE vit à unix/I/), bloc carte f71010. LE RITUEL DE SANTÉ : les 21
; vecteurs dorés dans l'ordre des dépendances (Q1 : zone, memcmp, memcpy,
; strlen, itoa, memset), la ligne unique du patrimoine (Q2 : « TRIADE M1 :
; minilibc N/21 » + « OK »/« KO », terminateur \n du profil), N rendu à
; l'appelant (Q3 frag-con SysV : le principal porte la terminaison).
; Q4 : l'auto-hébergement — le formatage de N par itoa, la longueur par
; strlen, la composition par memcpy, l'émission par écrire.
; D150 (I4) : ce qui TRAVERSE les appels vit en non volatil sauvegardé :
; s0 = N, s7 = le pointeur de travail, s4 = le tampon ligne (l'arène, I5 :
; alloué en phase de verdict, après le vecteur de réinitialisation), s5 =
; la longueur courante. Les volatils ne portent JAMAIS un état d'un appel
; à l'autre ; t1 n'est touché par AUCUN bloc du corpus (fiche § 2).
; Le cadre 0x40 (psABI : AUCUNE zone rouge — les stores vivent DANS le
; cadre alloué) : [0]=ra [8]=s0 [16]=s7 [24]=s4 [32]=s5, la décimale de
; travail (12 o) à sp+0x28, le pad à 16.
@A_ZONE_ALLOC = 0x1200
@A_ZONE_RESET = 0x1280
@A_MEMCMP = 0x10C0
@A_MEMCPY = 0x1080
@A_STRLEN = 0x1140
@A_ITOA = 0x1180
@A_MEMSET = 0x12C0
@A_ECRIRE = 0x1000
@SA = 0x140
@SB = 0x148
@SC = 0x150
@SD = 0x158
@MOTIF16 = 0x160
@SENT16 = 0x170
@MOTIF33 = 0x180
@ZERO16 = 0x1A8
@FF33 = 0x1B8
@S_VIDE = 0x1E0
@S_TRIADE = 0x1E8
@S_33 = 0x1F0
@I0 = 0x218
@IMAX = 0x220
@I123 = 0x230
@I7 = 0x240
@PREFIXE = 0x250
@SLASH = 0x248
@OK = 0x268
@KO = 0x270
addi sp, sp, -0x40
sd ra, 0(sp)
sd s0, 8(sp)
sd s7, 16(sp)
sd s4, 24(sp)
sd s5, 32(sp)
addi s0, zero, 0
; v1 : zone-alloc(16, 8) — pointeur non nul ET aligné 8
addi a0, zero, 0x10
addi a1, zero, 8
jal @A_ZONE_ALLOC
mv s7, a0
beqz a0, .f1
andi t0, a0, 7
bnez t0, .f1
addi s0, s0, 1
.f1:
; v2 : bornes disjointes — le second alloc à au moins 16 du premier
addi a0, zero, 0x10
addi a1, zero, 8
jal @A_ZONE_ALLOC
sub t0, a0, s7
addi t2, zero, 0x10
bltu t0, t2, .f2
addi s0, s0, 1
.f2:
; v3 : réutilisation déterministe après réinitialisation
jal @A_ZONE_RESET
addi a0, zero, 0x10
addi a1, zero, 8
jal @A_ZONE_ALLOC
bne a0, s7, .f3
addi s0, s0, 1
.f3:
; v4 : dépassement (0x7D0 > arène) → 0
addi a0, zero, 0x7D0
addi a1, zero, 8
jal @A_ZONE_ALLOC
bnez a0, .f4
addi s0, s0, 1
.f4:
; v5 : memcmp(SA, SB, 6) == 0 (exemplaires distincts, égaux)
addi a0, s1, @SA
addi a1, s1, @SB
addi a2, zero, 6
jal @A_MEMCMP
bnez a0, .f5
addi s0, s0, 1
.f5:
; v6 : memcmp(SA, SC, 6) == -1 (TRIADE < TRIADF)
addi a0, s1, @SA
addi a1, s1, @SC
addi a2, zero, 6
jal @A_MEMCMP
addi t0, zero, -1
bne a0, t0, .f6
addi s0, s0, 1
.f6:
; v7 : memcmp(SC, SA, 6) == +1 (le miroir exact de v6)
addi a0, s1, @SC
addi a1, s1, @SA
addi a2, zero, 6
jal @A_MEMCMP
addi t0, zero, 1
bne a0, t0, .f7
addi s0, s0, 1
.f7:
; v8 : préfixe — memcmp(SA, SD, 3) == 0
addi a0, s1, @SA
addi a1, s1, @SD
addi a2, zero, 3
jal @A_MEMCMP
bnez a0, .f8
addi s0, s0, 1
.f8:
; v9 : memcpy(alloc16, MOTIF16, 16) relu égal par memcmp
addi a0, zero, 0x10
addi a1, zero, 8
jal @A_ZONE_ALLOC
mv s7, a0
mv a0, s7
addi a1, s1, @MOTIF16
addi a2, zero, 0x10
jal @A_MEMCPY
mv a0, s7
addi a1, s1, @MOTIF16
addi a2, zero, 0x10
jal @A_MEMCMP
bnez a0, .f9
addi s0, s0, 1
.f9:
; v10 : longueur nulle sur sentinelle — le n=0 n'écrit RIEN (I4)
addi a0, zero, 0x10
addi a1, zero, 8
jal @A_ZONE_ALLOC
mv s7, a0
mv a0, s7
addi a1, s1, @SENT16
addi a2, zero, 0x10
jal @A_MEMCPY
mv a0, s7
addi a1, s1, @SENT16
addi a2, zero, 0
jal @A_MEMCPY
mv a0, s7
addi a1, s1, @SENT16
addi a2, zero, 0x10
jal @A_MEMCMP
bnez a0, .f10
addi s0, s0, 1
.f10:
; v11 : memcpy 33 octets
addi a0, zero, 0x30
addi a1, zero, 8
jal @A_ZONE_ALLOC
mv s7, a0
mv a0, s7
addi a1, s1, @MOTIF33
addi a2, zero, 0x21
jal @A_MEMCPY
mv a0, s7
addi a1, s1, @MOTIF33
addi a2, zero, 0x21
jal @A_MEMCMP
bnez a0, .f11
addi s0, s0, 1
.f11:
; v12 : strlen(vide) == 0
addi a0, s1, @S_VIDE
jal @A_STRLEN
bnez a0, .f12
addi s0, s0, 1
.f12:
; v13 : strlen(TRIADE) == 6
addi a0, s1, @S_TRIADE
jal @A_STRLEN
addi t0, zero, 6
bne a0, t0, .f13
addi s0, s0, 1
.f13:
; v14 : strlen(33 lettres) == 33
addi a0, s1, @S_33
jal @A_STRLEN
addi t0, zero, 0x21
bne a0, t0, .f14
addi s0, s0, 1
.f14:
; v15 : itoa(0) == "0"
addi a0, zero, 0
addi a1, sp, 0x28
jal @A_ITOA
addi a0, sp, 0x28
addi a1, s1, @I0
addi a2, zero, 2
jal @A_MEMCMP
bnez a0, .f15
addi s0, s0, 1
.f15:
; v16 : itoa(0xFFFFFFFF) == "4294967295" (-1 : la valeur u32, le masque
; de itoa normalise — le portage du « mov edi, 0xffffffff » x86-64)
addi a0, zero, -1
addi a1, sp, 0x28
jal @A_ITOA
addi a0, sp, 0x28
addi a1, s1, @IMAX
addi a2, zero, 0xB
jal @A_MEMCMP
bnez a0, .f16
addi s0, s0, 1
.f16:
; v17 : itoa(1234567890) == "1234567890" (0x499602D2 — lui+addi, la
; constante du vecteur doré : imm12 ne porte pas 1234567890)
lui a0, 0x49960
addi a0, a0, 0x2d2
addi a1, sp, 0x28
jal @A_ITOA
addi a0, sp, 0x28
addi a1, s1, @I123
addi a2, zero, 0xB
jal @A_MEMCMP
bnez a0, .f17
addi s0, s0, 1
.f17:
; v18 : itoa(7) == "7"
addi a0, zero, 7
addi a1, sp, 0x28
jal @A_ITOA
addi a0, sp, 0x28
addi a1, s1, @I7
addi a2, zero, 2
jal @A_MEMCMP
bnez a0, .f18
addi s0, s0, 1
.f18:
; v19 : memset(alloc16, 0, 16) == ZERO16
addi a0, zero, 0x10
addi a1, zero, 8
jal @A_ZONE_ALLOC
mv s7, a0
mv a0, s7
addi a1, zero, 0
addi a2, zero, 0x10
jal @A_MEMSET
mv a0, s7
addi a1, s1, @ZERO16
addi a2, zero, 0x10
jal @A_MEMCMP
bnez a0, .f19
addi s0, s0, 1
.f19:
; v20 : memset(alloc0x30, 0xFF, 33) == FF33
addi a0, zero, 0x30
addi a1, zero, 8
jal @A_ZONE_ALLOC
mv s7, a0
mv a0, s7
addi a1, zero, 0xFF
addi a2, zero, 0x21
jal @A_MEMSET
mv a0, s7
addi a1, s1, @FF33
addi a2, zero, 0x21
jal @A_MEMCMP
bnez a0, .f20
addi s0, s0, 1
.f20:
; v21 : memset longueur nulle sur sentinelle — le n=0 n'écrit RIEN
addi a0, zero, 0x10
addi a1, zero, 8
jal @A_ZONE_ALLOC
mv s7, a0
mv a0, s7
addi a1, s1, @SENT16
addi a2, zero, 0x10
jal @A_MEMCPY
mv a0, s7
addi a1, zero, 0xFF
addi a2, zero, 0
jal @A_MEMSET
mv a0, s7
addi a1, s1, @SENT16
addi a2, zero, 0x10
jal @A_MEMCMP
bnez a0, .f21
addi s0, s0, 1
.f21:
; — la phase de verdict (I5 : le tampon ligne dans l'arène, APRÈS le
; vecteur de réinitialisation) : « TRIADE M1 : minilibc N/21 OK\n »
addi a0, zero, 0x40
addi a1, zero, 8
jal @A_ZONE_ALLOC
mv s4, a0
addi s5, zero, 0
mv a0, s4
addi a1, s1, @PREFIXE
addi a2, zero, 0x15
jal @A_MEMCPY
addi s5, s5, 0x15
mv a0, s0
addi a1, sp, 0x28
jal @A_ITOA
addi a0, sp, 0x28
jal @A_STRLEN
mv t0, a0
add a0, s4, s5
addi a1, sp, 0x28
mv a2, t0
add s5, s5, t0
jal @A_MEMCPY
add a0, s4, s5
addi a1, s1, @SLASH
addi a2, zero, 1
jal @A_MEMCPY
addi s5, s5, 1
addi a0, zero, 0x15
addi a1, sp, 0x28
jal @A_ITOA
addi a0, sp, 0x28
jal @A_STRLEN
mv t0, a0
add a0, s4, s5
addi a1, sp, 0x28
mv a2, t0
add s5, s5, t0
jal @A_MEMCPY
addi t0, zero, 0x15
bne s0, t0, .ko
add a0, s4, s5
addi a1, s1, @OK
addi a2, zero, 4
jal @A_MEMCPY
addi s5, s5, 4
j .emis
.ko:
add a0, s4, s5
addi a1, s1, @KO
addi a2, zero, 4
jal @A_MEMCPY
addi s5, s5, 4
.emis:
; l'émission unique (Q2) puis N rendu (Q3) — le verdict TOUJOURS rendu
addi a0, zero, 1
mv a1, s4
mv a2, s5
jal @A_ECRIRE
mv a0, s0
ld ra, 0(sp)
ld s0, 8(sp)
ld s7, 16(sp)
ld s4, 24(sp)
ld s5, 32(sp)
addi sp, sp, 0x40
ret
