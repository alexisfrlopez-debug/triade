libc-08 · auto-test de la mini-libc · révision 3
Intention : exécuter les vecteurs dorés de chaque bloc de la mini-libc au
lancement de l'artefact et imprimer le verdict global — le rituel de santé
de la bibliothèque, première vérification à la R10.
Contrat :
  pre  : P1 le bloc est exécuté au lancement de l'artefact, dans la forme
             d'entrée du profil (frag-con : Windows — le bloc EST le point
             d'entrée PE de selftest.exe ; Linux — le bloc est appelé par le
             principal du jalon dès l'entrée ELF) ;
         P2 la pile est alignée à l'entrée selon la discipline du profil
             (rsp ≡ 8 mod 16 à l'entrée d'un bloc appelé — la forme
             d'orchestration vit en frag-con) ;
         P3 l'arène et son curseur sont vierges (image chargée, état nul) ;
         P4 l'entrée standard n'est pas consommée (aucune lecture).
  post : Q1 chaque vecteur doré est exécuté exactement une fois, dans l'ordre
         des dépendances : zone (libc-05/06), puis memcmp (libc-02),
         memcpy (libc-01), strlen (libc-03), itoa (libc-04), memset (libc-07) ;
         Q2 une ligne unique "TRIADE M1 : minilibc N/21" suivie de " OK" ou
             " KO" est soumise au service d'écriture du profil sur le flux de
             sortie, où N est le nombre de vecteurs réussis (frag-con :
             Windows — WriteFile, la ligne terminée \r\n, le flux obtenu par
             le bloc via le service de handles ; Linux — le bloc d'interface
             écrire du corpus, fd 1, la ligne terminée \n — le préfixe et le
             verdict sont invariants, le terminateur est la discipline du
             profil) ;
         Q3 le processus se termine au code du verdict : 0 si N = 21, sinon 1
             (frag-con : Windows — le bloc termine lui-même par le service de
             sortie ; Linux — le bloc rend N dans rax à son appelant, le
             principal du jalon porte la terminaison par sortir) ;
         Q4 la valeur N est formatée par libc-04 (auto-hébergement : l'auto-test
             utilise la bibliothèque qu'il teste).
  inv  : I1 le bloc n'appelle que les blocs libc-01…07 et le service
             d'écriture du profil (frag-con : Windows — io-01/io-02 et l'IAT
             GetStdHandle, jamais de syscall direct ; Linux — le bloc écrire
             du corpus, jamais de syscall direct) ;
         I2 le prologue réserve le cadre exigé par la convention du profil
             (frag-con : Windows — 0x40 octets, zone d'accueil + logettes,
             sauvegarde des non volatils de travail ; Linux — le cadre SysV,
             zone rouge interdite car le bloc appelle) et l'épilogue restaure
             symétriquement ;
         I3 aucun stockage sous rsp au moment d'un appel ;
         I4 les compteurs et pointeurs de travail qui traversent des appels
             vivent dans les non volatils sauvegardés ou en mémoire — jamais
             en volatile (D150 : les volatils meurent dans les appelés) ;
         I5 le tampon ligne est alloué dans l'arène en phase de verdict, après
             le vecteur de réinitialisation (libc-06) — jamais avant.
Échecs :
  E1 : le service d'écriture rend un verdict d'échec (sortie indisponible) →
       le verdict de l'auto-test reste porté par le code de sortie (Q3),
       propagation silencieuse documentée (repli : même discipline que
       hello-01).
Vecteurs :
  V1 : round-trip de notation 100 % (couvre la fidélité générale du bloc).
  V2 : propriété différentielle (oracle, artefact entier) : l'artefact entier
       est exécuté (frag-con : Windows — émulation IAT de l'oracle ; Linux —
       exécution native au labo) — la sortie doit être exactement la ligne de
       verdict du profil ("TRIADE M1 : minilibc 21/21 OK" + terminateur du
       profil) et le code de sortie 0 ; la corruption d'un octet quelconque
       d'un bloc libc fait dévier sortie ou code (non-vacuité) (couvre
       Q1-Q4).
  V3 : vecteurs dorés embarqués : zone (alignement, bornes disjointes,
       réutilisation après réinitialisation, dépassement → 0), memcmp (égal,
       inférieur, supérieur, préfixe), memcpy (16 octets, longueur nulle sur
       sentinelle, 33 octets), strlen (vide, "TRIADE", 33 lettres), itoa
       (0, 4294967295, 1234567890, 7), memset (zéros sur 16 octets, 0xFF sur
       33 octets, longueur nulle sur sentinelle) — 21 vecteurs (couvre Q1,
       Q4).
  V4 : test de rejet : toute notation du bloc appelant un bloc hors de I1, ou
       écrivant sous rsp au moment d'un appel, est refusée par l'oracle
       structurel (couvre I1, I2, I3).
Fixtures    : motifs et chaînes des blocs libc-01…04 et libc-07 (référence
              unique par identifiant, conformément à D20, au plan de
              l'image).
Provenance  : écrite-avant-code.
Décisions   : D7, D8, D26, D28, D29, D150 (l'état qui traverse vit en
              mémoire ou en non volatil sauvegardé), D149 (révision de
              granularité).
Historique  : R1 (dev.1, 18 vecteurs) révisée en R2 (dev.2) pour l'entrée de
              libc-07 memset dans la bibliothèque — l'extension du contrat
              d'auto-test accompagne l'ajout du bloc dans la réserve libc
              (démonstration R7 : aucun bloc scellé ne bouge). R2 (m1/I,
              instance Windows scellée 0.2.0) révisée en R3 au chantier
              M6-(b) : la révision de granularité (D149-(3)) — la FORME
              d'entrée (PE vs appel par le principal), les services
              (WriteFile/ExitProcess vs écrire/sortir), le terminateur de
              ligne (\r\n vs \n) et le porteur de terminaison (le bloc vs le
              principal) deviennent des paramétrisations de profil en
              frag-con ; les OBSERVABLES — l'ordre des 21 vecteurs (Q1), la
              ligne de verdict à préfixe et verdict invariants (Q2), le code
              de sortie 0/1 (Q3), l'auto-hébergement du formatage (Q4) —
              sont INVARIANTS ; l'instance Windows scellée demeure conforme.
