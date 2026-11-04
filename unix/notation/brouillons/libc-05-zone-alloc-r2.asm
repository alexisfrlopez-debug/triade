; libc-05-zone-alloc-r2 · brouillon étiqueté — spec libc-05:R2, bloc carte f61007
; taille/alignement nommés (frag-con : SysV — rdi/rsi ; msx64 — rcx/rdx).
; Le curseur et l'arène vivent au plan de l'image (frag-loc : le corpus —
; curseur 0x3000, arène 0x3040 alignée 64), atteints en relatif RIP (PIE —
; le lien-temps est un déplacement, jamais une adresse absolue). L'arithmétique
; est celle de R1 : borne alignée = (curseur + align-1) & ~(align-1), le
; pointeur = arène + borne, le nouveau curseur = borne + taille ; échec
; propre → 0, curseur inchangé (Q3) ; taille 0 → pointeur valide, curseur
; inchangé (Q4). Tout le travail aux volatils rax/r8/r9/r10 (I2 — la
; notation Windows employait les mêmes, aux noms d'arguments près).
@ARENE_TAILLE = 0x7C0
@CURSEUR = 0x3000
@ARENE = 0x3040
cmp rdi, @ARENE_TAILLE
ja .echec
test rsi, rsi
je .echec
lea r9, [rsi - 1]
test r9, rsi
jne .echec
cmp rsi, 64
ja .echec
lea r8, [rip + @CURSEUR]
mov rax, qword ptr [r8]
add rax, r9
not r9
and rax, r9
lea r10, [rip + @ARENE]
add r10, rax
add rax, rdi
cmp rax, @ARENE_TAILLE
ja .echec
mov qword ptr [r8], rax
mov rax, r10
ret
.echec:
xor eax, eax
ret
