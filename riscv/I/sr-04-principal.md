sr-04 · orchestration sonde · révision 1
Intention : le point d'entrée ELF de la sonde — la démonstration exécutable
du chantier M7-(a) (le moteur de notation RV64 aux oracles verts) : poser
les DEUX ancres de base à l'exécution (les paires auipc+addi — s1 = base,
s2 = base + 0x2000 la fenêtre .bss : le portage RV64 du lea rip
lié-temps soustrait, l'instruction auipc lit pc, addi soustrait le
lien-temps ; les charges RV64 n'atteignent que ±2047 o, le tampon vit
au-delà — l'ancre le porte), émettre la ligne de base, puis exercer la
table ERRNOS sur ses deux branches : une sonde volontaire write(-1, …)
rend -EBADF (errno nommé → verdict 1, la sonde continue), une sonde
volontaire write(1, 0x1, …) rend -EFAULT (errno hors table au chantier
(a) → VERDICT_FATAL 6, ligne fatale, arrêt propre code 6). C'est le seul
bloc non appelable : personne ne l'appelle, l'exécuteur du jalon
(qemu-riscv64, réserve instrumentale D149 nommée) y saute — à une base
que lui seul choisit.
Contrat :
  pre  : P1 l'exécution démarre à l'entrée ELF (e_entry 0x1140, RELATIF à
             la base — ET_DYN/PIE) : [sp] = argc (u64), [sp+8] = argv[0],
             … terminateur nul — l'ABI de démarrage Linux, et sp ≡ 0 mod
             16 (sans adresse de retour : la pile d'un point d'entrée n'a
             pas de cadre d'appelant, ra n'est pas initialisé) ;
         P2 aucun registre n'est garanti par le chargeur à l'entrée (hors
             sp) — le bloc n'hérite de RIEN ; la base n'est connue de
             nulle part : elle se POSE (les paires d'ancres, I3).
  post : Q1 nominal (stdout vivant, noyau conforme) : quatre lignes sur
             stdout — "sonde : base 0x" + hex16(base) + "\n" ; la ligne de
             la sonde 1 (préfixe write(-1), hex16(a0) = fffffffffffffff7,
             verdict 0000000000000001) ; la ligne de la sonde 2 (préfixe
             write(0x1), hex16(a0) = fffffffffffffff2, verdict
             0000000000000006) ; "sonde : VERDICT_FATAL (arret propre)\n"
             — et le code de sortie est 6 (le verdict fatal final, la
             démonstration complète des deux branches) ;
         Q2 émission déficiente (stdout fermé/plein au premier essai) : la
             première émission rend un a0 négatif → consultation sr-03 ;
             errno nommé → arrêt propre code 0 (le canal de constat est
             mort : plus rien n'est observable, chaque ligne restante
             serait également muette — jamais un crash) ; errno inattendu
             → ligne fatale tentée (muette si le canal est mort) et arrêt
             code 6 ;
         Q3 aucune sonde ne réussit par accident : les arguments (-1 hors
             domaine, 0x1 sous mmap_min_addr) sont des garanties du noyau ;
             le flux est générique (tout a0 négatif passe par sr-03), les
             lignes portent les valeurs réelles, jamais les attendues.
  inv  : I1 appels directs : sr-01 @ 0x1000, sr-02 @ 0x1040, sr-03 @
             0x10C0, et le sous-programme local .emit (étiquette interne au
             bloc, frontière d'instruction — déclaré : il émet la ligne
             d'une sonde et rend le verdict) exclusivement ;
         I2 appels système directs : ecall avec a7 = 94 (sys_exit_group
             ASM-GENERIC, fiche § 4) exclusivement — trois sites (sortie
             nominale code 0, sortie canal-mort code 0, sortie fatale
             code 6) ; a7 = 231 (exit_group x86-64) est un REFUS DE BUILD
             NOMMÉ (garde anti-table-x86) ; les write passent TOUS par
             sr-01, jamais en direct ;
         I3 données : les DEUX ancres sont posées aux sites déclarés du
             plan (ANCRE_BASE 0x1140, ANCRE_BSS 0x1148 — l'arithmétique
             auipc+addi est VÉRIFIÉE par le builder : site + HI*4096 + LO
             == cible, les déclarations de la notation confrontées au
             layout) ; les autres accès vivent en [s1 + RVA] (messages @
             0x1C0-0x284) et [s2 + déplacement] (tampon @ +0/+16/+32 —
             chaque déplacement est documenté dans la notation et DÉCLARÉ
             au builder) ;
         I4 la pile : le point d'entrée n'a pas de cadre d'appelant (sp
             N'EST JAMAIS touché au niveau du corps — jal ne pousse rien,
             ra porte le lien) ; le sous-programme .emit pose son cadre
             (addi sp, sp, -16 à l'entrée ; sd ra, 0(sp) — jal écrase ra,
             le lien se SAUVE ; addi sp, sp, 16 après ld ra — appariés,
             sp ≡ 0 mod 16 en tous points d'appel psABI) ; t1 = registre
             de travail interne du projet (fiche § 2) : il porte le a0
             brut à travers sr-02/sr-03 (qui respectent t1 par contrat) ;
             a1/a2 (préfixe/longueur de la ligne) sont consommés avant le
             premier appel (ils meurent au premier jal) ; le verdict vit
             au tampon [s2+32] (la mémoire traverse les appels et les
             syscalls, les registres volatils non) ;
         I5 aucune écriture hors .bss de l'image ; le code n'est jamais
             écrit (pas d'auto-modification — ce n'est pas le chantier (c)).
Échecs :
  E1 : stdout fermé (les deux sondes passent quand même — leurs write
       défaillants rendent EBADF nommé) → Q2 ;
  E2 : le noyau rend un errno imprévu sur une émission → Q2 branche
       fatale ; sur une sonde → la ligne porte le verdict réel (Q3).
Vecteurs :
  V1 : round-trip de notation 100 % (porte du chantier — capstone juge
       unique).
  V2 : oracle d'exécution (artefact entier, sous qemu-riscv64) : sur >= 6
       exécutions, quatre lignes conformes et code 6 à chaque fois ; la
       base est CONSTATÉE (page-alignée, >= 0x10000 — la réserve
       instrumentale D149 s'applique : la base vient du CHARGEUR qemu,
       l'ASLR émulé est ce que le chargeur en fait, le verdict le nomme —
       et l'indifférence à la base se démontre par bases FORCÉES si le
       chargeur ne randomise pas).
  V3 : falsification : la corruption d'un octet de n'importe quel bloc
       diverge (sortie, code ou crash) — zéro silence.
Fixtures    : les messages .rodata (longueurs figées par le plan
              d'adressage), la table ERRNOS, HEXCHARS.
Provenance  : écrite-avant-code.
Décisions   : D149 (programme M6/M7), D14 (universalité), le modèle
              su-04:R1 du jalon unix (la géométrie de la démonstration est
              PARTAGÉE — la ligne de preuve nomme a0, le registre de
              retour psABI, là où M6 nommait rax).
Historique  : R1. La symétrie avec su-04:R1 est délibérée (même rôle,
              même plan d'adressage, même démonstration) ; les différences
              sont TOUTES nommées : la paire d'ancres au lieu du lea rip
              (l'imm12 des charges RV64), la fenêtre s2 pour le .bss
              (au-delà de portée), le registre t1 au lieu de r10 (fiche
              § 2), le cadre de .emit qui SAUVE ra (jal écrase le lien —
              call poussait, jal ne pousse pas), la table asm-generic au
              lieu de la table native. Le code de sortie porte le verdict
              final (6) : la sonde démontre les deux branches de la
              table, la branche fatale est terminale par contrat.
