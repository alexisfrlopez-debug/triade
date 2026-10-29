; tcp-13-connexion · bloc connexion cliente résolue · spec tcp-13:R1 · bloc carte e50013
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x4400, taille 448 octets
; Dépendances : IAT ws2_32 : getaddrinfo, freeaddrinfo, socket, connect, closesocket ; cadre : hôte 256 o, hints 48 o, sockaddr 16 o
; Notation explicite générée par outils/auteur.py depuis brouillons/tcp-13-connexion.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 402 o · padding : 46 o (NOP)
; Étiquettes résolues : .copie=0x4431, .copie_fin=0x4446, .parcours=0x44d6, .addrinfo_trouve=0x44eb, .fermer_echec=0x4564, .liberer_echec=0x456d, .echec=0x457f, .fin=0x4581
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x44c0 + 0x6 - 0x2176 = 0x2350
;   0x4527 + 0x6 - 0x2225 = 0x2308
;   0x4547 + 0x6 - 0x21ed = 0x2360
;   0x4559 + 0x6 - 0x2207 = 0x2358
;   0x4567 + 0x6 - 0x2235 = 0x2338
;   0x4575 + 0x6 - 0x2223 = 0x2358
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x170
mov r13d, r8d
test rdx, rdx
je 0x457f
cmp rdx, 255
ja 0x457f
mov rbx, rcx
mov r12, rdx
xor eax, eax
cmp rax, r12
jae 0x4446
movzx r9d, byte ptr [rbx + rax]
mov byte ptr [rsp + rax + 0x20], r9b
add rax, 1
jmp 0x4431
mov byte ptr [rsp + rax + 0x20], 0
mov qword ptr [rsp + 0x120], 0
mov qword ptr [rsp + 0x128], 0
mov qword ptr [rsp + 0x130], 0
mov qword ptr [rsp + 0x138], 0
mov qword ptr [rsp + 0x140], 0
mov qword ptr [rsp + 0x148], 0
mov dword ptr [rsp + 0x124], 2
mov dword ptr [rsp + 0x128], 1
lea rcx, [rsp + 0x20]
xor edx, edx
lea r8, [rsp + 0x120]
lea r9, [rsp + 0x160]
call qword ptr [rip - 0x2176]
test eax, eax
jne 0x457f
mov rbx, qword ptr [rsp + 0x160]
test rbx, rbx
je 0x456d
cmp dword ptr [rbx + 4], 2
je 0x44eb
mov rbx, qword ptr [rbx + 40]
jmp 0x44d6
mov r12, qword ptr [rbx + 32]
mov rax, qword ptr [r12]
mov qword ptr [rsp + 0x150], rax
mov rax, qword ptr [r12 + 8]
mov qword ptr [rsp + 0x158], rax
mov eax, r13d
rol ax, 8
mov word ptr [rsp + 0x152], ax
mov ecx, 2
mov edx, 1
mov r8d, 6
call qword ptr [rip - 0x2225]
cmp rax, -1
je 0x456d
mov r14, rax
mov rcx, r14
lea rdx, [rsp + 0x150]
mov r8d, 16
call qword ptr [rip - 0x21ed]
test eax, eax
jne 0x4564
mov rcx, qword ptr [rsp + 0x160]
call qword ptr [rip - 0x2207]
mov rax, r14
jmp 0x4581
mov rcx, r14
call qword ptr [rip - 0x2235]
mov rcx, qword ptr [rsp + 0x160]
call qword ptr [rip - 0x2223]
xor eax, eax
jmp 0x4581
xor eax, eax
add rsp, 0x170
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
