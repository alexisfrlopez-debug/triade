; tls13-05-hmac-sha256 · bloc HMAC-SHA-256 (RFC 2104 : ipad/opad, la clé expulsée) · spec tls13-05:R1 · bloc carte h100005
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0xc3c0, taille 512 octets
; Domaine : tls13 (M9, l'ère 1.0.0) · Dépendances : tls13-01 (init ×2, DEUX contextes), tls13-03 (absorption), tls13-04 (finalisation) — appels directs aux adresses scellées (I1) ; K', le masque et les DEUX contextes sur la PILE (I2) — AUCUN déplacement RIP
; Notation explicite générée par outils/auteur.py depuis brouillons/tls13-05-hmac-sha256.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 435 o · padding : 77 o (NOP, 0x90)
; Étiquettes résolues : .cle_longue=0xc418, .masque_interieur=0xc45c, .xor_ipad=0xc482, .xor_opad=0xc4fd, .refus=0xc559, .fin=0xc560
; Appels directs (l'adresse scellée du plan — I1) : call 0xc000, call 0xc240, call 0xc300, call 0xc000, call 0xc240, call 0xc240, call 0xc300, call 0xc000, call 0xc240, call 0xc240, call 0xc300
push rbx
push r12
push r13
push r14
push r15
push rdi
push rsi
sub rsp, 0x1a0
mov rbx, qword ptr [rsp + 0x200]
test rbx, rbx
je 0xc559
mov r12, rcx
mov r13, rdx
mov r14, r8
mov r15, r9
cmp r13, 64
ja 0xc418
lea rdi, [rsp + 0x20]
mov rsi, r12
mov rcx, r13
rep movsb
lea rdi, [rsp + 0x20]
add rdi, r13
mov ecx, 64
sub ecx, r13d
xor eax, eax
rep stosb
jmp 0xc45c
lea rcx, [rsp + 0xa0]
call 0xc000
lea rcx, [rsp + 0xa0]
mov rdx, r12
mov r8, r13
call 0xc240
lea rcx, [rsp + 0xa0]
lea rdx, [rsp + 0x20]
call 0xc300
lea rdi, [rsp + 0x20]
add rdi, 32
mov ecx, 32
xor eax, eax
rep stosb
lea rcx, [rsp + 0xa0]
call 0xc000
movabs r10, 0x3636363636363636
lea rdi, [rsp + 0x60]
lea rsi, [rsp + 0x20]
mov ecx, 8
mov rax, qword ptr [rsi]
xor rax, r10
mov qword ptr [rdi], rax
add rsi, 8
add rdi, 8
dec ecx
jnz 0xc482
lea rcx, [rsp + 0xa0]
lea rdx, [rsp + 0x60]
mov r8d, 64
call 0xc240
lea rcx, [rsp + 0xa0]
mov rdx, r14
mov r8, r15
call 0xc240
lea rcx, [rsp + 0xa0]
lea rdx, [rsp + 0x180]
call 0xc300
lea rcx, [rsp + 0x110]
call 0xc000
movabs r10, 0x5c5c5c5c5c5c5c5c
lea rdi, [rsp + 0x60]
lea rsi, [rsp + 0x20]
mov ecx, 8
mov rax, qword ptr [rsi]
xor rax, r10
mov qword ptr [rdi], rax
add rsi, 8
add rdi, 8
dec ecx
jnz 0xc4fd
lea rcx, [rsp + 0x110]
lea rdx, [rsp + 0x60]
mov r8d, 64
call 0xc240
lea rcx, [rsp + 0x110]
lea rdx, [rsp + 0x180]
mov r8d, 32
call 0xc240
lea rcx, [rsp + 0x110]
mov rdx, rbx
call 0xc300
xor eax, eax
jmp 0xc560
mov rax, -1
add rsp, 0x1a0
pop rsi
pop rdi
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
