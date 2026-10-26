; win-05-journal · bloc démo · spec win-05:R1 · bloc carte d40005
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x18c0, taille 128 octets
; Dépendances : IAT user32 : SendMessageW ; état .data (HWND_JOURNAL)
; Notation explicite générée par outils/auteur.py depuis brouillons/win-05-journal.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 82 o · padding : 46 o (NOP)
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x18cd + 0x7 + 0x1f94 = 0x3868
;   0x18e7 + 0x6 + 0xf53 = 0x2840
;   0x18ed + 0x7 + 0x1f74 = 0x3868
;   0x1902 + 0x6 + 0xf38 = 0x2840
push rbx
push r12
sub rsp, 0x28
mov rbx, rcx
mov r12, rdx
mov rcx, qword ptr [rip + 0x1f94]
mov edx, 0xB1
mov r8, 0xFFFFFFFFFFFFFFFF
mov r9, 0xFFFFFFFFFFFFFFFF
call qword ptr [rip + 0xf53]
mov rcx, qword ptr [rip + 0x1f74]
mov edx, 0xC2
mov r8d, 1
mov r9, rbx
call qword ptr [rip + 0xf38]
xor eax, eax
add rsp, 0x28
pop r12
pop rbx
ret
