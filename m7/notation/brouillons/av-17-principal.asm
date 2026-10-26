; av-17-principal · brouillon étiqueté — spec av-17:R1, bloc carte d50017
; point d'entrée ELF (rsp ≡ 0 au démarrage, aucun push — miroir ah-09)
; modes : --hacher <fichier> (sha512sum) ; <m> <s> <cle> (chantier dev.1, exit 2)
; usage/ouverture/lecture/ecriture : stderr + exit 1 (préfixe sceau:)
; le magic « --hacher » : qword LE 0x7265686361682d2d PUIS octet 8 nul (I6)
@A_ABSORBER = 0x1680
@A_ECRITE = 0x1000
@A_FINALISER = 0x1780
@A_HEX = 0x1600
@A_INIT = 0x1100
@A_SORTIR = 0x1080
@MAGIC_HACHER = 0x7265686361682d2d
@R_CTX = 0x4000
@R_DIGEST = 0x4100
@R_LIGNE = 0x4200
@R_TAMPON = 0x5c00
@R_MSG_USAGE = 0x3400
@R_MSG_OUVERTURE = 0x3460
@R_MSG_LECTURE = 0x3480
@R_MSG_ECRITURE = 0x34a0
@R_MSG_CHANTIER = 0x3500
@L_USAGE = 0x44
@L_OUVERTURE = 0x1c
@L_LECTURE = 0x19
@L_ECRITURE = 0x19
@L_CHANTIER = 0x36
mov r14, qword ptr [rsp]
cmp r14, 3
jl .usage
jg .quatre
mov rbx, qword ptr [rsp + 0x10]
mov rax, @MAGIC_HACHER
cmp qword ptr [rbx], rax
jne .usage
cmp byte ptr [rbx + 8], 0
jne .usage
mov rbx, qword ptr [rsp + 0x18]
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
mov edx, 0x10000
syscall
test rax, rax
js .lecture_ko
je .fin_lecture
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
lea rdi, [rip + @R_DIGEST]
add rdi, 0x20
lea rsi, [rip + @R_LIGNE]
add rsi, 0x40
call @A_HEX
lea rax, [rip + @R_LIGNE]
mov byte ptr [rax + 0x80], 0x20
mov byte ptr [rax + 0x81], 0x20
lea rdi, [rip + @R_LIGNE]
add rdi, 0x82
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
mov byte ptr [rdi], 0xa
add rdi, 1
lea rax, [rip + @R_LIGNE]
sub rdi, rax
mov r13, rdi
mov edi, 1
lea rsi, [rip + @R_LIGNE]
mov rdx, r13
call @A_ECRITE
test eax, eax
js .ecriture_ko
xor edi, edi
call @A_SORTIR
.quatre:
cmp r14, 4
jne .usage
mov edi, 2
lea rsi, [rip + @R_MSG_CHANTIER]
mov edx, @L_CHANTIER
jmp .erreur_deux
.usage:
mov edi, 2
lea rsi, [rip + @R_MSG_USAGE]
mov edx, @L_USAGE
jmp .erreur_un
.ouverture:
mov edi, 2
lea rsi, [rip + @R_MSG_OUVERTURE]
mov edx, @L_OUVERTURE
jmp .erreur_un
.lecture_ko:
mov edi, 2
lea rsi, [rip + @R_MSG_LECTURE]
mov edx, @L_LECTURE
jmp .erreur_un
.ecriture_ko:
mov edi, 2
lea rsi, [rip + @R_MSG_ECRITURE]
mov edx, @L_ECRITURE
jmp .erreur_un
.erreur_deux:
mov edi, 2
call @A_ECRITE
mov edi, 2
call @A_SORTIR
.erreur_un:
mov edi, 2
call @A_ECRITE
mov edi, 1
call @A_SORTIR
