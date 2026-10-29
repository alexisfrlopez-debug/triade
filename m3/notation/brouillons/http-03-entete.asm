; http-03-entete · brouillon · ligne d'en-tête → nom/valeur · http-03:R1 · e50003
; feuille pure : aucun appel, aucun IAT, aucun état ; écriture UNIQUE de la zone
; d'accueil (32 o) APRÈS le verdict final (I1-I5) ; volatils uniquement, le
; rognage OWS n'ajuste que les bornes du span (I5 — aucun octet déplacé).
; entrée : rcx = ligne (sans CRLF), rdx = longueur, r8 = zone 32 o
; sortie : rax = 0 (zone remplie) / 1 pas de séparateur / 2 nom invalide
mov r11, r8
; --- premier deux-points ---
xor eax, eax
jmp .col_test
.col_boucle:
cmp byte ptr [rcx + rax], 0x3A
je .col_trouve
add rax, 1
.col_test:
cmp rax, rdx
jb .col_boucle
mov eax, 1
ret
.col_trouve:
; rax = index du deux-points = longueur du nom ; nom vide → verdict 2
test rax, rax
je .nom_invalide
; --- nom sans blanc (SP/HTAB) avant le deux-points (RFC 7230 §3.2.4) ---
xor r10d, r10d
.nom_boucle:
cmp r10, rax
jae .nom_ok
movzx r9d, byte ptr [rcx + r10]
cmp r9, 0x20
je .nom_invalide
cmp r9, 0x09
je .nom_invalide
add r10, 1
jmp .nom_boucle
.nom_ok:
; --- valeur : [k+1, fin), OWS rognés aux deux bornes ---
lea r10, [rax + 1]
mov r9, rdx
.rogne_g:
cmp r10, r9
jae .rogne_d
movzx edx, byte ptr [rcx + r10]
cmp dl, 0x20
je .rogne_avance
cmp dl, 0x09
je .rogne_avance
jmp .rogne_d
.rogne_avance:
add r10, 1
jmp .rogne_g
.rogne_d:
cmp r9, r10
jbe .ecrit
movzx edx, byte ptr [rcx + r9 - 1]
cmp dl, 0x20
je .rogne_recule
cmp dl, 0x09
je .rogne_recule
jmp .ecrit
.rogne_recule:
sub r9, 1
jmp .rogne_d
.ecrit:
mov qword ptr [r11], rcx
mov qword ptr [r11 + 8], rax
lea rdx, [rcx + r10]
mov qword ptr [r11 + 16], rdx
sub r9, r10
mov qword ptr [r11 + 24], r9
xor eax, eax
ret
.nom_invalide:
mov eax, 2
ret
