; tls13-12-f25519-propager-geler · brouillon étiqueté — spec tls13-12:R1, bloc carte h100012
; LE GARDIEN DE L'INVARIANT radix 2^51 — le bloc fusionné (UNE frontière pour
; les DEUX miroirs M7 : av-06 la propagation + av-10 le gel — LA DIVERGENCE
; NOMMÉE de la découpe M9, I3 de tls13-11). La passe SÉQUENTIELLE 0→4 :
; chaque membre coupé à 51 bits, le trop-plein passe au suivant, le
; débordement du cinquième REVIENT au premier multiplié par 19 (2^255 ≡ 19) ;
; PUIS le gel : retrancher p si et seulement si la valeur représentée est
; ≥ p. FEUILLE : aucun appel, aucun non-volatil, 0 octet de pile (I4/I5).
; rcx = la valeur (5 membres u64, 40 o — la sortie ÉCRASE) · P2 chaque
; membre < 2^57 en entrée, la valeur post-passe < 2^255 + 2^206 < 2p (la
; borne du gel — les producteurs 09/10/11 la démontrent avant l'appel) ·
; Q1 membres 1..4 < 2^51, membre 0 < 2^51 + 19·2^6 < 2^52 ; Q2 le gel
; laisse la valeur < p — OCTET-IDENTIQUE si déjà < p, zéro si elle valait
; exactement p · Q3 rax = 0.
; LE GEL SANS BRANCHE DE DONNÉES (I2 — L'AMÉLIORATION NOMMÉE sur le miroir
; av-10 qui branchait jb/ja) : la comparaison membre à membre DU CINQUIÈME
; AU PREMIER produit le drapeau « ≥ p » en registre SANS ÉCRIRE (les
; membres 1..4 post-passe sont ≤ 2^51−1 : l'égalité avec le membre de p
; suffit — le dépassement strict y est IMPOSSIBLE, la comparaison reduces
; à l'égalité), le masque 0/−1 DIFFUSÉ PAR SAR, la soustraction
; conditionnelle PAR ET LOGIQUE. Les membres de p (I3) : le membre 0 =
; 2^51 − 19 (F25519_P0 du plan, l'erratum d'écriture d'av-10 consigné par
; la spec elle-même — la notation RE-DÉRIVE, le juge est le code), les
; membres 1..4 = 2^51 − 1 (le masque M51 DU PLAN). Le masque M51 et la
; constante 19 en IMMÉDIATS — aucune donnée RIP (I1). Le temps est
; constant PAR CONSTRUCTION (I2/I3 des specs appelantes — le flot est sans
; AUCUNE branche de données). AUCUNE entrée IAT, AUCUN site syscall
; (charte § 7) ; NOP, 0x90 (charte § 8).
; 0 octet de pile : FEUILLE nue — l'entrée ≡ 8 (mod 16) n'exige rien.
movabs r10, 0x7ffffffffffff
; --- LA PASSE SÉQUENTIELLE 0→4 (I1 : le membre i masqué AVANT le i+1) ------
mov rax, qword ptr [rcx]
mov rdx, rax
shr rdx, 51
and rax, r10
mov r8, qword ptr [rcx + 8]
add r8, rdx
mov rdx, r8
shr rdx, 51
and r8, r10
mov qword ptr [rcx + 8], r8
mov r9, qword ptr [rcx + 16]
add r9, rdx
mov rdx, r9
shr rdx, 51
and r9, r10
mov qword ptr [rcx + 16], r9
mov r8, qword ptr [rcx + 24]
add r8, rdx
mov rdx, r8
shr rdx, 51
and r8, r10
mov qword ptr [rcx + 24], r8
mov r9, qword ptr [rcx + 32]
add r9, rdx
mov rdx, r9
shr rdx, 51
and r9, r10
mov qword ptr [rcx + 32], r9
imul rdx, rdx, 19
add rax, rdx
mov qword ptr [rcx], rax
; --- LE GEL SANS BRANCHE (I2) : le drapeau « ≥ p » du 5e au 1er ------------
; les membres 1..4 : l'égalité avec 2^51−1 (le membre de p) — le strict
; dépassement y est impossible post-passe (masqués à 2^51−1) ; le OU des
; XOR l'accumule en registre SANS ÉCRIRE
xor r9d, r9d
mov rax, qword ptr [rcx + 32]
xor rax, r10
or r9, rax
mov rax, qword ptr [rcx + 24]
xor rax, r10
or r9, rax
mov rax, qword ptr [rcx + 16]
xor rax, r10
or r9, rax
mov rax, qword ptr [rcx + 8]
xor rax, r10
or r9, rax
; le membre 0 : ≥ 2^51 − 19 (F25519_P0 — la borne du gel)
movabs r11, 0x7ffffffffffed
mov rax, qword ptr [rcx]
cmp rax, r11
setae r8b
test r9, r9
sete r9b
and r9d, r8d
shl r9, 63
sar r9, 63
; --- la soustraction conditionnelle PAR ET LOGIQUE (le masque 0/−1) --------
mov rdx, r11
and rdx, r9
sub rax, rdx
mov qword ptr [rcx], rax
mov rax, qword ptr [rcx + 8]
mov rdx, r10
and rdx, r9
sub rax, rdx
mov qword ptr [rcx + 8], rax
mov rax, qword ptr [rcx + 16]
mov rdx, r10
and rdx, r9
sub rax, rdx
mov qword ptr [rcx + 16], rax
mov rax, qword ptr [rcx + 24]
mov rdx, r10
and rdx, r9
sub rax, rdx
mov qword ptr [rcx + 24], rax
mov rax, qword ptr [rcx + 32]
mov rdx, r10
and rdx, r9
sub rax, rdx
mov qword ptr [rcx + 32], rax
xor eax, eax
ret
