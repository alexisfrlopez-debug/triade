; tcp-06-spawn · bloc lancement de thread · spec tcp-06:R1 · bloc carte c30006
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x4300, taille 64 octets
; Dépendances : IAT kernel32 : CreateThread
; Notation explicite générée par outils/auteur.py depuis brouillons/tcp-06-spawn.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 43 o · padding : 21 o (NOP)
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x4320 + 0x6 - 0x225e = 0x20c8
sub rsp, 0x38
mov r8, rcx
mov r9, rdx
xor ecx, ecx
xor edx, edx
mov qword ptr [rsp + 0x20], 0
mov qword ptr [rsp + 0x28], 0
call qword ptr [rip - 0x225e]
add rsp, 0x38
ret
