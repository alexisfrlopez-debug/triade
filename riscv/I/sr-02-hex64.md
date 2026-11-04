sr-02 · formatage hexadécimal u64 · révision 1
Intention : formater une valeur 64 bits en 16 caractères hexadécimaux
minuscules, à l'identique de la graphie des outils du noyau (%016lx) — le
bloc d'affichage de la sonde : la base de chargement (ligne 1), les a0
bruts et les verdicts (lignes des sondes). Miroir assumé de su-02:R1 du
jalon unix : l'arithmétique est la MÊME (16 itérations, nibble de poids
fort en tête), les registres changent (psABI) — et l'accès aux données
change de MÉCANISME : le rip-relatif n'existe pas en RV64, l'accès vit en
[ancre + déplacement] où l'ancre s1 = base est une PRÉCONDITION posée par
sr-04 (le seul bloc qui la calcule — la paire auipc+addi).
Contrat :
  pre  : P1 a0 contient la valeur à formater (u64 — la convention est la
             valeur BRUTE : un a0 négatif de syscall se formate en son
             complément à deux, 0xfffffffffffffff7 pour -9) ;
         P2 a1 pointe vers 16 octets inscriptibles (le tampon .bss — le
             principal passe toujours la fenêtre s2) ;
         P3 s1 = base de chargement (posée par sr-04 — l'ancre traversante
             du jalon ; le bloc ne LA POSE PAS, il la LIT) ;
         P4 la pile est alignée à l'entrée (sp ≡ 0 mod 16).
  post : Q1 les 16 caractères "0123456789abcdef" dérivés de la valeur sont
             écrits dans [a1, a1+16) ; a1 est avancé de 16 (le curseur
             retourne la fin — registre de travail, jamais une promesse) ;
             a0 n'est pas garanti (registre de travail).
  inv  : I1 données : lecture de la table HEXCHARS @ RVA 0x180
             exclusivement (16 octets, .rodata segment R) — l'accès est
             [s1 + 0x180 + nibble] : le déplacement 0x180 est DÉCLARÉ au
             builder (I3 de la carte) ;
         I2 feuille pure : aucun appel, aucun push, aucun registre non
             volatil touché (s1/s2 lus, jamais écrits), 0 octet de pile —
             et t1 JAMAIS touché : le registre de travail interne du
             projet (fiche § 2 — le portage de R10/R11) porte le a0 brut à
             travers ce bloc chez sr-04, il est RESPECTÉ ici (t0/t3/t4
             suffisent à l'arithmétique) ;
         I3 l'arithmétique : 16 itérations, décalage 60, 56, …, 0 — le
             caractère i porte le nibble (v >> (60 - 4*i)) & 0xF.
Échecs :
  E1 : aucun (bloc arithmétique pur — pas de chemin d'échec ; un tampon
       non inscriptible est une violation de P2, hors contrat).
Vecteurs :
  V1 : round-trip de notation 100 % (porte du chantier).
  V2 : oracle d'exécution (artefact entier, sous qemu-riscv64) : les
       lignes de la sonde portent les hex exacts — base en ligne 1 (16
       chiffres, alignée à la page), 0xfffffffffffffff7 et
       0xfffffffffffffff2 en a0 des sondes, 0x0000000000000001 et
       0x0000000000000006 en verdicts.
Fixtures    : HEXCHARS ("0123456789abcdef", 16 o — .rodata, via l'ancre s1).
Provenance  : écrite-avant-code.
Décisions   : D149, D14 (universalité), le modèle su-02:R1 du jalon unix.
Historique  : R1. Premier bloc de formatage du jalon. Le choix minuscule =
              %016lx du noyau ; le choix 16-caractères-fixes = pas de
              compression (les zéros de tête sont de l'information : ils
              distinguent 6 (verdict) de 0x6000000000000000). Le changement
              de mécanisme d'accès (ancre posée en précondition au lieu de
              rip-relatif) est le COÛT du portage RV64, assumé et déclaré :
              l'imm12 des charges n'atteint que ±2047 o.
