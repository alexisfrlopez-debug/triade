; tcp-09-conn · bloc thread par connexion · spec tcp-09:R1 · bloc carte c30009
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x4800, taille 384 octets
; Dépendances : blocs tcp-03/04/05, tcp-08 echo @0x4600, tcp-11 ; chaînes .rdata
; Notation explicite générée par outils/auteur.py depuis brouillons/tcp-09-conn.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 200 o · padding : 184 o (NOP)
; Étiquettes résolues : .boucle=0x4813, .envoyer=0x4867, .fin=0x488c
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x4840 + 0x7 - 0x21e3 = 0x2664
;   0x484f + 0x7 - 0x21ec = 0x266a
;   0x4894 + 0x7 - 0x21c3 = 0x26d8
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x460
mov rbx, rcx
mov rcx, rbx
lea rdx, [rsp + 0x30]
mov r8d, 1024
call 0x4140
test rax, rax
jle 0x488c
mov r12, rax
lea rcx, [rsp + 0x30]
lea rdx, [rsp + 0x30]
mov r8, r12
call 0x4600
lea rcx, [rip - 0x21e3]
mov edx, 5
mov r8d, r12d
lea r9, [rip - 0x21ec]
mov qword ptr [rsp + 0x20], 2
call 0x4b00
xor r13, r13
mov rcx, rbx
lea rdx, [rsp + 0x30]
add rdx, r13
mov r8, r12
sub r8, r13
call 0x4180
test rax, rax
jle 0x488c
add r13, rax
cmp r13, r12
jb 0x4867
jmp 0x4813
mov rcx, rbx
call 0x41c0
lea rcx, [rip - 0x21c3]
mov edx, 15
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call 0x4b00
add rsp, 0x460
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
