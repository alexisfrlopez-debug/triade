sr-03 · verdict d'erreur syscall · révision 1
Intention : traduire le retour d'un syscall échoué en verdict nommé — LE
bloc du contrat d'erreurs du jalon (fiche § 4), miroir exact de
su-03:R1 du jalon unix (la TROISIÈME instanciation du rôle) et de
tls-02:R1 du profil Windows (la table TOTALE des verdicts SSPI) : une
table dans .rodata (ERRNOS), une liste blanche d'errno attendus, tout
errno hors table = VERDICT_FATAL. La sonde l'alimente avec les a0 bruts
de ses deux sondes ; le corpus du chantier (b) héritera du même bloc pour
ses propres contrats d'échec.
Contrat :
  pre  : P1 a0 contient le retour BRUT du syscall (valeur négative, plage
             [-4095, -1] : la convention d'entrée est le a0 tel quel, le
             bloc en extrait l'errno) ;
         P2 la table ERRNOS @ RVA 0x140 est présente (le builder vérifie
             l'empreinte de la table contre layout.ERRNOS — source unique) ;
         P3 s1 = base de chargement (posée par sr-04 — comme sr-02, le
             bloc lit l'ancre, il ne la pose pas) ;
         P4 la pile est alignée à l'entrée (sp ≡ 0 mod 16).
  post : Q1 errno dans la table : a0 = verdict de l'entrée (u32 ; au
             chantier (a) : 1 = échec nommé) ;
         Q2 errno hors table (ou table vide) : a0 = 6 (VERDICT_FATAL) —
             l'appelant doit arrêter proprement, nommément (fail-closed).
  inv  : I1 données : lecture de la table ERRNOS @ RVA 0x140 exclusivement
             (accès [s1 + 0x180..0x144..] — le déplacement est DÉCLARÉ au
             builder ; format [nombre u32] puis {errno u32, verdict u32} —
             le balayage est exhaustif, le nombre borne) ;
         I2 feuille pure : aucun appel, aucun push, aucun registre non
             volatil touché, 0 octet de pile, t1 JAMAIS touché (le porteur
             du brut — fiche § 2 ; t0/t2/t4 suffisent au balayage) ;
         I3 le succès n'est JAMAIS consulté ici : a0 dans [0, 4095] est
             constaté par PLAGE chez l'appelant — la table ne connaît que
             les échecs (le miroir de HRESULTS : SEC_E_OK n'y vit qu'en
             tant qu'entrée de verdict, jamais comme plage).
Échecs :
  E1 : aucun (bloc de table pur — un errno imprévu n'est pas un échec du
       bloc, c'est sa Q2 : le verdict fatal EST le service rendu).
Vecteurs :
  V1 : round-trip de notation 100 % (porte du chantier).
  V2 : oracle d'exécution (artefact entier, sous qemu-riscv64) : la sonde
       1 rend errno 9 → verdict 1 émis en ligne ; la sonde 2 rend errno 14
       → verdict 6 émis en ligne, ligne FATALE suivie, code de sortie 6.
  V3 : la falsification d'un octet du bloc diverge (verdict ou crash).
Fixtures    : la table ERRNOS ([1][{9, 1}] au chantier (a) — layout.py,
              source unique).
Provenance  : écrite-avant-code.
Décisions   : D149, D79 (le modèle de la liste blanche vérifiée), D14
              (universalité — le modèle su-03:R1 du jalon unix).
Historique  : R1. La table EST le contrat d'erreurs du jalon : chaque
              entrée est motivée par un bloc (EBADF par sr-04:E1) — elle
              grandira par révision au chantier (b), jamais par caprice.
              Les errno asm-generic sont ceux de Linux RISC-V (9/14 — les
              MÊMES valeurs que x86-64 : la table errno de Linux est
              unifiée, seul l'INTERFACE d'appel change).
