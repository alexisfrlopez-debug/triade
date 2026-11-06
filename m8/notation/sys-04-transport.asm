; sys-04-transport · bloc le transport établi — le socket natif par AFD, sans ws2_32 (create + bind WILDCARD + connect) · spec sys-04:R1 · bloc carte g90004
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0xa240, taille 768 octets
; Dépendances : sys-02 × 3 PUIS sys-01 × 3 — create PUIS bind PUIS connect, la séquence MESURÉE mswsock (I6) ; chaque SSN résolu au geste même (Q3) ; les fixtures .text6 DEVICE/EA/BIND et les noms de résolution cités par déplacement (I3/T5)
; Notation explicite générée par outils/auteur.py depuis brouillons/sys-04-transport.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 676 o · padding : 92 o (NOP)
; Étiquettes résolues : .status_nonnul=0xa499, .status_iosb_create=0xa4a5, .status_iosb_bind=0xa4b2, .status_iosb_connect=0xa4bf, .resolution_echouee=0xa4cf, .epilogue=0xa4d9
; Déplacements RIP (cible = adresse + taille + disp) :
;   0xa253 + 0x7 + 0x6a56 = 0x10cb0
;   0xa284 + 0x7 + 0x6995 = 0x10c20
;   0xa321 + 0x7 + 0x6928 = 0x10c50
;   0xa34e + 0x7 + 0x696b = 0x10cc0
;   0xa38b + 0x7 + 0x68fe = 0x10c90
;   0xa3ce + 0x7 + 0x68eb = 0x10cc0
push rbx
push rbp
push rdi
sub rsp, 0x110
mov rbp, rcx
mov rdi, rdx
mov rbx, r8
lea rcx, [rip + 0x6a56]
mov edx, 11
mov r8, rbp
call 0xa040
test rax, rax
js 0xa4cf
mov word ptr [rsp + 0xC0], 40
mov word ptr [rsp + 0xC2], 42
lea r10, [rip + 0x6995]
mov qword ptr [rsp + 0xC8], r10
mov dword ptr [rsp + 0x90], 0x30
mov qword ptr [rsp + 0x98], 0
lea r10, [rsp + 0xC0]
mov qword ptr [rsp + 0xA0], r10
mov dword ptr [rsp + 0xA8], 0x40
mov qword ptr [rsp + 0xB0], 0
mov qword ptr [rsp + 0xB8], 0
lea rcx, [rsp + 0x58]
mov edx, 0xC0140000
lea r8, [rsp + 0x90]
lea r9, [rsp + 0x60]
mov qword ptr [rsp + 0x20], 0
mov qword ptr [rsp + 0x28], 0
mov qword ptr [rsp + 0x30], 3
mov qword ptr [rsp + 0x38], 1
mov qword ptr [rsp + 0x40], 0x20
lea r10, [rip + 0x6928]
mov qword ptr [rsp + 0x48], r10
mov qword ptr [rsp + 0x50], 54
call 0xa000
test eax, eax
jne 0xa499
cmp dword ptr [rsp + 0x60], 0
jne 0xa4a5
lea rcx, [rip + 0x696b]
mov edx, 21
mov r8, rbp
call 0xa040
test rax, rax
js 0xa4cf
mov rcx, qword ptr [rsp + 0x58]
xor edx, edx
xor r8d, r8d
xor r9d, r9d
lea r10, [rsp + 0x70]
mov qword ptr [rsp + 0x20], r10
mov qword ptr [rsp + 0x28], 0x12003
lea r10, [rip + 0x68fe]
mov qword ptr [rsp + 0x30], r10
mov qword ptr [rsp + 0x38], 0x14
lea r10, [rsp + 0xF8]
mov qword ptr [rsp + 0x40], r10
mov qword ptr [rsp + 0x48], 0x10
call 0xa000
test eax, eax
jne 0xa499
cmp dword ptr [rsp + 0x70], 0
jne 0xa4b2
lea rcx, [rip + 0x68eb]
mov edx, 21
mov r8, rbp
call 0xa040
test rax, rax
js 0xa4cf
mov qword ptr [rsp + 0xD0], 0
mov qword ptr [rsp + 0xD8], 0
mov qword ptr [rsp + 0xE0], 0
mov r10, qword ptr [rdi]
mov qword ptr [rsp + 0xE8], r10
mov r10, qword ptr [rdi + 8]
mov qword ptr [rsp + 0xF0], r10
mov rcx, qword ptr [rsp + 0x58]
xor edx, edx
xor r8d, r8d
xor r9d, r9d
lea r10, [rsp + 0x80]
mov qword ptr [rsp + 0x20], r10
mov qword ptr [rsp + 0x28], 0x12007
lea r10, [rsp + 0xD0]
mov qword ptr [rsp + 0x30], r10
mov qword ptr [rsp + 0x38], 0x28
mov qword ptr [rsp + 0x40], 0
mov qword ptr [rsp + 0x48], 0
call 0xa000
test eax, eax
jne 0xa499
cmp dword ptr [rsp + 0x80], 0
jne 0xa4bf
mov r10, qword ptr [rsp + 0x58]
mov qword ptr [rbx], r10
xor eax, eax
add rsp, 0x110
pop rdi
pop rbp
pop rbx
ret
mov rdx, rax
mov rax, -6
jmp 0xa4d9
mov edx, dword ptr [rsp + 0x60]
mov rax, -6
jmp 0xa4d9
mov edx, dword ptr [rsp + 0x70]
mov rax, -6
jmp 0xa4d9
mov edx, dword ptr [rsp + 0x80]
mov rax, -6
jmp 0xa4d9
mov rdx, rax
mov rax, -1
add rsp, 0x110
pop rdi
pop rbp
pop rbx
ret
