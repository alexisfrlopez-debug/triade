; tcp-05-close · bloc fermeture de socket · spec tcp-05:R1 · bloc carte c30005
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x41c0, taille 64 octets
; Dépendances : IAT ws2_32 : closesocket
; Notation explicite générée par outils/auteur.py depuis brouillons/tcp-05-close.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 15 o · padding : 49 o (NOP)
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x41c4 + 0x6 - 0x1e92 = 0x2338
sub rsp, 0x28
call qword ptr [rip - 0x1e92]
add rsp, 0x28
ret
