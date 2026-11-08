; loupe-17 · sauver : les octets modifiés écrits à l'octet, le témoin rendu · spec loupe-17:R1
; LE JOURNAL VIDE (Q1) : « rien à sauver » à la barre (le repli documenté,
; l'état nommé PAS un échec), rax = 0, AUCUN appel WriteFile — le harnais
; les compte.
; SINON (Q2) : POUR CHAQUE entrée du journal DANS SON ORDRE DE SAISIE (I2 :
; l'ordre interne de loupe-16, suivi TEL QUEL) : SetFilePointerEx(décalage,
; DEBUT_FICHIER) puis WriteFile d'UN SEUL octet — L'ÉCRITURE À L'OCTET,
; l'unité est l'octet, JAMAIS une plage (I4 : un hexadécimal éditeur ne
; crée pas d'octets) ; le pointeur d'écrits NUL (la poignée est
; synchrone — CreateFileW sans FILE_FLAG_OVERLAPPED ; le harnais compte
; les octets LUI-MÊME). L'ÉCHEC (E2) : -6, GetLastError CONSIGNÉ, ET
; FAIL-CLOSED — le journal DEMEURE, la marque demeure, les octets déjà
; écrits le restent : L'ÉCHEC NE PERD RIEN, le geste peut se reprendre
; (le second Ctrl+S reprend et FINIT — V3 le prouve) ; le témoin ne ment
; pas : il ne rend QUE le succès complet (aucun message ici, le -6 monte
; par .monter de loupe-09 — le générique « refus système »).
; LE SUCCÈS COMPLET (Q3) : journal.nombre = 0, cadre.sale = 0,
; refus_quitter = 0 — LA GARDE DE loupe-18 LEVÉE (la sortie ne ré-avertira
; plus : il n'y a plus rien à perdre).
; LE PANNEAU RE-NAÎT (Q4) : loupe-07 rappelé — LES EMPREINTES DU DISQUE
; (la sauvegarde a changé le fichier, le panneau suit : jamais un condensé
; d'avant) ; LE COÛT NOMMÉ : un passage de plus, le prix de la vérité ; un
; refus relayé TEL QUEL (E3 de loupe-07 — le panneau ne publie RIEN).
; LE TÉMOIN (Q5) : « N o écrits · 0xAABBCCDD..0xEEFFGGHH » à la barre — le
; compte exact EN DÉCIMAL, la PREMIÈRE et la DERNIÈRE adresses écrites en
; 8 chiffres MAJUSCULES (la table HEX du plan), composés AVANT LA VIDANGE
; (le journal est la source du témoin : .dec + .chaine + .hex8, LES
; SOUS-ROUTINES LOCALES AU CADRE RBP — le modèle loupe-10, chaque local à
; son emplacement stable) ; ce qui a bougé est DIT, pas suggéré.
; LA TAILLE DEMEURE (Q6) : l'écriture à l'octet ne change JAMAIS la taille
; — l'oracle le constate (GetFileSizeEx avant == après, côté harnais).
; E1 : SANS session → -4, « aucun fichier ouvert » à la barre.
; I1 : AUCUNE écriture hors des entrées du journal (le reste du fichier
; INTACT — la différentielle le prouve : SEULEMENT les N octets diffèrent)
; ; I3 : WriteFile et SetFilePointerEx vivent ICI SEULS dans le domaine
; (l'IAT fermée : loupe-16 l'a juré, le build le vérifie) ; registres non
; volatils rendus ; NOP, 0x90.
push rbx
push r12
push r13
push r14
push r15
push rbp
mov rbp, rsp
sub rsp, 0x28
mov r12, rcx
lea rbx, [rip + CADRE]
lea r13, [rip + JOURNAL]
; ==================== E1 : sans session → -4 nommé ===========================
cmp qword ptr [rbx + 528], -1
jne .session
lea rsi, [rip + L_SESSION]
call .message
mov eax, -4
jmp .sortie
.session:
; ==================== Q1 : le journal vide → « rien à sauver » ===============
cmp dword ptr [r13 + 4096], 0
jne .sauver
lea rsi, [rip + L_RIENSAUVER]
call .message
xor eax, eax
jmp .sortie
; ==================== Q2 : chaque entrée à son décalage, une par une ========
.sauver:
mov r14, r13
xor r15d, r15d
.boucle:
mov rcx, qword ptr [rbx + 528]
mov rdx, qword ptr [r14]
xor r8d, r8d
xor r9d, r9d
call qword ptr [rip + IAT_SETFILEPOINTEREX]
test eax, eax
jz .refus_systeme
mov rcx, qword ptr [rbx + 528]
lea rdx, [r14 + 8]
mov r8d, 1
xor r9d, r9d
mov qword ptr [rsp + 0x20], 0
call qword ptr [rip + IAT_WRITEFILE]
test eax, eax
jz .refus_systeme
inc r15d
add r14, 16
cmp r15d, dword ptr [r13 + 4096]
jb .boucle
; ==================== Q5 : le témoin composé AVANT la vidange ===============
lea rdi, [rip + SAISIE]
add rdi, 12
mov eax, r15d
call .dec
lea rsi, [rip + L_ECRITS]
call .chaine
mov rax, qword ptr [r13]
call .hex8
lea rsi, [rip + L_JUSQUA]
call .chaine
mov rax, qword ptr [r14 - 16]
call .hex8
mov byte ptr [rdi], 0
lea rax, [rip + SAISIE]
mov dword ptr [rax], 3
; ==================== Q3 : le succès — marque levée, garde levée ============
mov dword ptr [r13 + 4096], 0
mov dword ptr [rbx + 556], 0
mov dword ptr [rbx + 560], 0
; ==================== Q4 : le panneau re-naît (la vérité du disque) =========
lea rcx, [rip + EMPREINTES]
call LOUPE07
test eax, eax
jnz .sortie_relaye
; ==================== l'invalidation (le panneau suit) ======================
mov rcx, r12
xor edx, edx
mov r8d, 1
call qword ptr [rip + IAT_INVALIDATERECT]
xor eax, eax
jmp .sortie
; ==================== E2 : -6 FAIL-CLOSED (le journal demeure) ==============
.refus_systeme:
call qword ptr [rip + IAT_GETLASTERROR]
mov eax, -6
jmp .sortie
.sortie_relaye:
; (le verdict de loupe-07 relayé TEL QUEL — eax traverse, le panneau ne publie RIEN)
; ==================== LA SORTIE ==============================================
.sortie:
add rsp, 0x28
pop rbp
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
; ==================== LES SOUS-ROUTINES LOCALES (le cadre RBP partagé) =======
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
.chaine:
mov al, byte ptr [rsi]
mov byte ptr [rdi], al
test al, al
jz .chaine_fin
inc rsi
inc rdi
jmp .chaine
.chaine_fin:
ret
.dec:
lea r9, [rbp - 8]
xor r11d, r11d
mov r10d, 10
.dec_boucle:
xor edx, edx
div r10
add dl, 0x30
dec r9
mov byte ptr [r9], dl
inc r11d
test eax, eax
jnz .dec_boucle
.dec_copie:
mov al, byte ptr [r9]
mov byte ptr [rdi], al
inc r9
inc rdi
dec r11d
jnz .dec_copie
ret
.hex8:
lea r11, [rip + HEX]
mov r10, rax
mov r9d, 28
.hex8_boucle:
mov rax, r10
mov ecx, r9d
shr rax, cl
and eax, 0xf
movzx eax, byte ptr [r11 + rax]
mov byte ptr [rdi], al
inc rdi
sub r9d, 4
cmp r9d, 0
jge .hex8_boucle
ret
