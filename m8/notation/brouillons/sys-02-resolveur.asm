; sys-02-resolveur · le résolveur SSN · spec sys-02:R1 · bloc carte g90002
; Lire le numéro de service d'une fonction NT dans l'EAT de ntdll, SUR LA
; MACHINE qui exécute — le SSN comme DONNÉE (charte § 1), la fondation du
; domaine. ntdll est LUE, jamais appelée (charte § 3) : de la mémoire
; directe, les trois tables pointées par le répertoire export, rien d'autre.
; Les constantes citées vivent au plan d'adressage (m8/layout.py, source
; unique — T5 : E_LFANEW 0x3C, la fenêtre [E_LFANEW_MIN 0x40, E_LFANEW_MAX
; 0x400], MOTIF_PE « PE\0\0 » = 0x4550, OFF_EXPORT_RVA 0x88, EXP_NBNOMS
; 0x18, EXP_ADRFONC 0x1C, EXP_ADRNOMS 0x20, EXP_ADRORD 0x24, MOTIF_STUB
; 4C 8B D1 B8 = 0xB8D18B4C en dword little-endian, OFF_SSN 4) ; le harnais
; du chantier (b) re-vérifie la concordance octet par octet.
; La garde d'abord (fail-closed, charte § 5 — les verdicts sont de VRAIS
; négatifs 64 bits : mov rax, -N signe-étendu ; l'imm32 du SSN est
; zéro-étendu — jamais de collision entre un verdict et un numéro).
test rcx, rcx
je .span_invalide
test rdx, rdx
je .span_invalide
; la base (P3) : e_lfanew lu à +0x3C, la fenêtre [0x40, 0x400] d'abord —
; un décalage fou est un refus (-2), pas un crash
mov r11d, dword ptr [r8 + 0x3C]
cmp r11d, 0x40
jb .pas_module
cmp r11d, 0x400
ja .pas_module
; le motif PE (MOTIF_PE) : absent = -2
lea r9, [r8 + r11]
cmp dword ptr [r9], 0x4550
jne .pas_module
; le répertoire export (OFF_EXPORT_RVA @ PE+0x88) — RVA nul = -3
mov r10d, dword ptr [r9 + 0x88]
test r10d, r10d
jz .eat_absente
lea r10, [r8 + r10]
; le cadre : 0x48 (l'ombre 0x20 + quatre locaux — l'entrée ≡ 8 mod 16,
; 8 + 0x48 ≡ 0 : les appels sont alignés) ; I8 : AUCUNE écriture dans le
; module lu (le harnais le prouve aux canaris) ; I7 : les adresses de
; travail au cadre et en volatils, JAMAIS en non-volatils
sub rsp, 0x48
mov qword ptr [rsp + 0x20], rcx
mov qword ptr [rsp + 0x28], rdx
mov qword ptr [rsp + 0x30], r8
mov qword ptr [rsp + 0x38], r10
; la marche BORNÉE (I1, charte § 8) : NumberOfNames (EXP_NBNOMS @ +0x18)
; lu UNE fois — la borne vit en REGISTRE (r10) le temps de la boucle,
; sauvée par push/pop autour du memcmp ; la table des noms (EXP_ADRNOMS
; @ +0x20) dérivée une fois
mov r9d, dword ptr [r10 + 0x20]
lea r9, [r8 + r9]
mov r10d, dword ptr [r10 + 0x18]
xor eax, eax
.boucle:
cmp rax, r10
jae .nom_absent
mov r11d, dword ptr [r9 + rax*4]
add r11, qword ptr [rsp + 0x30]
mov rdx, qword ptr [rsp + 0x20]
mov r8, qword ptr [rsp + 0x28]
; l'unique appel direct du bloc (I2) : memcmp libc-02 (b20002, l'héritage
; scellé M1 — (ptr1, ptr2, n) → eax) ; trois pushes + 0x28 = 64 : le
; cadre demeure aligné pour l'appel
push rax
push r10
push r9
sub rsp, 0x28
mov rcx, r11
call MEMCMP
add rsp, 0x28
pop r9
pop r10
; le verdict de memcmp pose les drapeaux, l'indice revient APRÈS — le pop
; ne touche PAS les drapeaux : les deux traversent
test eax, eax
pop rax
jne .suivant
; ÉGALITÉ — l'ordinal (u16, EXP_ADRORD @ +0x24) puis la fonction (le RVA
; du stub, EXP_ADRFONC @ +0x1C) ; l'ordinal est un indice dans la table
; des fonctions (I1)
mov rdx, qword ptr [rsp + 0x38]
mov r11d, dword ptr [rdx + 0x24]
mov rdx, qword ptr [rsp + 0x30]
lea r11, [rdx + r11]
movzx ecx, word ptr [r11 + rax*2]
mov rdx, qword ptr [rsp + 0x38]
mov r11d, dword ptr [rdx + 0x1C]
mov rdx, qword ptr [rsp + 0x30]
lea r11, [rdx + r11]
mov r11d, dword ptr [r11 + rcx*4]
lea rdx, [rdx + r11]
; I3 : le MOTIF D'ABORD (MOTIF_STUB 4C 8B D1 B8 — les quatre octets du
; stub natif), l'imm32 à +4 (OFF_SSN) ENSUITE — jamais l'inverse ; un stub
; divergent = hook ou ère inconnue = refus NOMMÉ (-4), le numéro n'est PAS
; extrait (charte § 2)
cmp dword ptr [rdx], 0xB8D18B4C
jne .stub_divergent
mov eax, dword ptr [rdx + 4]
add rsp, 0x48
ret
.suivant:
add rax, 1
jmp .boucle
.nom_absent:
mov rax, -1
add rsp, 0x48
ret
.stub_divergent:
mov rax, -4
add rsp, 0x48
ret
.span_invalide:
mov rax, -5
ret
.pas_module:
mov rax, -2
ret
.eat_absente:
mov rax, -3
ret
