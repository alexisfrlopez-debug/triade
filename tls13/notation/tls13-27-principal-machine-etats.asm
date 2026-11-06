; tls13-27-principal-machine-etats · bloc la machine d'états du client (l'orchestration, § 2) · spec tls13-27:R1 · bloc carte h100027
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0xff40, taille 2944 octets
; Domaine : tls13 (M9, l'ère 1.0.0) · Dépendances : LE PRINCIPAL — l'orchestration sur le contexte session 17 520 o (la disposition DÉCLARÉE par la spec P1) ; LES COMPOSITIONS DÉCLARÉES (I1, LA LISTE FERMÉE) : tls13-14, tls13-22, tls13-23, tls13-24 (×3 étages), tls13-25 (×2 modes), tls13-26, tls13-20 (×2), tls13-21 (×2), tls13-03 (le transcript — chaque message ABSORBÉ AVANT traitement, charte § 4), tls13-04 (les coupes du hash sur la COPIE — I2), LE SOCLE tls13-28 pour TOUTE entrée/sortie ; QUATRE événements NOMMÉS (OUVRIR/ÉMETTRE/RECEVOIR/FERMER), tout événement hors de sa ligne → -3 ; LA DISCIPLINE D'ÉCHEC (Q2) : tout verdict négatif PROPAGÉ NOMMÉ, l'état passe à 5 (MORT), AUCUN octet applicatif après ; le réassemblage au tampon @ +1136 (la borne 2^14 NOMMÉE), le Certificate Verify ABSORBÉ sans vérification (le chantier futur nommé), l'extraction de la PREMIÈRE entrée du Certificate (le u24 lu) le DÉTROIT de tls13-26
; Notation explicite générée par outils/auteur.py depuis brouillons/tls13-27-principal-machine-etats.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 2906 o · padding : 38 o (NOP, 0x90)
; Étiquettes résolues : .ouvrir_ligne=0xff72, .sh_tete=0x100f3, .sh_tete_fin=0x1013c, .sh_corps=0x1016a, .sh_corps_fin=0x101b2, .protege=0x10306, .pr_tete=0x10318, .pr_tete_fin=0x10361, .pr_corps=0x103a5, .pr_corps_fin=0x103ed, .marche=0x10447, .absorbe=0x104e6, .cert=0x1052b, .fin_serveur=0x10593, .marche_avance=0x10741, .emettre_ligne=0x10754, .recevoir_ligne=0x107ea, .rc_tete=0x1082e, .rc_tete_fin=0x10874, .rc_corps=0x1089d, .rc_corps_fin=0x108e2, .rc_restituer=0x1092d, .rc_alerte=0x1093e, .rc_alerte_morte=0x1096c, .fermer_ligne=0x10989, .fermer_ok=0x109a0, .mort=0x10a36, .refus_etat_mort=0x10a4e, .refus_taille_mort=0x10a55, .refus_pre_etat=0x10a5c, .refus_pre_nul=0x10a6e, .refus_pre_taille=0x10a80, .refus_contexte_nul=0x10a92
; Appels directs (l'adresse scellée du plan — I1) : call 0xc000, call 0xf060, call 0xdc80, call 0xed00, call 0xc240, call 0x10a80, call 0x10a80, call 0x10a80, call 0xee20, call 0xc240, call 0xc300, call 0xf060, call 0x10a80, call 0x10a80, call 0xeb40, call 0xc300, call 0xc240, call 0xf9e0, call 0xf8e0, call 0xc300, call 0xf060, call 0xf8e0, call 0xc240, call 0xe9c0, call 0x10a80, call 0xe9c0, call 0x10a80, call 0x10a80, call 0x10a80, call 0xeb40, call 0xe9c0, call 0x10a80
test rcx, rcx
jz 0x10a92
cmp rdx, 1
je 0xff72
cmp rdx, 2
je 0x10754
cmp rdx, 3
je 0x107ea
cmp rdx, 4
je 0x10989
jmp 0x10a5c
cmp dword ptr [rcx + 1120], 0
jne 0x10a5c
test r8, r8
jz 0x10a6e
test r9, r9
jz 0x10a6e
sub rsp, 0x43c8
mov qword ptr [rsp + 0x28], rcx
mov qword ptr [rsp + 0x38], r9
mov qword ptr [rcx + 1128], r8
mov rcx, qword ptr [rsp + 0x28]
call 0xc000
test eax, eax
jnz 0x10a36
lea r10, [r9 + 32]
lea r11, [rcx + 160]
mov rax, qword ptr [r10]
mov qword ptr [r11], rax
mov rax, qword ptr [r10 + 8]
mov qword ptr [r11 + 8], rax
mov rax, qword ptr [r10 + 16]
mov qword ptr [r11 + 16], rax
mov rax, qword ptr [r10 + 24]
mov qword ptr [r11 + 24], rax
lea r10, [r9 + 64]
lea r11, [rcx + 1088]
mov rax, qword ptr [r10]
mov qword ptr [r11], rax
mov rax, qword ptr [r10 + 8]
mov qword ptr [r11 + 8], rax
mov rax, qword ptr [r10 + 16]
mov qword ptr [r11 + 16], rax
mov rax, qword ptr [r10 + 24]
mov qword ptr [r11 + 24], rax
mov rcx, qword ptr [rsp + 0x28]
add rcx, 112
xor edx, edx
xor r8d, r8d
call 0xf060
test eax, eax
jnz 0x10a36
mov rcx, qword ptr [rsp + 0x28]
add rcx, 192
mov rdx, qword ptr [rsp + 0x38]
add rdx, 32
call 0xdc80
test eax, eax
jnz 0x10a36
mov rcx, qword ptr [rsp + 0x38]
mov rdx, qword ptr [rsp + 0x28]
add rdx, 192
lea r8, [rsp + 0x80]
add r8, 5
mov r9d, 114
call 0xed00
test eax, eax
jnz 0x10a36
lea r10, [rsp + 0x80]
mov dword ptr [r10], 0x30316
mov byte ptr [r10 + 4], 0x76
mov rcx, qword ptr [rsp + 0x28]
lea rdx, [rsp + 0x85]
mov r8d, 114
call 0xc240
test eax, eax
jnz 0x10a36
mov rcx, qword ptr [rsp + 0x28]
mov rcx, qword ptr [rcx + 1128]
mov edx, 1
lea r8, [rsp + 0x80]
mov r9d, 119
call 0x10a80
test eax, eax
jnz 0x10a36
mov r10, qword ptr [rsp + 0x28]
mov dword ptr [r10 + 1120], 1
mov qword ptr [rsp + 0x40], 0
mov rax, qword ptr [rsp + 0x40]
cmp rax, 5
jae 0x1013c
mov rcx, qword ptr [rsp + 0x28]
mov rcx, qword ptr [rcx + 1128]
mov edx, 2
lea r8, [rsp + 0x80]
add r8, qword ptr [rsp + 0x40]
mov r9, 5
sub r9, qword ptr [rsp + 0x40]
call 0x10a80
test eax, eax
jle 0x10a36
add qword ptr [rsp + 0x40], rax
jmp 0x100f3
lea r10, [rsp + 0x80]
cmp byte ptr [r10], 22
jne 0x10a4e
movzx eax, word ptr [r10 + 3]
xchg al, ah
cmp rax, 16400
ja 0x10a55
lea rax, [rax + 5]
mov qword ptr [rsp + 0x58], rax
mov rax, qword ptr [rsp + 0x40]
cmp rax, qword ptr [rsp + 0x58]
jae 0x101b2
mov rcx, qword ptr [rsp + 0x28]
mov rcx, qword ptr [rcx + 1128]
mov edx, 2
lea r8, [rsp + 0x80]
add r8, qword ptr [rsp + 0x40]
mov r9, qword ptr [rsp + 0x58]
sub r9, qword ptr [rsp + 0x40]
call 0x10a80
test eax, eax
jle 0x10a36
add qword ptr [rsp + 0x40], rax
jmp 0x1016a
mov r8, qword ptr [rsp + 0x28]
add r8, 160
lea rcx, [rsp + 0x80]
add rcx, 5
mov rdx, qword ptr [rsp + 0x58]
sub rdx, 5
lea r9, [rsp + 0x40a0]
call 0xee20
test eax, eax
jnz 0x10a36
mov rcx, qword ptr [rsp + 0x28]
lea rdx, [rsp + 0x85]
mov r8, qword ptr [rsp + 0x58]
sub r8, 5
call 0xc240
test eax, eax
jnz 0x10a36
mov rsi, qword ptr [rsp + 0x28]
lea rdi, [rsp + 0x42b0]
mov ecx, 14
cld
rep movsq
lea rcx, [rsp + 0x42b0]
lea rdx, [rsp + 0x40a0]
add rdx, 32
call 0xc300
test eax, eax
jnz 0x10a36
mov rcx, qword ptr [rsp + 0x28]
add rcx, 112
lea rdx, [rsp + 0x40a0]
lea r8, [rsp + 0x40e0]
call 0xf060
test eax, eax
jnz 0x10a36
lea rsi, [rsp + 0x40e0]
mov rdi, qword ptr [rsp + 0x28]
add rdi, 224
mov ecx, 25
rep movsq
lea rsi, [rsp + 0x40e0]
add rsi, 200
mov rdi, qword ptr [rsp + 0x28]
add rdi, 424
mov ecx, 25
rep movsq
lea rsi, [rsp + 0x40e0]
add rsi, 400
mov rdi, qword ptr [rsp + 0x28]
add rdi, 1024
mov ecx, 4
rep movsq
lea rsi, [rsp + 0x40e0]
add rsi, 432
mov rdi, qword ptr [rsp + 0x28]
add rdi, 1056
mov ecx, 4
rep movsq
mov r10, qword ptr [rsp + 0x28]
mov dword ptr [r10 + 1120], 2
mov qword ptr [rsp + 0x48], 0
mov qword ptr [rsp + 0x40], 0
mov qword ptr [rsp + 0x50], 0
mov rax, qword ptr [rsp + 0x40]
cmp rax, 5
jae 0x10361
mov rcx, qword ptr [rsp + 0x28]
mov rcx, qword ptr [rcx + 1128]
mov edx, 2
lea r8, [rsp + 0x80]
add r8, qword ptr [rsp + 0x40]
mov r9, 5
sub r9, qword ptr [rsp + 0x40]
call 0x10a80
test eax, eax
jle 0x10a36
add qword ptr [rsp + 0x40], rax
jmp 0x10318
lea r10, [rsp + 0x80]
cmp byte ptr [r10], 23
jne 0x10a4e
movzx eax, word ptr [r10 + 3]
xchg al, ah
cmp rax, 16400
ja 0x10a55
lea r11, [rax - 17]
add r11, qword ptr [rsp + 0x48]
cmp r11, 16384
ja 0x10a55
lea rax, [rax + 5]
mov qword ptr [rsp + 0x58], rax
mov rax, qword ptr [rsp + 0x40]
cmp rax, qword ptr [rsp + 0x58]
jae 0x103ed
mov rcx, qword ptr [rsp + 0x28]
mov rcx, qword ptr [rcx + 1128]
mov edx, 2
lea r8, [rsp + 0x80]
add r8, qword ptr [rsp + 0x40]
mov r9, qword ptr [rsp + 0x58]
sub r9, qword ptr [rsp + 0x40]
call 0x10a80
test eax, eax
jle 0x10a36
add qword ptr [rsp + 0x40], rax
jmp 0x103a5
mov rcx, qword ptr [rsp + 0x28]
add rcx, 424
lea rdx, [rsp + 0x80]
mov r8, qword ptr [rsp + 0x58]
mov r9, qword ptr [rsp + 0x28]
add r9, 1136
add r9, qword ptr [rsp + 0x48]
lea r10, [rsp + 0x60]
mov qword ptr [rsp + 0x20], r10
call 0xeb40
test eax, eax
jnz 0x10a36
cmp byte ptr [rsp + 0x60], 22
jne 0x10a4e
mov rax, qword ptr [rsp + 0x58]
sub rax, 22
add qword ptr [rsp + 0x48], rax
mov rax, qword ptr [rsp + 0x48]
sub rax, qword ptr [rsp + 0x50]
cmp rax, 4
jb 0x10306
mov r10, qword ptr [rsp + 0x28]
add r10, 1136
add r10, qword ptr [rsp + 0x50]
movzx eax, byte ptr [r10 + 1]
shl rax, 16
movzx r11d, byte ptr [r10 + 2]
shl r11, 8
or rax, r11
movzx r11d, byte ptr [r10 + 3]
or rax, r11
mov qword ptr [rsp + 0x70], rax
lea r11, [rax + 4]
mov rcx, qword ptr [rsp + 0x48]
sub rcx, qword ptr [rsp + 0x50]
cmp r11, rcx
ja 0x10306
movzx r11d, byte ptr [r10]
mov qword ptr [rsp + 0x68], r11
cmp r11d, 0x14
jne 0x104e6
mov rsi, qword ptr [rsp + 0x28]
lea rdi, [rsp + 0x42b0]
mov ecx, 14
rep movsq
lea rcx, [rsp + 0x42b0]
lea rdx, [rsp + 0x4320]
call 0xc300
test eax, eax
jnz 0x10a36
mov rcx, qword ptr [rsp + 0x28]
mov r10, qword ptr [rsp + 0x28]
add r10, 1136
add r10, qword ptr [rsp + 0x50]
mov rdx, r10
mov r8, qword ptr [rsp + 0x70]
add r8, 4
call 0xc240
test eax, eax
jnz 0x10a36
mov rax, qword ptr [rsp + 0x68]
cmp rax, 0xb
je 0x1052b
cmp rax, 0x14
je 0x10593
jmp 0x10741
mov r10, qword ptr [rsp + 0x28]
add r10, 1136
add r10, qword ptr [rsp + 0x50]
movzx eax, byte ptr [r10 + 8]
shl rax, 16
movzx r11d, byte ptr [r10 + 9]
shl r11, 8
or rax, r11
movzx r11d, byte ptr [r10 + 10]
or rax, r11
mov r11, qword ptr [rsp + 0x70]
sub r11, 7
cmp rax, r11
ja 0x10a55
mov rcx, r10
add rcx, 11
mov rdx, rax
mov r8, qword ptr [rsp + 0x28]
add r8, 1088
call 0xf9e0
test eax, eax
jnz 0x10a36
jmp 0x10741
cmp qword ptr [rsp + 0x70], 32
jne 0x10a55
mov rcx, qword ptr [rsp + 0x28]
add rcx, 1056
lea rdx, [rsp + 0x4320]
mov r8, qword ptr [rsp + 0x28]
add r8, 1136
add r8, qword ptr [rsp + 0x50]
add r8, 4
mov r9d, 1
call 0xf8e0
test eax, eax
jnz 0x10a36
mov rsi, qword ptr [rsp + 0x28]
lea rdi, [rsp + 0x42b0]
mov ecx, 14
rep movsq
lea rcx, [rsp + 0x42b0]
lea rdx, [rsp + 0x4340]
call 0xc300
test eax, eax
jnz 0x10a36
mov rcx, qword ptr [rsp + 0x28]
add rcx, 112
lea rdx, [rsp + 0x4340]
mov r8, qword ptr [rsp + 0x28]
add r8, 624
call 0xf060
test eax, eax
jnz 0x10a36
mov rcx, qword ptr [rsp + 0x28]
add rcx, 1024
lea rdx, [rsp + 0x4340]
lea r8, [rsp + 0x4360]
xor r9d, r9d
call 0xf8e0
test eax, eax
jnz 0x10a36
lea r10, [rsp + 0x4380]
mov dword ptr [r10], 0x20000014
mov rax, qword ptr [rsp + 0x4360]
mov qword ptr [r10 + 4], rax
mov rax, qword ptr [rsp + 0x4368]
mov qword ptr [r10 + 12], rax
mov rax, qword ptr [rsp + 0x4370]
mov qword ptr [r10 + 20], rax
mov rax, qword ptr [rsp + 0x4378]
mov qword ptr [r10 + 28], rax
mov rcx, qword ptr [rsp + 0x28]
lea rdx, [rsp + 0x4380]
mov r8d, 36
call 0xc240
test eax, eax
jnz 0x10a36
mov rcx, qword ptr [rsp + 0x28]
add rcx, 224
mov edx, 22
lea r8, [rsp + 0x4380]
mov r9d, 36
lea r10, [rsp + 0x80]
mov qword ptr [rsp + 0x20], r10
call 0xe9c0
test eax, eax
jnz 0x10a36
mov rcx, qword ptr [rsp + 0x28]
mov rcx, qword ptr [rcx + 1128]
mov edx, 1
lea r8, [rsp + 0x80]
mov r9d, 58
call 0x10a80
test eax, eax
jnz 0x10a36
mov r10, qword ptr [rsp + 0x28]
mov dword ptr [r10 + 1120], 3
xor eax, eax
add rsp, 0x43c8
ret
mov rax, qword ptr [rsp + 0x70]
add rax, 4
add qword ptr [rsp + 0x50], rax
jmp 0x10447
cmp dword ptr [rcx + 1120], 3
jne 0x10a5c
sub rsp, 0x43c8
mov qword ptr [rsp + 0x28], rcx
mov qword ptr [rsp + 0x38], r9
mov qword ptr [rsp + 0x78], r8
mov qword ptr [rsp + 0x40], r9
mov rcx, qword ptr [rsp + 0x28]
add rcx, 624
mov edx, 23
mov r8, qword ptr [rsp + 0x78]
mov r9, qword ptr [rsp + 0x40]
lea r10, [rsp + 0x80]
mov qword ptr [rsp + 0x20], r10
call 0xe9c0
test eax, eax
jnz 0x10a36
mov rcx, qword ptr [rsp + 0x28]
mov rcx, qword ptr [rcx + 1128]
mov edx, 1
lea r8, [rsp + 0x80]
mov r9, qword ptr [rsp + 0x40]
add r9, 22
call 0x10a80
test eax, eax
jnz 0x10a36
xor eax, eax
add rsp, 0x43c8
ret
cmp dword ptr [rcx + 1120], 3
jne 0x10a5c
test r8, r8
jz 0x10a6e
cmp r9, 5
jb 0x10a80
sub rsp, 0x43c8
mov qword ptr [rsp + 0x28], rcx
mov qword ptr [rsp + 0x38], r9
mov qword ptr [rsp + 0x78], r8
mov qword ptr [rsp + 0x40], r9
mov qword ptr [rsp + 0x48], 0
mov rax, qword ptr [rsp + 0x48]
cmp rax, 5
jae 0x10874
mov rcx, qword ptr [rsp + 0x28]
mov rcx, qword ptr [rcx + 1128]
mov edx, 2
mov r8, qword ptr [rsp + 0x78]
add r8, qword ptr [rsp + 0x48]
mov r9, 5
sub r9, qword ptr [rsp + 0x48]
call 0x10a80
test eax, eax
jle 0x10a36
add qword ptr [rsp + 0x48], rax
jmp 0x1082e
mov r10, qword ptr [rsp + 0x78]
movzx eax, word ptr [r10 + 3]
xchg al, ah
lea rax, [rax + 5]
cmp rax, qword ptr [rsp + 0x40]
ja 0x10a55
mov qword ptr [rsp + 0x58], rax
mov qword ptr [rsp + 0x40], 5
mov rax, qword ptr [rsp + 0x40]
cmp rax, qword ptr [rsp + 0x58]
jae 0x108e2
mov rcx, qword ptr [rsp + 0x28]
mov rcx, qword ptr [rcx + 1128]
mov edx, 2
mov r8, qword ptr [rsp + 0x78]
add r8, qword ptr [rsp + 0x40]
mov r9, qword ptr [rsp + 0x58]
sub r9, qword ptr [rsp + 0x40]
call 0x10a80
test eax, eax
jle 0x10a36
add qword ptr [rsp + 0x40], rax
jmp 0x1089d
mov rcx, qword ptr [rsp + 0x28]
add rcx, 824
mov rdx, qword ptr [rsp + 0x78]
mov r8, qword ptr [rsp + 0x58]
mov r9, qword ptr [rsp + 0x78]
lea r10, [rsp + 0x60]
mov qword ptr [rsp + 0x20], r10
call 0xeb40
test eax, eax
jnz 0x10a36
movzx eax, byte ptr [rsp + 0x60]
cmp eax, 21
je 0x1093e
cmp eax, 22
je 0x1092d
cmp eax, 23
je 0x1092d
jmp 0x10a4e
mov rax, qword ptr [rsp + 0x58]
sub rax, 22
add rsp, 0x43c8
ret
cmp qword ptr [rsp + 0x58], 24
jne 0x1096c
mov r10, qword ptr [rsp + 0x78]
cmp word ptr [r10], 1
jne 0x1096c
mov r10, qword ptr [rsp + 0x28]
mov dword ptr [r10 + 1120], 4
xor eax, eax
add rsp, 0x43c8
ret
mov r10, qword ptr [rsp + 0x28]
mov dword ptr [r10 + 1120], 5
mov eax, -3
add rsp, 0x43c8
ret
cmp dword ptr [rcx + 1120], 3
je 0x109a0
cmp dword ptr [rcx + 1120], 4
je 0x109a0
jmp 0x10a5c
sub rsp, 0x43c8
mov qword ptr [rsp + 0x28], rcx
mov qword ptr [rsp + 0x38], r9
lea r10, [rsp + 0x4380]
mov word ptr [r10], 1
mov rcx, qword ptr [rsp + 0x28]
add rcx, 624
mov edx, 21
lea r8, [rsp + 0x4380]
mov r9d, 2
lea r10, [rsp + 0x80]
mov qword ptr [rsp + 0x20], r10
call 0xe9c0
test eax, eax
jnz 0x10a36
mov rcx, qword ptr [rsp + 0x28]
mov rcx, qword ptr [rcx + 1128]
mov edx, 1
lea r8, [rsp + 0x80]
mov r9d, 24
call 0x10a80
test eax, eax
jnz 0x10a36
mov r10, qword ptr [rsp + 0x28]
mov dword ptr [r10 + 1120], 4
xor eax, eax
add rsp, 0x43c8
ret
mov r10, qword ptr [rsp + 0x28]
mov dword ptr [r10 + 1120], 5
add rsp, 0x43c8
ret
mov eax, -3
jmp 0x10a36
mov eax, -2
jmp 0x10a36
mov dword ptr [rcx + 1120], 5
mov rax, -3
ret
mov dword ptr [rcx + 1120], 5
mov rax, -1
ret
mov dword ptr [rcx + 1120], 5
mov rax, -2
ret
mov rax, -1
ret
