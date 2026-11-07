; loupe-12-aller · bloc l'aller : la barre-saisie hexa, le saut exact, le refus nommé · spec loupe-12:R1 · bloc carte i110012
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x5400, taille 832 octets
; Domaine : loupe (M10, le TGN « Loupe ») · Dépendances : IAT user32 : InvalidateRect (le repaint demandé — le peintre est loupe-10) ; loupe-02 (la fenêtre relue au saut) ; loupe-14 (le commit CHERCHER délégué — le mode partagé, RENVOI) ; la zone SAISIE du plan (mode/actif/nibble/tampon) ; la règle de recadrage du plan (Q3 — recadre, la règle EXÉCUTABLE) ; le refus NOMMÉ monte à la barre (mode MESSAGE)
; Notation explicite générée par outils/auteur.py depuis brouillons/loupe-12-aller.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 796 o · padding : 36 o (NOP, 0x90)
; Étiquettes résolues : .touche=0x5432, .caract=0x5441, .longueur=0x5487, .longueur_fin=0x5497, .chiffre_maj=0x54ad, .chiffre_hex=0x54cd, .borne_chercher=0x54e3, .borne_mode=0x54e9, .corrige=0x5501, .echappe=0x5515, .acquitter=0x5527, .ouvrir=0x5539, .ouvrir_session=0x5559, .commit=0x557d, .commit_scan=0x55a0, .commit_chiffre=0x55cc, .commit_accumule=0x55cf, .commit_scan_fin=0x55de, .commit_recadre=0x5618, .recadre_pos=0x5626, .recadre_vmax_zero=0x5643, .recadre_vmax_fin=0x5645, .recadre_fin=0x564d, .commit_visible=0x566c, .commit_mal=0x568e, .commit_hors=0x56a1, .commit_echec=0x56b4, .commit_chercher=0x56c9, .rien=0x56e1, .sortie=0x56e3, .message=0x56f3, .message_copie=0x56fe, .message_fin=0x570e
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x5412 + 0x7 + 0x8be7 = 0xe000
;   0x544b + 0x7 + 0x8fae = 0xe400
;   0x5479 + 0x7 + 0x8f80 = 0xe400
;   0x54cd + 0x7 + 0x8f2c = 0xe400
;   0x5515 + 0x7 + 0x8ee4 = 0xe400
;   0x5527 + 0x7 + 0x8ed2 = 0xe400
;   0x5543 + 0x7 - 0x31af = 0x239b
;   0x5559 + 0x7 + 0x8ea0 = 0xe400
;   0x557d + 0x7 + 0x8e7c = 0xe400
;   0x558f + 0x7 + 0x8e6a = 0xe400
;   0x566c + 0x7 + 0x8d8d = 0xe400
;   0x5684 + 0x6 - 0x31f2 = 0x2498
;   0x568e + 0x7 - 0x3318 = 0x237d
;   0x56a1 + 0x7 - 0x3319 = 0x238f
;   0x56b7 + 0x7 + 0x8d42 = 0xe400
;   0x56f3 + 0x7 + 0x8d06 = 0xe400
;   0x570e + 0x7 + 0x8ceb = 0xe400
; Appels directs (l'adresse du plan — I1) : call 0x56f3, call 0x4240, call qword ptr [rip - 0x31f2], call 0x56f3, call 0x56f3, call 0x5800
push rbx
push rdi
push rsi
push r12
push r13
push r14
push r15
sub rsp, 0x30
mov r12, rcx
lea rbx, [rip + 0x8be7]
cmp rdx, 0x100
je 0x5432
cmp rdx, 0x102
je 0x5441
xor eax, eax
jmp 0x56e3
cmp r8d, 0x74
jne 0x56e1
jmp 0x5539
cmp r8d, 0x07
je 0x5539
lea rax, [rip + 0x8fae]
mov eax, dword ptr [rax]
test eax, eax
jz 0x56e1
cmp eax, 3
je 0x5527
cmp r8d, 0x0d
je 0x557d
cmp r8d, 0x1b
je 0x5515
lea r14, [rip + 0x8f80]
add r14, 12
xor r13d, r13d
cmp byte ptr [r14 + r13], 0
je 0x5497
inc r13d
cmp r13d, 79
jb 0x5487
cmp r8d, 0x08
je 0x5501
mov eax, r8d
cmp eax, 0x61
jb 0x54ad
cmp eax, 0x66
ja 0x54ad
sub eax, 0x20
cmp eax, 0x30
jb 0x56e1
cmp eax, 0x39
jbe 0x54cd
cmp eax, 0x41
jb 0x56e1
cmp eax, 0x46
ja 0x56e1
lea rdx, [rip + 0x8f2c]
mov edx, dword ptr [rdx]
cmp edx, 1
jne 0x54e3
mov r15d, 8
jmp 0x54e9
mov r15d, 64
cmp r13d, r15d
jae 0x56e1
mov byte ptr [r14 + r13], al
mov byte ptr [r14 + r13 + 1], 0
jmp 0x56e1
test r13d, r13d
jz 0x56e1
mov byte ptr [r14 + r13 - 1], 0
jmp 0x56e1
lea rax, [rip + 0x8ee4]
mov dword ptr [rax], 0
jmp 0x56e1
lea rax, [rip + 0x8ed2]
mov dword ptr [rax], 0
jmp 0x56e1
cmp qword ptr [rbx + 528], -1
jne 0x5559
lea rsi, [rip - 0x31af]
call 0x56f3
mov eax, -4
jmp 0x56e3
lea rax, [rip + 0x8ea0]
mov dword ptr [rax], 1
mov dword ptr [rax + 4], 0
mov dword ptr [rax + 8], 0
mov byte ptr [rax + 12], 0
jmp 0x56e1
lea rax, [rip + 0x8e7c]
mov eax, dword ptr [rax]
cmp eax, 2
je 0x56c9
lea rsi, [rip + 0x8e6a]
add rsi, 12
xor r10d, r10d
xor r11d, r11d
movzx eax, byte ptr [rsi]
test eax, eax
jz 0x55de
cmp eax, 0x30
jb 0x568e
cmp eax, 0x39
jbe 0x55cc
cmp eax, 0x41
jb 0x568e
cmp eax, 0x46
ja 0x568e
sub eax, 0x37
jmp 0x55cf
sub eax, 0x30
shl r10, 4
add r10, rax
inc r11d
inc rsi
jmp 0x55a0
test r11d, r11d
jz 0x568e
cmp r10, qword ptr [rbx + 520]
jae 0x56a1
mov qword ptr [rbx + 544], r10
mov rax, qword ptr [rbx + 536]
mov rcx, rax
mov edx, dword ptr [rbx + 552]
add rcx, rdx
cmp r10, rax
jb 0x5618
cmp r10, rcx
jb 0x566c
mov rcx, r10
sub rcx, 176
jns 0x5626
xor ecx, ecx
and rcx, -16
mov rax, qword ptr [rbx + 520]
sub rax, 384
jbe 0x5643
add rax, 15
and rax, -16
jmp 0x5645
xor eax, eax
cmp rcx, rax
jbe 0x564d
mov rcx, rax
cmp rcx, qword ptr [rbx + 536]
je 0x566c
mov r15, rcx
mov rcx, r15
call 0x4240
test eax, eax
jnz 0x56b4
mov qword ptr [rbx + 536], r15
lea rax, [rip + 0x8d8d]
mov dword ptr [rax], 0
mov rcx, r12
xor edx, edx
mov r8d, 1
call qword ptr [rip - 0x31f2]
xor eax, eax
jmp 0x56e3
lea rsi, [rip - 0x3318]
call 0x56f3
mov eax, -5
jmp 0x56e3
lea rsi, [rip - 0x3319]
call 0x56f3
mov eax, -3
jmp 0x56e3
mov r10d, eax
lea rax, [rip + 0x8d42]
mov dword ptr [rax], 0
mov eax, r10d
jmp 0x56e3
mov rcx, r12
mov edx, 0x102
mov r8d, 0x0d
xor r9d, r9d
call 0x5800
jmp 0x56e3
xor eax, eax
add rsp, 0x30
pop r15
pop r14
pop r13
pop r12
pop rsi
pop rdi
pop rbx
ret
lea rdi, [rip + 0x8d06]
add rdi, 12
mov al, byte ptr [rsi]
mov byte ptr [rdi], al
test al, al
jz 0x570e
inc rsi
inc rdi
jmp 0x56fe
lea rax, [rip + 0x8ceb]
mov dword ptr [rax], 3
ret
