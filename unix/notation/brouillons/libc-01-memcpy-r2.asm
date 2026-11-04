; libc-01-memcpy-r2 · brouillon étiqueté — spec libc-01:R2, bloc carte f61003
; La feuille pure : dst/src/n nommés (frag-con : SysV — rdi/rsi/rdx ;
; msx64 — rcx/rdx/r8). L'instance SysV est le cadeau de l'ABI : les arguments
; tombent DÉJÀ dans les registres de rep movsb (rdi destination, rsi source)
; — la notation Windows devait pousser rdi/rsi (non volatils msx64) pour
; s'en servir ; ici ils sont volatils et déjà en place : trois instructions.
; rax = dst (Q2), rcx = n, rep movsb avance rdi/rsi (volatils — libres),
; n = 0 : rcx nul, rep ne touche rien (I4). Aucun non volatil touché (I3).
mov rax, rdi
mov rcx, rdx
rep movsb byte ptr [rdi], byte ptr [rsi]
ret
