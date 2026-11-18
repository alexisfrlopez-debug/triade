; loupe-13-recherche · bloc la recherche : la première occurrence par memcmp hérité (pur) · spec loupe-13:R1 · bloc carte i110013
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x5740, taille 192 octets
; Domaine : loupe (M10, le TGN « Loupe ») · Dépendances : libc-02 memcmp (LE BLOC SCELLÉ M1 PAR LA CARTE — I2 : chaque candidat testé par le scellé, JAMAIS une boucle réécrite) ; AUCUNE entrée IAT (la feuille pure, charte § 9) ; le départ à [rsp+0x28] (P5, le 5e argument msx64, lu À L'ENTRÉE avant toute poussée) ; la position ABSOLUE de la PREMIÈRE occurrence ou −1 (LA FIN NOMMÉE), les trois refus −5
; LA CONSTRUCTION D210 (l'unité 03 × bras T) : la spirale des HUIT tours puis LE GESTE MÉCANIQUE DU LABO (nommé, bijectif — le précédent 336/341) : les tours convergèrent séparément (l'épargne aux non-volatils poussés au tour 7, le départ lu au tour 8, les arguments msx64 aux tours 6-8) sans jamais se combiner — le lab les unit : la remappe bijective des arguments (rdi→rcx, rsi→rdx, rdx→r8) ET de la position (r10→r15, l'épargné — r10 est VOLATILE, le scellé peut le détruire), le re-pose de la ligne du départ (AVANT toute poussée — le cadre ne le cache jamais), la Q2 calculée DANS RAX (r12 demeure window_len pur), le prologue UNE fois, le ret re-posé
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
mov rax, r12
sub rax, r15
cmp r14, rax
jg .fin_nomme
.search_loop:
mov rax, r15
add rax, r14
cmp rax, r12
ja .fin_nomme
lea rcx, [rbx + r15]
mov rdx, r13
mov r8, r14
call LIBC02
test eax, eax
jz .trouve
inc r15
jmp .search_loop
.trouve:
lea rax, [r15 + 1]
jmp .sortie
.fin_nomme:
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
