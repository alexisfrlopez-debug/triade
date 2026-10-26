; av-17-principal · bloc orchestration du vérificateur sceau · spec av-17:R1 · bloc carte d50017
; Profil : x86-64-linux-elf64 · ABI SysV · slot RVA 0x2920, taille 640 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/av-17-principal.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 478 o · padding : 162 o (NOP)
; Étiquettes résolues : .copie=0x2a2b, .copie_fin=0x2a3e, .ecriture_ko=0x2ac3, .erreur_deux=0x2ad6, .erreur_un=0x2aea, .fin_lecture=0x29ba, .lecture=0x2981, .lecture_ko=0x2ab0, .ouverture=0x2a9d, .quatre=0x2a71, .usage=0x2a8a
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x2975 + 0x7 + 0x1684 = 0x4000 (@R_CTX)
;   0x2986 + 0x7 + 0x3273 = 0x5c00 (@R_TAMPON)
;   0x29a2 + 0x7 + 0x1657 = 0x4000 (@R_CTX)
;   0x29a9 + 0x7 + 0x3250 = 0x5c00 (@R_TAMPON)
;   0x29c4 + 0x7 + 0x1635 = 0x4000 (@R_CTX)
;   0x29cb + 0x7 + 0x172e = 0x4100 (@R_DIGEST)
;   0x29d7 + 0x7 + 0x1722 = 0x4100 (@R_DIGEST)
;   0x29de + 0x7 + 0x181b = 0x4200 (@R_LIGNE)
;   0x29ea + 0x7 + 0x170f = 0x4100 (@R_DIGEST)
;   0x29f5 + 0x7 + 0x1804 = 0x4200 (@R_LIGNE)
;   0x2a05 + 0x7 + 0x17f4 = 0x4200 (@R_LIGNE)
;   0x2a1a + 0x7 + 0x17df = 0x4200 (@R_LIGNE)
;   0x2a45 + 0x7 + 0x17b4 = 0x4200 (@R_LIGNE)
;   0x2a57 + 0x7 + 0x17a2 = 0x4200 (@R_LIGNE)
;   0x2a7c + 0x7 + 0xa7d = 0x3500 (@R_MSG_CHANTIER)
;   0x2a8f + 0x7 + 0x96a = 0x3400 (@R_MSG_USAGE)
;   0x2aa2 + 0x7 + 0x9b7 = 0x3460 (@R_MSG_OUVERTURE)
;   0x2ab5 + 0x7 + 0x9c4 = 0x3480 (@R_MSG_LECTURE)
;   0x2ac8 + 0x7 + 0x9d1 = 0x34a0 (@R_MSG_ECRITURE)
; Symboles (vérifiés par build_sceau.py contre layout.py) : @A_ABSORBER=0x1680, @A_ECRITE=0x1000, @A_FINALISER=0x1780, @A_HEX=0x1600, @A_INIT=0x1100, @A_SORTIR=0x1080, @L_CHANTIER=0x36, @L_ECRITURE=0x19, @L_LECTURE=0x19, @L_OUVERTURE=0x1c, @L_USAGE=0x44, @MAGIC_HACHER=0x7265686361682d2d, @R_CTX=0x4000, @R_DIGEST=0x4100, @R_LIGNE=0x4200, @R_MSG_CHANTIER=0x3500, @R_MSG_ECRITURE=0x34a0, @R_MSG_LECTURE=0x3480, @R_MSG_OUVERTURE=0x3460, @R_MSG_USAGE=0x3400, @R_TAMPON=0x5c00
mov r14, qword ptr [rsp]
cmp r14, 3
jl 0x2a8a
jg 0x2a71
mov rbx, qword ptr [rsp + 0x10]
movabs rax, 0x7265686361682d2d
cmp qword ptr [rbx], rax
jne 0x2a8a
cmp byte ptr [rbx + 8], 0
jne 0x2a8a
mov rbx, qword ptr [rsp + 0x18]
mov eax, 2
mov rdi, rbx
xor esi, esi
xor edx, edx
syscall
test rax, rax
js 0x2a9d
mov r12, rax
lea rdi, [rip + 0x1684]
call 0x1100
xor eax, eax
mov rdi, r12
lea rsi, [rip + 0x3273]
mov edx, 0x10000
syscall
test rax, rax
js 0x2ab0
je 0x29ba
mov r13, rax
lea rdi, [rip + 0x1657]
lea rsi, [rip + 0x3250]
mov rdx, r13
call 0x1680
jmp 0x2981
mov eax, 3
mov rdi, r12
syscall
lea rdi, [rip + 0x1635]
lea rsi, [rip + 0x172e]
call 0x1780
lea rdi, [rip + 0x1722]
lea rsi, [rip + 0x181b]
call 0x1600
lea rdi, [rip + 0x170f]
add rdi, 0x20
lea rsi, [rip + 0x1804]
add rsi, 0x40
call 0x1600
lea rax, [rip + 0x17f4]
mov byte ptr [rax + 0x80], 0x20
mov byte ptr [rax + 0x81], 0x20
lea rdi, [rip + 0x17df]
add rdi, 0x82
mov rsi, rbx
movzx eax, byte ptr [rsi]
test al, al
je 0x2a3e
mov byte ptr [rdi], al
add rdi, 1
add rsi, 1
jmp 0x2a2b
mov byte ptr [rdi], 0xa
add rdi, 1
lea rax, [rip + 0x17b4]
sub rdi, rax
mov r13, rdi
mov edi, 1
lea rsi, [rip + 0x17a2]
mov rdx, r13
call 0x1000
test eax, eax
js 0x2ac3
xor edi, edi
call 0x1080
cmp r14, 4
jne 0x2a8a
mov edi, 2
lea rsi, [rip + 0xa7d]
mov edx, 0x36
jmp 0x2ad6
mov edi, 2
lea rsi, [rip + 0x96a]
mov edx, 0x44
jmp 0x2aea
mov edi, 2
lea rsi, [rip + 0x9b7]
mov edx, 0x1c
jmp 0x2aea
mov edi, 2
lea rsi, [rip + 0x9c4]
mov edx, 0x19
jmp 0x2aea
mov edi, 2
lea rsi, [rip + 0x9d1]
mov edx, 0x19
jmp 0x2aea
mov edi, 2
call 0x1000
mov edi, 2
call 0x1080
mov edi, 2
call 0x1000
mov edi, 1
call 0x1080
