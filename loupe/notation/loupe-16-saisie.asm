; loupe-16-saisie · bloc la saisie : l'octet au journal, la marque sale, le disque intact · spec loupe-16:R1 · bloc carte i110016
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x6240, taille 704 octets
; Domaine : loupe (M10, le TGN « Loupe ») · Dépendances : LE PREMIER CHIFFRE (Q1 : l'attente au nibble — la zone SAISIE actif/nibble du plan, déclaré au geste (a)) ; LE SECOND (Q2 : l'octet = (premier << 4) | second AU JOURNAL PAR DÉCALAGE — la réécriture REMPLACE, le compte n'augmente pas ; la borne E3 : 256 DISTINCTS → -3 « journal plein - Ctrl+S », RIEN perdu) ; ET À LA VUE (Q3 : l'octet au tampon — visible IMMÉDIATEMENT) ; LA MARQUE (Q4 : sale = 1, refus_quitter = 0 — LA GARDE DE loupe-18 RÉ-ARMÉE à CHAQUE écriture ; le curseur AVANCE clampé, LA VUE SUIT L'AVANCE — le renvoi de loupe-15 Q3 : l'INVARIANT DU DOMAINE [« le curseur ne sort JAMAIS de l'écran », README § le tableau] tient AUSSI à la saisie) ; VK_SUPPR à l'attente (Q5 : le nibble effacé) ; E1 SANS SESSION -4 nommé ; E2 LA CELLULE FANTÔME : hors [vue, vue+remplissage) → -3, RIEN au journal (le refus PRÉCÈDE) ; E4 le non-hexa IGNORÉ ; LE DISQUE INTACT (I1 : WriteFile vit chez loupe-17 SEUL — la liste IAT fermée) ; AUCUNE entrée IAT propre au-delà de la feuille partagée (I4)
; Notation explicite générée par outils/auteur.py depuis brouillons/loupe-16-saisie.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 660 o · padding : 44 o (NOP, 0x90)
; Étiquettes résolues : .session=0x627e, .classe=0x62ab, .maj=0x62bb, .chiffre=0x62db, .val=0x62e5, .val_faite=0x62e8, .second=0x6303, .cellule_ok=0x6348, .cherche=0x6368, .pas_la=0x637b, .ajoute=0x6399, .remplace=0x63aa, .apres=0x63ae, .avance_ok=0x63ec, .vis_pos=0x6404, .vis_cap=0x640e, .recadre=0x6426, .recadre_pos=0x6434, .recadre_vmax_zero=0x6451, .recadre_vmax_fin=0x6453, .recadre_fin=0x645b, .visible=0x647a, .rien=0x648b, .refus=0x648f, .sortie=0x649d, .message=0x64ab, .message_copie=0x64b6, .message_fin=0x64c6
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x6250 + 0x7 + 0x7da9 = 0xe000
;   0x6257 + 0x7 + 0x81a2 = 0xe400
;   0x6268 + 0x7 - 0x3ed4 = 0x239b
;   0x6332 + 0x7 - 0x3faa = 0x238f
;   0x6355 + 0x7 + 0x8144 = 0xe4a0
;   0x6383 + 0x7 - 0x3e6a = 0x2520
;   0x63f3 + 0x7 + 0x99f6 = 0xfdf0
;   0x6485 + 0x6 - 0x32eb = 0x31a0
;   0x64ab + 0x7 + 0x7f4e = 0xe400
;   0x64c6 + 0x7 + 0x7f33 = 0xe400
; Appels directs (l'adresse du plan — I1) : call 0x64ab, call 0x64ab, call 0x64ab, call 0x4240, call qword ptr [rip - 0x32eb]
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x20
mov r12, rcx
lea rbx, [rip + 0x7da9]
lea r13, [rip + 0x81a2]
cmp qword ptr [rbx + 528], -1
jne 0x627e
lea rsi, [rip - 0x3ed4]
call 0x64ab
push -4
pop rax
nop
nop
jmp 0x649d
mov r14, qword ptr [rbx + 544]
cmp r8d, 0x08
jne 0x62ab
cmp dword ptr [r13 + 4], 0
je 0x648b
mov dword ptr [r13 + 4], 0
mov dword ptr [r13 + 8], 0
jmp 0x648b
mov eax, r8d
cmp eax, 0x61
jb 0x62bb
cmp eax, 0x66
ja 0x62bb
sub eax, 0x20
cmp eax, 0x30
jb 0x648b
cmp eax, 0x39
jbe 0x62db
cmp eax, 0x41
jb 0x648b
cmp eax, 0x46
ja 0x648b
cmp eax, 0x39
jbe 0x62e5
sub eax, 0x37
jmp 0x62e8
sub eax, 0x30
mov r15d, eax
cmp dword ptr [r13 + 4], 0
jne 0x6303
mov dword ptr [r13 + 4], 1
mov dword ptr [r13 + 8], r15d
jmp 0x648b
mov r10d, dword ptr [r13 + 8]
mov dword ptr [r13 + 4], 0
mov dword ptr [r13 + 8], 0
mov rax, qword ptr [rbx + 552]
mov rdx, qword ptr [rbx + 536]
add rax, rdx
cmp r14, rdx
jb 0x6348
cmp r14, rax
jb 0x6348
lea rsi, [rip - 0x3faa]
call 0x64ab
push -3
pop rax
nop
nop
jmp 0x649d
mov eax, r10d
shl eax, 4
or eax, r15d
movzx r15d, al
lea rdx, [rip + 0x8144]
mov ecx, dword ptr [rdx + 4096]
mov r9, rdx
xor r8d, r8d
cmp r8d, ecx
jae 0x637b
cmp qword ptr [r9], r14
je 0x63aa
add r9, 16
inc r8d
jmp 0x6368
cmp ecx, 256
jb 0x6399
lea rsi, [rip - 0x3e6a]
call 0x64ab
push -3
pop rax
nop
nop
jmp 0x649d
mov qword ptr [r9], r14
mov byte ptr [r9 + 8], r15b
inc ecx
mov dword ptr [rdx + 4096], ecx
jmp 0x63ae
mov byte ptr [r9 + 8], r15b
mov rax, r14
sub rax, qword ptr [rbx + 536]
lea rdx, [rbx + 568]
mov byte ptr [rdx + rax], r15b
mov dword ptr [rbx + 556], 1
mov dword ptr [rbx + 560], 0
inc r14
mov rax, qword ptr [rbx + 520]
dec rax
cmp r14, rax
jb 0x63ec
mov r14, rax
mov qword ptr [rbx + 544], r14
lea rax, [rip + 0x99f6]
mov eax, dword ptr [rax + 8]
sub eax, 3
jns 0x6404
xor eax, eax
cmp eax, 24
jbe 0x640e
mov eax, 24
shl rax, 4
mov rdx, qword ptr [rbx + 536]
add rax, rdx
cmp r14, rdx
jb 0x6426
cmp r14, rax
jb 0x647a
mov rcx, r14
sub rcx, 176
jns 0x6434
xor ecx, ecx
and rcx, -16
mov rax, qword ptr [rbx + 520]
sub rax, 384
jbe 0x6451
add rax, 15
and rax, -16
jmp 0x6453
xor eax, eax
cmp rcx, rax
jbe 0x645b
mov rcx, rax
cmp rcx, qword ptr [rbx + 536]
je 0x647a
mov r15, rcx
mov rcx, r15
call 0x4240
test eax, eax
jnz 0x648f
mov qword ptr [rbx + 536], r15
mov rcx, r12
xor edx, edx
mov r8d, 1
call qword ptr [rip - 0x32eb]
xor eax, eax
jmp 0x649d
add rsp, 0x20
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
add rsp, 0x20
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
lea rdi, [rip + 0x7f4e]
add rdi, 12
mov al, byte ptr [rsi]
mov byte ptr [rdi], al
test al, al
jz 0x64c6
inc rsi
inc rdi
jmp 0x64b6
lea rax, [rip + 0x7f33]
mov dword ptr [rax], 3
ret
