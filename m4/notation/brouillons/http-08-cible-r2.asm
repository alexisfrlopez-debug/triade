; http-08-cible-r2 · bloc cible (forme) · spec http-08:R2 · révision du bloc e50008
; Ancêtre : http-08:R1 (D46, scellée 0.4.0 — spec m3/I/http-08-cible.md, citée
; non recopiée T5 ; balise immuable § 9). La révision AJOUTE le schéma chiffré,
; elle ne touche à RIEN d'autre : l'ordre des tests est documenté (I5) —
; « http:// » D'ABORD (héritage R1 octet pour octet), « https:// » ENSUITE.
; pre  : P1-P4 de R1 repris tels quels (P1 rcx span cible issu de http-02,
;        P2 rdx longueur u64 > 0, P3 r8d méthode — CONNECT=8 seule admettant
;        la forme autorité, P4 r9 zone d'accueil 40 o : forme u32 @0, autorité
;        ptr u64 @8 / longueur @16, chemin ptr u64 @24 / longueur @32) ; P5
;        pile alignée (rsp ≡ 8 mod 16).
; post : Q1-Q3 de R1 repris tels quels (rax 0 succès formes ABSOLUE=1 /
;        ORIGINE=2 / AUTORITÉ=3 ; rax 1 forme refusée ; rax 2 autorité vide
;        en forme absolue) ; Q4 NOUVEAU — forme absolue « https:// » (les 8
;        octets EXACTS, minuscules) : rax = 4, verdict « cible TLS » (valeur
;        propre à la révision, distincte du succès générique R1) ; la zone
;        est remplie aux règles R1 (forme ABSOLUE=1 — la STRUCTURE est
;        absolue ; autorité et chemin découpés à l'identique ; le port
;        implicite 443 est déductible du verdict — consigné dans la sortie,
;        la décision d'appeler tls-08 appartient à http-10:R2) ; Q5 — tout
;        schéma non reconnu (« HTTPs:// », « https:/ », « https:\ », toute
;        casse mixte) reçoit le refus de schéma de R1 : rax 3 si « :// »
;        générique, rax 1 sinon — AUCUNE tolérance nouvelle.
; inv  : I1 feuille pure (aucun appel, aucun IAT, aucune écriture hors la
;        zone d'accueil) ; I2 aucun octet de la cible recopié (spans dans le
;        tampon d'origine — le chemin par défaut « / » est la fixture .rdata
;        de l'ancêtre R1, propriété unique du bloc logique, réutilisée) ;
;        I3 le découpage absolu s'arrête au PREMIER « / » ou « ? » ; I4
;        non-volatils préservés ; I5 aucune terminaison NUL supposée — la
;        comparaison https est BYTE-EXACTE sur 8 octets, 8 pas 7 pas 9 : le
;        début d'autorité (rcx+7 ou rcx+8) porte le schéma, un préfixe
;        (« http://s://x » contre « https://x ») ne peut JAMAIS produire le
;        verdict 4 — structurellement : si le schéma était http, le début
;        d'autorité est rcx+7, distinct du seuil rcx+8 du verdict TLS.
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
jmp .ecrit
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
