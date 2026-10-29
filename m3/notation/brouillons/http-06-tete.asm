; http-06-tete · brouillon · détection de fin de tête · http-06:R1 · e50006
; feuille pure : aucun appel, aucun IAT, aucun état, aucune écriture (I1) ;
; un seul balayage linéaire (I2) — le terminateur est la paire CRLF CRLF,
; tout LF isolé est tranché au premier (Q4) ; propriétaire de MAX_TETE (I3).
; entrée : rcx = tampon, rdx = remplissage utile
; sortie : rax = 0 complet (rdx = longueur de tête, CRLFCRLF compris) / 1
;          incomplet / 2 limite dépassée (> 8192 sans terminateur) / 3 LF isolé
xor eax, eax
.boucle:
cmp rax, rdx
jae .fin_boucle
cmp byte ptr [rcx + rax], 0x0A
je .lf
add rax, 1
jmp .boucle
.lf:
test rax, rax
je .isole
cmp byte ptr [rcx + rax - 1], 0x0D
jne .isole
; premier CRLF complet : second ?
lea r9, [rax + 1]
cmp r9, rdx
jae .suite
cmp byte ptr [rcx + rax + 1], 0x0D
jne .suite
lea r9, [rax + 2]
cmp r9, rdx
jae .suite
cmp byte ptr [rcx + rax + 2], 0x0A
jne .suite
lea r9, [rax + 3]
cmp r9, 0x2000
ja .excessive
lea rdx, [rax + 3]
xor eax, eax
ret
.excessive:
mov eax, 2
ret
.suite:
add rax, 1
jmp .boucle
.isole:
mov eax, 3
ret
.fin_boucle:
cmp rdx, 0x2000
jbe .incomplet
mov eax, 2
ret
.incomplet:
mov eax, 1
ret
