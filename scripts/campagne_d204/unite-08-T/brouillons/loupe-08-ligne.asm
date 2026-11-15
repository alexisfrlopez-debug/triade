; loupe-08 · composer la ligne hexadécimale de 77 o : le décalage, les seize
; groupes, le miroir ASCII · brouillon auteur DE CAMPAGNE (l'unité 4, D204)
; spec loupe-08:R1 — l'écrit-avant-code : oracle-depuis-I.txt (le modèle AVANT
; ces octets ; le juge ne relit jamais l'accusé).
; LES CHOIX DE LA MAIN (l'unité 4 × bras T — la feuille pure) :
;   ① LA FEUILLE SANS CADRE : TROIS pushes (rbx r12 r13) et rien au-delà —
;      la feuille n'appelle rien, la pile ne se touche jamais sous rsp (I1 :
;      aucun état détenu, la zone rouge de msx64 n'existe pas et je n'y
;      écris pas) ;
;   ② LES BORNES AVANT LES PUSHES MÊMES (I2 le plus strict) : P1/P3 nuls,
;      P2 hors 1..16 → -5 SANS AUCUN GESTE — le refus ne pousse même pas
;      un registre : deux sorties, la droite et la refusée ;
;   ③ LE DÉCALAGE EN VOLATIL SÛR : r9 demeure de l'entrée au dernier
;      chiffre — aucun appel ne le détruit (la feuille ne connaît pas
;      d'intermédiaire : r14/r15 inutiles, jamais sauvés) ;
;   ④ LES HUIT CHIFFRES PAR ROTATION : rol 36 amène les bits 31-28 aux
;      bits 3-0, rol 4 descend le nibble suivant — le décalage tourne,
;      JAMAIS le compteur de décalage (le geste du scellé) ;
;   ⑤ LE SQUELETTE EN MOTS : la boucle des HUIT QWORDS d'espaces (loop,
;      le geste antique — HUIT itérations, jamais la boucle d'octets du
;      scellé) + le dword + le NUL ; les groupes absents et le miroir
;      absent demeurent des espaces : Q3 née du remplissage même, la
;      colonne ASCII ne bouge jamais ;
;   ⑥ LES GROUPES EN DEUX BOUCLES À PAS FIXE : la basse pose à 10 + 3·i,
;      la haute à 35 + 3·(i - 8) — l'espace médian déjà posé par le
;      squelette : JAMAIS le saut conditionnel de position ;
;   ⑦ LE MIROIR PAR LA SOUSTRACTION SUR LA COPIE : (c - 0x20) non-signé
;      ≤ 0x5E → le caractère DÉMEURÉ DANS AL (la jauge vit en edx —
;      jamais l'octet mesuré n'est l'octet posé), sinon le point — UNE
;      comparaison, jamais les deux bornes (Q2) ;
;   ⑧ la table « 0123456789ABCDEF » du plan PAR DÉPLACEMENT RIP (I4 —
;      R_HEX .rdata) ; la source LUE SEULE (I3) ; rax = 0 (Q4).
; appelés : AUCUN (la feuille pure — le miroir exact des feuilles tls13,
; charte § 9). IAT : AUCUNE entrée (I1 — la liste fermée est vide).
; ABI : msx64. rbx/r12/r13 sauvegardés (les trois du geste), les autres
; non-volatils JAMAIS TOUCHÉS ; aucune pile d'arguments (aucun appel).

; --- Les bornes d'abord (②/I2) : quatre refus SANS AUCUN GESTE ---
test rcx, rcx
jz .refus
test r8, r8
jz .refus
cmp rdx, 1
jb .refus
cmp rdx, 16
ja .refus

; --- Le cadre minimal (①) : trois pushes, la pile intacte au-delà ---
push rbx
push r12
push r13
mov rbx, rcx
mov r12, rdx
mov r13, r8
lea r11, [rip + HEX]

; --- Les huit chiffres du décalage (④) : la rotation, nibble à nibble ---
mov eax, r9d
rol rax, 36
xor r10d, r10d
.chiffre:
mov edx, eax
and edx, 0xf
movzx edx, byte ptr [r11 + rdx]
mov byte ptr [r13 + r10], dl
rol rax, 4
inc r10d
cmp r10d, 8
jb .chiffre

; --- Le squelette constant (⑤) : la boucle des huit qwords, le NUL ---
movabs rax, 0x2020202020202020
lea r9, [r13 + 8]
mov ecx, 8
.squelette:
mov qword ptr [r9], rax
add r9, 8
loop .squelette
mov dword ptr [r13 + 72], eax
mov byte ptr [r13 + 76], 0

; --- Les huit groupes bas (⑥) : « HH » à 10 + 3·i, i < la longueur ---
lea r9, [r13 + 10]
xor r10d, r10d
.groupe_bas:
cmp r10d, r12d
jae .fin_bas
movzx eax, byte ptr [rbx + r10]
mov edx, eax
shr edx, 4
and eax, 0xf
movzx edx, byte ptr [r11 + rdx]
mov byte ptr [r9], dl
movzx edx, byte ptr [r11 + rax]
mov byte ptr [r9 + 1], dl
add r9, 3
.fin_bas:
inc r10d
cmp r10d, 8
jb .groupe_bas

; --- Les huit groupes hauts (⑥) : à 35 + 3·(i - 8), le médian posé ---
lea r9, [r13 + 35]
mov r10d, 8
.groupe_haut:
cmp r10d, r12d
jae .fin_haut
movzx eax, byte ptr [rbx + r10]
mov edx, eax
shr edx, 4
and eax, 0xf
movzx edx, byte ptr [r11 + rdx]
mov byte ptr [r9], dl
movzx edx, byte ptr [r11 + rax]
mov byte ptr [r9 + 1], dl
add r9, 3
.fin_haut:
inc r10d
cmp r10d, 16
jb .groupe_haut

; --- Le miroir ASCII (⑦) : la soustraction sur la COPIE, une seule borne ---
xor r10d, r10d
.miroir:
cmp r10d, r12d
jae .miroir_fin
movzx eax, byte ptr [rbx + r10]
mov edx, eax
sub edx, 0x20
cmp edx, 0x5e
jbe .poser
mov al, 0x2e
.poser:
mov byte ptr [r13 + r10 + 60], al
inc r10d
jmp .miroir
.miroir_fin:
xor eax, eax
.sortie:
pop r13
pop r12
pop rbx
ret
.refus:
mov eax, -5
ret
