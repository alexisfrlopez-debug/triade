; hello-02-ecrire-r2 · brouillon étiqueté — spec hello-02:R2 (écrire), bloc carte f61001
; L'interface d'écriture du corpus : UN appel au service d'écriture du profil
; (frag-con : Linux — sys_write, fd/tampon/longueur en rdi/rsi/rdx — les
; arguments SysV coïncident avec les arguments syscall, zéro déplacement ;
; Windows — WriteFile IAT, HANDLE en rcx, shadow space 0x28 avant l'appel).
; Le verdict est BRUT (rax du noyau : count >= 0 ou -errno) — jamais masqué,
; jamais retenté (Q1, E1). Le syscall détruit rcx/r11 (ISA) — les volatils
; de l'ABI, personne n'y vivait. Aucune zone d'accueil : l'ABI n'en exige
; pas (I1 — le miroir exact de hello-02:R1 côté Windows).
@SYS_WRITE = 1
mov eax, @SYS_WRITE
syscall
ret
