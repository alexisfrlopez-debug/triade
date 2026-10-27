; http-05-nombre · brouillon · décimal ASCII borné → u32 · http-05:R1 · e50005
; feuille pure : aucun appel, aucun IAT, aucun état, AUCUNE écriture mémoire
; (I1) ; l'accumulation est testée À CHAQUE chiffre (I2) : l'intermédiaire
; 64 bits ne peut pas déborder (≤ 10 chiffres ⇒ < 2^36), le test
; val*10 + d > 0xFFFFFFFF est l'équivalent exact de la borne de I2 — aucune
; troncature silencieuse n'existe (V4) ; edx inchangé sur tout verdict non nul.
; entrée : rcx = span, rdx = longueur
; sortie : rax = 0 (edx = valeur u32) / 1 vide / 2 > 10 chiffres / 3 non-chiffre
;          / 4 débordement / 5 zéros de tête
test rdx, rdx
je .vide
cmp rdx, 10
ja .trop_long
cmp byte ptr [rcx], 0x30
jne .pas_zero
cmp rdx, 1
jne .zero_tete
.pas_zero:
xor eax, eax
xor r9d, r9d
.boucle:
cmp r9, rdx
jae .ok
movzx r10d, byte ptr [rcx + r9]
sub r10, 0x30
cmp r10, 9
ja .non_chiffre
lea rax, [rax + rax*4]
add rax, rax
add rax, r10
movabs r11, 0xFFFFFFFF
cmp rax, r11
ja .debordement
add r9, 1
jmp .boucle
.ok:
mov edx, eax
xor eax, eax
ret
.vide:
mov eax, 1
ret
.trop_long:
mov eax, 2
ret
.non_chiffre:
mov eax, 3
ret
.debordement:
mov eax, 4
ret
.zero_tete:
mov eax, 5
ret
