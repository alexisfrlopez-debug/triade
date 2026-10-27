; http-07-autorite · brouillon · autorité « hôte[:port] » · http-07:R1 · e50007
; feuille pure : aucun appel externe, aucun IAT, aucun état ; écriture UNIQUE de
; la zone d'accueil (24 o) après le verdict final (I1, Q5) ; volatils uniquement,
; pile équilibrée (l'assistant local .chiffres_port est une étiquette interne,
; miroir .protger de tcp-07 — aucun appel de bloc, aucun IAT).
; LE propriétaire du découpage d'autorité (T5) — crochets IPv6 exclus de la
; valeur rendue ; le DERNIER « : » hors crochets porte le port (I2) ; chiffres
; du port validés un à un, valeur testée <= 65535 avant publication (I3).
; entrée : rcx = span, rdx = longueur, r8d = port par défaut (0 = EXIGÉ),
;          r9 = zone 24 o (hôte ptr @0, hôte longueur @8, port u32 @16)
; sortie : rax = 0 / 1 hôte absent / 2 port invalide ou exigé absent / 3 crochet
; assistant .chiffres_port : r8 = curseur, rdx = compte à rebours (> 0, <= 5) ;
; retour r10d = port, CF = 1 si invalide — rax, r9, r11 préservés.
mov r11d, r8d
test rdx, rdx
je .hote_vide
cmp byte ptr [rcx], 0x5B
je .crochet
; --- forme simple : DERNIER deux-points (I2) ---
lea rax, [rdx - 1]
.dernier:
cmp byte ptr [rcx + rax], 0x3A
je .deux_points
test rax, rax
je .sans_port
sub rax, 1
jmp .dernier
.sans_port:
test r11d, r11d
je .port_invalide
mov r10d, r11d
mov rax, rdx
jmp .ecrit
.deux_points:
test rax, rax
je .hote_vide
lea r8, [rcx + rax + 1]
sub rdx, rax
sub rdx, 1
call .chiffres_port
jb .port_invalide
jmp .ecrit
; --- forme crochet : [hôteIPv6][:port] ---
.crochet:
mov rax, 1
.cherche_ferme:
cmp rax, rdx
jae .crochet_invalide
cmp byte ptr [rcx + rax], 0x5D
je .ferme
add rax, 1
jmp .cherche_ferme
.ferme:
sub rax, 1
test rax, rax
je .hote_vide
lea r10, [rax + 2]
cmp r10, rdx
jae .crochet_sans_port
cmp byte ptr [rcx + r10], 0x3A
jne .crochet_invalide
lea r8, [rcx + rax + 3]
sub rdx, rax
sub rdx, 3
call .chiffres_port
jb .port_invalide
lea rdx, [rcx + 1]
mov qword ptr [r9], rdx
mov qword ptr [r9 + 8], rax
mov dword ptr [r9 + 16], r10d
xor eax, eax
ret
.crochet_sans_port:
test r11d, r11d
je .port_invalide
lea rdx, [rcx + 1]
mov qword ptr [r9], rdx
mov qword ptr [r9 + 8], rax
mov dword ptr [r9 + 16], r11d
xor eax, eax
ret
; --- zone (forme simple) : hôte = (rcx, rax), port = r10d ---
.ecrit:
mov qword ptr [r9], rcx
mov qword ptr [r9 + 8], rax
mov dword ptr [r9 + 16], r10d
xor eax, eax
ret
; --- assistant local : chiffres du port ---
; rbx poussé (octet de travail — le compte à rebours rdx et le curseur r8
; vivent seuls, le chiffon ebx est l'octet courant) ; pile équilibrée.
.chiffres_port:
push rbx
test rdx, rdx
je .chiffres_ko
cmp rdx, 5
ja .chiffres_ko
xor r10d, r10d
.chiffres_boucle:
movzx ebx, byte ptr [r8]
sub ebx, 0x30
cmp ebx, 9
ja .chiffres_ko
lea r10, [r10 + r10*4]
add r10, r10
add r10, rbx
add r8, 1
sub rdx, 1
jne .chiffres_boucle
cmp r10d, 0xFFFF
ja .chiffres_ko
clc
pop rbx
ret
.chiffres_ko:
stc
pop rbx
ret
.hote_vide:
mov eax, 1
ret
.port_invalide:
mov eax, 2
ret
.crochet_invalide:
mov eax, 3
ret
