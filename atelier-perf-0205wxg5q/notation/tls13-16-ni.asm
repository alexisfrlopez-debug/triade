; tls13-16-ni · LA VARIANTE AES-NI du chiffrement de bloc — le chemin du couloir B (0205wxg5q) · spec tls13-16:R1 (LE MÊME CONTRAT — R4)
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0xCE00 (la marge .text2 VIERGE après la famille sha 0xC3C0 — AUCUN octet du scellé touché, le modèle OPT-01)
; Domaine : tls13 (M4) · Dépendances : tls13-16 SCELLÉ à 0xDF00 (LE REPLI — l'appel À SON ADRESSE, R7) ; les clés de tour au contexte (P1)
; LE CHEMIN AES-NI : l'état chargé (movdqu), pxor RK[0], NEUF aesenc (RK[1..9]), aesenclast (RK[10]) — LES DIX TOURS EN DIX INSTRUCTIONS
; (le GPR scellé les calcule par tables — la descente à l'ISA du hot path mesuré du chemin crypto M4) ;
; LE DISPATCH : la sonde CPUID feuille 1 ECX bit 25 (AES-NI) — la même sonde RAPPELÉE UNE FOIS PAR APPEL (le modèle shani-01 : le sondage
; par bloc eût mangé le gain) ; le repli : LE SCELLÉ APPELÉ À SON ADRESSE 0xDF00.
; LE CONTRAT (tls13-16:R1 À LA LETTRE — R4) : P1 les clés de tour (176 o), P2 l'entrée (16 o), P3 la sortie (16 o — peut chevaucher),
; Q1 AES-128 direct (FIPS 197 + SP 800-38A F.1.1), Q2 les clés et l'entrée INTACTES, Q3 rax = 0, I1-I3 (le flot sans branche de données,
; AUCUNE entrée IAT, les non-volatils rendus, NOP 0x90).
; Notation explicite — keystone assemble, le round-trip capstone 100 % exigé au build.
push rbx
push r12
push r13
push r14
sub rsp, 0x28
; LES ARGUMENTS aux registres SÛRS (CPUID détruit rax/rbx/rcx/rdx)
mov r12, rcx
mov r13, rdx
mov r14, r8
; LA SONDE CPUID (rbx SAUVÉ par le push — la convention) : feuille 1, ECX bit 25
mov eax, 1
xor ecx, ecx
cpuid
test ecx, 0x2000000
jz .repli
; LE CHEMIN AES-NI : les dix tours en dix instructions
movdqu xmm0, [r13]
movdqu xmm1, [r12]
pxor xmm0, xmm1
movdqu xmm1, [r12 + 16]
aesenc xmm0, xmm1
movdqu xmm1, [r12 + 32]
aesenc xmm0, xmm1
movdqu xmm1, [r12 + 48]
aesenc xmm0, xmm1
movdqu xmm1, [r12 + 64]
aesenc xmm0, xmm1
movdqu xmm1, [r12 + 80]
aesenc xmm0, xmm1
movdqu xmm1, [r12 + 96]
aesenc xmm0, xmm1
movdqu xmm1, [r12 + 112]
aesenc xmm0, xmm1
movdqu xmm1, [r12 + 128]
aesenc xmm0, xmm1
movdqu xmm1, [r12 + 144]
aesenc xmm0, xmm1
movdqu xmm1, [r12 + 160]
aesenclast xmm0, xmm1
movdqu [r14], xmm0
xor eax, eax
jmp .sortie
.repli:
; LE REPLI : le SCELLÉ appelé à SON ADRESSE (R7 — jamais réécrit) —
; les arguments REPOSÉS à leurs registres msx64 (rcx/rdx/r8)
mov rcx, r12
mov rdx, r13
mov r8, r14
call 0xDF00
jmp .sortie
.sortie:
add rsp, 0x28
pop r14
pop r13
pop r12
pop rbx
ret
