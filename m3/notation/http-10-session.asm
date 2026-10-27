; http-10-session · bloc session proxy · spec http-10:R2 · bloc carte e50010
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x5580, taille 2048 octets
; Dépendances : blocs tcp-03/04/05/06/11, tcp-13, http-01..09 ; IAT kernel32 CloseHandle (handle de la pompe détachée) ; chaînes .rdata ; R2 : corps de requête borné Content-Length INLINE (tcp-03/04), http-09 réservé au tunnel et au relais de réponse
; Notation explicite générée par outils/auteur.py depuis brouillons/http-10-session.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 1812 o · padding : 236 o (NOP)
; Étiquettes résolues : .accumuler=0x55bc, .tete_complete=0x5604, .requete_ok=0x5654, .cible_ok=0x5780, .origine_host=0x57a1, .forme_absolue=0x57b9, .forme_autorite=0x57d1, .resoudre=0x57e4, .sans_te=0x5815, .valider_cl=0x583e, .trancher=0x585f, .corps_deja=0x5a05, .corps_reste_nul=0x5a30, .corps_pomper=0x5a33, .corps_boucle=0x5a38, .corps_cap=0x5a4b, .relais_reponse=0x5a8b, .tunnel=0x5aa5, .fin=0x5b47, .fin_cliente=0x5b54, .repondre_400=0x5b90, .repondre_431=0x5ba0, .repondre_501=0x5bb0, .repondre_411=0x5bc0, .repondre_505=0x5bd0, .repondre_502=0x5be0, .repondre=0x5bee, .emettre=0x5bfb, .envoyer=0x5c0e, .emis=0x5c29, .emis_ko=0x5c2d, .emettre_fin=0x5c32, .copier=0x5c38, .copie_boucle=0x5c4b, .copie_fin=0x5c60, .pompe_amont=0x5c66
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x5596 + 0x7 - 0x2d2d = 0x2870
;   0x566e + 0x7 - 0x2d25 = 0x2950
;   0x56b7 + 0x7 - 0x2d5e = 0x2960
;   0x5705 + 0x7 - 0x2d9c = 0x2970
;   0x5ace + 0x7 - 0x3495 = 0x2640
;   0x5ae9 + 0x7 - 0x3260 = 0x2890
;   0x5b0c + 0x7 + 0x153 = 0x5c66
;   0x5b2a + 0x6 - 0x3a38 = 0x20f8
;   0x5b5c + 0x7 - 0x32c3 = 0x28a0
;   0x5b90 + 0x7 - 0x3637 = 0x2560
;   0x5ba0 + 0x7 - 0x3623 = 0x2584
;   0x5bb0 + 0x7 - 0x360f = 0x25a8
;   0x5bc0 + 0x7 - 0x35ff = 0x25c8
;   0x5bd0 + 0x7 - 0x35eb = 0x25ec
;   0x5be0 + 0x7 - 0x35d3 = 0x2614
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x7100
mov rbx, rcx
xor r12d, r12d
lea rcx, [rip - 0x2d2d]
mov edx, 20
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call 0x4b00
xor r13d, r13d
mov rcx, rsp
mov rdx, r13
call 0x5140
test rax, rax
je 0x5604
cmp rax, 2
je 0x5ba0
cmp rax, 3
je 0x5b90
mov rcx, rbx
lea rdx, [rsp + r13]
mov r8, 0x4000
sub r8, r13
call 0x4140
test rax, rax
jle 0x5b47
add r13, rax
jmp 0x55bc
mov r14, rdx
mov rcx, rsp
mov rdx, r14
xor r8d, r8d
call 0x4c00
mov qword ptr [rsp + 0x6FE0], r8
test rdx, rdx
je 0x5b90
mov rcx, rsp
lea r8, [rsp + 0x6F00]
call 0x4c80
test rax, rax
je 0x5654
cmp rax, 1
je 0x5bb0
cmp rax, 3
je 0x5bd0
jmp 0x5b90
mov r10, qword ptr [rsp + 0x6FE0]
lea rcx, [rsp + r10]
mov r11, r14
sub r11, r10
mov qword ptr [rsp + 0x6FE8], r11
lea r8, [rip - 0x2d25]
mov r9, 4
mov rdx, r11
lea rax, [rsp + 0x6F40]
sub rsp, 0x30
mov qword ptr [rsp + 0x20], rax
call 0x4f40
add rsp, 0x30
mov qword ptr [rsp + 0x6FF0], rax
cmp rax, 2
je 0x5b90
mov r10, qword ptr [rsp + 0x6FE0]
lea rcx, [rsp + r10]
lea r8, [rip - 0x2d5e]
mov r9, 14
mov rdx, qword ptr [rsp + 0x6FE8]
lea rax, [rsp + 0x6F60]
sub rsp, 0x30
mov qword ptr [rsp + 0x20], rax
call 0x4f40
add rsp, 0x30
mov qword ptr [rsp + 0x6FF8], rax
cmp rax, 2
je 0x5b90
mov r10, qword ptr [rsp + 0x6FE0]
lea rcx, [rsp + r10]
lea r8, [rip - 0x2d9c]
mov r9, 17
mov rdx, qword ptr [rsp + 0x6FE8]
lea rax, [rsp + 0x6F80]
sub rsp, 0x30
mov qword ptr [rsp + 0x20], rax
call 0x4f40
add rsp, 0x30
mov qword ptr [rsp + 0x7000], rax
cmp rax, 2
je 0x5b90
mov rcx, qword ptr [rsp + 0x6F18]
mov rdx, qword ptr [rsp + 0x6F20]
mov r8d, dword ptr [rsp + 0x6F00]
lea r9, [rsp + 0x6FB8]
call 0x5380
test rax, rax
je 0x5780
cmp rax, 3
je 0x5bb0
jmp 0x5b90
mov eax, dword ptr [rsp + 0x6FB8]
cmp eax, 3
je 0x57d1
cmp eax, 1
je 0x57b9
cmp qword ptr [rsp + 0x6FF0], 0
je 0x57a1
jmp 0x5b90
mov rcx, qword ptr [rsp + 0x6F50]
mov rdx, qword ptr [rsp + 0x6F58]
mov r8d, 80
jmp 0x57e4
mov rcx, qword ptr [rsp + 0x6FC0]
mov rdx, qword ptr [rsp + 0x6FC8]
mov r8d, 80
jmp 0x57e4
mov rcx, qword ptr [rsp + 0x6FC0]
mov rdx, qword ptr [rsp + 0x6FC8]
xor r8d, r8d
lea r9, [rsp + 0x6FA0]
call 0x5200
test rax, rax
jne 0x5b90
cmp qword ptr [rsp + 0x7000], 0
jne 0x5815
cmp qword ptr [rsp + 0x6F98], 0
je 0x5815
jmp 0x5bb0
cmp qword ptr [rsp + 0x6FF8], 0
je 0x583e
mov eax, dword ptr [rsp + 0x6F00]
cmp eax, 3
je 0x5bc0
cmp eax, 4
je 0x5bc0
xor r15d, r15d
jmp 0x585f
mov rcx, qword ptr [rsp + 0x6F70]
mov rdx, qword ptr [rsp + 0x6F78]
call 0x5080
test rax, rax
jne 0x5b90
mov r15d, edx
cmp dword ptr [rsp + 0x6F00], 8
je 0x5aa5
mov rcx, qword ptr [rsp + 0x6FA0]
mov rdx, qword ptr [rsp + 0x6FA8]
mov r8d, dword ptr [rsp + 0x6FB0]
call 0x4400
test rax, rax
je 0x5be0
mov r12, rax
mov qword ptr [rsp + 0x7008], 0
mov rdx, qword ptr [rsp + 0x6F08]
mov r8, qword ptr [rsp + 0x6F10]
lea rcx, [rsp + 0x4000]
add rcx, qword ptr [rsp + 0x7008]
call 0x5c38
mov rax, qword ptr [rsp + 0x6F10]
add qword ptr [rsp + 0x7008], rax
lea rcx, [rsp + 0x4000]
add rcx, qword ptr [rsp + 0x7008]
mov byte ptr [rcx], 0x20
add qword ptr [rsp + 0x7008], 1
mov rdx, qword ptr [rsp + 0x6FD0]
mov r8, qword ptr [rsp + 0x6FD8]
lea rcx, [rsp + 0x4000]
add rcx, qword ptr [rsp + 0x7008]
call 0x5c38
mov rax, qword ptr [rsp + 0x6FD8]
add qword ptr [rsp + 0x7008], rax
lea rcx, [rsp + 0x4000]
add rcx, qword ptr [rsp + 0x7008]
mov byte ptr [rcx], 0x20
add qword ptr [rsp + 0x7008], 1
mov rdx, qword ptr [rsp + 0x6F28]
mov r8, qword ptr [rsp + 0x6F30]
lea rcx, [rsp + 0x4000]
add rcx, qword ptr [rsp + 0x7008]
call 0x5c38
mov rax, qword ptr [rsp + 0x6F30]
add qword ptr [rsp + 0x7008], rax
lea rcx, [rsp + 0x4000]
add rcx, qword ptr [rsp + 0x7008]
mov word ptr [rcx], 0x0A0D
add qword ptr [rsp + 0x7008], 2
mov r10, qword ptr [rsp + 0x6FE0]
lea rcx, [rsp + 0x4000]
add rcx, qword ptr [rsp + 0x7008]
mov rdx, rsp
add rdx, r10
mov r8, r14
sub r8, r10
call 0x5c38
mov r10, qword ptr [rsp + 0x6FE0]
mov rax, r14
sub rax, r10
add qword ptr [rsp + 0x7008], rax
mov rcx, r12
lea rdx, [rsp + 0x4000]
mov r8, qword ptr [rsp + 0x7008]
call 0x5bfb
test rax, rax
jne 0x5b47
mov rax, r13
sub rax, r14
cmp rax, r15
jbe 0x5a05
mov rax, r15
mov r8, rax
lea rdx, [rsp + r14]
mov rcx, r12
call 0x5bfb
test rax, rax
jne 0x5b47
mov rax, r13
sub rax, r14
cmp rax, r15
jae 0x5a30
mov r14, r15
sub r14, rax
jmp 0x5a33
xor r14d, r14d
test r14, r14
je 0x5a8b
mov r8, r14
cmp r8, 0x4000
jbe 0x5a4b
mov r8, 0x4000
mov rcx, rbx
mov rdx, rsp
call 0x4140
test rax, rax
jle 0x5b47
mov qword ptr [rsp + 0x7018], rax
mov r8, rax
mov rdx, rsp
mov rcx, r12
call 0x5bfb
test rax, rax
jne 0x5b47
mov rax, qword ptr [rsp + 0x7018]
sub r14, rax
jne 0x5a38
mov rcx, r12
mov rdx, rbx
mov r8, rsp
mov r9, 0x4000
call 0x54c0
jmp 0x5b47
mov rcx, qword ptr [rsp + 0x6FA0]
mov rdx, qword ptr [rsp + 0x6FA8]
mov r8d, dword ptr [rsp + 0x6FB0]
call 0x4400
test rax, rax
je 0x5be0
mov r12, rax
lea rdx, [rip - 0x3495]
mov r8, 30
mov rcx, rbx
call 0x5bfb
test rax, rax
jne 0x5b47
lea rcx, [rip - 0x3260]
mov edx, 8
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call 0x4b00
lea rcx, [rip + 0x153]
mov rdx, r12
shl rdx, 32
or rdx, rbx
call 0x4300
test rax, rax
je 0x5b47
mov rcx, rax
call qword ptr [rip - 0x3a38]
mov rcx, rbx
mov rdx, r12
mov r8, rsp
mov r9, 0x4000
call 0x54c0
jmp 0x5b47
test r12, r12
je 0x5b54
mov rcx, r12
call 0x41c0
mov rcx, rbx
call 0x41c0
lea rcx, [rip - 0x32c3]
mov edx, 15
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call 0x4b00
add rsp, 0x7100
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
lea rdx, [rip - 0x3637]
mov r8, 35
jmp 0x5bee
lea rdx, [rip - 0x3623]
mov r8, 33
jmp 0x5bee
lea rdx, [rip - 0x360f]
mov r8, 31
jmp 0x5bee
lea rdx, [rip - 0x35ff]
mov r8, 33
jmp 0x5bee
lea rdx, [rip - 0x35eb]
mov r8, 38
jmp 0x5bee
lea rdx, [rip - 0x35d3]
mov r8, 40
mov rcx, rbx
call 0x5bfb
jmp 0x5b47
push rbx
push r12
push r13
mov rbx, rcx
mov r12, rdx
mov r13, r8
test r13, r13
je 0x5c29
mov rcx, rbx
mov rdx, r12
mov r8, r13
call 0x4180
test rax, rax
jle 0x5c2d
add r12, rax
sub r13, rax
jne 0x5c0e
xor eax, eax
jmp 0x5c32
mov eax, 1
pop r13
pop r12
pop rbx
ret
push rbx
push r12
push r13
mov rbx, rcx
mov r12, rdx
mov r13, r8
test r13, r13
je 0x5c60
movzx eax, byte ptr [r12]
mov byte ptr [rbx], al
add rbx, 1
add r12, 1
sub r13, 1
jne 0x5c4b
pop r13
pop r12
pop rbx
ret
mov rax, rcx
mov rdx, rcx
shr rax, 32
mov edx, edx
mov ecx, eax
sub rsp, 0x1028
lea r8, [rsp + 0x28]
mov r9, 4096
call 0x54c0
add rsp, 0x1028
ret
