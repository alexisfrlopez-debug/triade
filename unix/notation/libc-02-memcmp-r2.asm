; libc-02-memcmp-r2 · bloc comparaison mémoire normalisée (libc-02:R2) · spec libc-02:R2 · bloc carte f61004
; Profil : x86-64-linux-elf64 · ABI SysV · slot RVA 0x10c0, taille 128 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/libc-02-memcmp-r2.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 42 o · padding : 86 o (NOP)
; Étiquettes résolues : .fin=0x10e9, .sup=0x10e4
xor eax, eax
test rdx, rdx
je 0x10e9
mov rcx, rdx
repe cmpsb byte ptr [rsi], byte ptr [rdi]
je 0x10e9
movzx r10d, byte ptr [rdi - 1]
movzx r11d, byte ptr [rsi - 1]
cmp r10d, r11d
ja 0x10e4
mov eax, 0xffffffff
jmp 0x10e9
mov eax, 1
ret
