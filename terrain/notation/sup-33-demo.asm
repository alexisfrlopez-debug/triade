; sup-33-demo · bloc terrain · spec sup-33:R1 · bloc carte f60033
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x5400, taille 960 octets
; Dépendances : IAT kernel32#3 : WaitForSingleObject, GetExitCodeProcess, TerminateProcess, Sleep ; IAT user32#2 : FindWindowW, FindWindowExW, SendMessageTimeoutW ; IAT kernel32#1 : CloseHandle ; blocs sup-31, sup-36, libc-02 ; chaînes S10..S16 + NOM_DEMO + CLASSE_DEMO + fixture finale (zones données)
; Notation explicite générée par outils/auteur.py depuis brouillons/sup-33-demo.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 940 o · padding : 20 o (NOP)
; Étiquettes résolues : .boucle_fen=0x544f, .fen_ok=0x548f, .clic_ko=0x5515, .tuer_ko=0x552c, .sondage=0x5558, .boucle_sond=0x555e, .pas_encore=0x5592, .fermeture=0x55a2, .compte=0x561f, .compte_fin=0x5639, .embarque=0x5656, .verdict=0x568b, .ko=0x5700, .absent=0x5732, .fin=0x574b, .lire_journal=0x575a, .fin_ligne=0x577a, .fboucle=0x5783, .fret=0x57a6, .fsuite=0x57a7
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x540e + 0x7 - 0x28fa = 0x2b1b
;   0x5424 + 0x7 - 0x1048 = 0x43e3
;   0x543b + 0x7 - 0x1932 = 0x3b10
;   0x5442 + 0x7 - 0x16f9 = 0x3d50
;   0x5451 + 0x7 - 0x29c6 = 0x2a92
;   0x5458 + 0x6 - 0x30fe = 0x2360
;   0x5468 + 0x6 - 0x312e = 0x2340
;   0x5473 + 0x7 - 0x103f = 0x443b
;   0x5492 + 0x7 - 0x1959 = 0x3b40
;   0x5499 + 0x7 - 0x1081 = 0x441f
;   0x54b5 + 0x7 - 0x2a78 = 0x2a44
;   0x54bf + 0x6 - 0x315d = 0x2368
;   0x54f2 + 0x6 - 0x3188 = 0x2370
;   0x54fc + 0x7 - 0x10ad = 0x4456
;   0x5515 + 0x7 - 0x10a6 = 0x4476
;   0x5534 + 0x6 - 0x321a = 0x2320
;   0x5542 + 0x6 - 0x3238 = 0x2310
;   0x554b + 0x6 - 0x3459 = 0x20f8
;   0x556e + 0x7 - 0x1825 = 0x3d50
;   0x557c + 0x7 - 0xd11 = 0x4872
;   0x5597 + 0x6 - 0x325d = 0x2340
;   0x55ca + 0x6 - 0x3260 = 0x2370
;   0x55d8 + 0x6 - 0x32ce = 0x2310
;   0x55e1 + 0x7 - 0x1a98 = 0x3b50
;   0x55e8 + 0x6 - 0x32d6 = 0x2318
;   0x55f1 + 0x6 - 0x34ff = 0x20f8
;   0x55f7 + 0x7 - 0x1175 = 0x4489
;   0x5609 + 0x7 - 0x1ac0 = 0x3b50
;   0x5630 + 0x7 - 0x1adf = 0x3b58
;   0x5639 + 0x7 - 0x119a = 0x44a6
;   0x5656 + 0x7 - 0x1b05 = 0x3b58
;   0x5691 + 0x7 - 0x1b48 = 0x3b50
;   0x569a + 0x7 - 0x1b49 = 0x3b58
;   0x56a7 + 0x7 - 0x195e = 0x3d50
;   0x56b5 + 0x7 - 0xe4a = 0x4872
;   0x56cb + 0x7 - 0x1211 = 0x44c1
;   0x56e2 + 0x7 - 0x11e2 = 0x4507
;   0x5700 + 0x7 - 0x1225 = 0x44e2
;   0x5717 + 0x7 - 0x1206 = 0x4518
;   0x5732 + 0x7 - 0x1330 = 0x4409
;   0x575e + 0x7 + 0xc3e = 0x63a3
;   0x577c + 0x7 - 0x1c2b = 0x3b58
push rbx
push r12
push r13
push r14
push r15
push rbp
sub rsp, 0x48
lea rcx, [rip - 0x28fa]
xor edx, edx
call 0x5200
test eax, eax
je 0x5732
lea rcx, [rip - 0x1048]
mov edx, 38
xor r8d, r8d
xor r9d, r9d
call 0x5000
mov r12, qword ptr [rip - 0x1932]
lea rbx, [rip - 0x16f9]
mov r15d, 200
xor ecx, ecx
lea rdx, [rip - 0x29c6]
call qword ptr [rip - 0x30fe]
test rax, rax
jne 0x548f
mov ecx, 50
call qword ptr [rip - 0x312e]
dec r15d
jne 0x544f
lea rcx, [rip - 0x103f]
mov edx, 27
xor r8d, r8d
xor r9d, r9d
call 0x5000
jmp 0x552c
mov r14, rax
mov qword ptr [rip - 0x1959], rax
lea rcx, [rip - 0x1081]
mov edx, 28
xor r8d, r8d
xor r9d, r9d
call 0x5000
mov rcx, r14
xor edx, edx
lea r8, [rip - 0x2a78]
xor r9d, r9d
call qword ptr [rip - 0x315d]
test rax, rax
je 0x5515
mov rcx, rax
mov edx, 0xF5
xor r8d, r8d
xor r9d, r9d
mov dword ptr [rsp + 0x20], 2
mov dword ptr [rsp + 0x28], 90000
lea rax, [rsp + 0x38]
mov qword ptr [rsp + 0x30], rax
call qword ptr [rip - 0x3188]
test eax, eax
je 0x5515
lea rcx, [rip - 0x10ad]
mov edx, 32
xor r8d, r8d
xor r9d, r9d
call 0x5000
jmp 0x5558
lea rcx, [rip - 0x10a6]
mov edx, 19
xor r8d, r8d
xor r9d, r9d
call 0x5000
mov rcx, r12
mov edx, 1
call qword ptr [rip - 0x321a]
mov rcx, r12
mov edx, 5000
call qword ptr [rip - 0x3238]
mov rcx, r12
call qword ptr [rip - 0x3459]
xor eax, eax
jmp 0x574b
mov r15d, 150
call 0x575a
test rax, rax
je 0x5592
cmp rax, 31
jb 0x5592
lea rcx, [rip - 0x1825]
add rcx, rax
sub rcx, 31
lea rdx, [rip - 0xd11]
mov r8d, 31
call 0x1180
test eax, eax
je 0x55a2
mov ecx, 200
call qword ptr [rip - 0x325d]
dec r15d
jne 0x555e
mov rcx, r14
mov edx, 0x10
xor r8d, r8d
xor r9d, r9d
mov dword ptr [rsp + 0x20], 2
mov dword ptr [rsp + 0x28], 10000
lea rax, [rsp + 0x38]
mov qword ptr [rsp + 0x30], rax
call qword ptr [rip - 0x3260]
mov rcx, r12
mov edx, 10000
call qword ptr [rip - 0x32ce]
mov rcx, r12
lea rdx, [rip - 0x1a98]
call qword ptr [rip - 0x32d6]
mov rcx, r12
call qword ptr [rip - 0x34ff]
lea rcx, [rip - 0x1175]
mov edx, 29
mov r8d, 1
mov r9d, dword ptr [rip - 0x1ac0]
call 0x5000
call 0x575a
xor r13d, r13d
xor ecx, ecx
call 0x577a
test rdx, rdx
je 0x5639
inc r13d
lea rcx, [rax + 2]
cmp rcx, qword ptr [rip - 0x1adf]
jb 0x561f
lea rcx, [rip - 0x119a]
mov edx, 27
mov r8d, 1
mov r9d, r13d
call 0x5000
xor r15d, r15d
cmp r15, qword ptr [rip - 0x1b05]
jae 0x568b
mov rcx, r15
call 0x577a
mov r14, r15
mov r15, rax
lea rbp, [rax + rdx]
lea rcx, [rbx + r14]
mov rdx, r15
sub rdx, r14
xor r8d, r8d
xor r9d, r9d
call 0x5000
mov r15, rbp
jmp 0x5656
cmp r13d, 17
jne 0x5700
cmp dword ptr [rip - 0x1b48], 0
jne 0x5700
mov rax, qword ptr [rip - 0x1b49]
cmp rax, 31
jb 0x5700
lea rcx, [rip - 0x195e]
add rcx, rax
sub rcx, 31
lea rdx, [rip - 0xe4a]
mov r8d, 31
call 0x1180
test eax, eax
jne 0x5700
lea rcx, [rip - 0x1211]
mov edx, 33
xor r8d, r8d
xor r9d, r9d
call 0x5000
lea rcx, [rip - 0x11e2]
mov edx, 17
xor r8d, r8d
xor r9d, r9d
call 0x5000
mov eax, 1
jmp 0x574b
lea rcx, [rip - 0x1225]
mov edx, 37
xor r8d, r8d
xor r9d, r9d
call 0x5000
lea rcx, [rip - 0x1206]
mov edx, 17
xor r8d, r8d
xor r9d, r9d
call 0x5000
xor eax, eax
jmp 0x574b
lea rcx, [rip - 0x1330]
mov edx, 22
xor r8d, r8d
xor r9d, r9d
call 0x5000
xor eax, eax
add rsp, 0x48
pop rbp
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
sub rsp, 8
lea rcx, [rip + 0xc3e]
xor edx, edx
mov r8d, 17
xor r9d, r9d
call 0x4e00
add rsp, 8
ret
xor edx, edx
mov rax, qword ptr [rip - 0x1c2b]
cmp rcx, rax
jae 0x57a6
cmp byte ptr [rbx + rcx], 0x0D
jne 0x57a7
lea r9, [rcx + 1]
cmp r9, rax
jae 0x57a6
cmp byte ptr [rbx + r9], 0x0A
jne 0x57a7
mov rax, rcx
mov edx, 2
ret
inc rcx
jmp 0x5783
