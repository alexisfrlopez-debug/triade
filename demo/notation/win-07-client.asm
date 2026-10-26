; win-07-client · bloc démo · spec win-07:R1 · bloc carte d40007
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x1ac0, taille 192 octets
; Dépendances : IAT ws2_32 : socket, connect, closesocket
; Notation explicite générée par outils/auteur.py depuis brouillons/win-07-client.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 123 o · padding : 69 o (NOP)
; Étiquettes résolues : .echec_close=0x1b22, .echec=0x1b2b, .fin=0x1b2d
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x1af6 + 0x6 + 0x80c = 0x2308
;   0x1b13 + 0x6 + 0x837 = 0x2350
;   0x1b25 + 0x6 + 0x80d = 0x2338
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x40
mov dword ptr [rsp + 0x20], 0xA8610002
mov dword ptr [rsp + 0x24], 0x0100007F
mov qword ptr [rsp + 0x28], 0
mov ecx, 2
mov edx, 1
mov r8d, 6
call qword ptr [rip + 0x80c]
cmp rax, -1
je 0x1b2b
mov rbx, rax
mov rcx, rbx
lea rdx, [rsp + 0x20]
mov r8d, 16
call qword ptr [rip + 0x837]
test eax, eax
jne 0x1b22
mov rax, rbx
jmp 0x1b2d
mov rcx, rbx
call qword ptr [rip + 0x80d]
xor eax, eax
add rsp, 0x40
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
