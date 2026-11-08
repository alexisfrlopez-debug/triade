; loupe-18 · quitter : la sortie propre, aucun octet perdu, aucune fuite · spec loupe-18:R1
; LE DOUBLE-GESTE GARANTI (Q1/Q2) : WM_CLOSE (Alt+F4 ou le menu système)
; avec la marque sale ET la garde armée (refus_quitter = 0) → LE PREMIER
; GESTE EST REFUSÉ NOMMÉMENT : la garde posée (refus_quitter = 1), LA
; PHRASE à la barre « MODIFIÉ - Alt+F4 encore pour quitter sans sauver,
; Ctrl+S pour sauver » (le libellé du plan — le tiret ASCII, la leçon du
; geste (c)), MessageBeep (LE REFUS S'ENTEND), verdict -5 (L'ORDRE REFUSÉ
; EN L'ÉTAT — E1 : c'est L'ÉCHEC QUI GARDE, la sanction est la protection)
; — la fenêtre DEMEURE, rien n'est perdu ; le message -5 monte à la barre
; par loupe-09 (.monter : la phrase VIT DÉJÀ au tampon, le générique
; s'incline — jamais un refus muet) ;
; LE SECOND GESTE TRANSCHE (Q2 : marque sale + garde déjà posée) OU la
; marque PROPRE → DestroyWindow — l'utilisateur a tranché : sauver était à
; lui (I2 : LA SORTIE NE SAUVEGARDE JAMAIS ELLE-MÊME — la sauvegarde est
; un geste explicite de loupe-17, quitter ne décide JAMAIS à sa place).
; WM_DESTROY (Q3 — la fin de fenêtre, envoyée par DestroyWindow) :
; loupe-03 LA SESSION CLOSE PROPREMENT (la poignée rendue, le cadre
; re-vierge, l'hygiène des zones — le journal ABANDONNÉ DÉLIBÉRÉMENT :
; le double-geste l'a nommé, les octets non sauvés sont une VOLONTÉ, pas
; une perte), puis PostQuitMessage(0) — LA BOUCLE HÉRITÉE win-03 REND
; (GetMessageW rend 0), WinMain retourne, ExitProcess(0) (le dernier
; souffle vit chez loupe-09) ;
; I3 AUCUNE FUITE : la poignée close (loupe-03), le contexte de peinture
; toujours rendu (EndPaint chez loupe-10, y compris à l'avortement), la
; file quittée (PostQuitMessage UNE fois), le code de sortie 0 (LE SUCCÈS
; : même l'abandon délibéré est une sortie PROPRE) ; Q4 rax = 0 aux deux
; chemins de passage, -5 au chemin refusé (le verdict nommé monte à la
; barre — l'écran nomme ce qu'il refuse) ;
; I4 : l'IAT fermée du bloc (DestroyWindow, PostQuitMessage, MessageBeep —
; la clôture de session vit chez loupe-03, le processus meurt chez
; loupe-09) ; registres non volatils rendus ; NOP, 0x90.
push rbx
push r12
sub rsp, 0x28
mov r12, rcx
lea rbx, [rip + CADRE]
; ==================== le message (WM_CLOSE ou WM_DESTROY) ====================
cmp edx, 0x10
je .fermeture
cmp edx, 2
je .destruction
xor eax, eax
jmp .sortie
; ==================== WM_CLOSE : le double-geste (Q1/Q2) =====================
.fermeture:
cmp dword ptr [rbx + 556], 0
je .detruire
cmp dword ptr [rbx + 560], 0
jne .detruire
mov dword ptr [rbx + 560], 1
lea rsi, [rip + L_QUITTER]
call .message
xor ecx, ecx
call qword ptr [rip + IAT_MESSAGEBEEP]
mov eax, -5
jmp .sortie
.detruire:
mov rcx, r12
call qword ptr [rip + IAT_DESTROYWINDOW]
xor eax, eax
jmp .sortie
; ==================== WM_DESTROY : la sortie propre (Q3) ====================
.destruction:
call LOUPE03
xor ecx, ecx
call qword ptr [rip + IAT_POSTQUITMESSAGE]
xor eax, eax
; ==================== LA SORTIE ==============================================
.sortie:
add rsp, 0x28
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
