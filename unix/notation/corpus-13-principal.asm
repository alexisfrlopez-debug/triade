; corpus-13-principal · bloc orchestration du corpus paritaire (corpus-13:R1) · spec corpus-13:R1 · bloc carte f61013
; Profil : x86-64-linux-elf64 · ABI SysV · slot RVA 0x1c40, taille 320 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/corpus-13-principal.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 62 o · padding : 258 o (NOP)
; Étiquettes résolues : .fin=0x1c79, .ko=0x1c74
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x1c48 + 0x7 - 0x19cf = 0x280 (@J_PREF)
;   0x1c56 + 0x7 - 0x19bd = 0x2a0 (@J_SUFF)
; Symboles (vérifiés par build_m6.py contre layout.py) : @A_AUTOTEST=0x1340, @A_JOURNAL=0x1840, @A_SORTIR=0x1040, @J_PREF=0x280, @J_SUFF=0x2a0, @L_PREF=0x12, @L_SUFF=0xa
call 0x1340
mov rbx, rax
lea rdi, [rip - 0x19cf]
mov esi, 0x12
mov edx, ebx
lea rcx, [rip - 0x19bd]
mov r8d, 0xa
call 0x1840
cmp ebx, 0x15
jne 0x1c74
mov edi, 0
jmp 0x1c79
mov edi, 1
call 0x1040
