; sys-03-ecriture · l'écriture directe — la twin de hello-02 par NtWriteFile ·
; spec sys-03:R1 · bloc carte g90003
; LE premier usage réel du domaine : émettre LA MÊME LIGNE que hello-02
; (WriteFile par l'IAT kernel32, le scellé M0) par NtWriteFile EN SYSCALL
; DIRECT — zéro entrée IAT (I1 : la preuve STRUCTURELLE), le SSN résolu au
; geste même (Q2). La ligne est le FIXTURE PARTAGÉ (I4 : CITÉ par
; déplacement — le fixture-ligne de hello-02 à R_SYS_LIGNE, byte-exact le
; MESSAGE de m0/build_m0.py, 33 octets utiles) ; le nom est le fixture-nom
; à R_SYS_NOM (« NtWriteFile », 11 octets — la CLEF, erratum M8-(b) : la
; couche I disait 10, la mesure fait foi). Les constantes au plan
; d'adressage (m8/layout.py, source unique) ; le harnais re-vérifie.
; Le bloc sauvegarde ce qu'il utilise (I6 : rbx le handle, rbp la base —
; rdx de sys-03 est un ARGUMENT de sys-02, la ABI force le sauvetage) ;
; le cadre 0x58 : l'ombre 0x20 + les CINQ arguments de pile (0x28) + le
; IO_STATUS_BLOCK (0x10 — la pile du bloc, I2 : zone morte au retour).
push rbx
push rbp
sub rsp, 0x58
mov rbx, rdx
mov rbp, rcx
; Q2/I3 : résoudre AVANT d'émettre — sys-02 au geste même, JAMAIS un
; numéro en cache (charte § 6)
lea rcx, [rip + NOM]
mov edx, 11
mov r8, rbp
call SYS02
; I5 : échec de résolution = AUCUN syscall émis (la garde la plus
; importante du bloc) ; Q4 : rdx consigne LA CAUSE — le verdict du
; résolveur, nommé, jamais muet
test rax, rax
js .resolution_echouee
; rax = LE SSN (zéro-étendu, positif) — il RESTE en rax jusqu'au site
; syscall : P1 de sys-01, le numéro traverse le bloc entier
; Q3 : les NEUF arguments dans l'ordre NT — quatre en registres, CINQ à
; [rsp+0x28]+ AU MOMENT du syscall (charte § 4 : l'ombre et la pile
; d'appel de sys-01 sont AUSSI celles du noyau — le charme du trombone)
mov rcx, rbx
xor edx, edx
xor r8d, r8d
xor r9d, r9d
lea r10, [rsp + 0x48]
mov qword ptr [rsp + 0x20], r10
lea r10, [rip + LIGNE]
mov qword ptr [rsp + 0x28], r10
mov qword ptr [rsp + 0x30], 33
mov qword ptr [rsp + 0x38], 0
mov qword ptr [rsp + 0x40], 0
call SYS01
; Q4/I7 : le NTSTATUS n'est JAMAIS muet — succès = 0 NOMMÉ ; échec = -6
; avec le brut consigné en rdx ; la divergence rax/IO_STATUS_BLOCK est
; -6 (le noyau ne parle pas deux fois — un désaccord est une anomalie)
test eax, eax
jne .status_nonnul
cmp dword ptr [rsp + 0x48], 0
jne .status_iosb
xor eax, eax
add rsp, 0x58
pop rbp
pop rbx
ret
.status_nonnul:
mov rdx, rax
mov rax, -6
jmp .epilogue
.status_iosb:
mov edx, dword ptr [rsp + 0x48]
mov rax, -6
jmp .epilogue
.resolution_echouee:
mov rdx, rax
mov rax, -1
.epilogue:
add rsp, 0x58
pop rbp
pop rbx
ret
