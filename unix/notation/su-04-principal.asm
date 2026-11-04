; su-04-principal · bloc orchestration sonde · spec su-04:R1 · bloc carte f60004
; Profil : x86-64-linux-elf64 · ABI SysV · slot RVA 0x1140, taille 640 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/su-04-principal.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 468 o · padding : 172 o (NOP)
; Étiquettes résolues : .echec=0x12dc, .emit=0x1218, .fatal=0x12f2
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x1140 + 0x7 - 0xf87 = 0x1c0 (@MSG_BASE)
; Symboles (vérifiés par build_m6.py contre layout.py) : @A_ECRIRE=0x1000, @A_HEX64=0x1040, @A_VERDICT=0x10c0, @L_BASE=0xf, @L_FATAL=0x25, @L_FIN=0x1, @L_P1=0x1a, @L_P2=0x1b, @L_VERD=0xb, @MSG_BASE=0x1c0, @MSG_FATAL=0x260, @MSG_FIN=0x240, @MSG_P1=0x1e0, @MSG_P2=0x200, @MSG_VERD=0x220, @TAMPON=0x2000, @TAMPON_NUM=0x2020, @TAMPON_VERD=0x2010
lea rbx, [rip - 0xf87]
sub rbx, 0x1c0
mov rdi, rbx
lea rsi, [rbx + 0x2000]
call 0x1040
mov edi, 1
lea rsi, [rbx + 0x1c0]
mov edx, 0xf
call 0x1000
test rax, rax
js 0x12dc
mov edi, 1
lea rsi, [rbx + 0x2000]
mov edx, 0x10
call 0x1000
test rax, rax
js 0x12dc
mov edi, 1
lea rsi, [rbx + 0x240]
mov edx, 1
call 0x1000
test rax, rax
js 0x12dc
mov edi, 0xffffffff
lea rsi, [rbx + 0x1c0]
mov edx, 0xf
call 0x1000
mov r8d, 0x1e0
mov r9d, 0x1a
call 0x1218
mov edi, 1
mov esi, 1
mov edx, 0x1b
call 0x1000
mov r8d, 0x200
mov r9d, 0x1b
call 0x1218
cmp eax, 6
je 0x12f2
mov eax, 0xe7
xor edi, edi
syscall
sub rsp, 8
mov r10, rax
mov edi, 1
lea rsi, [rbx + r8]
mov edx, r9d
call 0x1000
test rax, rax
js 0x12dc
mov rdi, r10
call 0x10c0
mov dword ptr [rbx + 0x2020], eax
mov rdi, rax
lea rsi, [rbx + 0x2010]
call 0x1040
mov rdi, r10
lea rsi, [rbx + 0x2000]
call 0x1040
mov edi, 1
lea rsi, [rbx + 0x2000]
mov edx, 0x10
call 0x1000
test rax, rax
js 0x12dc
mov edi, 1
lea rsi, [rbx + 0x220]
mov edx, 0xb
call 0x1000
test rax, rax
js 0x12dc
mov edi, 1
lea rsi, [rbx + 0x2010]
mov edx, 0x10
call 0x1000
test rax, rax
js 0x12dc
mov edi, 1
lea rsi, [rbx + 0x240]
mov edx, 1
call 0x1000
test rax, rax
js 0x12dc
mov eax, dword ptr [rbx + 0x2020]
add rsp, 8
ret
mov rdi, rax
call 0x10c0
cmp eax, 6
je 0x12f2
mov eax, 0xe7
xor edi, edi
syscall
mov edi, 1
lea rsi, [rbx + 0x260]
mov edx, 0x25
call 0x1000
mov eax, 0xe7
mov edi, 6
syscall
