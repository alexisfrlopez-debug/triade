; http-02-requete · brouillon · ligne de requête → champs typés · http-02:R1 · e50002
; feuille pure : aucun appel, aucun IAT, aucun état ; écriture UNIQUE de la zone
; d'accueil (56 o) après le verdict final (I1-I4) ; la table des méthodes .rdata
; (8 entrées ptr/longueur + terminateur len 0) EST la validation (Q3) — le
; terminateur NUL de chaque nom clôt la comparaison (entrées NUL-terminées).
; Compactage : r8 = i2 | (longueur << 16) | (énum version << 32) — feuille sans
; cadre : un seul push rbx (octet de travail de la comparaison, I4 préservé).
; entrée : rcx = ligne (sans CRLF), rdx = longueur, r8 = zone 56 o
; sortie : rax = 0 / 1 méthode inconnue / 2 structure / 3 version / 4 cible
push rbx
push r12
mov r11, r8
; base d'image par ancre (D33) — la table des méthodes porte
; des RVA, convention du projet (miroir table R10 de tcp-12)
lea rax, [rip + ANCRE]
mov r12d, 0x2830
sub rax, r12
mov r12, rax
; --- scan 1 : premier SP (fin de méthode) ---
xor eax, eax
jmp .s1_test
.s1_boucle:
cmp byte ptr [rcx + rax], 0x20
je .s1_trouve
add rax, 1
.s1_test:
cmp rax, rdx
jb .s1_boucle
jmp .structure
.s1_trouve:
test rax, rax
je .structure
mov r9, rax
; --- scan 2 : second SP (fin de cible) ---
lea rax, [r9 + 1]
jmp .s2_test
.s2_boucle:
cmp byte ptr [rcx + rax], 0x20
je .s2_trouve
add rax, 1
.s2_test:
cmp rax, rdx
jb .s2_boucle
jmp .structure
.s2_trouve:
mov r8, rax
shl rdx, 16
or r8, rdx
; --- cible : longueur = i2 - i1 - 1 dans [1, 2048] (Q5) ---
mov rax, r8
and eax, 0xFFFF
sub rax, r9
sub rax, 1
test rax, rax
je .cible_ko
cmp rax, 0x800
ja .cible_ko
; --- version : exactement "HTTP/1.0" ou "HTTP/1.1" (sensible, Q4) ---
mov r10, r8
and r10d, 0xFFFF
mov rax, r8
shr rax, 16
and eax, 0xFFFF
sub rax, r10
sub rax, 1
test rax, rax
je .structure
cmp rax, 8
jne .version_ko
mov rax, qword ptr [rcx + r10 + 1]
movabs rdx, 0x302E312F50545448
cmp rax, rdx
je .ver10
movabs rdx, 0x312E312F50545448
cmp rax, rdx
je .ver11
jmp .version_ko
.ver10:
bts r8, 32
jmp .methode
.ver11:
bts r8, 33
; --- méthode : marche de table, comparaison octet à octet ---
.methode:
lea rax, [rip + TAB_METHODES]
.mtab:
mov rdx, qword ptr [rax + 8]
test rdx, rdx
je .minconnu
cmp rdx, r9
jne .msuiv
mov edx, dword ptr [rax]
add rdx, r12
mov r10, rcx
.mcmp:
movzx ebx, byte ptr [rdx]
test bl, bl
je .mtrouve
cmp bl, byte ptr [r10]
jne .msuiv
add rdx, 1
add r10, 1
jmp .mcmp
.msuiv:
add rax, 16
jmp .mtab
.mtrouve:
lea rdx, [rip + TAB_METHODES]
sub rax, rdx
shr rax, 4
add rax, 1
; --- zone (56 o), écriture unique après le verdict final ---
mov qword ptr [r11 + 8], rcx
mov qword ptr [r11 + 16], r9
lea rdx, [rcx + r9 + 1]
mov qword ptr [r11 + 24], rdx
mov rdx, r8
and edx, 0xFFFF
sub rdx, r9
sub rdx, 1
mov qword ptr [r11 + 32], rdx
mov rdx, r8
and edx, 0xFFFF
lea rdx, [rcx + rdx + 1]
mov qword ptr [r11 + 40], rdx
mov rdx, r8
shr rdx, 16
and edx, 0xFFFF
mov r10, r8
and r10d, 0xFFFF
sub rdx, r10
sub rdx, 1
mov qword ptr [r11 + 48], rdx
mov dword ptr [r11], eax
mov rdx, r8
shr rdx, 32
mov dword ptr [r11 + 4], edx
xor eax, eax
pop r12
pop rbx
ret
.structure:
mov eax, 2
pop r12
pop rbx
ret
.version_ko:
mov eax, 3
pop r12
pop rbx
ret
.cible_ko:
mov eax, 4
pop r12
pop rbx
ret
.minconnu:
mov eax, 1
pop r12
pop rbx
ret
