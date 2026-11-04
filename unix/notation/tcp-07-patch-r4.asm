; tcp-07-patch-r4 · bloc moteur de patch à chaud (tcp-07:R4) · spec tcp-07:R4 · bloc carte f61012
; Profil : x86-64-linux-elf64 · ABI SysV · slot RVA 0x1a40, taille 512 octets
; Notation explicite générée par outils/auteur.py depuis brouillons/tcp-07-patch-r4.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 362 o · padding : 150 o (NOP)
; Étiquettes résolues : .fin=0x1ba0, .protger=0x1b5e, .refus1=0x1b78, .refus2=0x1b7f, .refus3=0x1b86, .refus4=0x1b8d, .refus5=0x1b94, .restauration_echouee=0x1b9b, .retour=0x1b25, .somme=0x1a94
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x1a52 + 0x7 + 0x1daf = 0x3808 (@ETAT)
;   0x1a5c + 0x7 - 0x223 = 0x1840 (@ENTREE_JOURNAL)
;   0x1a75 + 0x7 - 0x153c = 0x540 (@TAB_SUM)
;   0x1a89 + 0x7 - 0x1790 = 0x300 (@STAGING)
;   0x1ac3 + 0x7 + 0x1d46 = 0x3810 (@ENTREE_SAUVEE)
;   0x1acd + 0x7 + 0x2ac = 0x1d80 (@CROISSANCE)
;   0x1ad4 + 0x7 - 0x17db = 0x300 (@STAGING)
;   0x1ae3 + 0x7 + 0x296 = 0x1d80 (@CROISSANCE)
;   0x1b38 + 0x7 + 0x1cd1 = 0x3810 (@ENTREE_SAUVEE)
; Symboles (vérifiés par build_m6.py contre layout.py) : @A_MEMCPY=0x1080, @CROISSANCE=0x1d80, @ENTREE_JOURNAL=0x1840, @ENTREE_SAUVEE=0x3810, @ETAT=0x3808, @PROT_RWX=0x7, @PROT_RX=0x5, @STAGING=0x300, @SYS_MPROTECT=0xa, @TAB_SUM=0x540
push rbx
push r12
push r13
push r14
push r15
cmp edi, 1
ja 0x1b78
lea r8, [rip + 0x1daf]
mov rax, qword ptr [r8]
lea r15, [rip - 0x223]
test edi, edi
jne 0x1b25
cmp rax, 1
je 0x1b8d
lea rbx, [rip - 0x153c]
mov r12d, dword ptr [rbx + 4]
test r12d, r12d
je 0x1b7f
lea r11, [rip - 0x1790]
xor eax, eax
xor ecx, ecx
add rax, qword ptr [r11 + rcx]
add rcx, 8
cmp rcx, r12
jb 0x1a94
mov r13, qword ptr [rbx + 8]
cmp rax, r13
jne 0x1b86
mov edi, 7
call 0x1b5e
test eax, eax
js 0x1b94
mov rax, qword ptr [r15]
lea rdx, [rip + 0x1d46]
mov qword ptr [rdx], rax
lea rdi, [rip + 0x2ac]
lea rsi, [rip - 0x17db]
mov rdx, r12
call 0x1080
lea rax, [rip + 0x296]
sub rax, r15
sub rax, 5
mov r11d, 0x909090
shl r11, 0x28
shl rax, 8
or r11, rax
or r11, 0xe9
mov qword ptr [r15], r11
mov edi, 5
call 0x1b5e
mov qword ptr [r8], 1
test eax, eax
js 0x1b9b
xor eax, eax
jmp 0x1ba0
test rax, rax
je 0x1b8d
mov edi, 7
call 0x1b5e
test eax, eax
js 0x1b94
lea rdx, [rip + 0x1cd1]
mov rdx, qword ptr [rdx]
mov qword ptr [r15], rdx
mov edi, 5
call 0x1b5e
mov qword ptr [r8], 0
test eax, eax
js 0x1b9b
xor eax, eax
jmp 0x1ba0
mov rdx, rdi
mov rdi, r15
and rdi, 0xfffffffffffff000
mov esi, 0x1000
mov eax, 0xa
syscall
ret
mov eax, 1
jmp 0x1ba0
mov eax, 2
jmp 0x1ba0
mov eax, 3
jmp 0x1ba0
mov eax, 4
jmp 0x1ba0
mov eax, 5
jmp 0x1ba0
mov eax, 5
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
