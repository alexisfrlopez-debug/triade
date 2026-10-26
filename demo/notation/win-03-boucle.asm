; win-03-boucle · bloc démo · spec win-03:R1 · bloc carte d40003
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x1580, taille 128 octets
; Dépendances : IAT user32 : GetMessageW, TranslateMessage, DispatchMessageW
; Notation explicite générée par outils/auteur.py depuis brouillons/win-03-boucle.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 75 o · padding : 53 o (NOP)
; Étiquettes résolues : .boucle=0x1592, .fin=0x15bb
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x159d + 0x6 + 0x1275 = 0x2818
;   0x15aa + 0x6 + 0x1270 = 0x2820
;   0x15b3 + 0x6 + 0x126f = 0x2828
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
call qword ptr [rip + 0x1275]
test eax, eax
jle 0x15bb
mov rcx, rbx
call qword ptr [rip + 0x1270]
mov rcx, rbx
call qword ptr [rip + 0x126f]
jmp 0x1592
xor eax, eax
add rsp, 0x50
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
