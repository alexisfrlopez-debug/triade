; loupe-08-ligne · bloc la ligne : 77 o exacts — le décalage, les 16 groupes, le miroir · spec loupe-08:R1 · bloc carte i110008
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x49c0, taille 320 octets
; Domaine : loupe (M10, le TGN « Loupe ») · Dépendances : AUCUNE entrée IAT (la feuille pure — le miroir exact des feuilles tls13, charte § 9) ; la table hexa « 0123456789ABCDEF » du plan (I4 — R_HEX .rdata, lue par déplacement RIP)
; Notation explicite générée par outils/auteur.py depuis brouillons/loupe-08-ligne.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 260 o · padding : 60 o (NOP, 0x90)
; Étiquettes résolues : .writedec_loop=0x49f6, .writ_hex_loop=0x4a21, .write_group_space=0x4a48, .after_group_write=0x4a4e, .write_single_space=0x4a6d, .next_hex_group=0x4a74, .write_hex_done=0x4a76, .writ_ascii_loop=0x4a83, .write_dot=0x4a9a, .after_ascii_write=0x4a9e, .write_ascii_space=0x4aa3, .next_ascii_char=0x4aac, .erreur_entree=0x4abc
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x49e9 + 0x7 - 0x29a0 = 0x2050
test rcx, rcx
jz 0x4abc
test r8, r8
jz 0x4abc
cmp rdx, 1
jl 0x4abc
cmp rdx, 16
jg 0x4abc
mov r10, r9
lea r11, [rip - 0x29a1]
mov r9d, 8
mov rax, r10
shr rax, 28
and rax, 0xF
mov al, [r11 + rax]
mov [r8], al
inc r8
shl r10, 4
dec r9d
jnz 0x49f6
mov word ptr [r8], 0x2020
add r8, 2
xor r9d, r9d
cmp r9d, edx
jae 0x4a48
movzx eax, byte ptr [rcx + r9]
mov r10d, eax
shr eax, 4
and r10d, 0xF
movzx eax, byte ptr [r11 + rax]
movzx r10d, byte ptr [r11 + r10]
mov [r8], al
mov [r8 + 1], r10b
jmp 0x4a4e
mov word ptr [r8], 0x2020
add r8, 2
inc r9d
cmp r9d, 16
jae 0x4a76
cmp r9d, 8
jne 0x4a6d
mov word ptr [r8], 0x2020
add r8, 2
jmp 0x4a74
mov byte ptr [r8], 0x20
inc r8
jmp 0x4a21
mov word ptr [r8], 0x2020
add r8, 2
xor r9d, r9d
cmp r9d, edx
jae 0x4aa3
movzx eax, byte ptr [rcx + r9]
cmp al, 0x20
jl 0x4a9a
cmp al, 0x7E
jg 0x4a9a
mov [r8], al
jmp 0x4a9e
mov byte ptr [r8], 0x2E
inc r9d
jmp 0x4aac
mov byte ptr [r8], 0x20
inc r9d
jmp 0x4aac
inc r8
cmp r9d, 16
jb 0x4a83
mov byte ptr [r8], 0
xor eax, eax
ret
mov rax, -5
ret
