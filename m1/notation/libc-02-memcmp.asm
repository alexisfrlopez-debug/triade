; libc-02-memcmp · bloc comparaison normalisée (memcmp) · spec libc-02:R1 · bloc carte b20002
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x1180, taille 128 octets
; Dépendances : bloc feuille ; aucun accès extérieur
; Notation explicite générée par outils/auteur.py depuis brouillons/libc-02-memcmp.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 57 o · padding : 71 o (NOP)
; Étiquettes résolues : .egal=0x11ac, .sup=0x11b0, .fin=0x11b5, .zero=0x11b8
xor eax, eax
test r8, r8
je 0x11b8
push rdi
push rsi
mov rdi, rcx
mov rsi, rdx
mov rcx, r8
repe cmpsb byte ptr [rsi], byte ptr [rdi]
je 0x11ac
movzx r10d, byte ptr [rdi - 1]
movzx r11d, byte ptr [rsi - 1]
cmp r10d, r11d
ja 0x11b0
mov eax, -1
jmp 0x11b5
xor eax, eax
jmp 0x11b5
mov eax, 1
pop rsi
pop rdi
ret
ret
