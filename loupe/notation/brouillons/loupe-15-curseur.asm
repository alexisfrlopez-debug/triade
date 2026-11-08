; loupe-15 · curseur : la cellule active, jamais perdue hors écran · spec loupe-15:R1
; LE PAS (Q1) : VK_GAUCHE/DROITE = ±1, VK_HAUT/BAS = ±16 (une ligne),
; VK_PRECEDENT/SUIVANT = ±352 (la page, LA MÊME UNITÉ que loupe-11 —
; GRILLE_LIGNES - 2 lignes) ; VK_DEBUT = l'aligne16_inf du curseur (le début
; de ligne) ; VK_FIN = min(aligne16_inf + 15, taille - 1) — LA FIN DE LIGNE
; RÉELLE (jamais un curseur sur un octet qui n'existe pas, la ligne finale
; incomplète le prouve au harnais).
; LA BORNE (Q2) : curseur' = clamp(curseur ± pas, 0, taille - 1) — LES BORDS
; SONT DES ARRÊTS : à 0 VK_GAUCHE reste à 0, à taille-1 VK_DROITE/BAS
; restent — le clamp NOMMÉ, rax = 0 QUAND MÊME (le bord n'est pas un échec,
; E1 : la navigation ne peut pas échouer, elle peut S'ARRÊTER).
; LA VUE SUIT (Q3) : LA FENÊTRE VISIBLE LUE AUX LIGNES VISIBLES de la
; vitrine — METRIQUES.lignes - 3 (la barre ancrée au bas, la leçon du geste
; (c)), capée à 24 (GRILLE_LIGNES) : [vue, vue + lignes_visibles × 16). LA
; LECTURE STRICTE de la spec (jamais perdu hors écran, Y COMPRIS la vitrine
; rétrécie ; à la vitrine 0.1.0 [30 lignes - 3 = 27 >= 24] la fenêtre == le
; remplissage 384 : LE MIROIR EXACT du commit de loupe-12, la même règle —
; renvoi, la source unique). LE RECADRAGE PAR LA RÈGLE DU PLAN : curseur -
; 176 (la 12e ligne) aligne16_inf, JAMAIS négatif, clapé vue_max
; (aligne16_sup de taille - 384) ; loupe-02 LA PREMIÈRE (le refus système
; relayé, la vue inchangée — le miroir de loupe-11/12) puis la vue posée ;
; la relecture SEULEMENT au recadrage (I2 : la vue ne bouge QUE POUR SUIVRE
; — le harnais compte les lectures : curseur dans la fenêtre → AUCUNE
; lecture, la vue INTACTE).
; L'INVALIDATION : TOUJOURS après un pas qui bouge le curseur (la
; surbrillance suit — la cellule active repeinte par loupe-10 au prochain
; WM_PAINT : le repaint DEMANDÉ, jamais volé ; le bloc ne peint RIEN, I3 —
; ni journal, ni empreintes, ni tampon : la navigation est PURE POSITION).
; LE REPLI (P2, Q4) : SANS session (la poignée INVALIDE) ou le fichier
; VIDE (taille 0 : aucune cellule n'existe) → rax = 0 SANS effet — les
; flèches dans la vitrine vide ne bougent rien (rendu à DefWindowProcW).
; I1 : le curseur TOUJOURS dans [0, taille-1] — LA BORNE EST LUE AU CADRE,
; jamais crue de l'appelant (le clamp PRÉCÈDE tout) ; I4 : AUCUNE entrée
; IAT propre au-delà de la feuille partagée InvalidateRect (la composition
; seule) ; registres non volatils rendus ; NOP, 0x90.
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x20
mov r12, rcx
lea rbx, [rip + CADRE]
; ==================== LE REPLI (P2 : rien bougé, la vitrine vide) ============
cmp qword ptr [rbx + 528], -1
je .rien
mov r13, qword ptr [rbx + 520]
test r13, r13
jz .rien
; ==================== LE PAS (Q1) ============================================
mov r14, qword ptr [rbx + 544]
cmp r8d, 0x24
je .debut
cmp r8d, 0x23
je .fin
cmp r8d, 0x25
je .gauche
cmp r8d, 0x27
je .droite
cmp r8d, 0x26
je .haut
cmp r8d, 0x28
je .bas
cmp r8d, 0x21
je .precedent
cmp r8d, 0x22
je .suivant
jmp .rien
.debut:
and r14, -16
jmp .pas_faite
.fin:
mov rax, r14
and rax, -16
add rax, 15
lea rdx, [r13 - 1]
cmp rax, rdx
jbe .fin_pos
mov rax, rdx
.fin_pos:
mov r14, rax
jmp .pas_faite
.gauche:
dec r14
jmp .borne
.droite:
inc r14
jmp .borne
.haut:
sub r14, 16
jmp .borne
.bas:
add r14, 16
jmp .borne
.precedent:
sub r14, 352
jmp .borne
.suivant:
add r14, 352
; ==================== LA BORNE (Q2 : le clamp, les arrêts) ===================
.borne:
test r14, r14
jns .borne_haute
xor r14d, r14d
jmp .pas_faite
.borne_haute:
cmp r14, r13
jb .pas_faite
lea r14, [r13 - 1]
.pas_faite:
mov qword ptr [rbx + 544], r14
; ==================== LA VUE SUIT (Q3 : la fenêtre visible) ==================
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
; ==================== LE RECADRAGE (la règle du plan, loupe-12 Q3) ==========
.recadre:
mov rcx, r14
sub rcx, 176
jns .recadre_pos
xor ecx, ecx
.recadre_pos:
and rcx, -16
mov rax, r13
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
; ==================== L'INVALIDATION (le repaint demandé) ====================
.visible:
mov rcx, r12
xor edx, edx
mov r8d, 1
call qword ptr [rip + IAT_INVALIDATERECT]
.rien:
xor eax, eax
jmp .sortie
; ==================== LE REFUS RELAYÉ (la vue INTACTE, le miroir 11/12) ======
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
