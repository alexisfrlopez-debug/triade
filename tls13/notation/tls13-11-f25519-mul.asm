; tls13-11-f25519-mul · bloc f25519 multiplication (école 5×5, repli ×19, miroir av-09) · spec tls13-11:R1 · bloc carte h100011
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0xcb40, taille 1152 octets
; Domaine : tls13 (M9, l'ère 1.0.0) · Dépendances : tls13-12 (UNE passe — I3) ; l'école 5×5 déroulée, les DIX accumulateurs u128 en PILE [sous-cadre 0xC0 — I1], le repli ×19 et la chaîne 51 bits (I2) ; rbx retenu (le pointeur b survit aux mul) ; AUCUN déplacement RIP
; Notation explicite générée par outils/auteur.py depuis brouillons/tls13-11-f25519-mul.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 1078 o · padding : 74 o (NOP, 0x90)
; Appels directs (l'adresse scellée du plan — I1) : call 0xcfc0
push rbx
sub rsp, 0xc0
mov rbx, rdx
xor eax, eax
mov qword ptr [rsp + 0x20], rax
mov qword ptr [rsp + 0x28], rax
mov qword ptr [rsp + 0x30], rax
mov qword ptr [rsp + 0x38], rax
mov qword ptr [rsp + 0x40], rax
mov qword ptr [rsp + 0x48], rax
mov qword ptr [rsp + 0x50], rax
mov qword ptr [rsp + 0x58], rax
mov qword ptr [rsp + 0x60], rax
mov qword ptr [rsp + 0x68], rax
mov qword ptr [rsp + 0x70], rax
mov qword ptr [rsp + 0x78], rax
mov qword ptr [rsp + 0x80], rax
mov qword ptr [rsp + 0x88], rax
mov qword ptr [rsp + 0x90], rax
mov qword ptr [rsp + 0x98], rax
mov qword ptr [rsp + 0xa0], rax
mov qword ptr [rsp + 0xa8], rax
mov qword ptr [rsp + 0xb0], rax
mov qword ptr [rsp + 0xb8], rax
mov r8, 19
mov rax, qword ptr [rcx]
mul qword ptr [rbx]
add qword ptr [rsp + 0x20], rax
adc qword ptr [rsp + 0x28], rdx
mov rax, qword ptr [rcx]
mul qword ptr [rbx + 8]
add qword ptr [rsp + 0x30], rax
adc qword ptr [rsp + 0x38], rdx
mov rax, qword ptr [rcx]
mul qword ptr [rbx + 16]
add qword ptr [rsp + 0x40], rax
adc qword ptr [rsp + 0x48], rdx
mov rax, qword ptr [rcx]
mul qword ptr [rbx + 24]
add qword ptr [rsp + 0x50], rax
adc qword ptr [rsp + 0x58], rdx
mov rax, qword ptr [rcx]
mul qword ptr [rbx + 32]
add qword ptr [rsp + 0x60], rax
adc qword ptr [rsp + 0x68], rdx
mov rax, qword ptr [rcx + 8]
mul qword ptr [rbx]
add qword ptr [rsp + 0x30], rax
adc qword ptr [rsp + 0x38], rdx
mov rax, qword ptr [rcx + 8]
mul qword ptr [rbx + 8]
add qword ptr [rsp + 0x40], rax
adc qword ptr [rsp + 0x48], rdx
mov rax, qword ptr [rcx + 8]
mul qword ptr [rbx + 16]
add qword ptr [rsp + 0x50], rax
adc qword ptr [rsp + 0x58], rdx
mov rax, qword ptr [rcx + 8]
mul qword ptr [rbx + 24]
add qword ptr [rsp + 0x60], rax
adc qword ptr [rsp + 0x68], rdx
mov rax, qword ptr [rcx + 8]
mul qword ptr [rbx + 32]
add qword ptr [rsp + 0x70], rax
adc qword ptr [rsp + 0x78], rdx
mov rax, qword ptr [rcx + 16]
mul qword ptr [rbx]
add qword ptr [rsp + 0x40], rax
adc qword ptr [rsp + 0x48], rdx
mov rax, qword ptr [rcx + 16]
mul qword ptr [rbx + 8]
add qword ptr [rsp + 0x50], rax
adc qword ptr [rsp + 0x58], rdx
mov rax, qword ptr [rcx + 16]
mul qword ptr [rbx + 16]
add qword ptr [rsp + 0x60], rax
adc qword ptr [rsp + 0x68], rdx
mov rax, qword ptr [rcx + 16]
mul qword ptr [rbx + 24]
add qword ptr [rsp + 0x70], rax
adc qword ptr [rsp + 0x78], rdx
mov rax, qword ptr [rcx + 16]
mul qword ptr [rbx + 32]
add qword ptr [rsp + 0x80], rax
adc qword ptr [rsp + 0x88], rdx
mov rax, qword ptr [rcx + 24]
mul qword ptr [rbx]
add qword ptr [rsp + 0x50], rax
adc qword ptr [rsp + 0x58], rdx
mov rax, qword ptr [rcx + 24]
mul qword ptr [rbx + 8]
add qword ptr [rsp + 0x60], rax
adc qword ptr [rsp + 0x68], rdx
mov rax, qword ptr [rcx + 24]
mul qword ptr [rbx + 16]
add qword ptr [rsp + 0x70], rax
adc qword ptr [rsp + 0x78], rdx
mov rax, qword ptr [rcx + 24]
mul qword ptr [rbx + 24]
add qword ptr [rsp + 0x80], rax
adc qword ptr [rsp + 0x88], rdx
mov rax, qword ptr [rcx + 24]
mul qword ptr [rbx + 32]
add qword ptr [rsp + 0x90], rax
adc qword ptr [rsp + 0x98], rdx
mov rax, qword ptr [rcx + 32]
mul qword ptr [rbx]
add qword ptr [rsp + 0x60], rax
adc qword ptr [rsp + 0x68], rdx
mov rax, qword ptr [rcx + 32]
mul qword ptr [rbx + 8]
add qword ptr [rsp + 0x70], rax
adc qword ptr [rsp + 0x78], rdx
mov rax, qword ptr [rcx + 32]
mul qword ptr [rbx + 16]
add qword ptr [rsp + 0x80], rax
adc qword ptr [rsp + 0x88], rdx
mov rax, qword ptr [rcx + 32]
mul qword ptr [rbx + 24]
add qword ptr [rsp + 0x90], rax
adc qword ptr [rsp + 0x98], rdx
mov rax, qword ptr [rcx + 32]
mul qword ptr [rbx + 32]
add qword ptr [rsp + 0xa0], rax
adc qword ptr [rsp + 0xa8], rdx
mov rax, qword ptr [rsp + 0x70]
mul r8
add rax, qword ptr [rsp + 0x20]
mov r10, rdx
adc r10, qword ptr [rsp + 0x28]
imul r11, qword ptr [rsp + 0x78], 19
add r10, r11
mov qword ptr [rsp + 0x20], rax
mov qword ptr [rsp + 0x28], r10
mov rax, qword ptr [rsp + 0x80]
mul r8
add rax, qword ptr [rsp + 0x30]
mov r10, rdx
adc r10, qword ptr [rsp + 0x38]
imul r11, qword ptr [rsp + 0x88], 19
add r10, r11
mov qword ptr [rsp + 0x30], rax
mov qword ptr [rsp + 0x38], r10
mov rax, qword ptr [rsp + 0x90]
mul r8
add rax, qword ptr [rsp + 0x40]
mov r10, rdx
adc r10, qword ptr [rsp + 0x48]
imul r11, qword ptr [rsp + 0x98], 19
add r10, r11
mov qword ptr [rsp + 0x40], rax
mov qword ptr [rsp + 0x48], r10
mov rax, qword ptr [rsp + 0xa0]
mul r8
add rax, qword ptr [rsp + 0x50]
mov r10, rdx
adc r10, qword ptr [rsp + 0x58]
imul r11, qword ptr [rsp + 0xa8], 19
add r10, r11
mov qword ptr [rsp + 0x50], rax
mov qword ptr [rsp + 0x58], r10
mov rax, qword ptr [rsp + 0xb0]
mul r8
add rax, qword ptr [rsp + 0x60]
mov r10, rdx
adc r10, qword ptr [rsp + 0x68]
imul r11, qword ptr [rsp + 0xb8], 19
add r10, r11
mov qword ptr [rsp + 0x60], rax
mov qword ptr [rsp + 0x68], r10
mov rax, qword ptr [rsp + 0x60]
mov rdx, qword ptr [rsp + 0x68]
mov r9, rax
shrd r9, rdx, 51
mov rax, r9
mul r8
add qword ptr [rsp + 0x20], rax
adc qword ptr [rsp + 0x28], rdx
movabs r10, 0x7ffffffffffff
xor r9d, r9d
mov rax, qword ptr [rsp + 0x20]
mov rdx, qword ptr [rsp + 0x28]
add rax, r9
adc rdx, 0
mov r11, rax
shrd r11, rdx, 51
and rax, r10
mov qword ptr [rcx], rax
mov r9, r11
mov rax, qword ptr [rsp + 0x30]
mov rdx, qword ptr [rsp + 0x38]
add rax, r9
adc rdx, 0
mov r11, rax
shrd r11, rdx, 51
and rax, r10
mov qword ptr [rcx + 8], rax
mov r9, r11
mov rax, qword ptr [rsp + 0x40]
mov rdx, qword ptr [rsp + 0x48]
add rax, r9
adc rdx, 0
mov r11, rax
shrd r11, rdx, 51
and rax, r10
mov qword ptr [rcx + 16], rax
mov r9, r11
mov rax, qword ptr [rsp + 0x50]
mov rdx, qword ptr [rsp + 0x58]
add rax, r9
adc rdx, 0
mov r11, rax
shrd r11, rdx, 51
and rax, r10
mov qword ptr [rcx + 24], rax
mov r9, r11
mov rax, qword ptr [rsp + 0x60]
and rax, r10
add rax, r9
mov r11, rax
shr r11, 51
and rax, r10
mov qword ptr [rcx + 32], rax
imul r11, r11, 19
add qword ptr [rcx], r11
call 0xcfc0
xor eax, eax
add rsp, 0xc0
pop rbx
ret
