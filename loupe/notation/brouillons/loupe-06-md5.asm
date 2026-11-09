; loupe-06 · md5 d'une gamme : l'empreinte du quotidien, notée neuve · spec loupe-06:R2
; LA RÉVISION R2 (l'Entrée 207 — LA CLASSE DES ARGUMENTS 5+ : le contexte
; 88 o DEMÉNAGE [rsp+0x20]→[rsp+0x40], le cadre 0xa0→0xc0, ET lpOverlapped
; NAÎT À SA PLACE VRAIE [rsp+0x20] — le VRAI ReadFile lisait A=0x67452301…
; AU SLOT DES ARGUMENTS : un pointeur fantôme. Le harnais relit LES
; MÊMES SLOTS QUE LE VRAI — le garde dérive de la convention.
; LA NOUVELLE NOTATION (aucun héritage : MD5 n'existe pas au projet, le
; quotidien le réclame — toutes les pièces vivent par leur md5 au journal
; des builds, D134). Le contexte 88 o SUR LA PILE (Q1 : A,B,C,D u32 @+0 ·
; longueur u64 @+16 · tampon[64] @+24 — la disposition miroir ah/tls13,
; les mêmes champs) ; LE CŒUR (Q2) : l'initialisation aux QUATRE abscisses
; (0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476 — RFC 1321 § 3.3), les
; SOIXANTE-QUATRE tours par blocs de 64 : les QUATRE rounds nommés (F de
; round lu sur les registres ANCIENS, g dérivé par lea — jamais une
; table), les décalages MD5_S et les constantes MD5_T LUES AUX TABLES
; PUBLIQUES .rdata du plan (I2 : la source unique vit au plan
; d'adressage — DÉRIVÉES PAR ARITHMÉTIQUE au geste (a), T[i] = floor(2^32
; · |sin(i+1)|)) ; le pas : A = D, D = C, C = B, B = B + rol(A₀ + F + T
; + X, S) — le tour canonique de la RFC § 3.4 ; l'absorption par LE
; TAMPOON du contexte (le couplage : jamais un bloc comprimé hors du
; tampon — le miroir tls13-03) ; le bourrement 0x80 puis les zéros, la
; longueur en BITS sur 64 bits @+56 (le petit-boutisme DE MD5, RFC 1321
; § 3.2) ; l'extraction des QUATRE mots sérialisés little-endian ; les
; fenêtres glissantes 64 Kio (Q3 : SetFilePointerEx + ReadFile dans
; TAMPON_CUMUL — un fichier de 2 Gio se condense, jamais tout en mémoire,
; I3 : le tampon de vue INTACT) ; I4 : le contexte ne survit pas au
; retour (la pile le rend) ; I5 : MD5 N'EST PAS UNE PREUVE — l'empreinte
; de cohérence du quotidien, RIEN DE PLUS.
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
mov dword ptr [rsp + 0x40], 0x67452301
mov dword ptr [rsp + 0x44], 0xefcdab89
mov dword ptr [rsp + 0x48], 0x98badcfe
mov dword ptr [rsp + 0x4c], 0x10325476
mov qword ptr [rsp + 0x50], 0
.boucle:
test r13, r13
jz .bourre
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
; LE PRÉ-ZÉRO DU COMPTE MORT (l'Entrée 207 : le VRAI ReadFile ÉCRIT la
; sortie au succès — la valeur n'est lue qu'après un succès : le zéro
; posé à la main était une pièce morte, il rend son cadre au budget)
lea r9, [rsp + 0xA0]
mov qword ptr [rsp + 0x20], 0
mov rcx, qword ptr [rbx + 528]
lea rdx, [rip + CUMUL]
mov r8, r15
call qword ptr [rip + IAT_READFILE]
test eax, eax
jz .refus_systeme
mov r15, qword ptr [rsp + 0xA0]
mov qword ptr [rsp + 0xA8], 0
.absorbe:
mov rax, qword ptr [rsp + 0xA8]
cmp rax, r15
jae .fenetre_fin
mov rdx, 64
mov rcx, qword ptr [rsp + 0x50]
and ecx, 63
sub rdx, rcx
mov r8, r15
sub r8, rax
cmp r8, rdx
jbe .k_ok
mov r8, rdx
.k_ok:
mov qword ptr [rsp + 0xB0], r8
lea rcx, [rsp + 0x58]
mov rax, qword ptr [rsp + 0x50]
and eax, 63
add rcx, rax
lea rdx, [rip + CUMUL]
mov rax, qword ptr [rsp + 0xA8]
add rdx, rax
mov r8, qword ptr [rsp + 0xB0]
call LIBC01
mov rax, qword ptr [rsp + 0xB0]
add qword ptr [rsp + 0x50], rax
mov rax, qword ptr [rsp + 0xA8]
add rax, qword ptr [rsp + 0xB0]
mov qword ptr [rsp + 0xA8], rax
mov rax, qword ptr [rsp + 0x50]
test eax, 63
jnz .absorbe
lea rcx, [rsp + 0x40]
lea rdx, [rsp + 0x58]
call .comprimer
jmp .absorbe
.fenetre_fin:
add r12, r15
sub r13, r15
jmp .boucle
.bourre:
mov rax, qword ptr [rsp + 0x50]
and eax, 63
mov r13d, eax
mov byte ptr [rsp + r13 + 0x58], 0x80
inc r13d
cmp r13d, 56
jbe .zeros56
lea rcx, [rsp + 0x58]
add rcx, r13
xor edx, edx
mov r8d, 64
sub r8d, r13d
call LIBC07
lea rcx, [rsp + 0x40]
lea rdx, [rsp + 0x58]
call .comprimer
xor r13d, r13d
.zeros56:
lea rcx, [rsp + 0x58]
add rcx, r13
xor edx, edx
mov r8d, 56
sub r8d, r13d
call LIBC07
mov rax, qword ptr [rsp + 0x50]
shl rax, 3
mov qword ptr [rsp + 0x90], rax
lea rcx, [rsp + 0x40]
lea rdx, [rsp + 0x58]
call .comprimer
mov eax, dword ptr [rsp + 0x40]
mov dword ptr [r14], eax
mov eax, dword ptr [rsp + 0x44]
mov dword ptr [r14 + 4], eax
mov eax, dword ptr [rsp + 0x48]
mov dword ptr [r14 + 8], eax
mov eax, dword ptr [rsp + 0x4c]
mov dword ptr [r14 + 12], eax
xor eax, eax
jmp .sortie
.comprimer:
push rbx
push r12
push r13
push r14
push r15
mov rbx, rcx
mov r15, rdx
mov r8d, dword ptr [rbx]
mov r9d, dword ptr [rbx + 4]
mov r10d, dword ptr [rbx + 8]
mov r11d, dword ptr [rbx + 12]
lea r14, [rip + MD5_S]
xor r12d, r12d
.tour:
cmp r12d, 16
jb .r1
cmp r12d, 32
jb .r2
cmp r12d, 48
jb .r3
mov eax, r10d
mov ecx, r11d
not ecx
or ecx, r9d
xor eax, ecx
mov r13d, r12d
shl r13d, 3
sub r13d, r12d
and r13d, 15
jmp .pas
.r1:
mov eax, r9d
and eax, r10d
mov ecx, r9d
not ecx
and ecx, r11d
or eax, ecx
mov r13d, r12d
jmp .pas
.r2:
mov eax, r11d
and eax, r9d
mov ecx, r11d
not ecx
and ecx, r10d
or eax, ecx
lea r13d, [r12 + r12*4 + 1]
and r13d, 15
jmp .pas
.r3:
mov eax, r9d
xor eax, r10d
xor eax, r11d
lea r13d, [r12 + r12*2 + 5]
and r13d, 15
.pas:
add eax, r8d
mov edx, dword ptr [r14 + r12*4 + 0x100]
add eax, edx
mov edx, dword ptr [r15 + r13*4]
add eax, edx
mov ecx, dword ptr [r14 + r12*4]
rol eax, cl
mov r8d, r11d
mov r11d, r10d
mov r10d, r9d
add r9d, eax
inc r12d
cmp r12d, 64
jb .tour
add dword ptr [rbx], r8d
add dword ptr [rbx + 4], r9d
add dword ptr [rbx + 8], r10d
add dword ptr [rbx + 12], r11d
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
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
