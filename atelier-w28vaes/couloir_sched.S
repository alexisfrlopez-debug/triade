# couloir_sched.S — LE SCHEDULE DE NOTATION EXÉCUTÉ (W28VAES, la pièce ii).
# Le couloir AES-256-GCM VAES/VPCLMULQDQ écrit en ASSEMBLAGE sur le calendrier
# de la notation gelée couloir-vaes.asm (7911d03f… INTACTE) : l'ÉTAGE 3 — les
# chaînes CTR pipelinées DEUX À DEUX (l'ILP que le compilateur ne garantit pas),
# la frontière réfléchie au pli, la réduction unique par pli. L'algorithme est
# À L'IDENTIQUE celui du portage C v3 — le domaine réfléchi, la frontière
# rev256 (deux blocs par passe), la réduction de Gueron : SEUL LE CALENDRIER
# DIFFÈRE — l'écart mesuré en propre (le résultat distinct pré-enregistré).
#
# Le contrat de contexte (couloir_sched.c, aligned 32) :
#   +0x000 rk[15]  (ymm × 15)      +0x1E0 Hr     (xmm)
#   +0x1F0 Hp[8]   (xmm × 8)       +0x260 H⁸     (Hp[7])
#   +0x270 ej0     (xmm)           +0x280 vb[4]  (ymm × 4)
#   +0x300 ligne0  (ymm)           +0x320 iv[12]
# Interface (SysV) : couloir_sched_msg(rdi=ctx, rsi=clair, rdx=chiffre,
#                                       rcx=aad, r8=alen, r9=tag)

.intel_syntax noprefix
.text
.globl couloir_sched_msg
.type couloir_sched_msg, @function
couloir_sched_msg:
.macro REFLE128 x, base, t1, t2, t3, tbl
    vpand   \t1, \x, [\base + 0x20]
    vpshufb \t1, \tbl, \t1
    vpsrlw  \t2, \x, 4
    vpand   \t2, \t2, [\base + 0x20]
    vpshufb \t2, \tbl, \t2
    vpsllw  \t3, \t1, 4
    vpand   \t3, \t3, [\base + 0x40]
    vpor    \x, \t3, \t2
.endm

# REFLE256 x, base, t1, t2 — la frontière réfléchie (deux blocs par passe)
# REFLE256 x, base, t1, t2, tbl — la frontière réfléchie (deux blocs par passe)
#   LA TABLE en REGISTRE (le contrôle seul peut être mémoire — la première
#   passe inversait table et contrôle, la cause de la pile divergente)
.macro REFLE256 x, base, t1, t2, tbl
    vpand   \t1, \x, [\base + 0x20]
    vpshufb \t1, \tbl, \t1
    vpsrlw  \t2, \x, 4
    vpand   \t2, \t2, [\base + 0x20]
    vpshufb \t2, \tbl, \t2
    vpsllw  \x, \t1, 4
    vpand   \x, \x, [\base + 0x40]
    vpor    \x, \x, \t2
.endm

# FRAPPE_PLI use_inc — la frappe CTR du pli r11 (les chaînes 0/1 puis 2/3
# pipelinées, l'ILP deux à deux), la frontière réfléchie, les c au c_buf
.macro FRAPPE_PLI use_inc
    mov     rax, r11
    shl     rax, 7
    lea     rsi, [r13 + rax]
    lea     rdi, [r14 + rax]
    vmovdqu ymm5, [rbx + 0x00]         # la table de réflexion en registre
    # ---- les paires 0/1 : chaînes pipelinées ----
    vpshufb ymm0, ymm4, [rbx + 0xE0]
    vpaddd  ymm4, ymm4, [rbx + 0x100]
    vpshufb ymm1, ymm4, [rbx + 0xE0]
    vpaddd  ymm4, ymm4, [rbx + 0x100]
    vpxor   ymm0, ymm0, [r12 + 0x000]
    vpxor   ymm1, ymm1, [r12 + 0x000]
    vaesenc ymm0, ymm0, [r12 + 0x020]
    vaesenc ymm1, ymm1, [r12 + 0x020]
    vaesenc ymm0, ymm0, [r12 + 0x040]
    vaesenc ymm1, ymm1, [r12 + 0x040]
    vaesenc ymm0, ymm0, [r12 + 0x060]
    vaesenc ymm1, ymm1, [r12 + 0x060]
    vaesenc ymm0, ymm0, [r12 + 0x080]
    vaesenc ymm1, ymm1, [r12 + 0x080]
    vaesenc ymm0, ymm0, [r12 + 0x0A0]
    vaesenc ymm1, ymm1, [r12 + 0x0A0]
    vaesenc ymm0, ymm0, [r12 + 0x0C0]
    vaesenc ymm1, ymm1, [r12 + 0x0C0]
    vaesenc ymm0, ymm0, [r12 + 0x0E0]
    vaesenc ymm1, ymm1, [r12 + 0x0E0]
    vaesenc ymm0, ymm0, [r12 + 0x100]
    vaesenc ymm1, ymm1, [r12 + 0x100]
    vaesenc ymm0, ymm0, [r12 + 0x120]
    vaesenc ymm1, ymm1, [r12 + 0x120]
    vaesenc ymm0, ymm0, [r12 + 0x140]
    vaesenc ymm1, ymm1, [r12 + 0x140]
    vaesenc ymm0, ymm0, [r12 + 0x160]
    vaesenc ymm1, ymm1, [r12 + 0x160]
    vaesenc ymm0, ymm0, [r12 + 0x180]
    vaesenc ymm1, ymm1, [r12 + 0x180]
    vaesenc ymm0, ymm0, [r12 + 0x1A0]
    vaesenc ymm1, ymm1, [r12 + 0x1A0]
    vaesenclast ymm0, ymm0, [r12 + 0x1C0]     # rk[14] = +0x1C0 : L'ERREUR DU PLI
    vaesenclast ymm1, ymm1, [r12 + 0x1C0]     # (rk[13]=+0x1A0, rk[14]=+0x1C0 — vérifié)
    vpxor   ymm0, ymm0, [rsi]
    vmovdqu [rdi], ymm0
    vpxor   ymm1, ymm1, [rsi + 32]
    vmovdqu [rdi + 32], ymm1
    REFLE256 ymm0, rbx, ymm2, ymm3, ymm5
    vmovdqu [rbx + 0x60], ymm0
    REFLE256 ymm1, rbx, ymm2, ymm3, ymm5
    vmovdqu [rbx + 0x80], ymm1
    # ---- les paires 2/3 : chaînes pipelinées ----
    vpshufb ymm0, ymm4, [rbx + 0xE0]
    vpaddd  ymm4, ymm4, [rbx + 0x100]
    vpshufb ymm1, ymm4, [rbx + 0xE0]
    vpaddd  ymm4, ymm4, [rbx + 0x100]
    vpxor   ymm0, ymm0, [r12 + 0x000]
    vpxor   ymm1, ymm1, [r12 + 0x000]
    vaesenc ymm0, ymm0, [r12 + 0x020]
    vaesenc ymm1, ymm1, [r12 + 0x020]
    vaesenc ymm0, ymm0, [r12 + 0x040]
    vaesenc ymm1, ymm1, [r12 + 0x040]
    vaesenc ymm0, ymm0, [r12 + 0x060]
    vaesenc ymm1, ymm1, [r12 + 0x060]
    vaesenc ymm0, ymm0, [r12 + 0x080]
    vaesenc ymm1, ymm1, [r12 + 0x080]
    vaesenc ymm0, ymm0, [r12 + 0x0A0]
    vaesenc ymm1, ymm1, [r12 + 0x0A0]
    vaesenc ymm0, ymm0, [r12 + 0x0C0]
    vaesenc ymm1, ymm1, [r12 + 0x0C0]
    vaesenc ymm0, ymm0, [r12 + 0x0E0]
    vaesenc ymm1, ymm1, [r12 + 0x0E0]
    vaesenc ymm0, ymm0, [r12 + 0x100]
    vaesenc ymm1, ymm1, [r12 + 0x100]
    vaesenc ymm0, ymm0, [r12 + 0x120]
    vaesenc ymm1, ymm1, [r12 + 0x120]
    vaesenc ymm0, ymm0, [r12 + 0x140]
    vaesenc ymm1, ymm1, [r12 + 0x140]
    vaesenc ymm0, ymm0, [r12 + 0x160]
    vaesenc ymm1, ymm1, [r12 + 0x160]
    vaesenc ymm0, ymm0, [r12 + 0x180]
    vaesenc ymm1, ymm1, [r12 + 0x180]
    vaesenc ymm0, ymm0, [r12 + 0x1A0]
    vaesenc ymm1, ymm1, [r12 + 0x1A0]
    vaesenclast ymm0, ymm0, [r12 + 0x1C0]
    vaesenclast ymm1, ymm1, [r12 + 0x1C0]
    vpxor   ymm0, ymm0, [rsi + 64]
    vmovdqu [rdi + 64], ymm0
    vpxor   ymm1, ymm1, [rsi + 96]
    vmovdqu [rdi + 96], ymm1
    REFLE256 ymm0, rbx, ymm2, ymm3, ymm5
    vmovdqu [rbx + 0xA0], ymm0
    REFLE256 ymm1, rbx, ymm2, ymm3, ymm5
    vmovdqu [rbx + 0xC0], ymm1
.endm

# PRODUIT idx, vb — le produit Karatsuba 2×128 de la paire idx aux piles
# PRODUIT idx, vb — le produit Karatsuba 2×128 de la paire idx aux piles.
#   LA CAUSE PROFONDE nommée : la première passe chargeait c dans YMM0 — la
#   moitié basse du ymm0 EST l'acc (xmm0) : chaque produit DÉTRUISAIT
#   l'accumulateur — le karatsuba du pli calculait (c⊗H⁸) au lieu de (acc⊗H⁸).
#   Le produit vit désormais en ymm9/ymm2/ymm3/ymm5/ymm6/ymm7/ymm8 — jamais ymm0.
.macro PRODUIT idx, vb
    vmovdqu ymm9, [rbx + 0x60 + \idx * 32]
    vpunpcklqdq ymm2, ymm9, ymm9
    vpunpckhqdq ymm3, ymm9, ymm9
    vpxor   ymm2, ymm2, ymm3
    vpunpcklqdq ymm3, \vb, \vb
    vpunpckhqdq ymm7, \vb, \vb
    vpxor   ymm3, ymm3, ymm7
    vpclmulqdq ymm7, ymm9, \vb, 0x00
    vpclmulqdq ymm5, ymm9, \vb, 0x11
    vpclmulqdq ymm6, ymm2, ymm3, 0x00
    vpxor   ymm6, ymm6, ymm7
    vpxor   ymm6, ymm6, ymm5
    vpslldq ymm8, ymm6, 8
    vpxor   ymm7, ymm7, ymm8
    vpxor   ymm10, ymm10, ymm7
    vpsrldq ymm8, ymm6, 8
    vpxor   ymm5, ymm5, ymm8
    vpxor   ymm11, ymm11, ymm5
.endm

# KARATSUBA a, b, lo, hi, t1, t2, t3, t4 — le produit 128×128 (xmm)
.macro KARATSUBA a, b, lo, hi, t1, t2, t3, t4
    vpunpcklqdq \t1, \a, \a
    vpunpckhqdq \t2, \a, \a
    vpxor   \t1, \t1, \t2                 # a01
    vpunpcklqdq \t3, \b, \b
    vpunpckhqdq \t4, \b, \b
    vpxor   \t3, \t3, \t4                 # b01
    vpclmulqdq \lo, \a, \b, 0x00
    vpclmulqdq \hi, \a, \b, 0x11
    vpclmulqdq \t2, \t1, \t3, 0x00        # m
    vpxor   \t2, \t2, \lo
    vpxor   \t2, \t2, \hi
    vpslldq \t4, \t2, 8
    vpxor   \lo, \lo, \t4
    vpsrldq \t4, \t2, 8
    vpxor   \hi, \hi, \t4
.endm

# REDUIT_GCM dst, lo, hi, t1, t2, t3 — la réduction de Gueron (xmm)
# REDUIT_GCM dst, lo, hi, t1, t2, t3, t4 — la réduction de Gueron (xmm)
#   H = xd ⊕ shl128(xd,1) ⊕ shl128(xd,2) ⊕ shl128(xd,7) — TOUS DEPUIS le xd ORIGINAL
# REDUIT_GCM dst, lo, hi, t1, t2, t3, t4, t5 — la réduction de Gueron, PURE SIMD
#   (zéro franchissement GPR — la première passe portait pextrq/pinsrq LEGACY :
#    l'écriture SSE d'un xmm ZERO la moitié haute du ymm correspondant — la
#    LIGNE des compteurs ymm4 fut la victime, la cause nommée)
.macro REDUIT_GCM dst, lo, hi, t1, t2, t3, t4, t5
    vpunpckhqdq \t1, \hi, \hi
    vpsrlq  \t2, \t1, 63
    vpsrlq  \t3, \t1, 62
    vpxor   \t2, \t2, \t3
    vpsrlq  \t3, \t1, 57
    vpxor   \t2, \t2, \t3
    vpxor   \t4, \hi, \t2
    vpand   \t4, \t4, [rip + MASK_LO]
    vpand   \t5, \hi, [rip + MASK_HI]
    vpor    \t1, \t4, \t5
    vpsllq  \t2, \t1, 1
    vpsrlq  \t3, \t1, 63
    vpslldq \t3, \t3, 8
    vpor    \t2, \t2, \t3
    vmovdqa \t4, \t1
    vpxor   \t4, \t4, \t2
    vpsllq  \t2, \t1, 2
    vpsrlq  \t3, \t1, 62
    vpslldq \t3, \t3, 8
    vpor    \t2, \t2, \t3
    vpxor   \t4, \t4, \t2
    vpsllq  \t2, \t1, 7
    vpsrlq  \t3, \t1, 57
    vpslldq \t3, \t3, 8
    vpor    \t2, \t2, \t3
    vpxor   \t4, \t4, \t2
    vpxor   \dst, \lo, \t4
.endm

# GFMUL dst, b, t1, t2, t3, t4, t5 — dst = reduit(karatsuba(dst, b))
# GFMUL dst, b, t1, t2, t3, t4, t5, t6 — dst = reduit(karatsuba(dst, b))
# GFMUL dst, b, t1..t7 — dst = reduit(karatsuba(dst, b))
.macro GFMUL dst, b, t1, t2, t3, t4, t5, t6, t7
    KARATSUBA \dst, \b, \t1, \t2, \t3, \t4, \t5, \t6
    REDUIT_GCM \dst, \t1, \t2, \t3, \t4, \t5, \t6, \t7
.endm

    push    rbp
    mov     rbp, rsp
    push    rbx
    push    r12
    push    r13
    push    r14
    push    r15
    sub     rsp, 0x2A0

    mov     r12, rdi                # r12 = ctx
    mov     r13, rsi                # r13 = clair
    mov     r14, rdx                # r14 = chiffre
    mov     r15, r9                 # r15 = tag

    # le cadre : [rbp-0x2A0 .. rbp-0x80] — base = rbx
    lea     rbx, [rbp - 0x2A0]
    # +0x00 TBL   +0x20 M    +0x40 MF0   +0x60 c_buf (0x80)
    # +0xE0 CTL   +0x100 DEUXM
    vmovdqu ymm0, [rip + TBLQ]
    vmovdqu [rbx + 0x00], ymm0
    vmovdqu ymm0, [rip + MASQM]
    vmovdqu [rbx + 0x20], ymm0
    vmovdqu ymm0, [rip + MF0Q]
    vmovdqu [rbx + 0x40], ymm0
    vmovdqu ymm0, [rip + CTLQ]
    vmovdqu [rbx + 0xE0], ymm0
    vmovdqu ymm0, [rip + DEUXM]
    vmovdqu [rbx + 0x100], ymm0

    # ---------------- l'AAD : le GHASH scalaire (xmm0 = acc) ----------------
    # rcx/r8 (aad/alen) SAUVÉS au cadre : REDUIT_GCM écrase rax/rdx/rcx
    vpxor   xmm13, xmm13, xmm13
    mov     [rbx + 0x1C0], rcx
    mov     [rbx + 0x1C8], r8
    test    r8, r8
    jz      .aad_fini
    xor     r10, r10
.aad_boucle:
    mov     rax, [rbx + 0x1C8]
    sub     rax, r10
    cmp     rax, 16
    jb      .aad_reste
    mov     rcx, [rbx + 0x1C0]
    vmovdqu xmm1, [rcx + r10]
    vmovdqu xmm5, [rbx + 0x00]
    REFLE128 xmm1, rbx, xmm2, xmm3, xmm4, xmm5
    vpxor   xmm13, xmm13, xmm1
    vmovdqa xmm1, [r12 + 0x1E0]
    GFMUL xmm13, xmm1, xmm2, xmm3, xmm4, xmm5, xmm6, xmm7, xmm8
    add     r10, 16
    mov     rax, [rbx + 0x1C8]
    cmp     r10, rax
    jb      .aad_boucle
    jmp     .aad_fini
.aad_reste:
    mov     rcx, [rbx + 0x1C0]
    lea     rdi, [rbx + 0x180]
    xor     r11, r11
.aad_copie:
    cmp     r11, rax
    jae     .aad_copie_fini
    lea     rsi, [rcx + r10]
    mov     al, [rsi + r11]
    mov     [rdi + r11], al
    inc     r11
    jmp     .aad_copie
.aad_copie_fini:
    vmovdqu xmm1, [rbx + 0x180]
    vmovdqu xmm5, [rbx + 0x00]
    REFLE128 xmm1, rbx, xmm2, xmm3, xmm4, xmm5
    vpxor   xmm13, xmm13, xmm1
    vmovdqa xmm1, [r12 + 0x1E0]
    GFMUL xmm13, xmm1, xmm2, xmm3, xmm4, xmm5, xmm6, xmm7, xmm8
.aad_fini:
    # L'ACC AU CADRE : ymm13 porte le vb1 (la collision nommée) — l'acc vit en
    # [rbx + 0x200] et n'est chargé QUE pour les réductions et le tag final
    vmovdqu [rbx + 0x200], xmm13

    # ---------------- la ligne des compteurs (posée par le pilote) ------------
    vmovdqu ymm4, [r12 + 0x300]

    # ---------------- les vb persistants ---------------------------------------
    vmovdqu ymm12, [r12 + 0x280]
    vmovdqu ymm13, [r12 + 0x2A0]
    vmovdqu ymm14, [r12 + 0x2C0]
    vmovdqu ymm15, [r12 + 0x2E0]

    # ---------------- la pile (ymm10 lo, ymm11 hi) ----------------------------
    vpxor   ymm10, ymm10, ymm10
    vpxor   ymm11, ymm11, ymm11

    # ---------------- LE PREMIER PLI : la frappe CTR ---------------------------
    xor     r11, r11                  # le pli courant (AVANT la frappe — la faute nommée)
    FRAPPE_PLI 0
.boucle_plis:
    # ---- les vb RECHARGÉS à chaque pli : les quatre constantes sont
    #      ré-immunisées contre TOUT écrasement de voie (la règle VEX.128 :
    #      une écriture xmm zero la moitié haute du ymm — l'acc vivant un
    #      instant en xmm13 tua le vb1, la cause des plis 1+ divergents) ----
    vmovdqu ymm12, [r12 + 0x280]
    vmovdqu ymm13, [r12 + 0x2A0]
    vmovdqu ymm14, [r12 + 0x2C0]
    vmovdqu ymm15, [r12 + 0x2E0]
    # ---- le GHASH du pli : les quatre produits aux piles ----
    PRODUIT 0, ymm12
    PRODUIT 1, ymm13
    PRODUIT 2, ymm14
    PRODUIT 3, ymm15

    # ---- la réduction du pli : la pile ymm pliée + acc⊗H⁸ ----
    # LA RÈGLE NOMMÉE : une écriture VEX.128 DANS un xmm ZERO la moitié haute du
    # ymm correspondant — xmm4 est la MOITIÉ BASSE de ymm4, LA LIGNE des
    # compteurs : elle est SAUVÉE au cadre et RESTAURÉE autour de la réduction
    # (la première passe l'écrivait sans sauvegarde — la ligne détruite à
    # chaque pli, le chiffré divergeant dès le pli 1, la cause profonde).
    vmovdqu [rbx + 0x1E0], ymm4        # la ligne sauvée
    vmovdqa xmm0, [rbx + 0x200]        # l'acc chargé en XMM0 : la moitié haute
    #                                   du ymm0 (la chaîne CTR) est MORTE ici —
    #                                   l'écrasement VEX.128 est SANS objet
    vextracti128 xmm3, ymm10, 0
    vextracti128 xmm2, ymm10, 1
    vpxor   xmm3, xmm3, xmm2          # p_lo
    vextracti128 xmm4, ymm11, 0
    vextracti128 xmm2, ymm11, 1
    vpxor   xmm4, xmm4, xmm2          # p_hi
    vmovdqa xmm5, [r12 + 0x260]        # H⁸
    KARATSUBA xmm0, xmm5, xmm6, xmm7, xmm1, xmm2, xmm8, xmm9
    vpxor   xmm3, xmm3, xmm6           # lo = p_lo ⊕ alo
    vpxor   xmm4, xmm4, xmm7           # hi = p_hi ⊕ ahi
    REDUIT_GCM xmm0, xmm3, xmm4, xmm1, xmm2, xmm5, xmm6, xmm7
    vmovdqu [rbx + 0x200], xmm0        # l'acc rendu au cadre
    vmovdqu ymm4, [rbx + 0x1E0]        # la ligne restaurée

    vpxor   ymm10, ymm10, ymm10
    vpxor   ymm11, ymm11, ymm11

    inc     r11
    cmp     r11, 32
    jae     .boucle_fin
    # ---- la frappe CTR du pli SUIVANT (la notation : CTR(g+1) ouverte avant
    #      le GHASH de g — ici l'ordre du bloc suivant, les chaînes pipelinées) --
    FRAPPE_PLI 1                        # le pli r11 (inc déjà fait)
    jmp     .boucle_plis
.boucle_fin:

    # ---------------- le bloc des longueurs + le tag ---------------------------
    mov     rax, r8
    shl     rax, 3
    bswap   rax                         # abits grand ordre
    mov     [rbx + 0x1A0], rax
    mov     rax, 4096
    shl     rax, 3
    bswap   rax
    mov     [rbx + 0x1A8], rax
    vmovdqa xmm0, [rbx + 0x200]        # l'acc final chargé (xmm0 : la voie
    #                                    haute morte au tag, sans objet)
    vmovdqu xmm1, [rbx + 0x1A0]
    vmovdqu xmm5, [rbx + 0x00]
    REFLE128 xmm1, rbx, xmm2, xmm3, xmm4, xmm5
    vpxor   xmm0, xmm0, xmm1
    vmovdqa xmm1, [r12 + 0x1E0]         # Hr
    GFMUL xmm0, xmm1, xmm2, xmm3, xmm4, xmm5, xmm6, xmm7, xmm8

    # le tag : rev128(acc) ⊕ E_K(J0)
    vmovdqa xmm1, xmm0
    vmovdqu xmm5, [rbx + 0x00]
    REFLE128 xmm1, rbx, xmm2, xmm3, xmm4, xmm5
    vmovdqa xmm5, [r12 + 0x270]         # ej0
    vpxor   xmm1, xmm1, xmm5
    vmovdqu [r15], xmm1

    add     rsp, 0x2A0
    pop     r15
    pop     r14
    pop     r13
    pop     r12
    pop     rbx
    pop     rbp
    vzeroupper
    ret
.size couloir_sched_msg, . - couloir_sched_msg

# =================== LES MACROS (les idiomes du portage C, en calendrier) ====

# REFLE128 x, base, t1, t2, t3 — la conversion au monde réfléchi (xmm)
    .section .rodata
    .align 32
TBLQ:   .byte 0,8,4,12,2,10,6,14,1,9,5,13,3,11,7,15
        .byte 0,8,4,12,2,10,6,14,1,9,5,13,3,11,7,15
MASQM:  .byte 0x0F,0x0F,0x0F,0x0F,0x0F,0x0F,0x0F,0x0F,0x0F,0x0F,0x0F,0x0F,0x0F,0x0F,0x0F,0x0F
        .byte 0x0F,0x0F,0x0F,0x0F,0x0F,0x0F,0x0F,0x0F,0x0F,0x0F,0x0F,0x0F,0x0F,0x0F,0x0F,0x0F
MF0Q:   .byte 0xF0,0xF0,0xF0,0xF0,0xF0,0xF0,0xF0,0xF0,0xF0,0xF0,0xF0,0xF0,0xF0,0xF0,0xF0,0xF0
        .byte 0xF0,0xF0,0xF0,0xF0,0xF0,0xF0,0xF0,0xF0,0xF0,0xF0,0xF0,0xF0,0xF0,0xF0,0xF0,0xF0
CTLQ:   .byte 4,5,6,7,8,9,10,11,12,13,14,15,3,2,1,0
        .byte 4,5,6,7,8,9,10,11,12,13,14,15,3,2,1,0
MASK_LO: .quad 0xFFFFFFFFFFFFFFFF, 0
MASK_HI: .quad 0, 0xFFFFFFFFFFFFFFFF
DEUXM:  .long 2,0,0,0
        .long 2,0,0,0


    .data
    .align 32