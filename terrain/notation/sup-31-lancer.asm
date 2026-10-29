; sup-31-lancer · bloc terrain · spec sup-31:R1 · bloc carte f60031
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x5200, taille 448 octets
; Dépendances : IAT kernel32#3 : CreateProcessA, CreatePipe ; IAT kernel32#1/#2 : CloseHandle, GetModuleFileNameA ; état .data ETAT_SUP (HPROC, PID, TUYAU_*)
; Notation explicite générée par outils/auteur.py depuis brouillons/sup-31-lancer.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 428 o · padding : 20 o (NOP)
; Étiquettes résolues : .balaye=0x523e, .sans_rep=0x5255, .rep_ok=0x5258, .pas_tuyaux=0x52ca, .si_ok=0x52f4, .fin_ok=0x534c, .echec_cp=0x5353, .echec_sec=0x535d, .ferme_premier=0x5361, .ferme_un=0x5376, .ferme_tuyaux=0x538a, .ferme_boucle=0x538d, .fin=0x539b
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x5231 + 0x6 - 0x23b7 = 0x2e80
;   0x5284 + 0x7 - 0x176b = 0x3b20
;   0x5297 + 0x6 - 0x2f95 = 0x2308
;   0x52a5 + 0x7 - 0x178c = 0x3b20
;   0x52bc + 0x6 - 0x2fba = 0x2308
;   0x52da + 0x7 - 0x17c1 = 0x3b20
;   0x52e5 + 0x7 - 0x17b4 = 0x3b38
;   0x5318 + 0x6 - 0x301e = 0x2300
;   0x5325 + 0x7 - 0x181c = 0x3b10
;   0x5330 + 0x6 - 0x323e = 0x20f8
;   0x5377 + 0x7 - 0x185e = 0x3b20
;   0x5382 + 0x6 - 0x3290 = 0x20f8
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x200
mov rbx, rcx
mov r12d, edx
lea r15, [rsp + 0xD0]
lea r13, [rsp + 0xE8]
xor ecx, ecx
mov rdx, r13
mov r8d, 280
call qword ptr [rip - 0x23b7]
test eax, eax
je 0x5255
mov rcx, rax
test rcx, rcx
je 0x5255
dec rcx
cmp byte ptr [rcx + r13], 0x5C
jne 0x523e
mov byte ptr [rcx + r13 + 1], 0
jmp 0x5258
xor r13d, r13d
xor eax, eax
lea rdi, [rsp + 0x20]
mov ecx, 24
rep stosq qword ptr [rdi], rax
mov dword ptr [rsp + 0x50], 24
mov dword ptr [rsp + 0x60], 1
mov dword ptr [rsp + 0x68], 0x68
test r12d, r12d
je 0x52ca
lea rcx, [rip - 0x176b]
lea rdx, [rcx + 8]
lea r8, [rsp + 0x50]
xor r9d, r9d
call qword ptr [rip - 0x2f95]
test eax, eax
je 0x535d
lea rcx, [rip - 0x178c]
lea rcx, [rcx + 16]
lea rdx, [rcx + 8]
lea r8, [rsp + 0x50]
xor r9d, r9d
call qword ptr [rip - 0x2fba]
test eax, eax
je 0x5361
test r12d, r12d
je 0x52f4
or dword ptr [rsp + 0xA4], 0x100
mov rax, qword ptr [rip - 0x17c1]
mov qword ptr [r15 - 0x18], rax
mov rax, qword ptr [rip - 0x17b4]
mov qword ptr [r15 - 0x10], rax
mov qword ptr [r15 - 0x8], rax
xor ecx, ecx
mov rdx, rbx
xor r8d, r8d
xor r9d, r9d
mov dword ptr [rsp + 0x20], r12d
mov qword ptr [rsp + 0x38], r13
lea rax, [rsp + 0x68]
mov qword ptr [rsp + 0x40], rax
mov qword ptr [rsp + 0x48], r15
call qword ptr [rip - 0x301e]
test eax, eax
je 0x5353
mov rax, qword ptr [r15]
mov qword ptr [rip - 0x181c], rax
mov rcx, qword ptr [r15 + 16]
call qword ptr [rip - 0x323e]
test r12d, r12d
je 0x534c
xor eax, eax
call 0x5376
mov eax, 3
call 0x5376
mov eax, 1
jmp 0x539b
test r12d, r12d
je 0x535d
call 0x538a
xor eax, eax
jmp 0x539b
xor eax, eax
call 0x5376
mov eax, 1
call 0x5376
xor eax, eax
jmp 0x539b
push rcx
lea rcx, [rip - 0x185e]
lea rcx, [rcx + rax*8]
call qword ptr [rip - 0x3290]
pop rcx
ret
push rcx
xor eax, eax
call 0x5376
inc eax
cmp eax, 4
jb 0x538d
pop rcx
ret
add rsp, 0x200
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
