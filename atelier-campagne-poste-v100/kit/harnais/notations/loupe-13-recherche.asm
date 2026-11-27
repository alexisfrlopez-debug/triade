; loupe-13-recherche · bloc la recherche : la première occurrence par memcmp hérité (pur) · spec loupe-13:R1 · bloc carte i110013
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x5740, taille 192 octets
; Domaine : loupe (M10, le TGN « Loupe ») · Dépendances : libc-02 memcmp (LE BLOC SCELLÉ M1 PAR LA CARTE — I2 : chaque candidat testé par le scellé, JAMAIS une boucle réécrite) ; AUCUNE entrée IAT (la feuille pure, charte § 9) ; le départ à [rsp+0x28] (P5, le 5e argument msx64) ; la position ABSOLUE de la PREMIÈRE occurrence ou −1 (LA FIN NOMMÉE)
; Notation explicite générée par outils/auteur.py depuis brouillons/loupe-13-recherche.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 126 o · padding : 66 o (NOP, 0x90)
; Étiquettes résolues : .boucle=0x577c, .trouve=0x579f, .fin_nomme=0x57a4, .refus_entree=0x57ab, .sortie=0x57b0
; Appels directs (l'adresse du plan — I1) : call 0x1180
mov rax, qword ptr [rsp + 0x28]
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x20
test r9, r9
jz 0x57ab
cmp r9, 32
ja 0x57ab
cmp rax, rdx
ja 0x57ab
mov rbx, rcx
mov r12, rdx
mov r13, r8
mov r14, r9
mov r15, rax
mov rax, r12
sub rax, r15
cmp r14, rax
jg 0x57a4
mov rax, r15
add rax, r14
cmp rax, r12
ja 0x57a4
lea rcx, [rbx + r15]
mov rdx, r13
mov r8, r14
call 0x1180
test eax, eax
jz 0x579f
inc r15
jmp 0x577c
mov rax, r15
jmp 0x57b0
push -1
pop rax
nop
nop
jmp 0x57b0
push -5
pop rax
nop
nop
add rsp, 0x20
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
