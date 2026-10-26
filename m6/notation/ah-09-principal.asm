; ah-09-principal · bloc orchestration hachoir · spec ah-09:R1 · bloc carte d40009
; Profil : x86-64-linux-elf64 · ABI SysV · slot RVA 0x1680, taille 512 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/ah-09-principal.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 337 o · padding : 175 o (NOP)
; Étiquettes résolues : .copie=0x173f, .copie_fin=0x1752, .ecriture=0x17c3, .erreur=0x1785, .fin_lecture=0x16f2, .lecture=0x16b9, .lecture_ko=0x17b5, .ouverture=0x17a7, .usage=0x1799
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x16ad + 0x7 + 0x194c = 0x3000 (@R_CTX)
;   0x16be + 0x7 + 0x2c3b = 0x4300 (@R_TAMPON)
;   0x16da + 0x7 + 0x191f = 0x3000 (@R_CTX)
;   0x16e1 + 0x7 + 0x2c18 = 0x4300 (@R_TAMPON)
;   0x16fc + 0x7 + 0x18fd = 0x3000 (@R_CTX)
;   0x1703 + 0x7 + 0x1976 = 0x3080 (@R_DIGEST)
;   0x170f + 0x7 + 0x196a = 0x3080 (@R_DIGEST)
;   0x1716 + 0x7 + 0x19a3 = 0x30c0 (@R_LIGNE)
;   0x1722 + 0x7 + 0x1997 = 0x30c0 (@R_LIGNE)
;   0x1731 + 0x7 + 0x1988 = 0x30c0 (@R_LIGNE)
;   0x1759 + 0x7 + 0x1960 = 0x30c0 (@R_LIGNE)
;   0x176b + 0x7 + 0x194e = 0x30c0 (@R_LIGNE)
;   0x1799 + 0x7 + 0x980 = 0x2120 (@R_MSG_USAGE)
;   0x17a7 + 0x7 + 0x992 = 0x2140 (@R_MSG_OUVERTURE)
;   0x17b5 + 0x7 + 0x9a4 = 0x2160 (@R_MSG_LECTURE)
;   0x17c3 + 0x7 + 0x9b6 = 0x2180 (@R_MSG_ECRITURE)
; Symboles (vérifiés par build_ah.py contre layout.py) : @A_ABSORBER=0x1400, @A_ECRITE=0x1000, @A_FINALISER=0x1500, @A_HEX=0x1600, @A_INIT=0x1100, @A_SORTIR=0x1080, @L_ECRITURE=0x1b, @L_LECTURE=0x1b, @L_OUVERTURE=0x1e, @L_USAGE=0x19, @R_CTX=0x3000, @R_DIGEST=0x3080, @R_LIGNE=0x30c0, @R_MSG_ECRITURE=0x2180, @R_MSG_LECTURE=0x2160, @R_MSG_OUVERTURE=0x2140, @R_MSG_USAGE=0x2120, @R_TAMPON=0x4300
mov rax, qword ptr [rsp]
cmp rax, 2
jne 0x1799
mov rbx, qword ptr [rsp + 0x10]
mov eax, 2
mov rdi, rbx
xor esi, esi
xor edx, edx
syscall
test rax, rax
js 0x17a7
mov r12, rax
lea rdi, [rip + 0x194c]
call 0x1100
xor eax, eax
mov rdi, r12
lea rsi, [rip + 0x2c3b]
mov edx, 0x10000
syscall
test rax, rax
js 0x17b5
je 0x16f2
mov r13, rax
lea rdi, [rip + 0x191f]
lea rsi, [rip + 0x2c18]
mov rdx, r13
call 0x1400
jmp 0x16b9
mov eax, 3
mov rdi, r12
syscall
lea rdi, [rip + 0x18fd]
lea rsi, [rip + 0x1976]
call 0x1500
lea rdi, [rip + 0x196a]
lea rsi, [rip + 0x19a3]
call 0x1600
lea rax, [rip + 0x1997]
mov byte ptr [rax + 0x40], 0x20
mov byte ptr [rax + 0x41], 0x20
lea rdi, [rip + 0x1988]
add rdi, 0x42
mov rsi, rbx
movzx eax, byte ptr [rsi]
test al, al
je 0x1752
mov byte ptr [rdi], al
add rdi, 1
add rsi, 1
jmp 0x173f
mov byte ptr [rdi], 0xa
add rdi, 1
lea rax, [rip + 0x1960]
sub rdi, rax
mov r13, rdi
mov edi, 1
lea rsi, [rip + 0x194e]
mov rdx, r13
call 0x1000
test eax, eax
js 0x17c3
xor edi, edi
call 0x1080
mov edi, 2
call 0x1000
mov edi, 1
call 0x1080
lea rsi, [rip + 0x980]
mov edx, 0x19
jmp 0x1785
lea rsi, [rip + 0x992]
mov edx, 0x1e
jmp 0x1785
lea rsi, [rip + 0x9a4]
mov edx, 0x1b
jmp 0x1785
lea rsi, [rip + 0x9b6]
mov edx, 0x1b
jmp 0x1785
