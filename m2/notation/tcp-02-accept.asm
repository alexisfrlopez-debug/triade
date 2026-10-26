; tcp-02-accept · bloc acceptation d'une connexion · spec tcp-02:R1 · bloc carte c30002
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x4100, taille 64 octets
; Dépendances : IAT ws2_32 : accept
; Notation explicite générée par outils/auteur.py depuis brouillons/tcp-02-accept.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 20 o · padding : 44 o (NOP)
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x4109 + 0x6 - 0x1def = 0x2320
sub rsp, 0x28
xor edx, edx
xor r8d, r8d
call qword ptr [rip - 0x1def]
add rsp, 0x28
ret
