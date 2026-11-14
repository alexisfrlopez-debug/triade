; loupe-02-lire · bloc lire : la fenêtre bornée au tampon + le recouvrement du journal · spec loupe-02:R1 · bloc carte i110002
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x4240, taille 320 octets
; Domaine : loupe (M10, le TGN « Loupe ») · Dépendances : IAT kernel32 : SetFilePointerEx, ReadFile, GetLastError — la liste fermée du bloc (D161) ; AUCUN appelé (lire ne déplace rien — Q3, le défilement est à loupe-11)
; Notation explicite générée par outils/auteur.py depuis brouillons/loupe-02-lire.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 292 o · padding : 28 o (NOP, 0x90)
; Étiquettes résolues : .boucle_journal=0x42fc, .entree_suivante=0x431c, .erreur_systeme=0x432a, .verdict_session=0x433f, .verdict_entree=0x4346, .verdict_hors_bornes=0x434d, .succes=0x4354, .sortie=0x4356
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x424d + 0x7 + 0x9dac = 0xe000
;   0x42a4 + 0x6 - 0x1182 = 0x3128
;   0x42c9 + 0x6 - 0x119f = 0x3130
;   0x42e4 + 0x7 + 0xa1b5 = 0xe4a0
;   0x432a + 0x6 - 0x11e8 = 0x3148
; Appels directs (l'adresse du plan — I1) : call qword ptr [rip - 0x1182], call qword ptr [rip - 0x119f], call qword ptr [rip - 0x11e8]
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x30
lea rbx, [rip + 0x9dac]
cmp qword ptr [rbx + 528], -1
je 0x433f
mov r12, rcx
test cl, 0x0F
jnz 0x4346
mov r15, qword ptr [rbx + 520]
cmp r12, r15
jae 0x434d
mov r13d, 384
mov rax, r15
sub rax, r12
cmp rax, r13
cmovbe r13, rax
mov r14, qword ptr [rbx + 528]
mov rcx, r14
mov rdx, r12
xor r8d, r8d
xor r9d, r9d
call qword ptr [rip - 0x1182]
test eax, eax
jz 0x432a
mov rcx, r14
lea rdx, [rbx + 568]
mov r8d, r13d
lea r9, [rsp + 0x28]
mov qword ptr [rsp + 0x20], 0
call qword ptr [rip - 0x119f]
test eax, eax
jz 0x432a
mov r14d, dword ptr [rsp + 0x28]
cmp r14, r13
jne 0x432a
mov dword ptr [rbx + 552], r13d
lea r14, [rip + 0xa1b5]
mov r10d, dword ptr [r14 + 4096]
test r10d, r10d
jz 0x4354
xor ecx, ecx
mov r11, r14
mov rax, qword ptr [r11]
cmp rax, r12
jb 0x431c
lea rdx, [r12 + r13]
cmp rax, rdx
jae 0x431c
sub rax, r12
movzx edx, byte ptr [r11 + 8]
mov byte ptr [rbx + rax + 568], dl
add r11, 16
inc rcx
cmp rcx, r10
jb 0x42fc
jmp 0x4354
call qword ptr [rip - 0x11e8]
xor edx, edx
mov dword ptr [rbx + 552], edx
mov eax, -6
jmp 0x4356
mov eax, -4
jmp 0x4356
mov eax, -5
jmp 0x4356
mov eax, -3
jmp 0x4356
xor eax, eax
add rsp, 0x30
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
