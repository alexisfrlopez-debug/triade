; tls13-16-ni-v2-pur · LE CHEMIN AES-NI PUR (le verdict porté par l'appelant hissé) — copie de laboratoire à la marge
; ABI msx64 (rcx = clés 176 o, rdx = entrée 16 o, r8 = sortie 16 o) — SEULEMENT les volatils employés, AUCUN prologue
movdqu xmm0, [rdx]
movdqu xmm1, [rcx]
pxor xmm0, xmm1
movdqu xmm1, [rcx + 16]
aesenc xmm0, xmm1
movdqu xmm1, [rcx + 32]
aesenc xmm0, xmm1
movdqu xmm1, [rcx + 48]
aesenc xmm0, xmm1
movdqu xmm1, [rcx + 64]
aesenc xmm0, xmm1
movdqu xmm1, [rcx + 80]
aesenc xmm0, xmm1
movdqu xmm1, [rcx + 96]
aesenc xmm0, xmm1
movdqu xmm1, [rcx + 112]
aesenc xmm0, xmm1
movdqu xmm1, [rcx + 128]
aesenc xmm0, xmm1
movdqu xmm1, [rcx + 144]
aesenc xmm0, xmm1
movdqu xmm1, [rcx + 160]
aesenclast xmm0, xmm1
movdqu [r8], xmm0
xor eax, eax
ret
