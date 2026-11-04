; tcp-11-journal-v2 · bloc journal v2 — le remplaçant (staging, POUR la croissance) · spec tcp-11:R2-v2 · bloc carte f61991
; Profil : x86-64-linux-elf64 · ABI SysV · slot RVA 0x1d80, taille 640 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/tcp-11-journal-v2.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 210 o · padding : 430 o (NOP)
; Étiquettes résolues : .acquis=0x1db1, .reattendre=0x1da1, .sans_champ=0x1e0e
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x1da1 + 0x7 + 0x1a58 = 0x3800 (@VERROU)
;   0x1db4 + 0x7 - 0x1b0b = 0x2b0 (@J2_MARK)
;   0x1e36 + 0xb + 0x19bf = 0x3800 (@VERROU)
; Symboles (vérifiés par build_m6.py contre layout.py) : @A_ECRIRE=0x1000, @A_ITOA=0x1180, @A_MEMCPY=0x1080, @A_STRLEN=0x1140, @J2_MARK=0x2b0, @SENTINELLE=0xffffffff, @VERROU=0x3800
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x60
mov rbx, rdi
mov r12, rsi
mov r13, rdx
mov r14, rcx
mov r15, r8
mov esi, 1
xchg qword ptr [rip + 0x1a58], rsi
test rsi, rsi
je 0x1db1
pause
jmp 0x1da1
mov rdi, rsp
lea rsi, [rip - 0x1b0b]
mov edx, 4
call 0x1080
lea rdi, [rsp + 4]
mov rsi, rbx
mov rdx, r12
call 0x1080
lea r12, [r12 + 4]
cmp r13d, -1
je 0x1e0e
mov edi, r13d
lea rsi, [rsp + 0x44]
call 0x1180
lea rdi, [rsp + 0x44]
call 0x1140
lea rdi, [rsp]
add rdi, r12
lea rsi, [rsp + 0x44]
mov rdx, rax
add r12, rax
call 0x1080
lea rdi, [rsp]
add rdi, r12
mov rsi, r14
mov rdx, r15
call 0x1080
add r12, r15
mov edi, 1
mov rsi, rsp
mov rdx, r12
call 0x1000
mov r14, rax
mov qword ptr [rip + 0x19bf], 0
mov rax, r14
add rsp, 0x60
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
