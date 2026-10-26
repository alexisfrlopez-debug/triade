ah-09 · orchestration hachoir · révision 1
Intention : le point d'entrée ELF de hachoir — l'orchestration complète :
argc/argv (ABI de démarrage SysV : [rsp] = argc, [rsp+8] = argv, le noyau
garantit rsp 16-aligné SANS adresse de retour — l'inverse exact du profil
msx64), ouverture du fichier, boucle de lecture 64 Kio, absorption,
finalisation, encodage, émission de la ligne au format sha256sum,
terminaison. C'est le seul bloc non appelable : personne ne l'appelle,
le noyau y saute.
Contrat :
  pre  : P1 l'exécution démarre à l'entrée ELF : [rsp] = argc (u64),
             [rsp+8] = argv[0], [rsp+16] = argv[1], … terminateur
             nul — l'ABI de démarrage Linux, et rsp ≡ 0 mod 16 (sans
             adresse de retour : la pile d'un _start n'a pas de cadre
             d'appelant) ;
         P2 aucun registre n'est garanti par le noyau à l'entrée (hors
             rsp) — le bloc n'hérite de RIEN.
  post : Q1 nominal (argc == 2, fichier lisible) : la ligne
             « <hex 64>  <argv[1]>\n » est écrite sur stdout (deux
             espaces, saut de ligne — format sha256sum exact) et le
             code de sortie est 0 ;
         Q2 usage (argc != 2) : la ligne « usage: hachoir <fichier>\n »
             sur stderr, code de sortie 1 ;
         Q3 ouverture impossible : « hachoir: ouverture impossible\n »
             sur stderr, code de sortie 1 ;
         Q4 lecture impossible (dont répertoire, EISDIR par ah-02) :
             « hachoir: erreur de lecture\n » sur stderr, code de
             sortie 1 ;
         Q5 écriture impossible : « hachoir: erreur d'ecriture\n » sur
             stderr, code de sortie 1 ;
         Q6 le fichier est fermé (sys_close) avant l'émission.
  inv  : I1 appels système directs : sys_open (rax = 2), sys_read
             (rax = 0), sys_close (rax = 3) — les blocs ah-01..03
             encapsulent write/exit mais PAS open/read/close (leur
             contrat est exploité via les wrappers sys du NOYAU
             directement ici : la spec le déclare, l'oracle autorise
             exactement ces trois numéros) ;
         I2 appels directs : ah-04 @ 0x1100, ah-06 @ 0x1400, ah-07 @
             0x1500, ah-08 @ 0x1600 exclusivement (ah-05 n'est jamais
             appelé directement par l'orchestration — uniquement via
             ah-06/ah-07) ;
         I3 données : contexte @ 0x3000, digest @ 0x3080, ligne @
             0x30C0, tampon 64 Kio @ 0x4300 (.bss), messages @ 0x2120+
             (.rodata) — chaque déplacement RIP est documenté dans la
             notation ;
         I4 registres : rbx (chemin argv[1]), r12 (descripteur), r13
             (longueur du morceau) traversent les appels — non-volatils
             SysV, aucun push nécessaire au niveau du bloc (le bloc ne
             retourne jamais : il termine par sys_exit) ; pile
             16-alignée à chaque point d'appel (le push/pop unique de
             la copie de chemin est apparié avant tout call) ;
         I5 aucune écriture hors .bss de l'image ; le code n'est jamais
             écrit (pas d'auto-modification — ce n'est pas le jalon M2).
Échecs :
  E1 : argc < 2 (pas de fichier) → Q2 ; E2 : argv[1] inexistant sur le
       disque ou sans permission → Q3 ; E3 : répertoire ou erreur de
       périphérique en lecture → Q4 ; E4 : stdout fermé ou plein → Q5.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : propriété différentielle (oracle, artefact entier) : sur chaque
       témoin (tailles 0, 1, 55, 56, 63, 64, 65, 127, 128, 1000, 65535,
       65536, 65537, 131072, aléatoires contraints), la ligne émise est
       octet-identique à « <sha256sum du témoin>  <chemin>\n » et le
       code de sortie est 0 (couvre Q1 sur toutes les transitions de
       bourrage et de tampon) ;
  V3 : chemins d'échec : sans argument, sur fichier inexistant, sur
       répertoire — messages exacts sur stderr, code 1 (couvre Q2-Q5) ;
  V4 : falsification : la corruption d'un octet de n'importe quel bloc
       est détectée (digest divergent ou échec d'exécution — zéro
       silence, couvre l'ensemble).
Fixtures    : les messages .rodata (usage, ouverture, lecture,
              écriture — longueurs figées par le plan d'adressage).
Provenance  : écrite-avant-code.
Décisions   : D34.
Historique  : R1. La symétrie avec tcp-12:R1 (orchestration M2) est
              délibérée : même rôle, profil inverse — là-bas
              GetStdHandle/IAT/WaitForMultipleObjects, ici l'ABI de
              démarrage nue et trois appels système directs. Le
              descripteur n'est jamais caché : hachoir est un filtre,
              pas un serveur.
