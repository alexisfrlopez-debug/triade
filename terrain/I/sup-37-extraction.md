sup-37 · extraction du kit embarqué (démo + proxy + annexe, 1 fichier) · révision 1
Intention : la réponse à « fais moi 1 seul exe qui contient tout » — le kit
terrain.1 était QUATRE fichiers à poser côte à côte (superviseur.exe,
demo.exe, proxy.exe, terrain_jetons.bin) ; l'exigence développeur D49 est UN
seul exe téléchargé, double-cliqué, fini. Les trois artefacts vivent désormais
EMBARQUÉS en section .blob (lecture seule) : demo.exe 0.3.0 (16 384 o,
scellé M2), proxy.exe 0.4.0-dev.1 (19 456 o, scellé M3) et l'annexe de
jetons Drive (248 o, la même annexe D48 — intégrée, plus jamais un fichier
à part). Ce bloc les POSE sur disque à côté de l'exécutable avant T1/T2/T3,
relit chaque fichier posé octet par octet (la preuve que le disque porte
l'artefact embarqué, pas une impression), et les retire à la fin du run :
le dossier de test ne contient plus, avant et après, que superviseur.exe et
le journal du run. UNE entrée publique à mode @0x6600 (le dispatch vit à la
première instruction — aucune adresse interne à aligner) : ecx = 0 ->
extraire, ecx = 1 -> nettoyer.
Contrat :
  pre  : P1 appelé par sup-09 APRÈS la porte R10 (l'intégrité de la zone
         .blob est déjà prouvée par la table R10 — la porte couvre la
         section embarquée, entrée « zone blob » : en-tête + demo.exe +
         proxy.exe ; l'emplacement de l'annexe en est EXCLU, propriété de
         la variante) ; P2 BUF_CHEMIN valide (DIR_LONG calculable par
         sup-36 — le pré-nettoyage de l'annexe passe par lui, le préfixe
         répertoire est le sien) ; P3 journal opérationnel ; P4 pile
         alignée ; P5 ecx = mode (0 extraire / 1 nettoyer).
  post : Q1 mode 0, pour demo.exe puis proxy.exe : écriture CreateFileA
         (GENERIC_WRITE, CREATE_ALWAYS — un artefact préexistant du kit
         terrain.1 est REMPLACÉ, l'embarqué fait foi) puis boucle
         WriteFile 512 o DEPUIS l'embarqué (jamais de copie intégrale en
         mémoire : TAMPON_CMD est trop petit, c'est le kernel qui copie) ;
         puis vérification : CreateFileA (GENERIC_READ, OPEN_EXISTING) ->
         boucle ReadFile 512 o dans TAMPON_CMD+ZONE_COMPO (occupations
         séquentielles, jamais concurrentes avec sup-35/36 — propriétaire
         transitoire documenté) + memcmp scellée contre l'embarqué,
         jusqu'à épuisement ; CloseHandle sur TOUT chemin ; Q2 verdicts
         journalisés : succès -> ligne « extrait, octets conformes » +
         ligne md5 attendu (constante posée par le plan, cohérence
         ASSERTÉE au build contre l'artefact scellé) ; écart d'octets ->
         ligne ÉCART, test associé sauté ; échec d'écriture -> ligne
         échec, test associé sauté ; Q3 premier effet du mode 0 :
         pré-nettoyage de l'annexe (sup-36 op 2 — une annexe périmée d'un
         kit terrain.1 ne doit jamais être réutilisée, et l'appel
         initialise le cache DIR_LONG, propriété unique de sup-36) ;
         Q4 annexe : longueur lue au slot (SLOT_JETONS, u64) ; 0 -> ligne
         « variante publique : annexe absente » (T3 sera déclaré non
         applicable par sup-09) ; sinon écriture + vérification idem,
         ligne « annexe extraite - T3 actif » ; écart d'annexe -> ligne
         ÉCART, le fichier CORROMPU reste posé (T3 échouera de lui-même,
         échec honnête — jamais de masquage) ; Q5 mode 0, rax = drapeaux :
         bit 0 = demo.exe posé et conforme, bit 1 = proxy.exe posé et
         conforme, bit 2 = T3 applicable (annexe déclarée par la VARIANTE,
         longueur != 0 — indépendant du succès de sa propre extraction :
         une livraison qui n'arrive pas à poser son annexe doit finir
         ECHEC, pas TOUT OK) ; Q6 mode 1 -> DeleteFileA (via sup-36 op 2)
         sur les trois noms (demo.exe, proxy.exe, terrain_jetons.bin —
         supprimer un fichier absent est bénin), ligne « nettoyage kit »
         journalisée, rax sans signification ; le nettoyage retire les
         fichiers posés par CE run — le journal du run, lui, reste (c'est
         le constat).
  inv  : I1 zéro fuite : tout handle ouvert (écriture ET vérification) est
         fermé sur TOUT chemin (succès, écart, lecture avortée — l'oracle
         liste les CloseHandle observés) ; I2 la comparaison relit le
         FICHIER posé (jamais le tampon d'écriture) — la preuve vit sur le
         disque ; I3 aucune longueur codée en dur : tout vient de l'en-tête
         .blob (le build ASSERTÉ égale les tailles réelles des artefacts) ;
         I4 l'emplacement de l'annexe est le SEUL octet mutable de l'image
         (deux variantes, D49) — hors table R10, jamais journalisé octet
         par octet (interdit 11) ; I5 les noms de fichiers passent par
         les constantes du plan (NOM_DEMO/NOM_PROXY/NOM_JETONS — une
         seule source, celles-là mêmes que T1/T2/T3 lisent) ; I6 le mode
         est dispatché à la PREMIÈRE instruction — aucune adresse interne
         du bloc n'est référencée de l'extérieur.
Échecs :
  E1 : écriture impossible (disque plein, droits) -> ligne échec, bit à 0,
       test sauté — le run continue (constat partiel > arrêt).
  E2 : octets relus en écart (antivirus qui réécrit, disque fatigué) ->
       ligne ÉCART, bit à 0, test sauté.
  E3 : annexe déclarée mais non posable -> bit 2 = 1 quand même, T3
       tournera et échouera de lui-même (S31/S33) — l'échec reste
       lisible, jamais masqué.
  E4 : lecture de vérification avortée (fichier disparu entre écriture
       et relecture) -> traité comme écart (E2).
Vecteurs :
  V1 : round-trip 100 %.
  V2 : émulation nominale — les deux artefacts posés puis relus octet
       conformes (les WriteFile observés portent les octets EMBARQUÉS
       exacts, les ReadFile servis rendent ces mêmes octets), mode 0
       rax = 0b111 (livraison) ; journal : lignes extrait + md5 dans
       l'ordre.
  V3 : émulation publique — slot annexe vide -> rax = 0b011 (bit 2 = 0),
       ligne « variante publique », terrain_jetons.bin JAMAIS écrit
       (pré-nettoyage seul).
  V4 : écriture sabotée (CreateFileA écriture échoue) -> bit 0 = 0,
       ligne échec, T1 sauté par sup-09, T2/T3 quand même.
  V5 : écart injecté (le FS virtuel sert un octet modifié à la relecture)
       -> ligne ÉCART, bit 1 = 0, T2 sauté, nettoyage quand même appelé.
  V6 : falsification — corrompre un octet de la zone .blob fait tomber la
       porte R10 AVANT toute extraction (la table couvre la zone) ; aucun
       fichier posé.
Fixtures    : NOM_DEMO/NOM_PROXY (.rdata ASCII libre), NOM_JETONS (zone
              données sup 2), chaînes S04*/S05*/S06*/S07 (zone données
              sup 3), BLOB_LONGUEURS/BLOB_LONGUEUR_PROXY/BLOB_DEMO/
              BLOB_PROXY/SLOT_JETONS (plan, section .blob).
Provenance  : écrite-avant-code (D49 — l'exigence « 1 seul exe » arrive
              après le constat terrain du 27/10 : quatre fichiers à poser
              main + une fausse alerte Defender sur proxy.exe téléchargé ;
              l'embarqué supprime la manipulation, le manifeste + la
              version de ressource habillent l'exécutable aux yeux des
              heuristiques, l'exclusion antivirus reste documentée côté
              LISEZMOI).
Décisions   : D49 ; sup-36 réutilisé tel quel (op 2 pour les suppressions
              et l'init DIR_LONG — l'écriture/lecture 512 o est LOCALE au
              bloc : sup-36 op 1 écrit depuis TAMPON_COMPO, trop petit
              pour 16 Ko) ; la relecture vit dans TAMPON_CMD+ZONE_COMPO
              (occupation séquentielle — propriétaire transitoire,
              charte terrain) ; jamais de md5 CALCULÉ au run (aucune
              crypto dans le superviseur, dépendance OS assumée) : le md5
              affiché est la constante du plan, prouvée au BUILD par
              assert contre l'artefact scellé — la preuve d'intégrité du
              run, c'est la relecture octet à octet ; le dispatch à mode
              remplace la double entrée fixe du premier jet (aligner une
              étiquette interne à 0x6800 à la main eût été fragile).
