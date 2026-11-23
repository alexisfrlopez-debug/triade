# REPRISE DU PROJET TRIADE — Fichier d'instruction

> Objet : reprendre le projet TRIADE là où il s'est arrêté, le plus vite
> possible, sans relire l'historique. Ce fichier est auto-suffisant. Il
> s'adresse autant au développeur qu'à un agent IA chargé de continuer.
> REDESSINÉ à la vague 14 (22/11/2026, la demande du maître) : le système
> des VAGUES d'instructions, la restauration du bac, la chaîne de release.

## 1. Le projet en 30 secondes

TRIADE est un protocole où un agent IA écrit du CODE MACHINE NATIF PUR
(x86-64, RISC-V, TLS 1.3) à la main, guidé par des spécifications signées
(couche I) et une carte chiffrée (couche C) verrouillée aux octets (couche
B). Trois couches indissociables ; priorités lexicographiques
**Sécurité > Performance > Optimisation > Coût en tokens**. Le dossier
publie des ÉDITIONS académiques (manuscrit, spécification, Livre du
Coffre, preuves, présentation) au DOI Zenodo
**10.5281/zenodo.24367343** (concept ; v0.23.3 = record 24450872 —
la version courante, les TROIS packs ; les records datés : 24420007 =
v0.22.1, 24438614 = v0.23.0, 24442241 = v0.23.1, 24442951 = v0.23.2).
LES DEUX ŒUVRES SÉPARÉES du protocole : le kit développeur v1.0.0 au
DOI 10.5281/zenodo.24457515 (concept 10.5281/zenodo.24457514) et le
corpus TRIADE-CORPUS-v1 au DOI 10.5281/zenodo.24457525 (concept
10.5281/zenodo.24457524).

## 2. LE RYTHME : LES VAGUES D'INSTRUCTIONS (le cœur de la reprise)

Le maître dépose des instructions au dossier **`instructions`** du coffre
Drive (le lien « nouvelles instructions ici, à archiver après
exécution »). Chaque vague = 6 instructions environ (fichiers
`Qwen__AAAAMMJJ_<code>.txt`). La session d'une vague :

1. **RESTAURER LE BAC** (§ 3) ;
2. **GELER LES PLANS** : un `PLAN-<CODE>.md` par instruction + la table
   `EMPREINTES-PLANS-VAGUE<N>.txt` (sha256) — COMMIT AVANT TOUTE DONNÉE
   (la règle reconduite des vagues 8-13) ;
3. **EXÉCUTER** chaque atelier `atelier-<nom>-<code>/` (un commit par
   atelier, sceau 14/14 avant/après : `python3 v06/sceau_I.py verifier`) ;
4. **ARCHIVER LES INSTRUCTIONS** : copie au dépôt
   `ARCHIVE/instructions_vague<N>_<AAAAMMJJ>/` (recoupée byte-byte), AU
   COFFRE le geste en deux étapes (retirer du `/instructions` PUIS ajouter
   au dossier ARCHIVE — l'appel combiné est refusé 403) ; le
   `/instructions` LAISSÉ VIDE ;
5. **LA RELEASE** (la commande du maître : « il faudra ensuite mettre à
   jour les miroirs et zenodo ») : l'édition ou la release corrective au
   concept Zenodo (§ 5), la livraison au coffre, les miroirs ;
6. **CONSIGNER** : l'Entrée au `worklog.md`, `OU-TROUVER-LES-LIVRABLES.md`,
   et LE PRÉSENT FICHIER mis à jour.

**L'ÉTAT PRÉSENT** : LE CORPUS v2 MINTÉ AU CONCEPT — LES 60 APPELS
v6 AJOUTÉS (Entrée 393, 23/11/2026 — la commande du maître « ajoute les
60 appels v6 au corpus et mets a jour tous les kits dans les depots git
drive et zenodo si necessaire » ; l'état déposé des Entrées 390-391
demeure — la commande du maître « fais
les depots zenodo », les deux gestes nommés aux Entrées 388/389 SUITE :
la doctrine « jamais mintés sans commande » honorée). LE KIT DÉVELOPPEUR
v1.0.0 au DOI 10.5281/zenodo.24457515 (LE CONCEPT 10.5281/zenodo.24457514
— une ŒUVRE SÉPARÉE : le zip 415 890 o, md5 bd751c04…, les 158 entrées,
licence BSL-1.1, upload_type software) ; LE CORPUS TRIADE-CORPUS-v1 au
DOI 10.5281/zenodo.24457525 (LE CONCEPT 10.5281/zenodo.24457524 : les
sept fichiers posés individuellement, 109 triples, BSL-1.1 + le canari
CC-BY-4.0, upload_type dataset) — chacun par LA VOIE DES PATRONS
(brouillon → bucket → métadonnées → PUBLISH), les md5 recoupés
byte-byte au bord anonyme (1/1 + 7/7 VERTS, les 18 VERT re-preuvés à
l'Entrée 391), les deux DOI résolvant chez doi.org ; L'ÉDITION du
protocole demeure v0.23.3 (LE RECORD 24450872, le concept
10.5281/zenodo.24367343). LE JETON RELAIS OAuth RENOUVELÉ (la
ré-autorisation interactive du maître — le refresh_token du 23/11,
11/11 copies Drive à jour, le SA physichong en repli lecture D263).
LA CONSIGNATION CLOSE EN DEUX GESTES : l'Entrée 390 au commit 4824215
(le worklog, l'OU-TROUVER, les § 1/§ 4/§ 6 du présent fichier, le
rapport à la racine du dépôt, le push GitHub, la première sync du
miroir) PUIS L'ACHÈVEMENT à l'Entrée 391 (la section ÉTAT PRÉSENT du
présent fichier demeurée à l'état 389 au 4824215 — l'écart nommé,
portée ; le rapport LIVRÉ AU /test du coffre et recoupé byte-byte ;
les 18 VERT du bord anonyme rejoués ; la ligne de pack du bundle
nommée — les octets du pack diffèrent à contenu identique selon la
lignée du bac — ET L'ÉQUIVALENCE PROUVÉE : les cinq refs et l'univers
des 12 569 objets identiques, la tête 4824215 ; le miroir re-syncé,
les trois bords re-vérifiés, le sceau-I 14/14). LA CAMPAGNE DU DÉCODAGE
CONTRAINT OUVERTE AU GUICHET ET REFUSÉE SUR PIÈCES (l'Entrée 392,
l'atelier 81eruqtl6 [TPL-ADD-v7 — l'écart de numérotation avec le
langage « campagne v6 » des SUITE 390/391 nommé au plan], la commande
du maître « commence la campagne v6 ») : le CLI SANS response_format
re-vérifié, le SDK laisse passer le champ, LE BACKEND L'IGNORE —
response_format accepté-mais-ignoré (P1 la sortie en texte libre ; P2
la violation ordonnée passée INTÉGRALE sous json_schema strict à
l'enum ; P3 la structure corps émise mais en fences markdown hors
contrainte) ; LE GUICHET REFUS, la campagne NON courue (jamais une
mesure habillée en contrainte), le motif canonnel calibré 5/5 aux
vertes v6 demeurant PRÊT AU DÉCODEUR (« si l'instrument l'expose un
jour ») ; le rapport-instrument-20261123.txt à la racine et au /test.
LES GESTES AU DÉVELOPPEUR restants : le poste réel (les lemmas
Tamarin + le run ProVerif), le métal nu (≥ 2 machines), les 28
livraisons H7, l'annotateur, l'endpoint de la seconde famille — LES
DÉPÔTS ZENODO DU KIT ET DU CORPUS SOLDÉS ET CONSIGNÉS ; l'entraînement
DPO au gym LA SEULE ROUTE VIVANTE de la voie nommée (les paires du
corpus + les 60 appels v6 au garde-brut au corpus à la prochaine
vague, le compute au développeur).
LE CORPUS v2 MINTÉ (l'Entrée 393) : l'atelier avmwtf5w — LES 60 APPELS
DE CAMPAGNE v6 extraits mécaniquement (les 18 tâches, 5 VERT / 13
REFUS, la correspondance PAR ID, le code v1 reconduit octet pour
octet), LA PREUVE v1 AVANT TOUT AJOUT (les 36 tâches v3/v4 à leur
affectation v1 EXACTE, les 109/109 lignes reproduites byte-byte —
l'étanchéité v1 préservée), LES SPLITS CONTINUS à la même règle (la
graine 20261126 : TRAIN 42 tâches / 129 lignes + le canari unique ·
DEV 6/20 · TEST 6/21 SANS dorée), la porte de scrub 169/169 admis au
contrôle négatif vécu, la cristallisation 10×, les exclusions nommées
(les 11 relance v6 et les 60 appels v5 hors commande, les tentatives
v2 toujours sans contrats) ; LE DOI 10.5281/zenodo.24463681 MINTÉ au
concept 10.5281/zenodo.24457524 résolvant sur v2 (la v1 au record
24457525 demeurée immuable), les 7/7 md5 recoupés byte-byte au bord
anonyme, le DOI chez doi.org ; LE KIT v1.0.0 VÉRIFIÉ INTACT (le record
24457515, 1/1 md5 — AUCUNE mise à jour nécessaire : aucune des 158
pièces ne bouge) ; les kits des dépôts git/Drive/Zenodo tenus (le
commit, le push, la sync du miroir, le rapport au /test, les trois
bords, le sceau-I 14/14) ; l'entraînement DPO au gym la route vivante
(les paires du corpus v2, le compute au développeur). Détail au
worklog (Entrées 385-393).

**L'ÉTAT PRÉSENT (Entrée 394, 23/11/2026) — LA VAGUE 16 OUVERTE ET NON CLOSE** : SIX INSTRUCTIONS du 23/11 reçues au \/instructions\ (0j7ywza2h la campagne TPL-ADD-v6, 0pljbn96b le kit Tamarin/ProVerif, 86d3ushrr les six résidus, am9d6o2th l'audit d'étanchéité, io3uh37cj les couloirs scellés, ru2rfjl2g l'ancrage/sentinelle/garde RAM) — LES SIX PLANS GELÉS (EMPREINTES-PLANS-VAGUE16.txt, le commit 71647ea d'abord). **AM9D6O2TH EXÉCUTÉ** : la fuite par contrat CONSTATÉE (dix contrats partagés, le TEST v2 contaminé par construction) et RÉPARÉE par groupe-de-contrat à la graine 20261126 (TRAIN 14 · DEV 2 · TEST 2, le TEST nu, le canari unique au TRAIN) — l'audit rejoué ÉTANCHE, les dix rebuilds bit-identiques (commit 2e18c73). **RU2RFJL2G PARTIEL** : le témoin d'époque et son vérificateur OFFLINE (6/6), la garde RAM native (5/5), les deux écarts nommés (commit 8e2a857). **86D3USHRR PARTIEL** : le recompte (delta 12, non 13) et le périmètre re-scopé. **QUATRE ATELIERS BLOQUÉS AU POSTE** (Tamarin/Maude, tectonic/weasyprint, keystone/capstone et le métal nu, l'instrument du décodage contraint) — nommés sur pièces. AU COFFRE : les DEUX instructions exécutées archivées à ARCHIVE/instructions_vague16_20261123, les QUATRE non exécutées laissées au /instructions (la vague n'est pas close) ; les six copiées au dépôt ARCHIVE/ ; la version Zenodo du corpus corrigé À LA COMMANDE du maître.

## 3. RESTAURER LE BAC NEUF (le pas à pas éprouvé à la vague 14)

```
1. jetons du coffre Drive /Tokens → /home/z/my-project/work/tokens/
   (oauth_token_relais.json [OAuth compte propriétaire — le refresh token
   d'upload peut meurer : le SA physichong couvre la LECTURE], zenodo.txt,
   token_git.txt)
2. cp le SA + le client_secret vers depot/.gdrive/ (chmod 600) ;
   echo le jeton zenodo > /home/z/my-project/work/mirrors_zenodo.txt
3. le bundle : télécharger TRIADE-sauvegarde-git/triade-history.bundle
   (145 Mo) → git clone <bundle> /home/z/my-project/depot && cd depot
   && git remote set-url origin https://github.com/alexisfrlopez-debug/triade.git
4. cp git-hooks/pre-commit .git/hooks/ (la garde de secrets h66o54pjd)
5. LES OUTILS DU BAC : pip install z3-solver unicorn keystone-engine
   capstone tiktoken ; apt-get download maude libbdd0c2 libtecla1t64
   libsigsegv2 libgcc-14-dev cpp gcc → dpkg-deb -x <chacun> maude-root/ ;
   curl tamarin-prover 1.12.0 linux64-ubuntu.tar.gz → /tmp/tamarin-prover
   (PATH=maude-root/usr/bin, LD_LIBRARY_PATH=maude-root/usr/lib/...) ;
   mingw : apt-get download gcc-mingw-w64-x86-64-posix + -x86-64 +
   binutils-mingw-w64-x86-64 + mingw-w64-x86-64-dev + gcc-14-base →
   dpkg-deb -x <chacun> /home/z/my-project/work/mingw-debs/root/
6. python3 scripts/check_auth.py  (le test des jetons, sans les montrer)
```
tectonic et openssl sont déjà au bac. Vérifier : `git log --oneline -3`
(la tête == le miroir GitHub : ls-remote), `python3 v06/sceau_I.py
verifier` (14 arbres VERTS).

## 4. OÙ TOUT SE TROUVE

| Emplacement | Contenu |
|---|---|
| `/home/z/my-project/depot` | LA SOURCE DE VÉRITÉ : le dépôt git complet (l'historique par le bundle ; l'arborescence § 6) |
| Coffre Drive (dossier racine « Triade ») | le `/instructions` (les vagues en attente), `ARCHIVE/` (les instructions exécutées, les packs supersédés), `/livrables` (les packs courants), `/test` (les constats du développeur), `TRIADE-sauvegarde-git/` (LE MIROIR du dépôt + triade-history.bundle + worklog + OU-TROUVER + les ateliers), `/Tokens`, `coffre_fort.bin` + `PHRASE-CONTROLE-COFFRE.txt` (garde durable D81), le conteneur de continuité |
| GitHub `alexisfrlopez-debug/triade` | le miroir distant (push à chaque release, vérifié anonymement ls-remote) |
| Zenodo | le concept 10.5281/zenodo.24367343 (les versions : …24420007 = v0.22.1, 24438614 = v0.23.0, 24442241 = v0.23.1, 24442951 = v0.23.2, **24450872 = v0.23.3 — la version courante, les trois packs**) ; LES ŒUVRES SÉPARÉES : le kit développeur v1.0.0 (concept 10.5281/zenodo.24457514 → record 24457515), le corpus TRIADE-CORPUS (concept 10.5281/zenodo.24457524 : …24457525 = v1, **24463681 = v2 — la version courante, les 60 appels v6 ajoutés, les 169 triples**) |
| `/home/z/my-project/download/` | les livrables du bac (miroir des pièces terrain) |

**Les jetons NE SONT JAMAIS committés** (la garde pre-commit h66o54pjd :
empreintes + entropie ; § 8 de l'ancien fichier demeure).

## 5. LA CHAÎNE DE RELEASE (la voie éprouvée v13)

1. **L'édition** (quand la vague porte une génération) : edition-v0<N>M0/
   née de la précédente, macros régénérées des journaux vivants
   (`scripts/vague13/regenerer_macros_v230.py`), tectonic + weasyprint
   pour les cinq pièces, LE LINTER (`scripts/vague12/linter_v230.py`,
   étendu à v232 : `scripts/vague14/linter_v232.py` — zéro rouge +
   contrôle négatif), les packs (soumission / présentation / complet)
   assemblés aux empreintes consignées (`scripts/vague14/
   assemble_pack_v232.py`) ;
2. **LA PUBLICATION ZENODO** (patrons v13/v14 : `scripts/vague13/
   publier_zenodo_v0230.py`, `scripts/vague14/publier_zenodo_v0232.py`) :
   la voie newversion → bucket → métadonnées → PUBLISH, reprise
   idempotente aux 500, les md5 recoupés byte-byte au bord anonyme,
   le DOI de version minté ;
3. **LA LIVRAISON AU COFFRE** (patrons v13/v14 : `scripts/vague13/
   livrer_coffre_vague13.py`, `scripts/vague14/livrer_coffre_v232.py`)
   : la racine, le /test, le /livrables, les supersédés au
   lot ARCHIVE — chaque pièce recoupée par re-téléchargement (le 308
   « Resume Incomplete » est LA réponse intermédiaire normale) ;
4. **LES MIROIRS** : `python3 scripts/drive_sync.py` (miroir + bundle),
   le push GitHub (jeton .gdrive/token_git.txt), la vérification
   `verifier_trois_bords_v230.py` (le patron) ;
5. **L'ARCHIVAGE DES INSTRUCTIONS** (§ 2 point 4) ; worklog + OU-TROUVER
   + le présent fichier mis à jour ; le commit final + push.

## 6. L'ARBRERESCEMENT du dépôt (l'essentiel)

```
depot/
├── worklog.md                      LE JOURNAL (fait foi pour le détail ;
│                                   la dernière Entrée = l'état)
├── OU-TROUVER-LES-LIVRABLES.md    la carte des livrables (maj chaque Entrée)
├── PLAN-*.md + EMPREINTES-PLANS-VAGUE*.txt   les plans gelés (une table par vague)
├── REPRISE_PROJET.md               CE FICHIER
├── docs/                           PROTOCOLE_TRIADE.md (la spec source de travail),
│                                   DECISIONS.md (D1-D251+), PLAN_MILESTONES.md,
│                                   les archives PDF (v0.2 → v0.15.8), le Livre
├── scripts/                        sync_backup.sh, drive_sync.py, build_pdf.sh,
│   ├── vague11/ vague12/ vague13/  les chaînes par vague (linter v230, patchers)
│   │   vague14/                 LA CHAÎNE v232 (linter étendu, assemble,
│   │                            publier, livrer — les patrons courants)
│   ├── spec_v158/ livre_v17/       les sources spec + Livre (tectonic/cover)
├── scripts/vague15/pack-v233/      L'ÉDITION courante (les sources v0.23.3)
├── depot-zenodo-v0233/             les packs v0.23.3 (soumission + complet ; la présentation à la racine)
├── atelier-*/                      LES ATELIERS par vague (un dossier par
│                                   instruction : rapport + outils + registres)
├── ARCHIVE/                        les instructions exécutées par vague
├── m0/ m1/ m2/ m3/ m4/ m5/ m6/ m7/ m8/ tls13/ riscv/ unix/ loupe/ demo/
│   terrain/ v06/                   les jalons scellés (SCEAU-I 14/14)
├── loupe/ tls13/                   les notation/ + I/ (le matériau TPL-ADD)
└── v06/sceau_I.py                  LA GARDE (verifier : 14 arbres VERTS)
```

## 7. Les règles qui ne se marchandent pas

- le plan gelé AVANT la donnée ; l'empreinte consignée ; le commit d'abord ;
- **aucun verdict fabriqué** : un échec mesuré est une pièce aussi
  précieuse qu'un vert (la trace consignée) ;
- **le verbatim historique demeure octet pour octet** : les corrections
  vivent en ERRATUM append-only à côté ;
- **aucun secret commité** (la garde h66o54pjd), le coffre réel jamais
  touché au laboratoire (D105), les scellés intacts (le sceau-I avant et
  après chaque geste) ;
- la sauvegarde systématique (sync_backup.sh) après chaque modification ;
- l'ordre des tâches JAMAIS re-tiré ; les graines consignées.

## 8. Le protocole de cette session de reprise (la v0.23.2, pour mémoire)

La session de génération promise à l'Entrée 384, suscitée par la
commande du maître « je n'ai pas la version presentation et soumission
du pack dans zenodo » : LES CINQ PIÈCES régénérées aux sources corrigées
(io13olvxz soldé), LE LINTER v232 ÉTENDU aux quatre règles nouvelles
(153 VERT 0 ROUGE + le contrôle négatif vécu), LES CORRECTIONS (a)-(j)
portées, la vague 14 au corps, LE SCEAU-I 14/14 avant/après, LES TROIS
PACKS assemblés (soumission / présentation / complet), LA PUBLICATION
ZENODO v0.23.2 (record 24442951, les trois md5 recoupés byte-byte), LA
LIVRAISON AU COFFRE (les trois packs au /livrables, le rapport et le
manifeste à la racine, les supersédés aux lots ARCHIVE). La session MORT
AU CONTEXT après la livraison — la présente reprise a achevé la chaîne :
LE COMMIT de la consignation (l'Entrée 385 au worklog, l'OU-TROUVER, le
script livrer_coffre_v232.py, le présent fichier), LE PUSH GitHub, LA
SYNC DU MIROIR Drive (bundle régénéré, worklog, OU-TROUVER, REPRISE),
LA VÉRIFICATION DES TROIS BORDS. Les GAPS nommés à l'Entrée 385 demeurent
(la mesure d'entrelacement GHASH, le re-run Tamarin de l'amendement, les
28 livraisons H7, l'annotateur, les machines du dudect — au geste du
maître ; la seconde machine).
