; tls13-01-sha256-init · brouillon étiqueté — spec tls13-01:R1, bloc carte h100001
; l'initialisation du contexte SHA-256 (FIPS 180-4 § 5.3.1) — miroir win de
; ah-04 (M6) : la même sémantique, l'ABI msx64, le contexte en ARGUMENT
; (rcx) — charte § 6 : jamais une adresse fixe, TLS hache plusieurs flux.
; Q3 : rax = 0 (le verdict OK de la table du domaine) — divergence nommée
; d'avec ah-04 qui rendait le pointeur.
; feuille pure : aucun push, aucun appel, aucune non-volatile touchée (I4)
mov dword ptr [rcx], 0x6a09e667
mov dword ptr [rcx + 4], 0xbb67ae85
mov dword ptr [rcx + 8], 0x3c6ef372
mov dword ptr [rcx + 0xc], 0xa54ff53a
mov dword ptr [rcx + 0x10], 0x510e527f
mov dword ptr [rcx + 0x14], 0x9b05688c
mov dword ptr [rcx + 0x18], 0x1f83d9ab
mov dword ptr [rcx + 0x1c], 0x5be0cd19
mov qword ptr [rcx + 0x60], 0
mov qword ptr [rcx + 0x68], 0
xor eax, eax
ret
