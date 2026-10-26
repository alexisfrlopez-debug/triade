; tcp-03-recv · bloc réception d'octets · spec tcp-03:R1 · bloc carte c30003
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x4140, taille 64 octets
; Dépendances : IAT ws2_32 : recv
; Notation explicite générée par outils/auteur.py depuis brouillons/tcp-03-recv.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 18 o · padding : 46 o (NOP)
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x4147 + 0x6 - 0x1e25 = 0x2328
sub rsp, 0x28
xor r9d, r9d
call qword ptr [rip - 0x1e25]
add rsp, 0x28
ret
