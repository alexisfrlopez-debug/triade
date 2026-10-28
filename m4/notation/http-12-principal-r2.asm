; http-12-principal-r2 · bloc orchestration proxy — révision câblage + porte R10 · spec http-12:R2 · bloc carte g70011
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x7dc0, taille 512 octets
; Dépendances : RÉVISION (ancêtre e50012 http-12:R1 scellé 0.4.0, cité § 9) — LE CÂBLAGE : la boucle lance http-10:R2 (0x74C0) ; la porte R10 devient marche aux BORNES (28 entrées, l'entrée .text3 remplace le terminateur @0x2810, fail-closed sur entrée trouée) ; l'ancêtre @0x1800 reste embarqué (R7)
; Notation explicite générée par outils/auteur.py depuis brouillons/http-12-principal-r2.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 458 o · padding : 54 o (NOP)
; Étiquettes résolues : .verif=0x7dec, .somme=0x7e12, .verif_ok=0x7e2f, .boucle=0x7ec3, .accept_echec=0x7ef6, .erreur_reseau=0x7f00, .arret=0x7f2e, .integrite_ko=0x7f5f
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x7dcd + 0x7 - 0x55a4 = 0x2830
;   0x7dde + 0x7 - 0x5785 = 0x2660
;   0x7de5 + 0x7 - 0x55cc = 0x2820
;   0x7e2f + 0x7 - 0x5616 = 0x2820
;   0x7e47 + 0x6 - 0x5d9d = 0x20b0
;   0x7e4d + 0x7 - 0x4654 = 0x3800
;   0x7e59 + 0x6 - 0x5daf = 0x20b0
;   0x7e5f + 0x7 - 0x465e = 0x3808
;   0x7e66 + 0x7 - 0x463d = 0x3830
;   0x7e6d + 0x6 - 0x5d9b = 0x20d8
;   0x7e73 + 0x7 - 0x563a = 0x2840
;   0x7ea0 + 0x7 - 0x4697 = 0x3810
;   0x7ea7 + 0x7 - 0x212e = 0x5d80
;   0x7ebd + 0x6 - 0x5dcb = 0x20f8
;   0x7ec3 + 0x7 - 0x46ba = 0x3810
;   0x7ed7 + 0x7 - 0xa1e = 0x74c0
;   0x7eee + 0x6 - 0x5dfc = 0x20f8
;   0x7ef6 + 0x8 - 0x46e6 = 0x3818
;   0x7f00 + 0x7 - 0x5617 = 0x28f0
;   0x7f28 + 0x6 - 0x5e6e = 0x20c0
;   0x7f2e + 0x7 - 0x5675 = 0x28c0
;   0x7f51 + 0x6 - 0x5c0f = 0x2348
;   0x7f59 + 0x6 - 0x5e9f = 0x20c0
;   0x7f64 + 0x6 - 0x5eba = 0x20b0
;   0x7f6d + 0x7 - 0x5664 = 0x2910
;   0x7f84 + 0x6 - 0x5eca = 0x20c0
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x60
lea rax, [rip - 0x55a4]
mov r14, rax
sub r14, 0x2830
lea rbx, [rip - 0x5785]
lea r15, [rip - 0x55cc]
cmp rbx, r15
jae 0x7e2f
mov edx, dword ptr [rbx]
test edx, edx
je 0x7f5f
mov r13d, dword ptr [rbx + 4]
test r13d, r13d
je 0x7f5f
mov r12, r14
add r12, rdx
xor eax, eax
xor ecx, ecx
add rax, qword ptr [r12 + rcx]
add rcx, 8
cmp rcx, r13
jb 0x7e12
cmp rax, qword ptr [rbx + 8]
jne 0x7f5f
add rbx, 16
jmp 0x7dec
mov rax, qword ptr [rip - 0x5616]
cmp rax, 0x40000
jb 0x7f5f
mov ecx, -11
call qword ptr [rip - 0x5d9d]
mov qword ptr [rip - 0x4654], rax
mov ecx, -10
call qword ptr [rip - 0x5daf]
mov qword ptr [rip - 0x465e], rax
lea rcx, [rip - 0x463d]
call qword ptr [rip - 0x5d9b]
lea rcx, [rip - 0x563a]
mov edx, 40
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call 0x4b00
call 0x4000
test rax, rax
je 0x7f00
mov qword ptr [rip - 0x4697], rax
lea rcx, [rip - 0x212e]
xor edx, edx
call 0x4300
test rax, rax
je 0x7f00
mov rcx, rax
call qword ptr [rip - 0x5dcb]
mov rcx, qword ptr [rip - 0x46ba]
call 0x4100
mov r12, rax
test rax, rax
js 0x7ef6
lea rcx, [rip - 0xa1e]
mov rdx, r12
call 0x4300
test rax, rax
je 0x7f00
mov rcx, rax
call qword ptr [rip - 0x5dfc]
jmp 0x7ec3
cmp qword ptr [rip - 0x46e6], 0
jne 0x7f2e
lea rcx, [rip - 0x5617]
mov edx, 22
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call 0x4b00
mov ecx, 2
call qword ptr [rip - 0x5e6e]
lea rcx, [rip - 0x5675]
mov edx, 7
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call 0x4b00
call qword ptr [rip - 0x5c0f]
xor ecx, ecx
call qword ptr [rip - 0x5e9f]
mov ecx, -11
call qword ptr [rip - 0x5eba]
mov rcx, rax
lea rdx, [rip - 0x5664]
mov r8d, 33
call 0x1040
mov ecx, 1
call qword ptr [rip - 0x5eca]
