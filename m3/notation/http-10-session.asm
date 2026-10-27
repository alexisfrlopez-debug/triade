; http-10-session · bloc session proxy · spec http-10:R2 · bloc carte e50010
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x5580, taille 2048 octets
; Dépendances : blocs tcp-03/04/05/06/11, tcp-13, http-01..09 ; IAT kernel32 CloseHandle (handle de la pompe détachée) ; chaînes .rdata ; R2 : corps de requête borné Content-Length INLINE (tcp-03/04), http-09 réservé au tunnel et au relais de réponse
; Notation explicite générée par outils/auteur.py depuis brouillons/http-10-session.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 1847 o · padding : 201 o (NOP)
; Étiquettes résolues : .probe=0x5590, .accumuler=0x55df, .tete_complete=0x5627, .requete_ok=0x5677, .cible_ok=0x57a3, .origine_host=0x57c4, .forme_absolue=0x57dc, .forme_autorite=0x57f4, .resoudre=0x5807, .sans_te=0x5838, .valider_cl=0x5861, .trancher=0x5882, .corps_deja=0x5a28, .corps_reste_nul=0x5a53, .corps_pomper=0x5a56, .corps_boucle=0x5a5b, .corps_cap=0x5a6e, .relais_reponse=0x5aae, .tunnel=0x5ac8, .fin=0x5b6a, .fin_cliente=0x5b77, .repondre_400=0x5bb3, .repondre_431=0x5bc3, .repondre_501=0x5bd3, .repondre_411=0x5be3, .repondre_505=0x5bf3, .repondre_502=0x5c03, .repondre=0x5c11, .emettre=0x5c1e, .envoyer=0x5c31, .emis=0x5c4c, .emis_ko=0x5c50, .emettre_fin=0x5c55, .copier=0x5c5b, .copie_boucle=0x5c6e, .copie_fin=0x5c83, .pompe_amont=0x5c89
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x55b9 + 0x7 - 0x2d50 = 0x2870
;   0x5691 + 0x7 - 0x2d48 = 0x2950
;   0x56da + 0x7 - 0x2d81 = 0x2960
;   0x5728 + 0x7 - 0x2dbf = 0x2970
;   0x5af1 + 0x7 - 0x34b8 = 0x2640
;   0x5b0c + 0x7 - 0x3283 = 0x2890
;   0x5b2f + 0x7 + 0x153 = 0x5c89
;   0x5b4d + 0x6 - 0x3a5b = 0x20f8
;   0x5b7f + 0x7 - 0x32e6 = 0x28a0
;   0x5bb3 + 0x7 - 0x365a = 0x2560
;   0x5bc3 + 0x7 - 0x3646 = 0x2584
;   0x5bd3 + 0x7 - 0x3632 = 0x25a8
;   0x5be3 + 0x7 - 0x3622 = 0x25c8
;   0x5bf3 + 0x7 - 0x360e = 0x25ec
;   0x5c03 + 0x7 - 0x35f6 = 0x2614
push rbx
push r12
push r13
push r14
push r15
mov r10, 0xfffffffffffff000
mov rax, qword ptr [rsp + r10]
sub r10, 0x1000
cmp r10, -0x7000
jge 0x5590
mov rax, qword ptr [rsp - 0x7100]
sub rsp, 0x7100
mov rbx, rcx
xor r12d, r12d
lea rcx, [rip - 0x2d50]
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
je 0x5627
cmp rax, 2
je 0x5bc3
cmp rax, 3
je 0x5bb3
mov rcx, rbx
lea rdx, [rsp + r13]
mov r8, 0x4000
sub r8, r13
call 0x4140
test rax, rax
jle 0x5b6a
add r13, rax
jmp 0x55df
mov r14, rdx
mov rcx, rsp
mov rdx, r14
xor r8d, r8d
call 0x4c00
mov qword ptr [rsp + 0x6FE0], r8
test rdx, rdx
je 0x5bb3
mov rcx, rsp
lea r8, [rsp + 0x6F00]
call 0x4c80
test rax, rax
je 0x5677
cmp rax, 1
je 0x5bd3
cmp rax, 3
je 0x5bf3
jmp 0x5bb3
mov r10, qword ptr [rsp + 0x6FE0]
lea rcx, [rsp + r10]
mov r11, r14
sub r11, r10
mov qword ptr [rsp + 0x6FE8], r11
lea r8, [rip - 0x2d48]
mov r9, 4
mov rdx, r11
lea rax, [rsp + 0x6F40]
sub rsp, 0x30
mov qword ptr [rsp + 0x20], rax
call 0x4f40
add rsp, 0x30
mov qword ptr [rsp + 0x6FF0], rax
cmp rax, 2
je 0x5bb3
mov r10, qword ptr [rsp + 0x6FE0]
lea rcx, [rsp + r10]
lea r8, [rip - 0x2d81]
mov r9, 14
mov rdx, qword ptr [rsp + 0x6FE8]
lea rax, [rsp + 0x6F60]
sub rsp, 0x30
mov qword ptr [rsp + 0x20], rax
call 0x4f40
add rsp, 0x30
mov qword ptr [rsp + 0x6FF8], rax
cmp rax, 2
je 0x5bb3
mov r10, qword ptr [rsp + 0x6FE0]
lea rcx, [rsp + r10]
lea r8, [rip - 0x2dbf]
mov r9, 17
mov rdx, qword ptr [rsp + 0x6FE8]
lea rax, [rsp + 0x6F80]
sub rsp, 0x30
mov qword ptr [rsp + 0x20], rax
call 0x4f40
add rsp, 0x30
mov qword ptr [rsp + 0x7000], rax
cmp rax, 2
je 0x5bb3
mov rcx, qword ptr [rsp + 0x6F18]
mov rdx, qword ptr [rsp + 0x6F20]
mov r8d, dword ptr [rsp + 0x6F00]
lea r9, [rsp + 0x6FB8]
call 0x5380
test rax, rax
je 0x57a3
cmp rax, 3
je 0x5bd3
jmp 0x5bb3
mov eax, dword ptr [rsp + 0x6FB8]
cmp eax, 3
je 0x57f4
cmp eax, 1
je 0x57dc
cmp qword ptr [rsp + 0x6FF0], 0
je 0x57c4
jmp 0x5bb3
mov rcx, qword ptr [rsp + 0x6F50]
mov rdx, qword ptr [rsp + 0x6F58]
mov r8d, 80
jmp 0x5807
mov rcx, qword ptr [rsp + 0x6FC0]
mov rdx, qword ptr [rsp + 0x6FC8]
mov r8d, 80
jmp 0x5807
mov rcx, qword ptr [rsp + 0x6FC0]
mov rdx, qword ptr [rsp + 0x6FC8]
xor r8d, r8d
lea r9, [rsp + 0x6FA0]
call 0x5200
test rax, rax
jne 0x5bb3
cmp qword ptr [rsp + 0x7000], 0
jne 0x5838
cmp qword ptr [rsp + 0x6F98], 0
je 0x5838
jmp 0x5bd3
cmp qword ptr [rsp + 0x6FF8], 0
je 0x5861
mov eax, dword ptr [rsp + 0x6F00]
cmp eax, 3
je 0x5be3
cmp eax, 4
je 0x5be3
xor r15d, r15d
jmp 0x5882
mov rcx, qword ptr [rsp + 0x6F70]
mov rdx, qword ptr [rsp + 0x6F78]
call 0x5080
test rax, rax
jne 0x5bb3
mov r15d, edx
cmp dword ptr [rsp + 0x6F00], 8
je 0x5ac8
mov rcx, qword ptr [rsp + 0x6FA0]
mov rdx, qword ptr [rsp + 0x6FA8]
mov r8d, dword ptr [rsp + 0x6FB0]
call 0x4400
test rax, rax
je 0x5c03
mov r12, rax
mov qword ptr [rsp + 0x7008], 0
mov rdx, qword ptr [rsp + 0x6F08]
mov r8, qword ptr [rsp + 0x6F10]
lea rcx, [rsp + 0x4000]
add rcx, qword ptr [rsp + 0x7008]
call 0x5c5b
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
call 0x5c5b
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
call 0x5c5b
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
call 0x5c5b
mov r10, qword ptr [rsp + 0x6FE0]
mov rax, r14
sub rax, r10
add qword ptr [rsp + 0x7008], rax
mov rcx, r12
lea rdx, [rsp + 0x4000]
mov r8, qword ptr [rsp + 0x7008]
call 0x5c1e
test rax, rax
jne 0x5b6a
mov rax, r13
sub rax, r14
cmp rax, r15
jbe 0x5a28
mov rax, r15
mov r8, rax
lea rdx, [rsp + r14]
mov rcx, r12
call 0x5c1e
test rax, rax
jne 0x5b6a
mov rax, r13
sub rax, r14
cmp rax, r15
jae 0x5a53
mov r14, r15
sub r14, rax
jmp 0x5a56
xor r14d, r14d
test r14, r14
je 0x5aae
mov r8, r14
cmp r8, 0x4000
jbe 0x5a6e
mov r8, 0x4000
mov rcx, rbx
mov rdx, rsp
call 0x4140
test rax, rax
jle 0x5b6a
mov qword ptr [rsp + 0x7018], rax
mov r8, rax
mov rdx, rsp
mov rcx, r12
call 0x5c1e
test rax, rax
jne 0x5b6a
mov rax, qword ptr [rsp + 0x7018]
sub r14, rax
jne 0x5a5b
mov rcx, r12
mov rdx, rbx
mov r8, rsp
mov r9, 0x4000
call 0x54c0
jmp 0x5b6a
mov rcx, qword ptr [rsp + 0x6FA0]
mov rdx, qword ptr [rsp + 0x6FA8]
mov r8d, dword ptr [rsp + 0x6FB0]
call 0x4400
test rax, rax
je 0x5c03
mov r12, rax
lea rdx, [rip - 0x34b8]
mov r8, 30
mov rcx, rbx
call 0x5c1e
test rax, rax
jne 0x5b6a
lea rcx, [rip - 0x3283]
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
je 0x5b6a
mov rcx, rax
call qword ptr [rip - 0x3a5b]
mov rcx, rbx
mov rdx, r12
mov r8, rsp
mov r9, 0x4000
call 0x54c0
jmp 0x5b6a
test r12, r12
je 0x5b77
mov rcx, r12
call 0x41c0
mov rcx, rbx
call 0x41c0
lea rcx, [rip - 0x32e6]
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
lea rdx, [rip - 0x365a]
mov r8, 35
jmp 0x5c11
lea rdx, [rip - 0x3646]
mov r8, 33
jmp 0x5c11
lea rdx, [rip - 0x3632]
mov r8, 31
jmp 0x5c11
lea rdx, [rip - 0x3622]
mov r8, 33
jmp 0x5c11
lea rdx, [rip - 0x360e]
mov r8, 38
jmp 0x5c11
lea rdx, [rip - 0x35f6]
mov r8, 40
mov rcx, rbx
call 0x5c1e
jmp 0x5b6a
push rbx
push r12
push r13
mov rbx, rcx
mov r12, rdx
mov r13, r8
test r13, r13
je 0x5c4c
mov rcx, rbx
mov rdx, r12
mov r8, r13
call 0x4180
test rax, rax
jle 0x5c50
add r12, rax
sub r13, rax
jne 0x5c31
xor eax, eax
jmp 0x5c55
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
je 0x5c83
movzx eax, byte ptr [r12]
mov byte ptr [rbx], al
add rbx, 1
add r12, 1
sub r13, 1
jne 0x5c6e
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
