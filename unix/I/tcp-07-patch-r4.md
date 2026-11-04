tcp-07 · moteur de patch à chaud · révision 4
Intention : basculer le bloc CIBLE du jalon entre sa version installée (v1)
et son remplaçant en zone de croissance, SANS JAMAIS écrire un bloc pendant
qu'il s'exécute — le remplaçant est d'abord intégralement copié dans la
croissance, puis l'entrée bascule par UNE écriture alignée unique de qword
(E9 rel32 + NOP x3), atomique sur x86-64 ; le rollback réécrit le qword
original sauvegardé. C'est l'instanciation du mécanisme de patch du profil
(manuel § 7.4) et l'exécution de la boucle de mise à jour § 5 sur du code
vivant.
Contrat :
  pre  : P1 mode (argument 1) : 0 = appliquer le remplaçant, 1 = retour
             arrière ; toute autre valeur est refusée (code 1) ;
         P2 le staging (au plan d'adressage de l'image — frag-loc) contient,
             pour le mode 0, le bloc remplaçant assemblé POUR l'adresse de
             croissance du plan (les déplacements relatifs de sa notation y
             sont résolus) ;
         P3 la table d'intégrité R10 (au plan de l'image) porte le staging en
             première entrée — (rva, taille, somme) : taille 0 = staging
             absent, la somme attendue est celle des qwords du staging ;
         P4 l'état (au plan de l'image) reflète la version active : 0 = v1,
             1 = v2 — maintenu par le seul présent bloc ;
         P5 l'entrée du bloc CIBLE est alignée 16 et ses 8 premiers octets
             constituent la zone trampolinable (R7) — la CIBLE (l'entrée et
             la croissance) vit au plan de l'image (frag-con : Windows M2 —
             le bloc echo, entrée 0x4600, croissance 0x4680 ; Linux corpus —
             le bloc journal tcp-11, l'entrée et la croissance au plan du
             corpus) ;
         P6 la pile est alignée à l'entrée du bloc (rsp ≡ 8 mod 16 —
             discipline partagée, frag-con, § 8.3-4).
  post : Q1 mode 0 réussi : la croissance (taille du staging) contient octet
             pour octet le staging ; les 8 premiers octets de l'entrée CIBLE
             contiennent E9 <rel32 vers la croissance> suivi de trois NOP ;
             l'original de ces 8 octets est conservé (au plan de l'image) ;
             l'état passe à 1 ; retour = 0 ;
         Q2 mode 1 réussi : les 8 premiers octets de l'entrée CIBLE sont
             restaurés à l'identique de l'original sauvegardé ; l'état passe
             à 0 ; retour = 0 ; la croissance n'est pas effacée (le
             remplaçant y dort, réactivable) ;
         Q3 l'écriture de bascule et celle de rollback sont chacune UNE
             seule écriture alignée de qword à l'entrée CIBLE (atomicité
             x86-64) — jamais deux écritures partielles observables ;
         Q4 pendant les écritures, la page du code est passée en lecture +
             écriture + exécution par le service de protection de pages du
             profil (frag-con : Windows — PAGE_EXECUTE_READWRITE 0x40, puis
             restaurée PAGE_EXECUTE_READ 0x20 ; Linux — PROT_READ|PROT_WRITE|
             PROT_EXEC 0x7, puis restaurée PROT_READ|PROT_EXEC 0x5), puis
             restaurée après la bascule — l'image reste exécutable en continu
             (I6, D39 : la page protégée contient le présent bloc lui-même) ;
         Q5 refus fail-closed (retour = code, AUCUN octet de code modifié,
             état inchangé) : code 1 mode invalide ; code 2 staging absent
             (taille 0) ; code 3 somme du staging divergente (intégrité
             douteuse — l'installation d'un remplaçant corrompu est
             interdite, R10) ; code 4 état incohérent avec la demande
             (appliquer alors que v2 actif, retour alors que v1 actif) ;
             code 5 le service de protection a refusé (avant toute écriture
             pour la phase d'ouverture ; après la bascule pour la phase de
             restauration) ;
         Q6 en cas d'échec de la restauration de protection APRÈS bascule
             réussie (mode 0), retour = 5 mais la bascule est effective et
             l'état est mis à jour (défaut documenté : l'image reste
             inscriptible et exécutable — le processus est dans un état
             incohérent, l'appelant journalise le refus).
  inv  : I1 appels au service de protection du profil (frag-con : Windows —
             IAT kernel32 VirtualProtect exclusivement, deux par opération
             réussie ; Linux — syscall mprotect direct, deux par opération
             réussie) ; appels internes : libc-01 memcpy (copie staging ->
             croissance) exclusivement ;
         I2 aucune autre zone de code n'est écrite que l'entrée CIBLE
             (8 octets) et la croissance (taille staging) ;
         I3 le qword de bascule est construit hors de l'image (registre),
             puis posé par mov qword ptr [entrée], reg — l'écriture n'est
             jamais décomposée ;
         I4 le prologue réserve le cadre exigé par la convention du profil
             (frag-con) et sauvegarde les non volatils de travail ;
             l'épilogue restaure symétriquement ;
         I5 aucun stockage sous rsp au moment d'un appel ; la loge de
             l'ancienne protection vit dans la réserve du sous-programme de
             protection (frag-con : Windows — la zone d'accueil ABI msx64 de
             0x28 octets, D41 ; Linux — aucune zone d'accueil, le syscall ne
             range rien chez l'appelant) ;
         I6 D39 (R2) : toute protection appliquée à une page contenant du
             code en cours d'exécution RETIENT le bit exécution — les phases
             d'écriture passent par la constante lecture+écriture+exécution
             du profil (0x40 Windows / 0x7 Linux), jamais la constante
             lecture+écriture seule (4 / 3) : en x86-64 le DEP est permanent,
             une page sans bit exécution faute à l'instruction suivante et
             tue le processus ;
         I7 D41 (R3) : le sous-programme de protection honore l'obligation
             ABI du profil AVANT l'appel au service (frag-con : Windows —
             0x28 octets de zone d'accueil, le code système /homeparams y
             range ses arguments, un défaut tua le processus au terrain
             démo.6 ; Linux — le syscall mprotect ne touche que rcx/r11,
             aucune zone d'accueil n'est exigée).
Échecs :
  E1 : staging absent ou corrompu → refus AVANT toute écriture (Q5) : le
       serveur continue de servir en v1 — la disponibilité prime (ordre
       lexicographique : sécurité d'abord, service ensuite).
  E2 : état incohérent (double application, rollback à vide) → refus code 4
       sans effet — les commandes répétées sont légitimes, le moteur est
       idempotent par refus.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : scénario complet (oracle) : appliquer → croissance = staging octet
       pour octet, entrée = E9 rel32 + NOP x3 (cible exacte : la croissance
       du plan), original sauvegardé, état 1, appels au service de protection
       appariés (exécution+écriture puis exécution seule) ; l'entrée APPELÉE
       retourne le comportement du remplaçant — LE PATCH EST EFFECTIF ;
       rollback → entrée restaurée octet pour octet, état 0, comportement v1
       de retour (couvre Q1-Q4, I6, I7).
  V3 : falsification du staging (un octet corrompu) → code 3, entrée
       inchangée, comportement v1 préservé (couvre Q5, E1, R10).
  V4 : états incohérents (appliquer x2, rollback x2, rollback sans
       application) → code 4, aucun effet (couvre E2).
  V5 : patch EN SESSION : bascule appliquée entre deux usages d'une même
       session — l'usage continue, le comportement change à l'usage suivant,
       sans interruption de service (critère de sortie M2 côté Windows, du
       chantier M6-(d) côté Linux).
  V6 : test de rejet : toute notation écrivant ailleurs que l'entrée/la
       croissance pendant la bascule, ou basculant par écritures partielles,
       est refusée par l'oracle structurel (couvre I2, I3).
  V7 : falsification DEP (D39, R2) : la constante de phase d'écriture
       réécrite vers la constante sans bit exécution (0x40 → 0x04 Windows,
       0x7 → 0x3 Linux — le défaut terrain exact et son équivalent) →
       l'exécution FAUTE au fetch depuis la page non exécutable au retour du
       service — zéro silence (couvre I6).
  V8 : falsification zone d'accueil (D41, R3, INSTANCE WINDOWS) : la réserve
       du sous-programme de protection réécrite 0x28 → 0x08 → le shim range
       rdx sur l'adresse de retour → l'émulation FAUTE au ret — zéro silence
       (couvre I7 ; l'instance Linux n'a pas de zone d'accueil — le
       paramétrage frag-con le documente, le vecteur est la propriété de
       l'instance Windows).
Fixtures    : staging et table d'intégrité au plan de l'image (le corpus
              dev.2 : le bloc remplaçant assemblé pour l'adresse de
              croissance ; l'absence : taille 0).
Provenance  : écrite-avant-code.
Décisions   : D7, D8, D33 (croissance/staging), D39 (protection : DEP
              permanent x64), D41 (zone d'accueil ABI msx64), R4 (contrat
              stable), R7 (entrée seule trampolinable), R10 (somme avant
              effet), D149 (révision de granularité).
Historique  : R1 (dev.1) révisée en R2 (terrain démo.4, D39) : les phases
              d'écriture passaient la page 0x4000 — qui contient le présent
              bloc — en PAGE_READWRITE (4), valeur sans bit execute : au
              retour du premier VirtualProtect, le fetch de l'instruction
              suivante violait DEP/NX et tuait le processus. Le diff se
              limite aux constantes de protection 4 → 0x40 aux deux sites et
              à Q4/I6/V2/V7 ; signature, codes d'échec et effets inchangés
              (R4). L'oracle applique désormais réellement les permissions
              (D39). R2 révisée en R3 (terrain démo.6, D41) : .protger
              appelait VirtualProtect avec sub rsp,8 : aligné au bit près,
              mais SANS les 0x20 octets de zone d'accueil ABI — kernel32
              (/homeparams) range rdx exactement sur l'adresse de retour, le
              ret saute à 0x700 et tue le processus. Diff limité à .protger
              (3 octets) ; I4/I5 précisés, I7/V8 ajoutés, V2 amendé ;
              signature, codes d'échec et effets inchangés (R4). R3 (m2/I,
              instance Windows scellée 0.3.0 dans echo.exe) révisée en R4 au
              chantier M6-(b) : la révision de granularité (D149-(3)) — le
              mode quitte rcx pour son NOM, la CIBLE et la croissance
              quittent les RVA littéraux de l'image M2 pour le plan de
              l'image (frag-loc), le service VirtualProtect devient « le
              service de protection de pages du profil » (mprotect chez
              l'instance Linux, syscall direct — aucune IAT au jalon), les
              constantes PAGE_* deviennent les constantes du profil
              (frag-con : 0x40/0x20 ↔ 0x7/0x5), la zone d'accueil devient
              une obligation du profil (I7 : 0x28 Windows, néant Linux) ;
              les OBSERVABLES — les six codes de refus nommés (Q5), la
              bascule atomique alignée (Q3), la croissance octet pour octet
              (Q1), le rollback (Q2), l'appariement des protections (Q4) —
              sont INVARIANTS ; l'instance Windows scellée demeure conforme.
