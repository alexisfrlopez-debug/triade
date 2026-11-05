; tls13-14-x25519-cle-publique · bloc X25519 clé publique (le couple du ClientHello) · spec tls13-14:R1 · bloc carte h100014
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0xdc80, taille 64 octets
; Domaine : tls13 (M9, l'ère 1.0.0) · Dépendances : tls13-13 (l'échelle au point de base — I1) ; le point 9 au fixture R_U9 (la fixture PUBLIQUE du domaine, jamais un octet de code)
; Notation explicite générée par outils/auteur.py depuis brouillons/tls13-14-x25519-cle-publique.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 23 o · padding : 41 o (NOP, 0x90)
; Déplacements RIP (cible = adresse + taille + disp) :
;   0xdc84 + 0x7 + 0x2275 = 0xff00
; Appels directs (l'adresse scellée du plan — I1) : call 0xd100
sub rsp, 0x28
lea r8, [rip + 0x2275]
call 0xd100
xor eax, eax
add rsp, 0x28
ret
