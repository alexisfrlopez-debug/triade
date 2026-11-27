; loupe-08-ligne · bloc la ligne : 77 o exacts — le décalage, les 16 groupes, le miroir · spec loupe-08:R1 · bloc carte i110008
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x49c0, taille 320 octets
; Domaine : loupe (M10, le TGN « Loupe ») · Dépendances : AUCUNE entrée IAT (la feuille pure — le miroir exact des feuilles tls13, charte § 9) ; la table hexa « 0123456789ABCDEF » du plan (I4 — R_HEX .rdata, lue par déplacement RIP) ; les bornes P2/P4 vérifiées AVANT la première écriture (I2 : exactement 77 o, jamais un de plus) ; la source LUE SEULE (I3)
; Notation explicite générée par outils/auteur.py depuis brouillons/loupe-08-ligne.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 271 o · padding : 49 o (NOP, 0x90)
; Étiquettes résolues : .dec_boucle=0x4a0c, .rempli_haut=0x4a32, .rempli_miroir=0x4a44, .grp_boucle=0x4a59, .grp_pos=0x4a6b, .grp_suivant=0x4a8c, .miroir_boucle=0x4a98, .miroir_point=0x4aae, .miroir_poser=0x4ab0, .miroir_fin=0x4aba, .refus_entree=0x4abe, .sortie=0x4ac3
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x49fd + 0x7 - 0x29b4 = 0x2050
push rbx
push r12
push r13
push r14
sub rsp, 0x28
test rcx, rcx
jz 0x4abe
test r8, r8
jz 0x4abe
cmp rdx, 1
jb 0x4abe
cmp rdx, 16
ja 0x4abe
mov rbx, rcx
mov r12, rdx
mov r13, r8
mov r14, r9
lea r11, [rip - 0x29b4]
mov edx, 28
xor r10d, r10d
mov rax, r14
mov cl, dl
shr rax, cl
and eax, 0xf
movzx eax, byte ptr [r11 + rax]
mov byte ptr [r13 + r10], al
sub edx, 4
inc r10d
cmp r10d, 8
jb 0x4a0c
mov eax, 8
mov byte ptr [r13 + rax], 0x20
inc eax
cmp eax, 60
jb 0x4a32
mov eax, 60
mov byte ptr [r13 + rax], 0x20
inc eax
cmp eax, 76
jb 0x4a44
mov byte ptr [r13 + 76], 0
xor r10d, r10d
cmp r10d, r12d
jae 0x4a8c
lea eax, [r10 + r10*2 + 10]
cmp r10d, 8
jb 0x4a6b
inc eax
movzx edx, byte ptr [rbx + r10]
mov ecx, edx
shr edx, 4
and ecx, 0xf
movzx edx, byte ptr [r11 + rdx]
mov byte ptr [r13 + rax], dl
movzx edx, byte ptr [r11 + rcx]
mov byte ptr [r13 + rax + 1], dl
inc r10d
cmp r10d, 16
jb 0x4a59
xor r10d, r10d
cmp r10d, r12d
jae 0x4aba
movzx edx, byte ptr [rbx + r10]
cmp dl, 0x20
jb 0x4aae
cmp dl, 0x7e
ja 0x4aae
jmp 0x4ab0
mov dl, 0x2e
mov byte ptr [r13 + r10 + 60], dl
inc r10d
jmp 0x4a98
xor eax, eax
jmp 0x4ac3
mov eax, -5
add rsp, 0x28
pop r14
pop r13
pop r12
pop rbx
ret
