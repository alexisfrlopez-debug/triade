; tls-01-nom-utf16 · bloc hôte span → UTF-16 (traduction unique) · spec tls-01:R1 · bloc carte g70001
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x6000, taille 128 octets
; Dépendances : feuille pure ; propriétaire T5 de la traduction span → UTF-16 (HOTE_MAX 255, octets >= 0x80 refusés)
; Notation explicite générée par outils/auteur.py depuis brouillons/tls-01-nom-utf16.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 89 o · padding : 39 o (NOP)
; Étiquettes résolues : .balaye=0x6011, .ascii=0x6023, .ecrit=0x6026, .termine=0x603b, .refus_longueur=0x604d, .refus_encodage=0x6053
test rdx, rdx
je 0x604d
cmp rdx, 255
ja 0x604d
xor r9d, r9d
cmp r9, rdx
jae 0x6023
test byte ptr [rcx + r9], 0x80
jnz 0x6053
add r9, 1
jmp 0x6011
xor r9d, r9d
cmp r9, rdx
jae 0x603b
movzx r10d, byte ptr [rcx + r9]
mov word ptr [r8 + r9*2], r10w
add r9, 1
jmp 0x6026
mov word ptr [r8 + r9*2], 0
lea rdx, [rdx + rdx]
add rdx, 2
xor eax, eax
ret
mov eax, 1
ret
mov eax, 2
ret
