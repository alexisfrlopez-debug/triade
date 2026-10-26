; porte R10 (sommes + version, algorithme de tcp-12) puis 4 vecteurs libc
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x40
lea rax, [rip + ANCRE]
mov r14, rax
sub r14, 0x2620
lea r12, [rip + TAB_SUM]
.verif:
mov edx, dword ptr [r12]
test edx, edx
je .porte_ok
mov r13d, dword ptr [r12 + 4]
mov rbx, r14
add rbx, rdx
xor eax, eax
xor ecx, ecx
.somme:
add rax, qword ptr [rbx + rcx]
add rcx, 8
cmp rcx, r13
jb .somme
cmp rax, qword ptr [r12 + 8]
jne .porte_ko
add r12, 0x10
jmp .verif
.porte_ok:
mov rax, qword ptr [rip + VERSION]
cmp rax, 0x30000
jb .porte_ko
xor r15d, r15d
lea rcx, [rsp + 0x20]
lea rdx, [rip + FIX_MEMCPY]
mov r8d, 16
call MEMCPY
lea rcx, [rsp + 0x20]
lea rdx, [rip + FIX_MEMCPY]
mov r8d, 16
call MEMCMP
test eax, eax
jne .t_memcmp
inc r15d
.t_memcmp:
lea rcx, [rip + FIX_MEMCMP_A]
lea rdx, [rip + FIX_MEMCMP_B]
mov r8d, 3
call MEMCMP
test eax, eax
jne .t_memcmp_neg
inc r15d
.t_memcmp_neg:
lea rcx, [rip + FIX_MEMCMP_A]
lea rdx, [rip + FIX_MEMCMP_C]
mov r8d, 3
call MEMCMP
cmp eax, -1
jne .t_strlen
inc r15d
.t_strlen:
lea rcx, [rip + FIX_STRLEN]
call STRLEN
cmp rax, 13
jne .t_itoa
inc r15d
.t_itoa:
mov ecx, 25000
lea rdx, [rsp + 0x30]
call ITOA
lea rcx, [rsp + 0x30]
lea rdx, [rip + FIX_ITOA]
mov r8d, 5
call MEMCMP
test eax, eax
jne .fin
inc r15d
jmp .fin
.porte_ko:
mov eax, 0xFFFFFFFF
jmp .retour
.fin:
mov eax, r15d
.retour:
add rsp, 0x40
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
