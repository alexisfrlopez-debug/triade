; corpus-13-principal · brouillon étiqueté — spec corpus-13:R1, bloc carte f61013
; LE RITUEL DE PARITÉ — le point d'entrée ELF de l'artefact du jalon
; (e_entry 0x1C40, RELATIF à la base — ET_DYN/PIE). L'ABI de démarrage
; Linux : [rsp] = argc, [rsp+8] = argv, terminateur nul, rsp ≡ 0 mod 16
; SANS adresse de retour (l'inverse exact du chargeur Windows — P1) ;
; argc/argv sont reçus et ignorés (P4 — le rituel ne prend pas de
; paramètre). Le code est indifférent à la base : TOUT accès vit en
; relatif RIP (I3) — nul besoin de calculer la base, contrairement à la
; sonde : le sujet de la sonde était la base, le sujet du corpus est le
; PATRIMOINE.
; Le déroulé : l'auto-test (libc-08 rend N en rax — la terminaison
; appartient au présent bloc, frag-con SysV de libc-08:R3 Q3) ; la ligne
; de journal du verdict par tcp-11 (préfixe "corpus : autotest ", champ
; N, suffixe " vecteurs\n" — le patrimoine M2 exercé) ; la terminaison au
; code du verdict par sortir (0 si N = 21, sinon 1 — Q3, deux sites).
; N traverse les appels en rbx (non volatil — D150, jamais un volatile) ;
; le corps ne pousse RIEN (I4 : un _start n'a pas de cadre d'appelant,
; les appels partent alignés tels quels — rsp ≡ 0 mod 16 à l'entrée).
@A_AUTOTEST = 0x1340
@A_JOURNAL = 0x1840
@A_SORTIR = 0x1040
@J_PREF = 0x280
@J_SUFF = 0x2A0
@L_PREF = 18
@L_SUFF = 10
call @A_AUTOTEST
mov rbx, rax
lea rdi, [rip + @J_PREF]
mov esi, @L_PREF
mov edx, ebx
lea rcx, [rip + @J_SUFF]
mov r8d, @L_SUFF
call @A_JOURNAL
cmp ebx, 21
jne .ko
mov edi, 0
jmp .fin
.ko:
mov edi, 1
.fin:
call @A_SORTIR
