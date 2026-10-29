; http-09-pompe · brouillon · pompe unidirectionnelle · http-09:R1 · e50009
; relais source -> destination jusqu'à la fin : N'EST JAMAIS fermée ici (Q4 —
; tcp-05 hors appels autorisés, I1 : tcp-03/tcp-04 uniquement) ; émissions
; partielles rejouées jusqu'à n total (Q1) ; total rendu sur tout verdict (Q3) ;
; un send <= 0 est tranché erreur destination (I5 : aucune boucle sans
; progression garantie).
; entrée : rcx = socket source, rdx = socket destination, r8 = tampon, r9 = capacité
; sortie : rax = 0 fin normale / 1 erreur source / 2 erreur destination
;          rdx = total pompé (u64, tout verdict)
push rbx
push rbp
push r12
push r13
push r14
push r15
sub rsp, 0x28
mov rbx, rcx
mov r12, rdx
mov r14, r9
mov qword ptr [rsp + 0x20], r8
xor r15d, r15d
.boucle:
mov rcx, rbx
mov rdx, qword ptr [rsp + 0x20]
mov r8, r14
call TCP_RECV
test rax, rax
js .v1
je .v0
mov rbp, rax
mov r13, qword ptr [rsp + 0x20]
.envoi:
mov rcx, r12
mov rdx, r13
mov r8, rbp
call TCP_SEND
test rax, rax
jle .v2
add r15, rax
add r13, rax
sub rbp, rax
jne .envoi
jmp .boucle
.v0:
xor eax, eax
jmp .fin
.v1:
mov eax, 1
jmp .fin
.v2:
mov eax, 2
.fin:
mov rdx, r15
add rsp, 0x28
pop r15
pop r14
pop r13
pop r12
pop rbp
pop rbx
ret
