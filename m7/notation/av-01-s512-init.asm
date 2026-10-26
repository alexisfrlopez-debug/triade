; av-01-s512-init · bloc initialisation du contexte SHA-512 · spec av-01:R1 · bloc carte d50001
; Profil : x86-64-linux-elf64 · ABI SysV · slot RVA 0x1100, taille 256 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/av-01-s512-init.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 136 o · padding : 120 o (NOP)
movabs rax, 0x6a09e667f3bcc908
mov qword ptr [rdi], rax
movabs rax, 0xbb67ae8584caa73b
mov qword ptr [rdi + 8], rax
movabs rax, 0x3c6ef372fe94f82b
mov qword ptr [rdi + 0x10], rax
movabs rax, 0xa54ff53a5f1d36f1
mov qword ptr [rdi + 0x18], rax
movabs rax, 0x510e527fade682d1
mov qword ptr [rdi + 0x20], rax
movabs rax, 0x9b05688c2b3e6c1f
mov qword ptr [rdi + 0x28], rax
movabs rax, 0x1f83d9abfb41bd6b
mov qword ptr [rdi + 0x30], rax
movabs rax, 0x5be0cd19137e2179
mov qword ptr [rdi + 0x38], rax
mov dword ptr [rdi + 0xc0], 0
mov qword ptr [rdi + 0xc8], 0
mov rax, rdi
ret
