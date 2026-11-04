; tcp-11-journal-r2 · brouillon étiqueté — spec tcp-11:R2, bloc carte f61011
; LA LIGNE DU PATRIMOINE M2 : préfixe + décimale optionnelle + suffixe,
; composés dans le cadre privé puis émis en UNE écriture, sous verrou —
; l'instance Linux du contrat scellé 0.3.0. Les cinq arguments nommés
; (frag-con : SysV — rdi/rsi/rdx/rcx/r8, TOUS en registres, l'ABI porte
; cinq arguments sans pile ; Windows — rcx/rdx/r8/r9 puis la loge pile,
; la discipline I4 de R1).
; LE VERROU DU PROFIL (I1, frag-con) : l'instance Windows prend la section
; critique kernel32 (initialisée par tcp-12) ; l'instance Linux prend le
; qword tournant au plan de l'image (0x3800, NÉ DÉVERROUROUILLÉ au
; chargement — AUCUNE initialisation, P5) : xchg à mémoire (verrou implicite
; ISA) pose 1 et rend l'ancien — ancien nul : verrou acquis ; sinon pause
; et on réessaie ; la remise est un store simple (x86-64 : ordre total).
; Le verdict d'écriture traverse le verrou en r14 (volatile — rendu APRÈS
; la remise, Q3 : jamais le verrou pris en sortant).
; Cadre : 5 push + 0x50 (80 = tampon 64 + brouillon itoa 16), multiple de
; 16 — tout appel part aligné.
@A_MEMCPY = 0x1080
@A_ITOA = 0x1180
@A_STRLEN = 0x1140
@A_ECRIRE = 0x1000
@VERROU = 0x3800
@SENTINELLE = 0xFFFFFFFF
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x50
mov rbx, rdi
mov r12, rsi
mov r13, rdx
mov r14, rcx
mov r15, r8
; --- prendre le verrou (tournant, xchg à verrou implicite) ---
mov esi, 1
.reattendre:
xchg rsi, qword ptr [rip + @VERROU]
test rsi, rsi
jz .acquis
pause
jmp .reattendre
.acquis:
; --- composer : préfixe ---
mov rdi, rsp
mov rsi, rbx
mov rdx, r12
call @A_MEMCPY
; --- le champ numérique (sentinelle : pas de champ) ---
cmp r13d, @SENTINELLE
je .sans_champ
mov edi, r13d
lea rsi, [rsp + 0x40]
call @A_ITOA
lea rdi, [rsp + 0x40]
call @A_STRLEN
mov rdi, rsp
add rdi, r12
lea rsi, [rsp + 0x40]
mov rdx, rax
; la longueur est capturée AVANT l'appel : memcpy rend dst (une adresse), jamais la longueur
add r12, rax
call @A_MEMCPY
.sans_champ:
; --- le suffixe ---
lea rdi, [rsp]
add rdi, r12
mov rsi, r14
mov rdx, r15
call @A_MEMCPY
add r12, r15
; --- UNE écriture, le verdict brut conservé ---
mov edi, 1
mov rsi, rsp
mov rdx, r12
call @A_ECRIRE
mov r14, rax
; --- rendre le verrou, puis le verdict (jamais l'inverse — Q3) ---
mov qword ptr [rip + @VERROU], 0
mov rax, r14
add rsp, 0x50
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
