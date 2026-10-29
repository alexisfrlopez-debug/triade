; http-10-session-r2 · bloc session proxy — révision routage TLS · spec http-10:R2 · bloc carte g70010
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x74c0, taille 2304 octets
; Dépendances : RÉVISION (ancêtre http-10 scellé 0.4.0, cité § 9) : routage https → tls-08 + table des réponses étendue (certificat invalide → 502 « certificat rejete »)
; Notation explicite générée par outils/auteur.py depuis brouillons/http-10-session-r2.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 2125 o · padding : 179 o (NOP)
; Étiquettes résolues : .probe=0x74d0, .accumuler=0x751f, .tete_complete=0x7567, .requete_ok=0x75b7, .cible_tls=0x76f1, .cible_ok=0x7709, .origine_host=0x772a, .forme_absolue=0x7742, .forme_autorite=0x775a, .resoudre=0x776d, .sans_te=0x779e, .valider_cl=0x77c7, .trancher=0x77e8, .reecriture=0x782e, .tls_garde=0x7a24, .emission_amont=0x7a32, .corps_deja=0x7a61, .corps_reste_nul=0x7a8c, .corps_pomper=0x7a8f, .corps_boucle=0x7a94, .corps_cap=0x7aa7, .relais_reponse=0x7ae7, .tunnel=0x7b01, .fin=0x7ba3, .fin_cliente=0x7bb0, .repondre_400=0x7bec, .repondre_431=0x7bfc, .repondre_501=0x7c0c, .repondre_411=0x7c1c, .repondre_505=0x7c2c, .repondre_502=0x7c3c, .repondre_502_cert=0x7c57, .repondre=0x7c67, .emettre=0x7c74, .envoyer=0x7c87, .emis=0x7ca2, .emis_ko=0x7ca6, .emettre_fin=0x7cab, .copier=0x7cb1, .copie_boucle=0x7cc4, .copie_fin=0x7cd9, .pompe_amont=0x7cdf
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x74f9 + 0x7 - 0x4c90 = 0x2870
;   0x75d1 + 0x7 - 0x4c88 = 0x2950
;   0x761a + 0x7 - 0x4cc1 = 0x2960
;   0x7668 + 0x7 - 0x4cff = 0x2970
;   0x7b2a + 0x7 - 0x54f1 = 0x2640
;   0x7b45 + 0x7 - 0x52bc = 0x2890
;   0x7b68 + 0x7 + 0x170 = 0x7cdf
;   0x7b86 + 0x6 - 0x5a94 = 0x20f8
;   0x7bb8 + 0x7 - 0x531f = 0x28a0
;   0x7bec + 0x7 - 0x5693 = 0x2560
;   0x7bfc + 0x7 - 0x567f = 0x2584
;   0x7c0c + 0x7 - 0x566b = 0x25a8
;   0x7c1c + 0x7 - 0x565b = 0x25c8
;   0x7c2c + 0x7 - 0x5647 = 0x25ec
;   0x7c3c + 0x7 - 0x562f = 0x2614
;   0x7c57 + 0x7 - 0x4fbe = 0x2ca0
push rbx
push r12
push r13
push r14
push r15
mov r10, -0x1000
mov rax, qword ptr [rsp + r10]
sub r10, 0x1000
cmp r10, -0x13000
jge 0x74d0
mov rax, qword ptr [rsp - 0x13390]
sub rsp, 0x13390
mov rbx, rcx
xor r12d, r12d
lea rcx, [rip - 0x4c90]
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
je 0x7567
cmp rax, 2
je 0x7bfc
cmp rax, 3
je 0x7bec
mov rcx, rbx
lea rdx, [rsp + r13]
mov r8, 0x4000
sub r8, r13
call 0x4140
test rax, rax
jle 0x7ba3
add r13, rax
jmp 0x751f
mov r14, rdx
mov rcx, rsp
mov rdx, r14
xor r8d, r8d
call 0x4c00
mov qword ptr [rsp + 0x6FE0], r8
test rdx, rdx
je 0x7bec
mov rcx, rsp
lea r8, [rsp + 0x6F00]
call 0x4c80
test rax, rax
je 0x75b7
cmp rax, 1
je 0x7c0c
cmp rax, 3
je 0x7c2c
jmp 0x7bec
mov r10, qword ptr [rsp + 0x6FE0]
lea rcx, [rsp + r10]
mov r11, r14
sub r11, r10
mov qword ptr [rsp + 0x6FE8], r11
lea r8, [rip - 0x4c88]
mov r9, 4
mov rdx, r11
lea rax, [rsp + 0x6F40]
sub rsp, 0x30
mov qword ptr [rsp + 0x20], rax
call 0x4f40
add rsp, 0x30
mov qword ptr [rsp + 0x6FF0], rax
cmp rax, 2
je 0x7bec
mov r10, qword ptr [rsp + 0x6FE0]
lea rcx, [rsp + r10]
lea r8, [rip - 0x4cc1]
mov r9, 14
mov rdx, qword ptr [rsp + 0x6FE8]
lea rax, [rsp + 0x6F60]
sub rsp, 0x30
mov qword ptr [rsp + 0x20], rax
call 0x4f40
add rsp, 0x30
mov qword ptr [rsp + 0x6FF8], rax
cmp rax, 2
je 0x7bec
mov r10, qword ptr [rsp + 0x6FE0]
lea rcx, [rsp + r10]
lea r8, [rip - 0x4cff]
mov r9, 17
mov rdx, qword ptr [rsp + 0x6FE8]
lea rax, [rsp + 0x6F80]
sub rsp, 0x30
mov qword ptr [rsp + 0x20], rax
call 0x4f40
add rsp, 0x30
mov qword ptr [rsp + 0x7000], rax
cmp rax, 2
je 0x7bec
mov rcx, qword ptr [rsp + 0x6F18]
mov rdx, qword ptr [rsp + 0x6F20]
mov r8d, dword ptr [rsp + 0x6F00]
lea r9, [rsp + 0x6FB8]
call 0x7340
mov qword ptr [rsp + 0x7010], rax
test rax, rax
je 0x7709
cmp rax, 3
je 0x7c0c
cmp rax, 4
je 0x76f1
jmp 0x7bec
mov rcx, qword ptr [rsp + 0x6FC0]
mov rdx, qword ptr [rsp + 0x6FC8]
mov r8d, 443
jmp 0x776d
mov eax, dword ptr [rsp + 0x6FB8]
cmp eax, 3
je 0x775a
cmp eax, 1
je 0x7742
cmp qword ptr [rsp + 0x6FF0], 0
je 0x772a
jmp 0x7bec
mov rcx, qword ptr [rsp + 0x6F50]
mov rdx, qword ptr [rsp + 0x6F58]
mov r8d, 80
jmp 0x776d
mov rcx, qword ptr [rsp + 0x6FC0]
mov rdx, qword ptr [rsp + 0x6FC8]
mov r8d, 80
jmp 0x776d
mov rcx, qword ptr [rsp + 0x6FC0]
mov rdx, qword ptr [rsp + 0x6FC8]
xor r8d, r8d
lea r9, [rsp + 0x6FA0]
call 0x5200
test rax, rax
jne 0x7bec
cmp qword ptr [rsp + 0x7000], 0
jne 0x779e
cmp qword ptr [rsp + 0x6F98], 0
je 0x779e
jmp 0x7c0c
cmp qword ptr [rsp + 0x6FF8], 0
je 0x77c7
mov eax, dword ptr [rsp + 0x6F00]
cmp eax, 3
je 0x7c1c
cmp eax, 4
je 0x7c1c
xor r15d, r15d
jmp 0x77e8
mov rcx, qword ptr [rsp + 0x6F70]
mov rdx, qword ptr [rsp + 0x6F78]
call 0x5080
test rax, rax
jne 0x7bec
mov r15d, edx
cmp qword ptr [rsp + 0x7010], 4
je 0x7a24
cmp dword ptr [rsp + 0x6F00], 8
je 0x7b01
mov rcx, qword ptr [rsp + 0x6FA0]
mov rdx, qword ptr [rsp + 0x6FA8]
mov r8d, dword ptr [rsp + 0x6FB0]
call 0x4400
test rax, rax
je 0x7c3c
mov r12, rax
mov qword ptr [rsp + 0x7008], 0
mov rdx, qword ptr [rsp + 0x6F08]
mov r8, qword ptr [rsp + 0x6F10]
lea rcx, [rsp + 0x4000]
add rcx, qword ptr [rsp + 0x7008]
call 0x7cb1
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
call 0x7cb1
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
call 0x7cb1
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
call 0x7cb1
mov r10, qword ptr [rsp + 0x6FE0]
mov rax, r14
sub rax, r10
add qword ptr [rsp + 0x7008], rax
cmp qword ptr [rsp + 0x7010], 4
jne 0x7a32
mov rax, qword ptr [rsp + 0x6FA0]
mov qword ptr [rsp + 0x7100], rax
mov rax, qword ptr [rsp + 0x6FA8]
mov qword ptr [rsp + 0x7108], rax
mov eax, dword ptr [rsp + 0x6FB0]
mov word ptr [rsp + 0x7110], ax
lea rax, [rsp + 0x4000]
mov qword ptr [rsp + 0x7118], rax
mov rax, qword ptr [rsp + 0x7008]
mov qword ptr [rsp + 0x7120], rax
mov qword ptr [rsp + 0x7128], rbx
mov qword ptr [rsp + 0x7020], rdi
lea rdi, [rsp + 0x7130]
xor eax, eax
mov rcx, 0x184C
rep stosq
mov rdi, qword ptr [rsp + 0x7020]
lea rcx, [rsp + 0x7130]
lea rdx, [rsp + 0x7100]
call 0x6d40
test rax, rax
je 0x7ba3
cmp eax, 3
je 0x7c57
jmp 0x7c3c
test r15, r15
jne 0x7c0c
jmp 0x782e
mov rcx, r12
lea rdx, [rsp + 0x4000]
mov r8, qword ptr [rsp + 0x7008]
call 0x7c74
test rax, rax
jne 0x7ba3
mov rax, r13
sub rax, r14
cmp rax, r15
jbe 0x7a61
mov rax, r15
mov r8, rax
lea rdx, [rsp + r14]
mov rcx, r12
call 0x7c74
test rax, rax
jne 0x7ba3
mov rax, r13
sub rax, r14
cmp rax, r15
jae 0x7a8c
mov r14, r15
sub r14, rax
jmp 0x7a8f
xor r14d, r14d
test r14, r14
je 0x7ae7
mov r8, r14
cmp r8, 0x4000
jbe 0x7aa7
mov r8, 0x4000
mov rcx, rbx
mov rdx, rsp
call 0x4140
test rax, rax
jle 0x7ba3
mov qword ptr [rsp + 0x7018], rax
mov r8, rax
mov rdx, rsp
mov rcx, r12
call 0x7c74
test rax, rax
jne 0x7ba3
mov rax, qword ptr [rsp + 0x7018]
sub r14, rax
jne 0x7a94
mov rcx, r12
mov rdx, rbx
mov r8, rsp
mov r9, 0x4000
call 0x54c0
jmp 0x7ba3
mov rcx, qword ptr [rsp + 0x6FA0]
mov rdx, qword ptr [rsp + 0x6FA8]
mov r8d, dword ptr [rsp + 0x6FB0]
call 0x4400
test rax, rax
je 0x7c3c
mov r12, rax
lea rdx, [rip - 0x54f1]
mov r8, 30
mov rcx, rbx
call 0x7c74
test rax, rax
jne 0x7ba3
lea rcx, [rip - 0x52bc]
mov edx, 8
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call 0x4b00
lea rcx, [rip + 0x170]
mov rdx, r12
shl rdx, 32
or rdx, rbx
call 0x4300
test rax, rax
je 0x7ba3
mov rcx, rax
call qword ptr [rip - 0x5a94]
mov rcx, rbx
mov rdx, r12
mov r8, rsp
mov r9, 0x4000
call 0x54c0
jmp 0x7ba3
test r12, r12
je 0x7bb0
mov rcx, r12
call 0x41c0
mov rcx, rbx
call 0x41c0
lea rcx, [rip - 0x531f]
mov edx, 15
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call 0x4b00
add rsp, 0x13390
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
lea rdx, [rip - 0x5693]
mov r8, 35
jmp 0x7c67
lea rdx, [rip - 0x567f]
mov r8, 33
jmp 0x7c67
lea rdx, [rip - 0x566b]
mov r8, 31
jmp 0x7c67
lea rdx, [rip - 0x565b]
mov r8, 33
jmp 0x7c67
lea rdx, [rip - 0x5647]
mov r8, 38
jmp 0x7c67
lea rdx, [rip - 0x562f]
mov r8, 40
mov rcx, rbx
call 0x7c74
jmp 0x7ba3
lea rdx, [rip - 0x4fbe]
mov r8, 34
jmp 0x7c67
mov rcx, rbx
call 0x7c74
jmp 0x7ba3
push rbx
push r12
push r13
mov rbx, rcx
mov r12, rdx
mov r13, r8
test r13, r13
je 0x7ca2
mov rcx, rbx
mov rdx, r12
mov r8, r13
call 0x4180
test rax, rax
jle 0x7ca6
add r12, rax
sub r13, rax
jne 0x7c87
xor eax, eax
jmp 0x7cab
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
je 0x7cd9
movzx eax, byte ptr [r12]
mov byte ptr [rbx], al
add rbx, 1
add r12, 1
sub r13, 1
jne 0x7cc4
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
