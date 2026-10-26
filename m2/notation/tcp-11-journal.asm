; tcp-11-journal · bloc ligne de journal console · spec tcp-11:R1 · bloc carte c30011
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x4b00, taille 256 octets
; Dépendances : IAT kernel32 : Enter/LeaveCriticalSection ; blocs libc-01/03/04, io-01 write @0x1040 ; état .data (stdout, CS)
; Notation explicite générée par outils/auteur.py depuis brouillons/tcp-11-journal.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 191 o · padding : 65 o (NOP)
; Étiquettes résolues : .sans_champ=0x4b62
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x4b21 + 0x7 - 0x12f8 = 0x3830
;   0x4b28 + 0x6 - 0x2a4e = 0x20e0
;   0x4b7b + 0x7 - 0x1382 = 0x3800
;   0x4b9e + 0x7 - 0x1375 = 0x3830
;   0x4ba5 + 0x6 - 0x2ac3 = 0x20e8
push rbx
push r12
push r13
push r14
push r15
mov rbx, qword ptr [rsp + 0x50]
sub rsp, 0x80
mov r12, rcx
mov r13, rdx
mov r14, r8
mov r15, r9
lea rcx, [rip - 0x12f8]
call qword ptr [rip - 0x2a4e]
lea rcx, [rsp + 0x40]
mov rdx, r12
mov r8, r13
call 0x1100
lea rax, [rsp + 0x40]
add rax, r13
cmp r14d, 0xFFFFFFFF
je 0x4b62
mov ecx, r14d
mov rdx, rax
call 0x1280
mov rcx, rax
call 0x1200
add r13, rax
lea rax, [rsp + 0x40]
add rax, r13
mov rcx, rax
mov rdx, r15
mov r8, rbx
call 0x1100
add r13, rbx
mov rcx, qword ptr [rip - 0x1382]
lea rdx, [rsp + 0x40]
mov r8, r13
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call 0x1040
mov r12, rax
lea rcx, [rip - 0x1375]
call qword ptr [rip - 0x2ac3]
mov rax, r12
add rsp, 0x80
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
