; tls13-07-hkdf-expand · brouillon étiqueté — spec tls13-07:R1, bloc carte h100007
; HKDF-Expand (RFC 5869 § 2.3) : OKM = T(1) || … || T(N), T(i) =
; HMAC(PRK, T(i−1) || info || octet(i)), T(0) = vide, N = ⌈L/32⌉. La boucle
; est BORNÉE PAR CONSTRUCTION : L ≤ 255 × 32 = 8160 (la borne du RFC — le
; compteur d'un seul octet, chaque i DISTINCT : la longueur est la garde).
; T(i−1) est LU DEPUIS OKM ELLE-MÊME (I2 : la sortie EST le tampon — les 32
; octets de l'itération précédente, AUCUNE seconde copie détenue) ; la
; DERNIÈRE itération dépose T(N) dans le brouillon 32 o de la pile puis
; recopie SEULS les L − 32(N−1) octets restants — la sortie n'est JAMAIS
; dépassée d'un octet. Le tampon T(i−1) || info || i vit sur la pile en
; ALLOCATION DYNAMIQUE 16-alignée (taille = (F + 0x78) & ~0xF : ombre 0x20,
; logement du 5e argument @+0x20, T @+0x28, info @+0x48, l'octet compteur,
; le brouillon 32 o — l'épilogue RECALCULE la taille depuis F).
; rcx = le PRK (32 o, FIXE — P1) · rdx = l'info (F o) · r8 = F (0 ≤ F ≤
; 2^61 − 33, la borne arithmétique : le tampon doit tenir) · r9 = L (1 ≤ L ≤
; 8160) · [rsp+0x28] = l'OKM (L o) · rax = 0 (ou -1/-2 NOMMÉS : pointeur de
; sortie nul ; L = 0, L > 8160 ; F hors borne). Le PRK et l'info INTACTS.
; Le temps est constant PAR RAPPORT AU PRK (I3 : le PRK est un secret dérivé
; — la propriété hérite de tls13-05 ; la boucle ne dépend QUE de L et F,
; publics). COMPOSITION DÉCLARÉE (I1) : tls13-05 appelé à CHAQUE itération.
; AUCUN état détenu (charte § 6) ; AUCUNE entrée IAT, AUCUN site syscall
; (charte § 7) ; la croissance du slot est NOP, 0x90 (charte § 8).
; 7 pushes (56 o) : entrée ≡ 8 → 8−56 ≡ 0 (mod 16) aux points d'appel ; le
; sub dynamique est 16-aligné, la parité est tenue ; le 5e argument de
; l'appelant relu à +0x60 AVANT l'allocation.
push rbx
push r12
push r13
push r14
push r15
push rdi
push rsi
mov rbx, qword ptr [rsp + 0x60]
test rbx, rbx
je .refus_nul
mov r12, rcx
mov r13, r9
mov r14, r8
mov r15, rdx
test r13, r13
jz .refus_taille
cmp r13, 8160
ja .refus_taille
lea rax, [r14 + 0x21]
movabs r10, 0x2000000000000000
cmp rax, r10
ja .refus_taille
mov rdi, 1
xor esi, esi
lea rax, [r14 + 0x78]
and al, 0xf0
sub rsp, rax
.boucle:
; --- T(i−1) ← OKM (I2 : la sortie est le tampon, 4 quads) -------------------
xor r10d, r10d
cmp rdi, 1
je .sans_t
lea r11, [rbx + rsi]
sub r11, 32
lea r10, [rsp + 0x28]
mov rax, qword ptr [r11]
mov qword ptr [r10], rax
mov rax, qword ptr [r11 + 8]
mov qword ptr [r10 + 8], rax
mov rax, qword ptr [r11 + 16]
mov qword ptr [r10 + 16], rax
mov rax, qword ptr [r11 + 24]
mov qword ptr [r10 + 24], rax
mov r10d, 32
.sans_t:
; --- l'info recopiée (F PUBLIC — le compte seul), l'octet i posé ------------
lea r11, [rsp + 0x28]
add r11, r10
xor ecx, ecx
.copie_info:
cmp rcx, r14
jae .compteur
mov al, byte ptr [r15 + rcx]
mov byte ptr [r11 + rcx], al
inc rcx
jmp .copie_info
.compteur:
add r11, r14
mov byte ptr [r11], dil
; --- TLS05(PRK, 32, T||info||i, F+1+32(i>1), brouillon) ---------------------
lea rax, [rsp + 0x49]
add rax, r14
mov qword ptr [rsp + 0x20], rax
mov rcx, r12
mov edx, 32
lea r8, [rsp + 0x28]
lea r9, [r14 + 1]
add r9, r10
call TLS05
; --- recopier k = min(32, L − écrit) du brouillon vers OKM -------------------
mov rcx, r13
sub rcx, rsi
cmp rcx, 32
jbe .k_entier
mov ecx, 32
.k_entier:
lea r11, [rsp + 0x49]
add r11, r14
lea r10, [rbx + rsi]
xor eax, eax
.recopier:
cmp rax, rcx
jae .recopie_fin
mov dl, byte ptr [r11 + rax]
mov byte ptr [r10 + rax], dl
inc rax
jmp .recopier
.recopie_fin:
add rsi, rcx
inc rdi
cmp rsi, r13
jae .fini
jmp .boucle
.fini:
xor eax, eax
lea rcx, [r14 + 0x78]
and cl, 0xf0
add rsp, rcx
pop rsi
pop rdi
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
.refus_nul:
mov rax, -1
jmp .refus_epilogue
.refus_taille:
mov rax, -2
.refus_epilogue:
pop rsi
pop rdi
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
