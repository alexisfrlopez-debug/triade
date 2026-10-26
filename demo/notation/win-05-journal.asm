; win-05-journal · bloc démo · spec win-05:R3 · bloc carte d40005
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x5000, taille 512 octets
; Dépendances : IAT user32 : SendMessageW ; blocs libc-03/04 ; bloc win-11 (miroir fichier) ; état .data (HWND_JOURNAL, BUF_MIROIR, BUF_CONV) ; deux entrées : scénario @0x5000 (force mode 2), trace @0x5008 (4 args)
; Notation explicite générée par outils/auteur.py depuis brouillons/win-05-journal.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 267 o · padding : 245 o (NOP)
; Étiquettes résolues : .principal=0x5000, .conv_txt=0x5042, .txt_fait=0x5054, .conv_val=0x5073, .crlf=0x5087, .mode2=0x509c, .envoi=0x509c, .fichier=0x50d7, .scenario=0x5100
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x5023 + 0x7 - 0x15da = 0x3a50
;   0x502a + 0x7 - 0x17c9 = 0x3868
;   0x5060 + 0x7 - 0x17d7 = 0x3890
;   0x506c + 0x7 - 0x17e3 = 0x3890
;   0x509c + 0x7 - 0x183b = 0x3868
;   0x50b6 + 0x6 - 0x287c = 0x2840
;   0x50bc + 0x7 - 0x185b = 0x3868
;   0x50d1 + 0x6 - 0x2897 = 0x2840
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x30
mov rbx, rcx
mov r12, rdx
mov r13d, r8d
mov r14d, r9d
mov qword ptr [rsp + 0x20], rdx
mov qword ptr [rsp + 0x28], rcx
lea r15, [rip - 0x15da]
mov rax, qword ptr [rip - 0x17c9]
test rax, rax
je 0x50d7
cmp r13d, 2
je 0x509c
xor ecx, ecx
cmp rcx, r12
jae 0x5054
movzx edx, byte ptr [rbx + rcx]
mov word ptr [r15 + rcx*2], dx
inc ecx
jmp 0x5042
mov r12, rcx
cmp r13d, 1
jne 0x5087
mov ecx, r14d
lea rdx, [rip - 0x17d7]
call 0x1280
lea rdx, [rip - 0x17e3]
movzx eax, byte ptr [rdx]
test eax, eax
je 0x5087
mov word ptr [r15 + r12*2], ax
inc rdx
inc r12
jmp 0x5073
mov dword ptr [r15 + r12*2], 0xA000D
mov word ptr [r15 + r12*2 + 4], 0
mov rbx, r15
jmp 0x509c
mov rcx, qword ptr [rip - 0x183b]
mov edx, 0xB1
mov r8, 0xFFFFFFFFFFFFFFFF
mov r9, 0xFFFFFFFFFFFFFFFF
call qword ptr [rip - 0x287c]
mov rcx, qword ptr [rip - 0x185b]
mov edx, 0xC2
mov r8d, 1
mov r9, rbx
call qword ptr [rip - 0x2897]
mov rcx, qword ptr [rsp + 0x28]
mov rdx, qword ptr [rsp + 0x20]
mov r8d, r13d
mov r9d, r14d
add rsp, 0x30
pop r15
pop r14
pop r13
pop r12
pop rbx
jmp 0x1e00
nop
nop
nop
nop
nop
nop
nop
mov r8d, 2
jmp 0x5000
