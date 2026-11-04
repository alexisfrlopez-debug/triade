; tcp-11-journal-r2 · bloc ligne de journal console (tcp-11:R2) · spec tcp-11:R2 · bloc carte f61011
; Profil : x86-64-linux-elf64 · ABI SysV · slot RVA 0x1840, taille 512 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/tcp-11-journal-r2.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 182 o · padding : 330 o (NOP)
; Étiquettes résolues : .acquis=0x1871, .reattendre=0x1861, .sans_champ=0x18b2
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x1861 + 0x7 + 0x1f98 = 0x3800 (@VERROU)
;   0x18da + 0xb + 0x1f1b = 0x3800 (@VERROU)
; Symboles (vérifiés par build_m6.py contre layout.py) : @A_ECRIRE=0x1000, @A_ITOA=0x1180, @A_MEMCPY=0x1080, @A_STRLEN=0x1140, @SENTINELLE=0xffffffff, @VERROU=0x3800
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x50
mov rbx, rdi
mov r12, rsi
mov r13, rdx
mov r14, rcx
mov r15, r8
mov esi, 1
xchg qword ptr [rip + 0x1f98], rsi
test rsi, rsi
je 0x1871
pause
jmp 0x1861
mov rdi, rsp
mov rsi, rbx
mov rdx, r12
call 0x1080
cmp r13d, -1
je 0x18b2
mov edi, r13d
lea rsi, [rsp + 0x40]
call 0x1180
lea rdi, [rsp + 0x40]
call 0x1140
mov rdi, rsp
add rdi, r12
lea rsi, [rsp + 0x40]
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
mov qword ptr [rip + 0x1f1b], 0
mov rax, r14
add rsp, 0x50
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
