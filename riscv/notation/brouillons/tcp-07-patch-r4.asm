; tcp-07-patch-r4 · brouillon étiqueté — spec tcp-07:R4 (le FICHIER CANONIQUE
; vit à unix/I/), bloc carte f71012. LE MOTEUR DE PATCH du corpus RV64 :
; la CIBLE est l'entrée du journal (tcp-11 @ 0x1840 — le plan du corpus),
; le remplaçant dort au staging (.rodata), la croissance 0x1D80 l'accueillera.
; LA SÉQUENCE DU PROFIL (fiche § 5) : mprotect RW (le bit exécution RETENU,
; D39/I6 : 0x7 jamais 0x3) → la copie staging→croissance → fence rw, rw →
; LA BASCULE (UN mot aligné — jal x0 vers la croissance, ATOMIQUE, construit
; en registres I3 : jamais une constante d'image) → fence.i (l'invalidation
; du cache d'instructions du cœur courant — la séquence multi-cœur est hors
; périmètre, la frontière est nommée fiche § 5) → mprotect RX.
; Les SIX refus nommés (Q5) : 1 mode invalide, 2 staging absent (taille 0),
; 3 somme divergente (R10 : la porte AVANT tout effet), 4 état incohérent,
; 5 le service de protection a refusé (avant l'écriture pour l'ouverture,
; après la bascule pour la refermeture — Q6 : la bascule est effective,
; l'état mis à jour, retour 5).
; LA FENÊTRE s3 = base + 0x1840 (l'entrée du journal — SA paire à LUI, au
; site 0x1A48) : la croissance = s3 + 0x540, la page = s3 & ~0xFFF (l'entrée
; et la croissance vivent la MÊME page 0x1000 — la page protégée contient le
; présent bloc lui-même, D39/R6). Le rollback restaure le mot original
; (ENTREE_SAUVEE, le qword du plan) et referme ; la croissance n'est PAS
; effacée (Q2 : le remplaçant y dort, réactivable).
; Le sous-programme local .protger (déclaré I1) : a0 = protection demandée
; → a0 = le verdict BRUT du service (0 ou -errno) ; la page de 0x1000 octets
; ne passe pas par imm12 (4096 > 2047) : addi 1 puis slli 12 ; le numéro
; 226 asm-generic (10 est le numéro x86-64 : REFUSÉ nommément, la garde).
@A_MEMCPY = 0x1080
@STAGING = 0x300
@TAILLE_SUM = 0x544
@SOMME_SUM = 0x548
@ETAT_REL = 0x408
@ENTREE_SAUVEE_REL = 0x410
@CROISSANCE_REL = 0x540
@SYS_MPROTECT = 226
@PROT_RWX = 7
@PROT_RX = 5
@ANCRE_ENTREE = 0x1A54
addi sp, sp, -16
sd ra, 0(sp)
sd s3, 8(sp)
addi t0, zero, 1
bltu t0, a0, .refus1
auipc s3, @ANCRE_ENTREE_HI
addi s3, s3, @ANCRE_ENTREE_LO
beqz a0, .applique
; — retour arrière (mode 1)
ld t0, @ETAT_REL(s2)
beqz t0, .refus4
addi a0, zero, @PROT_RWX
jal .protger
bltz a0, .refus5
ld t2, @ENTREE_SAUVEE_REL(s2)
sw t2, 0(s3)
fence.i
addi a0, zero, @PROT_RX
jal .protger
sd zero, @ETAT_REL(s2)
bltz a0, .restauration_echouee
addi a0, zero, 0
j .fin
.applique:
ld t0, @ETAT_REL(s2)
addi t2, zero, 1
beq t0, t2, .refus4
lw t0, @TAILLE_SUM(s1)
beqz t0, .refus2
; la porte R10 : la somme AVANT tout effet
addi t2, s1, @STAGING
addi t3, zero, 0
addi t4, zero, 0
.somme:
add t5, t2, t3
ld t6, 0(t5)
add t4, t4, t6
addi t3, t3, 8
bltu t3, t0, .somme
ld t6, @SOMME_SUM(s1)
bne t4, t6, .refus3
; ouvrir la page (RWX — D39 : jamais 0x3)
addi a0, zero, @PROT_RWX
jal .protger
bltz a0, .refus5
; l'original sauvé AVANT toute écriture (le mot d'entrée, zéro-étendu)
lwu t5, 0(s3)
sd t5, @ENTREE_SAUVEE_REL(s2)
; la copie staging → croissance
addi a0, s3, @CROISSANCE_REL
addi a1, s1, @STAGING
lw a2, @TAILLE_SUM(s1)
jal @A_MEMCPY
fence rw, rw
; la bascule : jal x0, croissance — CONSTRUIT EN REGISTRES (I3) depuis les
; adresses VIVANTES (le décalage = croissance - entrée, recalculé ici) ;
; J-type : imm[20]|imm[10:1]|imm[11]|imm[19:12]|rd=x0|opcode 0x6F
addi t2, s3, @CROISSANCE_REL
sub t2, t2, s3
srli t3, t2, 1
andi t3, t3, 0x3FF
slli t3, t3, 21
srli t4, t2, 11
andi t4, t4, 1
slli t4, t4, 20
srli t5, t2, 12
andi t5, t5, 0xFF
slli t5, t5, 12
srli t6, t2, 20
andi t6, t6, 1
slli t6, t6, 31
or t3, t3, t4
or t3, t3, t5
or t3, t3, t6
ori t3, t3, 0x6F
sw t3, 0(s3)
fence.i
; refermer (RX)
addi a0, zero, @PROT_RX
jal .protger
addi t0, zero, 1
sd t0, @ETAT_REL(s2)
bltz a0, .restauration_echouee
addi a0, zero, 0
j .fin
.refus1:
addi a0, zero, 1
j .fin
.refus2:
addi a0, zero, 2
j .fin
.refus3:
addi a0, zero, 3
j .fin
.refus4:
addi a0, zero, 4
j .fin
.refus5:
addi a0, zero, 5
j .fin
.restauration_echouee:
addi a0, zero, 5
.fin:
ld ra, 0(sp)
ld s3, 8(sp)
addi sp, sp, 16
ret
.protger:
srli t0, s3, 12
slli t0, t0, 12
mv t2, a0
mv a0, t0
addi a1, zero, 1
slli a1, a1, 12
mv a2, t2
addi a7, zero, @SYS_MPROTECT
ecall
ret
