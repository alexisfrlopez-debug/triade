; loupe-16 · saisie : l'octet écrit au journal, la marque sale posée · spec loupe-16:R1
; LA CLASSE (E4) : les SEIZE chiffres hexa écoutent (les minuscules portées
; aux MAJUSCULES — la convention de la saisie), TOUT autre caractère IGNORÉ
; proprement (rax = 0, rien — le repli documenté) ; VK_SUPPR (Q5) : pendant
; l'attente le nibble est EFFACÉ (le premier chiffre repart — l'attente
; annulée proprement), hors attente il est ignoré (l'échappée vit à la
; barre-saisie de loupe-12, le nibble ne connaît que le chiffre et VK_SUPPR).
; LE PREMIER CHIFFRE (Q1) : l'attente posée à la zone SAISIE du plan —
; actif = 1, nibble = la valeur 0..15 (RIEN n'est écrit : un demi-octet
; n'existe ni au disque ni au journal).
; LE SECOND (Q2) : l'octet = (premier << 4) | second — AU JOURNAL PAR
; DÉCALAGE (la zone JOURNAL du plan : 256 entrées de 16 o, u64 décalage ·
; u8 octet · 7 réserve, le nombre @ +4096) : le décalage DÉJÀ au journal →
; l'octet REMPLACÉ, le compte n'augmente pas (I2 : l'entrée par décalage,
; la sauvegarde écrira chaque octet UNE fois ; l'ordre interne est L'ORDRE
; DE SAISIE) ; LE JOURNAL PLEIN (E3 : 256 DISTINCTS en attente) → -3, la
; borne NOMMÉE à la barre « journal plein - Ctrl+S », RIEN perdu (l'octet
; refusé n'entre pas, l'état demeure).
; ET À LA VUE (Q3) : l'octet posé au tampon de session — visible
; IMMÉDIATEMENT (jamais une édition invisible ; la cellule est garantie
; dans la fenêtre par le refus E2 qui PRÉCÈDE).
; LA MARQUE (Q4) : cadre.sale = 1 ET refus_quitter = 0 — LA GARDE DE
; loupe-18 RÉ-ARMÉE À CHAQUE ÉCRITURE (après une NOUVELLE écriture le
; premier Alt+F4 re-vient avertir : la falsification V5 de la spec est la
; preuve croisée) ; le curseur AVANCE (+1, clampé à taille - 1) ET LA VUE
; SUIT L'AVANCE — LE RENVOI DE loupe-15 Q3 (la même règle : les lignes
; visibles de la vitrine, le recadrage du plan, loupe-02 la première) :
; L'INVARIANT DU DOMAINE « le curseur ne sort JAMAIS de l'écran » (README)
; TIENT AUSSI À LA SAISIE — la cellule suivante ATTEND À L'ÉCRAN.
; E1 : SANS session ouverte → -4, « aucun fichier ouvert » à la barre.
; E2 : LA CELLULE FANTÔME — le curseur hors [vue, vue + remplissage) (la
; cellule n'existe pas à la vue : un état forgé, le curseur visible étant
; l'invariant du domaine) → -3 « hors bornes », RIEN au journal (le refus
; PRÉCÈDE le journal, l'oracle le constate) — le fichier VIDE y vit aussi
; (taille 0 : aucune cellule n'existe, remplissage 0).
; I1 : LE DISQUE INTACT — AUCUNE écriture fichier ici (WriteFile vit chez
; loupe-17 SEUL, la liste IAT fermée du plan : la contrebande d'écriture
; est un refus de build) ; I4 : le curseur BORNÉ [0, taille-1] ; AUCUNE
; entrée IAT propre au-delà de la feuille partagée InvalidateRect ; NOP, 0x90.
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x20
mov r12, rcx
lea rbx, [rip + CADRE]
lea r13, [rip + SAISIE]
; ==================== E1 : sans session → -4 nommé ===========================
cmp qword ptr [rbx + 528], -1
jne .session
lea rsi, [rip + L_SESSION]
call .message
mov eax, -4
jmp .sortie
.session:
mov r14, qword ptr [rbx + 544]
; ==================== Q5 : VK_SUPPR à l'attente ==============================
cmp r8d, 0x08
jne .classe
cmp dword ptr [r13 + 4], 0
je .rien
mov dword ptr [r13 + 4], 0
mov dword ptr [r13 + 8], 0
jmp .rien
; ==================== E4 : la classe (les seize chiffres) ====================
.classe:
mov eax, r8d
cmp eax, 0x61
jb .maj
cmp eax, 0x66
ja .maj
sub eax, 0x20
.maj:
cmp eax, 0x30
jb .rien
cmp eax, 0x39
jbe .chiffre
cmp eax, 0x41
jb .rien
cmp eax, 0x46
ja .rien
.chiffre:
cmp eax, 0x39
jbe .val
sub eax, 0x37
jmp .val_faite
.val:
sub eax, 0x30
.val_faite:
mov r15d, eax
; ==================== Q1 : le premier chiffre → l'attente ====================
cmp dword ptr [r13 + 4], 0
jne .second
mov dword ptr [r13 + 4], 1
mov dword ptr [r13 + 8], r15d
jmp .rien
; ==================== E2 : la cellule fantôme (le refus PRÉCÈDE) ============
.second:
mov r10d, dword ptr [r13 + 8]
; (le PREMIER CHIFFRE SAUVÉ À r10d — l'attente LUE avant sa fin : la
; consommation efface la zone, l'octet se compose du SAUVÉ ; r10 volatile,
; AUCUN appel entre ici et la composition)
mov dword ptr [r13 + 4], 0
mov dword ptr [r13 + 8], 0
; (l'attente CONSOMMÉE PAR L'ENGAGEMENT — « le second chiffre engage » :
; succès ou refus, jamais un nibble zombie en attente — actif ET valeur
; effacés, l'état est NET)
mov rax, qword ptr [rbx + 552]
mov rdx, qword ptr [rbx + 536]
add rax, rdx
cmp r14, rdx
jb .cellule_ok
cmp r14, rax
jb .cellule_ok
lea rsi, [rip + L_HORSBORNES]
call .message
mov eax, -3
jmp .sortie
.cellule_ok:
; ==================== Q2 : l'octet au journal (par décalage) =================
mov eax, r10d
shl eax, 4
or eax, r15d
movzx r15d, al
lea rdx, [rip + JOURNAL]
mov ecx, dword ptr [rdx + 4096]
mov r9, rdx
xor r8d, r8d
.cherche:
cmp r8d, ecx
jae .pas_la
cmp qword ptr [r9], r14
je .remplace
add r9, 16
inc r8d
jmp .cherche
.pas_la:
cmp ecx, 256
jb .ajoute
lea rsi, [rip + L_JOURNALPLEIN]
call .message
mov eax, -3
jmp .sortie
.ajoute:
mov qword ptr [r9], r14
mov byte ptr [r9 + 8], r15b
inc ecx
mov dword ptr [rdx + 4096], ecx
jmp .apres
.remplace:
mov byte ptr [r9 + 8], r15b
.apres:
; ==================== Q3 : et à la vue (visible immédiatement) ===============
mov rax, r14
sub rax, qword ptr [rbx + 536]
lea rdx, [rbx + 568]
mov byte ptr [rdx + rax], r15b
; ==================== Q4 : la marque, la garde, le pas =======================
mov dword ptr [rbx + 556], 1
mov dword ptr [rbx + 560], 0
inc r14
mov rax, qword ptr [rbx + 520]
dec rax
cmp r14, rax
jb .avance_ok
mov r14, rax
.avance_ok:
mov qword ptr [rbx + 544], r14
; ==================== LA VUE SUIT L'AVANCE (le renvoi de loupe-15 Q3) =======
lea rax, [rip + METRIQUES]
mov eax, dword ptr [rax + 8]
sub eax, 3
jns .vis_pos
xor eax, eax
.vis_pos:
cmp eax, 24
jbe .vis_cap
mov eax, 24
.vis_cap:
shl rax, 4
mov rdx, qword ptr [rbx + 536]
add rax, rdx
cmp r14, rdx
jb .recadre
cmp r14, rax
jb .visible
.recadre:
mov rcx, r14
sub rcx, 176
jns .recadre_pos
xor ecx, ecx
.recadre_pos:
and rcx, -16
mov rax, qword ptr [rbx + 520]
sub rax, 384
jbe .recadre_vmax_zero
add rax, 15
and rax, -16
jmp .recadre_vmax_fin
.recadre_vmax_zero:
xor eax, eax
.recadre_vmax_fin:
cmp rcx, rax
jbe .recadre_fin
mov rcx, rax
.recadre_fin:
cmp rcx, qword ptr [rbx + 536]
je .visible
mov r15, rcx
mov rcx, r15
call LOUPE02
test eax, eax
jnz .refus
mov qword ptr [rbx + 536], r15
.visible:
mov rcx, r12
xor edx, edx
mov r8d, 1
call qword ptr [rip + IAT_INVALIDATERECT]
.rien:
xor eax, eax
jmp .sortie
.refus:
add rsp, 0x20
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
.sortie:
add rsp, 0x20
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
; ==================== LE MESSAGE À LA BARRE ===================================
.message:
lea rdi, [rip + SAISIE]
add rdi, 12
.message_copie:
mov al, byte ptr [rsi]
mov byte ptr [rdi], al
test al, al
jz .message_fin
inc rsi
inc rdi
jmp .message_copie
.message_fin:
lea rax, [rip + SAISIE]
mov dword ptr [rax], 3
ret
