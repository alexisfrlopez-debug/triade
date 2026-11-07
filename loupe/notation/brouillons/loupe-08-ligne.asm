; loupe-08 · composer UNE ligne hexadécimale : 77 o exacts, tampon fixe · spec loupe-08:R1
; LE FORMAT (Q1) : 8 chiffres hex du décalage (grand-boutiste, MAJUSCULES —
; la table R_HEX du plan, I4) · 2 espaces · 16 groupes « HH » séparés par un
; espace (l'espace médian DOUBLÉ après le huitième) · 2 espaces · le miroir
; ASCII de 16 · NUL — EXACTEMENT 77 o écrits, jamais un de plus (I2 : les
; bornes P2/P4 vérifiées AVANT la première écriture).
; LA LIGNE INCOMPLÈTE (Q3) : le remplissage d'espaces [8..75] POSE les
; séparateurs et les groupes absents d'un geste — les groupes au-delà de la
; longueur demeurent deux espaces, le miroir au-delà un espace : la colonne
; ASCII ne bouge JAMAIS (l'alignement est un invariant, pas une chance).
; LE MIROIR (Q2) : 0x20..0x7E → le caractère ; tout autre → « . » (le point
; de remplacement). LA SOURCE EST LUE SEULE (I3) ; rax = 0 (Q4).
; E1/E2/E3 : longueur 0, longueur 17+, pointeur nul → verdict -5, RIEN écrit.
; Feuille pure : AUCUNE entrée IAT, AUCUN état détenu (I1 — le miroir tls13).
push rbx
push r12
push r13
push r14
sub rsp, 0x28
test rcx, rcx
jz .refus_entree
test r8, r8
jz .refus_entree
cmp rdx, 1
jb .refus_entree
cmp rdx, 16
ja .refus_entree
mov rbx, rcx
mov r12, rdx
mov r13, r8
mov r14, r9
lea r11, [rip + HEX]
; — les 8 chiffres du décalage : les nibbles 28..0, grand-boutiste —
mov edx, 28
xor r10d, r10d
.dec_boucle:
mov rax, r14
mov cl, dl
shr rax, cl
and eax, 0xf
movzx eax, byte ptr [r11 + rax]
mov byte ptr [r13 + r10], al
sub edx, 4
inc r10d
cmp r10d, 8
jb .dec_boucle
; — le remplissage [8..59] : séparateurs, groupes vides, l'avant-miroir —
mov eax, 8
.rempli_haut:
mov byte ptr [r13 + rax], 0x20
inc eax
cmp eax, 60
jb .rempli_haut
; — le remplissage [60..75] : le miroir absent demeure un espace —
mov eax, 60
.rempli_miroir:
mov byte ptr [r13 + rax], 0x20
inc eax
cmp eax, 76
jb .rempli_miroir
mov byte ptr [r13 + 76], 0
; — les groupes hexa : pos = 10 + 3·i + (i >= 8 ? 1 : 0) —
xor r10d, r10d
.grp_boucle:
cmp r10d, r12d
jae .grp_suivant
lea eax, [r10 + r10*2 + 10]
cmp r10d, 8
jb .grp_pos
inc eax
.grp_pos:
movzx edx, byte ptr [rbx + r10]
mov ecx, edx
shr edx, 4
and ecx, 0xf
movzx edx, byte ptr [r11 + rdx]
mov byte ptr [r13 + rax], dl
movzx edx, byte ptr [r11 + rcx]
mov byte ptr [r13 + rax + 1], dl
.grp_suivant:
inc r10d
cmp r10d, 16
jb .grp_boucle
; — le miroir ASCII : 0x20..0x7E le caractère, sinon le point —
xor r10d, r10d
.miroir_boucle:
cmp r10d, r12d
jae .miroir_fin
movzx edx, byte ptr [rbx + r10]
cmp dl, 0x20
jb .miroir_point
cmp dl, 0x7e
ja .miroir_point
jmp .miroir_poser
.miroir_point:
mov dl, 0x2e
.miroir_poser:
mov byte ptr [r13 + r10 + 60], dl
inc r10d
jmp .miroir_boucle
.miroir_fin:
xor eax, eax
jmp .sortie
.refus_entree:
mov eax, -5
.sortie:
add rsp, 0x28
pop r14
pop r13
pop r12
pop rbx
ret
