; tcp-08-echo · bloc écho v1 — transformation identité (cible) · spec tcp-08:R1 · bloc carte c30008
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x4600, taille 64 octets
; Dépendances : bloc feuille ; aucun accès extérieur (cible du patch à chaud)
; Notation explicite générée par outils/auteur.py depuis brouillons/tcp-08-echo.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 28 o · padding : 36 o (NOP)
; Étiquettes résolues : .boucle=0x460b, .fin=0x461b
mov rax, r8
test r8, r8
je 0x461b
xor r9, r9
mov r10b, byte ptr [rdx + r9]
mov byte ptr [rcx + r9], r10b
inc r9
cmp r9, r8
jb 0x460b
ret
