; ah-09-principal · brouillon étiqueté — spec ah-09:R1, bloc carte d40009
; _start : [rsp]=argc, [rsp+8]=argv[0], [rsp+16]=argv[1], rsp ≡ 0 mod 16
; registres traversants : rbx=chemin, r12=fd, r13=longueur — non-volatils SysV,
; AUCUN push : les appels sont 16-alignés nativement (I4, appariement trivial),
; le bloc ne retourne jamais (terminaison par sys_exit via ah-03)
; syscalls directs open/read/close (I1), write/exit par les blocs (I2)
@A_ECRITE = 0x1000
@A_SORTIR = 0x1080
@A_INIT = 0x1100
@A_ABSORBER = 0x1400
@A_FINALISER = 0x1500
@A_HEX = 0x1600
@R_CTX = 0x3000
@R_DIGEST = 0x3080
@R_LIGNE = 0x30C0
@R_TAMPON = 0x4300
@R_MSG_USAGE = 0x2120
@L_USAGE = 25
@R_MSG_OUVERTURE = 0x2140
@L_OUVERTURE = 30
@R_MSG_LECTURE = 0x2160
@L_LECTURE = 27
@R_MSG_ECRITURE = 0x2180
@L_ECRITURE = 27
mov rax, qword ptr [rsp]
cmp rax, 2
jne .usage
mov rbx, qword ptr [rsp + 16]
mov eax, 2
mov rdi, rbx
xor esi, esi
xor edx, edx
syscall
test rax, rax
js .ouverture
mov r12, rax
lea rdi, [rip + @R_CTX]
call @A_INIT
.lecture:
xor eax, eax
mov rdi, r12
lea rsi, [rip + @R_TAMPON]
mov edx, 65536
syscall
test rax, rax
js .lecture_ko
jz .fin_lecture
mov r13, rax
lea rdi, [rip + @R_CTX]
lea rsi, [rip + @R_TAMPON]
mov rdx, r13
call @A_ABSORBER
jmp .lecture
.fin_lecture:
mov eax, 3
mov rdi, r12
syscall
lea rdi, [rip + @R_CTX]
lea rsi, [rip + @R_DIGEST]
call @A_FINALISER
lea rdi, [rip + @R_DIGEST]
lea rsi, [rip + @R_LIGNE]
call @A_HEX
lea rax, [rip + @R_LIGNE]
mov byte ptr [rax + 64], 0x20
mov byte ptr [rax + 65], 0x20
lea rdi, [rip + @R_LIGNE]
add rdi, 66
mov rsi, rbx
.copie:
movzx eax, byte ptr [rsi]
test al, al
je .copie_fin
mov byte ptr [rdi], al
add rdi, 1
add rsi, 1
jmp .copie
.copie_fin:
mov byte ptr [rdi], 0x0A
add rdi, 1
lea rax, [rip + @R_LIGNE]
sub rdi, rax
mov r13, rdi
mov edi, 1
lea rsi, [rip + @R_LIGNE]
mov rdx, r13
call @A_ECRITE
test eax, eax
js .ecriture
xor edi, edi
call @A_SORTIR
.erreur:
mov edi, 2
call @A_ECRITE
mov edi, 1
call @A_SORTIR
.usage:
lea rsi, [rip + @R_MSG_USAGE]
mov edx, @L_USAGE
jmp .erreur
.ouverture:
lea rsi, [rip + @R_MSG_OUVERTURE]
mov edx, @L_OUVERTURE
jmp .erreur
.lecture_ko:
lea rsi, [rip + @R_MSG_LECTURE]
mov edx, @L_LECTURE
jmp .erreur
.ecriture:
lea rsi, [rip + @R_MSG_ECRITURE]
mov edx, @L_ECRITURE
jmp .erreur
