; loupe-05-sha256 · bloc sha256 d'une gamme : l'héritage tls13 PAR LA CARTE · spec loupe-05:R1 · bloc carte i110005
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x4440, taille 384 octets
; Domaine : loupe (M10, le TGN « Loupe ») · Dépendances : tls13-01 (l'init, UNE fois), tls13-03 (l'absorption à chaque fenêtre), tls13-04 (la finalisation) — LA FAMILLE SHA PAR LA CARTE (R7 : les octets du scellé 1.0.0, jamais une copie ré-écrite) ; IAT kernel32 : SetFilePointerEx, ReadFile, GetLastError ; le contexte 112 o SUR LA PILE
; Notation explicite générée par outils/auteur.py depuis brouillons/loupe-05-sha256.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 313 o · padding : 71 o (NOP, 0x90)
; Étiquettes résolues : .boucle=0x449a, .fenetre_taille=0x44b1, .finalise=0x4535, .refus_session=0x4546, .refus_bornes=0x454d, .refus_sortie=0x4554, .refus_systeme=0x455b, .sortie=0x4568
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x4450 + 0x7 + 0x9ba9 = 0xe000
;   0x44c1 + 0x6 - 0x209f = 0x2428
;   0x44f3 + 0x7 + 0xbb06 = 0x10000
;   0x44fd + 0x6 - 0x20d3 = 0x2430
;   0x450c + 0x7 + 0xbaed = 0x10000
;   0x455b + 0x6 - 0x2119 = 0x2448
; Appels directs (l'adresse du plan — I1) : call 0xc000, call qword ptr [rip - 0x209f], call qword ptr [rip - 0x20d3], call 0xc240, call 0xc300, call qword ptr [rip - 0x2119]
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0xc0
lea rbx, [rip + 0x9ba9]
cmp qword ptr [rbx + 528], -1
je 0x4546
mov rax, rcx
add rax, rdx
jc 0x454d
cmp rax, qword ptr [rbx + 520]
ja 0x454d
test r8, r8
jz 0x4554
mov r12, rcx
mov r13, rdx
mov r14, r8
lea rcx, [rsp + 0x40]
call 0xc000
test r13, r13
jz 0x4535
mov r15d, 0x10000
cmp r13, r15
jae 0x44b1
mov r15, r13
mov rcx, qword ptr [rbx + 528]
mov rdx, r12
xor r8d, r8d
xor r9d, r9d
call qword ptr [rip - 0x209f]
test eax, eax
jz 0x455b
mov qword ptr [rsp + 0xB0], 0
lea r9, [rsp + 0xB0]
mov qword ptr [rsp + 0x20], 0
mov rcx, qword ptr [rbx + 528]
lea rdx, [rip + 0xbb06]
mov r8, r15
call qword ptr [rip - 0x20d3]
test eax, eax
jz 0x455b
lea rcx, [rsp + 0x40]
lea rdx, [rip + 0xbaed]
mov r8, qword ptr [rsp + 0xB0]
call 0xc240
add r12, qword ptr [rsp + 0xB0]
sub r13, qword ptr [rsp + 0xB0]
jmp 0x449a
lea rcx, [rsp + 0x40]
mov rdx, r14
call 0xc300
xor eax, eax
jmp 0x4568
mov eax, -4
jmp 0x4568
mov eax, -3
jmp 0x4568
mov eax, -5
jmp 0x4568
call qword ptr [rip - 0x2119]
mov eax, -6
jmp 0x4568
add rsp, 0xc0
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
