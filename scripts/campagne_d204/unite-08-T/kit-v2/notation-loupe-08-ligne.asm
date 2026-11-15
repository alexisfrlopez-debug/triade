; loupe-08-ligne · bloc la ligne : 77 o exacts — le décalage, les 16 groupes, le miroir · spec loupe-08:R1 · bloc carte i110008
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x49c0, taille 320 octets
; Domaine : loupe (M10, le TGN « Loupe ») · Dépendances : AUCUNE entrée IAT (la feuille pure — le miroir exact des feuilles tls13, charte § 9) ; la table hexa « 0123456789ABCDEF » du plan (I4 — R_HEX .rdata, lue par déplacement RIP) ; les bornes P2/P4 vérifiées AVANT la première écriture (I2 : exactement 77 o, jamais un de plus) ; la source LUE SEULE (I3)
; Notation explicite générée par outils/auteur.py depuis brouillons/loupe-08-ligne.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 296 o · padding : 24 o (NOP, 0x90)
; Étiquettes résolues : .chiffre=0x4a05, .squelette=0x4a34, .groupe_bas=0x4a4d, .fin_bas=0x4a74, .groupe_haut=0x4a87, .fin_haut=0x4aae, .miroir=0x4aba, .poser=0x4ad0, .miroir_fin=0x4ada, .sortie=0x4adc, .refus=0x4ae2
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x49f4 + 0x7 - 0x29ab = 0x2050
test rcx, rcx
jz 0x4ae2
test r8, r8
jz 0x4ae2
cmp rdx, 1
jb 0x4ae2
cmp rdx, 16
ja 0x4ae2
push rbx
push r12
push r13
mov rbx, rcx
mov r12, rdx
mov r13, r8
lea r11, [rip - 0x29ab]
mov eax, r9d
rol rax, 36
xor r10d, r10d
mov edx, eax
and edx, 0xf
movzx edx, byte ptr [r11 + rdx]
mov byte ptr [r13 + r10], dl
rol rax, 4
inc r10d
cmp r10d, 8
jb 0x4a05
movabs rax, 0x2020202020202020
lea r9, [r13 + 8]
mov ecx, 8
mov qword ptr [r9], rax
add r9, 8
loop 0x4a34
mov dword ptr [r13 + 72], eax
mov byte ptr [r13 + 76], 0
lea r9, [r13 + 10]
xor r10d, r10d
cmp r10d, r12d
jae 0x4a74
movzx eax, byte ptr [rbx + r10]
mov edx, eax
shr edx, 4
and eax, 0xf
movzx edx, byte ptr [r11 + rdx]
mov byte ptr [r9], dl
movzx edx, byte ptr [r11 + rax]
mov byte ptr [r9 + 1], dl
add r9, 3
inc r10d
cmp r10d, 8
jb 0x4a4d
lea r9, [r13 + 35]
mov r10d, 8
cmp r10d, r12d
jae 0x4aae
movzx eax, byte ptr [rbx + r10]
mov edx, eax
shr edx, 4
and eax, 0xf
movzx edx, byte ptr [r11 + rdx]
mov byte ptr [r9], dl
movzx edx, byte ptr [r11 + rax]
mov byte ptr [r9 + 1], dl
add r9, 3
inc r10d
cmp r10d, 16
jb 0x4a87
xor r10d, r10d
cmp r10d, r12d
jae 0x4ada
movzx eax, byte ptr [rbx + r10]
mov edx, eax
sub edx, 0x20
cmp edx, 0x5e
jbe 0x4ad0
mov al, 0x2e
mov byte ptr [r13 + r10 + 60], al
inc r10d
jmp 0x4aba
xor eax, eax
pop r13
pop r12
pop rbx
ret
mov eax, -5
ret
