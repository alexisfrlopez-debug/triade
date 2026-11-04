; libc-04-itoa-r3 · bloc conversion décimale u32 (libc-04:R3) · spec libc-04:R3 · bloc carte f61006
; Profil : x86-64-linux-elf64 · ABI SysV · slot RVA 0x1180, taille 128 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/libc-04-itoa-r3.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 59 o · padding : 69 o (NOP)
; Étiquettes résolues : .compacte=0x11a7, .fin=0x11b7, .genere=0x1193
mov r8, rsi
add r8, 0xb
mov byte ptr [r8], 0
mov eax, edi
mov r9d, 0xa
xor edx, edx
div r9d
add dl, 0x30
dec r8
mov byte ptr [r8], dl
test eax, eax
jne 0x1193
xor ecx, ecx
mov al, byte ptr [r8 + rcx]
mov byte ptr [rsi + rcx], al
test al, al
je 0x11b7
inc rcx
jmp 0x11a7
mov rax, rsi
ret
