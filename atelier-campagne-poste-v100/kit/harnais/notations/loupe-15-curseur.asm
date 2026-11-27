; loupe-15-curseur · bloc le curseur : la cellule active, la vue qui suit — jamais perdue · spec loupe-15:R1 · bloc carte i110015
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x6080, taille 448 octets
; Domaine : loupe (M10, le TGN « Loupe ») · Dépendances : LE PAS (Q1 : ±1/±16/±352, VK_DEBUT l'aligne16_inf, VK_FIN min(aligne16+15, taille-1) — la fin de ligne RÉELLE) ; LA BORNE (Q2 : le clamp [0, taille-1], les bords SONT DES ARRÊTS — rax = 0 QUAND MÊME, le bord n'est pas un échec) ; LA VUE SUIT (Q3 : la fenêtre visible LUE AUX LIGNES VISIBLES de la vitrine [METRIQUES.lignes - 3, capée 24 — la lecture STRICTE de la spec : le curseur JAMAIS perdu hors écran, y compris la vitrine rétrécie ; à la vitrine 0.1.0 la fenêtre == le remplissage 384, le miroir du commit de loupe-12] ; le recadrage par LA RÈGLE DU PLAN — curseur - 176 aligné16_inf, clapé vue_max) ; loupe-02 (la fenêtre relue, SEULEMENT au recadrage — I2 : le harnais compte les lectures) ; InvalidateRect (le repaint demandé : la surbrillance suit, le bloc ne peint RIEN — I3) ; le repli SANS session (P2 : rien bougé, la vitrine vide) ; AUCUNE entrée IAT PROPRE au delà de la feuille partagée (I4 — la composition seule, charte § 9)
; Notation explicite générée par outils/auteur.py depuis brouillons/loupe-15-curseur.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 391 o · padding : 57 o (NOP, 0x90)
; Étiquettes résolues : .debut=0x60f1, .fin=0x60f7, .fin_pos=0x610e, .gauche=0x6113, .droite=0x6118, .haut=0x611d, .bas=0x6123, .precedent=0x6129, .suivant=0x6132, .borne=0x6139, .borne_haute=0x6143, .pas_faite=0x614c, .vis_pos=0x6164, .vis_cap=0x616e, .recadre=0x6186, .recadre_pos=0x6194, .recadre_vmax_zero=0x61ad, .recadre_vmax_fin=0x61af, .recadre_fin=0x61b7, .visible=0x61d6, .rien=0x61e7, .refus=0x61eb, .sortie=0x61f9
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x6090 + 0x7 + 0x7f69 = 0xe000
;   0x6153 + 0x7 + 0x9c96 = 0xfdf0
;   0x61e1 + 0x6 - 0x3047 = 0x31a0
; Appels directs (l'adresse du plan — I1) : call 0x4240, call qword ptr [rip - 0x3047]
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x20
mov r12, rcx
lea rbx, [rip + 0x7f69]
cmp qword ptr [rbx + 528], -1
je 0x61e7
mov r13, qword ptr [rbx + 520]
test r13, r13
jz 0x61e7
mov r14, qword ptr [rbx + 544]
cmp r8d, 0x24
je 0x60f1
cmp r8d, 0x23
je 0x60f7
cmp r8d, 0x25
je 0x6113
cmp r8d, 0x27
je 0x6118
cmp r8d, 0x26
je 0x611d
cmp r8d, 0x28
je 0x6123
cmp r8d, 0x21
je 0x6129
cmp r8d, 0x22
je 0x6132
jmp 0x61e7
and r14, -16
jmp 0x614c
mov rax, r14
and rax, -16
add rax, 15
lea rdx, [r13 - 1]
cmp rax, rdx
jbe 0x610e
mov rax, rdx
mov r14, rax
jmp 0x614c
dec r14
jmp 0x6139
inc r14
jmp 0x6139
sub r14, 16
jmp 0x6139
add r14, 16
jmp 0x6139
sub r14, 352
jmp 0x6139
add r14, 352
test r14, r14
jns 0x6143
xor r14d, r14d
jmp 0x614c
cmp r14, r13
jb 0x614c
lea r14, [r13 - 1]
mov qword ptr [rbx + 544], r14
lea rax, [rip + 0x9c96]
mov eax, dword ptr [rax + 8]
sub eax, 3
jns 0x6164
xor eax, eax
cmp eax, 24
jbe 0x616e
mov eax, 24
shl rax, 4
mov rdx, qword ptr [rbx + 536]
add rax, rdx
cmp r14, rdx
jb 0x6186
cmp r14, rax
jb 0x61d6
mov rcx, r14
sub rcx, 176
jns 0x6194
xor ecx, ecx
and rcx, -16
mov rax, r13
sub rax, 384
jbe 0x61ad
add rax, 15
and rax, -16
jmp 0x61af
xor eax, eax
cmp rcx, rax
jbe 0x61b7
mov rcx, rax
cmp rcx, qword ptr [rbx + 536]
je 0x61d6
mov r15, rcx
mov rcx, r15
call 0x4240
test eax, eax
jnz 0x61eb
mov qword ptr [rbx + 536], r15
mov rcx, r12
xor edx, edx
mov r8d, 1
call qword ptr [rip - 0x3047]
xor eax, eax
jmp 0x61f9
add rsp, 0x20
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
add rsp, 0x20
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
