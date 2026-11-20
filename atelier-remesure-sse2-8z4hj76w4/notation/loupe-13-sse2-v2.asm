; loupe-13-sse2-v2 · LA VARIANTE SSE2 CORRIGÉE de la recherche d'octet — le couloir A re-mesuré (8z4hj76w4) · spec loupe-13:R1 (LE MÊME CONTRAT — R4)
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0xCC00 (la marge .text2 VIERGE du scellé — AUCUN octet du scellé touché, le modèle OPT-01)
; Domaine : loupe (M10) · Dépendances : libc-02 (le memcmp SCELLÉ à 0x1180 — LA BIBLIOTHÈQUE TENUE ÉGALE, la convention de parité)
; LA CORRECTION NOMMÉE : la vague 9 diffusait le MOTIF DE QUATRE OCTETS (movd + punpckldq + punpcklqdq — deux shuffles) au lieu du
; PREMIER OCTET — les occurrences aux alignements où m0 != m[p mod 4] étaient MANQUÉES (406/564 plantées, la différentielle plantée
; 8z4hj76w4) ; la correction : la chaîne COMPLÈTE movd + punpcklbw + punpcklwd + punpckldq + punpcklqdq (quatre shuffles, TOUS baseline
; SSE2 — la diffusion du premier octet SANS pshufb, l'interdit reconduit) ; chaque position du masque bsf-ée → r15 AVANCÉ au candidat →
; LA CONFIRMATION par LE memcmp SCELLÉ (le contrat Q4) ; l'absence du premier octet dans les 16 → l'avance de 16.
; LE CONTRAT (loupe-13:R1 À LA LETTRE — R4) : P1-P5, Q1-Q4, E1-E3, I1-I4 — la même signature (ptr u8, usize) -> usize,
; la position de LA PREMIÈRE occurrence, l'absence -1, le départ à [rsp+0x28], AUCUNE entrée IAT propre, les non-volatils rendus.
; Notation explicite — keystone assemble, le round-trip capstone 100 % exigé au build.
mov rax, qword ptr [rsp + 0x28]
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x20
test r9, r9
jz .refus_entree
cmp r9, 0x20
ja .refus_entree
cmp rax, rdx
ja .refus_entree
mov rbx, rcx
mov r12, rdx
mov r13, r8
mov r14, r9
mov r15, rax
movd xmm1, dword ptr [r13]
punpcklbw xmm1, xmm1
punpcklwd xmm1, xmm1
punpckldq xmm1, xmm1
punpcklqdq xmm1, xmm1
.balaye:
mov rcx, r12
sub rcx, r15
cmp rcx, r14
jl .absent
lea rcx, [r15 + 16]
cmp rcx, r12
ja .queue
movdqu xmm0, [rbx + r15]
pcmpeqb xmm0, xmm1
pmovmskb eax, xmm0
test eax, eax
jz .avance16
bsf eax, eax
add r15, rax
lea rcx, [rbx + r15]
mov rdx, r13
mov r8, r14
call 0x1180
test eax, eax
jz .trouve
inc r15
jmp .balaye
.avance16:
add r15, 16
jmp .balaye
.queue:
lea rcx, [rbx + r15]
mov rdx, r13
mov r8, r14
call 0x1180
test eax, eax
jz .trouve
inc r15
jmp .balaye
.trouve:
mov rax, r15
jmp .sortie
.absent:
push -1
pop rax
jmp .sortie
.refus_entree:
push -5
pop rax
.sortie:
add rsp, 0x20
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
