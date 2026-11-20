/* sequence-fencei.S — LA SONDE fence.i AU SILICIUM (kit l4nnwqlld, pièce 1-2)
 * ============================================================================
 * LE BUT : démontrer SUR FER RISC-V RÉELLE (une carte RV64GC sous Linux) ce
 * que les runs M7 vécus ne pouvaient que réserver (D149 : qemu-riscv64
 * exécute l'ISA par TCG — la sémantique du cache d'instructions y est celle
 * de l'hôte, jamais celle d'un cœur RISC-V) :
 *   (a) LA BASCULE VUE PAR LE CŒUR : le registre scratch t1 (fiche profil
 *       § 2/§ 5 — le portage R10/R11, JAMAIS un registre d'argument) chargé
 *       de l'adresse du slot, CONSIGNÉE au témoin à chaque run ; le saut
 *       jalr ra, 0(t1) — le transfert de contrôle PAR LE SCRATCH ;
 *   (b) L'INVALIDATION DU CACHE D'INSTRUCTIONS PROUVÉE AU TÉMOIN : le bras A
 *       (mprotect/mmap RW → écriture du mot ALIGNÉ 4 o ATOMIQUE → fence
 *       rw, rw → fence.i → RX → saut) rend le verdict du NOUVEAU mot dans
 *       100 % des runs (n ≥ 5) — le cœur a FETCHÉ l'instruction fraîche ;
 *   (c) L'OBSERVATION DU FETCH PÉRIMÉ (le bras B, SANS fence.i) : l'arm B
 *       suit TOUJOURS l'arm A de son run — le slot est CHAUD au cache
 *       d'instructions ; sans fence.i, le verdict rendu par un cœur servi
 *       par une ligne périmée est celui de l'ANCIEN mot. Le RISC-V n'EXIGE
 *       PAS la cohérence I/D (Unprivileged Spec, chap. « Fences ») : ce
 *       bras est une OBSERVATION consignée, JAMAIS une porte du verdict
 *       (un comportement non garanti architecturalement ne tranche rien).
 *
 * LE DESIGN (la lettre de la fiche riscv64-linux-elf64 § 5, séquence de
 * référence) : (1) la page du slot accessible en écriture ; (2) écrire le
 * nouveau bloc ; (3) fence rw, rw ; (4) la bascule — ICI le bloc EST un mot
 * unique (la granularité minimale : le mot de 4 o aligné, l'écriture
 * atomique sur RV64) ; (5) fence.i ; (6) la page rendue RX ; (7) le saut
 * via le scratch (jalr ra, 0(t1) — la variante APPELANTE du jalr x0 du
 * moteur : la sonde revient, le mécanisme scratch + fence.i est le même).
 *
 * DEUX MODES DE PAGE, fail-closed :
 *   mode 0 (préféré)  : une page RWX fraîche par mmap en tête de run — la
 *                       sonde copie le slot modèle dedans ; AUCUN mprotect
 *                       dans la boucle (le plus proche du mécanisme pur :
 *                       écrire → fence rw,rw → fence.i → sauter) ;
 *   mode 1 (repli)    : si le noyau REFUSE mmap RWX (politique execmem),
 *                       la sonde vit sur SA page .fencei_slot exécutable et
 *                       chaque bras fait le mprotect RW → … → RX complet
 *                       (la séquence § 5 intégrale, mprotect compris).
 * Le mode CONSIGNÉ au témoin — aucun des deux n'est un faux vert : un refus
 * de syscall est un ÉCHEC NOMMÉ (exit 2), jamais contourné en silence.
 *
 * LA CHAÎNE À PROVISIONNER (documentée au LISEZMOI du kit, la pièce
 * exacte) — l'assemblage :
 *   riscv64-linux-gnu-gcc -nostdlib -static \
 *       -march=rv64ima_zifencei_zicsr -mabi=lp64 \
 *       -o fencei-probe sequence-fencei.S
 * (Zifencei pour fence.i ; Zicsr pour rdcycle ; SANS C — .option norvc :
 * 4 octets par instruction, fiche § 1. Sur la carte même, le compilateur
 *  natif marche aux mêmes drapeaux.)
 *
 * LE TÉMOIN BINAIRE (stdout, redirection > temoin-probe.bin) : des
 * enregistrements de 48 octets, champs u64 petit-boutistes :
 *   en-tête  : [MAGIC, N_RUNS, 0xFF, adresse_du_slot, mode, 0]
 *   bras     : [run, arm ('A'=0x41/'B'=0x42), t1, mot_relu, verdict, cycles]
 * MAGIC = 0x45434931 (« ECI1 » little-endian). Le scénario décode, juge,
 * consigne — la pièce signée part au coffre.
 *
 * N_RUNS = 5 figé (le protocole exige n ≥ 5 ; davantage exige N_RUNS édité
 * et RÉ-ASSEMBLÉ — le geste nommé, l'empreinte du binaire reconsignée).
 */

    .option norvc                /* SANS extension C : 4 o exactement (fiche § 1) */

    .equ PROT_RW,      3         /* PROT_READ|PROT_WRITE */
    .equ PROT_RX,      5         /* PROT_READ|PROT_EXEC  */
    .equ PROT_RWX,     7         /* PROT_READ|PROT_WRITE|PROT_EXEC */
    .equ MAP_PRIVATE,  0x02
    .equ MAP_ANONYMOUS,0x20
    .equ NR_WRITE,     64        /* asm-generic (fiche § 4) */
    .equ NR_MPROTECT,  226
    .equ NR_MMAP,      222
    .equ NR_EXIT_GROUP,94
    .equ N_RUNS,       5
    .equ MAGIC,        0x45434931
    .equ V1,           0x00B00513  /* addi a0, zero, 11 — encodage VÉRIFIÉ
                                 * par l'assembleur maison du dépôt
                                 * (riscv/outils/as_rv64.py, au labo) */
    .equ V2,           0x01600513  /* addi a0, zero, 22 — idem, vérifié */
    .equ RET,          0x00008067  /* jalr x0, ra, 0    — idem, vérifié */
    .equ NOP,          0x00000013  /* addi x0, x0, 0    — idem, vérifié */

/* LE SLOT MODÈLE — une page exécutable à part (le repli mode 1) ; les QUATRE
 * encodages VÉRIFIÉS au laboratoire par l'assembleur maison du dépôt
 * (riscv/outils/as_rv64.py — le juge capstone 5.0.7 du dépôt en aval) :
 *   addi a0, zero, 11 -> 1305b000 (u32 LE 0x00B00513)
 *   addi a0, zero, 22 -> 13056001 (u32 LE 0x01600513)
 *   jalr x0, ra, 0    -> 67800000 (u32 LE 0x00008067)
 *   addi x0, x0, 0    -> 13000000 (u32 LE 0x00000013) */
    .section .fencei_slot, "ax", @progbits
    .balign 4096
    .globl slot_modele
slot_modele:
    .word V1                     /* LA BASCULE : le mot togglé, aligné 4 o */
    .word RET                    /* le retour du slot appelé               */
    .word NOP
    .word NOP
    .space 4080                  /* la page AU COMPLET : le mprotect du mode
                                  * repli est chirurgical — la page n'appartient
                                  * qu'au slot (jamais d'octet voisin touché) */

    .section .bss
    .balign 8
    .globl temoin_bin
temoin_bin:
    .space 4096
    .globl temoin_fin
temoin_fin:

    .section .rodata
refus_txt:
    .asciz "fencei-probe: REFUS NOMME (mmap/mprotect) — echec syscall, fail-closed\n"
refus_fin:

    .section .text
    .balign 4
    .globl _start
_start:
    /* s0 : curseur du témoin ; s1 : base de page du slot ; s2 : adresse du
     * slot ; s3 : compteur de runs ; s4 : mode (0 = RWX mmap, 1 = mprotect). */
    la      s0, temoin_bin
    la      s2, slot_modele
    li      t0, -4096
    and     s1, s2, t0
    li      s4, 1                    /* le mode repli par défaut … */

    /* … tenté de faire mieux : mmap RWX d'une page fraîche (mode 0) */
    li      a0, 0                    /* addr = NULL */
    li      a1, 4096
    li      a2, PROT_RWX
    li      a3, MAP_PRIVATE | MAP_ANONYMOUS
    li      a4, -1
    li      a5, 0
    li      a7, NR_MMAP
    ecall
    bltz    a0, mode_repli           /* refusé par le noyau : repli nommé */
    beqz   a0, mode_repli            /* NULL : refus de fait */
    /* copier le slot modèle (16 octets) vers la page fraîche */
    mv      t0, a0
    lw      t1, 0(s2)
    sw      t1, 0(t0)
    lw      t1, 4(s2)
    sw      t1, 4(t0)
    lw      t1, 8(s2)
    sw      t1, 8(t0)
    lw      t1, 12(s2)
    sw      t1, 12(t0)
    mv      s2, t0                   /* le slot vit désormais sur la page RWX */
    li      s4, 0
mode_repli:

    /* L'EN-TÊTE du témoin : [MAGIC, N_RUNS, 0xFF, slot, mode, 0] */
    li      t0, MAGIC
    sd      t0, 0(s0)
    li      t0, N_RUNS
    sd      t0, 8(s0)
    li      t0, 0xFF
    sd      t0, 16(s0)
    sd      s2, 24(s0)
    sd      s4, 32(s0)
    sd      zero, 40(s0)
    addi    s0, s0, 48

    li      s3, 1                    /* le premier run */

/* --- UN BRAS : la séquence § 5, le mot et le drapeau fence.i en paramètres ---- */
    .macro BRAS id_bras, mot, avec_fencei
.if \avec_fencei == 0
.if \id_bras != 0x42
    .error "le bras sans fence.i est le bras B (observation) — l'ordre est la loi"
.endif
.endif
    /* (1) la page accessible en écriture — mode 1 seul (mode 0 : déjà RWX) */
    beqz    s4, 9001f
    mv      a0, s1
    li      a1, 4096
    li      a2, PROT_RW
    li      a7, NR_MPROTECT
    ecall
    bltz    a0, refus
9001:
    /* LA BASCULE DU REGISTRE SCRATCH : t1 <- slot (jamais un registre
     * d'argument — fiche § 2/§ 5) */
    mv      t1, s2
    /* (2) écrire le nouveau bloc — LE MOT, aligné 4 o, atomique sur RV64 */
    li      t2, \mot
    sw      t2, 0(t1)
    /* (3) fence rw, rw : les écritures visibles */
    fence   rw, rw
    /* le mot relu : la vue DONNÉES du cœur, consignée au témoin */
    lw      a5, 0(t1)
.if \avec_fencei
    /* (5) fence.i : L'INVALIDATION DU CACHE D'INSTRUCTIONS du cœur courant */
    fence.i
.endif
    /* (6) la page rendue RX — mode 1 seul */
    beqz    s4, 9002f
    mv      a0, s1
    li      a1, 4096
    li      a2, PROT_RX
    li      a7, NR_MPROTECT
    ecall
    bltz    a0, refus
9002:
    /* les cycles AU-TOUR du saut : la mesure consignée (rdcycle, Zicsr) */
    rdcycle t3
    /* (7) LE SAUT VIA LE SCRATCH — la variante appelante du moteur */
    jalr    ra, 0(t1)
    rdcycle t4
    /* le témoignage : [run, arm, t1, mot, verdict(a0), cycles] */
    sd      s3, 0(s0)
    li      t5, \id_bras
    sd      t5, 8(s0)
    sd      t1, 16(s0)
    sd      a5, 24(s0)
    sd      a0, 32(s0)
    sub     t5, t4, t3
    sd      t5, 40(s0)
    addi    s0, s0, 48
    .endm

boucle_run:
    /* ARM A — AVEC fence.i : LE CRITÈRE (le verdict du NOUVEAU mot, 100 %) */
    BRAS    0x41, V2, 1
    /* ARM B — SANS fence.i : la sonde de fetch périmé (OBSERVATION consignée :
     * le slot est CHAUD — l'arm A vient de l'exécuter ; le mot mémoire est
     * retourné à v1, le cache peut encore servir v2) */
    BRAS    0x42, V1, 0

    addi    s3, s3, 1
    li      t0, N_RUNS + 1
    blt     s3, t0, boucle_run

    /* LE TÉMOIN PART : write(1, temoin_bin, 48 * (1 + 2*N_RUNS)) */
    li      a0, 1
    la      a1, temoin_bin
    li      a2, 48 * (1 + 2 * N_RUNS)
    li      a7, NR_WRITE
    ecall
    bltz    a0, refus
    li      a0, 0
    li      a7, NR_EXIT_GROUP
    ecall

refus:
    /* fail-closed : le refus NOMMÉ sur stderr, exit 2 — jamais un vert muet */
    li      a0, 2
    la      a1, refus_txt
    la      t0, refus_fin
    la      t1, refus_txt
    sub     a2, t0, t1
    li      a7, NR_WRITE
    ecall
    li      a0, 2
    li      a7, NR_EXIT_GROUP
    ecall
