; tls13-16-ni-v2-flux · LE SONDAGE HISSÉ : le verdict CPUID UNE fois par flot, la boucle par bloc au chemin pur
; ABI msx64 (rcx = clés, rdx = tableau d'entrées, r8 = tableau de sorties, r9 = N blocs) — l'état du flot aux NON-VOLATILS r12-r15
; (le scellé clobber ses volatils — le pointeur r9 DU FLOT jamais confié à l'appelé : la leçon du premier essai, l'écart nommé)
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x28
test r9, r9
jz .fin
mov r12, rcx
mov r13, rdx
mov r14, r8
mov r15, r9
mov r10, rcx
mov r11, rdx
mov eax, 1
xor ecx, ecx
cpuid
test ecx, 0x2000000
jz .repli_boucle
.boucle_ni:
mov rcx, r12
mov rdx, r13
mov r8, r14
call 0xce00
add r13, 16
add r14, 16
dec r15
jnz .boucle_ni
jmp .fin
.repli_boucle:
mov rcx, r12
mov rdx, r13
mov r8, r14
call 0xc400
add r13, 16
add r14, 16
dec r15
jnz .repli_boucle
.fin:
xor eax, eax
add rsp, 0x28
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
