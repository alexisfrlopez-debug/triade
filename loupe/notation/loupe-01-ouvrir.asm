; loupe-01-ouvrir · bloc ouvrir : le fichier donné à la session (la session née entière) · spec loupe-01:R1 · bloc carte i110001
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x4080, taille 448 octets
; Domaine : loupe (M10, le TGN « Loupe ») · Dépendances : IAT kernel32 : CreateFileW, GetFileSizeEx, CloseHandle, GetLastError ; libc-01 (la copie du chemin PAR LA CARTE) ; loupe-04 (le cadre vierge en tête), loupe-02 (la fenêtre à la vue 0), loupe-03 (la clôture sur refus), loupe-07 (le panneau né) — la session née ENTIÈRE (Q4)
; Notation explicite générée par outils/auteur.py depuis brouillons/loupe-01-ouvrir.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 389 o · padding : 59 o (NOP, 0x90)
; Étiquettes résolues : .taille_ok=0x412c, .mesure=0x4136, .mesure_fin=0x4167, .panneau=0x418c, .propage=0x41a0, .refus_session=0x41ad, .refus_os=0x41b4, .absent=0x41d0, .verrouille=0x41d7, .refus_taille_os=0x41de, .sortie=0x41f7
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x408d + 0x7 + 0x9f6c = 0xe000
;   0x40d4 + 0x6 - 0xfc2 = 0x3118
;   0x40f3 + 0x6 - 0xfd9 = 0x3120
;   0x4117 + 0x6 - 0xfdd = 0x3140
;   0x4152 + 0x6 - 0x1018 = 0x3140
;   0x418c + 0x7 + 0xa22d = 0xe3c0
;   0x41b4 + 0x6 - 0x1072 = 0x3148
;   0x41e5 + 0x6 - 0x10ab = 0x3140
; Appels directs (l'adresse du plan — I1) : call 0x4040, call qword ptr [rip - 0xfc2], call qword ptr [rip - 0xfd9], call qword ptr [rip - 0xfdd], call 0x4040, call qword ptr [rip - 0x1018], call 0x4040, call 0x1100, call 0x4240, call 0x4940, call 0x4380, call qword ptr [rip - 0x1072], call qword ptr [rip - 0x10ab], call 0x4040
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x40
lea rbx, [rip + 0x9f6c]
cmp qword ptr [rbx + 528], -1
jne 0x41ad
mov r12, rcx
call 0x4040
mov rcx, r12
mov edx, 0xc0000000
mov r8d, 1
xor r9d, r9d
mov dword ptr [rsp + 0x20], 3
mov dword ptr [rsp + 0x28], 0
mov qword ptr [rsp + 0x30], 0
call qword ptr [rip - 0xfc2]
cmp rax, -1
je 0x41b4
mov qword ptr [rbx + 528], rax
mov rcx, rax
lea rdx, [rsp + 0x20]
call qword ptr [rip - 0xfd9]
test eax, eax
jz 0x41de
mov r13, qword ptr [rsp + 0x20]
mov eax, 0x80000000
cmp r13, rax
jbe 0x412c
mov rcx, qword ptr [rbx + 528]
call qword ptr [rip - 0xfdd]
call 0x4040
push -3
pop rax
nop
nop
jmp 0x41f7
mov qword ptr [rbx + 520], r13
xor r14d, r14d
movzx eax, word ptr [r12 + r14*2]
test eax, eax
jz 0x4167
inc r14d
cmp r14d, 260
jb 0x4136
mov rcx, qword ptr [rbx + 528]
call qword ptr [rip - 0x1018]
call 0x4040
push -5
pop rax
nop
nop
jmp 0x41f7
mov rcx, rbx
mov rdx, r12
mov r8d, r14d
shl r8d, 1
add r8d, 2
call 0x1100
test r13, r13
jz 0x418c
xor ecx, ecx
call 0x4240
test eax, eax
js 0x41a0
lea rcx, [rip + 0xa22d]
call 0x4940
test eax, eax
js 0x41a0
xor eax, eax
jmp 0x41f7
movsxd r13, eax
call 0x4380
movsxd rax, r13d
jmp 0x41f7
push -5
pop rax
nop
nop
jmp 0x41f7
call qword ptr [rip - 0x1072]
cmp eax, 2
je 0x41d0
cmp eax, 3
je 0x41d0
cmp eax, 32
je 0x41d7
push -6
pop rax
nop
nop
jmp 0x41f7
push -2
pop rax
nop
nop
jmp 0x41f7
push -7
pop rax
nop
nop
jmp 0x41f7
mov rcx, qword ptr [rbx + 528]
call qword ptr [rip - 0x10ab]
call 0x4040
push -6
pop rax
nop
nop
jmp 0x41f7
add rsp, 0x40
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
