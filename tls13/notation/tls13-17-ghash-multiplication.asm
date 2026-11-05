; tls13-17-ghash-multiplication · bloc GHASH la multiplication GF(2^128) (SP 800-38D § 6.3) · spec tls13-17:R1 · bloc carte h100017
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0xdfc0, taille 192 octets
; Domaine : tls13 (M9, l'ère 1.0.0) · Dépendances : bloc feuille ; la marche de l'algorithme 1 SP 800-38D § 6.3 MOT POUR MOT — SANS TABLE PAR DONNÉE (I1 : le masque 0/−1 par sbb, le repli SANS BRANCHE — I2) ; LE DOMAINE GROS-BOUTISTE PAR BSWAP (la seconde faute nommée par la sonde du geste : les DEUX voies bswapées, le premier bit de la chaîne = le bit 63 de la voie haute, le sortant = le bit 0 de la voie basse, l'ordre shld/sbb/shl capture le drapeau AVANT l'écrasement) ; R = GCM_R du plan en IMMÉDIAT : l'octet 0 au SOMMET de la voie haute — 0xE1 << 56 ; le SEUL saut est la boucle sur le COMPTEUR
; Notation explicite générée par outils/auteur.py depuis brouillons/tls13-17-ghash-multiplication.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 162 o · padding : 30 o (NOP, 0x90)
; Étiquettes résolues : .boucle=0xe007
sub rsp, 0x28
mov rax, qword ptr [rdx]
bswap rax
mov r9, qword ptr [rdx + 8]
bswap r9
mov r10, qword ptr [r8]
bswap r10
mov r11, qword ptr [r8 + 8]
bswap r11
mov qword ptr [rsp], 0
mov qword ptr [rsp + 8], 0
mov qword ptr [rsp + 0x10], 128
movabs rdx, 0xe100000000000000
mov qword ptr [rsp + 0x18], rdx
shld rax, r9, 1
sbb rdx, rdx
shl r9, 1
mov r8, r10
and r8, rdx
xor qword ptr [rsp], r8
mov r8, r11
and r8, rdx
xor qword ptr [rsp + 8], r8
shrd r11, r10, 1
sbb rdx, rdx
shr r10, 1
mov r8, qword ptr [rsp + 0x18]
and r8, rdx
xor r10, r8
sub qword ptr [rsp + 0x10], 1
jnz 0xe007
mov rax, qword ptr [rsp]
bswap rax
mov qword ptr [rcx], rax
mov rax, qword ptr [rsp + 8]
bswap rax
mov qword ptr [rcx + 8], rax
xor eax, eax
add rsp, 0x28
ret
