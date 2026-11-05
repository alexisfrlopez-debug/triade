; tls13-08-hkdf-expand-label · bloc HKDF-Expand-Label (RFC 8446 § 7.1 : le calendrier) · spec tls13-08:R1 · bloc carte h100008
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0xc800, taille 384 octets
; Domaine : tls13 (M9, l'ère 1.0.0) · Dépendances : tls13-07 (l'expansion appelée UNE fois — I1) ; la structure HkdfLabel sérialisée GROS-BOUTISTE dans le tampon de PILE ; le préfixe « tls13 » en immédiats du plan (I2)
; Notation explicite générée par outils/auteur.py depuis brouillons/tls13-08-hkdf-expand-label.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 310 o · padding : 74 o (NOP, 0x90)
; Étiquettes résolues : .ctx_vide=0xc882, .copie_libelle=0xc8c3, .libelle_fini=0xc8d6, .copie_ctx=0xc8e1, .ctx_fini=0xc8f3, .refus_nul=0xc913, .refus_bornes=0xc91c, .fin=0xc923
; Appels directs (l'adresse scellée du plan — I1) : call 0xc680
push rbx
push r12
push r13
push r14
push r15
push rdi
push rsi
sub rsp, 0x2a0
mov rbx, qword ptr [rsp + 0x310]
mov rdi, qword ptr [rsp + 0x300]
mov rsi, qword ptr [rsp + 0x308]
mov r12, rcx
mov r13, rdx
mov r14, r8
mov r15, r9
test rbx, rbx
je 0xc913
test r12, r12
je 0xc913
test r13, r13
je 0xc913
test r14, r14
jz 0xc91c
cmp r14, 249
ja 0xc91c
cmp rdi, 255
ja 0xc91c
test rdi, rdi
jz 0xc882
test r15, r15
jz 0xc913
test rsi, rsi
jz 0xc91c
cmp rsi, 8160
ja 0xc91c
lea r10, [rsp + 0x28]
mov rax, rsi
xchg al, ah
mov word ptr [r10], ax
lea r11, [r14 + 6]
mov byte ptr [r10 + 2], r11b
mov dword ptr [r10 + 3], 0x31736c74
mov word ptr [r10 + 7], 0x2033
lea r11, [r10 + 9]
xor ecx, ecx
cmp rcx, r14
jae 0xc8d6
mov al, byte ptr [r13 + rcx]
mov byte ptr [r11 + rcx], al
inc rcx
jmp 0xc8c3
add r11, r14
mov byte ptr [r11], dil
inc r11
xor ecx, ecx
cmp rcx, rdi
jae 0xc8f3
mov al, byte ptr [r15 + rcx]
mov byte ptr [r11 + rcx], al
inc rcx
jmp 0xc8e1
lea rax, [r14 + rdi]
add rax, 10
mov qword ptr [rsp + 0x20], rbx
mov rcx, r12
mov rdx, r10
mov r8, rax
mov r9, rsi
call 0xc680
jmp 0xc923
mov rax, -1
jmp 0xc923
mov rax, -2
add rsp, 0x2a0
pop rsi
pop rdi
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
