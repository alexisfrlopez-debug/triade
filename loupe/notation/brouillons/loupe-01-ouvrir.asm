; loupe-01 · ouvrir : le fichier donné à la session · spec loupe-01:R1
; L'ORDRE DES REFUS (le réseau des specs) : P2 la session pas déjà ouverte
; (E4 : -5, RIEN TOUCHÉ — le test AVANT loupe-04, l'ancien fichier INTACT) ;
; loupe-04 D'ABORD (le cadre vierge — Q3 : « loupe-04 a posé le vierge ») ;
; CreateFileW (I1 : GENERIC_LECTURE|GENERIC_ECRITURE, PARTAGE_LECTURE offert
; jamais reçu, OUVRIR_EXISTANT — le neuf refusé) ; la traduction par gle
; (I4 : E1 2/3 → -2, E2 32 → -7, E3 le reste → -6 — jamais un code brut à
; la barre) ; GetFileSizeEx ; LA BORNE NOMMÉE (Q2 : taille > 2 Gio → -3,
; la poignée FERMÉE AVANT le retour — jamais une poignée pendante) ; la
; copie du chemin (Q3 : la mesure UTF-16 bornée 260 puis libc-01 PAR LA
; CARTE — jamais octet par octet réécrit ; la mesure sans NUL à 260 → -5,
; l'argument invalide, JAMAIS un débordement) ; LA SESSION NÉE ENTIÈRE
; (Q4 : loupe-02 la fenêtre à la vue 0, puis loupe-07 le panneau — un
; refus : loupe-03 ferme, le verdict remonte TEL QUEL, jamais une poignée
; pendante) ; I2 : AUCUNE écriture au fichier à l'ouverture.
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x40
lea rbx, [rip + CADRE]
cmp qword ptr [rbx + 528], -1
jne .refus_session
mov r12, rcx
call LOUPE04
mov rcx, r12
mov edx, 0xc0000000
mov r8d, 1
xor r9d, r9d
mov dword ptr [rsp], 3
mov dword ptr [rsp + 8], 0
mov qword ptr [rsp + 0x10], 0
call qword ptr [rip + IAT_CREATEFILEW]
cmp rax, -1
je .refus_os
mov qword ptr [rbx + 528], rax
mov rcx, rax
lea rdx, [rsp + 0x20]
call qword ptr [rip + IAT_GETFILESIZEEX]
test eax, eax
jz .refus_taille_os
mov r13, qword ptr [rsp + 0x20]
mov eax, 0x80000000
cmp r13, rax
jbe .taille_ok
mov rcx, qword ptr [rbx + 528]
call qword ptr [rip + IAT_CLOSEHANDLE]
call LOUPE04
mov eax, -3
jmp .sortie
.taille_ok:
mov qword ptr [rbx + 520], r13
xor r14d, r14d
.mesure:
movzx eax, word ptr [r12 + r14*2]
test eax, eax
jz .mesure_fin
inc r14d
cmp r14d, 260
jb .mesure
mov rcx, qword ptr [rbx + 528]
call qword ptr [rip + IAT_CLOSEHANDLE]
call LOUPE04
mov eax, -5
jmp .sortie
.mesure_fin:
mov rcx, rbx
mov rdx, r12
mov r8d, r14d
shl r8d, 1
add r8d, 2
call LIBC01
; LA FENÊTRE seulement si le fichier n'est pas VIDE (révision 3 de la
; spec : le vide est un fichier réel du quotidien — loupe-02 P3 refuse
; toute fenêtre sur taille 0 ; le remplissage 0 posé, LE PANNEAU DU VIDE
; existe : d41d8cd9… + e3b0c442…)
test r13, r13
jz .panneau
xor ecx, ecx
call LOUPE02
test eax, eax
js .propage
.panneau:
lea rcx, [rip + EMPREINTES]
call LOUPE07
test eax, eax
js .propage
xor eax, eax
jmp .sortie
.propage:
mov r13d, eax
call LOUPE03
mov eax, r13d
jmp .sortie
.refus_session:
mov eax, -5
jmp .sortie
.refus_os:
call qword ptr [rip + IAT_GETLASTERROR]
cmp eax, 2
je .absent
cmp eax, 3
je .absent
cmp eax, 32
je .verrouille
mov eax, -6
jmp .sortie
.absent:
mov eax, -2
jmp .sortie
.verrouille:
mov eax, -7
jmp .sortie
.refus_taille_os:
mov rcx, qword ptr [rbx + 528]
call qword ptr [rip + IAT_CLOSEHANDLE]
call LOUPE04
mov eax, -6
jmp .sortie
.sortie:
add rsp, 0x40
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
