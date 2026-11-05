; tls13-01-sha256-init · bloc initialisation du contexte SHA-256 (FIPS § 5.3.1) · spec tls13-01:R1 · bloc carte h100001
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0xc000, taille 128 octets
; Domaine : tls13 (M9, l'ère 1.0.0) · Dépendances : bloc feuille ; aucun état, aucun appel — les H0 posés au contexte en argument (charte § 6)
; Notation explicite générée par outils/auteur.py depuis brouillons/tls13-01-sha256-init.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 74 o · padding : 54 o (NOP, 0x90)
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
