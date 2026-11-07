; loupe-03 · fermer : la session close, jamais une poignée pendante · spec loupe-03:R1
; L'IDEMPOTENCE PAR CONSTRUCTION (V3/Q4 : session close → rax = 0, AUCUN
; appel CloseHandle — le harnais les compte —, rien bougé : le test AVANT
; tout) ; la fermeture réelle : CloseHandle UNE fois (Q1 — l'échec
; CONSOMMÉ : gle lu pour le harnais, la suite a lieu quand même, rax = 0
; quand même — E1 : « jamais une poignée pendante » prime, jamais le
; mensonge -6 d'une session close propre) ; loupe-04 le cadre re-vierge
; (Q2) ; L'HYGIÈNE DES ZONES (Q3 : le journal nombre = 0, le motif
; longueur = 0, le mode saisie = 0, les empreintes effacées par libc-07 —
; les zones de session ne fuient JAMAIS d'un fichier à l'autre) ; I1 : le
; disque n'est PAS touché (fermer ne sauvegarde RIEN — la sauvegarde est
; un geste délibéré à loupe-17).
push rbx
sub rsp, 0x20
lea rbx, [rip + CADRE]
cmp qword ptr [rbx + 528], -1
je .deja
mov rcx, qword ptr [rbx + 528]
call qword ptr [rip + IAT_CLOSEHANDLE]
test eax, eax
jnz .propre
call qword ptr [rip + IAT_GETLASTERROR]
.propre:
call LOUPE04
lea rax, [rip + JOURNAL]
mov dword ptr [rax + 4096], 0
lea rax, [rip + MOTIF]
mov dword ptr [rax + 32], 0
lea rax, [rip + SAISIE]
mov dword ptr [rax], 0
lea rcx, [rip + EMPREINTES]
xor edx, edx
mov r8d, 48
call LIBC07
.deja:
xor eax, eax
add rsp, 0x20
pop rbx
ret
