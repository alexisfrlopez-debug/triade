; tls13-11-f25519-mul · brouillon étiqueté — spec tls13-11:R1, bloc carte h100011
; f25519 : LA MULTIPLICATION — le bloc arithmétique le plus long du domaine,
; cœur de l'échelle (miroir win du contrat av-09, M7). L'ÉCOLE 5×5 : 25
; multiplications u64×u64→u128 accumulées en DIX logements u128 sur la PILE
; (I1 : le sous-cadre 0xC0 = 160 o de logements + 32 o d'ombre — le DIXIÈME
; reste NUL, il porte le REPLI UNIFORME : C[4] = T[4] + 19·T[9] avec T[9]
; vide, la double boucle bornée i:0→4 × j:0→4, k = i+j ≤ 8 ; l'adressage
; [rsp + k·16] — l'échelle 16 n'existe pas en x86, la notation DÉROULE et
; le montre). L'emprunt sortant d'un logement est IMPOSSIBLE : chacun
; reçoit < 5·2^104 < 2^107, la marge au 128 bits est 2^21 (I2). LE REPLI :
; C[k] = T[k] + 19·T[k+5] en u128 (2^255 ≡ 19 — le mul par 19 en deux
; morceaux : mul r8 pour le bas AVEC sa retenue, imul pour le haut, la
; marge < 2^48 ferme la question). L'EXTRACTION (I3, la recette av-09 I3
; citée) : le sommet d'abord — c = C4 >> 51 (shrd, le u128), C0 += 19·c ;
; la chaîne r0..r3 avec reports 51 bits (shrd à chaque cran) ; r4 =
; (C4&M51) + c3 masqué ; LE RETOUR FINAL r0 += 19·(r4 >> 51) — r0 sort <
; 2^51 + 19·2^12 < 2^52, la borne d'entrée 2^57 de tls13-12 respire.
; rcx = a (5 membres — la sortie ÉCRASE a) · rdx = b (5 membres) · les
; VALEURS lâches < 2^255 admises (l'école dépend des MEMBRES, le repli
; préserve l'équivalence mod p — P2 d'av-09) · P3 membres < 2^52 · Q1 la
; sortie ≡ a·b (mod p) et < p (après repli et chaîne la valeur est <
; 2^255 + 2^206 < 2p, LA PASSE de tls13-12 clôt) · Q2 membres < 2^52 ·
; Q3 rax = 0.
; COMPOSITION DÉCLARÉE (I3) : tls13-12 UNE fois — LA DIVERGENCE NOMMÉE de
; la découpe M9 : le M7 appelait av-06 PUIS av-10 [deux frontières], le M9
; les FUSIONNE en tls13-12 : une seule frontière d'appel, la même
; arithmétique. Le temps constant PAR CONSTRUCTION (I4 : les 25
; multiplications s'exécutent TOUJOURS — les intermédiaires de l'échelle
; sont des secrets, aucune branche ne les lit : LE BLOC EST SANS AUCUNE
; BRANCHE). rbx retenu (push/pop — le pointeur b survit aux mul qui
; détruisent rdx). AUCUNE entrée IAT, AUCUN site syscall (charte § 7) ;
; aucun état détenu (charte § 6) ; aucun non-volatil détruit (I6) ; NOP,
; 0x90 (charte § 8). AUCUN déplacement RIP — M51, 19 et les reports en
; immédiats et registres.
; push rbx (8 o) + sub rsp, 0xc0 (192 o) : entrée ≡ 8 → 8−8−192 ≡ 0
; (mod 16) au point d'appel ; [rsp+0x20..0xbf] = les DIX logements ;
; [rsp..0x1f] = l'ombre de tls13-12 (le bas du cadre, SOUS les logements —
; la frontière est tenue).
push rbx
sub rsp, 0xc0
mov rbx, rdx
; --- le zeroing des DIX logements (le dixième porte le repli uniforme) -----
xor eax, eax
mov qword ptr [rsp + 0x20], rax
mov qword ptr [rsp + 0x28], rax
mov qword ptr [rsp + 0x30], rax
mov qword ptr [rsp + 0x38], rax
mov qword ptr [rsp + 0x40], rax
mov qword ptr [rsp + 0x48], rax
mov qword ptr [rsp + 0x50], rax
mov qword ptr [rsp + 0x58], rax
mov qword ptr [rsp + 0x60], rax
mov qword ptr [rsp + 0x68], rax
mov qword ptr [rsp + 0x70], rax
mov qword ptr [rsp + 0x78], rax
mov qword ptr [rsp + 0x80], rax
mov qword ptr [rsp + 0x88], rax
mov qword ptr [rsp + 0x90], rax
mov qword ptr [rsp + 0x98], rax
mov qword ptr [rsp + 0xa0], rax
mov qword ptr [rsp + 0xa8], rax
mov qword ptr [rsp + 0xb0], rax
mov qword ptr [rsp + 0xb8], rax
mov r8, 19
; --- L'ÉCOLE 5×5 DÉROULÉE (i : 0→4, j : 0→4, k = i+j — I1) -------------------
; a_i RECHARGÉ AVANT CHAQUE mul : mul détruit rax (rdx:rax = rax·[rbx+8j]
; — le produit ÉCRASE l'opérande), le rechargement est LE geste de l'école
mov rax, qword ptr [rcx]
mul qword ptr [rbx]
add qword ptr [rsp + 0x20], rax
adc qword ptr [rsp + 0x28], rdx
mov rax, qword ptr [rcx]
mul qword ptr [rbx + 8]
add qword ptr [rsp + 0x30], rax
adc qword ptr [rsp + 0x38], rdx
mov rax, qword ptr [rcx]
mul qword ptr [rbx + 16]
add qword ptr [rsp + 0x40], rax
adc qword ptr [rsp + 0x48], rdx
mov rax, qword ptr [rcx]
mul qword ptr [rbx + 24]
add qword ptr [rsp + 0x50], rax
adc qword ptr [rsp + 0x58], rdx
mov rax, qword ptr [rcx]
mul qword ptr [rbx + 32]
add qword ptr [rsp + 0x60], rax
adc qword ptr [rsp + 0x68], rdx
mov rax, qword ptr [rcx + 8]
mul qword ptr [rbx]
add qword ptr [rsp + 0x30], rax
adc qword ptr [rsp + 0x38], rdx
mov rax, qword ptr [rcx + 8]
mul qword ptr [rbx + 8]
add qword ptr [rsp + 0x40], rax
adc qword ptr [rsp + 0x48], rdx
mov rax, qword ptr [rcx + 8]
mul qword ptr [rbx + 16]
add qword ptr [rsp + 0x50], rax
adc qword ptr [rsp + 0x58], rdx
mov rax, qword ptr [rcx + 8]
mul qword ptr [rbx + 24]
add qword ptr [rsp + 0x60], rax
adc qword ptr [rsp + 0x68], rdx
mov rax, qword ptr [rcx + 8]
mul qword ptr [rbx + 32]
add qword ptr [rsp + 0x70], rax
adc qword ptr [rsp + 0x78], rdx
mov rax, qword ptr [rcx + 16]
mul qword ptr [rbx]
add qword ptr [rsp + 0x40], rax
adc qword ptr [rsp + 0x48], rdx
mov rax, qword ptr [rcx + 16]
mul qword ptr [rbx + 8]
add qword ptr [rsp + 0x50], rax
adc qword ptr [rsp + 0x58], rdx
mov rax, qword ptr [rcx + 16]
mul qword ptr [rbx + 16]
add qword ptr [rsp + 0x60], rax
adc qword ptr [rsp + 0x68], rdx
mov rax, qword ptr [rcx + 16]
mul qword ptr [rbx + 24]
add qword ptr [rsp + 0x70], rax
adc qword ptr [rsp + 0x78], rdx
mov rax, qword ptr [rcx + 16]
mul qword ptr [rbx + 32]
add qword ptr [rsp + 0x80], rax
adc qword ptr [rsp + 0x88], rdx
mov rax, qword ptr [rcx + 24]
mul qword ptr [rbx]
add qword ptr [rsp + 0x50], rax
adc qword ptr [rsp + 0x58], rdx
mov rax, qword ptr [rcx + 24]
mul qword ptr [rbx + 8]
add qword ptr [rsp + 0x60], rax
adc qword ptr [rsp + 0x68], rdx
mov rax, qword ptr [rcx + 24]
mul qword ptr [rbx + 16]
add qword ptr [rsp + 0x70], rax
adc qword ptr [rsp + 0x78], rdx
mov rax, qword ptr [rcx + 24]
mul qword ptr [rbx + 24]
add qword ptr [rsp + 0x80], rax
adc qword ptr [rsp + 0x88], rdx
mov rax, qword ptr [rcx + 24]
mul qword ptr [rbx + 32]
add qword ptr [rsp + 0x90], rax
adc qword ptr [rsp + 0x98], rdx
mov rax, qword ptr [rcx + 32]
mul qword ptr [rbx]
add qword ptr [rsp + 0x60], rax
adc qword ptr [rsp + 0x68], rdx
mov rax, qword ptr [rcx + 32]
mul qword ptr [rbx + 8]
add qword ptr [rsp + 0x70], rax
adc qword ptr [rsp + 0x78], rdx
mov rax, qword ptr [rcx + 32]
mul qword ptr [rbx + 16]
add qword ptr [rsp + 0x80], rax
adc qword ptr [rsp + 0x88], rdx
mov rax, qword ptr [rcx + 32]
mul qword ptr [rbx + 24]
add qword ptr [rsp + 0x90], rax
adc qword ptr [rsp + 0x98], rdx
mov rax, qword ptr [rcx + 32]
mul qword ptr [rbx + 32]
add qword ptr [rsp + 0xa0], rax
adc qword ptr [rsp + 0xa8], rdx
; --- LE REPLI : C[k] = T[k] + 19·T[k+5] en u128 (I2) --------------------------
mov rax, qword ptr [rsp + 0x70]
mul r8
add rax, qword ptr [rsp + 0x20]
mov r10, rdx
adc r10, qword ptr [rsp + 0x28]
imul r11, qword ptr [rsp + 0x78], 19
add r10, r11
mov qword ptr [rsp + 0x20], rax
mov qword ptr [rsp + 0x28], r10
mov rax, qword ptr [rsp + 0x80]
mul r8
add rax, qword ptr [rsp + 0x30]
mov r10, rdx
adc r10, qword ptr [rsp + 0x38]
imul r11, qword ptr [rsp + 0x88], 19
add r10, r11
mov qword ptr [rsp + 0x30], rax
mov qword ptr [rsp + 0x38], r10
mov rax, qword ptr [rsp + 0x90]
mul r8
add rax, qword ptr [rsp + 0x40]
mov r10, rdx
adc r10, qword ptr [rsp + 0x48]
imul r11, qword ptr [rsp + 0x98], 19
add r10, r11
mov qword ptr [rsp + 0x40], rax
mov qword ptr [rsp + 0x48], r10
mov rax, qword ptr [rsp + 0xa0]
mul r8
add rax, qword ptr [rsp + 0x50]
mov r10, rdx
adc r10, qword ptr [rsp + 0x58]
imul r11, qword ptr [rsp + 0xa8], 19
add r10, r11
mov qword ptr [rsp + 0x50], rax
mov qword ptr [rsp + 0x58], r10
mov rax, qword ptr [rsp + 0xb0]
mul r8
add rax, qword ptr [rsp + 0x60]
mov r10, rdx
adc r10, qword ptr [rsp + 0x68]
imul r11, qword ptr [rsp + 0xb8], 19
add r10, r11
mov qword ptr [rsp + 0x60], rax
mov qword ptr [rsp + 0x68], r10
; --- LE SOMMET : c = C4 >> 51, C0 += 19·c (I3) -------------------------------
mov rax, qword ptr [rsp + 0x60]
mov rdx, qword ptr [rsp + 0x68]
mov r9, rax
shrd r9, rdx, 51
mov rax, r9
mul r8
add qword ptr [rsp + 0x20], rax
adc qword ptr [rsp + 0x28], rdx
; --- LA CHAÎNE r0..r3 avec reports 51 bits (I3) ------------------------------
movabs r10, 0x7ffffffffffff
xor r9d, r9d
mov rax, qword ptr [rsp + 0x20]
mov rdx, qword ptr [rsp + 0x28]
add rax, r9
adc rdx, 0
mov r11, rax
shrd r11, rdx, 51
and rax, r10
mov qword ptr [rcx], rax
mov r9, r11
mov rax, qword ptr [rsp + 0x30]
mov rdx, qword ptr [rsp + 0x38]
add rax, r9
adc rdx, 0
mov r11, rax
shrd r11, rdx, 51
and rax, r10
mov qword ptr [rcx + 8], rax
mov r9, r11
mov rax, qword ptr [rsp + 0x40]
mov rdx, qword ptr [rsp + 0x48]
add rax, r9
adc rdx, 0
mov r11, rax
shrd r11, rdx, 51
and rax, r10
mov qword ptr [rcx + 16], rax
mov r9, r11
mov rax, qword ptr [rsp + 0x50]
mov rdx, qword ptr [rsp + 0x58]
add rax, r9
adc rdx, 0
mov r11, rax
shrd r11, rdx, 51
and rax, r10
mov qword ptr [rcx + 24], rax
mov r9, r11
; --- r4 = (C4&M51) + c3, le RETOUR FINAL r0 += 19·(r4 >> 51) (I3) -----------
mov rax, qword ptr [rsp + 0x60]
and rax, r10
add rax, r9
mov r11, rax
shr r11, 51
and rax, r10
mov qword ptr [rcx + 32], rax
imul r11, r11, 19
add qword ptr [rcx], r11
call TLS12
xor eax, eax
add rsp, 0xc0
pop rbx
ret
