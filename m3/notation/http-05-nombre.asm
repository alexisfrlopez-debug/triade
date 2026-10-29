; http-05-nombre · bloc décimal borné · spec http-05:R1 · bloc carte e50005
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x5080, taille 192 octets
; Dépendances : feuille pure ; test de borne à chaque chiffre (I2)
; Notation explicite générée par outils/auteur.py depuis brouillons/http-05-nombre.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 113 o · padding : 79 o (NOP)
; Étiquettes résolues : .pas_zero=0x5096, .boucle=0x509b, .ok=0x50ce, .vide=0x50d3, .trop_long=0x50d9, .non_chiffre=0x50df, .debordement=0x50e5, .zero_tete=0x50eb
test rdx, rdx
je 0x50d3
cmp rdx, 10
ja 0x50d9
cmp byte ptr [rcx], 0x30
jne 0x5096
cmp rdx, 1
jne 0x50eb
xor eax, eax
xor r9d, r9d
cmp r9, rdx
jae 0x50ce
movzx r10d, byte ptr [rcx + r9]
sub r10, 0x30
cmp r10, 9
ja 0x50df
lea rax, [rax + rax*4]
add rax, rax
add rax, r10
movabs r11, 0xFFFFFFFF
cmp rax, r11
ja 0x50e5
add r9, 1
jmp 0x509b
mov edx, eax
xor eax, eax
ret
mov eax, 1
ret
mov eax, 2
ret
mov eax, 3
ret
mov eax, 4
ret
mov eax, 5
ret
