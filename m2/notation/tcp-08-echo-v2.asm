; tcp-08-echo-v2 · bloc écho v2 — transformation majuscules (remplaçant) · spec tcp-08:R2 · bloc carte c30014
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x4680, taille 128 octets
; Dépendances : bloc feuille ; aucun accès extérieur (remplaçant, zone de croissance)
; Notation explicite générée par outils/auteur.py depuis brouillons/tcp-08-echo-v2.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 44 o · padding : 84 o (NOP)
; Étiquettes résolues : .boucle=0x468b, .garder=0x469f, .fin=0x46ab
mov rax, r8
test r8, r8
je 0x46ab
xor r9, r9
mov r10b, byte ptr [rdx + r9]
cmp r10b, 0x61
jb 0x469f
cmp r10b, 0x7A
ja 0x469f
sub r10b, 0x20
mov byte ptr [rcx + r9], r10b
inc r9
cmp r9, r8
jb 0x468b
ret
