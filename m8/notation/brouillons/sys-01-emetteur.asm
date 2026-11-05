; sys-01-emetteur · l'émetteur syscall direct · spec sys-01:R1 · bloc carte g90001
; LE mécanisme du domaine : l'instruction syscall et RIEN d'autre. Le bloc
; reçoit le SSN en rax (P1 — une DONNÉE chargée par l'appelant, charte § 1 :
; jamais un octet de code) et les arguments DANS L'ORDRE EXACT de l'API NT
; (P2 — l'appelant a fait le travail msx64, l'ombre comprise) ; il exécute le
; seul remappage que le noyau exige (rcx→r10, charte § 4 — l'instruction
; syscall DÉTRUIT rcx et r11) puis l'instruction ; le NTSTATUS rendu traverse
; tel quel (Q2 — la table des verdicts appartient à l'APPELANT).
; SIX octets (I3 : AUCUN prologue — aucun push, aucun sub rsp : la pile de
; l'appelant EST la pile du syscall, le noyau lit [rsp+0x28] AU MOMENT de
; l'instruction, un mot de décalage décalerait TOUS les arguments de pile) ;
; I6 : le ret suit IMMÉDIATEMENT le site syscall ; I1 : aucun IAT, aucun
; appel — le site syscall (0F 05) est l'unique interaction système ; I2 :
; rax n'est JAMAIS écrit avant l'instruction (le SSN traverse) ; I4 : aucun
; non-volatil touché (le bloc n'a rien à garder) ; I5 : aucun état, aucune
; écriture mémoire du tout.
mov r10, rcx
syscall
ret
