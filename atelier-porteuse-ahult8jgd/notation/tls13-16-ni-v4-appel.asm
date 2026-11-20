; tls13-16-ni-v4-appel · LA PORTEUSE NUE À APPEL : le verdict CPUID REMONTÉ À
; L'APPELANT (une fois par SESSION, plus jamais par flot — la mesure v3 a nommé
; l'éléphant : le cpuid au bac virtualisé coûte ~2 500 cycles PAR FLOT, 42
; cycles/bloc à N=64) ; le flux EXIGE aes — L'ARRÊT DE LA CARTE (le scellé
; tls13-16 EST aesenc, I3 : la carte n'a JAMAIS eu de chemin GPR) ; l'appelant
; qui ne sonde pas prend sa responsabilité — le contrat AES-REQUIS, miroir du
; bloc scellé ; LE REPLI SUPPRIMÉ (le vestige du v2 : il appelait le scellé
; aesenc — le chemin mort nommé au rapport)
; LE MÉCANISME MESURÉ : le pointeur avance PAR LE MODE D'ADRESSAGE [r13 +
; rbp*8] (rbp compte en QUADS, 2 par bloc — aucun add, aucune table : la
; mesure v3 a montré la pose de table à 1,84 c/bloc SANS gain marginal — le
; moteur hors-ordre recouvrait déjà la chaîne add→mov→call) ; LE DÉROULAGE
; k=4 : quatre appels par itération, le compteur et le saut amortis
; ABI msx64 (rcx = clés, rdx = entrées, r8 = sorties, r9 = N blocs) — le
; contrat du flux v2 INTACT (N quelconque, aucune borne) ; l'état aux
; NON-VOLATILS rbx/rbp/r12-r15 — LE DÉCALAGE QUAD EN rbp : la leçon des
; porteurs REPRIS (l'indice NE VIT JAMAIS dans un volatil — l'appelé clobber
; rax : la première v4-appel paya la faute, 5/64 à la différentielle, l'écart
; nommé au registre) ; le reste N mod 4 à la boucle k=1 de tête
; Copie de laboratoire à la marge VIERGE 0xDC00 — le scellé (slot 0xDF00)
; INTACT ; appels : 0xCE00 (corps NI pur, labo v2)
push rbx
push rbp
push r12
push r13
push r14
push r15
sub rsp, 0x28
test r9, r9
jz .fin
mov r12, rcx
mov r13, rdx
mov r14, r8
mov r15, r9
mov rbx, r15
and rbx, 3
xor ebp, ebp
test rbx, rbx
jz .prep4
.boucle_reste:
mov rcx, r12
lea rdx, [r13 + rbp*8]
lea r8, [r14 + rbp*8]
call 0xce00
lea rbp, [rbp + 2]
dec rbx
jnz .boucle_reste
.prep4:
mov rbx, r15
shr rbx, 2
test rbx, rbx
jz .fin
.boucle_ni:
mov rcx, r12
lea rdx, [r13 + rbp*8]
lea r8, [r14 + rbp*8]
call 0xce00
mov rcx, r12
lea rdx, [r13 + rbp*8 + 16]
lea r8, [r14 + rbp*8 + 16]
call 0xce00
mov rcx, r12
lea rdx, [r13 + rbp*8 + 32]
lea r8, [r14 + rbp*8 + 32]
call 0xce00
mov rcx, r12
lea rdx, [r13 + rbp*8 + 48]
lea r8, [r14 + rbp*8 + 48]
call 0xce00
lea rbp, [rbp + 8]
dec rbx
jnz .boucle_ni
.fin:
xor eax, eax
add rsp, 0x28
pop r15
pop r14
pop r13
pop r12
pop rbp
pop rbx
ret
