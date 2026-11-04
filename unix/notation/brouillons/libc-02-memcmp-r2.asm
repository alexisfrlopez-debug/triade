; libc-02-memcmp-r2 · brouillon étiqueté — spec libc-02:R2, bloc carte f61004
; ptr1/ptr2/n nommés (frag-con : SysV — rdi/rsi/rdx ; msx64 — rcx/rdx/r8).
; repe cmpsb consomme rdi/rsi/rcx (volatils SysV, déjà en place — la
; notation Windows poussait rdi/rsi, ses non volatils) ; le verdict aux
; volatils de travail du projet r10/r11. Le verdict est exactement
; normalisé -1/0/+1 (Q1-Q3) : n = 0 rend 0 AVANT le parcours (Q3),
; l'égalité complète rend 0 (eax déjà nul), la divergence compare les
; DERNIERS octets examinés (rdi-1/rsi-1). Les régions ne sont jamais
; écrites (I4 — cmpsb ne lit que).
xor eax, eax
test rdx, rdx
je .fin
mov rcx, rdx
repe cmpsb byte ptr [rsi], byte ptr [rdi]
je .fin
movzx r10d, byte ptr [rdi - 1]
movzx r11d, byte ptr [rsi - 1]
cmp r10d, r11d
ja .sup
mov eax, -1
jmp .fin
.sup:
mov eax, 1
.fin:
ret
