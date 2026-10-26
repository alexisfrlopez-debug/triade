; tcp-04-send · bloc émission d'octets · spec tcp-04:R1 · bloc carte c30004
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x4180, taille 64 octets
; Dépendances : IAT ws2_32 : send
; Notation explicite générée par outils/auteur.py depuis brouillons/tcp-04-send.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 18 o · padding : 46 o (NOP)
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x4187 + 0x6 - 0x1e5d = 0x2330
sub rsp, 0x28
xor r9d, r9d
call qword ptr [rip - 0x1e5d]
add rsp, 0x28
ret
