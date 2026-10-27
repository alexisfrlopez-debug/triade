; balayeur d'extrait : dans un tampon d'octets NON FIABLES, trouver la
; premiere occurrence d'une etiquette littérale (memcmp glissant scelle),
; puis copier les octets qui la suivent jusqu'a l'octet d'arret (memcpy
; scelle) — pur, réentravant, aucun état .data ; tronque a capacite-1
; avec rax=0 (un jeton OAuth raccourci ne doit jamais circuler)
; pre : rcx = tampon, rdx = longueur utile, r8 = etiquette, r9 = len etiquette,
;       [rsp+0x28] = octet d'arret, [rsp+0x30] = destination, [rsp+0x38] = capacite
push rbx
push rbp
push r12
push r13
push r14
push r15
push r11
sub rsp, 0x10
mov rbx, rcx
mov r12, rdx
mov r13, r8
mov r14, r9
mov r15, qword ptr [rsp + 0x70]
mov rbp, qword ptr [rsp + 0x78]
cmp r12, r14
jb .absent
.boucle:
mov rcx, rbx
mov rdx, r13
mov r8, r14
call MEMCMP
test eax, eax
je .trouve
inc rbx
dec r12
cmp r12, r14
jae .boucle
.absent:
xor eax, eax
jmp .fin
.trouve:
add rbx, r14
sub r12, r14
xor r8d, r8d
.scan:
cmp r8, r12
jae .copie_prete
mov al, byte ptr [rbx + r8]
cmp al, r15b
je .copie_prete
inc r8
jmp .scan
.copie_prete:
mov rax, qword ptr [rsp + 0x80]
cmp r8, rax
jb .plein
dec rax
mov r8, rax
xor r12d, r12d
jmp .copie
.plein:
mov r12, r8
.copie:
mov qword ptr [rsp], r8
mov rcx, rbp
mov rdx, rbx
call MEMCPY
mov rax, qword ptr [rsp]
mov byte ptr [rbp + rax], 0
mov rax, r12
.fin:
add rsp, 0x10
pop r11
pop r15
pop r14
pop r13
pop r12
pop rbp
pop rbx
ret
