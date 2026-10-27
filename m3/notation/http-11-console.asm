; http-11-console · bloc console · spec http-11:R1 · bloc carte e50011
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x5d80, taille 256 octets
; Dépendances : IAT kernel32 ReadFile ; blocs libc-02, tcp-05, tcp-11 ; état .data (stdin, listen, quit) ; chaînes .rdata
; Notation explicite générée par outils/auteur.py depuis brouillons/http-11-console.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 224 o · padding : 32 o (NOP)
; Étiquettes résolues : .boucle=0x5d90, .inconnu=0x5e27, .fin=0x5e4f
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x5d90 + 0x7 - 0x258f = 0x3808
;   0x5db0 + 0x6 - 0x3cc6 = 0x20f0
;   0x5dd5 + 0x7 - 0x349c = 0x2940
;   0x5dec + 0xa - 0x25de = 0x3818
;   0x5df6 + 0x7 - 0x25ed = 0x3810
;   0x5e02 + 0x7 - 0x3549 = 0x28c0
;   0x5e27 + 0x7 - 0x355e = 0x28d0
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x80
mov rcx, qword ptr [rip - 0x258f]
lea rdx, [rsp + 0x40]
mov r8d, 64
lea r9, [rsp + 0x28]
mov qword ptr [rsp + 0x20], 0
call qword ptr [rip - 0x3cc6]
test eax, eax
je 0x5e4f
cmp dword ptr [rsp + 0x28], 0
je 0x5e4f
cmp dword ptr [rsp + 0x28], 6
jne 0x5e27
lea rcx, [rsp + 0x40]
lea rdx, [rip - 0x349c]
mov r8, 6
call 0x1180
test eax, eax
jne 0x5e27
mov dword ptr [rip - 0x25de], 1
mov rcx, qword ptr [rip - 0x25ed]
call 0x41c0
lea rcx, [rip - 0x3549]
mov edx, 7
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call 0x4b00
jmp 0x5e4f
lea rcx, [rip - 0x355e]
mov edx, 19
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call 0x4b00
jmp 0x5d90
add rsp, 0x80
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
