; http-08-cible-r2 · bloc cible (forme) — révision https · spec http-08:R2 · bloc carte g70009
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x7340, taille 384 octets
; Dépendances : RÉVISION (ancêtre e50008 http-08:R1 scellé 0.4.0, cité § 9) : schéma https:// BYTE-EXACT 8 octets minuscules, verdict TLS distinct, port 443 ; fixture SLASH
; Notation explicite générée par outils/auteur.py depuis brouillons/http-08-cible-r2.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 326 o · padding : 58 o (NOP)
; Étiquettes résolues : .test_https=0x737c, .absolu_scan=0x73a2, .absolu_boucle=0x73a5, .absolu_delim=0x73c0, .absolu_defaut=0x73c8, .absolu_zone=0x73d5, .pas_absolu=0x73f2, .pas_origine=0x7409, .sch_boucle=0x740b, .sch_deux_points=0x741c, .refuse=0x7439, .autorite=0x743f, .ecrit=0x7451, .ecrit_tls=0x7467, .autorite_vide=0x7480
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x73c8 + 0x7 - 0x4eff = 0x24d0
cmp r8d, 8
je 0x743f
cmp rdx, 7
jb 0x73f2
cmp dword ptr [rcx], 0x70747468
jne 0x73f2
cmp word ptr [rcx + 4], 0x2F3A
jne 0x737c
cmp byte ptr [rcx + 6], 0x2F
jne 0x73f2
lea r10, [rcx + rdx]
lea rdx, [rcx + 7]
jmp 0x73a2
cmp rdx, 8
jb 0x73f2
cmp byte ptr [rcx + 4], 0x73
jne 0x73f2
cmp byte ptr [rcx + 5], 0x3A
jne 0x73f2
cmp byte ptr [rcx + 6], 0x2F
jne 0x73f2
cmp byte ptr [rcx + 7], 0x2F
jne 0x73f2
lea r10, [rcx + rdx]
lea rdx, [rcx + 8]
mov rax, rdx
cmp rax, r10
jae 0x73c8
movzx r11d, byte ptr [rax]
cmp r11, 0x2F
je 0x73c0
cmp r11, 0x3F
je 0x73c8
add rax, 1
jmp 0x73a5
mov r8, rax
sub r10, rax
jmp 0x73d5
lea r8, [rip - 0x4eff]
mov r10d, 1
sub rax, rdx
test rax, rax
je 0x7480
lea r11, [rcx + 8]
cmp rdx, r11
mov r11d, 1
je 0x7467
jmp 0x7451
cmp byte ptr [rcx], 0x2F
jne 0x7409
mov r11d, 2
mov r8, rcx
mov r10, rdx
xor edx, edx
xor eax, eax
jmp 0x7451
xor eax, eax
cmp rax, rdx
jae 0x7439
cmp byte ptr [rcx + rax], 0x3A
je 0x741c
add rax, 1
jmp 0x740b
lea r10, [rax + 2]
cmp r10, rdx
jae 0x7439
cmp byte ptr [rcx + rax + 1], 0x2F
jne 0x7439
cmp byte ptr [rcx + rax + 2], 0x2F
jne 0x7439
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
