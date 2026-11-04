; tcp-07-patch-r4 · brouillon étiqueté — spec tcp-07:R4, bloc carte f61012
; LE MOTEUR DU PATRIMOINE M2 (scellé 0.3.0), instance Linux du mécanisme :
; mode nommé (frag-con : SysV — edi ; Windows — ecx). La CIBLE est
; l'ENTRÉE DU JOURNAL v1 (0x1840 — le plan du corpus, tcp-07:R4 P5 : la
; démonstration M5-(c) du chantier (d)), la croissance 0x1D80, le staging
; .rodata 0x300 (le journal v2 assemblé POUR la croissance), la table
; d'intégrité 0x540 (rva, taille, somme — la 1re entrée EST le staging :
; taille 0 = absent, la somme des qwords est la porte R10 AVANT tout
; effet). L'état (0x3808) et l'original (0x3810) vivent au plan.
; LE SERVICE DE PROTECTION DU PROFIL (I1, frag-con) : l'instance Windows
; appelait l'IAT kernel32 VirtualProtect (deux fois, avec la zone
; d'accueil 0x28 — D41) ; l'instance Linux appelle mprotect direct
; (syscall 10, rdi/rsi/rdx, AUCUNE zone d'accueil — le syscall ne range
; rien chez l'appelant, il ne détruit que rcx/r11) via le sous-programme
; local .protger (déclaré I1, le miroir de .protger Windows sans l'obligation
; ABI d'accueil). Les constantes du profil (I6, D39) : la phase d'écriture
; passe par RWX 0x7 — le bit exécution RETENU, la page contient le présent
; bloc — puis la restauration RX 0x5 ; JAMAIS 0x3 (le défaut terrain
; démo.4, le DEP permanent x64).
; La bascule : le qword E9 rel32 + NOP x3 construit en registre (I3),
; posé en UNE écriture alignée (Q3, atomicité x86-64) ; le rollback
; réécrit l'original sauvegardé ; la croissance n'est jamais effacée (Q2).
; Cadre : 5 push, AUCUN sub — l'entrée ≡ 8 mod 16, quarante octets de
; pushes laissent ≡ 0 : tout appel part aligné, rien ne vit sous rsp (I5).
@A_MEMCPY = 0x1080
@SYS_MPROTECT = 10
@PROT_RWX = 0x7
@PROT_RX = 0x5
@ENTREE_JOURNAL = 0x1840
@CROISSANCE = 0x1D80
@STAGING = 0x300
@TAB_SUM = 0x540
@ETAT = 0x3808
@ENTREE_SAUVEE = 0x3810
push rbx
push r12
push r13
push r14
push r15
; --- valider le mode (P1 : 0 appliquer, 1 retour — tout autre refusé) ---
cmp edi, 1
ja .refus1
lea r8, [rip + @ETAT]
mov rax, qword ptr [r8]
lea r15, [rip + @ENTREE_JOURNAL]
test edi, edi
jne .retour
; --- mode 0 : appliquer (état doit être v1 — Q5 code 4 sinon) ---
cmp rax, 1
je .refus4
; la porte R10 : staging présent (taille) puis somme des qwords
lea rbx, [rip + @TAB_SUM]
mov r12d, dword ptr [rbx + 4]
test r12d, r12d
je .refus2
lea r11, [rip + @STAGING]
xor eax, eax
xor ecx, ecx
.somme:
add rax, qword ptr [r11 + rcx]
add rcx, 8
cmp rcx, r12
jb .somme
mov r13, qword ptr [rbx + 8]
cmp rax, r13
jne .refus3
; ouvrir la page en écriture (D39 : RWX, le bit exécution retenu)
mov edi, @PROT_RWX
call .protger
test eax, eax
js .refus5
; sauver l'original des 8 octets de l'entrée
mov rax, qword ptr [r15]
lea rdx, [rip + @ENTREE_SAUVEE]
mov qword ptr [rdx], rax
; copier le staging -> croissance (octet pour octet, Q1)
lea rdi, [rip + @CROISSANCE]
lea rsi, [rip + @STAGING]
mov rdx, r12
call @A_MEMCPY
; le trampoline : E9 rel32 + NOP x3, UN qword aligné (Q3/I3)
lea rax, [rip + @CROISSANCE]
sub rax, r15
sub rax, 5
mov r11d, 0x909090
shl r11, 40
shl rax, 8
or r11, rax
or r11, 0xE9
mov qword ptr [r15], r11
; refermer la page (RX), l'état bascule, le verdict de restauration tranche
mov edi, @PROT_RX
call .protger
mov qword ptr [r8], 1
test eax, eax
js .restauration_echouee
xor eax, eax
jmp .fin
; --- mode 1 : retour arrière (état doit être v2 — Q5 code 4 sinon) ---
.retour:
test rax, rax
je .refus4
mov edi, @PROT_RWX
call .protger
test eax, eax
js .refus5
lea rdx, [rip + @ENTREE_SAUVEE]
mov rdx, qword ptr [rdx]
mov qword ptr [r15], rdx
mov edi, @PROT_RX
call .protger
mov qword ptr [r8], 0
test eax, eax
js .restauration_echouee
xor eax, eax
jmp .fin
; --- le sous-programme local : mprotect(page de la cible, 0x1000, prot) ---
; edi = la constante du profil (0x7 ou 0x5) ; r15 = la cible (non volatil,
; traversant) ; la page par masque du bas ; le verdict est le rax BRUT du
; noyau (0 succès, négatif = -errno, jamais transformé).
.protger:
mov rdx, rdi
mov rdi, r15
and rdi, -4096
mov esi, 0x1000
mov eax, @SYS_MPROTECT
syscall
ret
; --- les refus nommés (Q5 : AUCUN octet écrit, état inchangé) ---
.refus1:
mov eax, 1
jmp .fin
.refus2:
mov eax, 2
jmp .fin
.refus3:
mov eax, 3
jmp .fin
.refus4:
mov eax, 4
jmp .fin
.refus5:
mov eax, 5
jmp .fin
.restauration_echouee:
mov eax, 5
.fin:
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
