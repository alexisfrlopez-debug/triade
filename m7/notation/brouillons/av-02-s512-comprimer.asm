; av-02-s512-comprimer · brouillon étiqueté — spec av-02:R2, bloc carte d50002
; 80 rondes FIPS 180-4 § 4.1.3 en mots 64 bits — miroir u64 de ah-05:R1 :
;   Σ0 = ror 28 ^ ror 34 ^ ror 39 ; Σ1 = ror 14 ^ ror 18 ^ ror 41 (DROITES)
;   σ0 = ror 1 ^ ror 8 ^ shr 7   ; σ1 = ror 19 ^ ror 61 ^ shr 6
; W[80] u64 sur pile (@ rsp+0x20), ctx @ [rsp], K[80] @ rbp (lea RIP)
; 6 pushes + sub 0x2a8 : le sous-cadre couvre W (0x20+0x280) ; aucun appel
@R_K512 = 0x3000
push rbp
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x2a8
mov qword ptr [rsp], rdi
lea rbp, [rip + @R_K512]
lea rsi, [rdi + 0x40]
xor r15d, r15d
.charger:
mov rax, qword ptr [rsi + r15*8]
bswap rax
mov qword ptr [rsp + r15*8 + 0x20], rax
inc r15
cmp r15, 0x10
jl .charger
.etendre:
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
; W[i-7] @ [rsp + i*8 + 0x20 - 56] = [rsp + r15*8 - 0x18] (le défaut initial
; -0x38 lisait W[i-11] : offset = 0x20 - 7*8, l'addition du +0x20 avait été
; oubliée — défaut n°1 de m7, attrapé par l'oracle différentiel, journal 21)
add rdx, qword ptr [rsp + r15*8 - 0x18]
add rdx, r13
add rdx, qword ptr [rsp + r15*8 - 0x60]
mov qword ptr [rsp + r15*8 + 0x20], rdx
inc r15
cmp r15, 0x50
jl .etendre
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
.tour:
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
jl .tour
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
