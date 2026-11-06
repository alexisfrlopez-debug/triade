; tls13-21-enregistrement-deproteger · bloc l'enregistrement déprotéger (l'anti-rejoue par la séquence) · spec tls13-21:R1 · bloc carte h100021
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0xeb40, taille 448 octets
; Domaine : tls13 (M9, l'ère 1.0.0) · Dépendances : bloc ; tls13-19 (UNE composition — le déverrouillage) ; l'en-tête CONFRONTÉE AVANT TOUT (le type 23 → -1, la longueur déclarée == reçue et les bornes → -2, la version héritage IGNORÉE mais couverte par l'AAD : la mutation → -4, la cryptographie attrape ce que la logique ignore), l'AAD = l'en-tête REÇUE telle quelle, le nonce = IV ⊕ séquence, la restitution DERNIÈRE (le -4 : la sortie et le type INTACTS, la séquence ne bouge pas) ; le type = le DERNIER octet du texte interne déverrouillé dans le tampon LOCAL (la sortie P4 n'a que L−17 o) ; l'anti-rejoue par la séquence (une étiquette qui ne colle pas)
; Notation explicite générée par outils/auteur.py depuis brouillons/tls13-21-enregistrement-deproteger.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 403 o · padding : 45 o (NOP, 0x90)
; Étiquettes résolues : .copie=0xec6c, .copie_fin=0xec80, .refus_divergente=0xec97, .refus_nul=0xeca6, .refus_type=0xecb5, .refus_taille=0xecc4
; Appels directs (l'adresse scellée du plan — I1) : call 0xe500
sub rsp, 0x4078
test rcx, rcx
jz 0xeca6
test rdx, rdx
jz 0xeca6
test r9, r9
jz 0xeca6
mov rax, qword ptr [rsp + 0x40a0]
test rax, rax
jz 0xeca6
cmp r8, 23
jb 0xecc4
cmp byte ptr [rdx], 23
jne 0xecb5
movzx r10d, byte ptr [rdx + 3]
shl r10d, 8
movzx r11d, byte ptr [rdx + 4]
or r10d, r11d
lea r11, [r8 - 5]
cmp r10, r11
jne 0xecc4
cmp r10, 18
jb 0xecc4
cmp r10, 16400
ja 0xecc4
mov r11, qword ptr [rcx + 176]
mov qword ptr [rsp + 0x40], r11
mov r11d, dword ptr [rcx + 184]
mov dword ptr [rsp + 0x48], r11d
mov r11, qword ptr [rcx + 192]
bswap r11
xor qword ptr [rsp + 0x44], r11
mov qword ptr [rsp + 0x50], rdx
mov qword ptr [rsp + 0x58], rax
mov qword ptr [rsp + 0x60], r9
mov qword ptr [rsp + 0x68], rcx
lea r10, [rdx + r8 - 16]
mov qword ptr [rsp + 0x30], r10
lea r10, [rsp + 0x70]
mov qword ptr [rsp + 0x38], r10
lea r9, [r8 - 21]
lea r8, [rdx + 5]
lea rdx, [rsp + 0x40]
mov r10, qword ptr [rsp + 0x50]
mov qword ptr [rsp + 0x20], r10
mov qword ptr [rsp + 0x28], 5
call 0xe500
test eax, eax
jnz 0xec97
mov r10, qword ptr [rsp + 0x50]
movzx r11d, byte ptr [r10 + 3]
shl r11d, 8
movzx eax, byte ptr [r10 + 4]
or r11d, eax
sub r11d, 16
mov r10, r11
sub r10, 1
mov al, byte ptr [rsp + r10 + 0x70]
mov r10, qword ptr [rsp + 0x58]
mov byte ptr [r10], al
mov r10, qword ptr [rsp + 0x60]
lea r11, [r11 - 1]
xor eax, eax
cmp rax, r11
jae 0xec80
movzx edx, byte ptr [rsp + rax + 0x70]
mov byte ptr [r10 + rax], dl
add rax, 1
jmp 0xec6c
mov rcx, qword ptr [rsp + 0x68]
add qword ptr [rcx + 192], 1
xor eax, eax
add rsp, 0x4078
ret
mov rax, -4
add rsp, 0x4078
ret
mov rax, -1
add rsp, 0x4078
ret
mov rax, -1
add rsp, 0x4078
ret
mov rax, -2
add rsp, 0x4078
ret
