; sonde-session · LA SONDE HISSÉE UNE FOIS PAR SESSION POUR TOUS LES
; CORRIDORS (la condition nommée de fnvan0zes, le hoisting EXIGÉ par
; l'instruction 0g3400vql : le comptage cpuid par session == 1) ; le verdict
; en rax ET r10 : bit0 = PCLMULQDQ (leaf 1 ECX bit 1) ; bit1 = AES-NI (leaf 1
; ECX bit 25) ; bit2 = SHA-NI (leaf 7 EBX bit 29) ; bit3 = OSXSAVE (leaf 1
; ECX bit 27) ; rbx SAUVÉ (msx64 non-volatil — cpuid le détruit) ; le sondage
; est PUBLIC : aucune donnée secrète ne le traverse ; la sonde VIT à
; l'appelant — les couloirs ne sondent PLUS par appel
push rbx
xor r10d, r10d
mov eax, 1
cpuid
test ecx, 0x2
jz .pas_pclmul
or r10d, 1
.pas_pclmul:
test ecx, 0x2000000
jz .pas_aes
or r10d, 2
.pas_aes:
test ecx, 0x8000000
jz .pas_xsave
or r10d, 8
.pas_xsave:
mov eax, 7
xor ecx, ecx
cpuid
test ebx, 0x20000000
jz .pas_sha
or r10d, 4
.pas_sha:
mov eax, r10d
pop rbx
ret
