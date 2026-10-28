# TRIADE — Développement logiciel en code machine par agent IA

Protocole et outillage permettant à un agent IA de développer, vérifier et mettre à jour
des logiciels **100 % code machine natif**, sans compilateur ni langage de programmation,
grâce à une **Carte** de balises signée, chiffrée et fragmentée qui relie les intentions
aux octets. Ce que l'agent écrit est ce qui s'exécute — et rien d'autre.

Le protocole est **universel depuis la v0.3** : toute plateforme / OS / architecture est
un profil de cible vérifiable (profil primaire de validation : x86-64 / Windows 11,
PE32+ écrit à la main). La suite cryptographique est paramétrable par le développeur
(hachage SHA-256 par défaut, listes blanches), et l'**export de continuité** chiffré
permet de sauvegarder et transférer l'état de développement vers n'importe quel agent
conforme TRIADE.

## Licence

Le dépôt est sous **Business Source License 1.1** (D84, 28/10/2026) — concédant :
**Alexis Lopez**. Usage, copie, modification et redistribution autorisés **hors
production uniquement** jusqu'à la Change Date (**2030-10-28**), où l'œuvre
passe sous **GPL v3.0 ou ultérieure**. Tout usage en production (notamment par
ou pour le compte d'un employeur ou de toute entité commerciale) exige une
licence commerciale écrite du concédant. **Exclusions** (aucun droit concédé) :
`.keys/`, conteneurs de coffre-fort, `PHRASE-CONTROLE-COFFRE.txt`, `.gdrive/`
et tout jeton — cf. `LICENSE`. La barrière juridique complète la barrière
cryptographique du programme v0.6.0 (D85–D87 : attestation de non-exfiltration,
interrupteur d'homme mort Shamir, filigrane hors-ligne de la couche I).

## Priorités (non négociables, arbitrage lexicographique)

**Sécurité > Performance > Optimisation > Coût en tokens** — un objectif n'est jamais
sacrifié au profit d'un objectif de rang inférieur.

## Points d'entrée selon votre rôle

| Vous voulez... | Lisez |
|---|---|
| Reprendre le projet là où il s'est arrêté | `REPRISE_PROJET.md` |
| Démarrer un nouveau projet logiciel avec un agent IA | `PROTOCOLE_TRIADE_AGENT.md` |
| Consulter la spécification complète | `docs/PROTOCOLE_TRIADE.md` (v0.5.2, source de travail) — `docs/Protocole_TRIADE_v0.5.2_Specification.pdf` (archive formelle v0.5.2 : garde durable de la phrase de contrôle D81, menace du vol du coffre étendue § 13.1, M4 ouvert constaté D77 — D81) ; archives conservées : v0.5.1, v0.5.0, v0.4.0, v0.3, v0.2 ; vérification : `scripts/spec_v052/verify_spec.py` (cahier V1–V12) |
| Consulter la démonstration | `docs/Protocole_TRIADE_v0.3_Demonstration_RoomEq.pdf` (22 p.) — le protocole démontré par le recodage complet de RoomEq sous TRIADE : 42 modules, 437 tests, parité v2.2.2, comparatifs de code avant/après |
| Lire l'édition académique | `docs/Protocole_TRIADE_v0.4_Article_Recherche.pdf` (12 p., D18) — le protocole et son étude de cas restructurés en article de recherche IMRAD : formalisation (verrou croisé, ordre lexicographique), travaux connexes, menaces sur la validité ; vérification interne : `docs/VERIFICATION_v0.4_Article.md` |
| Comprendre le format de la Carte | `docs/FORMAT_CARTE.md` |
| Consulter les arbitrages | `docs/DECISIONS.md` (D1–D50 formalisées, format normalisé depuis D24 ; D51–D81 au fil des messages de commit et de `docs/JOURNAL_TRAVAIL.md`, Entrées 40–70) |
| Voir la feuille de route | `docs/PLAN_MILESTONES.md` (M0–M7) |

## Sauvegarde et continuité

Règle absolue — après **chaque** modification du projet :

```bash
bash scripts/sync_backup.sh "description courte de la modification"
```

Le script régénère d'abord le PDF formel si les sources du protocole ont changé (D17 :
`scripts/build_pdf.sh`, empreinte des sources comparée au stamp du dernier build),
committe, synchronise le miroir Google Drive (fichiers + bundle d'historique)
et pousse vers le repo GitHub privé. Le hook `post-commit` synchronise le Drive à chaque
commit. Vérification des jetons : `python3 scripts/check_auth.py`.

**Coffre-fort des phrases maîtresses (D75, ROTÉ D80, phrase de contrôle sous garde durable D81).** Toutes les phrases maîtresses du projet
— et de tout futur projet conduit sous TRIADE — vivent dans un conteneur unique chiffré
TRIADE-CF1 (`python3 coffre_fort.py` à la racine) : Argon2id + HKDF à
contexte dédié + XChaCha20-Poly1305, autotest de falsification (`python3 coffre_fort.py
autotest`). Le conteneur est exporté chiffré au racine du coffre Drive (copie projet) et
au coffre personnel du développeur ; après une réinitialisation du poste, `importer` +
`obtenir TRIADE lignee-D80 --vers-fichier .keys/passphrase.txt` restaurent la lignée
sans cérémonie. **D80 (rotation de lignée après exposition D76-D78)** : le conteneur
porte les DEUX lignées — `lignee-D74` (archive, « ne plus sceller avec ») et
`lignee-D80` (courante) ; la phrase de contrôle D75 est INOPÉRANTE. **D81 (garde
durable, consigne développeur)** : la phrase de contrôle courante vit dans
`PHRASE-CONTROLE-COFFRE.txt` (racine du dépôt + GitHub + miroir Drive + racine du
coffre Drive) — sauvegardée AVANT TOUTE AUTRE ACTION dès production, le fichier EST la
remise ; elle ouvre le conteneur (prouvé, restauration post-panne démontrée de bout en
bout — cf. `LISEZMOI-PHRASE-CONTROLE.txt`).
Format normatif : `docs/FORMAT_CARTE.md` § 11 ; discipline : spécification v0.5.2 § 15.3.

## État du projet

Conception terminée et **gouvernance vérifiée** (spécification v0.4.0 : couche I normalisée,
taxonomie des défauts T1–T6, R10 renforcée, R11 ajoutée, conformité par profil, traçabilité
I↔C↔B↔tests et tableau de bord — née des pratiques du recodage RoomEq), infrastructure de
sauvegarde opérationnelle. **Jalon M0 franchi le 26 octobre 2026** (D26) : chaîne
notation → octets → PE32+ → exécution prouvée sans compilateur — hello.exe (1 536 o,
sha256 c89e330c…), carte v0 signée Ed25519, verrou croisé fail-closed, exécution
constatée sur Windows 11. **Jalon M1 franchi le 26 octobre 2026** (D27–D32) —
mini-libc de sept blocs + autotest dans `selftest.exe` (9 216 o, sha256 8038585b…),
réutilisation inter-artefacts octet-identique des blocs io M0 (R7 démontrée), oracle
différentiel Unicorn 76 010 cas/exécution, cristallisation 11×10/10, suite de
conformité du profil verte (68 contrôles), budgets tokens mesurés (localiser 51/64,
éditer 719/3 000, ajouter 1 088/6 000 — D31), export de continuité chiffré au coffre
(D16) ; validation terrain Windows 11 constatée (ligne unique `TRIADE M1 : minilibc
21/21 OK`, D32) — **balise finale `0.2.0` scellée, immuable**. **Jalon M2 franchi
le 27 octobre 2026** (D33–D43) — boucle § 5 (patch à chaud en production +
rollback) DÉMONTRÉE sur machine réelle (journal terrain demo.8, 28/28 lignes
jusqu'à « DÉMO OK »), huit classes de défauts invisibles nommées et corrigées
(D35–D42), **balise finale `0.3.0` scellée, immuable**. **Jalon M3 franchi le 28 octobre 2026** (D45–D74) — entrées non fiables : harnais de
fuzzing à propriétés P1-P5 livré et falsifiable, 101 000 cas sans crash sur la surface scellée (D45) ;
couche I écrite avant le code — treize spécifications du domaine http
(D46, `m3/I/`) ; **proxy.exe scellé 0.4.0-dev.1** (D47 — étape (b) : oracle
à scénarios 153 036 cas verts, carte génération 5 sur 4 artefacts, R7 :
13 blocs octet-identiques M0/M1/M2) ; **étape (c) validée terrain 6×**
(D64–D71 : T2 du superviseur — proxy 0.4.0-dev.2 scellé D63, oracle
153 036 cas verts — vert à chaque run complet) ; **étape (d) ACCOMPLIE
(D72) : campagne million** — 1 000 000 cas SANS CRASH en 175 s sur le
périmètre parseur D46 (harnais `m3/fuzz_million.py` falsifiable :
deux mutations d'un octet du proxy scellé détectées ; 900 000
différentiels http-01..09 + 100 000 requêtes http-10 à propriétés
P1-P5, 200/200 sentinelles ; re-exécution à graine neuve identique —
2 × 10^6 cas cumulés ; rapport `m3/rapport_million.json`) ; **étape (e)
ACCOMPLIE (D73) : le fuzzing rejoint la conformité** — suite de conformité
§ 8.2 livrée (`m3/conformite_profil.py`, 161 contrôles : éléments 1-7
constatés depuis proxy.exe + contrôle de jalon « fuzzing à propriétés »
10^4 cas SANS CRASH à chaque exécution — harnais D72 réutilisé intégralement,
graine datée reproductible, auto-test de falsification inclus ; suite VERTE,
re-exécution à graine neuve identique ; `conformite.txt` lu par le tableau
de bord — le harnais million devient sentinelle perpétuelle de chaque
cristallisation rc/future, § 8.2/§ 9) ; **cristallisation et scellage
final (D74) : balise `0.4.0` scellée, immuable § 9** — 19 vérifications
graines 1-19 → 38/38 blocs à 10/10 (l'asymétrie R6 de l'héritage non
embarqué corrigée au passage, modèle journal 18 m2), 0.4.0-rc.1 puis
0.4.0 sur la validation terrain consignée (T2 6×, D64-D71) ; la lignée
de clés régénérée dans la session (4e réinitialisation, D27/D30
réappliquées) avec preuve de continuité byte-identique : proxy.exe
régénéré md5 dd12b649… égal au scellé D63 — le scellage est un fait de
carte, l'artefact n'a pas bougé d'un octet.
**Lignée terrain (D48–D71)** — `superviseur.exe` terrain.16 : le
harnais du terrain « 1 seul exe qui contient tout » (demo.exe,
proxy.exe et annexe de jetons EMBARQUÉS, section .blob), TOUS les
tests en 1 clic — T1 démo rejouée sans main humaine, T2 proxy
traversé par curl, T3 journal téléversé automatiquement ; **T3
DÉMONTRÉ de bout en bout sur machine réelle le 28/10 (D71, run 16 :
le journal `terrain_20261028_065408.txt` est parti TOUT SEUL dans le
dossier test)** — seize générations pour nommer et corriger les
tueurs de runs (ABI shadow space D62, pile proxy D63, --fail D65,
nettoyage du jeton D68, JSON indenté Google + HTTP/2 D69, tampon de
composition D70) ; T1 inchangé : D57 — exit 0xC0000005 de demo.9
publique, 5e reproduction, adresse de plantage attendue via WER.
**M3 est clos : balise finale `0.4.0` (D74)** — les cartes m0/m1/m2/terrain
restent chiffrées à l'ancienne lignée de clés (illisibles depuis la
restauration D71, état préexistant) : relève par l'ancienne phrase du coffre
développeur ou cérémonies de reconstruction byte-identiques (modèle D74) ;
la NOUVELLE phrase maîtresse de la lignée courante est au coffre du
développeur depuis la fin de session D74. **Composant transversal (D75) : coffre-fort
des phrases maîtresses** — conteneur chiffré TRIADE-CF1 (`coffre_fort.py`, spécification
v0.5.1 § 15.3 + FORMAT_CARTE § 11), autotest de falsification 19/19, phrase de contrôle
remise au développeur par cérémonie ; la phrase courante (lignée D74) y vit, export chiffré
au racine du coffre Drive + copie développeur ; l'ancienne phrase D30 doit y être ajoutée
côté développeur (`ajouter TRIADE lignee-D30`) — D78 : le reliquat Drive « phrase
maitresse triade.txt » ne portait PAS D30 mais la phrase COURANTE (preuve croisée :
octet-identique à `.keys/passphrase.txt`, déchiffre la carte m3, échoue sur m2 ;
l'audit D76 avait comparé le fichier entier au lieu de la ligne phrase) — phrase
active exposée ≈ 64 min sur le dossier partagé par lien (dépôt manuel 09:38:44 UTC,
corbeille 10:42), graine Ed25519 jamais exposée, copies claires locales détruites ;
**D80 : ROTATION DE LIGNÉE EXÉCUTÉE** — la phrase D74 est retirée du service,
lignée D80 opérationnelle, **carte m3 re-scellée à faits strictement inchangés**
(quatre fragments clairs octet-identiques, même graine Ed25519 donc même cle
publique, version 0.4.0 inchangée, proxy.exe inchangé dd12b649… ; re-vérification
graine 21 verte : R5 38/38, oracle 524 verrous + 153 036 cas, R8 38), coffre-fort
roté aux DEUX lignées (lignee-D74 archive + lignee-D80 courante, phrase de
contrôle D75 inopérante) ; côté développeur : VIDER la corbeille Drive (hygiène —
la phrase exposée est retirée du service, la copie y vit encore 30 j). **D81 : la phrase
de contrôle passe sous garde durable** — PHRASE-CONTROLE-COFFRE.txt au racine du dépôt
(commit dédié AVANT TOUT, GitHub + miroir + racine Drive, md5 vérifiés), le fichier est
la remise (l'affichage unique de cérémonie cesse d'être le canal de survie — la session
morte de D80 avait laissé la phrase D80 remise à personne dans le bac à sable) ;
spécification v0.5.2 (§ 1.6, § 13.1 menace étendue — confidentialité au repos = contrôle
d'accès au dossier Drive, mitigation première : restreindre le partage par lien —, § 15.3,
§ 17.6, cahier V1–V12, PDF QA 12/12) ; restauration post-panne prouvée de bout en bout.
**Coffre Drive nettoyé (D76)** : douze
livrables périmés archivés dans le sous-dossier `ARCHIVE/` de la racine (avec
LISEZMOI-ARCHIVE.txt, via l'outil du dépôt `scripts/drive_archiver.py` — déplacement
vérifié md5, jamais de suppression) ; la racine ne porte plus que les courants
(instructions, miroir, jetons, coffre-fort, `demo.exe` + LISEZMOI à jour, dossier test).
Suite : **M4 ouvert (D77)** — tunnel chiffré Schannel, couche I écrite-avant-code
(`m4/I/` : domaine `tls` créé — 8 spécifications + charte des contrats
cryptographiques [fail-closed intégral, certificat invalide = 502 propre, zéro
divulgation, compensation exacte] + révisions http-08:R2/http-10:R2, blocs
génération 6 g7xxxx) ; **étape (b) en cours** — D79 : layout.py (.text3 @ 0x6000,
héritage M0-M3 réexporté, HRESULT vérifiés à la source), notations tls-01/02/03
prouvées (différentiel de spécification 165 k cas zéro écart, falsification 6/6) ;
D82 : CADRE DE SESSION TLS et extension .rdata/IAT secur32 ARRÊTÉS (convention
partagée tls-04..08 + table des descripteurs M4 @0x29A0 + slots IAT 0x2A00-0x2A30),
tls-05 (cycle de vie des handles) notée-mesurée-prouvée — PREMIER BLOC À SHIMS du
jalon (harnais m4/harnais_cles.py : V1 round-trip 251 o + tls-02 intégrée, V2 dix
scénarios cadre octet par octet, V3 5 000 cas fuzzés zéro écart — graines 20261028/29,
V4 six mutations d'un point attrapées, témoin vert 7/7) ; **D83 : tls-04 (LA POIGNÉE
DE MAIN — LE critère M4) notée-mesurée-prouvée** — 544 o, boucle ISC bornée 16
allers, onze arguments msx64, garde E2 avant réception, échecs nommés sans
compensation ; harnais m4/harnais_poignee.py (VRAIS octets tls-02/tls-03/tcp-03/
tcp-04 embarqués : V2 seize scénarios cadre 0x9000 octet par octet + contrat
d'appels complet — certificat invalide = verdict 3, V3 5 000 cas fuzzés zéro
écart × 2 graines, V4 six mutations stable-en-taille attrapées, témoin 16/16) ;
**D88 : tls-06 (ÉMISSION CHIFFRÉE — le tunnel ÉMET) notée-mesurée-prouvée** —
491 o, boucle do-while des morceaux au message maximal NÉGOCIÉ (longueur 0 →
enregistrement vide), acquisition des tailles UNE fois par session
(QueryContextAttributesW, attribut 4 VÉRIFIÉ À LA SOURCE — discipline D79),
chiffrement SUR PLACE dans le cadre, destruction du clair copié sur échec
(Q2) ; harnais m4/harnais_emission.py (VRAIS octets tls-02/tls-03/tcp-04/
libc-01/libc-07 : V2 treize scénarios cadre octet par octet, V3 5 000 cas
fuzzés zéro écart × 2 graines, V4 six mutations attrapées + témoin 13/13) ;
**D89 : la convention du cadre de session AMENDÉE (zone de réception
2 × MAX_JETON, TAILLE_CADRE 0xC260 ; champs de géométrie +0x3A/+0x3C —
longueur utile / offset résidu, tls-07 unique propriétaire : la lecture
géométrique de « il sera écrasé » — l'écrasement du clair pompé est
l'œuvre de l'appel SUIVANT) puis tls-07 (RÉCEPTION DÉCHIFFRÉE — le
tunnel REÇOIT) notée-mesurée-prouvée** — 394 o, garde E2 unique sur la
somme offset + lot (une garde redondante nommée infalsifiable par le
différentiel : SUPPRIMÉE), descripteur type 2 (zone entière + 3 EMPTY),
DecryptMessageW (pfQOP réécrit 0), Q1 span du tampon 0 + champs
(lot − résidu, résidu), Q2 rien consommé, Q3 fin propre + curiosité
consignée, AUCUNE socket ; harnais m4/harnais_reception.py (VRAIS
octets tls-02/tls-03/libc-01 : V2 SEIZE scénarios EN CHAÎNES — le rôle
appelant lit la géométrie au cadre et réceptionne par-dessus, le span
d'un lot à deux enregistrements reste OCTET PAR OCTET intact : la
preuve géométrique ; V3a 4 000 appels + V3b 1 000 chaînes fuzzés zéro
écart × 2 graines, V4 DIX mutations attrapées + témoin 16/16) ;
**D90 : tls-08 (LA SESSION TLS CLIENTE — l'orchestrateur)
notée-mesurée-prouvée — LA SESSION COMPLÈTE EXISTE EN OCTETS** :
740 o, conventions D90 (paquet de session, VERDICT_CIBLE 7, fixtures
console « tunnel chiffre etabli » / « certificat rejete » — I4 : LE
critère M4, le verdict 3 de tls-04 produit la ligne console AVANT
compensation), l'ordre de Q1 est le contrat, TROIS règles
d'orchestrateur (DRAIN du résidu — jamais un enregistrement déchiffrable
en zone pendant que tcp-03 attendrait ; région vide = géométrie morte,
reprise en tête ; garde chambre nulle avant tcp-03), compensation
INTÉGRALE par COMPTAGE sur tout chemin (contexte SI écrit → credentials
SI acquis → socket SI ouverte, E4 = une ressaisie, le rax prime) ;
harnais m4/harnais_session.py — L'INTÉGRATION LA PLUS LARGE DU PROJET :
DIX-HUIT blocs réels (hello-02 M0 → tls-07 M4, R7), V2 VINGT scénarios
(cadre + paquet + contrat d'appels complet + comptes de compensation —
la ligne console EXACTE), V4 DOUZE mutations attrapées + témoin 20/20 —
53 PASS / 0 ÉCHEC × 2 graines ;
**D91 : http-08:R2 (LA PREMIÈRE RÉVISION DU DOMAINE HTTP SCELLÉ — le
parseur sait que le tunnel existe) notée-mesurée-prouvée** : lecture
contractuelle arrêtée avant notation (rax = 4 verdict « cible TLS »
porté par le retour — convention « mappe sur rax » ; zone aux règles R1 :
forme ABSOLUE = 1, Q3 hérité, verdicts 1/2/3 intacts) ; 326 o / 95
instructions, slot 0x7340×0x180 conservé ; « http:// » d'abord (tronçon
R1 octet pour octet), « https:// » ensuite BYTE-EXACT 8 octets, garde
len ≥ 8 avant toute lecture ; le début d'autorité porté dans rdx (LA
GÉOMÉTRIE PORTE LE SCHÉMA), verdict déduit structurellement au seuil
rcx+8 : le schéma préfixe « http://s://x » impossible PAR CONSTRUCTION ;
fixture « / » @0x24D0 de l'ancêtre réutilisée (RIP inter-sections) ;
harnais m4/harnais_cible_r2.py avec le DIFFÉRENTIEL D'ANCÊTRE (R1
scellé émulé contre R2 sur les mêmes entrées : 20 056 cas, écart ZÉRO,
divergence EXACTEMENT le domaine https byte-exact — tout autre écart
serait une régression de l'héritage scellé) + V2b spécification + V3
fuzz 20 000 + V4 six mutations stable-en-taille attrapées + témoin —
13 PASS / 0 ÉCHEC × 2 graines.
**D92 : http-10:R2 (LA RÉVISION DE ROUTAGE TLS — la session proxy route
la requête https dans le tunnel) notée-mesurée-prouvée** : 2125 o / 430
instructions, slot 0x74C0×0x900 conservé ; convention de cadre D92
(0x13390 = cadre R1 + verdict http-08:R2 @+0x7010 écrit sur tout chemin +
garde rdi @+0x7020 + paquet @+0x7100 + cadre TLS @+0x7130 ; probing D63
étendu aux bornes du cadre élargi) ; quatre arrêts contractuels — la
ligne console « certificat rejete » appartient à tls-08 SEUL (jamais
double-émise), l'entrée étiquetée « HTTP/1.1 502 Certificat rejete »
(34 o @0x2CA0) est la SEULE entrée nouvelle de la table (verdicts
2/4/5/6/7 → 502 R1 scellée), le port implicite 443 est le défaut passé à
http-07 (l'explicite gagne), un corps sur cible TLS est refusé 501
(refus honnête, miroir Transfer-Encoding) ; .cible_tls miroir de
.forme_absolue à r8d = 443 près, la chaîne résolution → contrôles →
réécriture est PARTAGÉE avec le chemin ordinaire, tls-08 appelé au
retour de la réécriture — 0 → fin, 3 → l'étiquetée, autre verdict →
502 générique ; harnais m4/harnais_session_r2.py — L'INTÉGRATION LA
PLUS LARGE DU PROJET (×2) : 29 blocs réels + L'ANCIÊTRE http-10:R3
scellé émulé sur les mêmes scénarios ; différentiel d'ancêtre (traces
normalisées par la base du cadre) : écart ZÉRO hors https, divergence
EXACTEMENT la cible https byte-exact ; 23 scénarios (réponse exacte au
client, lignes console UNE fois, compensation par comptage, PAQUET
capturé au passage de tls-08, cadre TLS VIERGE en canaris → zéro) ;
11 mutations attrapées + témoin ; V6bis prologue étendu + rejet I6' —
69 PASS / 0 ÉCHEC × 2 graines ; le différentiel a nommé une faute ABI
(rdi emprunté sans reçu par le rep stosq — corrigé, leçon consignée).
**D93 : L'ORACLE À SCÉNARIOS SSPI livré (m4/oracle_m4.py, 838 lignes —
réutilisation stricte D90/D92/D91, jamais deux sources) — les
orchestrateurs passent au VOLUME hostile** : F1 session tls-08
(générateurs d'HRESULT table TOTALE, TERMINATION PAR CONSTRUCTION :
E5 16 allers, un recv par cycle .relais, drain strictement
décroissant, maxmsg ≥ 1 ; Modele vs émulation 18 blocs : rax +
cadre 0xD000 octet par octet + contrat d'appels + comptes de
compensation + paquet intact) ; F2 le MODÈLE DE ROUTAGE dérivé de I
(P6/Q2'/Q3' — ModeleClient capture les octets effectivement émis,
_reponse_envoyee miroir de l'achèvement E8, table 0/3/autres)
contre l'émulation 29 blocs (réponse exacte, lignes console,
comptes, ports, GAI, paquet P6 au passage, cadre VIERGE, requête
intacte) + CONCORDANCE I croisée par modele_cible à CHAQUE
scénario + arrêts contractuels D92 (CL>0 / TE / POST-PUT sans
longueur / autorité vide / HTTPS:// / pair parti) ; F3
différentiel d'ancêtre à VOLUME (R7 : écart zéro hors https,
divergence exactement byte-exact — l'héritage non TLS couvert par
l'ancêtre émulé, la référence scellée) ; F4 falsification (8
mutations extraites D90/D92 TOUTES attrapées + modèle falsifié
nommé + témoin 6/6 + 6/6). QUATRE fautes nommées AVANT le vert
(layout du paquet de test D80 au-delà de 0x100 ; règle E5
« POST/PUT » lue dans la spec R1 — la notation était correcte ;
fragments vides = fermetures pour le shim ; échecs d'émission
contre le 501 délivré de l'ancêtre). Couverture MESURÉE (verdicts
F1 0:18/3:14/5:68/6:19/7:31, relais 16, poignée ≥ 2 allers 71,
compensation non triviale 109/150 ; F2 61 % routés ; F3 20 %
diverge) — **560 cas × graines 20261028/29/30/31 SANS écart**
(~18 s ; volume « reduit » 30 cas) ; executer(blobs, graine,
volume) prêt pour build_m4.py. Reste (b) : carte génération 6
(lignée D80), proxy.exe 0.5.0-dev.1. Terrain : D57 (WER) seul
point ouvert.

## Avertissement

Le dossier `.gdrive/` contient des jetons d'accès : il ne doit jamais être commité,
synchronisé ni affiché. Le dossier `.keys/` contient les secrets de la carte (phrase,
graine) et le conteneur chiffré du coffre-fort (D75) — jamais committés ni synchronisés
en clair ; la phrase de contrôle du coffre vit sous garde durable depuis D81
(`PHRASE-CONTROLE-COFFRE.txt` au racine du dépôt et au racine du coffre Drive —
décision développeur : le risque de perte l'emporte sur le risque d'exposition ;
restreindre le partage par lien du dossier Drive est la mitigation première).
L'application de validation (intercepteur MITM) est destinée à des
tests autorisés en environnement de laboratoire uniquement.
