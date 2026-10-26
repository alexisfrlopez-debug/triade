; ah-05-comprimer · brouillon étiqueté — spec ah-05:R1, bloc carte d40005
; compression SHA-256 FIPS § 6.2.2 : annexe W[64] sur pile, 64 tours, addition H
; registres : a=eax b=ebx c=ecx d=edx e=esi f=edi g=r8d h=r9d
;             T1=r10d T2 implicite r11d/r12d/r13d, K base=rbp, i=r15, ctx=r14
; appelé uniquement avec remplissage == 64 (contrat de coopération)
@k = 0x2000
push rbp
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x120
mov qword ptr [rsp], rdi
lea rbp, [rip + @k]
lea rsi, [rdi + 32]
xor r15d, r15d
.charger:
mov eax, dword ptr [rsi + r15*4]
bswap eax
mov dword ptr [rsp + r15*4 + 0x20], eax
inc r15
cmp r15, 16
jl .charger
.etendre:
mov eax, dword ptr [rsp + r15*4 + 0x18]
mov edx, eax
ror edx, 17
mov ecx, eax
ror ecx, 19
xor edx, ecx
shr eax, 10
xor edx, eax
mov r12d, dword ptr [rsp + r15*4 - 0x1c]
mov r13d, r12d
ror r13d, 7
mov eax, r12d
ror eax, 18
xor r13d, eax
shr r12d, 3
xor r13d, r12d
add edx, dword ptr [rsp + r15*4 + 0x4]
add edx, r13d
add edx, dword ptr [rsp + r15*4 - 0x20]
mov dword ptr [rsp + r15*4 + 0x20], edx
inc r15
cmp r15, 64
jl .etendre
mov r14, qword ptr [rsp]
mov eax, dword ptr [r14]
mov ebx, dword ptr [r14 + 4]
mov ecx, dword ptr [r14 + 8]
mov edx, dword ptr [r14 + 12]
mov esi, dword ptr [r14 + 16]
mov edi, dword ptr [r14 + 20]
mov r8d, dword ptr [r14 + 24]
mov r9d, dword ptr [r14 + 28]
xor r15d, r15d
.tour:
mov r10d, esi
ror r10d, 6
mov r11d, esi
ror r11d, 11
xor r10d, r11d
mov r11d, esi
ror r11d, 25
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
ror r12d, 13
xor r11d, r12d
mov r12d, eax
ror r12d, 22
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
cmp r15, 64
jl .tour
mov r14, qword ptr [rsp]
add dword ptr [r14], eax
add dword ptr [r14 + 4], ebx
add dword ptr [r14 + 8], ecx
add dword ptr [r14 + 12], edx
add dword ptr [r14 + 16], esi
add dword ptr [r14 + 20], edi
add dword ptr [r14 + 24], r8d
add dword ptr [r14 + 28], r9d
add rsp, 0x120
pop r15
pop r14
pop r13
pop r12
pop rbx
pop rbp
ret
