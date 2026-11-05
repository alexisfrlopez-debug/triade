; tls13-07-hkdf-expand · bloc HKDF-Expand (RFC 5869 § 2.3 : PRK + info → OKM) · spec tls13-07:R1 · bloc carte h100007
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0xc680, taille 384 octets
; Domaine : tls13 (M9, l'ère 1.0.0) · Dépendances : tls13-05 (l'HMAC appelé à CHAQUE itération — I1) ; le tampon T(i−1) || info || i en allocation dynamique 16-alignée sur la PILE ; T(i−1) LU DEPUIS OKM (I2)
; Notation explicite générée par outils/auteur.py depuis brouillons/tls13-07-hkdf-expand.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 347 o · padding : 37 o (NOP, 0x90)
; Étiquettes résolues : .boucle=0xc6e4, .sans_t=0xc71e, .copie_info=0xc728, .compteur=0xc73a, .k_entier=0xc777, .recopier=0xc785, .recopie_fin=0xc797, .fini=0xc7a7, .refus_nul=0xc7bf, .refus_taille=0xc7c8, .refus_epilogue=0xc7cf
; Appels directs (l'adresse scellée du plan — I1) : call 0xc3c0
push rbx
push r12
push r13
push r14
push r15
push rdi
push rsi
mov rbx, qword ptr [rsp + 0x60]
test rbx, rbx
je 0xc7bf
mov r12, rcx
mov r13, r9
mov r14, r8
mov r15, rdx
test r13, r13
jz 0xc7c8
cmp r13, 8160
ja 0xc7c8
lea rax, [r14 + 0x21]
movabs r10, 0x2000000000000000
cmp rax, r10
ja 0xc7c8
mov rdi, 1
xor esi, esi
lea rax, [r14 + 0x78]
and al, 0xf0
sub rsp, rax
xor r10d, r10d
cmp rdi, 1
je 0xc71e
lea r11, [rbx + rsi]
sub r11, 32
lea r10, [rsp + 0x28]
mov rax, qword ptr [r11]
mov qword ptr [r10], rax
mov rax, qword ptr [r11 + 8]
mov qword ptr [r10 + 8], rax
mov rax, qword ptr [r11 + 16]
mov qword ptr [r10 + 16], rax
mov rax, qword ptr [r11 + 24]
mov qword ptr [r10 + 24], rax
mov r10d, 32
lea r11, [rsp + 0x28]
add r11, r10
xor ecx, ecx
cmp rcx, r14
jae 0xc73a
mov al, byte ptr [r15 + rcx]
mov byte ptr [r11 + rcx], al
inc rcx
jmp 0xc728
add r11, r14
mov byte ptr [r11], dil
lea rax, [rsp + 0x49]
add rax, r14
mov qword ptr [rsp + 0x20], rax
mov rcx, r12
mov edx, 32
lea r8, [rsp + 0x28]
lea r9, [r14 + 1]
add r9, r10
call 0xc3c0
mov rcx, r13
sub rcx, rsi
cmp rcx, 32
jbe 0xc777
mov ecx, 32
lea r11, [rsp + 0x49]
add r11, r14
lea r10, [rbx + rsi]
xor eax, eax
cmp rax, rcx
jae 0xc797
mov dl, byte ptr [r11 + rax]
mov byte ptr [r10 + rax], dl
inc rax
jmp 0xc785
add rsi, rcx
inc rdi
cmp rsi, r13
jae 0xc7a7
jmp 0xc6e4
xor eax, eax
lea rcx, [r14 + 0x78]
and cl, 0xf0
add rsp, rcx
pop rsi
pop rdi
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
mov rax, -1
jmp 0xc7cf
mov rax, -2
pop rsi
pop rdi
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
