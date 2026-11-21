; loupe-13-avx2-hisse · LE COULOIR AVX2 DE LA RECHERCHE AU DISPATCH HISSÉ (x705m50vl, la vague 12) · spec loupe-13:R1 (LE MÊME CONTRAT — R4)
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0xE600 (la marge VIERGE — AUCUN octet du scellé touché, le modèle OPT-01)
; Domaine : loupe (M10) · Dépendances : libc-02 (le memcmp SCELLÉ à 0x1180 — LA BIBLIOTHÈQUE TENUE ÉGALE)
; LE DISPATCH HISSÉ (la condition nommée de fnvan0zes : « l'embarquement exigera le sondage hissé,
; le couloir porte la note » — la note EST TENUE ici) : le sondage CPUID (OSXSAVE → XGETBV ×CR0 →
; leaf 7 EBX bit 5) VIT À L'APPELANT, HISSE UNE FOIS PAR SESSION — le verdict RÉSOLU AU CHARGEMENT
; et PASSÉ SOUS R10 : r10 = 0 → LE CHEMIN AVX2 ; r10 ≠ 0 → LE REPLI BASELINE SSE2 — le bloc ne
; sonde JAMAIS ici, le cpuid (≈ 2 660 cycles la sortie au bac virtualisé, fnvan0zes) ne se paie
; plus par appel ; le repli DEMEURE JAMAIS un chemin mort : la machine sans AVX2 le vit (r10 ≠ 0)
; LA BOUCLE AVX2 : 32 octets par fenêtre (vmovdqu + vpcmpeqb + vpmovmskb), la queue à L'IDIOME
; MEMCHR (la dernière fenêtre de 32 NON-ALIGNÉE, les bits sous la position éteints — le même idiome
; que la libc), la confirmation par LE memcmp scellé (le contrat Q4 inchangé)
; LE CONTRAT (loupe-13:R1 À LA LETTRE — R4) : P1-P5, Q1-Q4, E1-E3, I1-I4 — la même signature, la
; première occurrence, l'absence -1, le départ à [rsp+0x28], les non-volatils rendus ; le corps
; SSE2 (xmm) et AVX2 (ymm) ne se touchent jamais (la discipline VEX)
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
; ---- LE DISPATCH HISSÉ (r10 = le verdict de session — aucun cpuid ici) --------------
; LE PORTEUR r11 : la fenêtre sauvée AVANT tout chemin — la leçon des registres
; porteurs (8z4hj76w4) reconduite : le repli16 est atteint DEPUIS la file AVX2
; (n < 32) où rcx est déjà consommé par le balayage ; r10 porte le verdict, le
; porteur vit à r11 ; rdx demeure intact aux DEUX entrées du repli (nommé)
mov r11, rcx
test r10, r10
jnz .repli
; ---- LE CHEMIN AVX2 ----------------------------------------------------------------
mov rbx, rcx
mov r12, rdx
mov r13, r8
mov r14, r9
mov r15, qword ptr [rsp + 0x70]
vpbroadcastb ymm1, byte ptr [r13]
.balaye32:
mov rcx, r12
sub rcx, r15
cmp rcx, r14
jl .absent
lea rcx, [r15 + 32]
cmp rcx, r12
ja .queue32
vmovdqu ymm0, [rbx + r15]
vpcmpeqb ymm0, ymm0, ymm1
vpmovmskb eax, ymm0
test eax, eax
jz .avance32
bsf eax, eax
add r15, rax
lea rcx, [rbx + r15]
mov rdx, r13
mov r8, r14
call 0x1180
test eax, eax
jz .trouve
inc r15
jmp .balaye32
.avance32:
add r15, 32
jmp .balaye32
.queue32:
cmp r12, 32
jl .repli16
lea r10, [r12 - 32]
vmovdqu ymm0, [rbx + r10]
vpcmpeqb ymm0, ymm0, ymm1
vpmovmskb eax, ymm0
mov rdx, r15
sub rdx, r10
cmp rdx, 32
jge .absent
mov ecx, edx
mov edx, -1
shl edx, cl
and eax, edx
jz .absent
bsf eax, eax
lea r15, [r10 + rax]
mov rcx, r12
sub rcx, r15
cmp rcx, r14
jl .absent
lea rcx, [rbx + r15]
mov rdx, r13
mov r8, r14
call 0x1180
test eax, eax
jz .trouve
inc r15
jmp .balaye32
; ---- LE REPLI BASELINE SSE2 (la v2 — jamais un chemin mort) -------------------------
.repli:
.repli16:
mov rbx, r11
mov r12, rdx
mov r13, r8
mov r14, r9
mov r15, qword ptr [rsp + 0x70]
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
vzeroupper
add rsp, 0x20
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
