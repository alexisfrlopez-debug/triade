; win-03-boucle · bloc démo · spec win-03:R1 · bloc carte d40003
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x15c0, taille 128 octets
; Dépendances : IAT user32 : GetMessageW, TranslateMessage, DispatchMessageW
; Notation explicite générée par outils/auteur.py depuis brouillons/win-03-boucle.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 75 o · padding : 53 o (NOP)
; Étiquettes résolues : .boucle=0x15d2, .fin=0x15fb
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x15dd + 0x6 + 0x1235 = 0x2818
;   0x15ea + 0x6 + 0x1230 = 0x2820
;   0x15f3 + 0x6 + 0x122f = 0x2828
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x50
lea rbx, [rsp + 0x20]
mov rcx, rbx
xor edx, edx
xor r8d, r8d
xor r9d, r9d
call qword ptr [rip + 0x1235]
test eax, eax
jle 0x15fb
mov rcx, rbx
call qword ptr [rip + 0x1230]
mov rcx, rbx
call qword ptr [rip + 0x122f]
jmp 0x15d2
xor eax, eax
add rsp, 0x50
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
