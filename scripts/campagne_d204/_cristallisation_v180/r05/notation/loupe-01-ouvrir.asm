; loupe-01-ouvrir · bloc ouvrir : le fichier donné à la session (la session née entière) · spec loupe-01:R3 · bloc carte i110001
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x4080, taille 448 octets
; Domaine : loupe (M10, le TGN « Loupe ») · Dépendances : IAT kernel32 : CreateFileW, GetFileSizeEx, CloseHandle, GetLastError ; libc-01 (la copie du chemin PAR LA CARTE) ; loupe-04 (le cadre vierge en tête), loupe-02 (la fenêtre à la vue 0), loupe-03 (la clôture sur refus), loupe-07 (le panneau né) — la session née ENTIÈRE (Q4)
; Notation explicite générée par outils/auteur.py depuis brouillons/loupe-01-ouvrir.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 403 o · padding : 45 o (NOP, 0x90)
; Étiquettes résolues : .loop_mesure=0x4125, .copie_chemin=0x4157, .naissance_panneau=0x4180, .erreur_os_create=0x4195, .verdict_absent=0x41b1, .verdict_verrouille=0x41b8, .hors_perimetre=0x41bf, .appel_echoue=0x41d8, .verdict_deja_ouvert=0x41e5, .erreur_os_size=0x41ec, .sortie=0x4205
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x408d + 0x7 + 0x9f6c = 0xe000
;   0x40d9 + 0x6 - 0xfc7 = 0x3118
;   0x40fe + 0x6 - 0xfe4 = 0x3120
;   0x4142 + 0x6 - 0x1008 = 0x3140
;   0x4180 + 0x7 + 0xa239 = 0xe3c0
;   0x4195 + 0x6 - 0x1053 = 0x3148
;   0x41c6 + 0x6 - 0x108c = 0x3140
;   0x41f3 + 0x6 - 0x10b9 = 0x3140
; Appels directs (l'adresse du plan — I1) : call 0x4040, call qword ptr [rip - 0xfc7], call qword ptr [rip - 0xfe4], call qword ptr [rip - 0x1008], call 0x4040, call 0x1100, call 0x4240, call 0x4940, call qword ptr [rip - 0x1053], call qword ptr [rip - 0x108c], call 0x4040, call 0x4380, call qword ptr [rip - 0x10b9], call 0x4040
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x40
lea rbx, [rip + 0x9f6c]
cmp qword ptr [rbx + 528], -1
jne 0x41e5
mov r12, rcx
call 0x4040
mov rcx, r12
mov r9, 0
mov r8, 1
mov edx, 0xC0000000
mov dword ptr [rsp + 0x20], 3
mov dword ptr [rsp + 0x28], 0
mov qword ptr [rsp + 0x30], 0
call qword ptr [rip - 0xfc7]
cmp rax, -1
je 0x4195
mov [rbx + 528], rax
mov rcx, [rbx + 528]
lea rdx, [rbx + 520]
call qword ptr [rip - 0xfe4]
test rax, rax
jz 0x41ec
mov r13, qword ptr [rbx + 520]
mov eax, 0x80000000
cmp r13, rax
ja 0x41bf
xor r8, r8
movzx eax, word ptr [r12 + r8]
test eax, eax
jz 0x4157
add r8, 2
cmp r8d, 520
jb 0x4125
mov rcx, [rbx + 528]
call qword ptr [rip - 0x1008]
call 0x4040
mov eax, -5
jmp 0x4205
lea rcx, [rbx]
mov rdx, r12
lea r8, [r8 + 2]
call 0x1100
mov rax, [rbx + 520]
test rax, rax
jz 0x4180
mov ecx, 0
call 0x4240
test eax, eax
jne 0x41d8
lea rcx, [rip + 0xa239]
call 0x4940
test eax, eax
jne 0x41d8
xor rax, rax
jmp 0x4205
call qword ptr [rip - 0x1053]
cmp eax, 2
je 0x41b1
cmp eax, 3
je 0x41b1
cmp eax, 32
je 0x41b8
mov eax, -6
jmp 0x4205
mov eax, -2
jmp 0x4205
mov eax, -7
jmp 0x4205
mov rcx, [rbx + 528]
call qword ptr [rip - 0x108c]
call 0x4040
mov eax, -3
jmp 0x4205
movsxd r13, eax
call 0x4380
mov eax, r13d
jmp 0x4205
mov eax, -5
jmp 0x4205
mov rcx, [rbx + 528]
call qword ptr [rip - 0x10b9]
call 0x4040
mov eax, -6
jmp 0x4205
add rsp, 0x40
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
