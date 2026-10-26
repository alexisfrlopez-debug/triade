; ah-04-initialiser · brouillon étiqueté — spec ah-04:R1, bloc carte d40004
; contexte SHA-256 à l'état initial FIPS § 5.3.3 — constantes en immédiats
; (autoporteur : aucun déplacement RIP, R7-friendly)
mov dword ptr [rdi], 0x6a09e667
mov dword ptr [rdi + 4], 0xbb67ae85
mov dword ptr [rdi + 8], 0x3c6ef372
mov dword ptr [rdi + 12], 0xa54ff53a
mov dword ptr [rdi + 16], 0x510e527f
mov dword ptr [rdi + 20], 0x9b05688c
mov dword ptr [rdi + 24], 0x1f83d9ab
mov dword ptr [rdi + 28], 0x5be0cd19
mov qword ptr [rdi + 96], 0
mov qword ptr [rdi + 104], 0
mov rax, rdi
ret
