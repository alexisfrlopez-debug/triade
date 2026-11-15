; loupe-13 · recherche : la première occurrence du motif dans la fenêtre ·
; brouillon auteur DE CAMPAGNE (l'unité 5, D204 — la feuille pure de la
; navigation, le juge par memcmp hérité PAR LA CARTE)
; spec loupe-13:R1 — l'écrit-avant-code : le modèle AVANT ces octets ; le
; juge ne relit jamais l'accusé.
; LES CHOIX DE LA MAIN (l'unité 5 × bras T — la feuille pure) :
;   ① LE DÉPART LU AU-DEVANT, LES BORNES AVANT LE CADRE : P5 lu à
;      [rsp+0x28] AVANT tout push (le cadre ne le cache jamais) ; les
;      TROIS refus (E1 le motif vide, E2 le motif > 32 MOTIF_MAX, E3 le
;      départ au-delà de la fenêtre) SANS AUCUN GESTE — le refus ne touche
;      pas la pile : DEUX sorties, la droite et la refusée ;
;   ② LA BORNE EN ADRESSE : le DERNIER candidat posé UNE FOIS en adresse
;      (fenêtre + taille − motif) avant la boucle — la boucle compare
;      POINTEUR À POINTEUR (cmp rbx, r14), l'arithmétique ne revit jamais
;      à l'intérieur ; le constat trivial (Q2 : le motif ne tient pas dans
;      la plage restante) est CE MÊME test — la FIN NOMMÉE sans une
;      itération, jamais une boucle ;
;   ③ LE CURSEUR EST LE POINTEUR : le candidat avance par inc — jamais un
;      index recalculé par lea à chaque pas ; la position rendue par une
;      seule SOUSTRACTION à la sortie (le candidat − la base) ;
;   ④ LA COMPARAISON PAR LA CARTE (I2) : chaque candidat testé par
;      libc-02 memcmp LE BLOC SCELLÉ M1 à 0x1180, byte-identique — jamais
;      une boucle de comparaison réécrite (R7) ; la liste d'appels est
;      FERMÉE (libc-02 seul) ;
;   ⑤ LE CADRE HONNÊTE : cinq pushes (rbx r12 r13 r14 r15) + l'ombre 0x20
;      — le scellé a droit à son ombre d'appel (l'ABI, jamais une
;      supposition sur ses entrailles) ; l'alignement tenu (8 − 40 − 32
;      ≡ 0 mod 16) ;
;   ⑥ LES MOINS VRAIS PAR LA PILE : push −1/pop rax, push −5/pop rax —
;      l'imm8 dépassé du signe à 64 bits ; « mov eax, −1 » mentirait le
;      haut (le juge lit rax entier) ;
;   ⑦ la fenêtre et le motif LUS SEULS (I3 — la pureté) ; la recherche
;      directe O(n·m), m ≤ 32 : AUCUNE table, AUCUNE allocation (I3) ; le
;      premier match gagne (Q4 — la boucle monte du départ, jamais un
;      saut) ; rax = la position ABSOLUE, départ compté (Q1).
; appelés : LIBC02 seul (la liste fermée — I2). IAT : AUCUNE entrée (I1 —
; la feuille pure, le miroir exact des feuilles tls13, charte § 9).
; ABI : msx64. rbx/r12/r13/r14/r15 sauvegardés (les cinq du geste), les
; autres non-volatils JAMAIS TOUCHÉS ; l'ombre 0x20 donnée à l'appel.

; --- P5 au-devant, puis les trois refus SANS AUCUN GESTE (①) ---
mov rax, qword ptr [rsp + 0x28]
test r9, r9
jz .refus
cmp r9, 32
ja .refus
cmp rax, rdx
ja .refus

; --- Le cadre honnête (⑤) : cinq pushes, l'ombre de l'appel ---
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x20
mov r15, rcx
mov r12, r8
mov r13, r9

; --- La borne en adresse (②③) : le premier et le DERNIER candidat ---
lea rbx, [rcx + rax]
lea r14, [rcx + rdx]
sub r14, r9
cmp rbx, r14
ja .fin_nomme

; --- La recherche directe (④⑦) : chaque candidat au scellé, le premier gagne ---
.boucle:
mov rcx, rbx
mov rdx, r12
mov r8, r13
call LIBC02
test eax, eax
jz .trouve
inc rbx
cmp rbx, r14
jbe .boucle

; --- La FIN NOMMÉE (⑥) : l'absence, le vrai −1 par la pile ---
.fin_nomme:
push -1
pop rax
jmp .sortie

; --- La première occurrence (③⑦) : la position par une soustraction ---
.trouve:
sub rbx, r15
lea rax, [rbx + 1]
jmp .sortie

; --- La refusée (①⑥) : le vrai −5 par la pile, la pile jamais touchée ---
.refus:
push -5
pop rax
ret

; --- La sortie (⑤) : le cadre rendu ---
.sortie:
add rsp, 0x20
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
