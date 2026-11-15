; loupe-13-recherche · bloc la recherche : la première occurrence par memcmp hérité (pur) · spec loupe-13:R1 · bloc carte i110013
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x5740, taille 192 octets
; Domaine : loupe (M10, le TGN « Loupe ») · Dépendances : AUCUNE entrée IAT (la feuille pure — le miroir exact des feuilles tls13, charte § 9) ; libc-02 memcmp (LE BLOC SCELLÉ M1 PAR LA CARTE — I2 : chaque candidat testé par le scellé, jamais une boucle réécrite, la liste d'appels FERMÉE) ; le départ P5 à [rsp+0x28] lu au-devant ; les bornes E1/E2/E3 AVANT tout geste ; la fenêtre et le motif LUS SEULS (I3)
; Notation explicite générée par outils/auteur.py depuis brouillons/loupe-13-recherche.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 116 o · padding : 76 o (NOP, 0x90)
; Étiquettes résolues : .boucle=0x577b, .fin_nomme=0x5795, .trouve=0x579a, .refus=0x57a2, .sortie=0x57a6
; Appels directs (l'adresse du plan — I1) : call 0x1180
mov rax, qword ptr [rsp + 0x28]
test r9, r9
jz 0x57a2
cmp r9, 32
ja 0x57a2
cmp rax, rdx
ja 0x57a2
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x20
mov r15, rcx
mov r12, r8
mov r13, r9
lea rbx, [rcx + rax]
lea r14, [rcx + rdx]
sub r14, r9
cmp rbx, r14
ja 0x5795
mov rcx, rbx
mov rdx, r12
mov r8, r13
call 0x1180
test eax, eax
jz 0x579a
inc rbx
cmp rbx, r14
jbe 0x577b
push -1
pop rax
jmp 0x57a6
sub rbx, r15
mov rax, rbx
jmp 0x57a6
push -5
pop rax
ret
add rsp, 0x20
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
