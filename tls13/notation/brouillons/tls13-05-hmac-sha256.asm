; tls13-05-hmac-sha256 · brouillon étiqueté — spec tls13-05:R1, bloc carte h100005
; HMAC-SHA-256 (RFC 2104 § 2) — LA brique d'authentification du domaine :
; HKDF (tls13-06/07) et le Finished (tls13-25) ne sont QUE des compositions
; d'elle. La clé EXPULSÉE à la taille du bloc (64 o : ≤ 64 → copiée puis
; zéro-paddée ; > 64 → HACHÉE d'abord, le condensé 32 o zéro-paddé — RFC
; 2104 § 2), les masques ipad/opad (0x36/0x5c, le plan d'adressage) posés
; sur 64 positions FIXES par HUIT quads (I3 : le temps est constant PAR
; RAPPORT AU CONTENU de la clé — la longueur K est PUBLIQUE, le nombre de
; tours du premier hachage peut en dépendre, le contenu JAMAIS).
; rcx = la clé · rdx = K (0 ≤ K ≤ 2^61, la clé VIDE est légale : K' = 64
; zéros) · r8 = le message (aucun alignement exigé) · r9 = M ·
; [rsp+0x28] = la sortie (32 o) · rax = 0 (Q3 — ou -1 NOMMÉ : pointeur de
; sortie nul). La clé et le message INTACTS (Q2).
; COMPOSITION DÉCLARÉE (I1) : TLS01 (init, ctx_i et ctx_o — le chemin de
; la clé longue emprunte ctx_i une première fois), TLS03 (absorption),
; TLS04 (finalisation) — appels directs aux adresses scellées du plan.
; Les DEUX contextes (2 × 112 o), K' (64 o) et le masque (64 o) vivent sur
; la PILE (I2 — aucun état détenu, réentrant par construction) : aucun
; état, aucune adresse fixe (charte § 6), AUCUNE entrée IAT, AUCUN site
; syscall (charte § 7), AUCUN déplacement RIP (l'ancêtre tls13-02 lisait
; K @0x2F00 — ici TOUT vit en immédiats et sur la pile).
; 7 pushes (56 o) : entrée ≡ 8 → 8−56 ≡ 0 (mod 16) aux points d'appel ;
; sub rsp, 0x1a0 : L'OMBRE msx64 (0x20) fournie à chaque bloc appelé, K'
; @+0x20, le masque @+0x60, ctx_i @+0xA0, ctx_o @+0x110, L'INTÉRIEUR @+0x180
; (32 o dédiés — le masque opad n'écrase JAMAIS le condensé intérieur) —
; le 5e argument de l'appelant relu à +0x200.
push rbx
push r12
push r13
push r14
push r15
push rdi
push rsi
sub rsp, 0x1a0
mov rbx, qword ptr [rsp + 0x200]
test rbx, rbx
je .refus
mov r12, rcx
mov r13, rdx
mov r14, r8
mov r15, r9
; --- K' : l'expulsion à la taille du bloc (K PUBLIC — le compte seul) -------
cmp r13, 64
ja .cle_longue
lea rdi, [rsp + 0x20]
mov rsi, r12
mov rcx, r13
rep movsb
lea rdi, [rsp + 0x20]
add rdi, r13
mov ecx, 64
sub ecx, r13d
xor eax, eax
rep stosb
jmp .masque_interieur
.cle_longue:
lea rcx, [rsp + 0xa0]
call TLS01
lea rcx, [rsp + 0xa0]
mov rdx, r12
mov r8, r13
call TLS03
lea rcx, [rsp + 0xa0]
lea rdx, [rsp + 0x20]
call TLS04
lea rdi, [rsp + 0x20]
add rdi, 32
mov ecx, 32
xor eax, eax
rep stosb
; --- le hachage INTÉRIEUR : H((K' ⊕ ipad) || message) ------------------------
.masque_interieur:
lea rcx, [rsp + 0xa0]
call TLS01
movabs r10, 0x3636363636363636
lea rdi, [rsp + 0x60]
lea rsi, [rsp + 0x20]
mov ecx, 8
.xor_ipad:
mov rax, qword ptr [rsi]
xor rax, r10
mov qword ptr [rdi], rax
add rsi, 8
add rdi, 8
dec ecx
jnz .xor_ipad
lea rcx, [rsp + 0xa0]
lea rdx, [rsp + 0x60]
mov r8d, 64
call TLS03
lea rcx, [rsp + 0xa0]
mov rdx, r14
mov r8, r15
call TLS03
lea rcx, [rsp + 0xa0]
lea rdx, [rsp + 0x180]
call TLS04
; --- le hachage EXTÉRIEUR : H((K' ⊕ opad) || intérieur) → SORTIE ------------
; l'INTÉRIEUR vit @+0x180 (32 o dédiés) : le masque opad @+0x60 ne l'écrase
; jamais — la double composition lue dans l'ordre du RFC 2104 § 2
lea rcx, [rsp + 0x110]
call TLS01
movabs r10, 0x5c5c5c5c5c5c5c5c
lea rdi, [rsp + 0x60]
lea rsi, [rsp + 0x20]
mov ecx, 8
.xor_opad:
mov rax, qword ptr [rsi]
xor rax, r10
mov qword ptr [rdi], rax
add rsi, 8
add rdi, 8
dec ecx
jnz .xor_opad
lea rcx, [rsp + 0x110]
lea rdx, [rsp + 0x60]
mov r8d, 64
call TLS03
lea rcx, [rsp + 0x110]
lea rdx, [rsp + 0x180]
mov r8d, 32
call TLS03
lea rcx, [rsp + 0x110]
mov rdx, rbx
call TLS04
xor eax, eax
jmp .fin
.refus:
mov rax, -1
.fin:
add rsp, 0x1a0
pop rsi
pop rdi
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
