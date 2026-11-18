; falsifiee-position · bloc la recherche : la position avancée d'un (LE MUTANT de la falsification) · spec loupe-13:R1 · bloc carte i110013
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x5740, taille 192 octets
; Domaine : loupe (M10, le TGN « Loupe ») · Dépendances : AUCUNE entrée IAT (la feuille pure) ; libc-02 memcmp (LE BLOC SCELLÉ M1 PAR LA CARTE) ; la falsification : la position avancée d'un
; Notation explicite générée par outils/auteur.py depuis brouillons/falsifiee-position.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 123 o · padding : 69 o (NOP, 0x90)
; Étiquettes résolues : .search_loop=0x577c, .trouve=0x579f, .fin_nomme=0x57a5, .refus_entree=0x57aa, .sortie=0x57ad
; Appels directs (l'adresse du plan — I1) : call 0x1180
mov rax, qword ptr [rsp + 0x28]
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x20
test r9, r9
jz 0x57aa
cmp r9, 0x20
ja 0x57aa
cmp rax, rdx
ja 0x57aa
mov rbx, rcx
mov r12, rdx
mov r13, r8
mov r14, r9
mov r15, rax
mov rax, r12
sub rax, r15
cmp r14, rax
jg 0x57a5
mov rax, r15
add rax, r14
cmp rax, r12
ja 0x57a5
lea rcx, [rbx + r15]
mov rdx, r13
mov r8, r14
call 0x1180
test eax, eax
jz 0x579f
inc r15
jmp 0x577c
lea rax, [r15 + 1]
jmp 0x57ad
push -1
pop rax
jmp 0x57ad
push -5
pop rax
add rsp, 0x20
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
