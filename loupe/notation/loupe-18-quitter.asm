; loupe-18-quitter · bloc la sortie : le double-geste garanti, aucune fuite (le bloc de la mort) · spec loupe-18:R1 · bloc carte i110018
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x6740, taille 192 octets
; Domaine : loupe (M10, le TGN « Loupe ») · Dépendances : LE DOUBLE-GESTE GARANTI (Q1/Q2 : marque sale + garde armée → le premier WM_CLOSE REFUSÉ NOMMÉMENT -5 — la phrase à la barre, MessageBeep : le refus s'entend — la fenêtre DEMEURE ; le second TRANSCHE : DestroyWindow) ; WM _DESTROY (Q3 : loupe-03 la session close PROPREMENT — le journal ABANDONNÉ DÉLIBÉRÉMENT, les octets non sauvés sont une VOLONTÉ — puis PostQuitMessage(0) : la boucle héritée win-03 rend, WinMain retourne, ExitProcess(0)) ; LA SORTIE NE SAUVEGARDE JAMAIS (I2 : la sauvegarde est un geste explicite de loupe-17) ; AUCUNE fuite (I3 : la poignée close, la file quittée UNE fois, le code de sortie 0 — même l'abandon délibéré est une sortie PROPRE) ; IAT user32 : DestroyWindow, PostQuitMessage, MessageBeep
; Notation explicite générée par outils/auteur.py depuis brouillons/loupe-18-quitter.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 163 o · padding : 29 o (NOP, 0x90)
; Étiquettes résolues : .fermeture=0x675f, .detruire=0x6796, .destruction=0x67a3, .sortie=0x67b2, .message=0x67ba, .message_copie=0x67c5, .message_fin=0x67d5
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x674a + 0x7 + 0x78af = 0xe000
;   0x677b + 0x7 - 0x4229 = 0x2559
;   0x6789 + 0x6 - 0x42bf = 0x24d0
;   0x6799 + 0x6 - 0x42e7 = 0x24b8
;   0x67aa + 0x6 - 0x42f0 = 0x24c0
;   0x67ba + 0x7 + 0x7c3f = 0xe400
;   0x67d5 + 0x7 + 0x7c24 = 0xe400
; Appels directs (l'adresse du plan — I1) : call 0x67ba, call qword ptr [rip - 0x42bf], call qword ptr [rip - 0x42e7], call 0x4380, call qword ptr [rip - 0x42f0]
push rbx
push r12
sub rsp, 0x28
mov r12, rcx
lea rbx, [rip + 0x78af]
cmp edx, 0x10
je 0x675f
cmp edx, 2
je 0x67a3
xor eax, eax
jmp 0x67b2
cmp dword ptr [rbx + 556], 0
je 0x6796
cmp dword ptr [rbx + 560], 0
jne 0x6796
mov dword ptr [rbx + 560], 1
lea rsi, [rip - 0x4229]
call 0x67ba
xor ecx, ecx
call qword ptr [rip - 0x42bf]
mov eax, -5
jmp 0x67b2
mov rcx, r12
call qword ptr [rip - 0x42e7]
xor eax, eax
jmp 0x67b2
call 0x4380
xor ecx, ecx
call qword ptr [rip - 0x42f0]
xor eax, eax
add rsp, 0x28
pop r12
pop rbx
ret
lea rdi, [rip + 0x7c3f]
add rdi, 12
mov al, byte ptr [rsi]
mov byte ptr [rdi], al
test al, al
jz 0x67d5
inc rsi
inc rdi
jmp 0x67c5
lea rax, [rip + 0x7c24]
mov dword ptr [rax], 3
ret
