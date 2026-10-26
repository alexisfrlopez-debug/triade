; win-10-echange · bloc démo · spec win-10:R1 · bloc carte d40010
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x4980, taille 384 octets
; Dépendances : IAT ws2_32 : send, recv ; bloc libc-02 memcmp ; phrase .rdata
; Notation explicite générée par outils/auteur.py depuis brouillons/win-10-echange.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 155 o · padding : 229 o (NOP)
; Étiquettes résolues : .envoi=0x4996, .recep=0x49c4, .echec=0x4a0b, .fin=0x4a0d
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x4999 + 0x7 - 0x22b8 = 0x26e8
;   0x49ac + 0x6 - 0x2682 = 0x2330
;   0x49d8 + 0x6 - 0x26b6 = 0x2328
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x40
mov rbx, rcx
mov r12, rdx
xor r13d, r13d
mov rcx, rbx
lea rdx, [rip - 0x22b8]
add rdx, r13
mov r8d, 14
sub r8d, r13d
call qword ptr [rip - 0x2682]
cmp rax, 0
jle 0x4a0b
add r13, rax
cmp r13, 14
jb 0x4996
xor r13d, r13d
mov rcx, rbx
lea rdx, [rsp + 0x20]
add rdx, r13
mov r8d, 14
sub r8d, r13d
call qword ptr [rip - 0x26b6]
cmp rax, 0
jle 0x4a0b
add r13, rax
cmp r13, 14
jb 0x49c4
lea rcx, [rsp + 0x20]
mov rdx, r12
mov r8d, 14
call 0x1180
test eax, eax
jne 0x4a0b
mov eax, 1
jmp 0x4a0d
xor eax, eax
add rsp, 0x40
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
