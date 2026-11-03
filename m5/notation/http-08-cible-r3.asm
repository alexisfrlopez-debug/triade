; http-08-cible-r3 · bloc cible (forme) — révision relèvement (verdict 5) · spec http-08:R3 · bloc carte g80001
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x8000, taille 448 octets
; Dépendances : RÉVISION (ancêtre g70009 http-08:R2 embarqué 0.5.1, cité § 9) : le verdict « cible à relever » (5) SOUS politique armée SEULEMENT — sans politique : R2 octet pour octet
; Notation explicite générée par outils/auteur.py depuis brouillons/http-08-cible-r3.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 377 o · padding : 71 o (NOP)
; Étiquettes résolues : .test_https=0x803c, .absolu_scan=0x8072, .absolu_boucle=0x8075, .absolu_delim=0x8090, .absolu_defaut=0x8098, .absolu_zone=0x80a5, .pas_absolu=0x80e5, .pas_origine=0x80fc, .sch_boucle=0x80fe, .sch_deux_points=0x810f, .refuse=0x812c, .autorite=0x8132, .ecrit=0x8144, .ecrit_tls=0x815a, .autorite_vide=0x8173
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x8098 + 0x7 - 0x5bcf = 0x24d0
cmp r8d, 8
je 0x8132
cmp rdx, 7
jb 0x80e5
cmp dword ptr [rcx], 0x70747468
jne 0x80e5
cmp word ptr [rcx + 4], 0x2F3A
jne 0x803c
cmp byte ptr [rcx + 6], 0x2F
jne 0x80e5
lea r10, [rcx + rdx]
lea rdx, [rcx + 7]
jmp 0x8072
cmp rdx, 8
jb 0x80e5
cmp byte ptr [rcx + 4], 0x73
jne 0x80e5
cmp byte ptr [rcx + 5], 0x3A
jne 0x80e5
cmp byte ptr [rcx + 6], 0x2F
jne 0x80e5
cmp byte ptr [rcx + 7], 0x2F
jne 0x80e5
lea r10, [rcx + rdx]
lea rdx, [rcx + 8]
mov rax, rdx
cmp rax, r10
jae 0x8098
movzx r11d, byte ptr [rax]
cmp r11, 0x2F
je 0x8090
cmp r11, 0x3F
je 0x8098
add rax, 1
jmp 0x8075
mov r8, rax
sub r10, rax
jmp 0x80a5
lea r8, [rip - 0x5bcf]
mov r10d, 1
sub rax, rdx
test rax, rax
je 0x8173
lea r11, [rcx + 8]
cmp rdx, r11
mov r11d, 1
je 0x815a
cmp qword ptr [rsp + 0x30], 0
je 0x8144
mov dword ptr [r9], r11d
mov qword ptr [r9 + 8], rdx
mov qword ptr [r9 + 16], rax
mov qword ptr [r9 + 24], r8
mov qword ptr [r9 + 32], r10
mov eax, 5
ret
cmp byte ptr [rcx], 0x2F
jne 0x80fc
mov r11d, 2
mov r8, rcx
mov r10, rdx
xor edx, edx
xor eax, eax
jmp 0x8144
xor eax, eax
cmp rax, rdx
jae 0x812c
cmp byte ptr [rcx + rax], 0x3A
je 0x810f
add rax, 1
jmp 0x80fe
lea r10, [rax + 2]
cmp r10, rdx
jae 0x812c
cmp byte ptr [rcx + rax + 1], 0x2F
jne 0x812c
cmp byte ptr [rcx + rax + 2], 0x2F
jne 0x812c
mov eax, 3
ret
mov eax, 1
ret
mov r11d, 3
mov rax, rdx
mov rdx, rcx
xor r8d, r8d
xor r10d, r10d
mov dword ptr [r9], r11d
mov qword ptr [r9 + 8], rdx
mov qword ptr [r9 + 16], rax
mov qword ptr [r9 + 24], r8
mov qword ptr [r9 + 32], r10
xor eax, eax
ret
mov dword ptr [r9], r11d
mov qword ptr [r9 + 8], rdx
mov qword ptr [r9 + 16], rax
mov qword ptr [r9 + 24], r8
mov qword ptr [r9 + 32], r10
mov eax, 4
ret
mov eax, 2
ret
