; av-03-s512-absorber · brouillon étiqueté — spec av-03:R1, bloc carte d50003
; miroir 128 octets de ah-06:R1 (jb STRICT — le correctif frontière du journal 20)
; contexte : H @ +0, tampon[128] @ +0x40, remplissage @ +0xc0, total @ +0xc8
; 5 pushes : 8 + 40 ≡ 0 mod 16 aux appels de compression
@A_COMPRIMER = 0x1200
push rbx
push r12
push r13
push r14
push r15
mov rbx, rdi
mov r12, rsi
mov r13, rdx
.boucle:
test r13, r13
je .fin
mov r14d, dword ptr [rbx + 0xc0]
mov r15d, 0x80
sub r15d, r14d
cmp r13, r15
jb .court
lea rdi, [rbx + r14 + 0x40]
mov rsi, r12
mov rcx, r15
rep movsb byte ptr [rdi], byte ptr [rsi]
add dword ptr [rbx + 0xc0], r15d
add qword ptr [rbx + 0xc8], r15
sub r13, r15
add r12, r15
mov rdi, rbx
call @A_COMPRIMER
mov dword ptr [rbx + 0xc0], 0
jmp .boucle
.court:
lea rdi, [rbx + r14 + 0x40]
mov rsi, r12
mov rcx, r13
rep movsb byte ptr [rdi], byte ptr [rsi]
add dword ptr [rbx + 0xc0], r13d
add qword ptr [rbx + 0xc8], r13
xor r13d, r13d
jmp .boucle
.fin:
mov rax, qword ptr [rbx + 0xc8]
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
