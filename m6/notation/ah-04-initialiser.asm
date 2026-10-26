; ah-04-initialiser · bloc initialisation du contexte SHA-256 · spec ah-04:R1 · bloc carte d40004
; Profil : x86-64-linux-elf64 · ABI SysV · slot RVA 0x1100, taille 256 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/ah-04-initialiser.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 75 o · padding : 181 o (NOP)
mov dword ptr [rdi], 0x6a09e667
mov dword ptr [rdi + 4], 0xbb67ae85
mov dword ptr [rdi + 8], 0x3c6ef372
mov dword ptr [rdi + 0xc], 0xa54ff53a
mov dword ptr [rdi + 0x10], 0x510e527f
mov dword ptr [rdi + 0x14], 0x9b05688c
mov dword ptr [rdi + 0x18], 0x1f83d9ab
mov dword ptr [rdi + 0x1c], 0x5be0cd19
mov qword ptr [rdi + 0x60], 0
mov qword ptr [rdi + 0x68], 0
mov rax, rdi
ret
