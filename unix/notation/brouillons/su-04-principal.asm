; su-04-principal · brouillon étiqueté — spec su-04:R1, bloc carte f60004
; _start (e_entry 0x1140, RELATIF à la base — ET_DYN/PIE) : [rsp]=argc…,
; rsp ≡ 0 mod 16, aucun push dans le corps (pas de cadre d'appelant).
; rbx = base de chargement (non-volatil SysV, traversant) ; r10 = registre
; de travail interne : il porte le rax brut à travers su-02/su-03 (qui
; clobber r8/r9) — su-01 n'y touche pas (syscall : rcx/r11 seuls détruits).
; Le sous-programme local .emit (déclaré I1) émet la ligne d'une sonde et
; rend le verdict : entrée rax = résultat brut, r8 = RVA du préfixe, r9 =
; longueur, rbx = base ; r8/r9 sont consommés AVANT le premier appel (ils
; meurent au premier) ; le verdict vit au tampon .bss +32 (la mémoire
; traverse les appels et les syscalls — r11 meurt dans chaque su-01).
; émissions vérifiées (I6) : rax < 0 → .echec (canal de constat atteint) ;
; sondes volontaires NON vérifiées sur place : leur rax négatif est le
; PAYLOAD, il passe par .emit → su-03 (jamais au hasard).
@A_ECRIRE = 0x1000
@A_HEX64 = 0x1040
@A_VERDICT = 0x10C0
@MSG_BASE = 0x1C0
@L_BASE = 15
@MSG_P1 = 0x1E0
@L_P1 = 26
@MSG_P2 = 0x200
@L_P2 = 27
@MSG_VERD = 0x220
@L_VERD = 11
@MSG_FIN = 0x240
@L_FIN = 1
@MSG_FATAL = 0x260
@L_FATAL = 37
@TAMPON = 0x2000
@TAMPON_VERD = 0x2010
@TAMPON_NUM = 0x2020
lea rbx, [rip + @MSG_BASE]
sub rbx, @MSG_BASE
mov rdi, rbx
lea rsi, [rbx + @TAMPON]
call @A_HEX64
mov edi, 1
lea rsi, [rbx + @MSG_BASE]
mov edx, @L_BASE
call @A_ECRIRE
test rax, rax
js .echec
mov edi, 1
lea rsi, [rbx + @TAMPON]
mov edx, 16
call @A_ECRIRE
test rax, rax
js .echec
mov edi, 1
lea rsi, [rbx + @MSG_FIN]
mov edx, @L_FIN
call @A_ECRIRE
test rax, rax
js .echec
mov edi, -1
lea rsi, [rbx + @MSG_BASE]
mov edx, @L_BASE
call @A_ECRIRE
mov r8d, @MSG_P1
mov r9d, @L_P1
call .emit
mov edi, 1
mov esi, 1
mov edx, @L_P2
call @A_ECRIRE
mov r8d, @MSG_P2
mov r9d, @L_P2
call .emit
cmp eax, 6
je .fatal
mov eax, 231
xor edi, edi
syscall
.emit:
sub rsp, 8
mov r10, rax
mov edi, 1
lea rsi, [rbx + r8]
mov edx, r9d
call @A_ECRIRE
test rax, rax
js .echec
mov rdi, r10
call @A_VERDICT
mov dword ptr [rbx + @TAMPON_NUM], eax
mov rdi, rax
lea rsi, [rbx + @TAMPON_VERD]
call @A_HEX64
mov rdi, r10
lea rsi, [rbx + @TAMPON]
call @A_HEX64
mov edi, 1
lea rsi, [rbx + @TAMPON]
mov edx, 16
call @A_ECRIRE
test rax, rax
js .echec
mov edi, 1
lea rsi, [rbx + @MSG_VERD]
mov edx, @L_VERD
call @A_ECRIRE
test rax, rax
js .echec
mov edi, 1
lea rsi, [rbx + @TAMPON_VERD]
mov edx, 16
call @A_ECRIRE
test rax, rax
js .echec
mov edi, 1
lea rsi, [rbx + @MSG_FIN]
mov edx, @L_FIN
call @A_ECRIRE
test rax, rax
js .echec
mov eax, dword ptr [rbx + @TAMPON_NUM]
add rsp, 8
ret
.echec:
mov rdi, rax
call @A_VERDICT
cmp eax, 6
je .fatal
mov eax, 231
xor edi, edi
syscall
.fatal:
mov edi, 1
lea rsi, [rbx + @MSG_FATAL]
mov edx, @L_FATAL
call @A_ECRIRE
mov eax, 231
mov edi, 6
syscall
