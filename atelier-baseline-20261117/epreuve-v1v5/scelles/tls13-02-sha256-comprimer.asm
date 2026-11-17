; tls13-02-sha256-comprimer · bloc compression d'un bloc de 64 o (FIPS § 6.2.2) · spec tls13-02:R1 · bloc carte h100002
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0xc080, taille 448 octets
; Domaine : tls13 (M9, l'ère 1.0.0) · Dépendances : bloc feuille ; le fixture K[64] @R_K cité par déplacement RIP (I3 de la spec) — AUCUN autre accès mémoire hors du contexte et de la pile
; Notation explicite générée par outils/auteur.py depuis brouillons/tls13-02-sha256-comprimer.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 387 o · padding : 61 o (NOP, 0x90)
; Étiquettes résolues : .charger=0xc0a7, .etendre=0xc0bb, .tour=0xc12e
; Déplacements RIP (cible = adresse + taille + disp) :
;   0xc09d + 0x7 - 0x91a4 = 0x2f00
push rbp
push rbx
push r12
push r13
push r14
push r15
push rdi
push rsi
sub rsp, 0x120
mov rdi, rcx
mov rsi, rdx
mov qword ptr [rsp], rdi
lea rbp, [rip - 0x91a4]
xor r15d, r15d
mov eax, dword ptr [rsi + r15*4]
bswap eax
mov dword ptr [rsp + r15*4 + 0x20], eax
inc r15
cmp r15, 0x10
jl 0xc0a7
mov eax, dword ptr [rsp + r15*4 + 0x18]
mov edx, eax
ror edx, 0x11
mov ecx, eax
ror ecx, 0x13
xor edx, ecx
shr eax, 0xa
xor edx, eax
mov r12d, dword ptr [rsp + r15*4 - 0x1c]
mov r13d, r12d
ror r13d, 7
mov eax, r12d
ror eax, 0x12
xor r13d, eax
shr r12d, 3
xor r13d, r12d
add edx, dword ptr [rsp + r15*4 + 4]
add edx, r13d
add edx, dword ptr [rsp + r15*4 - 0x20]
mov dword ptr [rsp + r15*4 + 0x20], edx
inc r15
cmp r15, 0x40
jl 0xc0bb
mov r14, qword ptr [rsp]
mov eax, dword ptr [r14]
mov ebx, dword ptr [r14 + 4]
mov ecx, dword ptr [r14 + 8]
mov edx, dword ptr [r14 + 0xc]
mov esi, dword ptr [r14 + 0x10]
mov edi, dword ptr [r14 + 0x14]
mov r8d, dword ptr [r14 + 0x18]
mov r9d, dword ptr [r14 + 0x1c]
xor r15d, r15d
mov r10d, esi
ror r10d, 6
mov r11d, esi
ror r11d, 0xb
xor r10d, r11d
mov r11d, esi
ror r11d, 0x19
xor r10d, r11d
add r10d, r9d
mov r11d, esi
and r11d, edi
mov r12d, esi
not r12d
and r12d, r8d
xor r11d, r12d
add r10d, r11d
add r10d, dword ptr [rbp + r15*4]
mov r12d, dword ptr [rsp + r15*4 + 0x20]
add r10d, r12d
mov r11d, eax
ror r11d, 2
mov r12d, eax
ror r12d, 0xd
xor r11d, r12d
mov r12d, eax
ror r12d, 0x16
xor r11d, r12d
mov r12d, eax
and r12d, ebx
mov r13d, eax
and r13d, ecx
xor r12d, r13d
mov r13d, ebx
and r13d, ecx
xor r12d, r13d
add r11d, r12d
mov r9d, r8d
mov r8d, edi
mov edi, esi
mov esi, edx
add esi, r10d
mov edx, ecx
mov ecx, ebx
mov ebx, eax
mov eax, r10d
add eax, r11d
inc r15
cmp r15, 0x40
jl 0xc12e
mov r14, qword ptr [rsp]
add dword ptr [r14], eax
add dword ptr [r14 + 4], ebx
add dword ptr [r14 + 8], ecx
add dword ptr [r14 + 0xc], edx
add dword ptr [r14 + 0x10], esi
add dword ptr [r14 + 0x14], edi
add dword ptr [r14 + 0x18], r8d
add dword ptr [r14 + 0x1c], r9d
add rsp, 0x120
pop rsi
pop rdi
pop r15
pop r14
pop r13
pop r12
pop rbx
pop rbp
xor eax, eax
ret
