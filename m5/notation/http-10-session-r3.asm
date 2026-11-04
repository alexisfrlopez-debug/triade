; http-10-session-r3 · bloc session proxy — routage du relèvement + ligne de flux · spec http-10:R3 · bloc carte g80002
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x81c0, taille 2752 octets
; Dépendances : RÉVISION (ancêtre g70010 http-10:R2 embarqué 0.5.1, cité § 9) : le routage du verdict 5 par LE MÊME chemin Q2' + LA LIGNE DE FLUX (tcp-11, zéro secret)
; Notation explicite générée par outils/auteur.py depuis brouillons/http-10-session-r3.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 2719 o · padding : 33 o (NOP)
; Étiquettes résolues : .probe=0x81d2, .accumuler=0x8231, .tete_complete=0x827c, .requete_ok=0x82cc, .cible_tls=0x8428, .cible_ok=0x8440, .origine_host=0x8461, .forme_absolue=0x8479, .forme_autorite=0x8491, .resoudre=0x84a4, .pas_releve=0x84d0, .flux_hote=0x853f, .sans_te=0x8597, .valider_cl=0x85d8, .trancher=0x85f9, .reecriture=0x865a, .paquet_tls=0x87b4, .tls_garde=0x8863, .emission_amont=0x887d, .corps_deja=0x88ac, .corps_reste_nul=0x88d7, .corps_pomper=0x88da, .corps_boucle=0x88df, .corps_cap=0x88f2, .relais_reponse=0x8935, .tunnel=0x895b, .fin=0x8a15, .fin_r1=0x8af0, .fin_cliente=0x8afd, .repondre_400=0x8b3b, .repondre_431=0x8b4b, .repondre_501=0x8b5b, .repondre_411=0x8b6b, .repondre_505=0x8b7b, .repondre_502=0x8b8b, .repondre_502_cert=0x8ba6, .repondre=0x8bb6, .emettre=0x8bc3, .envoyer=0x8bd6, .emis=0x8bf4, .emis_ko=0x8bf8, .emettre_fin=0x8bfd, .copier=0x8c03, .copie_boucle=0x8c16, .copie_fin=0x8c2b, .pompe_amont=0x8c31
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x820b + 0x7 - 0x59a2 = 0x2870
;   0x82e6 + 0x7 - 0x599d = 0x2950
;   0x832f + 0x7 - 0x59d6 = 0x2960
;   0x837d + 0x7 - 0x5a14 = 0x2970
;   0x83df + 0x7 - 0x4b86 = 0x3860
;   0x84f3 + 0x7 - 0x60ea = 0x2410
;   0x899c + 0x7 - 0x6363 = 0x2640
;   0x89b7 + 0x7 - 0x612e = 0x2890
;   0x89da + 0x7 + 0x250 = 0x8c31
;   0x89f8 + 0x6 - 0x6906 = 0x20f8
;   0x8b05 + 0x7 - 0x626c = 0x28a0
;   0x8b3b + 0x7 - 0x65e2 = 0x2560
;   0x8b4b + 0x7 - 0x65ce = 0x2584
;   0x8b5b + 0x7 - 0x65ba = 0x25a8
;   0x8b6b + 0x7 - 0x65aa = 0x25c8
;   0x8b7b + 0x7 - 0x6596 = 0x25ec
;   0x8b8b + 0x7 - 0x657e = 0x2614
;   0x8ba6 + 0x7 - 0x5f0d = 0x2ca0
push rbx
push r12
push r13
push r14
push r15
push rsi
push rdi
mov r10, -0x1000
mov rax, qword ptr [rsp + r10]
sub r10, 0x1000
cmp r10, -0x13000
jge 0x81d2
mov rax, qword ptr [rsp - 0x13390]
sub rsp, 0x13390
xor esi, esi
xor edi, edi
mov qword ptr [rsp + 0x7028], -1
mov rbx, rcx
xor r12d, r12d
lea rcx, [rip - 0x59a2]
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
je 0x827c
cmp rax, 2
je 0x8b4b
cmp rax, 3
je 0x8b3b
mov rcx, rbx
lea rdx, [rsp + r13]
mov r8, 0x4000
sub r8, r13
call 0x4140
test rax, rax
jle 0x8a15
add r13, rax
add rsi, rax
jmp 0x8231
mov r14, rdx
mov rcx, rsp
mov rdx, r14
xor r8d, r8d
call 0x4c00
mov qword ptr [rsp + 0x6FE0], r8
test rdx, rdx
je 0x8b3b
mov rcx, rsp
lea r8, [rsp + 0x6F00]
call 0x4c80
test rax, rax
je 0x82cc
cmp rax, 1
je 0x8b5b
cmp rax, 3
je 0x8b7b
jmp 0x8b3b
mov r10, qword ptr [rsp + 0x6FE0]
lea rcx, [rsp + r10]
mov r11, r14
sub r11, r10
mov qword ptr [rsp + 0x6FE8], r11
lea r8, [rip - 0x599d]
mov r9, 4
mov rdx, r11
lea rax, [rsp + 0x6F40]
sub rsp, 0x30
mov qword ptr [rsp + 0x20], rax
call 0x4f40
add rsp, 0x30
mov qword ptr [rsp + 0x6FF0], rax
cmp rax, 2
je 0x8b3b
mov r10, qword ptr [rsp + 0x6FE0]
lea rcx, [rsp + r10]
lea r8, [rip - 0x59d6]
mov r9, 14
mov rdx, qword ptr [rsp + 0x6FE8]
lea rax, [rsp + 0x6F60]
sub rsp, 0x30
mov qword ptr [rsp + 0x20], rax
call 0x4f40
add rsp, 0x30
mov qword ptr [rsp + 0x6FF8], rax
cmp rax, 2
je 0x8b3b
mov r10, qword ptr [rsp + 0x6FE0]
lea rcx, [rsp + r10]
lea r8, [rip - 0x5a14]
mov r9, 17
mov rdx, qword ptr [rsp + 0x6FE8]
lea rax, [rsp + 0x6F80]
sub rsp, 0x30
mov qword ptr [rsp + 0x20], rax
call 0x4f40
add rsp, 0x30
mov qword ptr [rsp + 0x7000], rax
cmp rax, 2
je 0x8b3b
mov rcx, qword ptr [rsp + 0x6F18]
mov rdx, qword ptr [rsp + 0x6F20]
mov r8d, dword ptr [rsp + 0x6F00]
lea r9, [rsp + 0x6FB8]
mov rax, qword ptr [rip - 0x4b86]
mov qword ptr [rsp + 0x70D0], rax
sub rsp, 0x30
mov qword ptr [rsp + 0x28], rax
call 0x8000
add rsp, 0x30
mov qword ptr [rsp + 0x7010], rax
test rax, rax
je 0x8440
cmp rax, 3
je 0x8b5b
cmp rax, 4
je 0x8428
cmp rax, 5
je 0x8428
jmp 0x8b3b
mov rcx, qword ptr [rsp + 0x6FC0]
mov rdx, qword ptr [rsp + 0x6FC8]
mov r8d, 443
jmp 0x84a4
mov eax, dword ptr [rsp + 0x6FB8]
cmp eax, 3
je 0x8491
cmp eax, 1
je 0x8479
cmp qword ptr [rsp + 0x6FF0], 0
je 0x8461
jmp 0x8b3b
mov rcx, qword ptr [rsp + 0x6F50]
mov rdx, qword ptr [rsp + 0x6F58]
mov r8d, 80
jmp 0x84a4
mov rcx, qword ptr [rsp + 0x6FC0]
mov rdx, qword ptr [rsp + 0x6FC8]
mov r8d, 80
jmp 0x84a4
mov rcx, qword ptr [rsp + 0x6FC0]
mov rdx, qword ptr [rsp + 0x6FC8]
xor r8d, r8d
lea r9, [rsp + 0x6FA0]
call 0x5200
test rax, rax
jne 0x8b3b
cmp qword ptr [rsp + 0x7010], 5
jne 0x84d0
mov dword ptr [rsp + 0x6FB0], 443
lea r10, [rsp + 0x7030]
mov dword ptr [r10], 0x78756C66
mov byte ptr [r10 + 4], 0x20
add r10, 5
mov eax, dword ptr [rsp + 0x6F00]
shl rax, 4
lea r11, [rip - 0x60ea]
mov rdx, r11
sub rdx, 0x2410
add r11, rax
sub r11, 16
mov rcx, r10
mov rax, qword ptr [r11]
add rax, rdx
mov rdx, rax
mov r8, qword ptr [r11 + 8]
call 0x8c03
add r10, r8
mov byte ptr [r10], 0x20
add r10, 1
mov r11, qword ptr [rsp + 0x6FA8]
cmp r11, 14
jbe 0x853f
mov r11d, 14
mov rcx, r10
mov rdx, qword ptr [rsp + 0x6FA0]
mov r8, r11
call 0x8c03
add r10, r8
mov byte ptr [r10], 0x3A
add r10, 1
lea rax, [rsp + 0x7030]
sub r10, rax
mov qword ptr [rsp + 0x70D8], r10
cmp qword ptr [rsp + 0x7000], 0
jne 0x8597
cmp qword ptr [rsp + 0x6F98], 0
je 0x8597
mov qword ptr [rsp + 0x7028], 501
jmp 0x8b5b
cmp qword ptr [rsp + 0x6FF8], 0
je 0x85d8
mov eax, dword ptr [rsp + 0x6F00]
cmp eax, 3
mov qword ptr [rsp + 0x7028], 411
je 0x8b6b
cmp eax, 4
mov qword ptr [rsp + 0x7028], 411
je 0x8b6b
xor r15d, r15d
jmp 0x85f9
mov rcx, qword ptr [rsp + 0x6F70]
mov rdx, qword ptr [rsp + 0x6F78]
call 0x5080
test rax, rax
jne 0x8b3b
mov r15d, edx
cmp qword ptr [rsp + 0x7010], 4
je 0x8863
cmp qword ptr [rsp + 0x7010], 5
je 0x8863
cmp dword ptr [rsp + 0x6F00], 8
je 0x895b
mov rcx, qword ptr [rsp + 0x6FA0]
mov rdx, qword ptr [rsp + 0x6FA8]
mov r8d, dword ptr [rsp + 0x6FB0]
call 0x4400
test rax, rax
mov qword ptr [rsp + 0x7028], 502
je 0x8b8b
mov r12, rax
mov qword ptr [rsp + 0x7008], 0
mov rdx, qword ptr [rsp + 0x6F08]
mov r8, qword ptr [rsp + 0x6F10]
lea rcx, [rsp + 0x4000]
add rcx, qword ptr [rsp + 0x7008]
call 0x8c03
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
call 0x8c03
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
call 0x8c03
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
call 0x8c03
mov r10, qword ptr [rsp + 0x6FE0]
mov rax, r14
sub rax, r10
add qword ptr [rsp + 0x7008], rax
cmp qword ptr [rsp + 0x7010], 4
je 0x87b4
cmp qword ptr [rsp + 0x7010], 5
jne 0x887d
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
mov qword ptr [rsp + 0x7028], rax
test rax, rax
je 0x8a15
cmp eax, 3
je 0x8ba6
jmp 0x8b8b
test r15, r15
mov qword ptr [rsp + 0x7028], 501
jne 0x8b5b
jmp 0x865a
mov rcx, r12
lea rdx, [rsp + 0x4000]
mov r8, qword ptr [rsp + 0x7008]
call 0x8bc3
test rax, rax
jne 0x8a15
mov rax, r13
sub rax, r14
cmp rax, r15
jbe 0x88ac
mov rax, r15
mov r8, rax
lea rdx, [rsp + r14]
mov rcx, r12
call 0x8bc3
test rax, rax
jne 0x8a15
mov rax, r13
sub rax, r14
cmp rax, r15
jae 0x88d7
mov r14, r15
sub r14, rax
jmp 0x88da
xor r14d, r14d
test r14, r14
je 0x8935
mov r8, r14
cmp r8, 0x4000
jbe 0x88f2
mov r8, 0x4000
mov rcx, rbx
mov rdx, rsp
call 0x4140
test rax, rax
jle 0x8a15
add rsi, rax
mov qword ptr [rsp + 0x7018], rax
mov r8, rax
mov rdx, rsp
mov rcx, r12
call 0x8bc3
test rax, rax
jne 0x8a15
mov rax, qword ptr [rsp + 0x7018]
sub r14, rax
jne 0x88df
mov qword ptr [rsp + 0x7028], 0
mov rcx, r12
mov rdx, rbx
mov r8, rsp
mov r9, 0x4000
call 0x54c0
jmp 0x8a15
mov rcx, qword ptr [rsp + 0x6FA0]
mov rdx, qword ptr [rsp + 0x6FA8]
mov r8d, dword ptr [rsp + 0x6FB0]
call 0x4400
test rax, rax
mov qword ptr [rsp + 0x7028], 502
je 0x8b8b
mov r12, rax
mov qword ptr [rsp + 0x7028], 0
lea rdx, [rip - 0x6363]
mov r8, 30
mov rcx, rbx
call 0x8bc3
test rax, rax
jne 0x8a15
lea rcx, [rip - 0x612e]
mov edx, 8
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call 0x4b00
lea rcx, [rip + 0x250]
mov rdx, r12
shl rdx, 32
or rdx, rbx
call 0x4300
test rax, rax
je 0x8a15
mov rcx, rax
call qword ptr [rip - 0x6906]
mov rcx, rbx
mov rdx, r12
mov r8, rsp
mov r9, 0x4000
call 0x54c0
jmp 0x8a15
cmp qword ptr [rsp + 0x7028], -1
je 0x8af0
cmp qword ptr [rsp + 0x70D0], 0
je 0x8af0
lea r13, [rsp + 0x7070]
mov byte ptr [r13], 0x20
mov byte ptr [r13 + 1], 0x76
mov byte ptr [r13 + 2], 0x3D
add r13, 3
mov ecx, dword ptr [rsp + 0x7028]
mov rdx, r13
call 0x1280
mov rcx, r13
call 0x1200
add r13, rax
mov byte ptr [r13], 0x20
mov byte ptr [r13 + 1], 0x65
mov byte ptr [r13 + 2], 0x3D
add r13, 3
mov ecx, esi
mov rdx, r13
call 0x1280
mov rcx, r13
call 0x1200
add r13, rax
mov byte ptr [r13], 0x20
mov byte ptr [r13 + 1], 0x73
mov byte ptr [r13 + 2], 0x3D
add r13, 3
mov ecx, edi
mov rdx, r13
call 0x1280
mov rcx, r13
call 0x1200
add r13, rax
mov word ptr [r13], 0x0A0D
add r13, 2
lea rcx, [rsp + 0x7030]
mov rdx, qword ptr [rsp + 0x70D8]
mov r8d, dword ptr [rsp + 0x6FB0]
lea r9, [rsp + 0x7070]
sub r13, r9
mov qword ptr [rsp + 0x20], r13
call 0x4b00
test r12, r12
je 0x8afd
mov rcx, r12
call 0x41c0
mov rcx, rbx
call 0x41c0
lea rcx, [rip - 0x626c]
mov edx, 15
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call 0x4b00
add rsp, 0x13390
pop rdi
pop rsi
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
lea rdx, [rip - 0x65e2]
mov r8, 35
jmp 0x8bb6
lea rdx, [rip - 0x65ce]
mov r8, 33
jmp 0x8bb6
lea rdx, [rip - 0x65ba]
mov r8, 31
jmp 0x8bb6
lea rdx, [rip - 0x65aa]
mov r8, 33
jmp 0x8bb6
lea rdx, [rip - 0x6596]
mov r8, 38
jmp 0x8bb6
lea rdx, [rip - 0x657e]
mov r8, 40
mov rcx, rbx
call 0x8bc3
jmp 0x8a15
lea rdx, [rip - 0x5f0d]
mov r8, 34
jmp 0x8bb6
mov rcx, rbx
call 0x8bc3
jmp 0x8a15
push rbx
push r12
push r13
mov rbx, rcx
mov r12, rdx
mov r13, r8
test r13, r13
je 0x8bf4
mov rcx, rbx
mov rdx, r12
mov r8, r13
call 0x4180
test rax, rax
jle 0x8bf8
add rdi, rax
add r12, rax
sub r13, rax
jne 0x8bd6
xor eax, eax
jmp 0x8bfd
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
je 0x8c2b
movzx eax, byte ptr [r12]
mov byte ptr [rbx], al
add rbx, 1
add r12, 1
sub r13, 1
jne 0x8c16
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
