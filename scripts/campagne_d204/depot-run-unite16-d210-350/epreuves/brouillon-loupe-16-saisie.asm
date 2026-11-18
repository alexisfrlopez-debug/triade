; loupe-16 · saisie : l'octet au journal, la marque sale, la garde ré-armée · spec loupe-16:R1
; LA COMPOSITION DE CAMPAGNE (l'unité 04 D210 × bras T — la notation
; écrite à la main) : DEUX tours d'auteur (it1 nommé F1-F5 aux contrôles
; — les offset 0x328, les non-volatils rsi/rdi détruits, l'étiquette IAT
; illégale, les lea morts, le verdict nu ; it2 corrigé) PUIS LA
; COMPOSITION DES ÉLÉMENTS CONVERGÉS (le geste mécanique du labo, nommé
; — le précédent des 336/341/346) : la présente it3, la composition
; bijective de l'auteur.
; LE CONTRAT EN BREF : E1 sans session (poignée == -1) → -4 nommé à la
; barre ; Q5 VK_SUPPR (0x08) à l'attente → le nibble effacé ; E4 les
; SEIZE chiffres écoutent (a-f porté à A-F), le reste IGNORÉ ; Q1 le
; premier chiffre pose l'attente (rien n'est écrit) ; Q2 le second
; compose l'octet = (premier << 4) | second, l'attente CONSOMMÉE avant
; tout contrôle ; E2 la cellule fantôme (curseur ≥ vue + remplissage —
; le DWORD @+552 SEUL, jamais le qword : la marque vit à +556) → -3,
; RIEN au journal ; le JOURNAL PAR DÉCALAGE (256 × 16 o — u64 décalage,
; u8 octet — le nombre u32 @+4096 : présent REMPLACÉ, absent AJOUTÉ, 256
; DISTINCTS → E3 -3 nommé) ; Q3 l'octet au tampon visible ; Q4 sale =
; 1, refus_quitter = 0 (LA GARDE RÉ-ARMÉE), le curseur +1 clampé ; LA
; VUE SUIT (V = lignes − 3 clampé [0,24] ; le curseur hors [vue, vue +
; 16·V) → aligne16_inf(curseur − 176) clampé à aligne16_sup(taille −
; 384) — LOUPE02 la relit, la feuille InvalidateRect repeint) ; I1 LE
; DISQUE INTACT ; NOP, 0x90.
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x20
mov r12, rcx
lea rbx, [rip + CADRE]
lea r13, [rip + SAISIE]
; ==================== E1 : la session (la poignée invalide hors session)
cmp qword ptr [rbx + 528], -1
jne .ouverte
lea r10, [rip + L_SESSION]
call .message
push -4
pop rax
nop
nop
jmp .fin
.ouverte:
mov r14, qword ptr [rbx + 544]
; ==================== Q5 : VK_SUPPR à l'attente (le nibble effacé) =======
cmp r8d, 0x08
jne .caractere
cmp dword ptr [r13 + 4], 0
je .silence
mov dword ptr [r13 + 4], 0
mov dword ptr [r13 + 8], 0
jmp .silence
; ==================== E4 : la classe (les seize chiffres) =================
.caractere:
mov eax, r8d
cmp eax, 0x61
jb .chiffres
cmp eax, 0x66
ja .chiffres
sub eax, 0x20
.chiffres:
cmp eax, 0x30
jb .silence
cmp eax, 0x39
jbe .neuf
cmp eax, 0x41
jb .silence
cmp eax, 0x46
ja .silence
sub eax, 0x37
jmp .valeur
.neuf:
sub eax, 0x30
.valeur:
mov r15d, eax
; ==================== Q1 : le premier chiffre (l'attente posée) ============
cmp dword ptr [r13 + 4], 0
jne .engager
mov dword ptr [r13 + 4], 1
mov dword ptr [r13 + 8], r15d
jmp .silence
; ==================== Q2 : le second (l'attente consommée, l'octet composé)
.engager:
mov r10d, dword ptr [r13 + 8]
mov dword ptr [r13 + 4], 0
mov dword ptr [r13 + 8], 0
mov eax, r10d
shl eax, 4
or eax, r15d
movzx r15d, al
; ==================== E2 : la cellule fantôme (le refus précède) ===========
mov eax, dword ptr [rbx + 552]
add rax, qword ptr [rbx + 536]
cmp r14, rax
jb .legitime
lea r10, [rip + L_HORSBORNES]
call .message
push -3
pop rax
nop
nop
jmp .fin
.legitime:
; ==================== Q2 : le journal par décalage =========================
lea rdx, [rip + JOURNAL]
mov r10d, dword ptr [rdx + 4096]
xor r8d, r8d
mov r9, rdx
.balaye:
cmp r8d, r10d
jae .absente
cmp qword ptr [r9], r14
je .remplace
add r9, 16
inc r8d
jmp .balaye
.absente:
cmp r10d, 256
jae .saturee
mov qword ptr [r9], r14
mov byte ptr [r9 + 8], r15b
inc r10d
mov dword ptr [rdx + 4096], r10d
jmp .apres
.remplace:
mov byte ptr [r9 + 8], r15b
jmp .apres
.saturee:
lea r10, [rip + L_JOURNALPLEIN]
call .message
push -3
pop rax
nop
nop
jmp .fin
.apres:
; ==================== Q3 : l'octet visible immédiatement ===================
mov rax, r14
sub rax, qword ptr [rbx + 536]
lea rdx, [rbx + 568]
mov byte ptr [rdx + rax], r15b
; ==================== Q4 : la marque, la garde, le pas ====================
mov dword ptr [rbx + 556], 1
mov dword ptr [rbx + 560], 0
inc r14
mov rax, qword ptr [rbx + 520]
dec rax
cmp r14, rax
jb .avance
mov r14, rax
.avance:
mov qword ptr [rbx + 544], r14
; ==================== LA VUE SUIT (le renvoi de loupe-15 Q3) ===============
lea rax, [rip + METRIQUES]
mov eax, dword ptr [rax + 8]
sub eax, 3
jns .lignes
xor eax, eax
.lignes:
cmp eax, 24
jbe .cap
mov eax, 24
.cap:
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
jns .amorce
xor ecx, ecx
.amorce:
and rcx, -16
mov rax, qword ptr [rbx + 520]
sub rax, 384
jbe .plancher
add rax, 15
and rax, -16
jmp .vmax
.plancher:
xor eax, eax
.vmax:
cmp rcx, rax
jbe .borne
mov rcx, rax
.borne:
cmp rcx, qword ptr [rbx + 536]
je .visible
mov r15, rcx
call LOUPE02
test eax, eax
jnz .echec
mov qword ptr [rbx + 536], r15
.visible:
mov rcx, r12
xor edx, edx
mov r8d, 1
call qword ptr [rip + IAT_INVALIDATERECT]
xor eax, eax
jmp .fin
.silence:
xor eax, eax
jmp .fin
.echec:
add rsp, 0x20
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
.fin:
add rsp, 0x20
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
; ==================== LE MESSAGE À LA BARRE (aux volatils seuls) ==========
.message:
lea r11, [rip + SAISIE]
add r11, 12
.copie:
mov al, byte ptr [r10]
mov byte ptr [r11], al
test al, al
jz .pose
inc r10
inc r11
jmp .copie
.pose:
lea r11, [rip + SAISIE]
mov dword ptr [r11], 3
ret
