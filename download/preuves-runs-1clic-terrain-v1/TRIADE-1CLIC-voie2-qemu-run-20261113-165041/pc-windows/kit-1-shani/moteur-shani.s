.intel_syntax noprefix
/* moteur-shani.s — GÉNÉRÉ par genere_moteur_shani.py (kit D205)
 * Les conventions : Windows x64 ; RIP-relatif ; aucun registre
 * non volatil détruit ; la pile alignée 16 aux appels. */
.text
.globl shani_compress
.globl moteur_avant
.globl moteur_apres
.globl cpuid_bloc
shani_compress:
    # le cadre : 0x68 = 104 o (8+104 ≡ 0 mod 16) —
    # [0x00..0x1F] ombre, [0x20] SAVEA, [0x30] SAVEC,
    # [0x40] xmm6 SAUVÉ (non volatil Windows), [0x50] xmm7 SAUVÉ
    sub  rsp, 0x68
    movdqa [rsp+0x40], xmm6
    movdqa [rsp+0x50], xmm7
    lea  r10, [rip + K256]
    lea  r11, [rip + MASK_BSWAP]
    movdqu xmm3, [rcx]
    movdqu xmm4, [rcx+16]
    pshufd xmm5, xmm4, 0xB1
    pshufd xmm6, xmm3, 0xB1
    punpcklqdq xmm5, xmm6
    movdqa xmm2, xmm5
    pshufd xmm5, xmm4, 0x1B
    pshufd xmm6, xmm3, 0x1B
    punpcklqdq xmm5, xmm6
    movdqa xmm1, xmm5
    movdqa [rsp+0x20], xmm2
    movdqa [rsp+0x30], xmm1
    movdqa xmm7, [r11]
    movdqu xmm3, [rdx]
    pshufb xmm3, xmm7
    movdqu xmm4, [rdx+16]
    pshufb xmm4, xmm7
    movdqu xmm5, [rdx+32]
    pshufb xmm5, xmm7
    movdqu xmm6, [rdx+48]
    pshufb xmm6, xmm7
    movdqa xmm0, [r10 + 0]
    paddd  xmm0, xmm3
    sha256rnds2 xmm1, xmm2
    pshufd xmm0, xmm0, 0x0E
    sha256rnds2 xmm2, xmm1
    movdqa xmm0, [r10 + 16]
    paddd  xmm0, xmm4
    sha256rnds2 xmm1, xmm2
    pshufd xmm0, xmm0, 0x0E
    sha256rnds2 xmm2, xmm1
    movdqa xmm0, [r10 + 32]
    paddd  xmm0, xmm5
    sha256rnds2 xmm1, xmm2
    pshufd xmm0, xmm0, 0x0E
    sha256rnds2 xmm2, xmm1
    movdqa xmm0, [r10 + 48]
    paddd  xmm0, xmm6
    sha256rnds2 xmm1, xmm2
    pshufd xmm0, xmm0, 0x0E
    sha256rnds2 xmm2, xmm1
    movdqa xmm7, xmm6
    palignr xmm7, xmm5, 4
    sha256msg1 xmm3, xmm4
    paddd  xmm3, xmm7
    sha256msg2 xmm3, xmm6
    movdqa xmm0, [r10 + 64]
    paddd  xmm0, xmm3
    sha256rnds2 xmm1, xmm2
    pshufd xmm0, xmm0, 0x0E
    sha256rnds2 xmm2, xmm1
    movdqa xmm7, xmm3
    palignr xmm7, xmm6, 4
    sha256msg1 xmm4, xmm5
    paddd  xmm4, xmm7
    sha256msg2 xmm4, xmm3
    movdqa xmm0, [r10 + 80]
    paddd  xmm0, xmm4
    sha256rnds2 xmm1, xmm2
    pshufd xmm0, xmm0, 0x0E
    sha256rnds2 xmm2, xmm1
    movdqa xmm7, xmm4
    palignr xmm7, xmm3, 4
    sha256msg1 xmm5, xmm6
    paddd  xmm5, xmm7
    sha256msg2 xmm5, xmm4
    movdqa xmm0, [r10 + 96]
    paddd  xmm0, xmm5
    sha256rnds2 xmm1, xmm2
    pshufd xmm0, xmm0, 0x0E
    sha256rnds2 xmm2, xmm1
    movdqa xmm7, xmm5
    palignr xmm7, xmm4, 4
    sha256msg1 xmm6, xmm3
    paddd  xmm6, xmm7
    sha256msg2 xmm6, xmm5
    movdqa xmm0, [r10 + 112]
    paddd  xmm0, xmm6
    sha256rnds2 xmm1, xmm2
    pshufd xmm0, xmm0, 0x0E
    sha256rnds2 xmm2, xmm1
    movdqa xmm7, xmm6
    palignr xmm7, xmm5, 4
    sha256msg1 xmm3, xmm4
    paddd  xmm3, xmm7
    sha256msg2 xmm3, xmm6
    movdqa xmm0, [r10 + 128]
    paddd  xmm0, xmm3
    sha256rnds2 xmm1, xmm2
    pshufd xmm0, xmm0, 0x0E
    sha256rnds2 xmm2, xmm1
    movdqa xmm7, xmm3
    palignr xmm7, xmm6, 4
    sha256msg1 xmm4, xmm5
    paddd  xmm4, xmm7
    sha256msg2 xmm4, xmm3
    movdqa xmm0, [r10 + 144]
    paddd  xmm0, xmm4
    sha256rnds2 xmm1, xmm2
    pshufd xmm0, xmm0, 0x0E
    sha256rnds2 xmm2, xmm1
    movdqa xmm7, xmm4
    palignr xmm7, xmm3, 4
    sha256msg1 xmm5, xmm6
    paddd  xmm5, xmm7
    sha256msg2 xmm5, xmm4
    movdqa xmm0, [r10 + 160]
    paddd  xmm0, xmm5
    sha256rnds2 xmm1, xmm2
    pshufd xmm0, xmm0, 0x0E
    sha256rnds2 xmm2, xmm1
    movdqa xmm7, xmm5
    palignr xmm7, xmm4, 4
    sha256msg1 xmm6, xmm3
    paddd  xmm6, xmm7
    sha256msg2 xmm6, xmm5
    movdqa xmm0, [r10 + 176]
    paddd  xmm0, xmm6
    sha256rnds2 xmm1, xmm2
    pshufd xmm0, xmm0, 0x0E
    sha256rnds2 xmm2, xmm1
    movdqa xmm7, xmm6
    palignr xmm7, xmm5, 4
    sha256msg1 xmm3, xmm4
    paddd  xmm3, xmm7
    sha256msg2 xmm3, xmm6
    movdqa xmm0, [r10 + 192]
    paddd  xmm0, xmm3
    sha256rnds2 xmm1, xmm2
    pshufd xmm0, xmm0, 0x0E
    sha256rnds2 xmm2, xmm1
    movdqa xmm7, xmm3
    palignr xmm7, xmm6, 4
    sha256msg1 xmm4, xmm5
    paddd  xmm4, xmm7
    sha256msg2 xmm4, xmm3
    movdqa xmm0, [r10 + 208]
    paddd  xmm0, xmm4
    sha256rnds2 xmm1, xmm2
    pshufd xmm0, xmm0, 0x0E
    sha256rnds2 xmm2, xmm1
    movdqa xmm7, xmm4
    palignr xmm7, xmm3, 4
    sha256msg1 xmm5, xmm6
    paddd  xmm5, xmm7
    sha256msg2 xmm5, xmm4
    movdqa xmm0, [r10 + 224]
    paddd  xmm0, xmm5
    sha256rnds2 xmm1, xmm2
    pshufd xmm0, xmm0, 0x0E
    sha256rnds2 xmm2, xmm1
    movdqa xmm7, xmm5
    palignr xmm7, xmm4, 4
    sha256msg1 xmm6, xmm3
    paddd  xmm6, xmm7
    sha256msg2 xmm6, xmm5
    movdqa xmm0, [r10 + 240]
    paddd  xmm0, xmm6
    sha256rnds2 xmm1, xmm2
    pshufd xmm0, xmm0, 0x0E
    sha256rnds2 xmm2, xmm1
    paddd  xmm2, [rsp+0x20]
    paddd  xmm1, [rsp+0x30]
    pshufd xmm3, xmm2, 0x1B
    pshufd xmm4, xmm1, 0x1B
    punpcklqdq xmm3, xmm4
    movdqu [rcx], xmm3
    pshufd xmm3, xmm2, 0x1B
    pshufd xmm4, xmm1, 0x1B
    punpckhqdq xmm3, xmm4
    movdqu [rcx+16], xmm3
    xor  eax, eax
    movdqa xmm6, [rsp+0x40]
    movdqa xmm7, [rsp+0x50]
    add  rsp, 0x68
    ret

moteur_avant:
    # rcx=f, rdx=etat, r8=bloc, r9=n → cycles
    sub  rsp, 0x58
    mov  [rsp+0x28], rcx
    mov  [rsp+0x30], rdx
    mov  [rsp+0x38], r8
    mov  [rsp+0x40], r9
    mov  dword ptr [rsp+0x44], 0
    lfence
    rdtsc
    shl  rdx, 32
    or   rdx, rax
    mov  [rsp+0x20], rdx
1:
    mov  rcx, [rsp+0x30]
    mov  rdx, [rsp+0x38]
    call qword ptr [rsp+0x28]
    inc  dword ptr [rsp+0x44]
    mov  eax, [rsp+0x44]
    cmp  eax, dword ptr [rsp+0x40]
    jb   1b
    rdtscp
    lfence
    shl  rdx, 32
    or   rdx, rax
    sub  rdx, [rsp+0x20]
    mov  rax, rdx
    add  rsp, 0x58
    ret

moteur_apres:
    # rcx=etat, rdx=bloc, r8=n → cycles (appel DIRECT)
    # cadre 0x48 = 72 o (8+72 ≡ 0 mod 16) : [0..0x1F] ombre,
    # [0x20] t0, [0x28] etat, [0x30] bloc, [0x38] n
    sub  rsp, 0x48
    mov  [rsp+0x28], rcx
    mov  [rsp+0x30], rdx
    mov  [rsp+0x38], r8d
    mov  dword ptr [rsp+0x3C], 0
    lfence
    rdtsc
    shl  rdx, 32
    or   rdx, rax
    mov  [rsp+0x20], rdx
2:
    mov  rcx, [rsp+0x28]
    mov  rdx, [rsp+0x30]
    call shani_compress
    inc  dword ptr [rsp+0x3C]
    mov  eax, [rsp+0x3C]
    cmp  eax, dword ptr [rsp+0x38]
    jb   2b
    rdtscp
    lfence
    shl  rdx, 32
    or   rdx, rax
    sub  rdx, [rsp+0x20]
    mov  rax, rdx
    add  rsp, 0x48
    ret

cpuid_bloc:
    # rcx=feuille, rdx=sous-feuille, r8=sortie u32[4]
    push rbx
    push rbp
    mov  eax, ecx
    mov  ecx, edx
    cpuid
    mov  [r8], eax
    mov  [r8+4], ebx
    mov  [r8+8], ecx
    mov  [r8+12], edx
    xor  eax, eax
    pop  rbp
    pop  rbx
    ret

.section .rodata
.balign 16
K256:
    .long 0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5
    .long 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5
    .long 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3
    .long 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174
    .long 0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc
    .long 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da
    .long 0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7
    .long 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967
    .long 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13
    .long 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85
    .long 0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3
    .long 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070
    .long 0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5
    .long 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3
    .long 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208
    .long 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
.balign 16
MASK_BSWAP:
    .byte 3, 2, 1, 0, 7, 6, 5, 4, 11, 10, 9, 8, 15, 14, 13, 12
