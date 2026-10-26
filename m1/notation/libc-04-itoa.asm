; libc-04-itoa · bloc conversion décimale u32 (itoa) · spec libc-04:R1 · bloc carte b20004
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x1280, taille 128 octets
; Dépendances : bloc feuille ; tampon fourni par l'appelant
; Notation explicite générée par outils/auteur.py depuis brouillons/libc-04-itoa.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 61 o · padding : 67 o (NOP)
; Étiquettes résolues : .boucle=0x128e, .compact=0x12a8, .fin=0x12b8
push rbx
mov rbx, rdx
lea r8, [rbx + 11]
mov byte ptr [r8], 0
mov eax, ecx
mov r9d, 10
xor edx, edx
div r9d
add dl, 48
dec r8
mov byte ptr [r8], dl
test eax, eax
jne 0x128e
xor ecx, ecx
mov al, byte ptr [r8 + rcx]
mov byte ptr [rbx + rcx], al
test al, al
je 0x12b8
inc rcx
jmp 0x12a8
mov rax, rbx
pop rbx
ret
