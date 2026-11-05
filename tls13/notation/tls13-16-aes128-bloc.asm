; tls13-16-aes128-bloc · bloc AES-128 le chiffrement d'un bloc (l'arrêt AES-NI) · spec tls13-16:R1 · bloc carte h100016
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0xdf00, taille 192 octets
; Domaine : tls13 (M9, l'ère 1.0.0) · Dépendances : bloc feuille ; pxor + NEUF AESENC + AESENCLAST — LA COMPOSITION BLANCHE rend FIPS 197 C.1 sur l'émulateur (la contre-preuve du labo AVANT la notation) ; les clés chargées par movdqu NON ALIGNÉES (aucune précondition cachée), la BRIQUE D'INVERSION n'existe pas — AES en sens unique
; Notation explicite générée par outils/auteur.py depuis brouillons/tls13-16-aes128-bloc.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 129 o · padding : 63 o (NOP, 0x90)
movdqu xmm0, xmmword ptr [rdx]
movdqu xmm1, xmmword ptr [rcx]
pxor xmm0, xmm1
movdqu xmm1, xmmword ptr [rcx + 0x10]
aesenc xmm0, xmm1
movdqu xmm1, xmmword ptr [rcx + 0x20]
aesenc xmm0, xmm1
movdqu xmm1, xmmword ptr [rcx + 0x30]
aesenc xmm0, xmm1
movdqu xmm1, xmmword ptr [rcx + 0x40]
aesenc xmm0, xmm1
movdqu xmm1, xmmword ptr [rcx + 0x50]
aesenc xmm0, xmm1
movdqu xmm1, xmmword ptr [rcx + 0x60]
aesenc xmm0, xmm1
movdqu xmm1, xmmword ptr [rcx + 0x70]
aesenc xmm0, xmm1
movdqu xmm1, xmmword ptr [rcx + 0x80]
aesenc xmm0, xmm1
movdqu xmm1, xmmword ptr [rcx + 0x90]
aesenc xmm0, xmm1
movdqu xmm1, xmmword ptr [rcx + 0xa0]
aesenclast xmm0, xmm1
movdqu xmmword ptr [r8], xmm0
xor eax, eax
ret
