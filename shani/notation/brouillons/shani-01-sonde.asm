; shani-01-sonde · brouillon étiqueté — spec shani-01:R1
; LA SONDE CPUID de la variante SHA-NI : rax = 1 si (feuille 7 EBX bit 29
; = SHA) ET (feuille 1 ECX bit 9 = SSSE3 — pshufb/palignr de shani-02),
; rax = 0 sinon. rbx SAUVÉ (CPUID le détruit, non volatil msx64 — I2).
; AUCUN autre effet (Q3) : aucune écriture mémoire, aucun état détenu.
; La liste fermée des lectures : les DEUX feuilles, RIEN d'autre (I1).
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
