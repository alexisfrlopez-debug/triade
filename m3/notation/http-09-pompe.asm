; http-09-pompe · bloc pompe unidirectionnelle · spec http-09:R1 · bloc carte e50009
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x54c0, taille 192 octets
; Dépendances : blocs tcp-03 @0x4140, tcp-04 @0x4180 — AUCUN autre, jamais tcp-05
; Notation explicite générée par outils/auteur.py depuis brouillons/http-09-pompe.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 128 o · padding : 64 o (NOP)
; Étiquettes résolues : .boucle=0x54df, .envoi=0x54fe, .v0=0x551e, .v1=0x5522, .v2=0x5529, .fin=0x552e
push rbx
push rbp
push r12
push r13
push r14
push r15
sub rsp, 0x28
mov rbx, rcx
mov r12, rdx
mov r14, r9
mov qword ptr [rsp + 0x20], r8
xor r15d, r15d
mov rcx, rbx
mov rdx, qword ptr [rsp + 0x20]
mov r8, r14
call 0x4140
test rax, rax
js 0x5522
je 0x551e
mov rbp, rax
mov r13, qword ptr [rsp + 0x20]
mov rcx, r12
mov rdx, r13
mov r8, rbp
call 0x4180
test rax, rax
jle 0x5529
add r15, rax
add r13, rax
sub rbp, rax
jne 0x54fe
jmp 0x54df
xor eax, eax
jmp 0x552e
mov eax, 1
jmp 0x552e
mov eax, 2
mov rdx, r15
add rsp, 0x28
pop r15
pop r14
pop r13
pop r12
pop rbp
pop rbx
ret
