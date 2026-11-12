; shani-03-absorber · brouillon étiqueté — spec shani-03:R1, bloc préfiguré g210003
; L'ABSORPTION TAMPONNÉE À DISPATCH — le miroir de tls13-03 (le contrat à la
; lettre, R4 : rcx = le contexte, rdx = les données, r8 = N ; l'invariance
; de découpage, le chemin PLEIN sur l'ÉGALITÉ STRICTE — journal 20 de la
; lignée : jbe laissait remplissage=64 sans compression) avec LA SEULE
; DIFFÉRENCE : la compression SÉLECTIONNÉE au geste.
;   - LA SONDE UNE FOIS PAR APPEL (R11 : le hot path est la compression,
;     pas le choix du chemin — le sondage par bloc mangerait le gain) :
;     call SHANI01, le verdict tenu en r15 SAUVÉ (non volatil) ;
;   - LES DEUX SITES D'APPEL DIRECTS ET STATIQUES (I1, la liste fermée) :
;     le chemin matériel call SHANI02, le repli call TLS02 LE SCELLÉ à
;     0xC080 (R7 — les adresses scellées intactes).
; 8 pushes (64 o) + sub 0x28 : entrée ≡ 8 → 8−64−40 ≡ 0 (mod 16) aux
; points d'appel ; le 0x28 porte L'OMBRE msx64 0x20 des trois appels.
push rbx
push r12
push r13
push r14
push r15
push rdi
push rsi
push rbp
sub rsp, 0x28
mov rbx, rcx
mov r12, rdx
mov r13, r8
call SHANI01
mov r15d, eax
.boucle:
test r13, r13
je .fin
mov r14d, dword ptr [rbx + 96]
mov ebp, 64
sub ebp, r14d
cmp r13, rbp
jb .court
lea rdi, [rbx + r14 + 32]
mov rsi, r12
mov rcx, rbp
rep movsb
add dword ptr [rbx + 96], ebp
add qword ptr [rbx + 104], rbp
sub r13, rbp
add r12, rbp
mov rcx, rbx
lea rdx, [rbx + 32]
test r15, r15
jz .scalaire
call SHANI02
jmp .apres
.scalaire:
call TLS02
.apres:
mov dword ptr [rbx + 96], 0
jmp .boucle
.court:
lea rdi, [rbx + r14 + 32]
mov rsi, r12
mov rcx, r13
rep movsb
add dword ptr [rbx + 96], r13d
add qword ptr [rbx + 104], r13
xor r13d, r13d
jmp .boucle
.fin:
xor eax, eax
add rsp, 0x28
pop rbp
pop rsi
pop rdi
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
