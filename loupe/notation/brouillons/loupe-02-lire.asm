; loupe-02 · lire : la fenêtre d'octets au tampon de session · spec loupe-02:R1
; LA FENÊTRE BORNÉE (I3 : la double borne — remplissage = min(384,
; taille − décalage), jamais un octet au-delà de la fin) ; la position
; REPOSITIONNÉE à chaque lecture (I4 : SetFilePointerEx AVANT ReadFile,
; jamais une position héritée) ; la lecture ne touche QUE le tampon du
; cadre (I2 : jamais TAMPON_CUMUL, jamais l'ECRAN) ; LE RECOUVREMENT DU
; JOURNAL (Q2 : chaque entrée dont le décalage vit dans la fenêtre
; remplace l'octet du tampon — l'édition survit au défilement) ; la vue
; et le curseur INTACTS (Q3 : lire ne déplace rien) ; E4 le fail-closed :
; remplissage = 0 sur refus système (le tampon ne montre JAMAIS un octet
; non lu) ; P2 l'alignement de ligne : décalage multiple de 16 (E2).
push rbx
push r12
push r13
push r14
sub rsp, 0x28
lea rbx, [rip + CADRE]
cmp qword ptr [rbx + 528], -1
je .refus_session
test rcx, 0xf
jne .refus_entree
mov r12, rcx
cmp r12, qword ptr [rbx + 520]
jae .refus_bornes
mov r13, qword ptr [rbx + 520]
sub r13, r12
cmp r13, 384
jbe .rempli
mov r13d, 384
.rempli:
mov dword ptr [rbx + 552], r13d
mov rcx, qword ptr [rbx + 528]
mov rdx, r12
xor r8d, r8d
xor r9d, r9d
call qword ptr [rip + IAT_SETFILEPOINTEREX]
test eax, eax
jz .refus_systeme
mov qword ptr [rsp + 0x20], 0
lea r9, [rsp + 0x20]
mov qword ptr [rsp], 0
mov rcx, qword ptr [rbx + 528]
lea rdx, [rbx + 568]
mov r8, r13
call qword ptr [rip + IAT_READFILE]
test eax, eax
jz .refus_systeme
lea r14, [rip + JOURNAL]
xor ecx, ecx
.recouvre:
cmp ecx, dword ptr [r14 + 4096]
jae .recouvre_fin
mov rax, rcx
shl rax, 4
mov rdx, qword ptr [r14 + rax]
cmp rdx, r12
jb .recouvre_suivant
mov r8, r12
add r8, r13
cmp rdx, r8
jae .recouvre_suivant
sub rdx, r12
mov al, byte ptr [r14 + rax + 8]
mov byte ptr [rbx + rdx + 568], al
.recouvre_suivant:
inc ecx
jmp .recouvre
.recouvre_fin:
xor eax, eax
jmp .sortie
.refus_session:
mov eax, -4
jmp .sortie
.refus_entree:
mov eax, -5
jmp .sortie
.refus_bornes:
mov eax, -3
jmp .sortie
.refus_systeme:
call qword ptr [rip + IAT_GETLASTERROR]
mov dword ptr [rbx + 552], 0
mov eax, -6
jmp .sortie
.sortie:
add rsp, 0x28
pop r14
pop r13
pop r12
pop rbx
ret
