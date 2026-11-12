; shani-01-sonde · bloc sonde CPUID SHA-NI+SSSE3 · spec shani-01:R1 · bloc carte g210001 (PRÉFIGURÉ — la variante n'est PAS dans la carte : charte § 3, le scellage appartient au développeur)
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0xd000, taille 64 octets
; Domaine : shani (la variante SHA-NI, D205 — JAMAIS SCELLÉE) · Dépendances : bloc feuille ; CPUID feuilles 7-0 (EBX bit 29 SHA) et 1 (ECX bit 9 SSSE3) — rbx sauvé (I2), AUCUN autre effet (Q3) ; AUCUN déplacement RIP
; Notation explicite générée par outils/auteur.py depuis brouillons/shani-01-sonde.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 42 o · padding : 22 o (NOP, 0x90)
push rbx
mov eax, 7
xor ecx, ecx
cpuid
mov r8d, ebx
shr r8d, 29
and r8d, 1
mov eax, 1
cpuid
shr ecx, 9
and ecx, 1
and r8d, ecx
mov eax, r8d
pop rbx
ret
