; http-01-ligne · brouillon · itérateur de ligne CRLF · http-01:R1 · e50001
; LE propriétaire du balayage de ligne (T5) : feuille pure, lecture seule,
; aucun registre non volatil touché, aucune écriture mémoire (I1-I4).
; entrée : rcx = tampon, rdx = longueur utile, r8 = curseur [0, longueur]
; sortie : rax = 0 trouvé (rdx = longueur sans CRLF, r8 = après CRLF) / 1 incomplet
mov rax, r8
jmp .test
.boucle:
add rax, 1
.test:
cmp rax, rdx
jae .incomplet
cmp byte ptr [rcx + rax], 0x0D
jne .boucle
lea r9, [rax + 1]
cmp r9, rdx
jae .incomplet
cmp byte ptr [rcx + r9], 0x0A
jne .boucle
lea r9, [rax + 2]
sub rax, r8
mov rdx, rax
mov r8, r9
xor eax, eax
ret
.incomplet:
mov eax, 1
ret
