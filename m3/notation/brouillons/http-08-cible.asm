; http-08-cible · brouillon · classification de la cible · http-08:R1 · e50008
; feuille pure : aucun appel, aucun IAT, aucun état ; écriture UNIQUE de la zone
; d'accueil (40 o) après le verdict final (I1, Q5) ; volatils uniquement, aucun
; octet de la cible recopié (I2 — spans d'origine, sauf le chemin par défaut
; « / » fixture .rdata de ce bloc) ; schéma « http:// » strict minuscule.
; entrée : rcx = cible, rdx = longueur (> 0), r8d = méthode (CONNECT = 8),
;          r9 = zone 40 o (forme u32 @0, autorité ptr @8, autorité len @16,
;          chemin ptr @24, chemin len @32)
; sortie : rax = 0 / 1 forme refusée / 2 autorité vide (absolue) / 3 schéma
; zone : ABSOLUE=1, ORIGINE=2, AUTORITÉ=3 ; l'autorité n'est JAMAIS interprétée
; ici (renvoi à http-07), le découpage s'arrête au premier « / » ou « ? » (I3).
cmp r8d, 8
je .autorite
; --- préfixe « http:// » (7 octets exacts, minuscules) ? ---
cmp rdx, 7
jb .pas_absolu
cmp dword ptr [rcx], 0x70747468
jne .pas_absolu
cmp word ptr [rcx + 4], 0x2F3A
jne .pas_absolu
cmp byte ptr [rcx + 6], 0x2F
jne .pas_absolu
; --- forme ABSOLUE : autorité = [7, k), k = premier « / » ou « ? » >= 7 ---
lea rax, [rcx + 7]
lea r10, [rcx + rdx]
.absolu_boucle:
cmp rax, r10
jae .absolu_defaut
movzx r11d, byte ptr [rax]
cmp r11, 0x2F
je .absolu_delim
cmp r11, 0x3F
je .absolu_defaut
add rax, 1
jmp .absolu_boucle
.absolu_delim:
; « / » : chemin = [rax, fin)
mov r8, rax
sub r10, rax
jmp .absolu_zone
.absolu_defaut:
; pas de délimiteur, ou « ? » : chemin = « / » (par DÉFINITION, fixture)
lea r8, [rip + SLASH]
mov r10d, 1
.absolu_zone:
lea rdx, [rcx + 7]
sub rax, rdx
test rax, rax
je .autorite_vide
mov r11d, 1
jmp .ecrit
; --- forme ORIGINE : la cible entière est le chemin ---
.pas_absolu:
cmp byte ptr [rcx], 0x2F
jne .pas_origine
mov r11d, 2
mov r8, rcx
mov r10, rdx
xor edx, edx
xor eax, eax
jmp .ecrit
; --- schéma non supporté (tout préfixe suivi de « :// » != « http », y
; --- compris préfixe VIDE « ://x » ; un « : » sans « // » qui suit n'est pas
; --- un schéma : Q2 refus — V2 différentiel, ex. « :A\x18\x8b » → 1) ---
.pas_origine:
xor eax, eax
.sch_boucle:
cmp rax, rdx
jae .refuse
cmp byte ptr [rcx + rax], 0x3A
je .sch_deux_points
add rax, 1
jmp .sch_boucle
.sch_deux_points:
lea r10, [rax + 2]
cmp r10, rdx
jae .refuse
cmp byte ptr [rcx + rax + 1], 0x2F
jne .refuse
cmp byte ptr [rcx + rax + 2], 0x2F
jne .refuse
mov eax, 3
ret
.refuse:
mov eax, 1
ret
; --- forme AUTORITÉ (CONNECT) : la cible entière est l'autorité ---
.autorite:
mov r11d, 3
mov rax, rdx
mov rdx, rcx
xor r8d, r8d
xor r10d, r10d
; --- zone (40 o), écriture unique ---
.ecrit:
mov dword ptr [r9], r11d
mov qword ptr [r9 + 8], rdx
mov qword ptr [r9 + 16], rax
mov qword ptr [r9 + 24], r8
mov qword ptr [r9 + 32], r10
xor eax, eax
ret
.autorite_vide:
mov eax, 2
ret
