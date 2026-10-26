; ah-05-comprimer · bloc compression d'un bloc de 64 octets · spec ah-05:R1 · bloc carte d40005
; Profil : x86-64-linux-elf64 · ABI SysV · slot RVA 0x1200, taille 512 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/ah-05-comprimer.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 379 o · padding : 133 o (NOP)
; Étiquettes résolues : .charger=0x1223, .etendre=0x1237, .tour=0x12aa
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x1215 + 0x7 + 0xde4 = 0x2000 (@k)
; Symboles (vérifiés par build_ah.py contre layout.py) : @k=0x2000
push rbp
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x120
mov qword ptr [rsp], rdi
lea rbp, [rip + 0xde4]
lea rsi, [rdi + 0x20]
xor r15d, r15d
mov eax, dword ptr [rsi + r15*4]
bswap eax
mov dword ptr [rsp + r15*4 + 0x20], eax
inc r15
cmp r15, 0x10
jl 0x1223
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
jl 0x1237
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
jl 0x12aa
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
pop r15
pop r14
pop r13
pop r12
pop rbx
pop rbp
ret
