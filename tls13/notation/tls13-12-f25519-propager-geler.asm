; tls13-12-f25519-propager-geler · bloc f25519 propagation + gel sans branche (av-06+av-10 fusionnés) · spec tls13-12:R1 · bloc carte h100012
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0xcfc0, taille 320 octets
; Domaine : tls13 (M9, l'ère 1.0.0) · Dépendances : bloc FEUILLE fusionné (miroirs av-06 + av-10, UNE frontière) ; la passe séquentielle 0→4 puis LE GEL SANS BRANCHE DE DONNÉES (I2 : le drapeau en registre, sar, le masque 0/-1, l'ET logique — l'amélioration nommée) ; le masque, 19 et les membres de p en IMMÉDIATS (I1/I3)
; Notation explicite générée par outils/auteur.py depuis brouillons/tls13-12-f25519-propager-geler.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 281 o · padding : 39 o (NOP, 0x90)
movabs r10, 0x7ffffffffffff
mov rax, qword ptr [rcx]
mov rdx, rax
shr rdx, 51
and rax, r10
mov r8, qword ptr [rcx + 8]
add r8, rdx
mov rdx, r8
shr rdx, 51
and r8, r10
mov qword ptr [rcx + 8], r8
mov r9, qword ptr [rcx + 16]
add r9, rdx
mov rdx, r9
shr rdx, 51
and r9, r10
mov qword ptr [rcx + 16], r9
mov r8, qword ptr [rcx + 24]
add r8, rdx
mov rdx, r8
shr rdx, 51
and r8, r10
mov qword ptr [rcx + 24], r8
mov r9, qword ptr [rcx + 32]
add r9, rdx
mov rdx, r9
shr rdx, 51
and r9, r10
mov qword ptr [rcx + 32], r9
imul rdx, rdx, 19
add rax, rdx
mov qword ptr [rcx], rax
xor r9d, r9d
mov rax, qword ptr [rcx + 32]
xor rax, r10
or r9, rax
mov rax, qword ptr [rcx + 24]
xor rax, r10
or r9, rax
mov rax, qword ptr [rcx + 16]
xor rax, r10
or r9, rax
mov rax, qword ptr [rcx + 8]
xor rax, r10
or r9, rax
movabs r11, 0x7ffffffffffed
mov rax, qword ptr [rcx]
cmp rax, r11
setae r8b
test r9, r9
sete r9b
and r9d, r8d
shl r9, 63
sar r9, 63
mov rdx, r11
and rdx, r9
sub rax, rdx
mov qword ptr [rcx], rax
mov rax, qword ptr [rcx + 8]
mov rdx, r10
and rdx, r9
sub rax, rdx
mov qword ptr [rcx + 8], rax
mov rax, qword ptr [rcx + 16]
mov rdx, r10
and rdx, r9
sub rax, rdx
mov qword ptr [rcx + 16], rax
mov rax, qword ptr [rcx + 24]
mov rdx, r10
and rdx, r9
sub rax, rdx
mov qword ptr [rcx + 24], rax
mov rax, qword ptr [rcx + 32]
mov rdx, r10
and rdx, r9
sub rax, rdx
mov qword ptr [rcx + 32], rax
xor eax, eax
ret
