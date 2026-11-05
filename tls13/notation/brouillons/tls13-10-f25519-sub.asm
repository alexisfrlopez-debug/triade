; tls13-10-f25519-sub · brouillon étiqueté — spec tls13-10:R1, bloc carte h100010
; f25519 : LA SOUSTRACTION RÉDUITE — additionner 2p membre à membre à a,
; retrancher b par soustraction chaînée sub/sbb, UNE passe de tls13-12 (le
; gardien) : le résultat est TOUJOURS < p. Le miroir win du contrat av-08
; (M7). LA CLÉ DU GESTE : les CINQ membres de 2p = 2^256 − 38 en radix 2^51
; — (2^51 − 38), (2^51 − 1)×3, (2^52 − 1) — DÉRIVÉS PAR ARITHMÉTIQUE du
; plan (F25519_P2_MEMBRES, la source unique ; ERRATUM I1 consigné AVANT la
; notation : l'écriture « (2^51 − 38) puis (2^51 − 1)×4 » compose 2^255 −
; 38 ≡ −19 (mod p) ≠ 2p — le membre 4 est 2^52 − 1, l'écriture seule est
; fautive, le juge est le code). EN IMMÉDIATS (miroir av-08 I1 : cinq mov
; imm64, pas de déplacement RIP, le bloc reste autoporteur).
; rcx = a (5 membres — la sortie ÉCRASE a ; valeur réduite < p OU lâche
; < 2^255 : les DEUX bornes tiennent, a + 2p − b < 2^257, la passe ramène
; < 2^255 + 2^206 < 2p) · rdx = b (5 membres, valeur lâche < 2^255 admise)
; · P3 membres < 2^52 · Q1 la sortie ≡ a − b (mod p) et < p · Q2 membres
; de sortie < 2^52 · Q3 rax = 0 — OU rax = −1 NOMMÉ : l'emprunt sortant au
; cinquième membre (la pré-condition VIOLÉE par l'appelant — IMPOSSIBLE
; des appelants internes : a + 2p ≥ 2p > b) : le bloc N'ÉCRIT RIEN à a
; (le scratch meurt), l'échec E1 d'av-08 ÉLEVÉ en verdict de la table du
; domaine — LE FAIL-CLOSED WIN SE PRONONCE, il ne se tait jamais.
; LA STRUCTURE : PASSE 1 les additions a + 2p vers le SCRATCH de pile
; (chaque somme < 2^53 : AUCUNE retenue — l'ordre n'importe pas) ; PASSE 2
; la chaîne sub/sbb DU SCRATCH contre b (l'emprunt voyage en CF, les mov
; intercalés ne le touchent jamais) ; le test final VERROU fail-closed ;
; le COMMIT du scratch vers a SEULEMENT sur succès. COMPOSITION (I2) :
; tls13-12 UNE fois. Le temps constant PAR CONSTRUCTION (I3 : le flot
; sub/sbb est sans branche de données — la branche du verrou porte sur le
; CONTRAT, jamais sur un secret). AUCUNE entrée IAT, AUCUN site syscall
; (charte § 7) ; aucun état détenu (charte § 6) ; aucun non-volatil
; détruit (I5) ; NOP, 0x90 (charte § 8). AUCUN déplacement RIP.
; sub rsp, 0x48 (72 o) : entrée ≡ 8 → 8−72 ≡ 0 (mod 16) au point d'appel ;
; [rsp+0x20..0x47] = le scratch 5 membres ; [rsp..0x1f] = l'ombre de
; tls13-12 (32 o — le bas du cadre, le scratch est AU-DESSUS, la frontière
; est tenue).
sub rsp, 0x48
; --- PASSE 1 : a + 2p vers le scratch (aucune retenue, la borne < 2^53) ----
mov rax, qword ptr [rcx]
movabs r11, 0x7ffffffffffda
add rax, r11
mov qword ptr [rsp + 0x20], rax
mov rax, qword ptr [rcx + 8]
movabs r11, 0x7ffffffffffff
add rax, r11
mov qword ptr [rsp + 0x28], rax
mov rax, qword ptr [rcx + 16]
movabs r11, 0x7ffffffffffff
add rax, r11
mov qword ptr [rsp + 0x30], rax
mov rax, qword ptr [rcx + 24]
movabs r11, 0x7ffffffffffff
add rax, r11
mov qword ptr [rsp + 0x38], rax
mov rax, qword ptr [rcx + 32]
movabs r11, 0xfffffffffffff
add rax, r11
mov qword ptr [rsp + 0x40], rax
; --- PASSE 2 : − b, la chaîne sub/sbb (l'emprunt en CF, les mov muets) -----
mov rax, qword ptr [rsp + 0x20]
sub rax, qword ptr [rdx]
mov qword ptr [rsp + 0x20], rax
mov rax, qword ptr [rsp + 0x28]
sbb rax, qword ptr [rdx + 8]
mov qword ptr [rsp + 0x28], rax
mov rax, qword ptr [rsp + 0x30]
sbb rax, qword ptr [rdx + 16]
mov qword ptr [rsp + 0x30], rax
mov rax, qword ptr [rsp + 0x38]
sbb rax, qword ptr [rdx + 24]
mov qword ptr [rsp + 0x38], rax
mov rax, qword ptr [rsp + 0x40]
sbb rax, qword ptr [rdx + 32]
mov qword ptr [rsp + 0x40], rax
jc .emprunt
; --- LE COMMIT : le scratch devient a (la sortie ÉCRASE a — Q1/Q2) ---------
mov rax, qword ptr [rsp + 0x20]
mov qword ptr [rcx], rax
mov rax, qword ptr [rsp + 0x28]
mov qword ptr [rcx + 8], rax
mov rax, qword ptr [rsp + 0x30]
mov qword ptr [rcx + 16], rax
mov rax, qword ptr [rsp + 0x38]
mov qword ptr [rcx + 24], rax
mov rax, qword ptr [rsp + 0x40]
mov qword ptr [rcx + 32], rax
call TLS12
xor eax, eax
add rsp, 0x48
ret
; --- LE VERROU fail-closed (E1 d'av-08 élevant en verdict — Q3) -------------
.emprunt:
mov rax, -1
add rsp, 0x48
ret
