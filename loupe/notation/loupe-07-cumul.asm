; loupe-07-cumul · bloc le cumul : les empreintes du fichier entier au panneau · spec loupe-07:R1 · bloc carte i110007
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x4940, taille 128 octets
; Domaine : loupe (M10, le TGN « Loupe ») · Dépendances : loupe-05 (le passage SHA-256) puis loupe-06 (le passage MD5) — LA COMPOSITION SEULE, DEUX passages l'un après l'autre (I2 : l'exclusion de famille) ; AUCUNE entrée IAT (le miroir des feuilles pures, charte § 9)
; Notation explicite générée par outils/auteur.py depuis brouillons/loupe-07-cumul.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 102 o · padding : 26 o (NOP, 0x90)
; Étiquettes résolues : .refus_session=0x4990, .refus_sortie=0x4997, .sortie=0x499e
; Déplacements RIP (cible = adresse + taille + disp) :
;   0x4947 + 0x7 + 0x96b2 = 0xe000
; Appels directs (l'adresse du plan — I1) : call 0x4440, call 0x45c0
push rbx
push r12
sub rsp, 0x28
lea rbx, [rip + 0x96b2]
cmp qword ptr [rbx + 528], -1
je 0x4990
test rcx, rcx
jz 0x4997
mov r12, rcx
xor ecx, ecx
mov rdx, qword ptr [rbx + 520]
lea r8, [r12 + 16]
call 0x4440
test eax, eax
js 0x499e
xor ecx, ecx
mov rdx, qword ptr [rbx + 520]
mov r8, r12
call 0x45c0
test eax, eax
js 0x499e
xor eax, eax
jmp 0x499e
mov eax, -4
jmp 0x499e
mov eax, -5
jmp 0x499e
add rsp, 0x28
pop r12
pop rbx
ret
