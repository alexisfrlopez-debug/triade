/* couloir_sched512.S — LE SCHEDULE DE NOTATION EXÉCUTÉ DE L'ÈRE 512 (W29VAES512,
 * la pièce ii — le prompt 3 de la vague 29, le plan gelé 83af57f9…).
 * Le couloir AES-256-GCM VAES512 écrit en ASSEMBLAGE sur le calendrier de la
 * notation couloir-vaes512.asm (a2c3a393… consignée AVANT) : les chaînes CTR
 * pipelinées DEUX À DEUX (l'ILP que le compilateur ne garantit pas), la
 * frontière réfléchie au zmm (QUATRE blocs par passe, la table en REGISTRE —
 * la faute (5) de la vague 28 nommée au source), les QUATRE voies de produit
 * par vpclmulqdq (le KARATSUBA par voie), la pile ZMM pliée aux quatre voies
 * UNE fois par pli — la réduction 128-bit via la repli C fold_pli (la frontière
 * asm/C nommée : huit appels par message, hors chaîne critique).
 *
 * LE CONTRAT DE CONTEXTE (couloir_sched512.c) :
 *   +0x000 rk[15] (zmm × 15)      +0x3C0 Hr      +0x3E0 Hp[32] (xmm × 32)
 *   +0x5E0 ej0 (xmm)              +0x5F0 iv[12]
 *   +0x600 vb[8] (zmm × 8) — les [H^{32-4p} | H^{31-4p} | H^{30-4p} | H^{29-4p}]
 *   +0x800 LIGNE (zmm, les compteurs [2|3|4|5] posés)  +0x880 CTL (zmm)
 *   +0x8C0 QUATRE (zmm, l'incrément masqué)  +0x900 M (0x0F)  +0x940 MF0 (0xF0)
 *   +0x980 T (la table de réflexion, chargée en zmm5)
 *   +0x9C0 l'acc (16 o, la repli C le tient)  +0x9E0 PILE_LO  +0xA20 PILE_HI
 *
 * Interface (SysV) : couloir_sched512_msg(rdi=ctx, rsi=clair, rdx=chiffre)
 */
.intel_syntax noprefix
.text
.globl couloir_sched512_msg
.type couloir_sched512_msg, @function
couloir_sched512_msg:
    push rbx
    push r12
    push r13
    push r14
    push r15
    mov  r10, rdi                 # le ctx
    mov  r13, rsi                 # le clair
    mov  r14, rdx                 # le chiffre
    mov  r12, r10                 # rk = ctx+0
    vmovdqu64 zmm0, [r10 + 0x800] # la ligne des compteurs
    vmovdqu64 zmm5, [r10 + 0x940] # LA TABLE DE RÉFLEXION EN REGISTRE (zmm5)
    vpxord zmm16, zmm16, zmm16    # la pile lo
    vpxord zmm17, zmm17, zmm17    # la pile hi
    xor  r15, r15                 # le pli (0..7)

# ---- LA FRAPPE PAIRE : les DEUX chaînes pipelinées ----------------------------
# FRAPPE2 a, b, off_a, off_b : les chaînes AES-256 de DEUX frappes en vol,
# puis l'aiguillage xor/clair, le store, la frontière, le produit.
.macro FRAPPE2 a, b, off_a, off_b, vb_a, vb_b
    vpshufb  \a, zmm0, [r10 + 0x840]          # la CTL
    vpaddd   zmm0, zmm0, [r10 + 0x880]        # += 4 au dword 0 de chaque voie
    vpshufb  \b, zmm0, [r10 + 0x840]
    vpaddd   zmm0, zmm0, [r10 + 0x880]
    vpxord   \a, \a, [r12]                    # rk0
    vpxord   \b, \b, [r12]
.irp OFF, 0x40, 0x80, 0xC0, 0x100, 0x140, 0x180, 0x1C0, 0x200, 0x240, 0x280, 0x2C0, 0x300, 0x340
    vaesenc  \a, \a, [r12 + \OFF]             # rk1..rk13 — les tours pipelinés
    vaesenc  \b, \b, [r12 + \OFF]
.endr
    vaesenclast \a, \a, [r12 + 0x380]         # rk14
    vaesenclast \b, \b, [r12 + 0x380]
    vpxord   \a, \a, [r13 + \off_a]           # ⊕ le clair (64 octets)
    vmovdqu64 [r14 + \off_a], \a              # le chiffre
    vpxord   \b, \b, [r13 + \off_b]
    vmovdqu64 [r14 + \off_b], \b
    # la frontière réfléchie (la table zmm5 en REGISTRE, le contrôle mémoire)
    vpandd   zmm6, \a, [r10 + 0x8C0]          # M = 0x0F
    vpshufb  zmm6, zmm5, zmm6
    vpsrlw   zmm7, \a, 4
    vpandd   zmm7, zmm7, [r10 + 0x8C0]
    vpshufb  zmm7, zmm5, zmm7
    vpsllw   \a, zmm6, 4
    vpandd   \a, \a, [r10 + 0x900]            # MF0 = 0xF0
    vpord    \a, \a, zmm7
    vpandd   zmm6, \b, [r10 + 0x8C0]
    vpshufb  zmm6, zmm5, zmm6
    vpsrlw   zmm7, \b, 4
    vpandd   zmm7, zmm7, [r10 + 0x8C0]
    vpshufb  zmm7, zmm5, zmm7
    vpsllw   \b, zmm6, 4
    vpandd   \b, \b, [r10 + 0x900]
    vpord    \b, \b, zmm7
    # le produit de la frappe a : a × vb_a → la pile
    vmovdqu64 zmm8, [r10 + \vb_a]             # le vb de la frappe
    vunpcklpd zmm6, \a, \a
    vunpckhpd zmm7, \a, \a
    vpxord    zmm6, zmm6, zmm7                # a01 doublé
    vunpcklpd zmm9, zmm8, zmm8
    vunpckhpd zmm10, zmm8, zmm8
    vpxord    zmm9, zmm9, zmm10               # b01 doublé
    vpclmulqdq zmm11, \a, zmm8, 0x00           # l
    vpclmulqdq zmm12, \a, zmm8, 0x11           # h
    vpclmulqdq zmm13, zmm6, zmm9, 0x00         # m
    vpxord    zmm13, zmm13, zmm11
    vpxord    zmm13, zmm13, zmm12             # m'
    vpslldq   zmm14, zmm13, 8
    vpxord    zmm16, zmm16, zmm11
    vpxord    zmm16, zmm16, zmm14             # la pile lo
    vpsrldq   zmm14, zmm13, 8
    vpxord    zmm17, zmm17, zmm12
    vpxord    zmm17, zmm17, zmm14             # la pile hi
    # le produit de la frappe b
    vmovdqu64 zmm8, [r10 + \vb_b]
    vunpcklpd zmm6, \b, \b
    vunpckhpd zmm7, \b, \b
    vpxord    zmm6, zmm6, zmm7
    vunpcklpd zmm9, zmm8, zmm8
    vunpckhpd zmm10, zmm8, zmm8
    vpxord    zmm9, zmm9, zmm10
    vpclmulqdq zmm11, \b, zmm8, 0x00
    vpclmulqdq zmm12, \b, zmm8, 0x11
    vpclmulqdq zmm13, zmm6, zmm9, 0x00
    vpxord    zmm13, zmm13, zmm11
    vpxord    zmm13, zmm13, zmm12
    vpslldq   zmm14, zmm13, 8
    vpxord    zmm16, zmm16, zmm11
    vpxord    zmm16, zmm16, zmm14
    vpsrldq   zmm14, zmm13, 8
    vpxord    zmm17, zmm17, zmm12
    vpxord    zmm17, zmm17, zmm14
.endm

.boucle_pli:
    FRAPPE2 zmm1, zmm2, 0x000, 0x040, 0x600, 0x640      # les frappes 0/1
    FRAPPE2 zmm3, zmm4, 0x080, 0x0C0, 0x680, 0x6C0      # les frappes 2/3
    FRAPPE2 zmm1, zmm2, 0x100, 0x140, 0x700, 0x740      # les frappes 4/5
    FRAPPE2 zmm3, zmm4, 0x180, 0x1C0, 0x780, 0x7C0      # les frappes 6/7
    # la repli : la pile rendue au ctx, la réduction par la C (huit appels
    # par message — la frontière asm/C nommée, hors chaîne critique)
    vmovdqu64 [r10 + 0x9C0], zmm16
    vmovdqu64 [r10 + 0xA00], zmm17
    vmovdqu64 [r10 + 0xA40], zmm0          # la LIGNE sauvée (la repli C clobber)
    mov  rdi, r10
    call fold_pli
    vmovdqu64 zmm0, [r10 + 0xA40]         # la ligne rendue
    vmovdqu64 zmm5, [r10 + 0x940]         # la table de réflexion rendue
    vpxord zmm16, zmm16, zmm16
    vpxord zmm17, zmm17, zmm17
    add  r13, 512
    add  r14, 512
    inc  r15
    cmp  r15, 8
    jb   .boucle_pli
    pop r15
    pop r14
    pop r13
    pop r12
    pop rbx
    ret
