; loupe-01-ouvrir · bloc ouvrir : le fichier donné à la session (la session née entière) · spec loupe-01:R1 · bloc carte i110001
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x4080, taille 448 octets
; Domaine : loupe (M10, le TGN « Loupe ») · Dépendances : IAT kernel32 : CreateFileW, GetFileSizeEx, CloseHandle, GetLastError ; libc-01 (la copie du chemin PAR LA CARTE) ; loupe-04 (le cadre vierge en tête), loupe-02 (la fenêtre à la vue 0), loupe-03 (la clôture sur refus), loupe-07 (le panneau né) — la session née ENTIÈRE (Q4)
; Notation explicite générée par outils/auteur.py depuis brouillons/loupe-01-ouvrir.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 388 o · padding : 60 o (NOP, 0x90)
; Étiquettes résolues : .taille_ok=0x412b, .mesure=0x4135, .mesure_fin=0x4166, .panneau=0x418b, .propage=0x419f, .refus_session=0x41ac, .refus_os=0x41b3, .absent=0x41cf, .verrouille=0x41d6, .refus_taille_os=0x41dd, .sortie=0x41f6
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x408d + 0x7 + 0x9f6c = 0xe000
;   0x40d3 + 0x6 - 0x1cc1 = 0x2418
;   0x40f2 + 0x6 - 0x1cd8 = 0x2420
;   0x4116 + 0x6 - 0x1cdc = 0x2440
;   0x4151 + 0x6 - 0x1d17 = 0x2440
;   0x418b + 0x7 + 0xa22e = 0xe3c0
;   0x41b3 + 0x6 - 0x1d71 = 0x2448
;   0x41e4 + 0x6 - 0x1daa = 0x2440
; Appels directs (l'adresse du plan — I1) : call 0x4040, call qword ptr [rip - 0x1cc1], call qword ptr [rip - 0x1cd8], call qword ptr [rip - 0x1cdc], call 0x4040, call qword ptr [rip - 0x1d17], call 0x4040, call 0x1100, call 0x4240, call 0x4940, call 0x4380, call qword ptr [rip - 0x1d71], call qword ptr [rip - 0x1daa], call 0x4040
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x40
lea rbx, [rip + 0x9f6c]
cmp qword ptr [rbx + 528], -1
jne 0x41ac
mov r12, rcx
call 0x4040
mov rcx, r12
mov edx, 0xc0000000
mov r8d, 1
xor r9d, r9d
mov dword ptr [rsp], 3
mov dword ptr [rsp + 8], 0
mov qword ptr [rsp + 0x10], 0
call qword ptr [rip - 0x1cc1]
cmp rax, -1
je 0x41b3
mov qword ptr [rbx + 528], rax
mov rcx, rax
lea rdx, [rsp + 0x20]
call qword ptr [rip - 0x1cd8]
test eax, eax
jz 0x41dd
mov r13, qword ptr [rsp + 0x20]
mov eax, 0x80000000
cmp r13, rax
jbe 0x412b
mov rcx, qword ptr [rbx + 528]
call qword ptr [rip - 0x1cdc]
call 0x4040
mov eax, -3
jmp 0x41f6
mov qword ptr [rbx + 520], r13
xor r14d, r14d
movzx eax, word ptr [r12 + r14*2]
test eax, eax
jz 0x4166
inc r14d
cmp r14d, 260
jb 0x4135
mov rcx, qword ptr [rbx + 528]
call qword ptr [rip - 0x1d17]
call 0x4040
mov eax, -5
jmp 0x41f6
mov rcx, rbx
mov rdx, r12
mov r8d, r14d
shl r8d, 1
add r8d, 2
call 0x1100
test r13, r13
jz 0x418b
xor ecx, ecx
call 0x4240
test eax, eax
js 0x419f
lea rcx, [rip + 0xa22e]
call 0x4940
test eax, eax
js 0x419f
xor eax, eax
jmp 0x41f6
mov r13d, eax
call 0x4380
mov eax, r13d
jmp 0x41f6
mov eax, -5
jmp 0x41f6
call qword ptr [rip - 0x1d71]
cmp eax, 2
je 0x41cf
cmp eax, 3
je 0x41cf
cmp eax, 32
je 0x41d6
mov eax, -6
jmp 0x41f6
mov eax, -2
jmp 0x41f6
mov eax, -7
jmp 0x41f6
mov rcx, qword ptr [rbx + 528]
call qword ptr [rip - 0x1daa]
call 0x4040
mov eax, -6
jmp 0x41f6
add rsp, 0x40
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
