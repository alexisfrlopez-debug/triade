; loupe-05 · sha256 d'une gamme : l'héritage tls13 PAR LA CARTE · spec loupe-05:R2
; LA RÉVISION R2 (l'Entrée 207 — LE TÉMOIN T1 A NOMMÉ [SESSION] -6 SUR
; LOUPE-01, L'AUTOPSIE A ISOLÉ LA CLASSE : LES ARGUMENTS 5+ DE L'ABI msx64
; VIVENT À [rsp+0x20+] APRÈS LE HOME SPACE — jamais DANS le contexte) : le
; contexte SHA DEMÉNAGE [rsp+0x20]→[rsp+0x40] (le cadre 0xa0→0xc0) ET
; lpOverlapped NAÎT À SA PLACE VRAIE [rsp+0x20] — le VRAI ReadFile lisait
; H0[0] 0x6A09E667… AU SLOT DES ARGUMENTS : un pointeur fantôme. Le
; harnais (shim CreateFileW/ReadFile) relit désormais LES MÊMES SLOTS QUE
; LE VRAI — le garde dérive de la convention, jamais de la pièce.
; LA COMPOSITION HÉRITÉE (Q2, LA LISTE FERMÉE) : tls13-01 (l'initialisation,
; UNE fois — le contexte 112 o SUR LA PILE, I2 : aucune constante SHA
; re-déclarée, la disposition vit à tls13-01) puis pour chaque fenêtre
; (SetFilePointerEx + ReadFile dans TAMPON_CUMUL, au plus 64 Kio — Q3 :
; un fichier de 2 Gio se condense, jamais tout en mémoire) tls13-03
; (l'absorption), puis tls13-04 (la finalisation → la sortie 32 o) ;
; I1/R7 : les octets de tls13-01..04 au build == les octets du scellé
; 1.0.0 — l'oracle le constatera octet par octet ; I3 : la lecture passe
; par TAMPON_CUMUL, JAMAIS le tampon de vue du cadre (l'exclusion de
; famille) ; I4 : le pointeur repositionné à CHAQUE fenêtre ; E4 : le
; refus système → -6, gle consigné, la sortie INTACTE (jamais un condensé
; partiel : le calcul ne publie que le vrai).
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0xc0
lea rbx, [rip + CADRE]
cmp qword ptr [rbx + 528], -1
je .refus_session
mov rax, rcx
add rax, rdx
jc .refus_bornes
cmp rax, qword ptr [rbx + 520]
ja .refus_bornes
test r8, r8
jz .refus_sortie
mov r12, rcx
mov r13, rdx
mov r14, r8
lea rcx, [rsp + 0x40]
call TLS01
.boucle:
test r13, r13
jz .finalise
mov r15d, 0x10000
cmp r13, r15
jae .fenetre_taille
mov r15, r13
.fenetre_taille:
mov rcx, qword ptr [rbx + 528]
mov rdx, r12
xor r8d, r8d
xor r9d, r9d
call qword ptr [rip + IAT_SETFILEPOINTEREX]
test eax, eax
jz .refus_systeme
mov qword ptr [rsp + 0xB0], 0
lea r9, [rsp + 0xB0]
mov qword ptr [rsp + 0x20], 0
mov rcx, qword ptr [rbx + 528]
lea rdx, [rip + CUMUL]
mov r8, r15
call qword ptr [rip + IAT_READFILE]
test eax, eax
jz .refus_systeme
lea rcx, [rsp + 0x40]
lea rdx, [rip + CUMUL]
mov r8, qword ptr [rsp + 0xB0]
call TLS03
add r12, qword ptr [rsp + 0xB0]
sub r13, qword ptr [rsp + 0xB0]
jmp .boucle
.finalise:
lea rcx, [rsp + 0x40]
mov rdx, r14
call TLS04
xor eax, eax
jmp .sortie
.refus_session:
mov eax, -4
jmp .sortie
.refus_bornes:
mov eax, -3
jmp .sortie
.refus_sortie:
mov eax, -5
jmp .sortie
.refus_systeme:
call qword ptr [rip + IAT_GETLASTERROR]
mov eax, -6
jmp .sortie
.sortie:
add rsp, 0xc0
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
