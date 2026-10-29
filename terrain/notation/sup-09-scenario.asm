; sup-09-scenario · bloc terrain · spec sup-09:R4 · bloc carte f60009
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x4c00, taille 512 octets
; Dépendances : blocs win-05 (entrée trace), win-06 autotest, sup-39 (prévol D101), sup-33, sup-34, sup-38, sup-35 ; lignes S00..S03/S90/S91 (zone données sup) ; TAMPON_AFF (.data) — R3 (terrain.17) : T4 entre T2 et T3, verdict à quatre tests ; R4 (terrain.18) : prévol orphelins + amont AVANT l'extraction (D101)
; Notation explicite générée par outils/auteur.py depuis brouillons/sup-09-scenario.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 432 o · padding : 80 o (NOP)
; Étiquettes résolues : .porte_ok=0x4c7d, .libc_ok=0x4ccf, .sans_t1=0x4d08, .apres_t1=0x4d0b, .sans_t2=0x4d1e, .apres_t2=0x4d21, .sans_t4=0x4d33, .apres_t4=0x4d35, .sans_t3=0x4d48, .apres_t3=0x4d4e, .echec=0x4d89, .fin=0x4da2
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x4c0d + 0x7 - 0x8d4 = 0x4340
;   0x4c24 + 0x7 - 0x113b = 0x3af0
;   0x4c48 + 0x7 - 0x8c0 = 0x438f
;   0x4c5f + 0x7 - 0x499 = 0x47cd
;   0x4c7d + 0x7 - 0x914 = 0x4370
;   0x4c9a + 0x7 - 0x8d9 = 0x43c8
;   0x4cb1 + 0x7 - 0x4eb = 0x47cd
;   0x4ccf + 0x7 - 0x92d = 0x43a9
;   0x4d6b + 0x7 - 0x5be = 0x47b4
;   0x4d89 + 0x7 - 0x5c3 = 0x47cd
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
lea rcx, [rip - 0x499]
mov edx, 40
xor r8d, r8d
xor r9d, r9d
call 0x5000
xor eax, eax
jmp 0x4da2
lea rcx, [rip - 0x914]
mov edx, 31
xor r8d, r8d
xor r9d, r9d
call 0x5000
cmp r15d, 4
je 0x4ccf
lea rcx, [rip - 0x8d9]
mov edx, 27
xor r8d, r8d
xor r9d, r9d
call 0x5000
lea rcx, [rip - 0x4eb]
mov edx, 40
xor r8d, r8d
xor r9d, r9d
call 0x5000
xor eax, eax
jmp 0x4da2
lea rcx, [rip - 0x92d]
mov edx, 31
xor r8d, r8d
xor r9d, r9d
call 0x5000
call 0x4b40
xor ecx, ecx
call 0x6600
mov r15d, eax
test r15d, 1
je 0x4d08
call 0x5400
mov r12d, eax
jmp 0x4d0b
xor r12d, r12d
test r15d, 2
je 0x4d1e
call 0x5800
mov r13d, eax
jmp 0x4d21
xor r13d, r13d
test r15d, 2
je 0x4d33
call 0x7200
mov ebx, eax
jmp 0x4d35
xor ebx, ebx
test r15d, 4
je 0x4d48
call 0x5e00
mov r14d, eax
jmp 0x4d4e
mov r14d, 1
mov ecx, 1
call 0x6600
test r12d, r12d
je 0x4d89
test r13d, r13d
je 0x4d89
test ebx, ebx
je 0x4d89
test r14d, r14d
je 0x4d89
lea rcx, [rip - 0x5be]
mov edx, 25
xor r8d, r8d
xor r9d, r9d
call 0x5000
mov eax, 1
jmp 0x4da2
lea rcx, [rip - 0x5c3]
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
