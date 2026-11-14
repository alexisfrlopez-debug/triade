; loupe-02 · lire : la fenêtre d'octets au tampon de session · brouillon auteur
; spec loupe-02:R1 — la fenêtre bornée + LE RECOUVREMENT du journal.
; choix : E1 la session d'abord (la poignée au cadre), E2 la grille (les quatre
;   bits bas du décalage), E3 la borne (la taille LUE AU CADRE, I1 — jamais
;   passée par l'appelant), PUIS la double borne du remplissage (min(384,
;   taille − décalage) par cmov), SetFilePointerEx (FILE_BEGIN, la position
;   reposée À CHAQUE lecture), ReadFile du remplissage EXACT au tampon, le lu
;   RECOUPÉ au demandé (fail-closed : le tampon ne montre JAMAIS un octet non
;   lu), le champ remplissage posé, PUIS le recouvrement du journal (Q2).
; le journal : le nombre vit à la zone (+4096) — loupe-16 l'arrête à
;   EDITS_MAX par construction (la zone EST 256 entrées, 4 112 o) ; le
;   recouvrement reste CONFINÉ au tampon par la double borne de la fenêtre.
; appelés : AUCUN bloc (lire ne déplace rien — Q3 ; le défilement est à
;   loupe-11). IAT : SetFilePointerEx, ReadFile, GetLastError (la liste
;   fermée, I4).
; garde fail-closed (E4) : SetFilePointerEx OU ReadFile en échec, OU lu !=
;   demandé → GetLastError CONSIGNÉ (l'appel — jamais le code brut exposé,
;   la table traduit), remplissage posé à 0, verdict -6.
; ABI : msx64. rbx/r12/r13/r14/r15 sauvegardés (utilisés), rsp aligné 16 aux
;   appels : cinq pushes + 0x30 de cadre (l'ombre 0x20 + le lu + la 5e
;   feuille de ReadFile à NULL). Les zones hors tampon JAMAIS touchées (I2).

; --- Prologue : le cadre, les non-volatils, l'ombre ---
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x30
lea rbx, [rip + CADRE] ; rbx = la base du cadre

; --- E1 : la session est-elle ouverte ? (P1 : la poignée ≠ INVALIDE) ---
cmp qword ptr [rbx + 528], -1
je .verdict_session

; --- E2 : le décalage est-il multiple de 16 ? (P2 : la grille droite) ---
mov r12, rcx ; r12 = le décalage de fenêtre
test cl, 0x0F
jnz .verdict_entree

; --- E3 : le décalage est-il dans le fichier ? (P3, I1 : la taille au cadre) ---
mov r15, qword ptr [rbx + 520] ; r15 = la taille LUE AU CADRE
cmp r12, r15
jae .verdict_hors_bornes

; --- Q1 : le remplissage = min(384, taille − décalage) — la double borne ---
mov r13d, 384
mov rax, r15
sub rax, r12 ; rax = taille − décalage (>= 1)
cmp rax, r13
cmovbe r13, rax ; r13 = le remplissage borné

; --- Q1 : la position reposée (SetFilePointerEx, FILE_BEGIN, À CHAQUE lecture) ---
mov r14, qword ptr [rbx + 528] ; r14 = la poignée de la session
mov rcx, r14
mov rdx, r12 ; le décalage
xor r8d, r8d ; lpNewFilePointer = NULL
xor r9d, r9d ; FILE_BEGIN = 0
call qword ptr [rip + IAT_SETFILEPOINTEREX]
test eax, eax
jz .erreur_systeme

; --- Q1 : la lecture du remplissage EXACT (ReadFile au tampon du cadre) ---
mov rcx, r14
lea rdx, [rbx + 568] ; le tampon du cadre (I2 : lui seul)
mov r8d, r13d ; le remplissage (<= 384)
lea r9, [rsp + 0x28] ; &lu (hors de l'ombre du callé)
mov qword ptr [rsp + 0x20], 0 ; lpOverlapped = NULL
call qword ptr [rip + IAT_READFILE]
test eax, eax
jz .erreur_systeme
mov r14d, dword ptr [rsp + 0x28] ; le lu
cmp r14, r13
jne .erreur_systeme ; fail-closed : jamais un octet non lu

; --- Q1 : le champ remplissage posé au cadre ---
mov dword ptr [rbx + 552], r13d

; --- Q2 : LE RECOUVREMENT du journal (l'édition survit au défilement) ---
lea r14, [rip + JOURNAL] ; la zone du journal (loupe-16)
mov r10d, dword ptr [r14 + 4096] ; le nombre d'entrées
test r10d, r10d
jz .succes ; le journal vide : rien à recouvrir
xor ecx, ecx ; i = 0
mov r11, r14 ; r11 = &entrée[i] (le pointeur qui marche)
.boucle_journal:
mov rax, qword ptr [r11] ; le décalage de l'entrée
cmp rax, r12
jb .entree_suivante ; avant la fenêtre : ignorée
lea rdx, [r12 + r13]
cmp rax, rdx
jae .entree_suivante ; après la fenêtre : ignorée
sub rax, r12 ; rax = l'indice dans le tampon (< remplissage)
movzx edx, byte ptr [r11 + 8] ; l'octet écrit
mov byte ptr [rbx + rax + 568], dl ; LE RECOUVREMENT
.entree_suivante:
add r11, 16 ; l'entrée suivante (JOUR_PAS)
inc rcx
cmp rcx, r10
jb .boucle_journal
jmp .succes ; la boucle finie : le recouvrement est fait

; --- E4 : l'échec système — le code CONSIGNÉ, remplissage 0 (fail-closed) ---
.erreur_systeme:
call qword ptr [rip + IAT_GETLASTERROR] ; le code consigné (jamais exposé brut)
xor edx, edx
mov dword ptr [rbx + 552], edx ; remplissage = 0 : rien de lu n'est montré
mov eax, -6
jmp .sortie

; --- E1 : sans session ouverte ---
.verdict_session:
mov eax, -4
jmp .sortie

; --- E2 : le décalage non aligné ---
.verdict_entree:
mov eax, -5
jmp .sortie

; --- E3 : le décalage hors du fichier ---
.verdict_hors_bornes:
mov eax, -3
jmp .sortie

; --- Q3 : le succès — rax = 0, la vue et le curseur INTACTS ---
.succes:
xor eax, eax

; --- Épilogue unique ---
.sortie:
add rsp, 0x30
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
