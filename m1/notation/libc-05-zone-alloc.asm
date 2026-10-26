; libc-05-zone-alloc · bloc allocateur par zone · spec libc-05:R1 · bloc carte b20005
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x1300, taille 128 octets
; Dépendances : données : curseur @0x3000, arène @0x3040
; Notation explicite générée par outils/auteur.py depuis brouillons/libc-05-zone-alloc.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 79 o · padding : 49 o (NOP)
; Étiquettes résolues : .invalide=0x134c
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x131d + 0x7 + 0x1cdc = 0x3000
;   0x1327 + 0x7 + 0x1d12 = 0x3040
cmp rcx, 0x7C0
ja 0x134c
test rdx, rdx
je 0x134c
lea r9, [rdx - 1]
test r9, rdx
jne 0x134c
cmp rdx, 64
ja 0x134c
lea r8, [rip + 0x1cdc]
mov rax, qword ptr [r8]
lea r10, [rip + 0x1d12]
add rax, r9
not r9
and rax, r9
add r10, rax
add rax, rcx
cmp rax, 0x7C0
ja 0x134c
mov qword ptr [r8], rax
mov rax, r10
ret
xor eax, eax
ret
