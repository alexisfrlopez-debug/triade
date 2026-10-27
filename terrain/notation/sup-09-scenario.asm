; sup-09-scenario · bloc terrain · spec sup-09:R1 · bloc carte f60009
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x4c00, taille 512 octets
; Dépendances : blocs win-05 (entrée trace), win-06 autotest, sup-33, sup-34, sup-35 ; lignes S00..S03/S90/S91 (zone données sup) ; TAMPON_AFF (.data)
; Notation explicite générée par outils/auteur.py depuis brouillons/sup-09-scenario.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 335 o · padding : 177 o (NOP)
; Étiquettes résolues : .porte_ok=0x4c7d, .libc_ok=0x4ccc, .echec=0x4d28, .fin=0x4d41
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x4c0d + 0x7 - 0x8d4 = 0x4340
;   0x4c24 + 0x7 - 0x113b = 0x3af0
;   0x4c48 + 0x7 - 0x8c0 = 0x438f
;   0x4c5f + 0x7 - 0x496 = 0x47d0
;   0x4c7d + 0x7 - 0x914 = 0x4370
;   0x4c9a + 0x7 - 0x8d9 = 0x43c8
;   0x4cb1 + 0x7 - 0x4e8 = 0x47d0
;   0x4ccc + 0x7 - 0x92a = 0x43a9
;   0x4d0a + 0x7 - 0x55a = 0x47b7
;   0x4d28 + 0x7 - 0x55f = 0x47d0
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x20
lea rcx, [rip - 0x8d4]
mov edx, 39
xor r8d, r8d
xor r9d, r9d
call 0x5000
lea rcx, [rip - 0x113b]
mov edx, 24
xor r8d, r8d
xor r9d, r9d
call 0x5000
call 0x1ac0
mov r15d, eax
cmp eax, 0xFFFFFFFF
jne 0x4c7d
lea rcx, [rip - 0x8c0]
mov edx, 26
xor r8d, r8d
xor r9d, r9d
call 0x5000
lea rcx, [rip - 0x496]
mov edx, 40
xor r8d, r8d
xor r9d, r9d
call 0x5000
xor eax, eax
jmp 0x4d41
lea rcx, [rip - 0x914]
mov edx, 31
xor r8d, r8d
xor r9d, r9d
call 0x5000
cmp r15d, 4
je 0x4ccc
lea rcx, [rip - 0x8d9]
mov edx, 27
xor r8d, r8d
xor r9d, r9d
call 0x5000
lea rcx, [rip - 0x4e8]
mov edx, 40
xor r8d, r8d
xor r9d, r9d
call 0x5000
xor eax, eax
jmp 0x4d41
lea rcx, [rip - 0x92a]
mov edx, 31
xor r8d, r8d
xor r9d, r9d
call 0x5000
call 0x5400
mov r12d, eax
call 0x5800
mov r13d, eax
call 0x5e00
mov r14d, eax
test r12d, r12d
je 0x4d28
test r13d, r13d
je 0x4d28
test r14d, r14d
je 0x4d28
lea rcx, [rip - 0x55a]
mov edx, 25
xor r8d, r8d
xor r9d, r9d
call 0x5000
mov eax, 1
jmp 0x4d41
lea rcx, [rip - 0x55f]
mov edx, 40
xor r8d, r8d
xor r9d, r9d
call 0x5000
xor eax, eax
add rsp, 0x20
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
