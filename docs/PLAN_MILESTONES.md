# FEUILLE DE ROUTE — Jalons M0 à M7

> La feuille de route décompose la validation du protocole en huit jalons, chacun couvrant
> une capacité nouvelle et se terminant par des critères de sortie mesurables. Aucun jalon
> n'est franchi sans que la carte soit signée, le verrou croisé vérifié et l'oracle passé :
> la discipline protocolaire s'applique dès le premier octet. Les jalons M0-M5 s'exécutent
> sur le profil primaire `x86-64-win11-pe` ; M6 et M7, ajoutés par la v0.3, valident
> l'universalité (D14). Mis à jour pour la v0.4.0 : conditions transverses d'acceptation
> (oracle vert, suite de conformité, tableau de bord conforme — spécification § 16) et
> critères de parité inter-profils (spécification § 8.3).
>
> **État : M0 franchi le 26 octobre 2026** (D26 amendée — validation terrain Windows 11
> constatée). **Jalon M1 franchi le 26 octobre 2026** (D32 — validation terrain
> Windows 11 constatée : ligne unique `TRIADE M1 : minilibc 21/21 OK`, contrat
> libc-08 Q2 ; balise finale **`0.2.0`** scellée, immuable § 9). **Jalon M2 franchi
> le 27 octobre 2026** (D43 — boucle § 5 démontrée sur machine réelle, balise
> finale **`0.3.0`** scellée, immuable § 9). **Jalon M3 franchi le 28 octobre
> 2026** (D74 — million de requêtes fuzzées sans crash D72, proxy transparent
> pour curl validé terrain 6× D64-D71, balise finale **`0.4.0`** scellée sur
> cristallisation 38/38 × 10/10, immuable § 9 ; la lignée de clés avait été
> régénérée dans la même session — 4e réinitialisation, D27/D30 réappliquées,
> preuve byte-identique dd12b649). **Jalon M4 franchi le 29 octobre 2026**
(D104 — run 17-H : tunnel chiffré établi et échec propre sur certificat
invalide sur machine réelle ; balise finale **`0.5.0`** scellée, arbre
`m4/I` signé sous le sceau de l'Intention). **Jalon M5 ouvert le
31 octobre 2026** (D133 — programme « Outil complet » ci-dessous) ; chantier
**(a) empreintes par build RÉALISÉ le 31 octobre 2026** (D134 — registre
docs/TABLEAU_BORD.md consigné PAR LES BUILDS, contrôle automatique
`scripts/empreintes_build.py verifier` avec refus nommés, recoupement des 15
modules d'ANNEXE A par `modules`) ; chantier **(b) interception en VM isolée
RÉALISÉ le 4 novembre 2026** (le critère (b) de D136 constaté VERT SUR PIÈCES au
run e4 — Entrée 143, D148 : la page de l'autorité servie ET rendue au navigateur au
marqueur TRIADE-M5B-PAGE-200 avec capture, la 502 « Certificat rejete » REÇUE par
le navigateur — réception triplement recoupée proxy/autorité/navigation, le crash e3
guéri à la base réelle ; balise finale **`0.6.0`** scellée au geste même, contrôle D146
exécuté AU scellage — **JALON M5 FRANCHI**) ; chantier **(c) patch à chaud du
journal en production REPORTÉ au programme M6** (D149 — porté par l'artefact Linux :
le moteur de patch tcp-07 instancié et embarqué, bascule pendant le trafic, rollback,
zéro régression ; le report est EXPLICITE, jamais silencieux). En parallèle (D34, anticipation
> restreinte) : échelle d'auto-hébergement — échelon 1 franchi (hachoir,
> `m6/`), échelon 2 phase 1 scellée (sceau SHA-512 natif, `m7/` — emprunt de
> nommage, les jalons M6/M7 du plan restent inchangés). Composant transversal ajouté
> par la v0.5.1 (D75), hors jalons : le coffre-fort des phrases maîtresses — conteneur
> chiffré TRIADE-CF1 (`coffre_fort.py`, spécification § 15.3 / FORMAT_CARTE § 11).
> Composant transversal v0.6.0 (D84–D87, 28/10) : **souveraineté cryptographique**
> (attestation de non-exfiltration, interrupteur d'homme mort Shamir, filigrane
> hors-ligne de la couche I) + passage du dépôt sous licence BSL 1.1 — cf. Le programme est
> ACCOMPLI et PROUVÉ SUR TERRAIN à la passation v0.6.0 (D133, 31/10) : la chaîne
> réelle du coffre a migré CF1 → CF2 → CF3 les 30–31 octobre 2026.
> section « Programme v0.6.0 » en fin de plan.

L'application cible — un outil de pentest de type intercepteur MITM pour Windows 11 — est
choisie comme stress test : elle exige du réseau, de la concurrence, du parsing d'entrées
non fiables et du chiffrement, soit un large éventail de blocs aux contrats très différents.
Son usage est encadré : tests autorisés en environnement de laboratoire, machine virtuelle
isolée, autorité de certification de test installée localement.

## Vue d'ensemble

| Jalon | Objectif | Livrables | Critères de sortie |
|---|---|---|---|
| M0 | Prouver la chaîne artefact | Éditeur PE32+ minimal ; hello.exe via WriteFile ; carte v0 à trois blocs ; vérificateur de round-trip | Exécution sur Windows 11 ; round-trip 100 % ; carte signée et vérifiée ; moins de 4 Kio. Règles : R1–R3, R8–R9. **Franchi le 26/10/2026** |
| M1 | Blocs réutilisables | Mini-libc scellée : memcpy, memcmp, strlen, itoa, allocateur par zone, memset ; **instrumentation des budgets tokens** ; suite de conformité § 8.2 ; export de continuité D16 | Oracle à 100 % ; première cristallisation ; adresses stables démontrées ; première mesure effective des budgets (localiser/éditer/ajouter). Règles : R5–R7. **Franchi le 26/10/2026 — balise finale `0.2.0` (D32)** |
| M2 | Code actif et patch à chaud | Serveur TCP écho ; thread par connexion ; journal console | Patch du bloc écho pendant exécution, sans interruption ; rollback démontré. Boucle complète. **Franchi le 27/10/2026 (D43) — balise finale `0.3.0`** |
| M3 | Entrées non fiables | Proxy HTTP ; parseur à contrats renforcés ; threading du tunnel | Un million de requêtes fuzzées sans crash ; proxy transparent pour curl. Contrats renforcés. **Franchi le 28/10/2026 (D74) — balise finale `0.4.0`** : étape (a) harnais P1-P5 falsifiable (D45) ; (b) proxy.exe scellé (D47, révisé D63 : 0.4.0-dev.2, oracle 153 036 cas verts, md5 dd12b649…) ; (c) validée terrain 6× (T2 du superviseur, D64-D71) ; (d) campagne million (D72 : 10^6 cas SANS CRASH en 175 s, re-exécution identique, harnais falsifiable) ; (e) suite de conformité § 8.2 (D73 : 161 contrôles, fuzzing intégré 10^4 cas/exécution, sentinelle perpétuelle) ; cristallisation 38/38 × 10/10 puis scellage rc.1 → 0.4.0 (D74 : lignée régénérée D27/D30, preuve byte-identique, asymétrie R6 de l'héritage non embarqué corrigée) |
| terrain/ (hors jalons) | Harnais du terrain (D48) | Superviseur GUI 1 clic : T1 démo + T2 proxy + T3 envoi Drive | **superviseur.exe 0.5.0-terrain.3 scellé (27/10/2026, D50) — 23 blocs dont 11 octet-identiques R7, kit embarqué « 1 seul exe » (D49), oracle 10 102 cas verts, carte génération 5, cristallisation 10/10, audit 61 contrôles ; terrain.2 ne lançait rien (SizeOfHeaders incohérent à six sections — chargeur refusait l'image) : corrigé d'un octet, règle chargeur imposée build+oracle+audit ; run 16 (D71, 28/10 06:54) : T3 démontré de bout en bout PREMIÈRE FOIS — journal terrain_20261028_065408.txt déposé TOUT SEUL dans le dossier test (chaîne de garde fermée, md5 superviseur == LISEZMOI) ; T2 6e vert consécutif ; T1 inchangé D57 (WER attendu)** ; **terrain.17 (D96, 29/10) : superviseur.exe 0.5.0-terrain.4 — T4 (sup-38, 1 505 o) juge LE CRITÈRE M4 sur machine réelle : le kit embarque proxy.exe 0.5.0-dev.2 (le câblage D95), le script client powershell (DONNÉE du plan) joue la forme absolue « GET https://… » qu'aucun client standard n'émet, la 502 étiquetée (34 o) et les événements du tunnel attendus OCTET POUR OCTET — fixtures croisées au build contre les octets de l'artefact scellé ; oracle 10 111 cas + 7 mutations, table R10 PLEINE (28 entrées), cristallisation 10/10, sha 5360ffe2… ; livré (variante publique — T3 sans annexe) dans download/, le journal du développeur attendu pour le scellage 0.5.0** |
| M4 | Tunnel chiffré | Contexte SSPI / Schannel ; poignée de main TLS ; relais chiffré | HTTPS en transit ; échec propre sur certificat invalide. Contrats cryptographiques — **ouvert le 28/10/2026 (D77) : couche I écrite-avant-code (`m4/I/` — domaine `tls` créé, 8 spécifications g7xxxx + charte des contrats cryptographiques : fail-closed intégral [table TOTALE des HRESULT SSPI], certificat invalide = échec nommé → 502 propre, zéro divulgation, compensation exacte ; révisions http-08:R2 [schéma https] et http-10:R2 [routage + table de réponses])** ; **étape (b) ENGAGÉE le 28/10 (D79) : les trois feuilles pures écrites, mesurées et prouvées** — plan d'adressage `.text3` créé (`m4/layout.py` : section 0x6000, héritage M3 réexporté, liste blanche HRESULT VÉRIFIÉE à la source — trois constantes corrigées : DECRYPT_FAILURE 0x80090330 [0x80090321 = BUFFER_TOO_SMALL], CONTEXT_EXPIRED 0x00090317, CERT_WRONG_USAGE 0x80090349) ; notations tls-01 (89 o), tls-02 (156 o), tls-03 (284 o) à la main via `m4/outils/auteur.py` (keystone assemble, rien d'autre) ; `m4/harnais_feuilles.py` : round-trip V1 6/6, différentiel de spécification V2/V3 ZÉRO écart (20009 hôtes + 125274 HRESULT [codes exacts + voisins à un bit + hors domaine] + 20304 triplets, graines 20261028/20261029, ~95 s), canaris + non-volatils + terminaison constatés, falsification V4 6/6 mutations attrapées (bornes relâchées, contrebande de classe, verdicts déviés) ; **suite (b) D82 : cadre de session TLS + extension .rdata/IAT secur32 ARRÊTÉS, tls-05 (cycle de vie des handles) notée-mesurée-prouvée — PREMIER BLOC À SHIMS du jalon** : cadre 0x8260 (CredHandle/CtxtHandle, socket, nom, verdict+HRESULT, allers, tailles de flux, zones émission/réception MAX_JETON — convention partagée tls-04..08, source unique layout.py) ; table des descripteurs M4 @0x29A0 + slots IAT secur32 0x2A00-0x2A30 + fixture package @0x2C00 (l'héritage M3 reste octet pour octet, R7) ; tls-05 : 251 o / 55 instructions / slot 0x65C0 conservé, les NEUF arguments d'AcquireCredentialsHandleW (frontière msx64), pAuthData NULL (P3 validation automatique), HRESULT sign-étendu routé par la VRAIE tls-02, zéro défensif de l'acquisition en échec ; `m4/harnais_cles.py` (mécanisme shims M2/M3 + leçon D79 : émulateur reconstruit à chaque chargement) : V1 round-trip 251 o + tls-02 intégrée, V2 dix scénarios cadre octet par octet + contrat d'appels complet, V3 5 000 cas fuzzés ZÉRO écart (graines 20261028/29), V4 six mutations d'un point attrapées + témoin vert 7/7 ; WIP tué par la panne d'infra post-D80 — récupéré, harnais re-exécuté vert (21 PASS × 2 graines), puis committé ; **suite (b) D83 : tls-04 (LA POIGNÉE DE MAIN — LE critère M4) notée-mesurée-prouvée** : 544 o / 115 instructions / slot 0x62C0×0x300 conservé (padding 224, D8 — tls-05 @0x65C0 inchangé) ; boucle ISC à ONZE arguments (msx64 : 4 registres + 7 pile), phContext NULL-puis-cadre+0x10, phNewContext cadre+0x10, pfContextAttr réécrit 0 avant chaque appel ; garde E5 (16 allers — la terminaison est CONSTATÉE par scénario), garde E2 (jeton hors borne avant toute réception complémentaire), accumulation fraîche après continuation, émission en boucle d'achèvement bornée (restant en argument — jamais l'envoyé), verdicts {3,4,5,6} → Q2 sans compensation (I3), fContextReq = layout.ISC_REQUETES 0xC01C (STREAM pour tls-03:1/tls-06/07, JAMAIS MANUAL_CRED_VALIDATION ni ALLOCATE_MEMORY) ; `m4/harnais_poignee.py` émulant les VRAIS octets de tls-02/tls-03/tcp-03/tcp-04 : V1 round-trip + 4 intégrations, V2 SEIZE scénarios (cadre 0x9000 octet par octet + contrat d'appels complet — le certificat invalide traverse exactement le chemin spécifié D77), V3 5 000 cas fuzzés ZÉRO écart × graines 20261028/29 (10 000 cas), V4 six mutations stable-en-taille attrapées + témoin 16/16 ; le différentiel a nommé QUATRE défauts avant le vert (dont deux dans la notation : l'envoyé passé en longueur, et xor eax,eax écrasant le cadre avant phContext) ; défaut d'outil corrigé avant première utilisation : IAT_ICS déclaré deux fois (InitializeCriticalSection M3 éclipsé par InitializeSecurityContextW M4) → secur32 renommé IAT_ISC ; reste (b) après D83 : tls-06..08 + révisions http-08:R2/http-10:R2 + oracle à scénarios SSPI + carte génération 6 (lignée D80) + proxy.exe 0.5.0-dev.1 ; **suite (b) D88 : tls-06 (ÉMISSION CHIFFRÉE — le tunnel ÉMET) notée-mesurée-prouvée** : 491 o / 105 instructions / 9 étiquettes, slot préfiguré 0x6740×0x300 CONSERVÉ (padding 277, D8 — l'adresse préfigurée de tls-07 @0x6A40 reste exacte) ; SECPKG_ATTR_STREAM_SIZES = 4 VÉRIFIÉ À LA SOURCE (deux pages Microsoft concordantes — discipline D79, constante unique nouvelle) ; garde P4/I3 cBuffers @+0x4C : acquisition des tailles UNE fois par session (cadre VIERGE http-10:R2, convention D81 — échec E3 : zéro défensif du bloc, modèle tls-05 D82, AUCUN enregistrement entamé) ; boucle do-while des morceaux (longueur 0 → UN enregistrement vide, P3 ; morceau = min(restant, message maximal NÉGOCIÉ), jamais de constante — charte § 8) ; copie libc-01 vers zone+en-tête (convention contigu tls-03 : en-tête AVANT, queue APRÈS), descripteur tls-03 type 1 SUR la copie (5e argument [rsp+0x20] = adresse des tailles, P5), EncryptMessageW à QUATRE arguments registre (phContext cadre+0x10, fQOP 0, pMessage descripteur de pile, MessageSeqNo 0), total de l'enregistrement lu des TROIS cbBuffer APRÈS l'appel (leçon D83 (d) : la bibliothèque consigne les longueurs produites), émission tcp-04 en boucle d'achèvement bornée (le RESTANT en argument, jamais l'envoyé — leçon D83 (b)), E1 → verdict tls-02 + DESTRUCTION du clair copié par libc-07 (empreinte complète — Q2 : zéro octet clair résiduel), E2 → verdict 5, volatils seuls (I5, sub rsp 0xE8) ; `m4/harnais_emission.py` émulant les VRAIS octets de tls-02 + tls-03 + tcp-04 + libc-01 + libc-07 (héritage scellé m1/m2, R7 — copie et neutralisation testées à travers leurs octets réels) ; règles shims partagées modèle/émulation : QCA en succès consigne 5 u32 / en échec BARBOUILLE (le zéro défensif doit annuler — falsifiable), EM en succès chiffre SUR PLACE (motifs déterministes) et reconduit les cbBuffer / en échec ne touche rien (le clair subsiste — la notation DOIT détruire) / en descripteur invalide répond SEC_E_INVALID_TOKEN sans écriture ; V2 TREIZE scénarios (cadre 0x9000 octet par octet — clair copié, chiffré produit, ou ZÉROS après destruction ; contrat d'appels QCA/EM/SEND complet ; span de l'appelant intact Q3 ; QCA jamais rappelée I3), V3 5 000 cas fuzzés ZÉRO ÉCART × graines 20261028/29 (10 000 cas cumulés), V4 six mutations stable-en-taille attrapées (attribut QCA 4→5, descripteur tls-03 dévié, pMessage EM dévié, socket déviée, scrub amputé, achèvement court-circuité jz→jnz) + témoin 13/13 ; LE DIFFÉRENTIEL EST PASSÉ VERT AU PREMIER PASSAGE COMPLET — fait notable consigné : tls-06 fut écrite sur les PATRONS PROUVÉS de tls-04 et les pièges des sessions précédentes (envoyé vs restant, cbBuffer à la capacité, cadre écrasé, mutation stable en taille) traités AVANT l'écriture — les leçons capitalisent, le coût du vert baisse à chaque bloc ; **suite (b) D89 : la CONVENTION DU CADRE AMENDÉE puis tls-07 (RÉCEPTION DÉCHIFFRÉE — le tunnel REÇOIT) notée-mesurée-prouvée** : la spec tls-07:R1 (P1/E2) exigeait une zone de réception de 2 × MAX_JETON alors que la convention D81 n'en offrait qu'une de MAX_JETON — zone portée à 32 768 o, TAILLE_CADRE 0x8260 → 0xC260, et les DEUX u16 réservés @+0x3A/+0x3C REVENDIQUÉS par tls-07 (longueur utile réception / offset résidu — la géométrie de la région vivante ; lecture géométrique de Q1 « il sera écrasé » : l'écrasement est l'œuvre de l'appel SUIVANT, tls-07 normalise l'offset à 0 au début de chaque appel — le clair pompé est mort, le lot descend en tête par libc-01 ; c'est la seule lecture satisfaisant span dans la zone + pompage après retour + résidu en tête) ; preuve d'innocuité : aucune notation scellée n'écrit +0x3A/+0x3C (vérifié), tls-04 voit « ≥ MAX_JETON », R7 intact ; tls-07 : 394 o / 79 instructions / slot préfiguré 0x6A40×0x300 CONSERVÉ (padding 374, D8 — l'adresse préfigurée de tls-08 @0x6D40 reste exacte) ; garde E2 UNIQUE sur la somme offset + lot (AVANT tout appel et tout déplacement — une seconde garde sur la longueur seule fut nommée REDONDANTE par le différentiel : infalsifiable, donc sans preuve — SUPPRIMÉE, 407 → 394 o) ; descripteur tls-03 type 2 (zone ENTIÈRE en DATA + 3 EMPTY, sémantique SSPI), DecryptMessageW 4 arguments registre (pfQOP réécrit 0 avant l'appel), verdict tls-02 intégral, Q1 → span du tampon 0 PAR la bibliothèque + champs (lot − résidu, résidu), Q2 → rien consommé, Q3 → fin propre + curiosité « fin propre avec résidu » consignée, Q4 → verdict + HRESULT, AUCUNE socket (I2) ; `m4/harnais_reception.py` émulant les VRAIS octets de tls-02 + tls-03 + libc-01 ; règles shims D89 partagées modèle/émulation (DM déchiffre sur place + réécrit tampons 0/1, MISSING sans toucher la zone, pfQOP non nul en succès — falsifiable, INVALID_TOKEN fail-closed) ; V2 SEIZE scénarios EN CHAÎNES (le rôle appelant tls-08 joué par le harnais lit la géométrie AU CADRE et réceptionne PAR-DESSUS — le span d'un lot à deux enregistrements reste OCTET PAR OCTET intact : la preuve géométrique ; frontière exacte 32 769 E2 / capacité exacte 32 768 passe), V3a 4 000 appels + V3b 1 000 chaînes × 3-4 appels fuzzés ZÉRO ÉCART × graines 20261028/29, V4 DIX mutations stable-en-taille TOUTES ATTRAPÉES + témoin 16/16 — BILAN 34 PASS / 0 ÉCHEC × 2 graines ; **suite (b) D90 : tls-08 (LA SESSION TLS CLIENTE — l'orchestrateur) notée-mesurée-prouvée : la session complète existe en octets** : 740 o / 157 instructions / slot préfiguré 0x6D40×0x600 CONSERVÉ (padding 796, D8 — http-08:R2 @0x7340 et http-10:R2 @0x7480 restent exactes) ; TROIS conventions D90 AVANT la notation (layout.py, source unique) : le PAQUET DE SESSION (P2 — +0x00/+0x08 hôte, +0x10 port, +0x18/+0x20 requête, +0x28 socket cliente ; le « contexte de réponse » vit dans le cadre http-10:R2, non consommé — la 502 suit le RETOUR du verdict), VERDICT_CIBLE = 7 (« cible injoignable » : tcp-13 échoue OU tls-01 refuse — hors domaine tls-02, les verdicts 2-6 transportés TELS QUELS), fixtures console « tunnel chiffre etabli » @0x2C60 / « certificat rejete » @0x2C80 (propriétaire unique tls-08) ; l'ORDRE de Q1 est le contrat : tcp-13 → nom → credentials → poignée → console → requête chiffrée → relais (tcp-03 PAR-DESSUS le résidu → tls-07 → tcp-04 vers le CLIENT, le clair TEL QUEL jamais parsé) ; TROIS règles d'orchestrateur : le DRAIN (verdict 0 avec résidu → tls-07 rappelé SANS réception — jamais un enregistrement déchiffrable en zone pendant que tcp-03 attend), la région VIDE rend sa géométrie MORTTE (offset repris en tête — sans elle un lot exactement consommé de 0x8000 tuerait une session saine), la garde chambre NULLE avant tcp-03 (r8 > 0 est SON contrat P3 — fail-closed avant l'appel système, verdict 5 « zone dépassée ») ; compensation INTÉGRALE par comptage sur TOUT chemin (contexte SI écrit → credentials SI acquis → socket SI ouverte, l'ordre EST le contrat, remise à zéro tls-05 = garde anti-double, E4 : UNE ressaisie, aucune écriture au cadre — le rax prime), champs défensivement zéroés à l'entrée (précédent D83) ; LE CRITÈRE M4 : verdict 3 de tls-04 → ligne console « certificat rejete » AVANT compensation → verdict 3 transporté (la 502 labellisée attend http-10:R2) ; `m4/harnais_session.py` — L'INTÉGRATION LA PLUS LARGE DU PROJET : DIX-HUIT blocs réels (hello-02 M0, libc-01/03/04/07 M1, tcp-03/04/05/11 M2, tcp-13 M3, tls-01..07 M4 — R7), IAT entière en fausses adresses, entrée ABI exacte (RSP ≡ 8 mod 16) ; V2 VINGT scénarios (sept de la spec + treize frontières — drain, fermetures système, E5, tls-01 refus, densité, lot exactement consommé, ACH échec, connect échec…) : cadre 0xD000 octet par octet + paquet INTACT + contrat d'appels complet (GAI→freeaddrinfo, ACH, ISC, QCA, EM, DM, RECV/SEND, DSC/FCH, closesocket, ECS/WF/LCS — la ligne console EXACTE) + COMPTES de compensation (Acquire 1 / Delete 0-1 [+1 simulé] / Free 1 [+1 idem] / serveur 1) ; V3 non applicable (orchestrateur — héritage M3, harnais déterministe) ; V4 DOUZE mutations stable-en-taille TOUTES ATTRAPÉES + témoin 20/20 — BILAN 53 PASS / 0 ÉCHEC × graines 20261028/29 ; le différentiel a nommé TROIS défauts du HARNAIS (cadre-canari violant la virginité P1 — la garde tls-06 cBuffers lisait le canari : « vierge » = ZÉRO, en-tête zéro + zones canari ; tuple GAI ; verdict attendu ACH) — aucun dans la notation ; **suite (b) D91 : http-08:R2 (LA PREMIÈRE RÉVISION DU DOMAINE HTTP SCELLÉ — le parseur sait que le tunnel existe) notée-mesurée-prouvée** : lecture contractuelle ARRÊTÉE avant la notation (rax = 4, verdict « cible TLS » à valeur propre PORTÉ PAR LE RETOUR — convention D90 « mappe sur rax » ; zone remplie aux règles R1 : forme ABSOLUE = 1 [la structure reste absolue, le schéma vit dans le verdict — port implicite 443 déductible], découpages identiques, Q3 hérité applicable à https : « https:// » seul → 2) ; 326 o / 95 instructions / 15 étiquettes, slot préfiguré 0x7340×0x180 conservé (padding 58, D8) ; ordre des tests documenté (I5) : « http:// » D'ABORD (tronçon d'entrée R1 octet pour octet — l'échec du word avec [4]=':' rend https impossible), « https:// » ENSUITE BYTE-EXACT 8 octets (garde len ≥ 8 AVANT toute lecture de [rcx+7] — jamais hors span) ; le début d'autorité PORTÉ dans rdx dès le match (rcx+7 / rcx+8 — LA GÉOMÉTRIE PORTE LE SCHÉMA), verdict déduit STRUCTURELLEMENT au seuil rcx+8 (lea r11 / cmp / mov r11d, 1 — les drapeaux du cmp survivent au mov) : le schéma préfixe « http://s://x » IMPOSSIBLE PAR CONSTRUCTION ; boucle de scan R1 partagée, cinq écritures de zone dupliquées (.ecrit / .ecrit_tls — chaque chemin de verdict explicite) ; fixture « / » @0x24D0 de l'ancêtre RÉUTILISÉE (déplacement RIP inter-sections, R7) ; `m4/harnais_cible_r2.py` avec le DIFFÉRENTIEL D'ANCÊTRE (preuve propre aux révisions : l'ancêtre R1 scellé assemblé à 0x5380 — round-trip 241 o, le préalable — ÉMULÉ contre R2 sur les MÊMES entrées : 20 056 cas, écart ZÉRO, divergence EXACTEMENT le domaine https byte-exact — R1 3 zone intacte → R2 4 zone remplie ou Q3 2 sur autorité vide, tout autre écart serait une régression de l'héritage scellé) + V2b différentiel de spécification (zones 40 o octet par octet, le padding @4-7 JAMAIS écrit) + V3 fuzz 20 000 cas non fiables (octets ≥ 0x80 et NUL — survie, terminaison, verdict conforme, aucune écriture hors zone) + V4 SIX mutations stable-en-taille TOUTES ATTRAPÉES (huitième octet amnésié, casse 's'→'S', LE SCHÉMA PRÉFIXE lea [rcx+8]→[rcx+7], verdict 4→5, forme 1→5, « ? » 0x3F→0x40) + témoin VERT — BILAN 13 PASS / 0 ÉCHEC × graines 20261028/29 ; le différentiel a nommé UN défaut du HARNAIS (domaine de divergence défini par le TEST byte-exact, pas par le verdict produit — « https:// » à autorité vide rend Q3 2 : divergence 3→2 légitime classée à tort régression) ; incohérence docstring layout (http-10:R2 0x7480 → 0x74C0, valeur D77 pré-élargissement) nommée et corrigée ; **D92 : http-10:R2 LA RÉVISION DE ROUTAGE TLS notée-mesurée-prouvée — 2125 o / 430 instructions, slot 0x74C0×0x900 conservé ; convention de cadre D92 (0x13390 : verdict http-08:R2 @+0x7010 écrit sur tout chemin, garde rdi @+0x7020 — le rep stosq du cadre TLS emprunte le non-volatil ABI avec reçu, paquet @+0x7100, cadre TLS @+0x7130 ; probing D63 étendu -0x1000..-0x13000 + touche [rsp-0x13390], innocuité @+0x7010/@+0x7020 par balayage) ; quatre arrêts contractuels (ligne console certificat = tls-08 SEUL, jamais double-émise ; entrée étiquetée « 502 Certificat rejete » @0x2CA0 SEULE entrée nouvelle, verdicts 2/4/5/6/7 → 502 R1 ; port 443 défaut http-07, l'explicite gagne ; corps CL>0 sur TLS → 501 refus honnête, miroir TE) ; .cible_tls miroir exact de .forme_absolue à r8d=443 près, chaîne http-07→TE/CL→réécriture PARTAGÉE, deux dispatches sur le verdict consigné, tls-08 appelé (rcx cadre, rdx paquet) — 0 → .fin, 3 → l'étiquetée, autre → 502 R1 ; « CONNECT https:// » impossible (méthode 8 routée avant tout test de schème)** ; harnais_session_r2.py — L'INTÉGRATION LA PLUS LARGE DU PROJET (×2) : 29 blocs réels + L'ANCIÊTRE http-10:R3 scellé émulé ; différentiel d'ancêtre (traces normalisées par la base du cadre — l'adresse appartient à la notation, le contenu au contrat) : écart ZÉRO hors https, divergence EXACTEMENT https byte-exact ; 23 scénarios (réponse exacte, lignes console une fois, comptage, PAQUET capturé au passage de tls-08, cadre VIERGE canaris→zéro) ; 11 mutations attrapées + témoin ; V6bis prologue + rejet I6' — 69 PASS / 0 ÉCHEC × 2 graines ; le différentiel a nommé une faute ABI (rdi sans reçu) corrigée par la garde @+0x7020 ; **suite (b) D93 : L'ORACLE À SCÉNARIOS SSPI livré (`m4/oracle_m4.py`, 838 lignes — réutilisation stricte D90/D92/D91, jamais deux sources) — F1 session tls-08 à volume hostile (générateurs d'HRESULT table TOTALE, TERMINATION PAR CONSTRUCTION : E5 16 allers, un recv par cycle .relais, drain strictement décroissant, maxmsg ≥ 1 ; Modele vs émulation 18 blocs : rax + cadre 0xD000 octet par octet + contrat d'appels + comptes + paquet intact) ; F2 LE MODÈLE DE ROUTAGE dérivé de I (P6/Q2'/Q3' : ModeleClient capture les octets effectivement émis — _pomper D90 repris tel quel, conformité au parent constatée par comparer_traces ; _reponse_envoyee miroir de l'achèvement E8 ; table 0 → flux pompé par tls-08 / 3 → l'étiquetée / 2-4-5-6-7 → 502 R1) contre l'émulation 29 blocs (réponse exacte, lignes console, comptes, ports, GAI, paquet P6 au passage, cadre VIERGE, requête intacte) + CONCORDANCE I croisée par modele_cible à CHAQUE scénario + arrêts contractuels D92 (CL>0 / TE / POST-PUT sans longueur / autorité vide / HTTPS:// mal cassé / pair parti) ; F3 différentiel d'ancêtre à VOLUME (R7 : écart zéro hors https, divergence exactement byte-exact — l'héritage http non TLS couvert par l'ancêtre émulé, la référence scellée) ; F4 falsification (8 mutations extraites D90/D92 TOUTES attrapées + modèle falsifié nommé + témoin 6/6 + 6/6) ; QUATRE fautes nommées AVANT le vert (layout du paquet de test D80 au-delà de 0x100, règle E5 « POST/PUT » lue dans la spec R1, fragments vides = fermetures pour le shim, échecs d'émission contre le 501 délivré de l'ancêtre) ; couverture MESURÉE (verdicts F1 0:18 / 3:14 / 5:68 / 6:19 / 7:31, relais atteint 16, poignée ≥ 2 allers 71, compensation non triviale 109/150 ; F2 61 % routés ; F3 20 % diverge) — **560 cas × graines 20261028/29/30/31 SANS écart** (~18 s l'exécution complète, volume « reduit » 30 cas ; `executer(blobs, graine, volume)` prêt pour build_m4.py — lève EchecOracle sur tout écart, empreinte hachée au rapport de build)** ; **suite (b) D94 : LE BUILD livré — proxy.exe 0.5.0-dev.1 (28 160 o, sha 43e2e40d…) + carte génération 6 (lignée D80)** : `m4/build_m4.py` + `m4/carte_m4.py` — l'héritage re-vérifié (build_m3.assembler_tout rejoué : R5 26/26 + 524 verrous M3) et l'image M3 composée prouvée ÉGALE au scellé 0.4.0 OCTET PAR OCTET avant extension (sha bf02769f…) ; **libc-07 (memset) devient EMBARQUÉ** @0x13C0 (zone reserve-libc, octets selftest.exe — R7 direct ; exigé par tls-06/tls-07) ; **la porte R10 gagne son entrée** (27 blocs + terminateur finissent EXACTEMENT à 0x2820 = R_VERSION — l'entrée appendue @0x2800, terminateur à 0x2810, le http-12 scellé garde la nouvelle entrée sans bouger, les 27 sommes recalculées du binaire à la validation, version 0x00050001 ≥ plancher) ; deltas .rdata documentés (8e entrée de la table des réponses @0x2550 [l'entrée ÉTIQUETÉE D92], entrée R10, version, extension @0x29A0+ : descripteurs 3 DLL, secur32.dll, IAT/INT/hints ×7, package, fixtures) ; **ARRÊT D94 offsets fichier** : la cinquième en-tête de section (528 o) pousse .text à 0x400 — packaging +0x200 CONTIGU (0x400/0x1400/0x2400/0x2E00/0x4E00, fin 0x6E00), RVA INTACTS (préfiguration D77 encodée en TEXT3_FILE=0x4E00) ; oracle structurel M4 **417 verrous** (tables d'autorisation extraites par scripts/diag_structure_m4.py : IAT PAR BLOC — secur32 ×7 vérifiées, tls-08 AUCUNE, http-10:R2 CloseHandle SEUL [I6'] —, appels directs, données RIP, concordance des DÉPLACEMENTS RIP DÉCLARÉS contre le désassemblage, prologue probing D63 armé sur 0x13390, tailles déclarées == assemblées, D8, pile, syscall, RSP) ; canon() étendu (alias jcc, qualificateurs déductibles, complément à deux à la largeur, crochets, chaînes) ; l'oracle D93 sur les blobs du build : 560 cas verts ; verifier-puis-écrire 37/37 ; carte génération 6 signée Ed25519 (MÊME graine — le témoin ne bouge pas), 48 blocs sur 5 artefacts, verrou croisé 48 empreintes, cristallisation 3/10 en trois runs, artefact BYTE-STABLE ; anti-rollback R6 armé — **ÉTAPE (b) CLOSE** ; **suite D95 : LE CÂBLAGE livré — http-12:R2 notée-mesurée-prouvée puis embarquée, proxy.exe 0.5.0-dev.2 (28 160 o INCHANGÉS, sha b813f65e…)** : la boucle d'acceptation lance http-10:R2 (0x74C0 — UNE instruction fonctionnelle change, le `lea` du spawn ; l'entrée PE passe à 0x7DC0, delta PE documenté, l'ancêtre @0x1800 reste embarqué octet pour octet R7 — mort au lancement, vivant à la preuve d'héritage) ; **LA PORTE R10 .text3 vient avec le câblage (pas en contrebande)** : la table est PLEINE (27 entrées + terminateur @0x2810, R_VERSION @0x2820 immovable R7) — l'entrée #28 (0x6000, 0x2000, somme .text3) REMPLACE le terminateur et la marche de http-12:R2 s'arrête à la BORNE (l'adresse de R_VERSION) : fail-closed sur entrée trouée (rva nul / taille nulle = KO — la troncature silencieuse du terminateur M3 n'existe plus), LA COUCHE M4 ENTIÈRE GARDÉE AU LANCEMENT (bloc 0x7DC0 compris : la porte se garde elle-même, miroir http-12:R1 @0x1800) ; spec m4/I/http-12-principal-r2.md écrite-avant-code ; notation 458 o / 99 instructions / slot 0x7DC0×0x200 (la section ne grandit pas — l'ancienne réserve int3 absorbe le câblage, réserve 0x7FC0-0x7FFF) ; `m4/harnais_principal_r2.py` — différentiel d'ancêtre à 12 scénarios (traces R1 == R2 sauf la cible du spawn 0x5580 → 0x74C0 ; divergence légitime .text3 NOMMÉE : R1 ne la garde pas, R2 la nomme KO — miroir du domaine https D91), fuzz de la porte 400 mutations d'un point (modèle de marche DEPUIS LA SPÉCIFICATION contre les OCTETS — même verdict, ZÉRO passage silencieux), falsification 6/6 (LE CONTRE-CÂBLAGE lea → 0x5580, les bornes ±0x10 [l'entrée .text3 sautée / la version lue comme entrée], le plancher abaissé, le code E3, le sens du test d'arrêt) + témoin — 12 PASS / 0 ÉCHEC × graines 20261028/29 ; CINQ fautes du HARNAIS nommées avant le vert (symboles de fixtures croisés MSG_KO/MSG_ERREUR/MSG_CONNEXION ; drapeau R_QUIT semé un octet sur un qword lu entier ; appel tcp-01 omis du modèle en échec d'écoute ; remplissage uniforme puis linéaire → collisions de somme : PRNG seedé ; mutations sans effet au fuzz) — aucune dans la notation ; build dev.2 en UNE décision verte (assert BLOCS_M4 == layout : la notation orpheline impossible) : section .text3 composée D'ABORD (la porte scelle sa somme dessus), validation = marche aux bornes 28 entrées (le MÊME contrat que la notation — jamais deux sources), oracle structurel M4 473 verrous (+56 : IAT g70011, appels directs, données RIP dont les DEUX cibles de code par lea), verifier-puis-écrire 38/38, carte génération 6 : 49 blocs, verrou croisé 49 empreintes + signature Ed25519, cristallisation 3/10 en trois runs BYTE-STABLE (sha inchangé), anti-rollback armé (dev.2 > dev.1 licite) — **LE CRITÈRE M4 EST CÂBLÉ DE BOUT EN BOUT : entrée PE → http-12:R2 → http-10:R2 → tls-08 → Schannel** ; **cristallisation 10/10 (D96 : 49/49 blocs, 10 runs byte-stables, sha b813f65e… inchangé) ; terrain.17 (D96) LIVRÉ : T4 jouera https saine + certificat invalide → 502 étiquetée sur machine réelle (le kit porte le proxy M4, les fixtures croisées contre l'artefact) — le scellage 0.5.0 attend le journal du développeur** ; terrain : D57 (WER) seul point ouvert |
| M5 | L'outil complet | Autorité de test locale ; interception et re-chiffrement ; journal des flux ; interface en ligne de commande | Interception d'un flux navigateur en VM isolée ; patch à chaud du journal en production ; empreintes par build activées. Intégralité du protocole. **Franchi le 04/11/2026 — balise finale `0.6.0`** (Entrée 143, D148 : critère (b) de D136 constaté VERT sur pièces au run e4 ; le chantier (c) reporté au programme M6 par D149) |
| M6 | Portabilité inter-OS | Profil `x86-64-linux-elf64` complet : même couche I réutilisée sans modification ; mini-libc re-scellée pour le profil ; hello et serveur écho sur Linux ; **suite de conformité du profil** | **Suite de conformité verte (§ 8.2)** ; diff nul sur la couche I ; carte multi-profils signée et vérifiée ; le même oracle passe sur les deux profils ; **parité inter-profils vérifiée (§ 8.3)**. **Franchi le 05/11/2026 — balise finale `0.7.0`** (Entrée 149, D154 : run terrain WSL2 vert sur pièces — recoup labo 22/22, le noyau 6.18.54.1-microsoft-standard-WSL2 de la machine du développeur DISTINCT de celui du labo, ASLR complet ; conformité 7/7 exécutée AU scellage même, l'artefact INTACT sha dd14195c… ; le chantier M5-(c) refermé sur le profil Linux — la bascule pendant le trafic, le rollback, la zéro régression) |
| M7 | Portabilité inter-ISA | Profil `riscv64-linux-elf64` : blocs re-générés pour une ISA à instructions de taille fixe ; patch à chaud adapté (registre scratch + `fence.i`) ; **suite de conformité du profil** | Round-trip 100 % sur la nouvelle ISA ; **suite de conformité verte (7/7 — 29 contrôles, le 05/11)** ; patch à chaud conforme au profil (**DÉMONTRÉ en exécution — le démonstrateur invité, la bascule pendant le trafic**) ; verrou croisé multi-profils (**VIVANT — 26 empreintes DEUX ISA**) ; **parité inter-profils vérifiée (§ 8.3 par exécution)** ; export de continuité multi-profils vérifié (**VERT DE BOUT EN BOUT — 34+5 verrouillés, 5 cartes, 81 specs I, les rituels rejoués sur les octets transportés**) — **les chantiers (a)(b)(c) RÉALISÉS (05/11, Entrées 150/152/153), la 0.8.0-rc.1 SCELLÉE ; (d) RÉALISÉ (05/11, Entrées 154/155 : la part laboratoire — l'export VERT + le kit terrain DÉPOSÉ au coffre /test avec l'instrument embarqué + la clôture D143 du run m6d — puis LE RUN TERRAIN VERT SUR PIÈCES 16/16 + LE RECOUP LABO VERT 29/29 sur pièces croisées + LA FINALE 0.8.0 SCELLÉE, l'artefact intact) — LE JALON M7 FRANCHI, l'universalité DÉMONTRÉE (win 0.6.0 / linux 0.7.0 / riscv 0.8.0)** |
| M8 | Syscalls directs (win) | Le domaine `sys` sur le profil primaire : l'émetteur syscall direct (le trombone ABI, zéro IAT), le résolveur SSN (l'EAT de ntdll LUE directement, le motif du stub VÉRIFIÉ avant l'extraction), l'usage réel (la twin de hello-02 par NtWriteFile — la même observable, le second chemin) ; **le SSN est une DONNÉE, jamais un octet de code** | Le mécanisme prouvé au harnais (round-trip, oracle structurel — la règle AUCUN IAT PAR BLOC sys, différentiel sur FIXTURES ntdll) ; le terrain : le VRAI ntdll lu sur la machine du développeur, le motif confronté, la ligne comparée par les DEUX chemins, tout stub divergent = refus nommé ; run terrain VERT sur pièces → balise finale `0.9.0` — **OUVERT le 05/11/2026 (D160, Entrée 156) : la couche I écrite-avant-code LIVRÉE (chantier (a) RÉALISÉ) ; les blocs notés-mesurés-prouvés LIVRÉS (chantier (b) RÉALISÉ — Entrée 157, D161 : les trois notations 6/293/164 o, l'arrêt des slots sur mesure, le harnais 61/61 VERTS sur fixtures ntdll synthétiques — la twin au différentiel, la MÊME ligne par les DEUX chemins) ; les chantiers (c)/(d) attendent** |

## Conditions transverses d'acceptation (v0.4.0)

Ajoutées par la v0.4.0 (spécification § 16), elles s'appliquent à **chaque** jalon, en sus
des critères propres :

1. **Oracle vert** — 100 % des tests différentiels de la couche I concernée (R5).
2. **Suite de conformité verte** pour les éléments du profil couverts par le jalon (§ 8.2).
3. **Tableau de bord conforme** (§ 15.2) — aucune métrique au rouge, les métriques « cible »
   explicitement annotées comme telles tant que l'outillage n'est pas déployé (budgets
   tokens : première mesure effective à M1).
4. **Carte signée, verrou croisé vérifié** — inchangé depuis la v0.1 : dès le premier octet.
5. **Journal à jour** — décisions, optimisations (R11) et classification taxonomique des
   défauts corrigés dans le périmètre du jalon.

## Jalons charnières

**M0 est le jalon existentiel — il est franchi.** Il prouvait que la chaîne notation,
octets, exécutable, exécution fonctionne de bout en bout sans compilateur, et que la
carte rend le résultat vérifiable. Validation acquise le 26 octobre 2026 (D26 amendée) :
round-trip 100 %, 31 verrous structurels PASS, artefact `hello.exe` de 1 536 octets
déterministe, carte v0 signée Ed25519, verrou croisé fail-closed, exécution constatée
sur Windows 11 (sortie exacte du contrat). Livrables : éditeur PE32+ minimal (écriture des
en-têtes DOS/COFF/PE32+ et des sections `.text`/`.rdata` par le script de build),
hello.exe affiché via WriteFile, carte v0 décrivant les trois blocs initiaux, et le
vérificateur de round-trip keystone/capstone — le tout dans `m0/`.

**M2 est le jalon de vérité du protocole.** Le patch à chaud sur code en cours d'exécution
est la capacité qui a motivé l'architecture de balises depuis la première discussion. Sa
démonstration — bascule atomique par trampoline de 12 à 16 octets, continuité de service,
rollback copy-on-write — valide que l'investissement dans la carte et le verrou croisé
paie concrètement. Scénario de sortie : remplacer le bloc d'écho du serveur TCP pendant
qu'il traite des connexions, sans interruption de service.

Les jalons suivants (M3 à M5) étendent le périmètre fonctionnel sans ajouter de mécanisme
protocolaire nouveau : ils éprouvent les mêmes règles sur des contrats de plus en plus
exigeants — parsing d'entrées non fiables (M3), contrats cryptographiques (M4), intégration
complète de l'outil avec interception TLS, journalisation et traçage par build (M5).

## Universalité — M6 et M7 (v0.3)

Ajoutés par la v0.3 (décision D14), M6 et M7 transforment la portabilité de promesse en
propriété démontrée, en isolant chaque variable. **M6 change l'OS à ISA constante** : le
profil `x86-64-linux-elf64` diffère du profil primaire par l'ABI (SysV : RDI RSI RDX RCX
R8 R9, zone rouge de 128 octets — le piège inverse de msx64), le format (ELF64 avec PIE et
RELRO, écrit à la main) et l'interface système (syscalls + libc). Le critère décisif est le
**diff nul sur la couche I** : les contrats écrits pour Windows s'instancient sur Linux
sans réécriture — c'est la preuve que l'intention vit bien dans I et pas dans les octets.
**M7 change d'ISA** : le profil `riscv64-linux-elf64` impose des instructions de taille
fixe, une convention psABI (a0-a7) et un patch à chaud sans trampoline relatif — bascule
par registre scratch suivie de `fence.i`. Le critère décisif est que **le même oracle**,
dérivé de la couche I inchangée, valide les blocs des deux ISA : le coût de vérification
ne double pas, il se mutualise. M7 vérifie de surcroît un export de continuité
multi-profils de bout en bout.

L'ordre est délibéré : valider d'abord le mécanisme des profils (une seule variable à la
fois), puis l'indépendance de l'ISA. Les profils `aarch64-macos-macho` et `wasm32-wasi`
restent réservés : le protocole ne promet pas la portabilité, il la vérifie — chaque
profil déclaré supporté doit avoir franchi ses critères de sortie.

## Indicateurs de santé transverses

Mesurés à chaque jalon, ils valident que l'économie promise par le protocole est réellement
délivrée :

| Indicateur | Cible | Premier mesuré |
|---|---|---|
| Précision de localisation (bon bloc identifié du premier coup) | 95 % | M0 |
| Coût moyen d'une édition simple | 5 000 tokens | M1 |
| Taux de régression post-patch (rollback exclus) | zéro | M2 |
| Corruptions détectées par l'oracle | toutes, zéro silence | chaque jalon |
| Échecs de verrou croisé non bloquants | zéro (fail-closed strict) | chaque jalon |

## Rappels protocolaires par jalon

- M0 : règles R1–R3 (jamais de binaire nu, intention d'abord, balisage) et R8–R9 (verrou
  croisé, carte signée) dès le premier octet.
- M1 : règles R5–R7 (vérifie-puis-écrit, cristallisation, adresses stables) — la
  mini-libc est le premier terrain de cristallisation.
- M2 : boucle complète, patch à chaud et rollback démontrés.
- M3 : contrats renforcés sur entrées non fiables — fuzzing systématique.
- M4 : contrats cryptographiques — échec propre sur certificat invalide.
- M5 : intégralité du protocole, empreintes par build activées, interception en VM isolée.
- M6 : profil `x86-64-linux-elf64` — règles identiques, ABI/format/interface différents.
- M7 : profil `riscv64-linux-elf64` — règles identiques, ISA différente, patch à chaud
  adapté.

Après M7 : bloc optionnel de syscalls directs, TLS 1.3 pur en blocs scellés, profils
additionnels (`aarch64-macos-macho`, `wasm32-wasi`) — volontairement hors périmètre
courant afin que chaque addition s'appuie sur des résultats mesurés. **L'ère est
OUVERTE le 05/11/2026 (D160, Entrée 156) : la première famille est le jalon M8
(le domaine `sys` — voir « Programme d'après M7 ») ; la clause « hors périmètre »
est levée NOMMÉMENT pour elle seule, les deux autres familles attendent leur
décision propre.**

## Programme v0.6.0 — Souveraineté cryptographique (composant transversal, hors jalons)

Ouvert le 28/10/2026 par directives développeur (décisions **D84–D87**, format
normalisé § 15.1) — en complément du passage du dépôt sous **licence BSL 1.1**
(concédant Alexis Lopez, cf. `LICENSE`). La menace nommée : l'expropriation par
l'employeur — un tiers qui s'empare du binaire, du dépôt, voire des clés du
poste. La v0.6.0 renforce la preuve cryptographique sur trois axes ; la
spécification `PROTOCOLE_TRIADE.md` passera à v0.6.0 quand les trois composants
seront écrits (modèle v0.5.1 : spécifiés à l'implémentation, pas avant).

| Axe | Décision | Mécanisme | Critère de sortie |
|---|---|---|---|
| 1. Attestation de non-exfiltration | D85 | L'environnement d'exécution de l'IA fournit une attestation matérielle TPM 2.0/SGX (quote vérifiable) du code manipulant TRIADE-CF1 : code identifié, sans egress cloud des dérivés du coffre, sorties scellées localement ; le coffre CF2 refuse de déverrouiller sans quote (fail-closed) | Conteneur « exige-attestation » : ouvert avec quote, REFUS nommé sans quote ; quotes altérées/rejouées rejetées (falsifiabilité) |
| 2. Interrupteur d'homme mort | D86 | Clé maîtresse du coffre CF2 découpée en Shamir (jamais stockée entière) ; sentinelle d'audit d'accès sur la couche C — lecture par processus hors liste blanche → destruction des fragments (écrasement multi-passe) → coffre indéchiffrable | Scénario d'exfiltration simulé en VM : fragments détruits, conteneur indéchiffrable ; fausses alertes nulles en essai nominal ; latence détection→destruction bornée |
| 3. Filigrane de l'Intention | D87 | Chaque arbre de couche I condensé puis signé par la clé Ed25519 du développeur **hors-ligne** (jamais dans le bac à sable) ; build et chemin de patch refusent une couche I non signée → tout diff d'intention exige la clé physique | Cérémonie hors-ligne documentée ; signature I vérifiée sur tous les jalons scellés ; falsification d'un octet rejetée ; diff non signé refusé par le chemin de patch |

**Positionnement** : priorité aux axes 2 et 3 (CF2-Shamir, sceau I) après le
scellage 0.5.0 de M4 — ils touchent les disciplines § 15.3 et FORMAT_CARTE § 11
et doivent s'intégrer aux cérémonies de rotation et de garde existantes ;
l'axe 1 (attestation TEE) selon disponibilité d'une infrastructure à racine de
confiance — l'exigence est d'ores et déjà consignée, l'infrastructure actuelle
(VM cloud sans TEE) ne peut pas la satisfaire et le dit.

**Avancement** : **axes 2 et 3 LIVRÉS en phase laboratoire (D105/D106,
29/10)** — axe 3 : spec écrite-avant-code (`v06/I/README.md`), cérémonie
hors-ligne autoportière (`v06/ceremonie_hors_ligne.py`, stdlib seule,
autotest RFC 8032 fail-closed), dix arbres signés (`v06/sceau-I/`), gardes
sceau-I dans `build_m4.py` et `build_terrain.py`, falsifiabilité 47/47 ;
l'état « test » est VISIBLE tant que le développeur n'a pas exécuté la
cérémonie réelle (`download/LISEZMOI-cle-I.txt`). Axe 2 : spec
écrite-avant-code (`v06/I/CF2/README.md` — l'arbre v06/I porte les deux
axes, balise `v0.6.0-axes2-3`), coffre CF2 à clé maîtresse jamais stockée
entière (Shamir sur générateur PRIMITIF 0x03 — 0x02 n'est pas primitif
modulo 0x11B, ordre 51 : consigné), sentinelle inotify + attribution /proc
à double seuil (latence mesurée 0,05 s, borne 2 s), destruction trois
passes + PV, migration CF1 → CF2, falsifiabilité 43/43
(`v06/test_cf2.py`) ; le coffre réel n'a pas migré — l'acte qui arme
l'interrupteur appartient au développeur
(`download/LISEZMOI-coffre-CF2.txt`). Les cérémonies sont menées par le
MAÎTRE DE CÉRÉMONIE GRAPHIQUE (D107 : `v06/ceremonie_gui.py`, un fichier,
deux profils, zéro ligne de commande — falsifiabilité 36/36 + fumée Xvfb
14/14) et le kit complet est déposé dans le dossier **/Cérémonie du
Drive** (D108, 30/10 : 14 fichiers vérifiés md5 aller-retour, `v06/` en
mini-dépôt portable, MANIFESTE d'empreintes, aucun secret) — les
cérémonies réelles peuvent s'armer depuis le dépôt OU depuis le Drive.
Les trois composants étant écrits
(l'axe 1 D85 reste une exigence consignée — infrastructure sans TEE), la
passation de la spécification à v0.6.0 était MÛRE : **elle est effective
(D133, 31/10/2026)** — l'arbitrage du développeur a tranché : passer avec
l'axe 1 consigné. L'état au moment de la passation : axes 2 et 3 non seulement
livrés mais PROUVÉS TERRAIN — la chaîne réelle du coffre a migré CF1 → CF2
(le 31/10 : phrase changée D110, cinq gardes seuil 3, trois copies hors-ligne,
CF1 laissé intact) puis CF2 → CF3 (le 30–31/10 : époque 1, checksum
`0cc89a96`, verdict à froid VERT deux fois, CF2 laissé intact jusqu'au geste
explicite de destruction) —, la re-cérémonie du sceau accomplie par le
développeur depuis son clone (D126 : dix signatures vérifiées, commit 20f40bc
poussé), l'outillage de migration livré (D127), les cérémonies conduites par
le maître de cérémonie graphique avec le kit Drive identique au miroir par
construction (D130). Un AXE 4 s'est ajouté en cours de route, né du terrain :
la serrure à triple scellement CF3 (D121) — le démon sentinelle remplacé par
un piège hors machine, la sentinelle instantanée PAR INVOCATION, le cycle en
deux actes. La spécification `PROTOCOLE_TRIADE.md` est passée à v0.6.0 puis à
v0.6.1 (D137) ; le PDF formel et le *Livre du Coffre* (complément opératoire,
v1.1) l'accompagnent (`docs/`). Le niveau d'un coffre neuf — CF1, CF2 ou CF3 —
est arbitré par le développeur à la création de son projet (D137, v0.6.1) : la
chaîne de migration appartient à l'histoire du coffre réel et demeure
disponible à tout moment.

**Hiérarchie des clés qui en découle (trois gardes, trois menaces)** : phrase
de lignée (chiffre les enveloppes, vol au repos) ; graine Ed25519 en ligne
(signe les cartes — les FAITS) ; clé I hors-ligne (signe l'intention — la
VOLONTÉ). La barrière juridique (BSL, D84) et la barrière cryptographique
(D85–D87) se répondent : la licence pour les tribunaux, les preuves pour la
machine.

## Programme M5 — Outil complet (ouvert le 31/10/2026, D133)

Le jalon de l'outil complet s'ouvre sur trois chantiers mesurables, ordonnés par
la dépendance — (a) arme la preuve dont (b) et (c) ont besoin pour être auditables :

| Chantier | Contenu | Critère de sortie mesurable |
|---|---|---|
| (a) Empreintes par build actives — **RÉALISÉ (D134, 31/10)** | chaque build consigne l'empreinte de son artefact au tableau de bord et au journal de travail ; la comparaison inter-build devient un contrôle automatique | tout artefact livré porte son empreinte CONSIGNÉE par le build qui l'a produit ; une divergence inter-build est un refus nommé — CONSTATÉ : registre rattrapé des dix PDF livrés, build_livre.sh né, deux consignations PAR LE BUILD, seize contrôles de falsifiabilité, refus nommés vivants |
| (b) Interception en VM isolée — **RÉALISÉ (04/11/2026, Entrée 143/D148)** | le proxy transparent M3 porte le tunnel M4 au scénario réel complet : navigateur, VM isolée, autorité de test locale | un flux navigateur intercepté de bout en bout dans la VM (journal + témoin sur disque, leçon D99) ; échec propre sur certificat invalide constaté dans LE MÊME run — CONSTATÉ au run e4 : critère (b) de D136 VERT sur pièces (page au marqueur + capture, 502 « Certificat rejete » reçue — réception triplement recoupée), crash e3 guéri à la base réelle, finale `0.6.0` scellée |
| (c) Patch à chaud du journal en production — **REPORTÉ au programme M6 (D149, 04/11), REFERMÉ au chantier M6-(d) (05/11/2026 — Entrée 149 : démontré sur le profil Linux, run terrain VERT sur pièces, balise finale `0.7.0`)** | l'écriture vivante du superviseur terrain sous patch, retour arrière prêt | patch appliqué pendant le trafic, journal cohérent, rollback démontré, zéro régression (suite de conformité verte) — le critère sera démontré sur le profil Linux (M6-(d) : moteur tcp-07 instancié et embarqué, bascule pendant le trafic, rollback) |

Conditions transverses inchangées : oracle vert, suite de conformité verte,
tableau de bord conforme, carte signée — et, depuis le sceau, couche I signée
à chaque build. La discipline du terrain demeure la règle : l'évidence avant
le correctif, chaque run rapporte ses propres preuves.

## Programme M6/M7 — Universalité (ouvert le 04/11/2026, D149)

M5 rentré (balise `0.6.0`), les jalons d'universalité prennent la suite : transformer
la portabilité de promesse en propriété démontrée, **une variable à la fois** — l'OS
d'abord (M6, à ISA constante), l'ISA ensuite (M7). Le profil `x86-64-linux-elf64`
n'est PAS une page blanche : l'échelle d'auto-hébergement (D34) y vit déjà — le
hachoir (`m6/`, échelon 1 : ELF64 écrit à la main, exécuté nativement au labo, oracle
différentiel FIPS 180-4 sur le terrain natif) et le sceau (`m7/`, échelon 2 phase 1) —
la chaîne notation → octets → ELF64 → exécution réelle est PROUVÉE. Le jalon M6 porte
ce qui manque à l'universalité : la **parité du patrimoine** des jalons Windows
(M0–M5), le **diff nul sur la couche I**, le **même oracle vert sur les deux
profils**, et le durcissement format de l'artefact du jalon (PIE, NX, segments
R/RX/RW — l'ELF minimal auto-hôte demeure valide pour sa lignée, l'écart est nommé).

Les fiches de profil complètes (sept éléments + anti-rollback, spécification § 16)
vivent à `docs/PROFIL_x86-64-linux-elf64.md` et `docs/PROFIL_riscv64-linux-elf64.md`
— le protocole exige une fiche écrite et vérifiée AVANT toute instanciation (manuel
§ 2) ; leurs constats labo sont datés du 04/11/2026 et re-vérifiés au premier
chantier qui les touche. **Convention de dossiers (D149)** : le jalon M6 vit dans
`unix/`, le jalon M7 dans `riscv/` — les noms `m6/` et `m7/` appartiennent à
l'échelle d'auto-hébergement (emprunt de nommage consigné, le présent programme ne
le défait pas).

**État du programme.** **Chantiers M6-(a), M6-(b) et M6-(c) RÉALISÉS — le
04/11/2026 pour (a)/(b), le 05/11/2026 pour (c)** (Entrées 145-147, D150-D152)
— la sonde `unix/` (M6-(a), Entrée 145) a posé le durcissement format DÉMONTRÉ
en exécution (ET_DYN/PIE à base aléatoire constatée, W^X depuis les phdr,
table ERRNOS exercée sur ses deux branches — balise 0.7.0-dev.1) ; **le corpus
paritaire (M6-(b), Entrée 146) L'INSTANCIE ET LE MESURE** : les DOUZE blocs du
patrimoine M0-M5 révisés R+1 au niveau FORMEL (audit de couplage `unix/I/
AUDIT-COUPLAGE-CORPUS.md` : la classe A est VIDE, la voie du diff nul passe
ENTIÈREMENT par la révision de granularité) + `corpus-13` le principal propre
au jalon (domaine neuf, modèle ah-09) ; le diff nul MESURÉ PAR SCRIPT
(`unix/diff_nul.py`, 39 recoupements : fichiers canoniques `unix/I/` empreintés
zéro copie, observables R1↔R+1 équivalents, les CINQ scellés Windows
octet-identiques à l'état zéro mesuré avant le geste) ; l'oracle m1 régénéré
VERT sur l'instance Linux (76 631 cas verts, 20 verrous, exécution native,
falsification 12/12 zéro silence — tcp-07 épuisé par SON scénario et le V7 DEP
en fils) ; l'artefact `unix/corpus` 12 288 o (ET_DYN/PIE, héritage M6-(a)
recoupé `readelf`), sha256 dd14195c…, la balise 0.7.0-dev.2 posée, la carte
génération 1 du corpus. **La suite de conformité + le scellage (M6-(c),
Entrée 147) : la suite VERTE 7/7** (`unix/conformite_profil.py`, modèle m5 —
37 contrôles PASS, les SEPT éléments CONSTATÉS depuis l'artefact relu + le
diff nul REJOUÉ à chaque passage) ; **le contrôle D146 adapté NÉ**
(`unix/controle_base_reelle.py` : l'image PIE EXÉCUTÉE PAR LE NOYAU, 6 bases
réelles DISTINCTES constatées par témoin ptrace/maps, ADDR_NO_RANDOMIZE
recoupé, le mutant « RVA nu » mort nommé — la classe exacte du crash e3) ;
la cristallisation conduite à 10/10 (l'incident intermittent de la cartouche
— l'allocateur de sommets sous concurrence — nommé et corrigé : le sommet est
PAR FIL, D152 ; le bloc tcp-11 EXONÉRÉ sur pièces, l'artefact n'a pas bougé
d'un octet) ; **LE SCELLAGE 0.7.0-rc.1 POSÉ avec le D146 EXÉCUTÉ AU SCELLAGE
même** (modèle D147 — cristallisation 10/10 + conformité 7/7 + bascule de
balise dans frag-bld, occurrence unique assertée, re-scellage vérifié en
mémoire avant l'unique écriture ; l'artefact INTACT sha dd14195c…, le
scellage est un fait de carte) ; **les gardes VIVANTES sur pièces**
(re-scellage REFUSÉ, reconstruction REFUSÉE, la balise scellée SURVIT à la
re-vérification — le registre des versions acceptées vit au code, plancher
0.7.0-dev.1). **Le chantier M6-(d) : LA PART LABORATOIRE EST ACCOMPLIE —
le chantier M5-(c) REFERMÉ au labo (05/11/2026, Entrée 148, D153)** : la
démonstration `unix/demo_patch.py` VERTE sur pièces sur l'artefact scellé
relu (la boucle d'écriture basculée ENTRE DEUX USAGES — tcp-07:R4 V5 ;
le journal cohérent OCTET POUR OCTET ; la bascule sous CONCURRENCE RÉELLE —
le qword d'atomicité Q3 posé pendant qu'un fil ouvrier journalise, les DEUX
formats constatés dans son trafic ; le rollback en pleine session ; le
retour à l'état image ; la zéro régression — le fichier n'a pas bougé d'un
octet, le rituel rejoué vert) — et la suite de conformité EXÉCUTE la
démonstration à chaque passage (l'élément 5 devenu contrôle RÉEL, toujours
VERTE 7/7 — 37 contrôles) ; **LE KIT TERRAIN AU COFFRE `/test`** (la vague
m6d : kit-m6d.zip — l'artefact + le scénario AUTONOME python3/ctypes, la
cartouche PRÉ-ASSEMBLÉE recoupée contre l'instrument de l'oracle octet
pour octet, relogée au terrain par un fixup imm64 unique — + LISEZMOI +
preuves-m6/ ; la vague e4 consommée archivée D143 ; le kit EXACT éprouvé
au labo PAR EXTRACTION VIERGE + RUN : VERT 16/16). **LE RUN DU DÉVELOPPEUR
EST VENU (05/11/2026, Entrée 149, D154) — LE JALON M6 FRANCHI** : la machine
du développeur (WSL2, la recommandation D149 suivie — le premier geste, lancé
sous Windows natif, était mort NOMMÉ AVANT T0 : `libc.so.6` introuvable, le
fail-closed tient hors terrain) a rendu son verdict **VERT 16/16** sur le
noyau `6.18.54.1-microsoft-standard-WSL2` — UN AUTRE noyau que celui du
laboratoire (5.10.134…), l'ASLR complet constaté (`randomize_va_space=2`), le
scellé relu `dd14195c…` avant tout geste ; les TROIS pièces renvoyées au
coffre `/test/preuves-m6/`, le RECOUP LABO **VERT 22/22** sur pièces croisées
(`scripts/recouper_run_m6d.py` : témoin ↔ journal ↔ verdict recoupés entre
eux, l'arithmétique recomptée — 800 + 400 == 1 200, 778 + 560 == 1 338,
14 890 o émis == attendus —, les constats vérifiés contre la SOURCE du
scénario, le noyau constaté distinct, l'artefact recalculé au geste même ; le
premier passage avait échoué NOMMÉ : le défaut était dans l'INSTRUMENT du
recoup, corrigé et rejoué — D154) ; **LA FINALE `0.7.0` SCELLÉE** au geste
même (`--sceller-final` : D146 adapté vert + cristallisation 10/10 +
conformité 7/7 — la suite EXÉCUTANT la démonstration M5-(c) — bascule
rc.1 → 0.7.0 dans frag-bld, verrou croisé 13/13, l'artefact INTACT — les
gardes vivantes : re-scellage REFUSÉ, reconstruction REFUSÉE, la balise
PRÉSERVÉE par la re-vérification). La clôture D143 des pièces du run (leur
déplacement vers `archives-preuves/preuves-run-m6d/` avec le verdict du
recoup) attend le dépôt du kit M7, modèle e4 ; les décisions développeur
(réserve qemu) demeurent non bloquantes.

**Le chantier M7-(a) RÉALISÉ — le 05/11/2026** (Entrée 150, D155) : **LE
MOTEUR DE NOTATION RV64 EST** — keystone ne porte pas l'ISA (constat
re-vérifié au geste même), l'assembleur **RV64IMA+Zifencei maison du
dépôt** (`riscv/outils/as_rv64.py` : six formats R/I/S/B/U/J, 4 o
exactement, SANS extension C, refus nommés fail-closed) assemble, et sa
preuve est une **PORTE** (`riscv/notation/porte_roundtrip.py`) : round-trip
**100 % en DEUX directions** — 783 textes du corpus du profil (AVANT :
assemble → désassemble → ré-assemble) + 1037 encodages légaux de l'espace
RV64IMA+Zifencei (INVERSE : le rendu INTÉGRAL du juge ré-assemble en ses
octets), **capstone 5.0.7 juge unique** (quatre leçons attrapées par la
porte au geste même : negw, funct7 des décalages W, jalr deux-opérandes,
fence « unknown » — D155). **qemu-riscv64 OPÉRATIONNEL au labo** (critère
de sortie du chantier) : l'installation est une PROCÉDURE du dépôt
(`riscv/outils/installer_qemu.sh`, extraction locale sans privilèges du
paquet qemu-user statique 10.0.13 — le binaire est un instrument
gitignoré, la procédure est la pièce). **La lignée `riscv/` née** (layout
D8 décliné — géométrie MIRROIR du plan unix, seul le demi-octet ISA
change : e_machine 0xF3, e_flags 0, instructions 4 o, NOP canonique
`addi x0,x0,0`, réserves `ebreak` ; table ERRNOS MÊME contrat ; syscalls
ASM-GENERIC avec **garde anti-table-x86** — a7=1 (write x86-64) est un
REFUS DE BUILD NOMMÉ, la parité est SÉMANTIQUE jamais lexicale) ;
**quatre specs écrites-avant-code** (`sr-01..sr-04`, le domaine `sr` —
les miroirs de su-01..04 : le contrat survit au portage, l'ABI change,
les ancres auipc+addi remplacent le lea rip, t1 remplace r10/r11, le
cadre de .emit SAUVE ra — jal ne pousse pas) ; la sonde construite par
`riscv/build_m7.py` : **120 instructions, round-trip 100 %, oracle
structurel 219 verrous** (appels/syscalls/données déclarés PAR BLOC,
paires d'ancres re-vérifiées depuis le code désassemblé, taille 4 par
instruction — garde anti-C, pile psABI appariée, t1 respecté, symboles
confrontés au layout — leçon C1), **ELF64 durci ET_DYN/PIE EM_RISCV**
(3 segments R/RX/RW, W^X depuis les phdr, PT_GNU_STACK sans X, 8 192 o,
sha256 d122bc68…), **l'oracle d'exécution SOUS QEMU VERT** (réserve
instrumentale D149 NOMMÉE : TCG, noyau et syscalls RÉELS) : 6/6 runs
conformes — quatre lignes octet pour octet (la base calculée par les
paires d'ancres en tête, a0 = fffffffffffffff7 → verdict 1 [EBADF nommé],
a0 = fffffffffffffff2 → verdict 6 [EFAULT hors table, VERDICT_FATAL,
arrêt propre], code de sortie 6) ; **la table ERRNOS exercée sur ses deux
branches**, la **falsification 12/12 zéro silence** ; **l'indifférence à
la base DÉMONTRÉE par bases forcées du CHARGEUR** (constat d'instrument
D155 : qemu 10 ne randomise PAS l'image PIE invitée — base par défaut
constante 0x555555556000 CONSTATÉE, -B seul sans effet, le levier est -R
la fenêtre de réservation : trois configurations VERTES à 0x2aaac000 /
0xaaaac000 / 0x55556000) ; la **carte génération 1** du jalon (QUATRIÈME
sel Argon2id distinct, clés projet partagées D27, signature Ed25519,
verrou croisé 4/4) + le tableau de bord ; la re-vérification complète
rejouée (cristallisation 2/10, R5/R8 verts) ; **la balise 0.8.0-dev.1
posée par le premier build du jalon** (geste de BUILD, jamais de
scellage — plancher 0x00080000).

**Le chantier M7-(b) RÉALISÉ — le 05/11/2026** (Entrée 152, D156) : **LE
CORPUS PARITAIRE RV64 — LA TROISIÈME INSTANCIATION DE LA MÊME COUCHE I** —
les DOUZE blocs du patrimoine (hello-02/03, libc-01..08, tcp-07/11) +
corpus-13, la notation RV64 native de 523 instructions (round-trip 100 %,
graphie canonique du juge) ; **l'instance charge LES MÊMES FICHIERS
CANONIQUES de unix/I/** (13 specs, empreintes mesurées, AUCUNE copie — le
diff nul VERT en 4 recoupements : canoniques, observables R1↔R+1 par la
chaîne M6 rejouée, 7 scellés octet-identiques à l'état zéro, parité § 8.3)
; **GÉOMÉTRIE MIROIR du plan unix** (D8 : les MÊMES RVA, les MÊMES
fixtures, f71xxxx à la série du corpus) ; **QUATRE LEÇONS DU GESTE**
(D156 : LA LEÇON imm12 — le verrou 0x3800 vu de la base .bbs vivait à
+0x800 hors plage DE UN, la fenêtre s'est posée AU CENTRE 0x3400 ; le
PIÈGE AMO — l'ISA AMO adresse [rs1] SANS déplacement, refus nommé, le
déplacement vit dans la formation déclarée ; le RECYCLAGE s3 — dédié par
rôle, la fenêtre de tcp-07 n'est pas l'ardoise de tcp-11 ; LA PORTE A
GRANDI — l'extension A amoswap entre à la porte 791 + 1045 aux deux
directions) ; **l'oracle qemu VERT SUR PIÈCES** (réserve D149) : le
rituel de parité 6/6 — les DEUX lignes octet pour octet (« TRIADE M1 :
minilibc 21/21 OK\n » puis « corpus : autotest 21 vecteurs\n ») code 0
— **LA PARITÉ § 8.3 PAR EXÉCUTION sur les TROIS profils** ; les bases
forcées du CHARGEUR VERTES ; la falsification 13 mutations 12/12 blocs
rompus (zéro silence ; tcp-07 hors-chemin du rituel, son scénario est le
chantier (c)) ; **1535 verrous structurels** (la garde anti-table-x86
vivante : write 64, mprotect 226, exit_group 94 asm-generic) ; l'artefact
`riscv/corpus` 12 288 o sha256 b34a7147… DÉTERMINISME constaté au
rebuild ; la carte génération 1 au SIXIÈME sel (frag-con TROIS PROFILS
par bloc — la TROISIÈME colonne psABI est née, § 8.3-4) ; la
re-vérification rejouée (cristallisation 2/10) ; **la balise 0.8.0-dev.2
posée par le build du corpus** (geste de BUILD — le scellage 0.8.0-rc.1
viendra du chantier (c) avec le contrôle D146 adapté à l'exécuteur).

**Le chantier M7-(c) RÉALISÉ — le 05/11/2026** (Entrée 153, D157) : **LE
PATCH fence.i + LE VERROU MULTI-PROFILS + LE SCELLAGE 0.8.0-rc.1** — LA
SÉQUENCE scratch+fence.i DÉMONTRÉE EN EXÉCUTION sous qemu par LE
DÉMONSTRATEUR INVITÉ `riscv/demo` (f72001, 191 instructions à 0x2000 dans
la réserve RX — l'image porte les MÊMES blocs du corpus + le
démonstrateur ; le modèle unix/demo_patch.py PORTÉ EN INVITÉ) : la bascule
pendant le trafic — **1 200 usages de l'ENTRÉE du journal, l'apply ENTRE
les usages 399/400, le rollback entre 799/800, la transcription byte-exact
(15 425 o), 800 lignes v1 + 400 v2 (marque j2:), l'effet au geste même
(j2: verdict / verdict), le retour à l'état image, les refus nommés 1-4
(l'absent et la somme par mutation IN-GUEST de la table), le DEP falsifié
(SIGSEGV, 4 290 o exacts), la falsification du démonstrateur, les bases
forcées, zéro régression** ; LA CORRECTION tcp-07 (D157 : le PORT avait
oublié le marshalling du prot — `mv a2, t2`, nommé au premier apply, la
pièce par QEMU_STRACE ; le corpus REBUILDÉ sha ec343b4e…) ; LE VERROU
CROISÉ MULTI-PROFILS VIVANT (26 empreintes des DEUX ISA avant l'édition,
la géométrie miroir, la couche I partagée) ; LE CONTRÔLE D146 ADAPTÉ
(base réelle CONSTATÉE PAR TRACE in_asm — 0x555555556000 ×6 + 3 forçages
distincts) ; LA CONFORMITÉ § 8.2 VERTE 7/7 (29 contrôles) ; LA
CRISTALLISATION 10/10 ; **SCELLAGE 0.8.0-rc.1** (D146 + multi-profils +
R6 + 7/7, la bascule dans frag-bld, l'artefact INTACT — le scellage est
un fait de carte) ; **LES TROIS GARDES VIVANTES** (re-scellage et
reconstruction REFUSÉS, la re-vérification PRÉSERVE la balise).

**Le chantier M7-(d), LA PART LABORATOIRE RÉALISÉE — le 05/11/2026**
(Entrée 154, D158) : **L'EXPORT DE CONTINUITÉ MULTI-PROFILS VERT DE BOUT
EN BOUT** (`riscv/export_continuite.py`, le premier export depuis M1 —
D16/FORMAT_CARTE § 8 aux TROIS profils déclarés) : le conteneur TRIADE-EXP1
729 277 o CHIFFRÉ (XChaCha20-Poly1305, Argon2id sur un sel DÉDIÉ à
l'export puis HKDF) + SIGNÉ (Ed25519, la lignée D27) portant 126 fichiers —
81 spécifications I (m0..m5, les canoniques unix/I, les miroirs riscv/I),
CINQ artefacts B (m5/proxy.exe 0.6.0, unix/sonde + unix/corpus 0.7.0,
riscv/sonde + riscv/corpus 0.8.0-rc.1), les CINQ cartes C de l'ère courante
; **l'import AUTO-PORTANT aux CINQ étapes § 8.2** — la table de géométrie
par artefact et les paramètres publics de dérivation par carte vivent AU
MANIFESTE chiffré+signé (l'import ne doit au dépôt QUE la clé publique) ;
le verrou croisé : 34 empreintes de blocs (les DEUX ISA) + 5 artefacts
entiers recoupés aux frag-bld ; **la preuve d'exécution de bout en bout** :
les rituels rejoués sur les octets TRANSPORTÉS (corpus unix natif, corpus
riscv sous qemu — les DEUX lignes code 0 ; le scellé win : frontière
nommée, son rituel vit au poste Windows) ; l'export POUSSÉ au coffre Drive
racine « Triade » ; **LE KIT TERRAIN M7 ASSEMBLÉ ET ÉPROUVÉ** (D153 :
extraction vierge + run au labo — VERT 16 PASS / 0 ÉCHEC) : le scellé
riscv/corpus + le démonstrateur riscv/demo + **l'INSTRUMENT EMBARQUÉ**
qemu-riscv64 10.0.13 STATIQUE (md5 consigné — aucun paquet, aucun réseau,
aucun root) + le scénario PRÉ-ASSEMBLÉ (constantes FIGÉES du plan, chaînes
recoupées PAR AST, site DEP par désassemblage, 191 adresses) ; **LA
CLÔTURE D143 DU RUN m6d FAITE** (la vague m6d archivée dans
archives-livraisons/vagues-m6/ ; les pièces du run dans
archives-preuves/preuves-run-m6d/ AVEC le verdict du recoup labo — Entrée
149 ; les deux index mis à jour) ; preuves-m7/ NÉ au coffre, la vague m7d
DÉPOSÉE (kit-m7d.zip + LISEZMOI-m7d.txt). **LE SCELLAGE 0.8.0 ATTEND LE
RUN TERRAIN DU DÉVELOPPEUR** (modèle m6d : le kit → le run sur sa machine
→ le recoup sur pièces → --sceller-final) — TROIS leçons D158 (le bit
exécutable de l'image invitée EXIGÉ par qemu-user et rétabli geste nommé ;
les cartes d'ère passée ne se transportent pas ; les lignées homonymes se
chargent par chemin absolu).

**LE CHANTIER M7-(d) ACCOMPLI, LE JALON M7 FRANCHI — le 05/11/2026**
(Entrées 154/155, D158/D159) : **LE RUN TERRAIN VERT SUR PIÈCES** — le kit
m7d exécuté par la machine du développeur (WSL2, noyau
`6.18.54.1-microsoft-standard-WSL2` — UN AUTRE noyau que celui du
laboratoire, l'INSTRUMENT EMBARQUÉ du kit qemu-riscv64 10.0.13 statique
md5 `bae5a36f…`, le scellé relu `ec343b4e…` avant tout geste, la réserve
D149 NOMMÉE) : **16 PASS / 0 ÉCHEC, VERDICT : VERT** — le même verdict que
l'épreuve d'extraction vierge du labo ; **LE RECOUP LABORATOIRE VERT 29/29
SUR PIÈCES CROISÉES** (rapatriement md5 contrôlés par pièce + recoup :
les pièces recoupées ENTRE ELLES, l'arithmétique RECOMPTÉE DEPUIS LA
SOURCE — le générateur déterministe importé, l'attendu re-généré au geste
même — le noyau constaté distinct, les artefacts recalculés, le kit du
coffre == le kit éprouvé ; le premier passage a échoué nommé : trois
défauts d'INSTRUMENT, corrigés et rejoués, les pièces immuables) ; **LA
FINALE 0.8.0 SCELLÉE** (`--sceller-final` né au geste, modèle unix/m6d :
verrou multi-profils AVANT l'édition + contrôle D146 adapté +
cristallisation 13×10/10 + conformité 7/7 au geste même + bascule
rc.1→0.8.0 occurrence unique + l'ARTEFACT INTACT — le scellage est un fait
de carte ; les trois gardes vivantes constatées) ; **L'ÉVÉNEMENT DE
REPRISE D159** : le poste de laboratoire restauré à l'instantané M6-(c) en
ouverture du geste, l'intégralité du jalon retrouvée aux MIROIRS (GitHub —
la pointe consignée D141 ; le coffre Drive — kit et pièces), la reprise
par fetch + reset à la pointe consignée, l'instrument réinstallé par sa
procédure (md5 IDENTIQUE) — rien de perdu ; **LA CLÔTURE D143 DU RUN m7d**
: les pièces à archives-preuves/preuves-run-m7d/ AVEC le verdict du
recoup labo (l'archive porte le jugement avec les pièces), preuves-m7/
demeure le réceptacle, la vague m7d demeure la vague courante (aucun kit
M8 annoncé, rien ne se jette) ; FRONTIÈRES : l'export de continuité au
coffre demeure celui du geste lab (0.8.0-rc.1, daté — les artefacts
intacts, l'export 0.8.0 naîtra d'un geste dédié si demandé) ; le terrain
natif Windows n'exécute pas l'instrument du kit (binaire Linux statique —
WSL2 le terrain attendu). **LE PROGRAMME M6/M7 (D149) EST ACCOMPLI : les
chantiers d'après M7 (bloc optionnel de syscalls directs, TLS 1.3 pur en
blocs scellés, profils additionnels) attendent la décision du
développeur.**
**La décision est VENUE le même jour (« continue ») : l'ère d'après M7 est
OUVERTE — D160, Entrée 156, la section « Programme d'après M7 » ci-dessous ;
l'export de continuité 0.8.0 a refermé l'ère M6/M7 proprement avant
l'ouverture.**

| Chantier M6 | Contenu | Critère de sortie mesurable |
|---|---|---|
| (a) Le durcissement format — l'ELF64 du jalon | le writer du jalon (`unix/build_m6.py`, modèle `m6/build_ah.py`) porte l'image à ET_DYN (PIE, base aléatoire), trois segments R/RX/RW, PT_GNU_STACK sans X ; table ERRNOS (contrat d'erreurs des syscalls, miroir de la table HRESULTS) ; layout `unix/layout.py` (modèle D8) | un ELF64 durci minimal exécuté au labo, l'image PIE chargée par le noyau à une base aléatoire CONSTATÉE ; W^X vérifié depuis les phdr ; round-trip 100 % |
| (b) Le corpus paritaire — le diff nul sur I | audit de couplage des contrats candidats (classés A : instanciables tels quels / B : révision de granularité / C : couplés à l'OS) ; révision R+1 des contrats B au niveau FORMEL (arguments nommés, convention d'appel déplacée vers frag-con — spécification § 8.3-4), invariance des octets Windows ASSERTÉE (les scellés ne bougent pas), sceau de l'Intention suivi pour les arbres I modifiés (cérémonie, modèle D87) ; instanciation SysV du corpus nominal : les SEPT blocs purs `libc-01..07` + `libc-08` autotest + `tcp-07` moteur de patch + `tcp-11` journal + les DEUX contrats d'interface (écrire/sortir — les révisions formelles de hello-02/hello-03) + un principal propre au jalon (domaine neuf, modèle ah-09) | le diff nul MESURÉ PAR SCRIPT (les instances des deux profils chargent les MÊMES fichiers I, empreintes identiques) ; l'oracle m1 régénéré VERT sur l'instance Linux (exécution native au labo) ; parité § 8.3 par exécution (verdicts de vecteurs équivalents, frag-con documenté par bloc) |
| (c) La suite de conformité + le scellage | `unix/conformite_profil.py` (modèle `m5/conformite_profil.py`) : les SEPT éléments constatés depuis l'artefact, jamais déclarés ; porte R10 déclinée ELF ; anti-rollback LICENSE (plancher 0.7.0-dev.1) ; cristallisation ; scellage `0.7.0-rc.1` avec le contrôle D146 adapté (exécution full-ELF à la base réelle — l'image PIE au noyau : un pointeur nu y meurt exactement comme sur le terrain, l'émulation à base fixe reste interdite comme témoin unique) | suite VERTE 7/7 ; scellage rc.1 avec contrôle D146 exécuté AU scellage (modèle D147) ; gardes vivantes (re-scellage et reconstruction refusés) |
| (d) Le patch en production + le terrain — le chantier M5-(c) refermé | le moteur de patch `tcp-07` instancié (mprotect) et EMBARQUÉ : bascule du bloc journal PENDANT le trafic (la boucle d'écriture), journal cohérent, rollback démontré, zéro régression — LE critère M5-(c) sur le profil Linux ; kit terrain Linux (artefact + scénario + LISEZMOI) au coffre `/test`, run sur la machine Linux du développeur (WSL2 recommandé — D149), preuves renvoyées, verdict sur pièces (D138/D145/D148) ; si vert : `--sceller-final` pose `0.7.0` | patch pendant le trafic + rollback + zéro régression démontrés sur pièces (suite de conformité verte, l'élément 5 EMBARQUÉ) ; run terrain VERT sur pièces → balise finale `0.7.0`, jalon M6 franchi |

| Chantier M7 (après M6) | Contenu | Critère de sortie mesurable |
|---|---|---|
| (a) Le moteur de notation RV64 | CONSTAT LABO 04/11 : keystone 0.9.2 ne porte PAS le RISC-V, capstone 5.0.7 désassemble RV64 — livrable : l'assembleur RV64IMA+Zifencei maison du dépôt (formats R/I/S/B/U/J, 4 o) OU un moteur tiers passé à la même porte ; installation de qemu-riscv64 (absent du bac à sable au constat, re-vérifié avant usage) | round-trip 100 % sur le corpus d'instructions du profil (capstone juge unique) ; qemu-riscv64 opérationnel au labo |
| (b) L'instanciation — la troisième couche | re-vérification des constats de la fiche `docs/PROFIL_riscv64-linux-elf64.md` ; le MÊME corpus que M6 (troisième instanciation de la même couche I) ; table de syscalls asm-generic avec garde anti-table-x86 (write=1 est un refus nommé) | diff nul mesuré par script (mêmes fichiers I) ; oracle VERT sur l'instance RISC-V (exécution qemu) ; parité § 8.3 sur les TROIS profils |
| (c) Le patch `fence.i` + le verrou multi-profils | séquence scratch + `fence.i` démontrée en exécution (écriture alignée atomique, rollback) ; verrou croisé multi-profils (empreintes des blocs des DEUX ISA vérifiées avant chaque édition, R8 étendue) | suite de conformité VERTE 7/7 (élément 5 : patch conforme au profil) ; verrou croisé multi-profils vivant |
| (d) L'export multi-profils + le terrain | export de continuité chiffré + signé portant les couches I/B des profils — importé et vérifié de bout en bout aux CINQ étapes (§ 6 du manuel : déchiffrer, signature, verrou croisé, oracle régénéré, reprise) ; kit terrain (qemu-riscv64 — réserve instrumentale D149 NOMMÉE dans chaque verdict) ; si vert : finale `0.8.0` | export → import → reprise SANS écart ; run terrain VERT sur pièces → balise `0.8.0`, jalon M7 franchi — l'universalité DÉMONTRÉE : chaque profil déclaré supporté a franchi ses critères |

**Frontières du programme, nommées.** Le corpus nominal M6 est RESTREINT
(minilibc + interface + moteur de patch + journal + principal) : le serveur écho
complet de M2 (contrats tcp d'interface socket, tcp-01..06/08..10/12) N'EST PAS
instancié au jalon — le critère § 18-M6 (diff nul, même oracle, parité) se
démontre sur le corpus nominal, et l'extension au corpus réseau est un chantier
OUVERT, à la demande du développeur, jamais une réduction silencieuse. Les
constats labo (keystone sans RISC-V, capstone RV64 OK, qemu absent) sont datés et
re-vérifiés au chantier qui les touche.

**Décisions du développeur attendues** (nommées, aucune ne bloque le démarrage de
M6-(a)) : (1) le terrain M6 — WSL2 (recommandé : noyau Linux complet sur la machine
Windows 11, aucun outil nouveau) ou VM Linux isolée (lignée des runs e*) ;
(2) le terrain M7 — qemu-riscv64, l'émulation de processus étant la réserve
instrumentale consignée (aucune fer RISC-V) ; (3) l'aval du report du chantier
M5-(c) dans M6-(d) (D149 le consigne — le critère sera démontré sur le profil
Linux, moteur de patch embarqué).

## Programme d'après M7 — les additions mesurées (ouvert le 05/11/2026, D160)

La demande « continue » du développeur au lendemain de la finale 0.8.0 EST la
décision d'ouverture (D160, le modèle D149). L'ordre des familles est LA
FONDATION D'ABORD — chacune s'appuie sur les résultats MESURÉS de la
précédente : **(1) le jalon M8, le bloc optionnel de syscalls directs** (OUVERT
— la lignée m8/, le domaine `sys` créé au registre figé, la charte à huit
règles, la couche I écrite-avant-code livrée) ; **(2) TLS 1.3 pur en blocs
scellés** (la grande œuvre de la souveraineté complète — HORS PÉRIMÈTRE jusqu'à
sa décision propre d'ouverture : elle s'appuiera sur le domaine sys, la
fondation I/O) ; **(3) les profils additionnels** (`aarch64-macos-macho`,
`wasm32-wasi` — HORS PÉRIMÈTRE : chacun répétera M6/M7 sur résultats mesurés).
L'ère a été refermée PROPRE avant l'ouverture : l'export de continuité 0.8.0
(le conteneur régénéré porte la carte 0.8.0 scellée, import à sec + rituels
VERTS sur les octets transportés, la copie au coffre racine — Entrée 156).

| Chantier M8 (win, l'ère 0.9.0) | Contenu | Critère de sortie mesurable |
|---|---|---|
| (a) La couche I du domaine `sys` | écrit-avant-code (D77) : la charte des syscalls directs à HUIT règles + les spécifications sys-01 (l'émetteur — le trombone ABI, aucun prologue), sys-02 (le résolveur SSN — l'EAT de ntdll LUE, jamais appelée), sys-03 (la twin de hello-02 par NtWriteFile, zéro IAT) ; le plan d'adressage né (m8/layout.py : .text5 préfigurée, MOTIF_STUB/PE/EAT en source unique, la table des SEPT verdicts, les versions 0.9.0) | **RÉALISÉ le 05/11/2026** (Entrée 156, D160) : le registre figé étendu (`sys`, M8), le contrat précède l'octet |
| (b) Les blocs notés-mesurés-prouvés | la notation à la main (auteur.py), le round-trip, le harnais différentiel sur FIXTURES ntdll synthétiques (le labo ne connaît pas le SSN du terrain et ne le devine jamais — le motif vérifié avant l'extraction), la falsification (zéro silence) | **RÉALISÉ le 05/11/2026** (Entrée 157, D161) : round-trip 100 % + concordance au plan (12/12 et 4/4 immédiats) ; le harnais **61 contrôles · 61 VERTS** sur TROIS graines (l'émetteur au noyau simulé — la pile de l'appelant lue à [rsp+0x28], I3 ; le résolveur : la marche bornée, les SIX refus nommés, le motif AVANT l'imm32 ; **la twin : la MÊME ligne par les DEUX chemins octet pour octet** — la preuve d'observable) ; les QUINZE mutations de falsification ATTRAPÉES, les témoins intacts verts ; l'arrêt D161 des slots sur les longueurs réelles (0xA000/0x40, 0xA040/0x140, 0xA180/0xC0) et les fixtures .rdata dans la zone vierge (nom @0x2EC0, ligne @0x2ED0, borne @0x2F00) |
| (c) Le build 0.9.0-dev.1 + la carte | la composition .text5 sur le corps 0.6.0 INTACT (R7 — deltas PE documentés, modèle D94/D136), l'oracle structurel AVEC la règle du domaine (AUCUN IAT PAR BLOC sys — la preuve structurelle), la carte génération 8, la balise 0.9.0-dev.1 (geste de BUILD, jamais scellage) | l'oracle VERT (la règle AUCUN IAT constatée sur les octets) ; la carte signée, verrou croisé étendu ; le scellé 0.6.0 byte-identique au corps |
| (d) Le terrain — le VRAI ntdll | le kit au coffre `/test` (l'artefact + le scénario : le run lit le VRAI ntdll de la machine du développeur, le motif confronté, la ligne comparée — la version Windows consignée au témoin) ; le run, les preuves au coffre, le recoup sur pièces (D138/D145/D148) ; si vert : la finale `0.9.0` | run terrain VERT sur pièces → balise finale `0.9.0` — le second chemin preuve : la même observable SANS un seul import, sur la machine du développeur |

**Frontières du programme d'après M7, nommées.** La clause spec « hors périmètre
courant » est LEVÉE NOMMÉMENT pour la seule première famille (D160) ; la
PEB-walk (trouver ntdll sans IAT — l'IAT-free du principal) et la
contre-mesure du hooking (stubs crochetés) sont des CHANTIERS FUTURS NOMMÉS :
en l'état, la base est FOURNIE par l'appelant et un stub divergent est un
REFUS nommé — le résolveur ne devine jamais, il ne s'adapte jamais en silence.

## Le projet fils COFFRE-FORT (fondé D135, 31/10/2026 — développement différé)

Le coffre fort dispose désormais de son PROPRE dépôt
(github.com/alexisfrlopez-debug/coffre-fort), de son PROPRE dossier Drive
(« Coffre-Fort », frère du dossier « Triade »), de son PROPRE plan des jalons
(M0-M6 : acte fondateur, détachement, profils d'application, commutateur
d'homme mort, succession post-mortem, durcissement par domaine, passation
v1.0) et d'instructions de reprise auto-suffisantes — l'analyse fondatrice du
développeur (journalisme et lanceurs d'alerte, finance de haute sécurité,
défense et infrastructures critiques, héritage numérique) y est citée
integralement. RIEN du code TRIADE n'y est forké : le chantier s'ouvrira sur
UN MESSAGE du développeur, au bouclage de TRIADE. Le père continue sa route
sans ralentir — la fondation du fils n'emprunte rien au jalon M5 ni aux
suivants ; toute dépendance vivante entre les deux dépôts serait un défaut
à consigner. Le plan détaillé vit au FILS (docs/PLAN_MILESTONES.md du dépôt
coffre-fort) ; la fondation est consignée D135 / Entrée 123 du présent dépôt.
