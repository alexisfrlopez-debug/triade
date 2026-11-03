; http-08-cible-r3 · bloc cible (forme) — révision relèvement · spec http-08:R3 · bloc carte g80001
; Ancêtre : http-08:R2 (D77, embarquée 0.5.1 @0x7340 — la spécification R2 vit
; dans m4/I/ et ne change pas : la balise est immuable § 9). La révision vit en
; M5 (.text4 0x8000) et ne modifie que CE que le relèvement exige : SOUS
; politique armée, la forme absolue « http:// » reçoit le verdict PROPRE
; « cible à relever » (rax 5). Tout le reste de R2 (forme origine, forme
; autorité CONNECT, https:// byte-exact, chemin, casse, bornes, ordre des
; tests) est REPRIS TEL QUEL — cité, non recopié (T5).
; pre  : P1-P4 de http-08:R2 repris tels quels (span cible, longueur, sorties
;        méthode/chemin/autorité, zone d'accueil 40 o) ; P5 NOUVEAU : la
;        politique (u64 à la loge d'argument 5 — [rsp+0x30] du callee) vaut
;        0 ou 1 ; le test est un test de ZÉRO.
; post : Q1-Q3, Q5 de R2 repris tels quels ; Q4 de R2 repris tel quel
;        (« https:// » → rax 4, port implicite 443) ; Q6 NOUVEAU — forme
;        absolue « http:// » (7 octets exacts, minuscules) ET P5 != 0 :
;        rax = 5, la zone remplie aux règles R1 (forme ABSOLUE=1) ; SANS
;        politique : R2 OCTET POUR OCTET sur tout chemin.
; inv  : I1-I5 de R2 repris (feuille pure, aucune écriture hors la zone,
;        aucun NUL supposé, non-volatils, comparaisons byte-exactes) ;
;        I6 : « http:// » D'ABORD — le verdict 5 naît À LA PLACE du succès
;        générique, jamais après ; I7 : la politique est LUE UNE fois
;        ([rsp+0x30]), jamais écrite.
; Dépendances : RÉVISION (ancêtre g70009 http-08:R2 embarqué 0.5.1, cité § 9)
; Notation explicite générée par outils/auteur.py depuis brouillons/http-08-cible-r3.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
cmp r8d, 8
je .autorite
cmp rdx, 7
jb .pas_absolu
cmp dword ptr [rcx], 0x70747468
jne .pas_absolu
cmp word ptr [rcx + 4], 0x2F3A
jne .test_https
cmp byte ptr [rcx + 6], 0x2F
jne .pas_absolu
lea r10, [rcx + rdx]
lea rdx, [rcx + 7]
jmp .absolu_scan
.test_https:
cmp rdx, 8
jb .pas_absolu
cmp byte ptr [rcx + 4], 0x73
jne .pas_absolu
cmp byte ptr [rcx + 5], 0x3A
jne .pas_absolu
cmp byte ptr [rcx + 6], 0x2F
jne .pas_absolu
cmp byte ptr [rcx + 7], 0x2F
jne .pas_absolu
lea r10, [rcx + rdx]
lea rdx, [rcx + 8]
.absolu_scan:
mov rax, rdx
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
mov r8, rax
sub r10, rax
jmp .absolu_zone
.absolu_defaut:
lea r8, [rip + SLASH]
mov r10d, 1
.absolu_zone:
sub rax, rdx
test rax, rax
je .autorite_vide
lea r11, [rcx + 8]
cmp rdx, r11
mov r11d, 1
je .ecrit_tls
; R3 (P5/Q6) : le verdict « cible à relever » naît À LA PLACE du succès
; générique — la politique vit à la loge 5 ([rsp+0x30] du callee) ;
; le test est un test de ZÉRO (l'appelant n'écrit jamais autre chose que
; 0 ou 1) ; I6 : le verdict 5 est structuralement hors d'atteinte des
; schémas préfixes (l'autorité du 5 commence à rcx+7, celle du 4 à rcx+8
; — le saut .ecrit_tls ci-dessus les sépare AVANT tout test de politique)
cmp qword ptr [rsp + 0x30], 0
je .ecrit
; politique armée : la zone est remplie aux règles R1 (forme ABSOLUE=1 —
; r11d vient d'être posé), le verdict porte la valeur propre 5
mov dword ptr [r9], r11d
mov qword ptr [r9 + 8], rdx
mov qword ptr [r9 + 16], rax
mov qword ptr [r9 + 24], r8
mov qword ptr [r9 + 32], r10
mov eax, 5
ret
.pas_absolu:
cmp byte ptr [rcx], 0x2F
jne .pas_origine
mov r11d, 2
mov r8, rcx
mov r10, rdx
xor edx, edx
xor eax, eax
jmp .ecrit
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
.autorite:
mov r11d, 3
mov rax, rdx
mov rdx, rcx
xor r8d, r8d
xor r10d, r10d
.ecrit:
mov dword ptr [r9], r11d
mov qword ptr [r9 + 8], rdx
mov qword ptr [r9 + 16], rax
mov qword ptr [r9 + 24], r8
mov qword ptr [r9 + 32], r10
xor eax, eax
ret
.ecrit_tls:
mov dword ptr [r9], r11d
mov qword ptr [r9 + 8], rdx
mov qword ptr [r9 + 16], rax
mov qword ptr [r9 + 24], r8
mov qword ptr [r9 + 32], r10
mov eax, 4
ret
.autorite_vide:
mov eax, 2
ret
