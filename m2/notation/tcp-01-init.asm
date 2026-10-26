; tcp-01-init · bloc initialisation serveur TCP · spec tcp-01:R1 · bloc carte c30001
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x4000, taille 256 octets
; Dépendances : IAT ws2_32 : WSAStartup, socket, bind, listen, closesocket, WSACleanup
; Notation explicite générée par outils/auteur.py depuis brouillons/tcp-01-init.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 173 o · padding : 83 o (NOP)
; Étiquettes résolues : .echec_sock=0x408b, .echec_wsa=0x4094, .echec=0x409a, .fin=0x409c
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x4033 + 0x6 - 0x1d39 = 0x2300
;   0x404d + 0x6 - 0x1d4b = 0x2308
;   0x406a + 0x6 - 0x1d60 = 0x2310
;   0x407c + 0x6 - 0x1d6a = 0x2318
;   0x408e + 0x6 - 0x1d5c = 0x2338
;   0x4094 + 0x6 - 0x1d52 = 0x2348
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x210
mov dword ptr [rsp + 0x20], 0xA8610002
mov dword ptr [rsp + 0x24], 0
mov qword ptr [rsp + 0x28], 0
mov ecx, 0x202
lea rdx, [rsp + 0x30]
call qword ptr [rip - 0x1d39]
test eax, eax
jne 0x409a
mov ecx, 2
mov edx, 1
mov r8d, 6
call qword ptr [rip - 0x1d4b]
cmp rax, -1
je 0x4094
mov rbx, rax
mov rcx, rbx
lea rdx, [rsp + 0x20]
mov r8d, 16
call qword ptr [rip - 0x1d60]
test eax, eax
jne 0x408b
mov rcx, rbx
mov edx, 8
call qword ptr [rip - 0x1d6a]
test eax, eax
jne 0x408b
mov rax, rbx
jmp 0x409c
mov rcx, rbx
call qword ptr [rip - 0x1d5c]
call qword ptr [rip - 0x1d52]
xor eax, eax
add rsp, 0x210
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
