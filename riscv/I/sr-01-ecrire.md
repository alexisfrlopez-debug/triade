sr-01 · écriture par appel système · révision 1
Intention : écrire des octets sur un descripteur de fichiers — le bloc
d'entrée/sortie élémentaire du jalon, miroir exact de su-01:R1 du jalon
unix (l'intention est la MÊME, l'ISA change — c'est la démonstration du
jalon M7 : le contrat survit au portage) et de ah-01:R1 de l'échelle
auto-hôte : l'artefact parle directement au noyau, sans bibliothèque,
sans tampon intermédiaire. Chez la sonde, le bloc a un second rôle,
déclaré : c'est L'INSTRUMENT DES SONDES d'erreur — le principal l'appelle
aussi avec des arguments volontairement défaillants (descripteur
invalide, tampon illisible) pour faire rendre au noyau les errno que la
table ERRNOS traduit (sr-03).
Contrat :
  pre  : P1 a0 contient le descripteur de fichiers (i32 ; ex. 1 = stdout ;
             les sondes passent -1, hors domaine, pour provoquer EBADF) ;
         P2 a1 pointe vers le tampon à écrire (mémoire lisible — sauf pour
             la sonde du tampon, qui passe délibérément 0x1, non mappé) ;
         P3 a2 contient le nombre d'octets à écrire (i32 ; n <= 2^31-1) ;
         P4 la pile est alignée à l'entrée (sp ≡ 0 mod 16 — l'appelant
             vient d'exécuter jal, qui ne pousse RIEN : ra porte le lien).
  post : Q1 succès : a0 contient le nombre d'octets écrits (>= 0) ;
         Q2 échec noyau : a0 contient -errno (valeur négative, la plage
             [-4095, -1] du contrat d'erreurs du jalon — jamais un crash).
  inv  : I1 appel système : instruction ecall avec a7 = 64 (sys_write de
             la table ASM-GENERIC du jalon, fiche § 4) exclusivement —
             aucun autre numéro, aucune autre interface ; a7=1 (write
             x86-64) est un REFUS DE BUILD NOMMÉ au moment de la notation
             (la garde anti-table-x86 vit au builder : la parité est
             SÉMANTIQUE, jamais lexicale) ;
         I2 feuille : 0 octet de pile consommé, aucun stockage sous sp
             (psABI : AUCUNE zone rouge — le piège INVERSE de SysV x86-64,
             fiche § 2), aucun registre non volatil touché, aucune paire
             d'ancre ; l'instruction ecall détruit a0 seul (le retour) ;
         I3 le bloc ne tamponne pas : un appel, un verdict — l'appelant
             gère les écritures partielles et les errno (le principal de
             la sonde route tout a0 négatif par sr-03, jamais au hasard).
Échecs :
  E1 : descripteur invalide ou fermé → a0 = -EBADF (-9) — échec nommé de
       la table (verdict 1) ; c'est le chemin de la sonde 1 ;
  E2 : tampon illisible → a0 = -EFAULT (-14) — errno hors table au
       chantier (a) → VERDICT_FATAL ; c'est le chemin de la sonde 2 ;
  E3 : n > ce que le descripteur accepte → écriture partielle (Q1).
Vecteurs :
  V1 : round-trip de notation 100 % (porte du chantier — capstone juge
       unique, corpus d'instructions du profil).
  V2 : oracle d'exécution (artefact entier, sous qemu-riscv64 — réserve
       instrumentale D149 nommée dans chaque verdict) : les émissions de
       la sonde passent toutes par ce bloc (code de sortie et lignes
       attendus octet pour octet) ; les deux sondes d'erreur rendent
       exactement -9 et -14.
Fixtures    : néant (le bloc ne possède aucune donnée).
Provenance  : écrite-avant-code.
Décisions   : D149 (programme M6/M7), D14 (universalité), le modèle
              su-01:R1 du jalon unix (la TROISIÈME instanciation du même
              rôle — l'ISA change, le contrat survit).
Historique  : R1. Premier bloc du domaine sr — la sonde de la notation
              RV64. Le contrat est celui de su-01:R1, révisé pour la
              convention psABI (a0-a2/a7, ecall) et pour la table
              asm-generic (write = 64, PAS 1 — la garde du jalon).
