; sys-03-ecriture · bloc écriture directe — la twin de hello-02 par NtWriteFile · spec sys-03:R1 · bloc carte g90003
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0xa180, taille 192 octets
; Dépendances : sys-02 (la résolution au geste même) PUIS sys-01 (l'émission) — l'ordre est le contrat (I3) ; les fixtures .rdata NOM/LIGNE cités par déplacement (I4)
; Notation explicite générée par outils/auteur.py depuis brouillons/sys-03-ecriture.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 164 o · padding : 28 o (NOP)
; Étiquettes résolues : .status_nonnul=0xa1fa, .status_iosb=0xa206, .resolution_echouee=0xa213, .epilogue=0xa21d
; Déplacements RIP (cible = adresse + taille + disp) :
;   0xa18c + 0x7 - 0x72d3 = 0x2ec0
;   0xa1ba + 0x7 - 0x72f1 = 0x2ed0
push rbx
push rbp
sub rsp, 0x58
mov rbx, rdx
mov rbp, rcx
lea rcx, [rip - 0x72d3]
mov edx, 11
mov r8, rbp
call 0xa040
test rax, rax
js 0xa213
mov rcx, rbx
xor edx, edx
xor r8d, r8d
xor r9d, r9d
lea r10, [rsp + 0x48]
mov qword ptr [rsp + 0x20], r10
lea r10, [rip - 0x72f1]
mov qword ptr [rsp + 0x28], r10
mov qword ptr [rsp + 0x30], 33
mov qword ptr [rsp + 0x38], 0
mov qword ptr [rsp + 0x40], 0
call 0xa000
test eax, eax
jne 0xa1fa
cmp dword ptr [rsp + 0x48], 0
jne 0xa206
xor eax, eax
add rsp, 0x58
pop rbp
pop rbx
ret
mov rdx, rax
mov rax, -6
jmp 0xa21d
mov edx, dword ptr [rsp + 0x48]
mov rax, -6
jmp 0xa21d
mov rdx, rax
mov rax, -1
add rsp, 0x58
pop rbp
pop rbx
ret
