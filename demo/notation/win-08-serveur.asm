; win-08-serveur · bloc démo · spec win-08:R3 · bloc carte d40008
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x1d00, taille 256 octets
; Dépendances : blocs tcp-01/02/06, win-05 (entrée scénario, ligne d'échec) ; IAT kernel32 : CloseHandle ; état .data
; Notation explicite générée par outils/auteur.py depuis brouillons/win-08-serveur.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 139 o · padding : 117 o (NOP)
; Étiquettes résolues : .boucle=0x1d29, .echec=0x1d5f, .fin=0x1d7d
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x1d17 + 0x7 + 0x1af2 = 0x3810
;   0x1d1e + 0xb + 0x1b57 = 0x3880
;   0x1d29 + 0x7 + 0x1ae0 = 0x3810
;   0x1d3d + 0x7 + 0x2abc = 0x4800
;   0x1d57 + 0x6 + 0x39b = 0x20f8
;   0x1d5f + 0xb + 0x1b16 = 0x3880
;   0x1d6a + 0x7 + 0xefb = 0x2c6c
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x30
call 0x4000
test rax, rax
je 0x1d5f
mov qword ptr [rip + 0x1af2], rax
mov qword ptr [rip + 0x1b57], 1
mov rcx, qword ptr [rip + 0x1ae0]
call 0x4100
test rax, rax
js 0x1d7d
mov r12, rax
lea rcx, [rip + 0x2abc]
mov rdx, r12
call 0x4300
test rax, rax
je 0x1d7d
mov r13, rax
mov rcx, r13
call qword ptr [rip + 0x39b]
jmp 0x1d29
mov qword ptr [rip + 0x1b16], 2
lea rcx, [rip + 0xefb]
mov edx, 37
call 0x5100
xor eax, eax
add rsp, 0x30
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
