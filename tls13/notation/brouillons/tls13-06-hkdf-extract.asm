; tls13-06-hkdf-extract · brouillon étiqueté — spec tls13-06:R1, bloc carte h100006
; HKDF-Extract (RFC 5869 § 2.1) : PRK = HMAC-SHA-256(sel, IKM) — le sel
; DEVIENT la clé du HMAC (l'expulsion du sel EST le geste du bloc, I1) ; le
; sel ABSENT (S = 0) devient les 32 zéros du RFC 5869 § 2.2 (« a string of
; HashLen zeros ») — le cas est PORTÉ PAR LA PILE (le calendrier TLS 1.3
; l'exige au tout premier extrait : sel vide, jamais contourné par
; l'appelant). L'IKM vide est REFUSÉ (verdict -2, P4) ; le PRK nul REFUSÉ
; (verdict -1, Q3). Le temps est constant PAR RAPPORT À L'IKM (I3 — le
; secret partagé x25519 est un IKM : la propriété hérite de tls13-05, le
; bloc n'ajoute AUCUNE branche sur le contenu).
; rcx = le sel (S o, ignoré si S = 0) · rdx = S (0 ≤ S ≤ 2^61) ·
; r8 = l'IKM (I o) · r9 = I (1 ≤ I ≤ 2^61) · [rsp+0x28] = le PRK (32 o) ·
; rax = 0 (ou -1/-2 NOMMÉS). Le sel et l'IKM INTACTS (Q2).
; COMPOSITION DÉCLARÉE (I1) : tls13-05 appelé UNE fois, à l'adresse
; scellée. AUCUN état détenu (charte § 6) ; AUCUNE entrée IAT, AUCUN site
; syscall (charte § 7) ; aucun registre non volatil détruit (I4) ; la
; croissance du slot est NOP, 0x90 (I5, charte § 8).
; 5 pushes (40 o) : entrée ≡ 8 → 8−40 ≡ 0 (mod 16) au point d'appel ;
; sub rsp, 0x50 : l'ombre msx64 (0x20) + le logement du 5e argument de
; TLS05 @+0x20 + les 32 zéros @+0x28 posés par QUATRE quads — AUCUN
; registre non volatil touché (rdi rendu : le défaut du premier geste
; nommé par le harnais V4) — le 5e argument de l'appelant relu à +0xA0.
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x50
mov rbx, qword ptr [rsp + 0xa0]
mov r15, r8
mov r14, r9
test rbx, rbx
je .refus_nul
test r14, r14
jz .refus_vide
mov r13, rdx
mov qword ptr [rsp + 0x28], 0
mov qword ptr [rsp + 0x30], 0
mov qword ptr [rsp + 0x38], 0
mov qword ptr [rsp + 0x40], 0
test r13, r13
jz .sel_vide
mov r12, rcx
jmp .hmac
.sel_vide:
lea r12, [rsp + 0x28]
mov r13d, 32
.hmac:
mov [rsp + 0x20], rbx
mov rcx, r12
mov rdx, r13
mov r8, r15
mov r9, r14
call TLS05
jmp .fin
.refus_nul:
mov rax, -1
jmp .fin
.refus_vide:
mov rax, -2
.fin:
add rsp, 0x50
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
