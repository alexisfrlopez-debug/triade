; tcp-07-patch · brouillon · moteur de patch à chaud · (rcx mode) -> rax code · tcp-07:R3 · c30007
; mode 0 : vérifier somme staging -> protéger RWX (D39 : jamais RW — la page contient
; ce bloc lui-même, DEP permanent en x64) -> sauver entrée -> copier en croissance ->
; basculer par UN qword aligné (E9 rel32 + NOP x3) -> restaurer RX
; D41 : .protger réserve 0x28 avant l'appel IAT (0x20 zone d'accueil ABI msx64
; — le code système /homeparams y range rcx/rdx/r8/r9 — + 0x8 alignement) ; la loge
; old-protect vit à [rsp+0x20], hors zone d'accueil, jamais sous rsp
; mode 1 : protéger RWX -> réécrire le qword original sauvegardé -> restaurer RX
; codes : 0 ok · 1 mode · 2 staging absent · 3 intégrité · 4 état · 5 protection
; r15 = entrée echo (calculée une fois) ; .protger = bascule locale de protection
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x40
cmp ecx, 1
ja .mode_invalide
mov rax, qword ptr [rip + ETAT_PATCH]
lea r15, [rip + ECHO]
test ecx, ecx
jne .rollback
cmp rax, 1
je .incoherent
mov r12d, dword ptr [rip + TAB_TAILLE]
test r12d, r12d
je .rien
lea rbx, [rip + STAGING]
xor eax, eax
xor ecx, ecx
.somme:
add rax, qword ptr [rbx + rcx]
add rcx, 8
cmp rcx, r12
jb .somme
mov r13, qword ptr [rip + TAB_SOMME]
cmp rax, r13
jne .integrite
mov r8d, 0x40
call .protger
test eax, eax
je .protection
mov rax, qword ptr [r15]
mov qword ptr [rip + ENTREE_SAUVEE], rax
lea rcx, [rip + CROISSANCE]
lea rdx, [rip + STAGING]
mov r8, r12
call MEMCPY
lea rax, [rip + CROISSANCE]
sub rax, r15
sub rax, 5
mov r11d, 0x909090
shl r11, 40
shl rax, 8
or r11, rax
or r11, 0xE9
mov qword ptr [r15], r11
mov r8d, 0x20
call .protger
mov qword ptr [rip + ETAT_PATCH], 1
test eax, eax
je .protection_tardive
xor eax, eax
jmp .fin
.protection_tardive:
mov eax, 5
jmp .fin
.rollback:
test rax, rax
je .incoherent
mov r8d, 0x40
call .protger
test eax, eax
je .protection
mov rdx, qword ptr [rip + ENTREE_SAUVEE]
mov qword ptr [r15], rdx
mov r8d, 0x20
call .protger
mov qword ptr [rip + ETAT_PATCH], 0
test eax, eax
je .protection_tardive
xor eax, eax
jmp .fin
.protger:
sub rsp, 0x28
mov rcx, r15
and rcx, 0xfffffffffffff000
mov rdx, 0x700
lea r9, [rsp + 0x20]
call qword ptr [rip + IAT_VPROTECT]
add rsp, 0x28
ret
.mode_invalide:
mov eax, 1
jmp .fin
.rien:
mov eax, 2
jmp .fin
.integrite:
mov eax, 3
jmp .fin
.incoherent:
mov eax, 4
jmp .fin
.protection:
mov eax, 5
.fin:
add rsp, 0x40
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
