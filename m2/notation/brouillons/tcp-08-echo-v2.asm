; tcp-08-echo v2 · brouillon · transformation majuscules (remplaçant) · (rcx dst, rdx src, r8 n) -> rax n
; spec tcp-08:R2 · c30014 · assemblé POUR 0x4680 (croissance — staging .rdata, bascule tcp-07)
; FEUILLE : aucun appel, aucun push, volatils uniquement (I1/I2) — contrat stable R4
; R2 : tout octet dans [0x61, 0x7A] est émis diminué de 0x20, tout autre tel quel
; Entrée alignée 16 : aucune cible de saut dans les 8 premiers octets (I3)
mov rax, r8
test r8, r8
je .fin
xor r9, r9
.boucle:
mov r10b, byte ptr [rdx + r9]
cmp r10b, 0x61
jb .garder
cmp r10b, 0x7A
ja .garder
sub r10b, 0x20
.garder:
mov byte ptr [rcx + r9], r10b
inc r9
cmp r9, r8
jb .boucle
.fin:
ret
