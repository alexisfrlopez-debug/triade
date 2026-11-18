; Bloc LOUPE-16 SAISIE (Unité 04 D210)
; Conformité msx64, ABI x86-64 Win11 PE

; Prologue sauvegarde
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x20

; Initialisation des pointeurs locaux
lea rbx, [rip + CADRE]
lea r13, [rip + SAISIE]
lea rdx, [rip + JOURNAL]
lea rax, [rip + METRIQUES]
lea r10, [rip + L_SESSION]

; Contrat 1 : E1 - Poignée invalide
mov r11, qword ptr [rbx + 0x328] ; CADRE.poignée
cmp r11, -1
jne .contrat_q5
lea rsi, [rip + L_SESSION]
call .message
push -4
pop rax
jmp .sortie_verdict_negatif

.contrat_q5:
; Contrat 2 : Q5 - Touche VK_SUPPR (0x08)
cmp r8d, 0x08
jne .contrat_e4
mov r11d, dword ptr [r13 + 0x4] ; SAISIE.actif
test r11d, r11d
jz .sortie_succes
mov dword ptr [r13 + 0x4], 0 ; SAISIE.actif = 0
mov dword ptr [r13 + 0x8], 0 ; SAISIE.nibble = 0
jmp .sortie_succes

.contrat_e4:
; Contrat 3 : E4 - Classement du caractère
mov r11d, r8d
cmp r11d, 'a'
jb .contrat_q1
cmp r11d, 'f'
jbe .classe_majuscule
cmp r11d, '0'
jb .contrat_q1
cmp r11d, '9'
ja .contrat_q1
sub r11d, '0'
jmp .contrat_q1_valide

.classe_majuscule:
sub r11d, 0x20
cmp r11d, 'A'
jb .contrat_q1
cmp r11d, 'F'
ja .contrat_q1
sub r11d, '7'

.contrat_q1_valide:
; Contrat 4 : Q1 - Premier chiffre
mov dword ptr [r13 + 0x8], r11d ; SAISIE.nibble = valeur
mov dword ptr [r13 + 0x4], 1 ; SAISIE.actif = 1
jmp .sortie_succes

.contrat_q1:
; Caractère ignoré
jmp .sortie_succes

.contrat_q2:
; Contrat 5 : Q2 - Deuxième chiffre (r10d contient le premier)
mov dword ptr [r13 + 0x4], 0 ; SAISIE.actif = 0 (consommé)
mov dword ptr [r13 + 0x8], 0 ; SAISIE.nibble = 0 (consommé)
mov r11d, dword ptr [r13 + 0x8] ; SAISIE.nibble (sera 0, mais logique Q2)
shl r10d, 4
or r10d, r11d ; r10d = octet composé
jmp .contrat_e2

.contrat_e2:
; Contrat 6 : E2 - Curseur hors de la fenêtre
mov r11d, dword ptr [rbx + 0x220] ; CADRE.remplissage
mov r12, qword ptr [rbx + 0x210] ; CADRE.vue
add r12, r11d
mov r14, qword ptr [rbx + 0x218] ; CADRE.curseur
cmp r14, r12
jb .contrat_q7
lea rsi, [rip + L_HORSBORNES]
call .message
push -3
pop rax
jmp .sortie_verdict_negatif

.contrat_q7:
; Contrat 7 : Q7 - Journalisation
mov r11d, dword ptr [rdx + 0x1000] ; JOURNAL.nombre
test r11d, r11d
jz .ajout_entree ; Cas particulier : 0 entrées
xor r15, r15 ; Boucle sur les entrées
.boucle_journal:
mov r12, qword ptr [rdx + r15*8] ; JOURNAL[i].decalage
cmp r12, r14 ; JOURNAL[i].decalage == curseur ?
je .remplacement_entree
inc r15
cmp r15d, r11d
jb .boucle_journal

; Entrée non trouvée
cmp r11d, 256
jge .contrat_e3 ; Journal plein
jmp .ajout_entree

.remplacement_entree:
mov byte ptr [rdx + r15*8 + 8], r10b ; JOURNAL[i].octet = r10b
jmp .contrat_q3

.ajout_entree:
mov qword ptr [rdx + r11*8], r14 ; JOURNAL[nombre].decalage = curseur
mov byte ptr [rdx + r11*8 + 8], r10b ; JOURNAL[nombre].octet = r10b
inc dword ptr [rdx + 0x1000] ; JOURNAL.nombre++

.contrat_q3:
; Contrat 8 : Q3 - Écriture dans le tampon
mov r11, qword ptr [rbx + 0x210] ; CADRE.vue
mov r12, qword ptr [rbx + 0x218] ; CADRE.curseur
sub r12, r11
mov byte ptr [rbx + r12 + 0x258], r10b ; CADRE.tampon[curseur-vue]

.contrat_q4:
; Contrat 9 : Q4 - Marquage et curseur
mov dword ptr [rbx + 0x23C], 1 ; CADRE.sale = 1
mov dword ptr [rbx + 0x240], 0 ; CADRE.refus_quitter = 0
mov r11, qword ptr [rbx + 0x208] ; CADRE.taille
dec r11
mov r12, qword ptr [rbx + 0x218] ; CADRE.curseur
inc r12
cmp r12, r11
cmova r12, r11
mov qword ptr [rbx + 0x218], r12 ; CADRE.curseur = curseur_clampé

.contrat_vue:
; Contrat 10 : LA VUE SUIT
mov r11d, dword ptr [rax + 0x8] ; METRIQUES.lignes
mov r12d, r11d
sub r12d, 3
cmp r12d, 0
jge .vue_suite_1
mov r12d, 0
.vue_suite_1:
cmp r12d, 24
jle .vue_suite_2
mov r12d, 24
.vue_suite_2:
; r12d = V (nouvelle vue candidate)
mov r13d, r12d
shl r13d, 4 ; V16 = V * 16
mov r14, qword ptr [rbx + 0x210] ; CADRE.vue (ancienne)
mov r15, qword ptr [rbx + 0x218] ; CADRE.curseur
add r14, r13d
cmp r15, r14
jb .vue_invariante ; curseur dans [vue, vue+V16)

; Calcul de la nouvelle vue
lea r11, [r15 - 0xB0] ; curseur - 176
and r11, -16 ; aligne16_inf
mov r13, qword ptr [rbx + 0x208] ; CADRE.taille
sub r13, 384
cmp r13, 0
jge .vue_suite_3
mov r13, 0
.vue_suite_3:
and r13, -16 ; aligne16_sup
cmp r11, r13
cmova r11, r13 ; nouvelle vue clampée
cmp r11, qword ptr [rbx + 0x210] ; diffère de l'ancienne ?
je .vue_invariante
mov rcx, r11
call LOUPE02
test eax, eax
jnz .sortie_verdict_negatif ; échec de LOUPE02, on sort sans écrire
mov qword ptr [rbx + 0x210], r11 ; MAJ de la vue

.vue_invariante:

.contrat_feuille:
; Contrat 11 : La feuille INVALIDATERECT
mov rcx, qword ptr [rbx + 0x208] ; CADRE.poignée (HWND)
mov rdx, 0
mov r8d, 1
call qword ptr [rip + IAT_INVALIDATERECT]

.sortie_succes:
xor eax, eax ; rax = 0

.sortie_verdict_negatif:
; Épilogue restauration
add rsp, 0x20
pop r15
pop r14
pop r13
pop r12
pop rbx
ret

.message:
; Sous-routine .message : copie une étiquette dans la barre
xor rax, rax
.message_loop:
mov dil, byte ptr [rsi + rax]
test dil, dil
jz .message_fin
mov byte ptr [r13 + 0xC + rax], dil ; SAISIE.barre[rax]
inc rax
jmp .message_loop
.message_fin:
mov byte ptr [r13 + 0xC + rax], 0 ; SAISIE.barre[NUL] = 0
mov dword ptr [r13 + 0x0], 3 ; SAISIE.mode = 3
ret

; Données du plan (références symboliques)
CADRE:
SAISIE:
JOURNAL:
METRIQUES:
L_SESSION:
L_HORSBORNES:
L_JOURNALPLEIN:
IAT_INVALIDATERECT: