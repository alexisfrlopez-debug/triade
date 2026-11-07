; loupe-03-fermer · bloc fermer : jamais une poignée pendante (idempotent) · spec loupe-03:R1 · bloc carte i110003
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x4380, taille 192 octets
; Domaine : loupe (M10, le TGN « Loupe ») · Dépendances : IAT kernel32 : CloseHandle, GetLastError ; loupe-04 (le cadre re-vierge), libc-07 (l'hygiène des empreintes) ; idempotent par construction, jamais une poignée pendante
; Notation explicite générée par outils/auteur.py depuis brouillons/loupe-03-fermer.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 122 o · padding : 70 o (NOP, 0x90)
; Étiquettes résolues : .propre=0x43ad, .deja=0x43f2
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x4385 + 0x7 + 0x9c74 = 0xe000
;   0x439d + 0x6 - 0x1f63 = 0x2440
;   0x43a7 + 0x6 - 0x1f65 = 0x2448
;   0x43b2 + 0x7 + 0xa0e7 = 0xe4a0
;   0x43c3 + 0x7 + 0xa096 = 0xe460
;   0x43d1 + 0x7 + 0xa028 = 0xe400
;   0x43de + 0x7 + 0x9fdb = 0xe3c0
; Appels directs (l'adresse du plan — I1) : call qword ptr [rip - 0x1f63], call qword ptr [rip - 0x1f65], call 0x4040, call 0x13c0
push rbx
sub rsp, 0x20
lea rbx, [rip + 0x9c74]
cmp qword ptr [rbx + 528], -1
je 0x43f2
mov rcx, qword ptr [rbx + 528]
call qword ptr [rip - 0x1f63]
test eax, eax
jnz 0x43ad
call qword ptr [rip - 0x1f65]
call 0x4040
lea rax, [rip + 0xa0e7]
mov dword ptr [rax + 4096], 0
lea rax, [rip + 0xa096]
mov dword ptr [rax + 32], 0
lea rax, [rip + 0xa028]
mov dword ptr [rax], 0
lea rcx, [rip + 0x9fdb]
xor edx, edx
mov r8d, 48
call 0x13c0
xor eax, eax
add rsp, 0x20
pop rbx
ret
