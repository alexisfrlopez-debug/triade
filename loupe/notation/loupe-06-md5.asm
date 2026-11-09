; loupe-06-md5 · bloc md5 d'une gamme : l'empreinte du quotidien, notée neuve (RFC 1321) · spec loupe-06:R1 · bloc carte i110006
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x45c0, taille 896 octets
; Domaine : loupe (M10, le TGN « Loupe ») · Dépendances : LA NOUVELLE NOTATION (aucun héritage : MD5 n'existe pas au projet) ; les tables MD5_S/MD5_T PUBLIQUES .rdata lues PAR DÉPLACEMENT RIP (I2 — la source unique vit au plan) ; libc-01 (le couplage du tampon PAR LA CARTE) et libc-07 (les zéros du bourre PAR LA CARTE) ; IAT kernel32 : SetFilePointerEx, ReadFile, GetLastError ; le cœur .comprimer : FEUILLE PURE en sous-routine locale, les QUATRE rounds nommés (RFC 1321 § 3.4)
; Notation explicite générée par outils/auteur.py depuis brouillons/loupe-06-md5.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 871 o · padding : 25 o (NOP, 0x90)
; Étiquettes résolues : .boucle=0x4639, .fenetre_taille=0x4650, .absorbe=0x46b2, .k_ok=0x46e3, .fenetre_fin=0x4763, .bourre=0x476e, .zeros56=0x47b2, .comprimer=0x4810, .tour=0x4838, .r1=0x4867, .r2=0x487c, .r3=0x4897, .pas=0x48a9, .refus_session=0x48f4, .refus_bornes=0x48fb, .refus_sortie=0x4902, .refus_systeme=0x4909, .sortie=0x4916
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x45d0 + 0x7 + 0x9a29 = 0xe000
;   0x4660 + 0x6 - 0x223e = 0x2428
;   0x4686 + 0x7 + 0xb973 = 0x10000
;   0x4690 + 0x6 - 0x2266 = 0x2430
;   0x46fb + 0x7 + 0xb8fe = 0x10000
;   0x482e + 0x7 - 0x2735 = 0x2100
;   0x4909 + 0x6 - 0x24c7 = 0x2448
; Appels directs (l'adresse du plan — I1) : call qword ptr [rip - 0x223e], call qword ptr [rip - 0x2266], call 0x1100, call 0x4810, call 0x13c0, call 0x4810, call 0x13c0, call 0x4810, call qword ptr [rip - 0x24c7]
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0xc0
lea rbx, [rip + 0x9a29]
cmp qword ptr [rbx + 528], -1
je 0x48f4
mov rax, rcx
add rax, rdx
jc 0x48fb
cmp rax, qword ptr [rbx + 520]
ja 0x48fb
test r8, r8
jz 0x4902
mov r12, rcx
mov r13, rdx
mov r14, r8
mov dword ptr [rsp + 0x40], 0x67452301
mov dword ptr [rsp + 0x44], 0xefcdab89
mov dword ptr [rsp + 0x48], 0x98badcfe
mov dword ptr [rsp + 0x4c], 0x10325476
mov qword ptr [rsp + 0x50], 0
test r13, r13
jz 0x476e
mov r15d, 0x10000
cmp r13, r15
jae 0x4650
mov r15, r13
mov rcx, qword ptr [rbx + 528]
mov rdx, r12
xor r8d, r8d
xor r9d, r9d
call qword ptr [rip - 0x223e]
test eax, eax
jz 0x4909
lea r9, [rsp + 0xA0]
mov qword ptr [rsp + 0x20], 0
mov rcx, qword ptr [rbx + 528]
lea rdx, [rip + 0xb973]
mov r8, r15
call qword ptr [rip - 0x2266]
test eax, eax
jz 0x4909
mov r15, qword ptr [rsp + 0xA0]
mov qword ptr [rsp + 0xA8], 0
mov rax, qword ptr [rsp + 0xA8]
cmp rax, r15
jae 0x4763
mov rdx, 64
mov rcx, qword ptr [rsp + 0x50]
and ecx, 63
sub rdx, rcx
mov r8, r15
sub r8, rax
cmp r8, rdx
jbe 0x46e3
mov r8, rdx
mov qword ptr [rsp + 0xB0], r8
lea rcx, [rsp + 0x58]
mov rax, qword ptr [rsp + 0x50]
and eax, 63
add rcx, rax
lea rdx, [rip + 0xb8fe]
mov rax, qword ptr [rsp + 0xA8]
add rdx, rax
mov r8, qword ptr [rsp + 0xB0]
call 0x1100
mov rax, qword ptr [rsp + 0xB0]
add qword ptr [rsp + 0x50], rax
mov rax, qword ptr [rsp + 0xA8]
add rax, qword ptr [rsp + 0xB0]
mov qword ptr [rsp + 0xA8], rax
mov rax, qword ptr [rsp + 0x50]
test eax, 63
jnz 0x46b2
lea rcx, [rsp + 0x40]
lea rdx, [rsp + 0x58]
call 0x4810
jmp 0x46b2
add r12, r15
sub r13, r15
jmp 0x4639
mov rax, qword ptr [rsp + 0x50]
and eax, 63
mov r13d, eax
mov byte ptr [rsp + r13 + 0x58], 0x80
inc r13d
cmp r13d, 56
jbe 0x47b2
lea rcx, [rsp + 0x58]
add rcx, r13
xor edx, edx
mov r8d, 64
sub r8d, r13d
call 0x13c0
lea rcx, [rsp + 0x40]
lea rdx, [rsp + 0x58]
call 0x4810
xor r13d, r13d
lea rcx, [rsp + 0x58]
add rcx, r13
xor edx, edx
mov r8d, 56
sub r8d, r13d
call 0x13c0
mov rax, qword ptr [rsp + 0x50]
shl rax, 3
mov qword ptr [rsp + 0x90], rax
lea rcx, [rsp + 0x40]
lea rdx, [rsp + 0x58]
call 0x4810
mov eax, dword ptr [rsp + 0x40]
mov dword ptr [r14], eax
mov eax, dword ptr [rsp + 0x44]
mov dword ptr [r14 + 4], eax
mov eax, dword ptr [rsp + 0x48]
mov dword ptr [r14 + 8], eax
mov eax, dword ptr [rsp + 0x4c]
mov dword ptr [r14 + 12], eax
xor eax, eax
jmp 0x4916
push rbx
push r12
push r13
push r14
push r15
mov rbx, rcx
mov r15, rdx
mov r8d, dword ptr [rbx]
mov r9d, dword ptr [rbx + 4]
mov r10d, dword ptr [rbx + 8]
mov r11d, dword ptr [rbx + 12]
lea r14, [rip - 0x2735]
xor r12d, r12d
cmp r12d, 16
jb 0x4867
cmp r12d, 32
jb 0x487c
cmp r12d, 48
jb 0x4897
mov eax, r10d
mov ecx, r11d
not ecx
or ecx, r9d
xor eax, ecx
mov r13d, r12d
shl r13d, 3
sub r13d, r12d
and r13d, 15
jmp 0x48a9
mov eax, r9d
and eax, r10d
mov ecx, r9d
not ecx
and ecx, r11d
or eax, ecx
mov r13d, r12d
jmp 0x48a9
mov eax, r11d
and eax, r9d
mov ecx, r11d
not ecx
and ecx, r10d
or eax, ecx
lea r13d, [r12 + r12*4 + 1]
and r13d, 15
jmp 0x48a9
mov eax, r9d
xor eax, r10d
xor eax, r11d
lea r13d, [r12 + r12*2 + 5]
and r13d, 15
add eax, r8d
mov edx, dword ptr [r14 + r12*4 + 0x100]
add eax, edx
mov edx, dword ptr [r15 + r13*4]
add eax, edx
mov ecx, dword ptr [r14 + r12*4]
rol eax, cl
mov r8d, r11d
mov r11d, r10d
mov r10d, r9d
add r9d, eax
inc r12d
cmp r12d, 64
jb 0x4838
add dword ptr [rbx], r8d
add dword ptr [rbx + 4], r9d
add dword ptr [rbx + 8], r10d
add dword ptr [rbx + 12], r11d
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
mov eax, -4
jmp 0x4916
mov eax, -3
jmp 0x4916
mov eax, -5
jmp 0x4916
call qword ptr [rip - 0x24c7]
mov eax, -6
jmp 0x4916
add rsp, 0xc0
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
