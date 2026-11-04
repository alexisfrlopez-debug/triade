; libc-07-memset-r2 · brouillon étiqueté — spec libc-07:R2, bloc carte f61009
; dst/valeur/n nommés (frag-con : SysV — rdi/rsi(8 bits)/rdx ; msx64 —
; rcx/dl/r8). rep stosb veut rdi/al/rcx : la destination est DÉJÀ en rdi
; (le second cadeau de l'ABI — l'instance Windows poussait rbx/rdi, ses
; non volatils, pour libérer les registres de l'instruction) ; l'octet
; monte de sil vers al — MAIS al est le BAS de rax : dst vit donc en r10
; (volatile, survit à rep stosb) et remonte en rax au retour (Q2 — le
; défaut attrapé par l'oracle natif au premier build : mov rax, rdi PUIS
; mov al, sil rendait rax != dst, la post-condition violée).
; n = 0 : rcx nul, rep ne touche rien (I4).
mov r10, rdi
mov rcx, rdx
mov al, sil
rep stosb byte ptr [rdi], al
mov rax, r10
ret
