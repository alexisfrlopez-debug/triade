; loupe-02-lire · bloc lire : la fenêtre bornée au tampon + le recouvrement du journal · spec loupe-02:R1 · bloc carte i110002
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x4240, taille 320 octets
; Domaine : loupe (M10, le TGN « Loupe ») · Dépendances : IAT kernel32 : SetFilePointerEx, ReadFile, GetLastError — la liste fermée du bloc (D161) ; AUCUN appelé (lire ne déplace rien — Q3, le défilement est à loupe-11)
; Notation explicite générée par outils/auteur.py depuis brouillons/loupe-02-lire.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 300 o · padding : 20 o (NOP, 0x90)
; Étiquettes résolues : .rempli=0x4296, .recouvre=0x42f5, .recouvre_suivant=0x432c, .recouvre_fin=0x4330, .refus_session=0x4334, .refus_entree=0x433b, .refus_bornes=0x4342, .refus_systeme=0x4349, .sortie=0x4360
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x424b + 0x7 + 0x9dae = 0xe000
;   0x42ad + 0x6 - 0x118b = 0x3128
;   0x42e2 + 0x6 - 0x11b8 = 0x3130
;   0x42ec + 0x7 + 0xa1ad = 0xe4a0
;   0x4349 + 0x6 - 0x1207 = 0x3148
; Appels directs (l'adresse du plan — I1) : call qword ptr [rip - 0x118b], call qword ptr [rip - 0x11b8], call qword ptr [rip - 0x1207]
push rbx
push r12
push r13
push r14
sub rsp, 0x28
lea rbx, [rip + 0x9dae]
cmp qword ptr [rbx + 528], -1
je 0x4334
test rcx, 0xf
jne 0x433b
mov r12, rcx
cmp r12, qword ptr [rbx + 520]
jae 0x4342
mov r13, qword ptr [rbx + 520]
sub r13, r12
cmp r13, 384
jbe 0x4296
mov r13d, 384
mov dword ptr [rbx + 552], r13d
mov rcx, qword ptr [rbx + 528]
mov rdx, r12
xor r8d, r8d
xor r9d, r9d
call qword ptr [rip - 0x118b]
test eax, eax
jz 0x4349
mov rcx, qword ptr [rbx + 528]
lea rdx, [rbx + 568]
mov r8, r13
mov qword ptr [rsp + 0x20], 0
mov qword ptr [rsp], 0
lea r9, [rsp + 0x20]
call qword ptr [rip - 0x11b8]
test eax, eax
jz 0x4349
lea r14, [rip + 0xa1ad]
xor ecx, ecx
cmp ecx, dword ptr [r14 + 4096]
jae 0x4330
mov rax, rcx
shl rax, 4
mov rdx, qword ptr [r14 + rax]
cmp rdx, r12
jb 0x432c
mov r8, r12
add r8, r13
cmp rdx, r8
jae 0x432c
sub rdx, r12
mov al, byte ptr [r14 + rax + 8]
mov byte ptr [rbx + rdx + 568], al
inc ecx
jmp 0x42f5
inc ecx
jmp 0x42f5
xor eax, eax
jmp 0x4360
push -4
pop rax
nop
nop
jmp 0x4360
push -5
pop rax
nop
nop
jmp 0x4360
push -3
pop rax
nop
nop
jmp 0x4360
call qword ptr [rip - 0x1207]
mov dword ptr [rbx + 552], 0
push -6
pop rax
nop
nop
jmp 0x4360
add rsp, 0x28
pop r14
pop r13
pop r12
pop rbx
ret
