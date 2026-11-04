; libc-04-itoa-r3 · brouillon étiqueté — spec libc-04:R3, bloc carte f61006
; valeur/tampon nommés (frag-con : SysV — edi/rsi ; msx64 — ecx/rdx).
; Génération en place au sens R2/R3 : chiffres produits en ordre inverse
; depuis la fin (offset 11, le NUL d'abord), puis compactés vers l'avant —
; l'espace de travail au-delà du NUL n'est pas spécifié (Q4), la borne
; dure est le tampon de douze octets. Le curseur vit en r8, le diviseur
; en r9d, le compteur de compactage en rcx : TOUT volatil (I3 — l'instance
; Windows travaillait en rbx sauvegardé ; l'instance SysV n'a pas besoin
; de toucher un seul non volatil, l'observable « aucun non volatil modifié
; à la sortie » est le même). Division par 10 explicite (D21 — pas de
; magie multiplicative).
mov r8, rsi
add r8, 11
mov byte ptr [r8], 0
mov eax, edi
mov r9d, 10
.genere:
xor edx, edx
div r9d
add dl, 48
dec r8
mov byte ptr [r8], dl
test eax, eax
jne .genere
xor ecx, ecx
.compacte:
mov al, byte ptr [r8 + rcx]
mov byte ptr [rsi + rcx], al
test al, al
je .fin
inc rcx
jmp .compacte
.fin:
mov rax, rsi
ret
