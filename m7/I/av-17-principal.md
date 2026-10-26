av-17 · orchestration du vérificateur sceau · révision 1
Intention : le point d'entrée de sceau — deux modes :
  `sceau --hacher <fichier>` : ligne sha512sum exacte sur stdout
  (diagnostic : l'agent gagne un hacheur SHA-512 natif, le complément
  512 bits du hachoir 256) ;
  `sceau <message> <signature> <cle-hex>` : vérification Ed25519 — en
  0.8.0-dev.1 la vérification est EN CHANTIER (message explicite, code
  2) : la couche I est posée (av-05..16), la notation vient en dev.2 ;
  la révision 2 du bloc livrera le mode complet (lecture du message,
  SHA-512 de R'||A||M, verdict OK/KO, codes 0/1).
  Les erreurs d'usage/ouverture/lecture sont miroir de hachoir (ah-09),
  préfixées « sceau: ».
Contrat :
  pre  : P1 le bloc est le point d'entrée ELF de sceau (rsp ≡ 0 mod 16
             à l'arrivée noyau — pas de retour : exit par av-sortir) ;
         P2 argv/argc lisibles sur la pile initiale (argc @ [rsp],
             argv[i] @ [rsp + 8 + 8i], vecteur terminé par NULL).
  post : Q1 mode hacher : la ligne « <sha512-hex>  <chemin>\n » est
             émise sur stdout (128 caractères hexadécimaux par DEUX
             appels de l'héritage ah-08 : moitié basse puis haute du
             digest), exit 0 ; les chemins d'échec d'usage (argc ≠ 3
             pour ce mode), d'ouverture, de lecture, d'écriture :
             message exact sur stderr, exit 1 ;
         Q2 mode vérification (argc == 4) : 0.8.0-dev.1 émet
             « TRIADE sceau : verification en chantier (0.8.0-dev.1) »
             sur stderr, exit 2 — le mode est un contract D'ATTENTE,
             la révision 2 le remplace (croissance R7 : révision du
             bloc, pas silencieuse) ;
         Q3 tout autre argv : usage sur stderr, exit 1 ;
         Q4 le processus se termine TOUJOURS par av-sortir (héritage
             ah-03) : 0 nominal, 1 erreur d'usage/E-S, 2 chantier.
  inv  : I1 appels directs : héritages d40001 (av-écrire), d40003
             (av-sortir), d40008 (av-hex), famille av-01/03/04 (SHA-512 :
             init, absorber en boucle 64 Kio, finaliser) — la lecture
             du fichier est DIRECTE (syscall read, miroir ah-09 I1 :
             l'héritage ah-02 n'est pas embarqué) ;
         I2 syscalls autorisés : 0 (read), 2 (open), 3 (close) ;
         I3 ordre SHA-512 du mode hacher : av-01, boucle (read 64 Kio →
             av-03), av-04 → digest @ R_DIGEST ; en mode vérification
             (dev.2) : av-01, av-03(R' 32 o), av-03(A 32 o), boucle
             message, av-04 — l'ordre R'||A||M est le contrat I3
             d'av-16, ce bloc le respecte à la lettre ;
         I4 données RIP : R_CTX, R_DIGEST, R_LIGNE, R_TAMPON, les
             messages R_MSG_* (usage, ouverture, lecture, écriture,
             chantier) — déclarées, cibles vérifiées ;
         I5 aucun push (miroir ah-09 : l'ABI de démarrage ne sauvegarde
             rien — sortie par exit, jamais ret) ;
         I6 la comparaison du mode « --hacher » : qword de argv[1]
             contre l'immédiat 0x7265686361682d2d (« --hacher »
             little-endian) PUIS test de l'octet 8 NUL — un préfixe
             plus long ne doit pas matcher (la discipline frontière,
             leçon C1).
Échecs :
  E1 : usage (argc incohérent) → stderr usage, exit 1.
  E2 : ouverture impossible, lecture en échec, écriture en échec →
       message préfixé « sceau: », exit 1 (miroir hachoir).
  E3 : mode vérification demandé avant livraison → chantier, exit 2
       (explicit, jamais silencieux).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : oracle natif différentiel : vecteurs dorés FIPS 180-4 SHA-512
       (vide, « abc », 448 bits, million de 'a') et tailles de
       transition (0, 1, 111, 112, 127, 128, 129, 1000, 65535, 65536,
       65537, 131072) — ligne octet-identique à sha512sum, code 0 ;
       chemins d'échec (sans argument, inexistant, répertoire) —
       messages exacts, code 1 ; mode 4 arguments — message chantier,
       code 2 (couvre Q1-Q4, E1-E3).
  V3 : falsification : chaque octet de code du bloc corrompu diverge
       sur la batterie de scénarios — zéro silence.
Fixtures    : chaînes .rdata (usage, ouverture, lecture, écriture,
              chantier — tailles par machine, vérifiées par le builder).
Provenance  : écrite-avant-code.
Décisions   : D34.
Historique  : R1. Le double appel d'av-hex (32 octets chacun) plutôt
              qu'un nouveau bloc hexa-64 : l'héritage est le critère
              R7 — réutiliser l'existant scellé vaut mieux que
              dupliquer ; la ligne de 128 caractères est assemblée par
              deux moitiés, l'arithmétique d'adresses est dans les
              symboles vérifiés.
