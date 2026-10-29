; tcp-13-connexion · brouillon · connexion cliente résolue · tcp-13:R1 · e50013
; le pendant client de tcp-01 pour une cible ARBITRAIRE : getaddrinfo (DNS ou
; littéral, IPv4) puis connect sur la première adresse AF_INET ; la traduction
; span -> chaîne C (Q2) est la propriété UNIQUE de ce bloc ; le port passe en
; ordre réseau par une instruction du bloc (I3 — rol, aucune entrée IAT htons) ;
; nettoyage COMPLET sur tout chemin (Q4) : freeaddrinfo si résolu, closesocket
; si créée ; WSACleanup JAMAIS (Q5).
; entrée : rcx = span hôte (crochets exclus par http-07), rdx = longueur,
;          r8d = port (ordre hôte)
; sortie : rax = socket amont connectée (non nulle) / 0 échec nommé
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x170
; cadre : [rsp,0x20) shadow ; hôte [0x20,0x120) 256 o ; hints [0x120,0x150) ;
; sockaddr [0x150,0x160) ; résultat [0x160,0x168)
mov r13d, r8d
test rdx, rdx
je .echec
cmp rdx, 255
ja .echec
mov rbx, rcx
mov r12, rdx
xor eax, eax
.copie:
cmp rax, r12
jae .copie_fin
movzx r9d, byte ptr [rbx + rax]
mov byte ptr [rsp + rax + 0x20], r9b
add rax, 1
jmp .copie
.copie_fin:
mov byte ptr [rsp + rax + 0x20], 0
; hints : zéro, AF_INET, SOCK_STREAM, protocole 0 (Q3)
mov qword ptr [rsp + 0x120], 0
mov qword ptr [rsp + 0x128], 0
mov qword ptr [rsp + 0x130], 0
mov qword ptr [rsp + 0x138], 0
mov qword ptr [rsp + 0x140], 0
mov qword ptr [rsp + 0x148], 0
mov dword ptr [rsp + 0x124], 2
mov dword ptr [rsp + 0x128], 1
; getaddrinfo(hôte, NULL, hints, &résultat)
lea rcx, [rsp + 0x20]
xor edx, edx
lea r8, [rsp + 0x120]
lea r9, [rsp + 0x160]
call qword ptr [rip + IAT_GETADDRINFO]
test eax, eax
jne .echec
; parcours défensif : première entrée AF_INET
mov rbx, qword ptr [rsp + 0x160]
.parcours:
test rbx, rbx
je .liberer_echec
cmp dword ptr [rbx + 4], 2
je .addrinfo_trouve
mov rbx, qword ptr [rbx + 40]
jmp .parcours
.addrinfo_trouve:
mov r12, qword ptr [rbx + 32]
mov rax, qword ptr [r12]
mov qword ptr [rsp + 0x150], rax
mov rax, qword ptr [r12 + 8]
mov qword ptr [rsp + 0x158], rax
; port en ordre réseau (I3) — écrit par ce bloc depuis P3
mov eax, r13d
rol ax, 8
mov word ptr [rsp + 0x152], ax
; socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
mov ecx, 2
mov edx, 1
mov r8d, 6
call qword ptr [rip + IAT_SOCKET]
cmp rax, -1
je .liberer_echec
mov r14, rax
; connect(socket, sockaddr, 16)
mov rcx, r14
lea rdx, [rsp + 0x150]
mov r8d, 16
call qword ptr [rip + IAT_CONNECT]
test eax, eax
jne .fermer_echec
mov rcx, qword ptr [rsp + 0x160]
call qword ptr [rip + IAT_FREEADDRINFO]
mov rax, r14
jmp .fin
.fermer_echec:
mov rcx, r14
call qword ptr [rip + IAT_CLOSESOCK]
.liberer_echec:
mov rcx, qword ptr [rsp + 0x160]
call qword ptr [rip + IAT_FREEADDRINFO]
xor eax, eax
jmp .fin
.echec:
xor eax, eax
.fin:
add rsp, 0x170
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
