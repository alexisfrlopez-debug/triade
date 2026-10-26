; av-02-s512-comprimer · bloc compression d'un bloc de 128 octets · spec av-02:R2 · bloc carte d50002
; Profil : x86-64-linux-elf64 · ABI SysV · slot RVA 0x1200, taille 1024 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/av-02-s512-comprimer.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 392 o · padding : 632 o (NOP)
; Étiquettes résolues : .charger=0x1223, .etendre=0x1238, .tour=0x12b2
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x1215 + 0x7 + 0x1de4 = 0x3000 (@R_K512)
; Symboles (vérifiés par build_sceau.py contre layout.py) : @R_K512=0x3000
push rbp
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x2a8
mov qword ptr [rsp], rdi
lea rbp, [rip + 0x1de4]
lea rsi, [rdi + 0x40]
xor r15d, r15d
mov rax, qword ptr [rsi + r15*8]
bswap rax
mov qword ptr [rsp + r15*8 + 0x20], rax
inc r15
cmp r15, 0x10
jl 0x1223
mov rax, qword ptr [rsp + r15*8 + 0x10]
mov rdx, rax
ror rdx, 0x13
mov rcx, rax
ror rcx, 0x3d
xor rdx, rcx
shr rax, 6
xor rdx, rax
mov r12, qword ptr [rsp + r15*8 - 0x58]
mov r13, r12
ror r13, 1
mov rax, r12
ror rax, 8
xor r13, rax
shr r12, 7
xor r13, r12
add rdx, qword ptr [rsp + r15*8 - 0x18]
add rdx, r13
add rdx, qword ptr [rsp + r15*8 - 0x60]
mov qword ptr [rsp + r15*8 + 0x20], rdx
inc r15
cmp r15, 0x50
jl 0x1238
mov r14, qword ptr [rsp]
mov rax, qword ptr [r14]
mov rbx, qword ptr [r14 + 8]
mov rcx, qword ptr [r14 + 0x10]
mov rdx, qword ptr [r14 + 0x18]
mov rsi, qword ptr [r14 + 0x20]
mov rdi, qword ptr [r14 + 0x28]
mov r8, qword ptr [r14 + 0x30]
mov r9, qword ptr [r14 + 0x38]
xor r15d, r15d
mov r10, rsi
ror r10, 0xe
mov r11, rsi
ror r11, 0x12
xor r10, r11
mov r11, rsi
ror r11, 0x29
xor r10, r11
add r10, r9
mov r11, rsi
and r11, rdi
mov r12, rsi
not r12
and r12, r8
xor r11, r12
add r10, r11
add r10, qword ptr [rbp + r15*8]
mov r12, qword ptr [rsp + r15*8 + 0x20]
add r10, r12
mov r11, rax
ror r11, 0x1c
mov r12, rax
ror r12, 0x22
xor r11, r12
mov r12, rax
ror r12, 0x27
xor r11, r12
mov r12, rax
and r12, rbx
mov r13, rax
and r13, rcx
xor r12, r13
mov r13, rbx
and r13, rcx
xor r12, r13
add r11, r12
mov r9, r8
mov r8, rdi
mov rdi, rsi
mov rsi, rdx
add rsi, r10
mov rdx, rcx
mov rcx, rbx
mov rbx, rax
mov rax, r10
add rax, r11
inc r15
cmp r15, 0x50
jl 0x12b2
mov r14, qword ptr [rsp]
add qword ptr [r14], rax
add qword ptr [r14 + 8], rbx
add qword ptr [r14 + 0x10], rcx
add qword ptr [r14 + 0x18], rdx
add qword ptr [r14 + 0x20], rsi
add qword ptr [r14 + 0x28], rdi
add qword ptr [r14 + 0x30], r8
add qword ptr [r14 + 0x38], r9
add rsp, 0x2a8
pop r15
pop r14
pop r13
pop r12
pop rbx
pop rbp
ret
