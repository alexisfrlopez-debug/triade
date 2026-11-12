; shani-03-absorber · bloc absorption tamponnée à dispatch SHA-NI/scalaire · spec shani-03:R1 · bloc carte g210003 (PRÉFIGURÉ — la variante n'est PAS dans la carte : charte § 3, le scellage appartient au développeur)
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0xd400, taille 192 octets
; Domaine : shani (la variante SHA-NI, D205 — JAMAIS SCELLÉE) · Dépendances : shani-01 (la sonde — UNE fois par appel, I1) ; DEUX appels directs déclarés : shani-02 la variante, tls13-02 LE SCELLÉ à 0xC080 (le repli, R7) ; le miroir de tls13-03 (le chemin PLEIN sur l'ÉGALITÉ STRICTE)
; Notation explicite générée par outils/auteur.py depuis brouillons/shani-03-absorber.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 159 o · padding : 33 o (NOP, 0x90)
; Étiquettes résolues : .boucle=0xd421, .scalaire=0xd464, .apres=0xd469, .court=0xd472, .fin=0xd48c
; Appels directs (le plan, source unique — I1) : call 0xd000, call 0xd080, call 0xc080
; Sauts : je 0xd48c, jb 0xd472, jz 0xd464, jmp 0xd469, jmp 0xd421, jmp 0xd421
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
call 0xd000
mov r15d, eax
test r13, r13
je 0xd48c
mov r14d, dword ptr [rbx + 96]
mov ebp, 64
sub ebp, r14d
cmp r13, rbp
jb 0xd472
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
jz 0xd464
call 0xd080
jmp 0xd469
call 0xc080
mov dword ptr [rbx + 96], 0
jmp 0xd421
lea rdi, [rbx + r14 + 32]
mov rsi, r12
mov rcx, r13
rep movsb
add dword ptr [rbx + 96], r13d
add qword ptr [rbx + 104], r13
xor r13d, r13d
jmp 0xd421
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
