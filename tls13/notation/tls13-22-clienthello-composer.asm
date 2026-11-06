; tls13-22-clienthello-composer · bloc le ClientHello composé (l'offre scellée du jalon, 114 o) · spec tls13-22:R1 · bloc carte h100022
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0xed00, taille 288 octets
; Domaine : tls13 (M9, l'ère 1.0.0) · Dépendances : bloc feuille de la famille poignée ; LA COMPOSITION PAR OCTETS FIXES — chaque champ à son offset constant (I1), les valeurs protocolaires du plan d'adressage en IMMÉDIATS (T5), l'aléa copié @ +6, la clé publique copiée @ +82 ; AUCUNE branche, AUCUNE construction variable — le message est FIXE (charte § 1) ; le message ne TOUCHE PAS au transcript (I2 — le principal chronique)
; Notation explicite générée par outils/auteur.py depuis brouillons/tls13-22-clienthello-composer.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 241 o · padding : 47 o (NOP, 0x90)
; Étiquettes résolues : .refus_nul=0xede1, .refus_taille=0xede9
test rcx, rcx
jz 0xede1
test rdx, rdx
jz 0xede1
test r8, r8
jz 0xede1
cmp r9, 114
jb 0xede9
mov dword ptr [r8], 0x6e000001
mov word ptr [r8 + 4], 0x303
mov r10, qword ptr [rcx]
mov qword ptr [r8 + 6], r10
mov r10, qword ptr [rcx + 8]
mov qword ptr [r8 + 14], r10
mov r10, qword ptr [rcx + 16]
mov qword ptr [r8 + 22], r10
mov r10, qword ptr [rcx + 24]
mov qword ptr [r8 + 30], r10
mov byte ptr [r8 + 38], 0
mov dword ptr [r8 + 39], 0x1130200
mov word ptr [r8 + 43], 1
mov word ptr [r8 + 45], 0x4300
mov dword ptr [r8 + 47], 0x3002b00
mov byte ptr [r8 + 51], 2
mov word ptr [r8 + 52], 0x403
mov dword ptr [r8 + 54], 0x4000a00
mov dword ptr [r8 + 58], 0x1d000200
mov dword ptr [r8 + 62], 0x6000d00
mov dword ptr [r8 + 66], 0x4080400
mov word ptr [r8 + 70], 0x104
mov dword ptr [r8 + 72], 0x26003300
mov dword ptr [r8 + 76], 0x1d002400
mov word ptr [r8 + 80], 0x2000
mov r10, qword ptr [rdx]
mov qword ptr [r8 + 82], r10
mov r10, qword ptr [rdx + 8]
mov qword ptr [r8 + 90], r10
mov r10, qword ptr [rdx + 16]
mov qword ptr [r8 + 98], r10
mov r10, qword ptr [rdx + 24]
mov qword ptr [r8 + 106], r10
xor eax, eax
ret
mov rax, -1
ret
mov rax, -2
ret
