; hello-03-sortir-r2 · brouillon étiqueté — spec hello-03:R2 (sortir), bloc carte f61002
; L'interface de terminaison du corpus : le service de sortie du profil
; (frag-con : Linux — sys_exit_group ; Windows — ExitProcess IAT). Le code
; (argument 1, 32 bits significatifs) voyage en edi → rdi tel quel. L'appel
; ne revient JAMAIS : ud2 défensif immédiat (I1 — l'inaccessibilité est
; matérialisée, fail-closed esprit R10 ; l'arrêt défensif est du profil, la
; discipline est la même).
@SYS_EXIT_GROUP = 231
mov eax, @SYS_EXIT_GROUP
syscall
ud2
