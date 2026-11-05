; tls13-08-hkdf-expand-label · brouillon étiqueté — spec tls13-08:R1, bloc carte h100008
; HKDF-Expand-Label (RFC 8446 § 7.1) — LE bloc du calendrier : TOUTES les
; clés de TLS 1.3 naissent de lui. La structure HkdfLabel { longueur u16
; GROS-BOUTISTE ; étiquette = « tls13 » + libellé ; contexte } sérialisée
; OCTET PAR OCTET dans le tampon de pile (I1 : 2 + 1 + 6 + libellé + 1 +
; contexte, construite par immédiats fixes), puis remise à tls13-07 (UNE
; composition déclarée, I1). Le préfixe « tls13 » est une CONSTANTE du plan
; d'adressage (I2 : tls13/layout.py PREFIXE_ETIQUETTE — les immédiats
; 0x31736c74 « tls1 » + 0x2033 « 3 » — jamais recopiée, T5). Le libellé et
; le contexte sont des DONNÉES PUBLIQUES ; le secret ne traverse QUE la
; remise (I3 : le temps est constant PAR RAPPORT AU SECRET).
; rcx = le secret (32 o) · rdx = le libellé SANS préfixe (1..249) · r8 = sa
; longueur · r9 = le contexte (C o, ignoré si C = 0) · [rsp+0x28] = C
; (0..255) · [rsp+0x30] = L (1..8160) · [rsp+0x38] = la sortie (L o) ·
; rax = 0 (ou -1/-2 NOMMÉS : pointeurs nuls ; libellé vide ou > 249, C > 255,
; L = 0 ou > 8160). Le secret, le libellé et le contexte INTACTS (Q2).
; AUCUN état détenu (charte § 6) ; AUCUNE entrée IAT, AUCUN site syscall
; (charte § 7) ; la croissance du slot est NOP, 0x90 (charte § 8).
; ERRATUM consigné (sur pièces, AVANT la notation — le modèle M9 av-10) :
; la spec écrit « ≤ 264 o » pour le tampon — l'arithmétique des bornes
; P3/P5 donne 2 + 1 + 255 + 1 + 255 = 514 o ; le tampon est ARRÊTÉ à 0x202
; (514) — la borne de la SPEC est le contrat, son addition seule est fautive.
; 7 pushes (56 o) : entrée ≡ 8 → 8−56 ≡ 0 (mod 16) au point d'appel ;
; sub rsp, 0x2a0 : l'ombre (0x20) + le logement du 5e argument de TLS07
; @+0x20 + le tampon HkdfLabel @+0x28 (514 o) — les 5e/6e/7e arguments de
; l'appelant relus à +0x300/+0x308/+0x310.
push rbx
push r12
push r13
push r14
push r15
push rdi
push rsi
sub rsp, 0x2a0
mov rbx, qword ptr [rsp + 0x310]
mov rdi, qword ptr [rsp + 0x300]
mov rsi, qword ptr [rsp + 0x308]
mov r12, rcx
mov r13, rdx
mov r14, r8
mov r15, r9
test rbx, rbx
je .refus_nul
test r12, r12
je .refus_nul
test r13, r13
je .refus_nul
test r14, r14
jz .refus_bornes
cmp r14, 249
ja .refus_bornes
cmp rdi, 255
ja .refus_bornes
test rdi, rdi
jz .ctx_vide
test r15, r15
jz .refus_nul
.ctx_vide:
test rsi, rsi
jz .refus_bornes
cmp rsi, 8160
ja .refus_bornes
; --- la sérialisation GROS-BOUTISTE (I1 : immédiats fixes) ------------------
lea r10, [rsp + 0x28]
mov rax, rsi
xchg al, ah
mov word ptr [r10], ax
lea r11, [r14 + 6]
mov byte ptr [r10 + 2], r11b
mov dword ptr [r10 + 3], 0x31736c74
mov word ptr [r10 + 7], 0x2033
lea r11, [r10 + 9]
xor ecx, ecx
.copie_libelle:
cmp rcx, r14
jae .libelle_fini
mov al, byte ptr [r13 + rcx]
mov byte ptr [r11 + rcx], al
inc rcx
jmp .copie_libelle
.libelle_fini:
add r11, r14
mov byte ptr [r11], dil
inc r11
xor ecx, ecx
.copie_ctx:
cmp rcx, rdi
jae .ctx_fini
mov al, byte ptr [r15 + rcx]
mov byte ptr [r11 + rcx], al
inc rcx
jmp .copie_ctx
.ctx_fini:
lea rax, [r14 + rdi]
add rax, 10
; --- la remise à tls13-07 (I1 : UNE composition déclarée) --------------------
mov qword ptr [rsp + 0x20], rbx
mov rcx, r12
mov rdx, r10
mov r8, rax
mov r9, rsi
call TLS07
jmp .fin
.refus_nul:
mov rax, -1
jmp .fin
.refus_bornes:
mov rax, -2
.fin:
add rsp, 0x2a0
pop rsi
pop rdi
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
