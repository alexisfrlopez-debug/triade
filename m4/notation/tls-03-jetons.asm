; tls-03-jetons · bloc jetons SSPI (descripteurs) · spec tls-03:R1 · bloc carte g70003
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x6180, taille 320 octets
; Dépendances : feuille pure ; propriétaire T5 de la mise en page SecBufferDesc/SecBuffer (types 0/1/2, MAX_JETON 16384, tailles de flux en [rsp+0x28] pour le type 1 — convention cadre contigu : en-tête AVANT le clair, queue APRÈS)
; Notation explicite générée par outils/auteur.py depuis brouillons/tls-03-jetons.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 284 o · padding : 36 o (NOP)
; Étiquettes résolues : .poignee=0x61f0, .emission=0x6227, .refus_longueur=0x6290, .refus_type=0x6296
cmp ecx, 3
jae 0x6296
test ecx, ecx
jz 0x61f0
cmp ecx, 1
je 0x6227
mov dword ptr [r9], 0
lea r11, [r9 + 0x10]
mov qword ptr [r9 + 8], r11
mov dword ptr [r9 + 4], 4
mov dword ptr [r9 + 0x10], r8d
mov dword ptr [r9 + 0x14], 1
mov qword ptr [r9 + 0x18], rdx
mov qword ptr [r9 + 0x20], 0
mov qword ptr [r9 + 0x28], 0
mov qword ptr [r9 + 0x30], 0
mov qword ptr [r9 + 0x38], 0
mov qword ptr [r9 + 0x40], 0
mov qword ptr [r9 + 0x48], 0
xor eax, eax
ret
cmp r8, 16384
ja 0x6290
mov dword ptr [r9], 0
lea r11, [r9 + 0x10]
mov qword ptr [r9 + 8], r11
mov dword ptr [r9 + 4], 1
mov dword ptr [r9 + 0x10], r8d
mov dword ptr [r9 + 0x14], 2
mov qword ptr [r9 + 0x18], rdx
xor eax, eax
ret
mov r11, [rsp + 0x28]
mov r10d, [r11 + 8]
cmp r8, r10
ja 0x6290
mov r10d, [r11]
mov r11d, [r11 + 4]
mov dword ptr [r9], 0
lea rax, [r9 + 0x10]
mov qword ptr [r9 + 8], rax
mov dword ptr [r9 + 4], 3
mov dword ptr [r9 + 0x10], r10d
mov dword ptr [r9 + 0x14], 7
mov rax, rdx
sub rax, r10
mov qword ptr [r9 + 0x18], rax
mov dword ptr [r9 + 0x20], r8d
mov dword ptr [r9 + 0x24], 1
mov qword ptr [r9 + 0x28], rdx
mov dword ptr [r9 + 0x30], r11d
mov dword ptr [r9 + 0x34], 6
lea rax, [rdx + r8]
mov qword ptr [r9 + 0x38], rax
xor eax, eax
ret
mov eax, 1
ret
mov eax, 2
ret
