; tls13-09-f25519-add · brouillon étiqueté — spec tls13-09:R1, bloc carte h100009
; f25519 : L'ADDITION RÉDUITE — cinq additions membres à membres, UNE passe
; de tls13-12 (le gardien) : le résultat est TOUJOURS fortement réduit (< p).
; Le miroir win du contrat av-07 (M7) : la même arithmétique, l'ABI msx64
; (rcx/rdx au lieu de rdi/rsi) — la notation ré-écrit, le contrat se cite.
; rcx = a (le premier opérande, 5 membres = 40 o — la sortie ÉCRASE a,
; miroir av-07 Q2) · rdx = b (5 membres) · P3 les membres des deux opérandes
; < 2^52 (l'invariant — les VALEURS peuvent être lâches < 2^255 : la somme
; membre à membre < 2^53 ne déborde JAMAIS l'u64, la représentation est
; EXACTE, l'équivalence mod p vit dans la passe) · Q1 la sortie ≡ a + b
; (mod p) et < p (la démonstration CITÉE d'av-07 Q1 : a + b < 2·2^255, la
; passe ramène < 2^255 + 2^206 < 2p, le gel retranche) · Q2 membres de
; sortie < 2^52 · Q3 rax = 0.
; COMPOSITION DÉCLARÉE (I1) : tls13-12 UNE fois, à l'adresse scellée — la
; somme de cinq membres < 2^53 respecte sa borne d'entrée 2^57. Le temps
; constant PAR CONSTRUCTION (I2 : les intermédiaires de l'échelle tls13-13
; sont des secrets — le flot d'additions est sans AUCUNE branche de
; données, la propriété est gratuite et la spec la NOMME). AUCUNE entrée
; IAT, AUCUN site syscall (charte § 7) ; aucun état détenu (charte § 6) ;
; aucun registre non volatil détruit (I4) ; la croissance du slot est NOP,
; 0x90 (charte § 8). AUCUN déplacement RIP — tout vit en registres.
; 0 push + sub rsp, 0x28 (40 o = l'ombre msx64 0x20 + l'alignement 8 :
; entrée ≡ 8 → 8−40 ≡ 0 (mod 16) au point d'appel) — les DEUX opérandes
; lues AVANT la passe, la sortie écrite À a, la pile ne porte RIEN.
mov rax, qword ptr [rdx]
add qword ptr [rcx], rax
mov rax, qword ptr [rdx + 8]
add qword ptr [rcx + 8], rax
mov rax, qword ptr [rdx + 16]
add qword ptr [rcx + 16], rax
mov rax, qword ptr [rdx + 24]
add qword ptr [rcx + 24], rax
mov rax, qword ptr [rdx + 32]
add qword ptr [rcx + 32], rax
sub rsp, 0x28
call TLS12
add rsp, 0x28
xor eax, eax
ret
