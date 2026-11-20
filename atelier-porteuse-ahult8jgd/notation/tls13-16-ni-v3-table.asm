; tls13-16-ni-v3-table · LA TABLE D'ADRESSES PRÉCALCULÉE : les adresses des N blocs
; posées UNE fois par flot au prologue, la boucle lit [table + i*8] — PLUS AUCUN add
; par bloc : la chaîne add→mov→call du v2 DISSOUTE (la charge porte l'adresse, chaque
; lecture [rbx + r13*8] est INDÉPENDANTE — le moteur hors-ordre recouvre les blocs)
; ABI msx64 (rcx = clés, rdx = entrées, r8 = sorties, r9 = N blocs) — le contrat du
; flux v2 INTACT ; l'état du flot aux NON-VOLATILS rbx/rbp/r12-r15 (rbx = table des
; entrées, rbp = table des sorties — les volatils ne portent RIEN au-delà d'un appel)
; LA BORNE NOMMÉE : N ≤ 256 (les deux tables de pile 2 × 0x800 o) — N > 256 →
; rax = -2, RIEN chiffré (fail-closed) ; le sondage CPUID UNE fois par flot (hisssé
; du v2 — AVANT la pose : cpuid clobber rbx, les pointeurs reposés après) ; le repli
; appelle le scellé tls13-16 (copie 0xC400) AUX ADRESSES DE LA TABLE (même porteur)
; Copie de laboratoire à la marge VIERGE 0xD200 — le scellé (slot 0xDF00) INTACT
; appels : 0xCE00 (corps NI pur, labo v2) · 0xC400 (scellé tls13-16, repli)
push rbx
push rbp
push r12
push r13
push r14
push r15
sub rsp, 0x1028
test r9, r9
jz .fin
cmp r9, 256
ja .refus
mov r12, rcx
mov r13, rdx
mov r14, r8
mov r15, r9
lea r10, [rsp + 0x28]
lea r11, [rsp + 0x828]
xor eax, eax
xor esi, esi
.pose:
lea rdx, [r13 + rsi]
lea r8, [r14 + rsi]
mov [r10 + rax*8], rdx
mov [r11 + rax*8], r8
lea rsi, [rsi + 16]
inc rax
cmp rax, r15
jne .pose
mov eax, 1
xor ecx, ecx
cpuid
lea rbx, [rsp + 0x28]
lea rbp, [rsp + 0x828]
test ecx, 0x2000000
jz .repli_boucle
xor r13d, r13d
.boucle_ni:
mov rcx, r12
mov rdx, [rbx + r13*8]
mov r8, [rbp + r13*8]
call 0xce00
inc r13
cmp r13, r15
jne .boucle_ni
jmp .fin
.repli_boucle:
xor r13d, r13d
.boucle_repli:
mov rcx, r12
mov rdx, [rbx + r13*8]
mov r8, [rbp + r13*8]
call 0xc400
inc r13
cmp r13, r15
jne .boucle_repli
.fin:
xor eax, eax
add rsp, 0x1028
pop r15
pop r14
pop r13
pop r12
pop rbp
pop rbx
ret
.refus:
mov rax, -2
add rsp, 0x1028
pop r15
pop r14
pop r13
pop r12
pop rbp
pop rbx
ret
