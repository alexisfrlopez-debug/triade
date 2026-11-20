; tls13-16-ni-v3-deroule · LE DÉROULAGE k=4 SUR LA TABLE : la table d'adresses du
; v3-table (posée une fois par flot) ET la chaîne payée UNE FOIS PAR QUATRE — les
; quatre lectures d'adresses [rbx + r13*8 + {0,8,16,24}] sont ÉMISES D'UN SEUL
; regard, indépendantes entre elles ; le compteur et le saut amortis sur 4 blocs
; ABI msx64 (rcx = clés, rdx = entrées, r8 = sorties, r9 = N blocs) — le contrat
; du flux v2 INTACT ; l'état aux NON-VOLATILS rbx/rbp/r12-r15 ; LA BORNE NOMMÉE :
; N ≤ 256 → rax = -2, RIEN chiffré (fail-closed) ; le reste N mod 4 à la boucle
; k=1 de tête (le cas général tenu) ; le repli au scellé tls13-16 (copie 0xC400)
; aux adresses de la table ; le sondage CPUID UNE fois par flot
; Copie de laboratoire à la marge VIERGE 0xD400 — le scellé (slot 0xDF00) INTACT
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
mov r14, r15
shr r14, 2
xor r13d, r13d
test r14, r14
jz .reste_prep
.boucle_ni:
mov rcx, r12
mov rdx, [rbx + r13*8]
mov r8, [rbp + r13*8]
call 0xce00
mov rcx, r12
mov rdx, [rbx + r13*8 + 8]
mov r8, [rbp + r13*8 + 8]
call 0xce00
mov rcx, r12
mov rdx, [rbx + r13*8 + 16]
mov r8, [rbp + r13*8 + 16]
call 0xce00
mov rcx, r12
mov rdx, [rbx + r13*8 + 24]
mov r8, [rbp + r13*8 + 24]
call 0xce00
lea r13, [r13 + 4]
dec r14
jnz .boucle_ni
.reste_prep:
mov r14, r15
and r14, 3
jz .fin
mov r13, r15
sub r13, r14
.boucle_reste:
mov rcx, r12
mov rdx, [rbx + r13*8]
mov r8, [rbp + r13*8]
call 0xce00
inc r13
dec r14
jnz .boucle_reste
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
