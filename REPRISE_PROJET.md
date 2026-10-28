# REPRISE DU PROJET TRIADE — Fichier d'instruction

> Objet : reprendre le projet TRIADE là où il s'est arrêté, en moins de dix minutes, sans
> relire l'historique des conversations. Ce fichier est auto-suffisant : tout ce qu'il
> mentionne est présent dans la sauvegarde. Il s'adresse autant au développeur qu'à un
> agent IA chargé de continuer le travail.

- Dernière mise à jour : 28 octobre 2026
- Version de la spécification : v0.5.2 (garde durable de la phrase de contrôle du coffre-fort D81 — § 1.6, § 15.3, § 17.6 ; révisions antérieures : v0.5.1 coffre-fort D75 ; v0.5.0 validation normée § 8.4, taxonomie X1-X8 § 8.5, budget 64 tokens D31) ; **programme v0.6.0 « souveraineté cryptographique » OUVERT (D84–D87)** — exigences consignées, spécification à venir à l'implémentation ; **dépôt sous licence BSL 1.1** (D84, concédant Alexis Lopez)
- État général : conception terminée, infrastructure de sauvegarde opérationnelle, **méthode démontrée à échelle réelle** (recodage RoomEq v3), **jalons M0 et M1 franchis** (validations terrain Windows 11 constatées) — M1 clos à la **balise finale `0.2.0`** (D32 : ligne unique `TRIADE M1 : minilibc 21/21 OK`, cristallisation 11×10/10, conformité 68/68, budgets mesurés, adresses stables démontrées) ; **M2 clos à la balise finale `0.3.0`** (D43 : boucle § 5 DÉMONTRÉE sur machine réelle — journal terrain demo.8, 28/28 lignes jusqu'à « DÉMO OK » ; conformité 124/124 ré-exécutée au scellage ; rc.2 = correctif IAT D35 ; rc.2 = correctif IAT D35 ; rc.3 = correctif DEP D39 : tcp-07:R2 — la phase d'écriture du patch passait SA PROPRE page en PAGE_READWRITE sans execute, tuant le processus au premier VirtualProtect ; oracle durci qui APPLIQUE les permissions réelles, 50 532 cas, cristallisation 10/10, conformité 124/124 ; constat terrain : porte R10 + libc 4/4 + CLIC démontrés sous Windows 11, la boucle § 5 complète attendue pour le scellage final 0.3.0 ; rc.4 = correctif D41 : tcp-07:R3 — .protger réservait 8 octets au lieu de 0x28 avant l'appel IAT VirtualProtect : kernel32 (/homeparams) rangeait rdx=0x700 sur l'adresse de retour de .protger, le ret sautait à 0x700 et tuait le processus ; oracles durcis /homeparams, 50 533 cas, cristallisation 10/10, conformité 124/124) ; **jalon démo : demo.exe 0.3.0-demo.9 livré (D43 — FINALE de lignée sans sondes ; md5 73c064fb…)** — demo.1 : fenêtre vide (RECT.top lu comme largeur, D36) ; demo.2 : démarrage corrigé et VALIDÉ terrain (journal 24 : L00→L02→L01, zéro LKO) MAIS capture terrain 26/10 20:56 : ÉCRAN VIDE au démarrage (traces fichier seul — spec win-02:R2 « jumeau silencieux », D37) et bouton non rendu ; demo.3 (D37) : miroir universel win-05:R3 (écran PUIS fichier, entrée trace @0x5000 + shim scénario @0x5100, .text2 0x1400/image 0x6000/fichier 16384 o) + diagnostics L4C/L4D — **VALIDÉ terrain 26/10 22:11** (journal 150 o : L00→L02→L4C=1→L4D=1→L01, la fenêtre AFFICHE son démarrage ; capture : 4 lignes lues, géométrie edit h-56 confirmée au pixel, DPI 125 %) MAIS bouton ENCORE invisible avec L4D=1 → **D38 : w/h de WM_SIZE vivaient en r10d/r11d VOLATILES relus après l'appel MoveWindow** (syscall écrit RFLAGS dans r11 par matériel → bouton placé hors client avec retour VRAI — invisible en statique, bénit par un oracle dont les shims ne modélisaient pas l'ABI caller-saved) ; demo.4 : **win-04:R4** (w/h en r14d/r15d callee-saved, invariant I6, taille identique) + **oracle durci : clobber des volatiles à chaque retour IAT** (r10=0, r11=0x246 réaliste, 78 cas verts, falsification V5 — réécrire les usages en r10d/r11d fait échouer l'invariant géométrique : le bouton invisible est impossible à réintroduire) ; défaut latent même classe dans libc-09 (M2, non embarqué, scellé carte) DIFFÉRÉ à la prochaine révision M2 (scanner garde : scripts/scan_abi_volatile.py) ; sha256:7e4e9105… ; **terrain 26/10 21:53 : LE CLIC A EU LIEU (D38 validé sur machine réelle — L03), porte R10 VERTE + libc 4/4 verts exécutés sur terrain, puis MORT en phase mécanique : D39 — tcp-07 passait SA page 0x4000 en PAGE_READWRITE (SANS bit execute) : DEP permanent en x64 → violation NX au retour du premier VirtualProtect, processus mort net, journal gelé après J_LIBC_OK (5e classe de défaut invisible sans exécution : sémantique de protection non modélisée — le shim VirtualProtect acquittait sans appliquer ; la spec R1 elle-même exigeait RW)** ; demo.5 : **tcp-07:R2** (PAGE_EXECUTE_READWRITE 0x40 pendant les écritures, invariant I6 « jamais de phase non exécutable pour la page du code en cours », restauration RX inchangée, diff 2 constantes) + cascade M2 **rc.3 scellée** + oracles durcis des deux côtés (permissions réelles, appariement RWX/RX 8/8, falsification V7 : 0x40→0x04 doit FAIRE FAUTER l'émulation — par appel direct, la porte R10 détecterait l'octet avant la mécanique) ; sha256:dc5215c5… ; **terrain 26/10 22:34 : journal demo.5 = MÊME FRONTIERE (10 lignes, gel après J_LIBC_OK) alors que L00 prouve que c'est le binaire corrigé qui a tourné — le DEP était nécessaire mais pas suffisant : audit exhaustif SANS défaut (binaire fidèle, payload v2 position-indépendant, .reloc vide → base préférée, oracle 79 cas verts re-exécuté) → 6e classe de défaut invisible sans exécution terrain (D40)** ; demo.6 : **win-09:R2 INSTRUMENTÉE (D40)** — 3 sondes de trace mode 0 (avant écho#1 / après tcp-07 pose / après memcmp v2) qui écrivent le journal fichier à chaque frontière : la dernière sonde visible localisera l'instruction mortelle ; slot win-09 0x380→0x3C0 (trou libre 0x4F80-0x4FFF), sondes en interstices .rdata (0x2748/0x276C/0x22F1, zones pleines), oracle durci (journal nominal 14 lignes, entrée trace 0x5000 déclarée, sondes dans les données RIP autorisées) ; 79 cas verts, falsification 28/28, héritage R7 intact, carte re-scellée ; sha256:1ad1b7df… ; sondes TEMPORAIRES (retrait R3 après correction) ; **terrain 27/10 : journal demo.6 lu (12 lignes, mort après « sonde1 avant echo », fenêtre disparue = crash processus) — les sondes ont localisé l'intervalle ; D41 : écho v1 (11 instructions pures) et memcmp (prouvé au sceau 4/4) éliminés, la POSE coupable — .protger appelait VirtualProtect SANS zone d'accueil ABI msx64 (7e classe de défaut invisible : obligation côté appelant, kernel32 /homeparams range rdx=0x700 sur l'adresse de retour → ret vers 0x700) ; audit systémique 58 sites IAT : 57 sains, 1 défaillant ; demo.7 : tcp-07:R3 (sub/add rsp,0x28 + lea r9,[rsp+0x20], diff 3 octets, zéro déplacement déplacé), M2 rc.4 scellée en cascade, oracles durcis /homeparams (M2 50 533 cas + V8, démo 80 cas + V8, falsification 28/28), shadow space 58/58 sain, diff demo.6→demo.7 chirurgical 7 octets ; sha256:1917c9af… (md5 89cf9e23…) ; attente terrain : journal demo.7 complet 14 lignes jusqu'à « boucle § 5 complète — DÉMO OK » → retrait des sondes + scellage final 0.3.0 ; **terrain 27/10 : journal demo.8 lu — 28/28 lignes jusqu'à « boucle § 5 complète - DÉMO OK » : LA BOUCLE § 5 EST DÉMONTRÉE SUR MACHINE RÉELLE** (D42 validé : le premier échange — point de mort de demo.7 — a vécu ; S1/S2 lus après « client : connecté », course bénigne documentée ; sonde4/sonde5 autour de chacun des 3 échanges identité/MAJUSCULES/retour ; D43 : 8e classe = section critique R_CS jamais initialisée dans l'hôte démo — win-09:R3 init en tête de scénario, le devoir de tcp-12 non embarqué) ; demo.9 (D43) : retrait de TOUTES les sondes (win-08:R3/win-09:R4/win-10:R3 — 140 o de code, 7 chaînes retour zéro, diff chirurgical 1 047 o zéro hors zone, correctifs D41/D42 VIVANTS, oracle 86 cas verts + journal nominal 11 lignes exactes = anti-régression du retrait, audit_demo9.py TOUT CONFORME) — FINALE de lignée ; **M2 scellé 0.3.0** (opération de carte, modèle M1 0.2.0 : conformité 124/124, balise rc.4→0.3.0, re-scellage Ed25519)** ; **jalon M3 en cours (ouvert D45)** : harnais de fuzzing P1-P5 falsifiable (101 000 cas sans crash sur la surface scellée), couche I écrite-avant-code — 13 spécifications http-xx + tcp-13 (D46) ; **étape (b) accomplie (D47, journal 36) : proxy.exe 0.4.0-dev.1 scellé** — plan d'adressage arrêté sur les mesures réelles, 13 notations à la main, oracle à scénarios 153 036 cas verts + falsification détectée, carte génération 5 (38 blocs sur 4 artefacts, verrou croisé 38), R7 : 13 blocs octet-identiques M0/M1/M2 ; deux révisions nées de l'implémentation : http-06:R2 (le trou du succès excessif — une tête > 8192 AVEC terminateur était un succès : contournement 431 + débordement du tampon de réécriture http-10), http-10:R2 (corps relayé par boucles tcp-03/04 INLINE bornées Content-Length — http-09 s'arrêterait à l'EOF du client qui attend la réponse : interblocage ; pompe détachée (amont<<32)|cliente) ; défaut http-08 attrapé par le différentiel (deux-points en position 0 sans « // » → verdict 1, pas 3) ; sha256 85d2aa21c1532a50… ; **chantier lignée sceau `m7/` : échelon 2 de l'échelle d'auto-hébergement D34** (vérification native — SHA-512 natif scellé 0.8.0-dev.1, Ed25519 en cours ; NB : `m7/` est un emprunt de nommage au sens D34/m6, le jalon M7 RISC-V du plan reste inchangé) ; **lignée terrain (D48, journal 37) : superviseur.exe 0.5.0-terrain.2 scellé** — la réponse à l'exigence du développeur (TOUS les tests en 1 clic par une GUI + journal téléversé automatiquement dans le dossier test du Drive) : T1 rejoue demo.exe SANS main humaine (fenêtre trouvée, bouton cliqué, 17 lignes exactes vérifiées, journal embarqué brut), T2 lance proxy.exe et le traverse par curl (http + https tunnel, événements console vérifiés, « quit », exit 0 — C'EST le run de l'étape (c) de M3), T3 téléverse le journal du run (nom unique terrain_YYYYMMDD_HHMMSS.txt) par curl.exe relais TLS via la voie drive_sync.py exacte ; 22 blocs embarqués dont 11 octet-identiques R7 (coquille démo éprouvée D36-D43), oracle 807 verrous + 10 080 cas verts + falsification 24/24 + 5 mutations, carte génération 5 (22 empreintes, cristallisation 10/10), sha256 d73aa99c… ; annexe terrain_jetons.bin (4 champs NUL, 248 o, interdit 11 — posée au dossier test par le canal de livraison, jamais au dépôt) ; **terrain.2 (D49, journal 38) : kit embarqué** — « 1 seul exe qui contient tout » : demo.exe + proxy.exe + annexe de jetons dans la section .blob (lecture seule), extraction vérifiée par relecture octet à octet puis nettoyage, VERSIONINFO + manifeste asInvoker en .rsrc, 61 952 o, 23 blocs, oracle 10 102 cas verts, audit 53 contrôles ; **constat développeur 27/10 soir : « il ne se passe rien quand je lance superviseur.exe » → terrain.3 (D50, journal 39)** : le champ PE SizeOfHeaders valait 0x200 (écrit L.FILE_ALIGN, juste par coïncidence pour ≤ 4 sections) pour 0x238 o d'en-têtes réels à SIX sections — la table des sections débordait de la zone déclarée, le chargeur Windows refusait l'image AVANT TOUT CODE (9e classe de défaut invisible à l'émulation : l'oracle mappait par le plan, jamais par l'en-tête du fichier) ; correctif UN OCTET (offset 0x95 : 0x02→0x04, SizeOfHeaders 0x400), règle chargeur imposée au build + à l'oracle (falsifiable : il rejette désormais terrain.2 avec le diagnostic exact) + à l'audit (61 contrôles, dont aucune zone R10 ne couvre les IAT mutées par le chargeur), re-scellage 0.5.0-terrain.3 (u64 0x00050103), diff chirurgical 23/23 blocs intacts + 3 octets .rdata + 1 octet .text2 + 1 octet d'en-tête, cristallisation 10/10 (graines 22-31), publique md5 2fb19c0f… / livraison md5 40b2f350…, LISEZMOI v3 ; premier journal terrain_*.txt attendu (la fenêtre doit s'OUVRIR au double-clic)** ; **lignée terrain terrain.4→terrain.16 (D51–D71) : seize générations pour faire vivre T3** — les tueurs de runs nommés un à un : ABI shadow space du superviseur (D62 : sup-34 .curl appelait l'IAT sans zone d'accueil 0x28 — spill homeparams sur l'adresse de retour, signature exacte des morts au premier curl ; correctif 2 octets imm8 08→28, terrain.10 survit), pile du proxy 0x7100 sans probing (D63 : http-10:R3 écrit à la main, **proxy.exe 0.4.0-dev.2 scellé** — oracle 153 036 cas verts, md5 dd12b649…, embarqué au superviseur terrain), **T2 VERT HISTORIQUE (D64, run 22:10)** puis 6 verts consécutifs — l'étape (c) de M3 est validée terrain ; T1 élucidé (D64 : l'échec démo était un ARTEFACT DE MESURE DOUBLE — le kit embarquait demo10-diagnostique dont le journal 706 o était coupé à 640 par le lecteur ; la démo publique 73c064fb n'a JAMAIS réussi sur machine réelle : D57, exit 0xC0000005, 5e reproduction propre — adresse de plantage attendue via WER/Observateur d'événements côté développeur) ; la chasse T3 : --fail interdisait toute réponse d'erreur sur disque (D65), le nettoyage sup-35 détruisait terrain_jeton.json même écrit (D68 : 5→4 DeleteFileA, terrain.14), Google répond en JSON INDENTÉ et curl HTTP/2 écrit location: en minuscules (D69 : l'étiquette compacte cherchée était absente du réel → rax=0 « jeton KO code=0 » ; --http1.1 forcé, terrain.15), S33 réussit puis mort 2 ms plus tard par débordement du tampon de composition 484>352 sur .text2 non inscriptible (D70 : TAMPON_COMPO 0x3100 1888 o + PUT quoté, terrain.16) ; **run 16 (D71, 28/10 06:54) : T3 DÉMONTRÉ DE BOUT EN BOUT SUR MACHINE RÉELLE — PREMIÈRE FOIS — le journal terrain_20261028_065408.txt est parti TOUT SEUL dans le dossier test** (md5 5221e0c2…, 56 lignes finissant à S34 par construction — cliché lu à l'instant du PUT ; superviseur-terrain16.exe md5 34ee9f58… == LISEZMOI, chaîne de garde fermée, kit 73c064fb/dd12b649 conformes ; T2 6e vert consécutif ; D48 réalisé au bout de 16 générations) ; **D72 (28/10) : étape (d) de M3 ACCOMPLIE — campagne million** : harnais `m3/fuzz_million.py` (686 lignes, tracké, FALSIFIABLE — deux mutations d'un octet du proxy scellé détectées : table des méthodes @0x16A0, réponse 400 @0x1769 ; témoin sauvage PASS), 1 000 000 cas SANS CRASH en 175 s sur le périmètre D46 (900 000 différentiels feuilles http-01..09 + 100 000 requêtes complètes http-10 à propriétés P1-P5, 8 générateurs nommés, 200/200 sentinelles canoniques, rejeu sur état vierge de tout échec — zéro), re-exécution à graine neuve 20261029 : même verdict en 176 s (2 × 10^6 cas cumulés), rapport `m3/rapport_million.json` ; **D73 (28/10) : étape (e) de M3 ACCOMPLIE — le fuzzing rejoint la conformité** : suite de conformité § 8.2 livrée (`m3/conformite_profil.py`, 161 contrôles — éléments 1-7 constatés depuis proxy.exe [26 blocs, 23 slots IAT, porte R10, héritages R7] + contrôle de jalon « fuzzing à propriétés » : harnais D72 réutilisé intégralement, 10^4 cas SANS CRASH par exécution [9 000 feuilles + 1 000 accumulation P1-P5], graine datée reproductible, auto-test de falsification inclus ; suite VERTE, re-exécution à graine neuve identique, ~2 s tout compris ; falsifiable — trois mutations d'un octet détectées, témoin vert ; `conformite.txt` lu par le tableau de bord) ; **D74 (28/10) : M3 SCELLÉ à la balise finale 0.4.0 — jalon CLOS** : lignée de clés régénérée (4e réinitialisation, D27/D30 réappliquées — preuve byte-identique : proxy.exe régénéré md5 dd12b649… égal au scellé D63, l'artefact n'a pas bougé d'un octet), cristallisation 38/38 × 10/10 (19 vérifications graines 1-19 ; l'asymétrie R6 de l'héritage non embarqué corrigée au passage, modèle journal 18 m2), 0.4.0-rc.1 puis 0.4.0 FINALE sur la validation terrain consignée (T2 6×, D64-D71), conformité 161/161 re-exécutée à chaque scellage, garde anti-rollback posée (toute reconstruction d'une carte cristallisée refusée) ; **état des enveloppes : les cartes m0/m1/m2/terrain restent chiffrées à l'ancienne lignée D30 (illisibles depuis la restauration D71 — état préexistant) ; la nouvelle phrase maîtresse est au coffre du développeur depuis la fin de session D74** ; **D75 (28/10) : coffre-fort des phrases maîtresses — composant du protocole (spécification v0.5.1)** : conteneur chiffré TRIADE-CF1 (`coffre_fort.py`, racine du dépôt — l'outil est public, le conteneur jamais) centralisant TOUTES les phrases maîtresses PAR PROJET : phrase de contrôle au coffre développeur (jamais stockée, affichée UNE fois), Argon2id 64 Mio/3 it + HKDF contexte dédié + XChaCha20-Poly1305, autotest de falsification 19/19 PASS ; conteneur exporté chiffré au racine du coffre Drive (copie projet) + copie développeur (download/) ; la phrase courante (lignée D74) y vit dès à présent — l'ancienne phrase D30 doit y être AJOUTÉE par le développeur (`ajouter TRIADE lignee-D30`) ; relève post-réinitialisation SANS cérémonie : importer le conteneur puis `obtenir TRIADE lignee-D74 --vers-fichier .keys/passphrase.txt` ; terrain : D57 (WER) seul point ouvert ; **D76 (28/10) : coffre Drive nettoyé** — douze livrables périmés archivés dans le sous-dossier `ARCHIVE/` de la racine (avec LISEZMOI-ARCHIVE.txt explicatif ; outil `scripts/drive_archiver.py` : déplacement vérifié md5, idempotent, JAMAIS de suppression), la racine ne porte plus que les courants (instructions, miroir TRIADE/, Tokens/, coffre-fort, demo.exe + LISEZMOI à jour, dossier test du terrain) ; suite : M4 (tunnel chiffré Schannel) ; **D78 (28/10, 11:30) : incident D76 RE-QUALIFIÉ — le reliquat exposé portait la phrase COURANTE, pas D30** : le fichier « phrase maitresse triade.txt » (52 o = étiquette 16 car. + phrase 32 hex, modèle D27) déposé manuellement au miroir Drive à 09:38:44 UTC (34 min après la cérémonie D74 — le développeur y avait consigné sa phrase neuve) contenait la phrase ACTIVE D74 — preuve croisée `scripts/preuve_d78.py` 10/10 : octet-identique à `.keys/passphrase.txt`, DÉCHIFFRE frag-loc de la carte m3 (génération 5) et ÉCHOUE sur la carte m2 (génération 2) ; l'audit D76 avait comparé le FICHIER ENTIER (étiquette comprise) à la phrase nue — erreur nommée : les comparaisons de secrets se font sur le contenu extrait ; exposition ≈ 64 min (09:38:44 → corbeille 10:42) de la phrase active sur le dossier partagé par lien ; graine Ed25519 jamais exposée (l'intégrité signée des artefacts est intacte — la phrase ne protège que la confidentialité des cartes au repos) ; copies en clair locales détruites (quarantaine D76 + reliquat, md5 consignés) ; la phrase vit AUSSI au coffre-fort (entrée `lignee-D74`, D75) — le conteneur n'a pas bougé d'un octet (md5 ed2de621…, export Drive vérifié aller-retour) ; RESTE DÉVELOPPEUR : VIDER la corbeille Drive (urgent — copie de la phrase active, récupérable 30 j) + décider de la rotation de lignée (recommandée par prudence, exécutable au prochain « go », modèle D74) ; **D79 (28/10, 12:35) : M4 étape (b) ENGAGÉE — les trois feuilles pures prouvées** : `m4/layout.py` (plan .text3 @ 0x6000, héritage M3 réexporté, **liste blanche HRESULT VÉRIFIÉE à la source — 3 constantes corrigées** : DECRYPT_FAILURE 0x80090330 [0x80090321 = BUFFER_TOO_SMALL], CONTEXT_EXPIRED 0x00090317, CERT_WRONG_USAGE 0x80090349), notations à la main tls-01/02/03 (89/156/284 o, slots D8 0x80/0x100/0x140), `m4/harnais_feuilles.py` — différentiel de spécification **ZÉRO écart** (20 009 hôtes + 125 274 HRESULT [codes exacts, voisins à un bit, hors domaine] + 20 304 triplets, graines 20261028/29, ~95 s), canaris + non-volatils + terminaison constatés, falsification 6/6 mutations attrapées ; leçon d'émulation : le cache de traduction unicorn n'est PAS invalidé par mem_write sur du code exécuté — chaque chargement reconstruit l'émulateur ; reste (b) : tls-04..08 + révisions http + oracle à shims SSPI + carte génération 6 + proxy.exe 0.5.0-dev.1 ; **D80 (28/10, 12:35) : ROTATION DE LIGNÉE EXÉCUTÉE — l'exposition D76-D78 est refermée** : la phrase maîtresse D74 (exposée ≈ 64 min) est retirée du service, **lignée D80 opérationnelle** (128 bits, modèle D27, jamais affichée — vit en `.keys/passphrase.txt` + coffre-fort entrée `lignee-D80`) ; **carte m3 re-scellée à faits strictement inchangés** (pré-vol `prevol_rotation_d80.py` : la phrase D74 n'ouvrait QUE la carte m3 — terrain/m0/m1/m2/démo échouaient, le glissement D78 « m3+terrain » est corrigé par la preuve) : les QUATRE fragments clairs OCTET-IDENTIQUES, MÊME graine Ed25519 (cle publique inchangée), en-tête version=0.4.0 generation=5 inchangés, empreinte_racine nouvelle, proxy.exe inchangé dd12b649… ; re-vérification graine 21 verte (R5 38/38, oracle 524 verrous + 153 036 cas, R8 38, frag-loc/con régénérés octet-identiques, journal R6 gagne le run) ; **coffre-fort roté** (modèle D78 : ré-init + re-scelage — la phrase de contrôle D75 vit au seul développeur) : DEUX entrées `lignee-D74` (archive, « ne plus sceller avec ») + `lignee-D80` (courante), relèves prouvées octet pour octet + cryptographiques, export chiffré download/ + racine Drive (md5 0323029a…) ; **l'ancienne phrase de contrôle D75 est INOPÉRANTE** — la nouvelle est remise par cérémonie de fin de tour (affichage UNE fois puis destruction du fichier de session) ; copie claire D74 détruite (vit chiffrée au coffre + cartes d'archive git) ; le bilan de cérémonie portait un faux négatif nommé (virgule absorbée par `\S+` — constat `constat_d80_bis.py` : graine=21, version=0.4.0, empreinte bf02769f… conformes, bilan effectif 36/36) ; **D81 (28/10, 14:30) : la phrase de contrôle du coffre-fort PASSE SOUS GARDE DURABLE (consigne développeur, spécification v0.5.2)** — la session d'exécution de D80 était MORTE avant la cérémonie de remise : la phrase ne vivait plus que dans le bac à sable, un décès d'infra de plus et le coffre entier devenait indéchiffrable ; nouvelle discipline : PRODUITE → SAUVEGARDÉE AVANT TOUTE AUTRE ACTION (`PHRASE-CONTROLE-COFFRE.txt` au racine du dépôt [commit dédié f652234, GitHub, miroir Drive] + racine du coffre Drive, md5 vérifiés) → LE FICHIER EST LA REMISE (l'affichage unique de cérémonie cesse d'être le canal de survie) ; restauration post-panne PROUVÉE de bout en bout (phrase téléchargée du Drive → conteneur ouvert → entrées listées) ; cahier V1–V12 TOUS PASSÉS, PDF v0.5.2 QA 12/12 ; arbitrage consigné : risque de PERTE (vécu) > risque d'EXPOSITION (URL non devinable) — la confidentialité au repos repose désormais sur le contrôle d'accès au dossier Drive (mitigation première : RESTREINDRE le partage par lien) ; fichier de session détruit (md5 consigné) ; **D82 (28/10, 15:30) : M4 (b) — cadre de session TLS + extension .rdata/IAT secur32 ARRÊTÉS, tls-05 notée-mesurée-prouvée** (premier bloc À SHIMS du jalon : harnais `m4/harnais_cles.py` V1-V4 — round-trip 251 o + tls-02 intégrée, dix scénarios cadre octet par octet, 5 000 cas fuzzés zéro écart [graines 20261028/29], six mutations d'un point attrapées, témoin vert 7/7 ; le WIP était mort avec la session D80 — récupéré, re-vérifié vert, committé)

---

## 1. Le projet en 30 secondes

TRIADE est un protocole permettant à un agent IA de développer, vérifier et mettre à jour du
**code machine natif pur** — sans compilateur ni langage de programmation — guidé par une
carte de balises. Depuis la v0.3, le protocole est **universel** : toute plateforme/OS/
architecture est un profil de cible vérifiable, et le profil primaire de validation est
x86-64 / Windows 11 (exécutables PE32+ écrits à la main). Le principe repose sur trois
couches indissociables : la couche I (Intention) porte les contrats et spécifications,
indépendants de la cible ; la couche B (Binaire) porte les octets scellés réellement
exécutés, un binaire par profil ; la couche C (Carte) est l'index signé, chiffré et
fragmenté qui lie les deux et sert d'unique interface de développement à l'agent. Le
livrable est 100 % code machine ; la Carte reste strictement privée, détenue côté
développeur — mais récupérable et transférable grâce à l'export de continuité chiffré.

L'application de validation est un outil de pentest de type intercepteur MITM (tests
autorisés en environnement de laboratoire uniquement, machine virtuelle isolée). Les
priorités du projet sont ordonnées lexicographiquement et ne se marchandent pas :
**Sécurité > Performance > Optimisation > Coût en tokens**.

## 2. État actuel du projet

| Domaine | État | Détail |
|---|---|---|
| Spécification v0.5.2 | Terminée | `docs/PROTOCOLE_TRIADE.md` (source de travail) et `docs/Protocole_TRIADE_v0.5.2_Specification.pdf` (archive formelle, chaîne LaTeX/Tectonic `scripts/spec_v052/` — née spec_v040 → spec_v050 → spec_v051, D25/D44/D75/D81) ; v0.5.2 (D81) : garde durable de la phrase de contrôle (§ 1.6, § 15.3, § 17.6), menace du vol du coffre étendue (§ 13.1), M4 ouvert constaté (D77) ; cahier de vérification V1–V12 (`scripts/spec_v052/verify_spec.py`) ; archives v0.5.1, v0.5.0, v0.4.0, v0.3, v0.2 conservées |
| Journal des décisions | Suivi | D1–D50 consignées dans `docs/DECISIONS.md` (format normalisé depuis D24) ; D51–D81 au fil des messages de commit et de `docs/JOURNAL_TRAVAIL.md` (Entrées 40–70) — formalisation dans DECISIONS.md différée au prochain passage |
| Feuille de route | Terminée | Jalons M0 à M7 dans `docs/PLAN_MILESTONES.md`, critères de sortie mesurables |
| Format de la Carte | Spécifié | `docs/FORMAT_CARTE.md` — en-tête normalisé, quatre fragments, verrou croisé, export de continuité, re-cryptage |
| Démonstration RoomEq | Livrée | `docs/Protocole_TRIADE_v0.3_Demonstration_RoomEq.pdf` (22 p.) — le protocole v0.3 démontré par le recodage complet de RoomEq (42 modules, 437 tests, parité v2.2.2), avec comparatifs de code avant/après ; dépôt `../roomeq` cristallisé depuis au tag `v3.0.2` (v3.0.0 → v3.0.2 : deux échecs de CI honorés puis corrigés, release GitHub publiée) |
| Article de recherche v0.4 | Livré | `docs/Protocole_TRIADE_v0.4_Article_Recherche.pdf` (12 p.) — édition académique du protocole (D18) : restructuration IMRAD, formalisation (verrou croisé κ, ordre lexicographique ≻_lex, règles en transitions), travaux connexes (dette technique, DbC, AISE), étude de cas avec RQ et design déclaré, menaces sur la validité (Wohlin) dont l'écart source/natif ; rapport de vérification interne : `docs/VERIFICATION_v0.4_Article.md` |
| Implémentation | **M3 clos — balise finale 0.4.0 (D74)** | `m0/` validé terrain (D26) ; `m1/` clos à la balise finale `0.2.0` (D32) ; `m2/` clos à la balise finale `0.3.0` (D43) ; `m3/` : **balise finale `0.4.0` scellée (D74)** — proxy.exe inchangé (md5 dd12b649…, D63), campagne million D72 (10^6 cas SANS CRASH, harnais falsifiable), suite de conformité § 8.2 D73 (161 contrôles VERTE, fuzzing 10^4 cas/exécution), cristallisation 38/38 × 10/10, scellage rc.1 → 0.4.0 sur validation terrain consignée (T2 6×, D64-D71) ; lignée de clés régénérée D74 (4e réinitialisation, D27/D30, preuve byte-identique) ; **carte m3 re-scellée D80 sous la lignée D80 — enveloppe neuve, faits inchangés, même cle publique** (rotation de lignée après exposition D76-D78) ; `terrain/` : superviseur.exe terrain.16 — T3 DÉMONTRÉ sur machine réelle (D71), T1 = D57 en attente WER ; **M4 ouvert (D77)** : couche I écrite-avant-code (`m4/I/` — domaine `tls` : 8 spécifications [nom UTF-16, table des verdicts SSPI, jetons, poignée de main, handles, émission, réception, session] + révisions http-08:R2/http-10:R2, charte des contrats cryptographiques : fail-closed intégral, certificat invalide = échec nommé 502 propre, zéro divulgation, compensation exacte) ; étape (b) en cours : D79 layout .text3 + tls-01..03 prouvées (165 k cas zéro écart) ; D82 cadre de session TLS + IAT secur32 arrêtés, tls-05 (premier bloc à shims) prouvée — 21 PASS × 2 graines, 5 000 cas fuzzés zéro écart, falsification 6/6 ; **D83 : tls-04 LA POIGNÉE DE MAIN (LE critère M4) notée-mesurée-prouvée — 544 o, boucle ISC bornée 16 allers, 16 scénarios cadre octet par octet + contrat d'appels complet, 10 000 cas fuzzés zéro écart (2 graines), 6/6 mutations** ; D88 : tls-06 ÉMISSION notée-prouvée (491 o, 34 PASS × 2 graines) ; **D89 : convention du cadre AMENDÉE (zone réception 2 × MAX_JETON → TAILLE_CADRE 0xC260, champs de géométrie +0x3A/+0x3C) puis tls-07 RÉCEPTION notée-mesurée-prouvée — 394 o, 16 scénarios EN CHAÎNES, 10 000 cas + 2 000 chaînes fuzzés zéro écart (2 graines), 10/10 mutations** ; **D90 : tls-08 LA SESSION (l'orchestrateur) notée-mesurée-prouvée — la session complète existe en octets : 740 o, conventions D90 (paquet de session PAQUET_*, VERDICT_CIBLE 7, fixtures console 0x2C60/0x2C80), DRAIN du résidu, reprise en tête, garde chambre, compensation INTÉGRALE par comptage ; harnais à 18 BLOCS RÉELS intégrés (M0→M4) — 20 scénarios, 12 mutations, 53 PASS / 0 ÉCHEC × 2 graines** — reste (b) : révisions http-08:R2/http-10:R2, oracle SSPI, carte génération 6, proxy.exe 0.5.0-dev.1 |
| Infrastructure | Opérationnelle | Dépôt git local + sauvegarde Google Drive + miroir GitHub privé + synchro systématique ; coffre-fort des phrases maîtresses (D75) — conteneur chiffré TRIADE-CF1 au racine du Drive + copie développeur, **roté D80 avec les DEUX lignées (D74 archive + D80 courante)** ; phrase de contrôle sous garde durable D81 (`PHRASE-CONTROLE-COFFRE.txt` dépôt + racine Drive + miroir — le fichier est la remise, restauration post-panne prouvée) ; racine du coffre Drive nettoyée (D76 : livrables périmés archivés dans ARCHIVE/, courants seuls) |

Aucune chaîne de build extérieure : les octets viennent de la notation. Le projet a
franchi son jalon existentiel — la phase de réalisation se poursuit avec M4 (M0/M1/M2/M3
clos et scellés : 0.2.0, 0.3.0, 0.4.0 ; T3 terrain démontré).

## Nouveautés de la v0.3

Trois évolutions demandées par le développeur, consignées en D14–D16 :

1. **Universalité totale** (D14) : le protocole ne dépend plus d'aucune plateforme. Chaque
cible est un profil — ISA, ABI, format d'exécutable, interface système, patch à chaud,
notation, padding — défini par sept éléments vérifiables. La couche I s'écrit une fois, la
carte indexe par profil, chaque profil a son binaire. Validation par jalons : M6
(Linux x86-64 — portabilité inter-OS) et M7 (RISC-V 64 — portabilité inter-ISA).
2. **Cryptographie paramétrable** (D15) : SHA-256 reste le hachage par défaut, mais le
   développeur peut changer d'algorithme — hachage, signature, chiffrement — dans des
listes blanches garantissant le seuil de sécurité. Le choix est consigné dans l'en-tête
signé de la carte, les empreintes sont préfixées (`sha256:…`), et changer en cours de
projet est une migration atomique et journalisée (re-cryptage).
3. **Export de continuité** (D16) : le développeur peut sauvegarder et transférer
l'intégralité de son état de développement — couches I, B, C et manifeste autodescriptif —
sous forme d'un conteneur chiffré et signé, afin de reprendre le projet avec n'importe
quel agent conforme TRIADE. Procédure d'import en cinq étapes ; l'oracle, éphémère, est
régénéré à l'arrivée et jamais exporté.

## 3. Où tout se trouve

### 3.1 Les trois copies du projet

| Emplacement | Rôle | Contenu |
|---|---|---|
| `/home/z/my-project/triade` | Source de vérité | Dépôt git complet (fichiers + historique) |
| Google Drive, dossier « Triade » | Sauvegarde + livraison | Sous-dossier `TRIADE/` (miroir des fichiers) + `TRIADE/triade-history.bundle` (historique git complet) + à la racine (NETTOYÉE D76 — courants seuls ; ONZE entrées depuis D81) : les deux fichiers d'instruction, **la phrase de contrôle du coffre-fort** (`PHRASE-CONTROLE-COFFRE.txt` + son LISEZMOI — D81, garde durable, ouvre le conteneur), le **coffre-fort chiffré des phrases maîtresses** (`coffre_fort.bin`, D75 — roté D80, porte les lignées D74 [archive] + D80 [courante] ; indéchiffrable sans la phrase de contrôle), le livrable `demo.exe` + son LISEZMOI à jour (T1 / enquête D57 — WER), et le dossier « test » du terrain (superviseur-terrain16.exe + LISEZMOI-terrain16.txt + `terrain_jetons.bin` [annexe D48 — secret, hors dépôt] + journaux `terrain_*.txt` téléversés par le superviseur) ; le sous-dossier `ARCHIVE/` (créé D76) reçoit les livrables périmés — douze éléments + LISEZMOI-ARCHIVE.txt, jamais supprimés, via `scripts/drive_archiver.py` ; les courants proxy/superviseur vivent au miroir (`TRIADE/m3/proxy.exe`) et dans le kit embarqué du superviseur terrain.16 |
| GitHub `alexisfrlopez-debug/triade` | Miroir distant | Repo privé, poussé à chaque sauvegarde |

### 3.2 Arborescence du dépôt

```
triade/
├── README.md                          Carte d'identité du dépôt
├── REPRISE_PROJET.md                  Ce fichier — reprise rapide
├── PROTOCOLE_TRIADE_AGENT.md          Manuel d'utilisation pour un agent IA (nouveau projet)
├── coffre_fort.py                     Coffre-fort des phrases maîtresses par projet (D75) — conteneur TRIADE-CF1 chiffré, autotest de falsification ; le conteneur .keys/coffre_fort.bin n'est JAMAIS committé
├── LISEZMOI-ARCHIVE.txt               Sommaire du dossier ARCHIVE/ du coffre Drive (D76) — pourquoi chaque livrable périmé y vit, où vit le courant
├── PHRASE-CONTROLE-COFFRE.txt         Phrase de contrôle du coffre-fort, seule sur une ligne (D81 — garde durable : commit AVANT TOUT, GitHub + miroir + racine Drive ; le fichier EST la remise ; lisible par coffre_fort.py --phrase-fichier)
├── LISEZMOI-PHRASE-CONTROLE.txt       Pourquoi la phrase vit au dépôt (consigne développeur D81), usage, restauration post-panne, avertissement exposition + mitigations
├── docs/
│   ├── PROTOCOLE_TRIADE.md            Spécification v0.5.2 — source de travail (archives formelles v0.2 à v0.5.2 dans docs/)
│   ├── Protocole_TRIADE_v0.4.0_Specification.pdf   Spécification v0.4.0 — archive formelle (LaTeX/Tectonic, D25)
│   ├── VERIFICATION_v0.4.0.md         Rapport de vérification interne de la v0.4.0 (64 contrôles PASS)
│   ├── Protocole_TRIADE_v0.3_Specification.pdf   Spécification v0.3 — archive conservée (27 p.)
│   ├── Protocole_TRIADE_v0.3_Demonstration_RoomEq.pdf   Démonstration v0.3 — étude de cas RoomEq (22 p.)
│   ├── Protocole_TRIADE_v0.4_Article_Recherche.pdf   Édition académique v0.4 — article de recherche IMRAD (12 p.)
│   ├── VERIFICATION_v0.4_Article.md   Rapport de vérification interne de l'article (avant empaquetage)
│   ├── Protocole_TRIADE_v0.2_Specification.pdf   Spécification v0.2 — archive formelle (erratum : numérotation corrigée)
│   ├── FORMAT_CARTE.md                Format détaillé de la Carte (couche C) — à jour v0.4.0
│   ├── DECISIONS.md                   Journal des décisions D1–D26
│   └── PLAN_MILESTONES.md             Feuille de route M0–M7 — à jour v0.4.0 (conditions transverses)
├── scripts/
│   ├── sync_backup.sh                 Sauvegarde complète : PDF à jour + commit + Drive + GitHub
│   ├── build_pdf.sh                   Régénération systématique du PDF formel (D17/D25 — chaîne LaTeX/Tectonic v0.5.1)
│   ├── drive_sync.py                  Synchronisation Google Drive (fichiers + bundle)
│   ├── drive_livraison.py             Livraison terrain au coffre racine Drive (idempotente, vérifiée ; --dossier-test = dossier « test » du développeur)
│   ├── drive_recuperer.py             Rapatrie les fichiers du dossier Drive « test » vers upload/ (constats terrain)
│   ├── check_auth.py                  Vérification des jetons d'accès
│   ├── spec_v051/                     Sources de la spécification v0.5.1 (LaTeX/Tectonic — née spec_v040 → spec_v050, D25/D44/D75)
│   │   ├── main.tex + sec-a…d.tex     Corps monocolonne avec sommaire (5 fichiers)
│   │   ├── cover.html                 Couverture (Template 03, validée)
│   │   ├── merge_cover.py             Fusion couverture + corps, normalisation A4, métadonnées
│   │   └── verify_spec.py             Contrôles mécaniques pré-empaquetage (cahier V1–V11)
│   ├── triade_v03_spec.py             Générateur du PDF v0.3 (ReportLab — archive, remplacé par la chaîne v0.4.0)
│   ├── triade_v03_cover.html          Source HTML de la couverture v0.3
│   ├── triade_v03_demo_roomeq.py      Générateur du PDF de démonstration RoomEq (édition, régénération manuelle)
│   ├── triade_v03_demo_cover.html     Source HTML de la couverture de la démonstration
│   ├── article_v04/                   Sources de l'article v0.4 (LaTeX/Tectonic, D18 — régénération manuelle)
│   │   ├── main.tex + sec-*.tex + refs.bib   Corps IMRAD (8 fichiers) et bibliographie (29 réf.)
│   │   ├── cover.html                 Couverture académique (Template 03, validée)
│   │   ├── merge_cover.py             Fusion couverture + corps, normalisation A4, métadonnées
│   │   └── verify_article.py          Contrôles programmatiques pré-empaquetage (44 contrôles)
│   ├── triade_v02_spec.py             Générateur du PDF v0.2 (erratum appliqué)
│   ├── triade_cover.html              Source HTML de la couverture v0.2
│   ├── triade_diagram_arch.html       Source HTML du diagramme d'architecture
│   ├── triade_diagram_loop.html       Source HTML du diagramme de la boucle de mise à jour
│   └── assets/                        Images référencées par la spécification
├── m0/                                 Jalon M0 (franchi) — chaîne artefact : I + notation + éditeur PE32+ + carte v0 + hello.exe
├── m1/                                 Jalon M1 (franchi — balise finale 0.2.0) — mini-libc + autotest + carte projet + conformité + budgets + export
│   ├── README.md                       Carte d'identité du jalon (résultats, validation terrain)
│   ├── I/ · notation/ · layout.py      8 specs libc, notation x86-64, plan d'adressage D28
│   ├── build_m1.py                     Chaîne : assemblage, oracles, PE32+, carte, verrou croisé
│   ├── oracle_differentiel.py          Oracle éphémère (D1) sur Unicorn (D29)
│   ├── conformite_profil.py            Suite de conformité profil § 8.2 (68 contrôles)
│   ├── budgets_tokens.py               Instrumentation des budgets (D31) → budgets.json
│   ├── demo_r7.py                      Démonstration des adresses stables (R7)
│   ├── export_continuite.py            Export de continuité chiffré + signé (D16)
│   └── selftest.exe · carte/           Artefact 9 216 o + carte projet multi-artefacts
├── m2/                                 Jalon M2 (clos — balise finale 0.3.0, D43) — serveur echo + patch à chaud + rollback + echo.exe
├── m3/                                 Jalon M3 (clos — balise finale 0.4.0, D74) — parseur HTTP + proxy : I (13 specs D46), notations, oracle 153 036 cas, conformité 161/161, campagne million D72, proxy.exe 0.4.0 (md5 dd12b649…)
├── m4/                                 Jalon M4 (ouvert D77) — tunnel chiffré Schannel : couche I écrite-avant-code (m4/I/ — 8 spécifications tls + révisions http-08:R2/http-10:R2, charte des contrats cryptographiques) ; étape (b) ENGAGÉE (D79) : layout.py (plan .text3 0x6000 + liste blanche HRESULT vérifiée + ISC_REQUETES D83), outils/auteur.py (IAT_ISC D83), notation/ tls-01..03 (feuilles pures mesurées 89/156/284 o), harnais_feuilles.py (V1-V4 : différentiel de spécification 165 k cas sans écart, 6/6 mutations attrapées) ; D81-D82 : tls-05-cles (5 bloc à shims, 251 o) + harnais_cles.py ; D83 : tls-04-poignee (544 o — LE critère M4, boucle ISC) + harnais_poignee.py (16 scénarios + fuzz 2×5 000 + 6/6 mutations)
├── demo/                               Lignée démo GUI (finale 0.3.0-demo.9, D43) — coquille win éprouvée terrain D36-D43 + journaux terrain archivés
├── m6/ · m7/                           Échelle d'auto-hébergement D34 — hachoir SHA-256, sceau SHA-512/Ed25519 (emprunts de nommage, hors plan M6/M7 nominal)
├── terrain/                            Lignée terrain (D48) — superviseur.exe : TOUS les tests en 1 clic (T1 démo, T2 proxy, T3 envoi Drive) + journal auto-téléversé
│   ├── I/ · notation/ · layout.py      11 specs sup écrites-avant-code + notations + plan d'adressage (génération 5, blocs f6xxxx)
│   ├── build_terrain.py · oracle_terrain.py · carte_terrain.py   Chaîne : 22 blocs → superviseur.exe + oracle (807 verrous, 10 080 cas) + carte
│   └── superviseur.exe · carte/        Artefact 20 992 o WINDOWS_GUI (0.5.0-terrain.1) + carte génération 5
├── git-hooks/
│   └── post-commit                    Hook : synchro Drive après chaque commit
└── .gdrive/                           Jetons d'accès — LOCAUX, jamais commités (voir § 8)
```

## 4. Restaurer le projet depuis cette sauvegarde

### 4.1 Méthode A — depuis le bundle git (recommandée, conserve l'historique)

1. Télécharger `TRIADE/triade-history.bundle` depuis le dossier Drive « Triade ».
2. `git clone triade-history.bundle triade && cd triade`
3. Recopier les jetons d'accès dans `triade/.gdrive/` (voir 4.3).
4. `bash scripts/sync_backup.sh "reprise du projet"` — réinstalle le hook post-commit,
   resynchronise le Drive et pousse vers GitHub si la remote est configurée.
5. Phrases maîtresses (D75/D81) : télécharger `coffre_fort.bin` ET
   `PHRASE-CONTROLE-COFFRE.txt` au racine du Drive (tous deux AUSSI dans le dépôt
   git et le miroir TRIADE/) puis `python3 coffre_fort.py importer coffre_fort.bin`
   et `python3 coffre_fort.py obtenir TRIADE lignee-D80 --vers-fichier
   .keys/passphrase.txt --phrase-fichier PHRASE-CONTROLE-COFFRE.txt` — la lignée
   redevient opérationnelle sans cérémonie (la phrase de contrôle vit au dépôt,
   D81 : le fichier est la remise) ; vérifier avec
   `python3 m3/build_m3.py --verifier --graine 1`.

### 4.2 Méthode B — copie directe des fichiers

1. Télécharger le contenu du sous-dossier `TRIADE/` du Drive.
2. `git init -b main && git add -A && git commit -m "restauration depuis le Drive"`
   (l'historique repart de zéro — préférer la méthode A quand elle est possible).

### 4.3 Jetons d'accès

Les jetons (OAuth Google Drive, GitHub, compte de service) vivent dans `triade/.gdrive/`
avec des permissions 600. Ils ne sont **jamais** commités ni synchronisés. Sur un poste
neuf, les récupérer depuis le dossier Drive « Triade » → sous-dossier « Tokens », ou les
régénérer, puis valider avec `python3 scripts/check_auth.py`.

## 5. Règle absolue : sauvegarde systématique

**Après chaque modification du projet, sans exception :**

```bash
cd /home/z/my-project/triade && bash scripts/sync_backup.sh "description courte de la modification"
```

Ce script exécute, dans l'ordre : régénération du PDF formel si les sources du protocole
ont changé (D17 — `scripts/build_pdf.sh`, empreinte SHA-256 des sources comparée au stamp
du dernier build), commit git (message passé en argument, sinon horodatage
automatique), synchro Google Drive (miroir des fichiers + régénération du bundle
d'historique + copie des fichiers d'instruction à la racine du Drive), puis push GitHub si
la remote `origin` est configurée. Le hook `post-commit` déclenche en outre une synchro Drive
à chaque commit, même manuel. Un agent IA travaillant sur ce projet DOIT exécuter cette
commande à chaque modification — c'est une exigence du protocole d'infrastructure,
consignée en D13 et D17 dans `docs/DECISIONS.md` et rappelée au § 11 du manuel agent.

## 6. Décisions structurantes — résumé

Le journal complet, avec alternatives rejetées et justifications, est dans `docs/DECISIONS.md`.

| ID | Décision | Choix retenu |
|---|---|---|
| D1 | Oracle de vérification | Éphémère et obligatoire : régénéré à chaque session depuis I, détruit après usage |
| D2 | Notation | keystone (assemblage) + capstone (round-trip), in-process ; nasm en repli |
| D3 | Couche I | Contrats légers : signatures typées, pré/post-conditions, invariants |
| D4 | Crypto de la carte | Ed25519 + XChaCha20-Poly1305 + Argon2id |
| D5 | Verrou croisé | SHA-256 par bloc scellé + carte signée en entier |
| D6 | Empreintes par build | Variante unique par livraison (réordonnancement, nops, encodages) |
| D7 | Appels système | API Windows via IAT (kernel32, ws2_32, Schannel) — pas de syscalls directs |
| D8 | Granularité des blocs | 32 à 512 instructions, un bloc = une responsabilité, padding 16 octets |
| D9 | TLS | Schannel (SSPI) au jalon M4 ; TLS 1.3 pur reporté après M7 |
| D10 | Cible | x86-64, Windows 11, PE32+ à la main, DEP/ASLR/CFG — profil primaire (amendée par D14) |
| D11 | Architecture de sauvegarde | Git local (vérité) + Drive (miroir fichiers + bundle) + GitHub privé |
| D12 | Gestion des jetons | `.gdrive/` local, chmod 600, jamais commités ni synchronisés |
| D13 | Sauvegarde systématique | `sync_backup.sh` après chaque modification + hook post-commit |
| D14 | Universalité | Profils de cible à sept éléments vérifiables ; Win11 x86-64 reste le profil primaire de validation |
| D15 | Suite cryptographique | Paramétrable (hachage SHA-256 par défaut, signature, chiffrement) — listes blanches, en-tête signé, re-cryptage atomique |
| D16 | Récupération de la carte | Export de continuité chiffré et signé (I+B+C+manifeste), import en cinq étapes, oracle jamais exporté |
| D17 | PDF formel | Régénération systématique : `build_pdf.sh` compare l'empreinte des sources au stamp du dernier build et reconstruit avant chaque commit |
| D18 | Édition académique v0.4 | Article de recherche IMRAD (12 p.) : formalisation, travaux connexes, menaces sur la validité ; noyau normatif v0.3 inchangé, régénération manuelle (`scripts/article_v04/`) |
| D19 | Invariants de révision | La hiérarchie Sécurité > Performance > Optimisation > Coût en tokens devient invariant : aucune révision ne peut la modifier sans invalider explicitement le protocole |
| D20 | Couche I normalisée | Gabarit de spécification (identifiants stables, cas d'échec, vecteurs dorés, fixtures, provenance) + taxonomie T1–T6 des défauts de contrat non écrit |
| D21 | R11 — optimisation mesurée | Hot path identifié par mesure + mesures avant/après au journal d'optimisation + contrat stable ; l'optimisation prématurée est interdite (sanction : refus de commit) |
| D22 | Conformité par profil | Suite de conformité exécutable par profil (§ 8.2) + parité inter-profils vérifiée par exécution (§ 8.3) — critères d'acceptation explicites de M6/M7 |
| D23 | Pratiques officialisées | Reverse-specs (statut prête/validée), pré-versions dev.N/rc.N/X.Y.Z (balises immuables, monotonie anti-rollback), fixtures contractuelles à copie unique référencée (défaut T5 sinon) |
| D24 | Traçabilité et gouvernance | Table I↔C↔B↔tests obligatoire (champ `spec=`, refus de build si maillon manquant), journal des décisions normalisé (append-only, pas de rétrodatage), tableau de bord de conformité (11 métriques) ; norme de fragmentation et localisation par intention consolidées |
| D25 | PDF formel v0.4.0 | Chaîne LaTeX/Tectonic (`scripts/spec_v040/`) remplace le générateur ReportLab v0.3 ; archives v0.2/v0.3 conservées, non régénérées |
| D26 | Jalon M0 (amendée) | Chaîne artefact implémentée dans `m0/` (I gabarit 2.2, notation keystone layout fixe, éditeur PE32+ à la main, oracle round-trip + 31 verrous, carte v0 signée, verrou croisé fail-closed) ; **validée sur le terrain le 26/10/2026 — M0 franchi** (hello.exe 1 536 o exécuté sur Windows 11, sortie exacte du contrat) |
| D27 | Continuité des clés | Régénération + centralisation dans `triade/.keys/` après réinitialisation du bac à sable ; la carte se reconstruit depuis I + notation, preuve par artefact byte-identique |
| D28 | Plan d'adressage M1 | Zones io/libc/app (R7), carte projet multi-artefacts (11 blocs, 2 exécutables), mini-libc, structures PE héritées aux RVA exactes |
| D29 | Substrat d'oracle | Unicorn (émulation x86-64) : oracle différentiel local, shims IAT, falsification systématique — le terrain reste la preuve d'environnement |
| D30 | Troisième réinitialisation | D27 réappliquée : rebuilds byte-identiques hello.exe/selftest.exe, lignée régénérée ; premier export de continuité généré (le coffre préserve désormais la lignée scellée) |
| D31 | Budget localiser amendé | Mesure M1 (cl100k_base) : le gabarit canonique v0.4.0 mesurait déjà 43 tokens — budget 40 → 64 et format frag-loc allégé (51 tok mesurés) ; éditer 719/3 000, ajouter 1 086/6 000 |
| D32 | Jalon M1 franchi | Validation terrain Windows 11 constatée (ligne unique `21/21 OK`, contrat libc-08 Q2) → balise finale `0.2.0` immuable ; anti-rollback étendu aux balises finales ; erratum documentation (« ligne unique », pas « 21 lignes ») |

## 7. Étapes de réalisation — M0 à M3 clos, M4 en cours (tunnel chiffré)

### 7.1 Jalons M0 et M1 — procès-verbaux

**M0 franchi le 26 octobre 2026** (D26 et son amendement). La chaîne existentielle
notation → octets → PE32+ → exécution est prouvée de bout en bout **sans
compilateur** : round-trip 100 %, 31 verrous, `hello.exe` 1 536 o déterministe,
carte v0 signée, exécution constatée sur Windows 11. Détail : `m0/README.md`.

**M1 franchi le 26 octobre 2026** (scellage `0.2.0-rc.1` après dev.1, dev.2 et la
session de cristallisation — D27-D31 ; puis **D32**). Les quatre critères de sortie
étaient acquis au scellage rc.1 :

1. **Oracle à 100 %** : 76 010 cas différentiels verts par exécution (Unicorn,
   D29 — entrées contraintes par les pré-conditions, référence dérivée de I,
   falsification 10/10) + 134 verrous structurels + émulation du binaire entier
   (sortie exacte, code 0) ; ~1,2 M cas cumulés sur la lignée (graines 3-16).
2. **Première cristallisation (R6)** : 11/11 blocs à 10/10 — immuables.
3. **Adresses stables démontrées (R7)** : `demo_r7.py` — memset entré en dev.2
   exclusivement dans la réserve int3, aucun octet scellé déplacé, blocs io
   octet-identiques à `hello.exe` dans les deux artefacts.
4. **Première mesure effective des budgets (D31)** : localiser 51 (cible 64),
   éditer 719 (cible 3 000), ajouter 1 088 (cible 6 000) — `budgets_tokens.py`,
   re-mesurés au scellage final.

**Validation terrain (D32) : PASS.** `selftest.exe` exécuté sur la machine
Windows 11 du développeur (`C:\Users\Alek\Downloads>selftest.exe`) : la ligne
unique `TRIADE M1 : minilibc 21/21 OK` s'affiche à l'identique du contrat
libc-08 Q2 (vecteur doré V2), retour au prompt sans incident ; le code de sortie 0
(post-condition Q3) est reconfirmé par l'oracle après scellage (graines 15-16 :
76 010 cas verts, sortie exacte, code 0). Erratum consigné : la procédure de
validation annonçait « 21 lignes » — le contrat exige une ligne unique, l'artefact
fait foi (D32). La **balise finale `0.2.0`** est scellée par
`build_m1.py --sceller-final` (cristallisation 10/10 + conformité 68/68
re-exécutées, manifeste frag-bld basculé, carte re-signée) — immuable (§ 9), tout
défaut ultérieur se corrige en `0.2.1` à contrat stable (R4).

Suite de conformité du profil (§ 8.2, D22) : **verte, 68/68 contrôles** (éléments
1-4 et 6-7 ; l'élément 5 — patch à chaud — est le jalon M2). Détail complet :
`m1/README.md` (procès-verbal inclus). La continuité ne dépend plus du poste :
l'export de continuité chiffré et signé (D16, lignée 0.2.0) est conservé au
dossier `ARCHIVE/` du coffre Drive (D76) ; la voie de reprise courante est le
bundle git complet (`TRIADE/triade-history.bundle`, méthode A).

### 7.2 M2 : patch à chaud (le jalon de vérité)

Serveur TCP écho, thread par connexion, journal console ; patch du bloc écho
**pendant l'exécution** (trampoline 12-16 o, bascule atomique), sans interruption,
rollback démontré. La boucle de mise à jour complète (§ 5) s'exécute pour la
première fois sur du code vivant. Règles au premier plan : R4 (contrat stable),
R7 (points d'entrée seuls trampolinables), R10 (fail-closed au chargement) ;
l'élément 5 de la suite de conformité passe au vert avec M2. Critères de sortie :
patch sans interruption de service, rollback démontré, boucle complète — et les
conditions transverses (§ 16 : oracle vert, conformité, tableau de bord, carte
signée, journal à jour). Premier chantier : spécifications I des nouveaux blocs
(réseau ws2_32, threads, trampoline) écrites **avant** la notation (R1-R3), plan
d'adressage étendu aux zones réseau/thread dans la continuité de D28.

**État M2 (clos au 27/10/2026, journal 32 / D43)** : **le jalon M2 est clos à
la balise finale `0.3.0`** — la boucle § 5 (patch à chaud EN PRODUCTION pendan
le trafic + retour arrière) est **démontrée sur machine réelle** : le journal
terrain demo.8 (28/28 lignes, md5 84f5d58e…) se termine par « boucle § 5
complète - DÉMO OK », sondes vertes des deux côtés de la socket (S1/S2 serveur
lus après « client : connecté » — course bénigne documentée ; sonde4/5 autour
de chacun des trois échanges identité → MAJUSCULES → retour arrière). La
cascade terrain aura nommé et corrigé **8 classes de défauts en 8 lectures de
journal** (D36 RECT, D37 jumeau silencieux, D38 volatiles, D39 DEP, D40
méthodologie des sondes, D41 zone d'accueil ABI, D41 POSE, D42 section
critique héritée jamais initialisée — chaque correction byte-exact, chaque
régression impossible : falsifications V4-V9 + audits trackés).
**demo.9** (D43, md5 73c064fb…, u64 0x00030109) est la **finale de lignée** :
TOUTES les sondes retirées (win-08:R3/win-09:R4/win-10:R3 — 140 o de code,
7 chaînes retournées au zéro des zones libres, diff demo.8→demo.9 chirurgical
1 047 o, zéro hors zone ; le correctif D42 [init R_CS en tête de scénario]
reste VIVANT), oracle 86 cas verts + journal nominal de 11 lignes exactes
(l'anti-régression du retrait), audit `scripts/audit_demo9.py` TOUT CONFORME,
héritage R7 intact (16 blocs + staging octet-identiques). Le **scellage final
0.3.0** est une opération de carte (modèle M1 0.2.0) : conformité 124/124
ré-exécutée VERTE, balise rc.4→0.3.0, fragments re-chiffrés et re-signés
Ed25519, immuable § 9 (défaut → 0.3.1 à contrat stable). Journal terrain
final attendu si relecture : 17 lignes (6 de démarrage + 11 de preuve).
Détail complet : `docs/JOURNAL_TRAVAIL.md` (journaux 22 à 32), décisions
D36-D43 dans `docs/DECISIONS.md`, archives terrain
`demo/journal_terrain_demo*.txt`.

**État M3 (ouvert au 27/10/2026, journal 34 / D45)** : le jalon des entrées
non fiables est ouvert par la MÉTHODE avant les blocs — le harnais de fuzzing
à propriétés (`m3/fuzz.py`, tracké) est livré et calibré : cinq propriétés
dérivées des contrats (P1 survie, P2 terminaison, P3 différentiel, P4
fermeture unique, P5 mémoire par crochet d'écriture Unicorn), six générateurs
nommés, rejeu sur état vierge de tout échec, graines reproductibles.
**Campagne d'ouverture : 101 000 cas SANS CRASH** sur la surface d'entrées
non fiables déjà scellée (tcp-09 session serveur, win-10 échange client) —
zéro violation confirmée ; le harnais est FALSIFIABLE (auto-test : deux
défauts d'un octet injectés, détectés 122/300 et 300/300). Leçon de
calibration consignée : les premières divergences étaient dans le modèle du
harnais (cap recv, sémantique du retour 0), pas dans le bloc — miroir de la
classe X6. **Étape (a) accomplie (D46, journal 35) : la couche I de M3 est
écrite avant le code** — treize spécifications écrites-avant-code du domaine
http (http-01 à http-12, domaine créé réservé M3) et de l'extension cliente
tcp-13 (getaddrinfo + connect sur cible arbitraire — win-07 démo était soudé
à 127.0.0.1:25000) : huit parseurs FEUILLES PURES (itérateur CRLF
[propriétaire T5], ligne de requête [la table des huit méthodes EST la
validation], ligne d'en-tête, recherche d'en-tête [l'unique comparaison
insensible à la casse du domaine], décimal borné [test de borne à chaque
chiffre, zéros de tête rejetés], fin de tête [MAX_TETE = 8192, LF isolé →
400], autorité [propriétaire T5 du découpage hôte:port], cible
[formes absolue/origine/autorité]), une pompe (ne ferme JAMAIS), la session
(unique propriétaire des fermetures et de la table des réponses
400/411/431/501/502/505/200-tunnel), la console (quit) et l'orchestrateur
(porte R10 plancher 0x00040000, ordre d'initialisation D42 en invariant) ;
charte des contrats renforcés liée par renvoi (m3/I/README.md) : spans
partout, verdicts eax nommés, constantes à propriétaire unique, CRLF
strict, schéma minuscule strict, une requête par connexion, réponse jamais
parsée, échec avant l'entrée système ; réutilisation R7 préfigurée
(tcp-01..06/11 + libc + io aux RVA exacts, IAT inchangée + getaddrinfo/
freeaddrinfo appendus 0x2350/0x2358, tcp-13 au trou libre net 0x4200, zone
http depuis 0x4C00, http-12 au slot d'application 0x1800) ; surface de
fuzzing délimitée par contrat (http-01..09 + accumulation http-10 — le
périmètre du million). **Étape (b) accomplie (D47, journal 36) :
proxy.exe 0.4.0-dev.1 est scellé** — le plan d'adressage est arrêté sur
les mesures réelles des notations (http-02 424 o, http-10 1 746 o,
tcp-13 402 o — la préfiguration D46 sous-estimait ; zone http depuis
0x4C00, tcp-13 0x4400-0x45BF, http-12 au slot d'application 0x1800,
IAT + getaddrinfo/freeaddrinfo/connect) ; treize brouillons écrits à la
main puis résolus par outils/auteur.py (round-trip capstone 100 %,
26 blocs embarqués) ; oracle à scénarios (structurel 523 verrous,
différentiel 153 036 cas verts, falsification détectée — le crash EST
une détection) ; réutilisation R7 prouvée : 13 blocs octet-identiques
aux artefacts scellés M0/M1/M2 ; carte génération 5 (38 blocs indexés
sur 4 artefacts — hello.exe, selftest.exe, echo.exe, proxy.exe),
verrou croisé 38 empreintes ; 19 456 octets, entrée 0x1800 (http-12 :
porte R10, bannière « TRIADE M3 : proxy demarre (port 25000) »,
console « quit », codes 0/1/2) ; sha256 85d2aa21c1532a50… Deux
révisions de spécification nées de l'implémentation : http-06:R2 (le
trou du succès excessif — une tête AVEC terminateur au-delà de 8192
était un succès : contournement 431 + débordement du tampon de
réécriture ; Q1 bornée, Q3 étendue) et http-10:R2 (corps de requête
relayé par boucles tcp-03/tcp-04 INLINE bornées Content-Length —
http-09 s'arrêterait à l'EOF du client qui attend la réponse :
interblocage ; pompe détachée (amont<<32)|cliente, CloseHandle IAT,
assistants internes I5) ; un défaut de notation attrapé par le
différentiel au premier build : http-08 (deux-points en position 0
sans « // » → verdict 1, pas 3 — le modèle suit la spécification,
jamais l'inverse).

**Étape (c) validée terrain — SIX FOIS (D64–D71)** : T2 du superviseur (proxy.exe
traversé par curl — http 640 o + https tunnel 577 o, console 7 lignes conformes,
exit 0) est vert à chaque run complet depuis D64. Le passage à **proxy.exe
0.4.0-dev.2** (D63 : pile probing http-10:R3 écrite à la main — `sub rsp,0x7100`
sans probing tuait au commit 0x1000 ; oracle 153 036 cas verts, md5 dd12b649…)
avait fait basculer T2 au vert historique (D64, run 22:10) après le correctif ABI
du superviseur (D62 : sup-34 .curl appelait l'IAT sans zone d'accueil — spill
homeparams sur l'adresse de retour, correctif imm8 08→28). T1 élucidé (D64) :
l'échec démo était un artefact de mesure double (journal diagnostique 706 o coupé
à 640 par le lecteur) ; la démo publique 73c064fb n'a jamais réussi sur machine
réelle — D57, exit 0xC0000005, 5e reproduction propre, adresse de plantage
attendue via WER/Observateur d'événements côté développeur.

**Terrain : T3 DÉMONTRÉ de bout en bout (D71, journal 60 — run 16 du 28/10 06:54)** —
la mission fondatrice D48 (« le journal partira TOUT SEUL ») est réalisée sur
machine réelle au bout de 16 générations : S33 jeton OAuth obtenu, S34 session
upload ouverte (la ligne-miroir de la mort terrain.15), dépôt
`terrain_20261028_065408.txt` constaté dans le dossier test (md5 5221e0c2…,
56 lignes finissant à S34 par construction — cliché lu à l'instant du PUT) ;
chaîne de garde fermée (superviseur-terrain16.exe md5 34ee9f58… == LISEZMOI,
S00 terrain16, R10 27/27, kit embarqué 73c064fb/dd12b649 conformes). La chasse
aura traversé seize générations (terrain.1→terrain.16) : ABI shadow space D62,
pile du proxy D63, --fail curl D65 (aucune réponse d'erreur sur disque), preuve
refresh_token vivant depuis le bac + S33 réseau local D66, nettoyage destructeur
du jeton D68 (5→4 DeleteFileA, terrain.14), JSON indenté de Google + location:
minuscules en HTTP/2 D69 (--http1.1 forcé, terrain.15), débordement du tampon de
composition après S33 réussie D70 (TAMPON_COMPO 0x3100 1888 o + PUT quoté,
terrain.16) — chaque tueur nommé, corrigé byte-exact, scellé.

**Étape (d) ACCOMPLIE (D72, journal 61) : la campagne million.** Le critère
quantitatif de sortie de M3 — « un million de requêtes fuzzées sans crash » —
est REMPLI sur le périmètre D46 : harnais `m3/fuzz_million.py` (686 lignes,
tracké, FALSIFIABLE — deux mutations d'un octet du proxy scellé détectées : table
des méthodes @0x16A0, réponse 400 @0x1769 ; témoin sauvage PASS) ; 1 000 000 cas
SANS CRASH en 175,0 s (graine 20261028, proxy md5 dd12b649…) : 900 000
différentiels feuilles http-01..09 (100 000 par parseur, générateurs hostiles à
pleines tailles, frontières 2048/8192, tranches d'émulateur neuf) + 100 000
requêtes complètes http-10 à propriétés P1-P5 (8 générateurs nommés, 200/200
sentinelles canoniques, rejeu sur état vierge de tout échec — zéro) ; re-exécution
à graine neuve 20261029 : même verdict en 176,1 s (2 × 10^6 cas cumulés) ; rapport
`m3/rapport_million.json` tracké (graine, empreintes, répartition, cadences par
cible). Aucune 10e classe de défaut n'a surgi : les parseurs à contrats renforcés
encaissent l'arbitraire exactement comme leurs contrats l'exigent.

**Étape (e) accomplie (D73)** : la suite de conformité du profil (§ 8.2) est
livrée — `m3/conformite_profil.py`, 161 contrôles : éléments 1-7 constatés
depuis proxy.exe (26 blocs, 23 slots IAT, porte R10 vivante, 13 héritages R7
octet-identiques, réserves int3, round-trip 1 372 instructions, oracle
structurel 524 verrous) + contrôle de jalon « fuzzing à propriétés » :
harnais D72 réutilisé intégralement, 10^4 cas SANS CRASH par exécution
(9 000 feuilles + 1 000 accumulation P1-P5), graine datée reproductible,
auto-test de falsification inclus ; suite VERTE (re-exécution à graine neuve
identique, ~2 s tout compris) ; falsifiable — trois mutations d'un octet
détectées (somme R10, machine COFF, octet d'héritage), témoin vert ;
`conformite.txt` (ligne ASCII) lu par le tableau de bord (`suite_conformite_profil`).
La première exécution fut ROUGE sur le scellé vert : quatre contrôles hérités
de m1/m2 décrivaient la norme des blocs mono-entrée/mono-sortie — corrigés sur
citation de la couche I (assistant interne http-07, sondes de pile http-10:R3
en lecture, multi-entrées http-10, constantes movabs http-02:Q4/http-05:Q5).

**M3 est clos (D74) : balise finale 0.4.0 scellée, immuable § 9.** La session
a mené la cristallisation (38/38 × 10/10, 19 vérifications graines 1-19) puis
le scellage 0.4.0-rc.1 → 0.4.0 (conformité 161/161 re-exécutée à chaque
scellage ; validation terrain consignée : T2 du superviseur 6 verts consécutifs
D64-D71 sur les octets dd12b649 inchangés — le scellage est un fait de carte).
La lignée de clés avait été perdue à la réinitialisation qui a précédé la
session D71 (la graine Ed25519, jamais confiée, est irrécupérable) : D74 a
réappliqué D27/D30 — régénération de `triade/.keys/`, reconstruction de la
carte m3 depuis I + notation, **preuve de continuité byte-identique**
(proxy.exe régénéré md5 dd12b649… égal au scellé D63). L'asymétrie R6 de
l'héritage non embarqué (12 blocs à 1/10) a été corrigée au passage au
modèle du journal 18 m2. Garde anti-rollback : toute reconstruction d'une
carte cristallisée est désormais refusée (testée sur 0.4.0).

**État des clés et des enveloppes** (important pour la reprise) : **la lignée
Courante est D80 depuis la rotation D80** — la phrase D74 (exposée ≈ 64 min,
D76-D78) est RETIRÉE du service : elle ne vit plus qu'en coffre-fort (entrée
`lignee-D74`, archive) et dans les cartes m3 de l'historique git. La phrase D80
vit en `.keys/passphrase.txt` (opérationnel) + coffre-fort (entrée `lignee-D80`)
; `.keys/` local perdu = importer le conteneur puis `obtenir TRIADE lignee-D80
--vers-fichier .keys/passphrase.txt` (SANS cérémonie, § 15.3). La carte m3 a été
re-scellée D80 (enveloppe neuve, faits inchangés, même cle publique Ed25519,
proxy.exe inchangé dd12b649…) ; la graine Ed25519 n'a PAS été rotée (jamais
exposée). Les cartes m0/m1/m2/terrain/démo du dépôt restent chiffrées à l'ANCIENNE
lignée (pré-D74) : illisibles avec les phrases courantes — c'est un état
préexistant, sans effet sur M3 (verrou croisé m3 = artefacts + notation) ;
deux relèves possibles : (a) lecture par l'ancienne phrase conservée au coffre
personnel du développeur (D30), (b) cérémonies de reconstruction byte-identiques
au modèle D74 (m0/m1/m2 : construire + 10 vérificateurs + scellage ; terrain :
spécifique).

**Coffre-fort des phrases maîtresses (D75 — ROTÉ D80)** : conteneur chiffré
TRIADE-CF1 (`coffre_fort.py`, racine du dépôt ; conteneur `.keys/coffre_fort.bin`
jamais committé), exporté chiffré au racine du coffre Drive (copie projet) et au coffre
personnel du développeur (copie `download/coffre_fort.bin`). **Le conteneur a été roté
D80** (ré-init + re-scelage des entrées — équivalent conforme de `changer-phrase` +
`ajouter`, modèle D78) : il porte désormais les entrées `lignee-D74` (archive —
déverrouille les cartes m3 de l'historique git antérieures à D80, ne plus sceller avec)
et `lignee-D80` (courante — déverrouille la carte m3 re-scellée et les cartes M4+).
**La phrase de contrôle D75 est INOPÉRANTE depuis D80** : la NOUVELLE phrase de
contrôle (D80) vit SOUS GARDE DURABLE depuis D81 — `PHRASE-CONTROLE-COFFRE.txt`
au racine du dépôt (commit dédié AVANT TOUTE AUTRE ACTION : GitHub + miroir Drive
par le hook) et au racine du coffre Drive, md5 vérifiés ; LE FICHIER EST LA REMISE
(l'affichage unique de cérémonie a cessé d'être le canal de survie — la session
morte de D80 l'a démontré : la phrase était remise à personne) ; restauration
post-panne prouvée (téléchargement Drive → conteneur ouvert). NB D81 : le dossier
Drive étant partagé par lien, la confidentialité au repos repose sur le contrôle
d'accès au dossier — RESTREINDRE le partage par lien est la mitigation première
(décision développeur, arbitrage PERTE > EXPOSITION consigné § 13.1) ; une phrase
commise en git y demeure à vie : on ne compte plus sur sa confidentialité, la
rotation reste le remède. Après une réinitialisation
du poste : importer le conteneur puis `obtenir TRIADE lignee-D80 --vers-fichier
.keys/passphrase.txt` — la phrase est restaurée SANS cérémonie de régénération (la
graine Ed25519 reste régénérable uniquement, D30). À faire côté développeur : le
cas échéant AJOUTER l'ancienne phrase D30 au coffre (`python3 coffre_fort.py ajouter
TRIADE lignee-D30 --description "ancienne lignée D30 — déverrouille les cartes
m0/m1/m2/terrain/démo"`) — elle seule relit les enveloppes anciennes ; le développeur
tient la NOUVELLE phrase de contrôle, il écrit au conteneur directement.
NB D78 (conservé, correctif du NB D76) : le reliquat « phrase maitresse triade.txt »
trouvé sur le miroir Drive portait la phrase COURANTE D74 (preuve croisée : la phrase
extraite est octet-identique à l'ancien `.keys/passphrase.txt`, déchiffre la carte m3
d'avant rotation, échoue sur la carte m2 ; l'audit D76 avait comparé le fichier entier
— étiquette comprise — à la phrase nue, d'où la conclusion erronée « probablement
D30 »). Ce fichier était le dépôt manuel du développeur (09:38:44 UTC, 34 min après
la cérémonie D74) : la phrase ACTIVE a été exposée ≈ 64 min sur le dossier partagé
par lien, puis corbeillée à D76 — d'où la rotation D80. La phrase D30, elle, n'existe
nulle part côté assistant : elle ne peut venir que du coffre personnel du développeur.
Actions développeur : VIDER la corbeille Drive (la copie D74 y vit encore 30 j — la
phrase étant retirée du service depuis D80, l'urgence descend d'un cran, l'hygiène
demeure), et le cas échéant ajouter la phrase D30 au coffre. Chaque future
cérémonie de clés alimente le coffre dans la même
session (discipline § 15.3, FORMAT_CARTE § 11).

**Suite du projet** : M4 — tunnel chiffré (contexte SSPI/Schannel, poignée de
main TLS, relais chiffré ; échec propre sur certificat invalide) — **OUVERT le
28/10 (D77) par sa couche I écrite-avant-code** : `m4/I/` crée le domaine `tls`
(huit spécifications — tls-01 hôte span → UTF-16 [traduction unique, miroir
tcp-13:Q2] ; tls-02 table TOTALE des verdicts SSPI [tout HRESULT classé, le
non-documenté = fatal nommé — fail-closed intégral] ; tls-03 jetons/descripteurs
[propriétaire unique de la mise en page SSPI] ; tls-04 poignée de main cliente
[boucle InitializeSecurityContext bornée 16 allers, jetons ≤ 16 Kio] ; tls-05
cycle de vie des handles [compensation exacte] ; tls-06 émission chiffrée
[tailles négociées, jamais de constantes inventées, clair de l'appelant intact] ;
tls-07 réception déchiffrée [incomplet = état nommé, résidu Extra à propriétaire
unique, close_notify = fin propre] ; tls-08 session TLS cliente [propriétaire de
la socket serveur et de la compensation intégrale, compensation constatée par
comptage]) et révise le domaine http en ses DEUX seuls points de contact
(http-08:R2 : schéma « https:// » strict minuscule, verdict TLS distinct ;
http-10:R2 : routage vers tls-08 + table des réponses étendue — certificat
invalide → 502 « certificat rejete », ligne console SANS secret) ; sept entrées
IAT secur32 prévues ; le reste du parseur M3 est réutilisé octet pour octet (R7).
**Étape (b) en cours** — D79 : `m4/layout.py` (.text3 @ 0x6000, héritage M0-M3
réexporté, liste blanche HRESULT vérifiée à la source — 3 constantes corrigées),
notations tls-01/02/03 prouvées (différentiel de spécification 165 k cas zéro
écart, falsification 6/6, leçon unicorn consignée) ; D82 : CADRE DE SESSION TLS
arrêté (CredHandle/CtxtHandle @+0x00/+0x10, socket @+0x20, nom @+0x28, verdict
@+0x30, allers @+0x38, tailles de flux @+0x40, zones émission/réception @+0x260/
@+0x4260 — taille 0x8260, fourni VIERGE par http-10:R2) + extension .rdata secur32
(table des descripteurs M4 @0x29A0, « secur32.dll » @0x29F0, slots IAT
0x2A00-0x2A30, INT @0x2A40, fixture package @0x2C00) + **tls-05 (cycle de vie des
handles) notée-mesurée-prouvée — PREMIER BLOC À SHIMS DU JALON** : `m4/harnais_cles.py`
(V1 round-trip 251 o + tls-02 intégrée de bout en bout ; V2 dix scénarios de la
spec, cadre prédit octet par octet, contrat d'appels complet ; V3 5 000 cas fuzzés
ZÉRO écart, graines 20261028/29 ; V4 six mutations d'un point attrapées, témoin
vert 7/7 — leçon : mutation stable en taille) ; **D83 : tls-04 (LA POIGNÉE DE
MAIN — LE critère M4, boucle ISC bornée 16 allers) notée-mesurée-prouvée** :
544 o / 115 instructions / slot 0x62C0×0x300 conservé ; `m4/harnais_poignee.py`
émule les VRAIS octets de tls-02/tls-03/tcp-03/tcp-04 — V2 SEIZE scénarios de
la spec (cadre 0x9000 octet par octet + contrat d'appels complet des ONZE
arguments d'ISC, certificat invalide = verdict 3), V3 5 000 cas fuzzés ZÉRO
écart × 2 graines (10 000 cas), V4 six mutations stable-en-taille attrapées +
témoin 16/16 ; le différentiel a nommé QUATRE défauts avant le vert (dont deux
dans la notation : l'envoyé passé en longueur à tcp-04, xor eax,eax écrasant
le cadre avant phContext) ; IAT_ICS (collision M3/M4 dans auteur.py) corrigé
en IAT_ISC avant première utilisation ; **suite (b) D88 : tls-06 (ÉMISSION
CHIFFRÉE — le tunnel ÉMET) notée-mesurée-prouvée** : 491 o / 105
instructions / 9 étiquettes, slot préfiguré 0x6740×0x300 CONSERVÉ (padding
277, D8 — l'adresse préfigurée de tls-07 @0x6A40 reste exacte) ;
SECPKG_ATTR_STREAM_SIZES = 4 VÉRIFIÉ À LA SOURCE (deux pages Microsoft
concordantes — discipline D79) ; garde P4/I3 cBuffers @+0x4C (acquisition
UNE fois par session, échec E3 → zéro défensif du bloc tailles, modèle
tls-05 D82, AUCUN enregistrement entamé) ; boucle do-while des morceaux
(longueur 0 → UN enregistrement vide, P3 ; morceau = min(restant, message
maximal NÉGOCIÉ), jamais de constante) ; copie libc-01 vers zone+en-tête
(convention contigu tls-03), descripteur tls-03 type 1 SUR la copie (5e
argument [rsp+0x20] = adresse des tailles), EncryptMessageW à QUATRE
arguments registre (fQOP 0, MessageSeqNo 0), total lu des TROIS cbBuffer
APRÈS l'appel (leçon D83 (d)), émission tcp-04 en boucle d'achèvement (le
RESTANT en argument — leçon D83 (b)), E1 → verdict tls-02 + DESTRUCTION du
clair copié par libc-07 (Q2 : zéro octet clair résiduel), E2 → verdict 5,
volatils seuls ; `m4/harnais_emission.py` (VRAIS octets tls-02/tls-03/
tcp-04/libc-01/libc-07, héritage scellé m1/m2 R7) : V2 TREIZE scénarios
(cadre 0x9000 octet par octet + contrat d'appels QCA/EM/SEND complet + span
intact Q3 + QCA jamais rappelée I3), V3 5 000 cas fuzzés ZÉRO ÉCART ×
graines 20261028/29 (10 000 cas cumulés), V4 six mutations
stable-en-taille attrapées + témoin 13/13 — LE DIFFÉRENTIEL EST PASSÉ VERT
AU PREMIER PASSAGE COMPLET (fait notable : tls-06 fut écrite sur les
patrons prouvés de tls-04, les pièges des sessions précédentes traités
AVANT l'écriture — les leçons capitalisent) ; **suite (b) D89 : la CONVENTION DU CADRE AMENDÉE (première fois
depuis D81 — exigée par la spec tls-07:R1 P1/E2, AVANT la notation,
preuve d'innocuité contre l'héritage scellé) puis tls-07 (RÉCEPTION
DÉCHIFFRÉE — le tunnel REÇOIT) notée-mesurée-prouvée** : zone de
réception 2 × MAX_JETON = 32 768 o (TAILLE_CADRE 0x8260 → 0xC260),
DEUX u16 réservés revendiqués @+0x3A/+0x3C (longueur utile réception /
offset résidu — la géométrie de la région vivante, tls-07 unique
propriétaire ; lecture géométrique de Q1 « il sera écrasé » :
l'écrasement est l'œuvre de l'appel SUIVANT — tls-07 normalise
l'offset à 0 au début de chaque appel, le clair pompé est mort, le
lot descend en tête par libc-01 ; la SEULE lecture satisfaisant
span-dans-la-zone + pompage-après-retour + résidu-en-tête) ; aucune
notation scellée n'écrit +0x3A/+0x3C (vérifié), tls-04 voit « ≥
MAX_JETON », R7 intact ; tls-07 : 394 o / 79 instructions, slot
préfiguré 0x6A40×0x300 CONSERVÉ (padding 374, D8 — l'adresse
préfigurée de tls-08 @0x6D40 reste exacte) ; garde E2 UNIQUE sur la
somme offset + lot AVANT tout appel et tout déplacement (une seconde
garde sur la longueur seule fut nommée REDONDANTE par le
différentiel — infalsifiable, donc sans preuve : SUPPRIMÉE, 407 →
394 o) ; descripteur tls-03 type 2 (zone ENTIÈRE en DATA + 3 EMPTY),
DecryptMessageW 4 arguments registre (pfQOP réécrit 0 avant
l'appel), verdict tls-02 intégral, Q1 → span du tampon 0 PAR la
bibliothèque + champs (lot − résidu, résidu), Q2 → rien consommé,
Q3 → fin propre + curiosité « fin propre avec résidu » consignée,
Q4 → verdict + HRESULT, AUCUNE socket (I2) ; `m4/harnais_reception.py`
(VRAIS octets tls-02/tls-03/libc-01, règles shims D89 partagées
modèle/émulation dans layout.py) : V2 SEIZE scénarios EN CHAÎNES (le
rôle appelant tls-08 joué par le harnais lit la géométrie AU CADRE
et réceptionne PAR-DESSUS — le span d'un lot à deux enregistrements
reste OCTET PAR OCTET intact après le retour : la preuve géométrique ;
frontière exacte 32 769 = E2, capacité exacte 32 768 = passe), V3a
4 000 appels + V3b 1 000 chaînes × 3-4 appels fuzzés ZÉRO ÉCART ×
graines 20261028/29, V4 DIX mutations stable-en-taille TOUTES
ATTRAPÉES + témoin 16/16 — BILAN 34 PASS / 0 ÉCHEC × 2 graines ;
reste (b) : tls-08 (orchestration — l'état final de tls-04 doit y
initialiser les champs de géométrie à l'entrée du relais), révisions
http-08:R2/http-10:R2, oracle à scénarios SSPI, carte génération 6
(lignée D80), proxy.exe 0.5.0-dev.1.
**Suite (b) D90 : tls-08 LA SESSION TLS CLIENTE (l'orchestrateur)
notée-mesurée-prouvée — LA SESSION COMPLÈTE EXISTE EN OCTETS** :
740 o / 157 instructions / 16 étiquettes, slot préfiguré 0x6D40×0x600
CONSERVÉ (padding 796, D8 — les révisions http restent à leurs
adresses préfigurées) ; TROIS conventions AVANT la notation
(layout.py, source unique) : le PAQUET DE SESSION (P2 — hôte/port/
requête/socket cliente ; le « contexte de réponse » vit dans le cadre
http-10:R2, NON consommé : la 502 suit le RETOUR du verdict), le
VERDICT_CIBLE 7 (« cible injoignable » : tcp-13 échoue OU tls-01
refuse — hors domaine tls-02, les verdicts 2-6 transportés TELS
QUELS), les fixtures console « tunnel chiffre etabli » @0x2C60 /
« certificat rejete » @0x2C80 (I4 — LE critère M4 : le verdict 3 de
tls-04 produit la ligne AVANT compensation) ; l'ORDRE de Q1 est le
contrat (tcp-13 → nom → credentials → poignée → console → requête →
relais, le clair pompé TEL QUEL jamais parsé) ; TROIS règles
d'orchestrateur : le DRAIN (un verdict 0 de tls-07 avec résidu non
vide est rappelé SANS réception — jamais un enregistrement
déchiffrable en zone pendant que tcp-03 attendrait), la région
vivante VIDE rend sa géométrie morte (offset repris en tête — sans
elle un lot exactement consommé de 0x8000 tuerait une session saine
à la frontière), la garde chambre NULLE avant tcp-03 (r8 > 0 est SON
contrat P3 — fail-closed avant l'appel système, verdict 5 « zone
dépassée ») ; compensation INTÉGRALE par COMPTAGE sur tout chemin :
contexte SI écrit → credentials SI acquis → socket SI ouverte, dans
cet ordre, chacun EXACTEMENT une fois (la remise à zéro de tls-05
après succès constaté est la garde anti-double), E4 = UNE ressaisie
et l'ordre jamais interrompu, aucune écriture au cadre (le rax
prime — http-10:R2 mappe sur le RETOUR) ; `m4/harnais_session.py`
— L'INTÉGRATION LA PLUS LARGE DU PROJET : DIX-HUIT blocs réels
(hello-02 M0, libc-01/03/04/07 M1, tcp-03/04/05/11 M2, tcp-13 M3,
tls-01..07 M4 — R7, octets scellés lus au dépôt), IAT entière en
fausses adresses, entrée ABI exacte (RSP ≡ 8 mod 16) ; V2 VINGT
scénarios (sept de la spec + treize frontières) : cadre 0xD000 octet
par octet + paquet INTACT + contrat d'appels complet (GAI →
freeaddrinfo, ACH, ISC, QCA, EM, DM, RECV/SEND, DSC/FCH,
closesocket, ECS/WF/LCS — la ligne console EXACTE aux octets près) +
COMPTES de compensation ; V3 non applicable (orchestrateur —
héritage M3, harnais déterministe) ; V4 DOUZE mutations
stable-en-taille TOUTES ATTRAPÉES + témoin 20/20 — BILAN 53 PASS /
0 ÉCHEC × graines 20261028/29 ; le différentiel a nommé TROIS
défauts du HARNAIS (le cadre-canari violait la virginité du contrat
P1 : « vierge » = ZÉRO, la garde d'acquisition de tls-06 lisait le
canari — leçon D90 consignée ; tuple GAI ; verdict attendu ACH),
AUCUN dans la notation ; points croisés reportés à http-10:R2 (les
verdicts 4/2 transportés devront trouver leurs entrées de table ;
ne PAS double-émettre la ligne console certificat).
Terrain : D57 (WER, adresse de plantage de la démo) reste le seul point ouvert — le
circuit de constat est désormais réflexe (D71). Hygiène : rotation/restriction
des jetons du dossier Tokens/ (avertissement § 8 toujours réel) ; vider la
corbeille Drive (trace de la phrase D74 — retirée du service depuis la rotation
D80, la corbeille reste à vider par hygiène).

**Souveraineté (D84–D87, 28/10, directives développeur)** : le dépôt est passé
sous **licence BSL 1.1** (`LICENSE` à la racine — concédant **Alexis Lopez**,
Additional Use Grant None, Change Date 2030-10-28 → GPL v3.0+, **secrets et
matériaux de garde exclus** de l'œuvre concédée ; tout usage de production —
notamment par l'employeur — exige une licence commerciale, violation =
termination automatique des droits). Le **programme v0.6.0 « preuve
cryptographique »** est ouvert et consigné (DECISIONS.md D85–D87 + PLAN
section dédiée, alternatives rejetées et critères de sortie par axe) :
(i) **attestation de non-exfiltration** — l'environnement d'exécution de l'IA
devra fournir une quote TPM 2.0/SGX du code manipulant TRIADE-CF1, le coffre
CF2 refusant de déverrouiller sans quote (fail-closed ; l'infrastructure
actuelle sans TEE ne peut pas la satisfaire, dit tel quel) ; (ii) **interrupteur
d'homme mort** — clé maîtresse du coffre CF2 découpée en Shamir, sentinelle
d'audit d'accès détruisant les fragments si un processus non blanchi lit la
couche C : le coffre devient informationnellement mort ; (iii) **filigrane de
l'Intention** — couche I signée par la clé Ed25519 **hors-ligne** du développeur
(le bac à sable ne la verra jamais) : tout diff d'intention exige la clé
physique, le code volé ne peut pas évoluer. Réalisation : priorité CF2-Shamir +
sceau I APRÈS le scellage 0.5.0 de M4 (intégration aux cérémonies § 15.3 /
FORMAT_CARTE § 11) ; la spécification reste v0.5.2 jusqu'à l'écriture des trois
composants (modèle v0.5.1). Hiérarchie des clés qui en découle : phrase de
lignée (enveloppes) / graine en ligne (cartes, FAITS) / clé I hors-ligne
(intention, VOLONTÉ).

## 8. Avertissement sécurité — jetons

Les jetons d'accès ont été stockés dans un dossier Drive partagé par lien. Toute personne
détenant le lien peut les lire : c'est une exposition réelle, incompatible avec la priorité
Sécurité du projet une fois l'infrastructure en place. Recommandations, par ordre de
préférence : restreindre le partage du dossier aux comptes nommés ; ou supprimer les
fichiers de jetons du Drive après vérification que la synchro fonctionne (les copies
locales dans `.gdrive/` suffisent) ; et faire une rotation des jetons au moindre doute sur
une exposition. Ne jamais recopier ces jetons dans le dépôt, dans le bundle ou dans un
fichier synchronisé.

## 9. Commandes utiles

| Commande | Effet |
|---|---|
| `bash scripts/sync_backup.sh "msg"` | Sauvegarde complète (PDF formel si sources changées + commit + Drive + GitHub) |
| `python3 coffre_fort.py lister/verifier/obtenir … --phrase-fichier PHRASE-CONTROLE-COFFRE.txt` | Ouvre le coffre-fort avec la phrase sous garde durable (D81 — p.ex. `obtenir TRIADE lignee-D80 --vers-fichier .keys/passphrase.txt`) |
| `python3 m1/build_m1.py --verifier --graine N` | Ré-vérification complète M1 (R5/R8) + cristallisation (R6) |
| `python3 m2/build_m2.py --verifier --graine N` | Ré-vérification complète M2 (R5/R8) + cristallisation (R6) |
| `python3 m3/outils/auteur.py` | Résout les étiquettes des brouillons M3 → notation explicite (keystone assemble, round-trip capstone) |
| `python3 m3/build_m3.py` | Chaîne M3 complète : assemblage 26 blocs → proxy.exe + oracle (153 036 cas) + carte génération 5 + verrou croisé |
| `python3 m3/build_m3.py --verifier --graine N` | Ré-vérification M3 (notation↔artefact R5, oracle, cristallisation R6, verrou croisé R8) |
| `python3 m3/build_m3.py --sceller-rc` | Scellage 0.4.0-rc.1 (exige 10/10 + conformité verte — D74 ; à présent scellé : la garde anti-rollback refuse) |
| `python3 m3/build_m3.py --sceller-final` | Scellage de la balise finale 0.4.0 (exige rc.1 exactement une fois + conformité + validation terrain consignée — D74) |
| `python3 terrain/build_terrain.py` | Chaîne terrain complète : assemblage 22 blocs → superviseur.exe + oracle (10 080 cas) + carte génération 5 + verrou croisé (D48) |
| `python3 terrain/build_terrain.py --verifier --graine N` | Ré-vérification terrain (R5/R8 + cristallisation R6 — chaque run incrémente les compteurs, 10/10 = cristallisé) |
| `python3 scripts/ecrire_annexe_terrain.py` | Génère `.gdrive/terrain_jetons.bin` (annexe T3, 4 champs NUL ≤ 480 o — SECRET, jamais commité, livraison --dossier-test uniquement) |
| `python3 m1/build_m1.py --sceller-final` | Scellage de la balise finale (exige 10/10 + conformité verte + constat terrain consigné, D32) |
| `python3 m1/conformite_profil.py` | Suite de conformité du profil § 8.2 (68 contrôles, éléments 1-4 et 6-7) |
| `python3 m1/budgets_tokens.py` | Mesure des budgets tokens (écrit `m1/budgets.json`) |
| `python3 m1/demo_r7.py` | Démonstration des adresses stables (R7, lit l'historique git) |
| `python3 m1/export_continuite.py` | Export de continuité chiffré + signé (D16) avec auto-vérification d'import |
| `python3 m1/export_continuite.py --verifier F` | Procédure d'import à sec sur un conteneur F (FORMAT_CARTE § 8.2) |
| `python3 scripts/triade_v03_demo_roomeq.py` | Régénère le PDF de démonstration RoomEq (couverture rendue au préalable via `html2poster.js` — voir en-tête du script) |
| `pdf.py convert.latex scripts/article_v04/main.tex --runs 3` puis `python3 scripts/article_v04/merge_cover.py` | Régénère le corps de l'article v0.4 puis fusionne couverture + corps (couverture : `html2poster.js` sur `cover.html` — voir l'en-tête de `merge_cover.py`) |
| `python3 scripts/article_v04/verify_article.py` | Contrôles pré-empaquetage de l'article (terminologie, IMRAD, références, flottants) |
| `python3 scripts/drive_sync.py` | Synchronisation Drive seule (idempotente) |
| `python3 scripts/drive_livraison.py F…` | Pousse des livrables terrain à la racine du Drive (idempotent, vérification md5 après téléversement ; `--dossier-test` = dossier « test » du développeur ; `--verifier` = état du coffre) |
| `python3 scripts/drive_recuperer.py F…` | Rapatrie un fichier du dossier Drive « test » vers `upload/` (md5 vérifié ; `--lister` = contenu) |
| `python3 scripts/drive_archiver.py F…` | Archive des livrables périmés de la racine du coffre Drive vers `ARCHIVE/` (D76 — déplacement vérifié md5, idempotent, jamais de suppression ; `--verifier` = état racine + ARCHIVE) |
| `python3 scripts/check_auth.py` | Vérifie les jetons Drive et GitHub sans les afficher |
| `git log --oneline` | Historique des modifications |
| `git bundle verify triade-history.bundle` | Vérifie l'intégrité du bundle de sauvegarde |
