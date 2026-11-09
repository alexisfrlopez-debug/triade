; loupe-11-defilement · bloc le défilement : borné à la fin réelle (la dernière fenêtre voit) · spec loupe-11:R1 · bloc carte i110011
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x5180, taille 640 octets
; Domaine : loupe (M10, le TGN « Loupe ») · Dépendances : IAT user32 : GetScrollInfo, SetScrollInfo, InvalidateRect ; IAT kernel32 : GetLastError (E1 le refus nommé) ; loupe-02 (la fenêtre relue — le recouvrement du journal y vit) ; le pas et la borne de la spec (vue_max : LA DERNIÈRE fenêtre voit le dernier octet) ; l'alignement 16 inviolable (I1) ; jamais une lecture hors fichier (I2 : le clamp PRÉCÈDE la lecture)
; Notation explicite générée par outils/auteur.py depuis brouillons/loupe-11-defilement.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 568 o · padding : 72 o (NOP, 0x90)
; Étiquettes résolues : .vmax_zero=0x51c1, .vmax_fin=0x51c3, .taille=0x51e9, .taille_zero=0x5203, .taille_pose=0x5205, .vscroll=0x5214, .pas_ligne_haut=0x5241, .pas_ligne_bas=0x5249, .pas_page_haut=0x5251, .pas_page_bas=0x5259, .poignee=0x5261, .pas_applique=0x52bd, .borne=0x52c7, .borne_haut=0x52d0, .borne_fin=0x52d8, .ascenseur_remis=0x52ff, .molette=0x5372, .rien=0x5397, .sans_session=0x539b, .refus_gsi=0x539f, .sortie=0x53aa
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x5190 + 0x7 + 0x8e69 = 0xe000
;   0x51ef + 0x7 + 0xabfa = 0xfdf0
;   0x5205 + 0x7 + 0xabe4 = 0xfdf0
;   0x52a3 + 0x6 - 0x2e01 = 0x24a8
;   0x5321 + 0x7 + 0xaac8 = 0xfdf0
;   0x5357 + 0x6 - 0x2ead = 0x24b0
;   0x5368 + 0x6 - 0x2ed6 = 0x2498
;   0x539f + 0x6 - 0x2f5d = 0x2448
; Appels directs (l'adresse du plan — I1) : call qword ptr [rip - 0x2e01], call 0x4240, call qword ptr [rip - 0x2ead], call qword ptr [rip - 0x2ed6], call qword ptr [rip - 0x2f5d]
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x40
mov r14, rcx
lea rbx, [rip + 0x8e69]
cmp qword ptr [rbx + 528], -1
je 0x539b
mov r15, rdx
mov rax, qword ptr [rbx + 520]
sub rax, 384
jbe 0x51c1
add rax, 15
and rax, -16
jmp 0x51c3
xor eax, eax
mov r13, rax
cmp r15, 5
je 0x51e9
cmp r15, 0x115
je 0x5214
cmp r15, 0x20a
je 0x5372
xor eax, eax
jmp 0x53aa
mov eax, r9d
shr eax, 16
lea rdx, [rip + 0xabfa]
mov ecx, dword ptr [rdx + 4]
test ecx, ecx
jz 0x5203
xor edx, edx
div ecx
jmp 0x5205
xor eax, eax
lea rdx, [rip + 0xabe4]
mov dword ptr [rdx + 8], eax
jmp 0x52ff
mov eax, r8d
and eax, 0xffff
cmp eax, 0
je 0x5241
cmp eax, 1
je 0x5249
cmp eax, 2
je 0x5251
cmp eax, 3
je 0x5259
cmp eax, 4
je 0x5261
cmp eax, 5
je 0x5261
xor eax, eax
jmp 0x53aa
mov r12d, -16
jmp 0x52bd
mov r12d, 16
jmp 0x52bd
mov r12d, -352
jmp 0x52bd
mov r12d, 352
jmp 0x52bd
mov dword ptr [rsp], 28
mov dword ptr [rsp + 4], 0x10
mov dword ptr [rsp + 8], 0
mov dword ptr [rsp + 12], 0
mov dword ptr [rsp + 16], 0
mov dword ptr [rsp + 20], 0
mov dword ptr [rsp + 24], 0
mov rcx, r14
mov edx, 1
mov r8, rsp
call qword ptr [rip - 0x2e01]
test eax, eax
jz 0x539f
mov eax, dword ptr [rsp + 24]
shl eax, 4
mov r12, rax
jmp 0x52c7
movsxd r12, r12d
add r12, qword ptr [rbx + 536]
cmp r12, 0
jge 0x52d0
xor r12d, r12d
cmp r12, r13
jbe 0x52d8
mov r12, r13
mov rax, qword ptr [rbx + 536]
cmp r12, rax
je 0x5397
mov rcx, r12
call 0x4240
test eax, eax
jnz 0x53aa
mov qword ptr [rbx + 536], r12
mov dword ptr [rsp], 28
mov dword ptr [rsp + 4], 7
mov dword ptr [rsp + 8], 0
mov rax, r13
shr rax, 4
mov dword ptr [rsp + 12], eax
lea rax, [rip + 0xaac8]
mov eax, dword ptr [rax + 8]
mov dword ptr [rsp + 16], eax
mov rax, qword ptr [rbx + 536]
shr rax, 4
mov dword ptr [rsp + 20], eax
mov dword ptr [rsp + 24], 0
mov rcx, r14
mov edx, 1
mov r8, rsp
mov r9d, 1
call qword ptr [rip - 0x2ead]
mov rcx, r14
xor edx, edx
mov r8d, 1
call qword ptr [rip - 0x2ed6]
xor eax, eax
jmp 0x53aa
mov eax, r8d
shr eax, 16
movsx eax, ax
mov ecx, 120
cdq
idiv ecx
imul eax, eax, 48
neg eax
movsxd r12, eax
add r12, qword ptr [rbx + 536]
jmp 0x52c7
xor eax, eax
jmp 0x53aa
xor eax, eax
jmp 0x53aa
call qword ptr [rip - 0x2f5d]
mov eax, -6
add rsp, 0x40
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
