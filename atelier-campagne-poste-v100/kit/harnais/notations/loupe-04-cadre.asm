; loupe-04-cadre · bloc le cadre de session posé vierge (la structure unique) · spec loupe-04:R1 · bloc carte i110004
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x4040, taille 64 octets
; Domaine : loupe (M10, le TGN « Loupe ») · Dépendances : libc-07 (le memset hérité PAR LA CARTE — byte-identique au scellé M1, jamais une boucle réécrite) ; le cadre posé vierge, la poignée INVALIDE ; AUCUNE entrée IAT (le miroir des feuilles pures, charte § 9)
; Notation explicite générée par outils/auteur.py depuis brouillons/loupe-04-cadre.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 47 o · padding : 17 o (NOP, 0x90)
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x4045 + 0x7 + 0x9fb4 = 0xe000
; Appels directs (l'adresse du plan — I1) : call 0x13c0
push rbx
sub rsp, 0x20
lea rbx, [rip + 0x9fb4]
mov rcx, rbx
xor edx, edx
mov r8d, 960
call 0x13c0
mov qword ptr [rbx + 528], -1
xor eax, eax
add rsp, 0x20
pop rbx
ret
