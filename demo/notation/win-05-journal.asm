; win-05-journal · bloc démo · spec win-05:R2 · bloc carte d40005
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x19c0, taille 256 octets
; Dépendances : IAT user32 : SendMessageW ; bloc win-11 (miroir fichier) ; état .data (HWND_JOURNAL)
; Notation explicite générée par outils/auteur.py depuis brouillons/win-05-journal.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 99 o · padding : 157 o (NOP)
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x19cd + 0x7 + 0x1e94 = 0x3868
;   0x19e7 + 0x6 + 0xe53 = 0x2840
;   0x19ed + 0x7 + 0x1e74 = 0x3868
;   0x1a02 + 0x6 + 0xe38 = 0x2840
push rbx
push r12
sub rsp, 0x28
mov rbx, rcx
mov r12, rdx
mov rcx, qword ptr [rip + 0x1e94]
mov edx, 0xB1
mov r8, 0xFFFFFFFFFFFFFFFF
mov r9, 0xFFFFFFFFFFFFFFFF
call qword ptr [rip + 0xe53]
mov rcx, qword ptr [rip + 0x1e74]
mov edx, 0xC2
mov r8d, 1
mov r9, rbx
call qword ptr [rip + 0xe38]
mov rcx, rbx
mov rdx, r12
mov r8d, 2
call 0x1e00
xor eax, eax
add rsp, 0x28
pop r12
pop rbx
ret
