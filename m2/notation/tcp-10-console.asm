; tcp-10-console · bloc thread console · spec tcp-10:R1 · bloc carte c30010
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x4980, taille 384 octets
; Dépendances : IAT kernel32 : ReadFile ; blocs libc-02, tcp-07, tcp-05, tcp-11 ; état .data (stdin, listen, quit) ; chaînes .rdata
; Notation explicite générée par outils/auteur.py depuis brouillons/tcp-10-console.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 312 o · padding : 72 o (NOP)
; Étiquettes résolues : .boucle=0x498d, .refus=0x49fa, .journal_statique=0x4a06, .pas_patch=0x4a22, .pas_rollback=0x4a5f, .inconnue=0x4a99, .sortie=0x4aaa
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x498d + 0x7 - 0x118c = 0x3808
;   0x49ad + 0x6 - 0x28c3 = 0x20f0
;   0x49cb + 0x7 - 0x22a2 = 0x2730
;   0x49ec + 0x7 - 0x2383 = 0x2670
;   0x49fa + 0x7 - 0x233d = 0x26c4
;   0x4a2d + 0x7 - 0x22fc = 0x2738
;   0x4a51 + 0x7 - 0x23c8 = 0x2690
;   0x4a6a + 0x7 - 0x232f = 0x2742
;   0x4a80 + 0xb - 0x1273 = 0x3818
;   0x4a8b + 0x7 - 0x1282 = 0x3810
;   0x4a99 + 0x7 - 0x23f0 = 0x26b0
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x70
mov rcx, qword ptr [rip - 0x118c]
lea rdx, [rsp + 0x30]
mov r8d, 64
lea r9, [rsp + 0x28]
mov qword ptr [rsp + 0x20], 0
call qword ptr [rip - 0x28c3]
test eax, eax
je 0x4aaa
mov r12, qword ptr [rsp + 0x28]
cmp r12, 7
jne 0x4a22
lea rcx, [rsp + 0x30]
lea rdx, [rip - 0x22a2]
mov r8d, 7
call 0x1180
test eax, eax
jne 0x4a22
xor ecx, ecx
call 0x4400
test eax, eax
jne 0x49fa
lea rcx, [rip - 0x2383]
mov edx, 28
jmp 0x4a06
lea rcx, [rip - 0x233d]
mov edx, 17
mov r8d, 0xFFFFFFFF
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call 0x4b00
jmp 0x498d
cmp r12, 9
jne 0x4a5f
lea rcx, [rsp + 0x30]
lea rdx, [rip - 0x22fc]
mov r8d, 9
call 0x1180
test eax, eax
jne 0x4a5f
mov ecx, 1
call 0x4400
test eax, eax
jne 0x49fa
lea rcx, [rip - 0x23c8]
mov edx, 26
jmp 0x4a06
cmp r12, 6
jne 0x4a99
lea rcx, [rsp + 0x30]
lea rdx, [rip - 0x232f]
mov r8d, 6
call 0x1180
test eax, eax
jne 0x4a99
mov qword ptr [rip - 0x1273], 1
mov rcx, qword ptr [rip - 0x1282]
call 0x41c0
jmp 0x4aaa
lea rcx, [rip - 0x23f0]
mov edx, 19
jmp 0x4a06
add rsp, 0x70
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
