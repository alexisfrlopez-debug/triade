; loupe-17-sauver · bloc la sauvegarde : l'écriture à l'octet, le panneau re-né, le témoin · spec loupe-17:R1 · bloc carte i110017
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x6500, taille 576 octets
; Domaine : loupe (M10, le TGN « Loupe ») · Dépendances : LE JOURNAL VIDE (Q1 : « rien à sauver », AUCUN appel — les appels comptés) ; SINON (Q2 : CHAQUE entrée DANS SON ORDRE DE SAISIE — SetFilePointerEx(décalage, DEBUT_FICHIER) puis WriteFile d'UN octet : L'ÉCRITURE À L'OCTET, jamais une plage ; le pointeur d'écrits NUL — la poignée synchrone ; l'échec -6 FAIL-CLOSED : le journal DEMEURE, la marque demeure, les octets déjà écrits le restent — le geste se reprend) ; LE SUCCÈS (Q3 : journal vidé, marque levée, garde levée) ; LE PANNEAU RE-NAÎT (Q4 : loupe-07 rappelé — les empreintes du DISQUE, le coût NOMMÉ : un passage de plus) ; LE TÉMOIN (Q5 : « N o écrits · 0xA..0xB » à la barre — le compte exact, la première et la dernière adresses écrites, composés AVANT la vidange [dec + hex8, les sous-routines locales au cadre RBP, le modèle loupe-10]) ; la taille DEMEURE (Q6 : l'oracle le constate) ; E1 -4 nommé ; IAT kernel32 : SetFilePointerEx, WriteFile, GetLastError ; IAT user32 : InvalidateRect (WriteFile vit ICI SEUL dans le domaine — I3 : la contrebande d'écriture est un refus de build)
; Notation explicite générée par outils/auteur.py depuis brouillons/loupe-17-sauver.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 521 o · padding : 55 o (NOP, 0x90)
; Étiquettes résolues : .session=0x6542, .sauver=0x655f, .boucle=0x6565, .refus_systeme=0x664f, .sortie_relaye=0x665c, .sortie=0x665c, .message=0x666b, .message_copie=0x6676, .message_fin=0x6686, .chaine=0x6694, .chaine_fin=0x66a4, .dec=0x66a5, .dec_boucle=0x66b2, .dec_copie=0x66c7, .hex8=0x66d8, .hex8_boucle=0x66e8
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x6514 + 0x7 + 0x7ae5 = 0xe000
;   0x651b + 0x7 + 0x7f7e = 0xe4a0
;   0x652c + 0x7 - 0x4198 = 0x239b
;   0x654c + 0x7 - 0x401c = 0x2537
;   0x6575 + 0x6 - 0x4153 = 0x2428
;   0x65a0 + 0x6 - 0x416e = 0x2438
;   0x65be + 0x7 + 0x7e3b = 0xe400
;   0x65d1 + 0x7 - 0x4093 = 0x2545
;   0x65e6 + 0x7 - 0x4099 = 0x2554
;   0x65fe + 0x7 + 0x7dfb = 0xe400
;   0x662a + 0x7 + 0x7d8f = 0xe3c0
;   0x6645 + 0x6 - 0x41b3 = 0x2498
;   0x664f + 0x6 - 0x420d = 0x2448
;   0x666b + 0x7 + 0x7d8e = 0xe400
;   0x6686 + 0x7 + 0x7d73 = 0xe400
;   0x66d8 + 0x7 - 0x468f = 0x2050
; Appels directs (l'adresse du plan — I1) : call 0x666b, call 0x666b, call qword ptr [rip - 0x4153], call qword ptr [rip - 0x416e], call 0x66a5, call 0x6694, call 0x66d8, call 0x6694, call 0x66d8, call 0x4940, call qword ptr [rip - 0x41b3], call qword ptr [rip - 0x420d]
push rbx
push r12
push r13
push r14
push r15
push rbp
mov rbp, rsp
sub rsp, 0x28
mov r12, rcx
lea rbx, [rip + 0x7ae5]
lea r13, [rip + 0x7f7e]
cmp qword ptr [rbx + 528], -1
jne 0x6542
lea rsi, [rip - 0x4198]
call 0x666b
mov eax, -4
jmp 0x665c
cmp dword ptr [r13 + 4096], 0
jne 0x655f
lea rsi, [rip - 0x401c]
call 0x666b
xor eax, eax
jmp 0x665c
mov r14, r13
xor r15d, r15d
mov rcx, qword ptr [rbx + 528]
mov rdx, qword ptr [r14]
xor r8d, r8d
xor r9d, r9d
call qword ptr [rip - 0x4153]
test eax, eax
jz 0x664f
mov rcx, qword ptr [rbx + 528]
lea rdx, [r14 + 8]
mov r8d, 1
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call qword ptr [rip - 0x416e]
test eax, eax
jz 0x664f
inc r15d
add r14, 16
cmp r15d, dword ptr [r13 + 4096]
jb 0x6565
lea rdi, [rip + 0x7e3b]
add rdi, 12
mov eax, r15d
call 0x66a5
lea rsi, [rip - 0x4093]
call 0x6694
mov rax, qword ptr [r13]
call 0x66d8
lea rsi, [rip - 0x4099]
call 0x6694
mov rax, qword ptr [r14 - 16]
call 0x66d8
mov byte ptr [rdi], 0
lea rax, [rip + 0x7dfb]
mov dword ptr [rax], 3
mov dword ptr [r13 + 4096], 0
mov dword ptr [rbx + 556], 0
mov dword ptr [rbx + 560], 0
lea rcx, [rip + 0x7d8f]
call 0x4940
test eax, eax
jnz 0x665c
mov rcx, r12
xor edx, edx
mov r8d, 1
call qword ptr [rip - 0x41b3]
xor eax, eax
jmp 0x665c
call qword ptr [rip - 0x420d]
mov eax, -6
jmp 0x665c
add rsp, 0x28
pop rbp
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
lea rdi, [rip + 0x7d8e]
add rdi, 12
mov al, byte ptr [rsi]
mov byte ptr [rdi], al
test al, al
jz 0x6686
inc rsi
inc rdi
jmp 0x6676
lea rax, [rip + 0x7d73]
mov dword ptr [rax], 3
ret
mov al, byte ptr [rsi]
mov byte ptr [rdi], al
test al, al
jz 0x66a4
inc rsi
inc rdi
jmp 0x6694
ret
lea r9, [rbp - 8]
xor r11d, r11d
mov r10d, 10
xor edx, edx
div r10
add dl, 0x30
dec r9
mov byte ptr [r9], dl
inc r11d
test eax, eax
jnz 0x66b2
mov al, byte ptr [r9]
mov byte ptr [rdi], al
inc r9
inc rdi
dec r11d
jnz 0x66c7
ret
lea r11, [rip - 0x468f]
mov r10, rax
mov r9d, 28
mov rax, r10
mov ecx, r9d
shr rax, cl
and eax, 0xf
movzx eax, byte ptr [r11 + rax]
mov byte ptr [rdi], al
inc rdi
sub r9d, 4
cmp r9d, 0
jge 0x66e8
ret
