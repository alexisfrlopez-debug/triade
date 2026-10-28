; tls-06-emission · bloc émission chiffrée · spec tls-06:R1 · bloc carte g70006
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x6740, taille 768 octets
; Dépendances : IAT secur32 QueryContextAttributesW / EncryptMessage ; tcp-04 ; tls-03 type 1 ; tailles négociées
; Notation explicite générée par outils/auteur.py depuis brouillons/tls-06-emission.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 491 o · padding : 277 o (NOP)
; Étiquettes résolues : .acquises=0x67a6, .tailles=0x67a6, .morceau=0x67a6, .borne=0x67bc, .boucle_envoi=0x6870, .emis=0x68af, .em_echec=0x68e9, .rompue=0x6916, .echec=0x691b
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x676e + 0x6 - 0x3d54 = 0x2a20
;   0x6826 + 0x6 - 0x3e04 = 0x2a28
sub rsp, 0xE8
mov qword ptr [rsp + 0x60], rcx
mov qword ptr [rsp + 0x68], rdx
mov qword ptr [rsp + 0x70], r8
mov rax, [rsp + 0x60]
cmp dword ptr [rax + 0x4C], 0
jne 0x67a6
lea rcx, [rax + 0x10]
mov edx, 4
lea r8, [rax + 0x40]
call qword ptr [rip - 0x3d54]
movsxd rcx, eax
call 0x6080
mov r10, [rsp + 0x60]
mov dword ptr [r10 + 0x34], edx
test eax, eax
jz 0x67a6
mov qword ptr [r10 + 0x40], 0
mov qword ptr [r10 + 0x48], 0
mov dword ptr [r10 + 0x50], 0
jmp 0x691b
mov rax, [rsp + 0x60]
mov r11d, [rax + 0x48]
mov rax, [rsp + 0x70]
cmp rax, r11
jbe 0x67bc
mov rax, r11
mov [rsp + 0x78], rax
mov rax, [rsp + 0x60]
mov ecx, [rax + 0x40]
lea rcx, [rax + rcx + 0x260]
mov rdx, [rsp + 0x68]
mov r8, [rsp + 0x78]
call 0x1100
mov rax, [rsp + 0x60]
lea r11, [rax + 0x40]
mov [rsp + 0x20], r11
mov ecx, [rax + 0x40]
lea rdx, [rax + rcx + 0x260]
mov r8, [rsp + 0x78]
lea r9, [rsp + 0x90]
mov ecx, 1
call 0x6180
mov rax, [rsp + 0x60]
lea rcx, [rax + 0x10]
xor edx, edx
lea r8, [rsp + 0x90]
xor r9d, r9d
call qword ptr [rip - 0x3e04]
movsxd rcx, eax
call 0x6080
mov r10, [rsp + 0x60]
mov dword ptr [r10 + 0x34], edx
test eax, eax
jnz 0x68e9
mov eax, [rsp + 0xA0]
mov ecx, [rsp + 0xB0]
add eax, ecx
mov ecx, [rsp + 0xC0]
add eax, ecx
mov [rsp + 0x88], rax
xor eax, eax
mov [rsp + 0x80], rax
mov rax, [rsp + 0x88]
mov r8, [rsp + 0x80]
sub rax, r8
jz 0x68af
mov rdx, [rsp + 0x60]
mov rcx, [rdx + 0x20]
lea rdx, [rdx + 0x260]
add rdx, r8
mov r8, rax
call 0x4180
test rax, rax
jle 0x6916
add qword ptr [rsp + 0x80], rax
jmp 0x6870
mov rax, [rsp + 0x68]
add rax, [rsp + 0x78]
mov [rsp + 0x68], rax
mov rax, [rsp + 0x70]
sub rax, [rsp + 0x78]
mov [rsp + 0x70], rax
jnz 0x67a6
mov rax, [rsp + 0x60]
mov dword ptr [rax + 0x30], 0
xor eax, eax
add rsp, 0xE8
ret
mov dword ptr [rsp + 0x58], eax
mov rdx, [rsp + 0x60]
lea rcx, [rdx + 0x260]
mov r8d, [rdx + 0x40]
add r8d, [rdx + 0x44]
mov rax, [rsp + 0x78]
add r8d, eax
xor edx, edx
call 0x13c0
mov eax, [rsp + 0x58]
jmp 0x691b
mov eax, 5
mov rdx, [rsp + 0x60]
mov [rdx + 0x30], eax
add rsp, 0xE8
ret
