# REPRISE DU PROJET TRIADE — Fichier d'instruction

> Objet : reprendre le projet TRIADE là où il s'est arrêté, en moins de dix minutes, sans
> relire l'historique des conversations. Ce fichier est auto-suffisant : tout ce qu'il
> mentionne est présent dans la sauvegarde. Il s'adresse autant au développeur qu'à un
> agent IA chargé de continuer le travail.

- Dernière mise à jour : 27 octobre 2026
- Version de la spécification : v0.4.0 (gouvernance vérifiée — figée pour le démarrage du jalon M0 ; budget de localisation amendé à 64 tokens par D31)
- État général : conception terminée, infrastructure de sauvegarde opérationnelle, **méthode démontrée à échelle réelle** (recodage RoomEq v3), **jalons M0 et M1 franchis** (validations terrain Windows 11 constatées) — M1 clos à la **balise finale `0.2.0`** (D32 : ligne unique `TRIADE M1 : minilibc 21/21 OK`, cristallisation 11×10/10, conformité 68/68, budgets mesurés, adresses stables démontrées) ; **M2 clos à la balise finale `0.3.0`** (D43 : boucle § 5 DÉMONTRÉE sur machine réelle — journal terrain demo.8, 28/28 lignes jusqu'à « DÉMO OK » ; conformité 124/124 ré-exécutée au scellage ; rc.2 = correctif IAT D35 ; rc.2 = correctif IAT D35 ; rc.3 = correctif DEP D39 : tcp-07:R2 — la phase d'écriture du patch passait SA PROPRE page en PAGE_READWRITE sans execute, tuant le processus au premier VirtualProtect ; oracle durci qui APPLIQUE les permissions réelles, 50 532 cas, cristallisation 10/10, conformité 124/124 ; constat terrain : porte R10 + libc 4/4 + CLIC démontrés sous Windows 11, la boucle § 5 complète attendue pour le scellage final 0.3.0 ; rc.4 = correctif D41 : tcp-07:R3 — .protger réservait 8 octets au lieu de 0x28 avant l'appel IAT VirtualProtect : kernel32 (/homeparams) rangeait rdx=0x700 sur l'adresse de retour de .protger, le ret sautait à 0x700 et tuait le processus ; oracles durcis /homeparams, 50 533 cas, cristallisation 10/10, conformité 124/124) ; **jalon démo : demo.exe 0.3.0-demo.9 livré (D43 — FINALE de lignée sans sondes ; md5 73c064fb…)** — demo.1 : fenêtre vide (RECT.top lu comme largeur, D36) ; demo.2 : démarrage corrigé et VALIDÉ terrain (journal 24 : L00→L02→L01, zéro LKO) MAIS capture terrain 26/10 20:56 : ÉCRAN VIDE au démarrage (traces fichier seul — spec win-02:R2 « jumeau silencieux », D37) et bouton non rendu ; demo.3 (D37) : miroir universel win-05:R3 (écran PUIS fichier, entrée trace @0x5000 + shim scénario @0x5100, .text2 0x1400/image 0x6000/fichier 16384 o) + diagnostics L4C/L4D — **VALIDÉ terrain 26/10 22:11** (journal 150 o : L00→L02→L4C=1→L4D=1→L01, la fenêtre AFFICHE son démarrage ; capture : 4 lignes lues, géométrie edit h-56 confirmée au pixel, DPI 125 %) MAIS bouton ENCORE invisible avec L4D=1 → **D38 : w/h de WM_SIZE vivaient en r10d/r11d VOLATILES relus après l'appel MoveWindow** (syscall écrit RFLAGS dans r11 par matériel → bouton placé hors client avec retour VRAI — invisible en statique, bénit par un oracle dont les shims ne modélisaient pas l'ABI caller-saved) ; demo.4 : **win-04:R4** (w/h en r14d/r15d callee-saved, invariant I6, taille identique) + **oracle durci : clobber des volatiles à chaque retour IAT** (r10=0, r11=0x246 réaliste, 78 cas verts, falsification V5 — réécrire les usages en r10d/r11d fait échouer l'invariant géométrique : le bouton invisible est impossible à réintroduire) ; défaut latent même classe dans libc-09 (M2, non embarqué, scellé carte) DIFFÉRÉ à la prochaine révision M2 (scanner garde : scripts/scan_abi_volatile.py) ; sha256:7e4e9105… ; **terrain 26/10 21:53 : LE CLIC A EU LIEU (D38 validé sur machine réelle — L03), porte R10 VERTE + libc 4/4 verts exécutés sur terrain, puis MORT en phase mécanique : D39 — tcp-07 passait SA page 0x4000 en PAGE_READWRITE (SANS bit execute) : DEP permanent en x64 → violation NX au retour du premier VirtualProtect, processus mort net, journal gelé après J_LIBC_OK (5e classe de défaut invisible sans exécution : sémantique de protection non modélisée — le shim VirtualProtect acquittait sans appliquer ; la spec R1 elle-même exigeait RW)** ; demo.5 : **tcp-07:R2** (PAGE_EXECUTE_READWRITE 0x40 pendant les écritures, invariant I6 « jamais de phase non exécutable pour la page du code en cours », restauration RX inchangée, diff 2 constantes) + cascade M2 **rc.3 scellée** + oracles durcis des deux côtés (permissions réelles, appariement RWX/RX 8/8, falsification V7 : 0x40→0x04 doit FAIRE FAUTER l'émulation — par appel direct, la porte R10 détecterait l'octet avant la mécanique) ; sha256:dc5215c5… ; **terrain 26/10 22:34 : journal demo.5 = MÊME FRONTIERE (10 lignes, gel après J_LIBC_OK) alors que L00 prouve que c'est le binaire corrigé qui a tourné — le DEP était nécessaire mais pas suffisant : audit exhaustif SANS défaut (binaire fidèle, payload v2 position-indépendant, .reloc vide → base préférée, oracle 79 cas verts re-exécuté) → 6e classe de défaut invisible sans exécution terrain (D40)** ; demo.6 : **win-09:R2 INSTRUMENTÉE (D40)** — 3 sondes de trace mode 0 (avant écho#1 / après tcp-07 pose / après memcmp v2) qui écrivent le journal fichier à chaque frontière : la dernière sonde visible localisera l'instruction mortelle ; slot win-09 0x380→0x3C0 (trou libre 0x4F80-0x4FFF), sondes en interstices .rdata (0x2748/0x276C/0x22F1, zones pleines), oracle durci (journal nominal 14 lignes, entrée trace 0x5000 déclarée, sondes dans les données RIP autorisées) ; 79 cas verts, falsification 28/28, héritage R7 intact, carte re-scellée ; sha256:1ad1b7df… ; sondes TEMPORAIRES (retrait R3 après correction) ; **terrain 27/10 : journal demo.6 lu (12 lignes, mort après « sonde1 avant echo », fenêtre disparue = crash processus) — les sondes ont localisé l'intervalle ; D41 : écho v1 (11 instructions pures) et memcmp (prouvé au sceau 4/4) éliminés, la POSE coupable — .protger appelait VirtualProtect SANS zone d'accueil ABI msx64 (7e classe de défaut invisible : obligation côté appelant, kernel32 /homeparams range rdx=0x700 sur l'adresse de retour → ret vers 0x700) ; audit systémique 58 sites IAT : 57 sains, 1 défaillant ; demo.7 : tcp-07:R3 (sub/add rsp,0x28 + lea r9,[rsp+0x20], diff 3 octets, zéro déplacement déplacé), M2 rc.4 scellée en cascade, oracles durcis /homeparams (M2 50 533 cas + V8, démo 80 cas + V8, falsification 28/28), shadow space 58/58 sain, diff demo.6→demo.7 chirurgical 7 octets ; sha256:1917c9af… (md5 89cf9e23…) ; attente terrain : journal demo.7 complet 14 lignes jusqu'à « boucle § 5 complète — DÉMO OK » → retrait des sondes + scellage final 0.3.0 ; **terrain 27/10 : journal demo.8 lu — 28/28 lignes jusqu'à « boucle § 5 complète - DÉMO OK » : LA BOUCLE § 5 EST DÉMONTRÉE SUR MACHINE RÉELLE** (D42 validé : le premier échange — point de mort de demo.7 — a vécu ; S1/S2 lus après « client : connecté », course bénigne documentée ; sonde4/sonde5 autour de chacun des 3 échanges identité/MAJUSCULES/retour ; D43 : 8e classe = section critique R_CS jamais initialisée dans l'hôte démo — win-09:R3 init en tête de scénario, le devoir de tcp-12 non embarqué) ; demo.9 (D43) : retrait de TOUTES les sondes (win-08:R3/win-09:R4/win-10:R3 — 140 o de code, 7 chaînes retour zéro, diff chirurgical 1 047 o zéro hors zone, correctifs D41/D42 VIVANTS, oracle 86 cas verts + journal nominal 11 lignes exactes = anti-régression du retrait, audit_demo9.py TOUT CONFORME) — FINALE de lignée ; **M2 scellé 0.3.0** (opération de carte, modèle M1 0.2.0 : conformité 124/124, balise rc.4→0.3.0, re-scellage Ed25519)** ; **chantier lignée sceau `m7/` : échelon 2 de l'échelle d'auto-hébergement D34** (vérification native — SHA-512 natif scellé 0.8.0-dev.1, Ed25519 en cours ; NB : `m7/` est un emprunt de nommage au sens D34/m6, le jalon M7 RISC-V du plan reste inchangé)

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
| Spécification v0.5.0 | Terminée | `docs/PROTOCOLE_TRIADE.md` (source de travail) et `docs/Protocole_TRIADE_v0.5.0_Specification.pdf` (archive formelle, chaîne LaTeX/Tectonic `scripts/spec_v050/` — née spec_v040, D25) ; révision du retour du terrain (D44) : validation terrain normée — boucle d'évidence (§ 8.4), taxonomie X1–X8 des défauts invisibles à l'émulation (§ 8.5, une classe par décision D35–D42), jalons M0–M2 constatés franchis, budgets mesurés, corrections (64 tokens, typographie) ; cahier de vérification V1–V10 (`scripts/spec_v050/verify_spec.py`) ; archives v0.4.0, v0.3, v0.2 conservées |
| Journal des décisions | Terminé | D1 à D32 consignées dans `docs/DECISIONS.md` (format normalisé depuis D24) |
| Feuille de route | Terminée | Jalons M0 à M7 dans `docs/PLAN_MILESTONES.md`, critères de sortie mesurables |
| Format de la Carte | Spécifié | `docs/FORMAT_CARTE.md` — en-tête normalisé, quatre fragments, verrou croisé, export de continuité, re-cryptage |
| Démonstration RoomEq | Livrée | `docs/Protocole_TRIADE_v0.3_Demonstration_RoomEq.pdf` (22 p.) — le protocole v0.3 démontré par le recodage complet de RoomEq (42 modules, 437 tests, parité v2.2.2), avec comparatifs de code avant/après ; dépôt `../roomeq` cristallisé depuis au tag `v3.0.2` (v3.0.0 → v3.0.2 : deux échecs de CI honorés puis corrigés, release GitHub publiée) |
| Article de recherche v0.4 | Livré | `docs/Protocole_TRIADE_v0.4_Article_Recherche.pdf` (12 p.) — édition académique du protocole (D18) : restructuration IMRAD, formalisation (verrou croisé κ, ordre lexicographique ≻_lex, règles en transitions), travaux connexes (dette technique, DbC, AISE), étude de cas avec RQ et design déclaré, menaces sur la validité (Wohlin) dont l'écart source/natif ; rapport de vérification interne : `docs/VERIFICATION_v0.4_Article.md` |
| Implémentation | **M1 franchi** | `m0/` validé terrain (D26) et `m1/` clos à la **balise finale `0.2.0`** (D32) : mini-libc de 7 blocs + autotest, oracle différentiel Unicorn 76 010 cas/exécution + 134 verrous, cristallisation 11×10/10, conformité profil verte 68/68, budgets mesurés (D31), démonstration R7, validation terrain Windows 11 constatée (26/10/2026) ; export de continuité (D16) au coffre sur la lignée 0.2.0 |
| Infrastructure | Opérationnelle | Dépôt git local + sauvegarde Google Drive + miroir GitHub privé + synchro systématique ; export de continuité chiffré au coffre Drive (racine) |

Aucune chaîne de build extérieure : les octets viennent de la notation. Le projet a
franchi son jalon existentiel — la phase de réalisation se poursuit avec M1.

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
| Google Drive, dossier « Triade » | Sauvegarde + livraison | Sous-dossier `TRIADE/` (miroir des fichiers) + `TRIADE/triade-history.bundle` (historique git complet) + à la racine : les deux fichiers d'instruction, les conteneurs de continuité (D16) et les **livrables terrain** (`demo.exe`, `LISEZMOI-demo.txt` — via `scripts/drive_livraison.py`) |
| GitHub `alexisfrlopez-debug/triade` | Miroir distant | Repo privé, poussé à chaque sauvegarde |

### 3.2 Arborescence du dépôt

```
triade/
├── README.md                          Carte d'identité du dépôt
├── REPRISE_PROJET.md                  Ce fichier — reprise rapide
├── PROTOCOLE_TRIADE_AGENT.md          Manuel d'utilisation pour un agent IA (nouveau projet)
├── docs/
│   ├── PROTOCOLE_TRIADE.md            Spécification v0.4.0 — source de travail
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
│   ├── build_pdf.sh                   Régénération systématique du PDF formel (D17/D25 — chaîne LaTeX/Tectonic v0.4.0)
│   ├── drive_sync.py                  Synchronisation Google Drive (fichiers + bundle)
│   ├── drive_livraison.py             Livraison terrain au coffre racine Drive (idempotente, vérifiée ; --dossier-test = dossier « test » du développeur)
│   ├── drive_recuperer.py             Rapatrie les fichiers du dossier Drive « test » vers upload/ (constats terrain)
│   ├── check_auth.py                  Vérification des jetons d'accès
│   ├── spec_v040/                     Sources de la spécification v0.4.0 (LaTeX/Tectonic, D25)
│   │   ├── main.tex + sec-a…d.tex     Corps monocolonne avec sommaire (5 fichiers)
│   │   ├── cover.html                 Couverture (Template 03, validée)
│   │   ├── merge_cover.py             Fusion couverture + corps, normalisation A4, métadonnées
│   │   └── verify_spec.py             Contrôles mécaniques pré-empaquetage (64 contrôles)
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

## 7. Étape en cours : le jalon M2 (patch à chaud)

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
l'export de continuité chiffré et signé (D16) est au coffre (racine du Drive) sur
la lignée 0.2.0.

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
périmètre du million). Prochaines étapes : (b) plan d'adressage M3 +
notation + oracle à scénarios + build proxy.exe ; (c) proxy transparent
curl ; (d) campagne million sur le périmètre parseur (~39 min/10^6 cas) ;
(e) le fuzzing rejoint la suite de conformité.

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
| `python3 m1/build_m1.py --verifier --graine N` | Ré-vérification complète M1 (R5/R8) + cristallisation (R6) |
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
| `python3 scripts/check_auth.py` | Vérifie les jetons Drive et GitHub sans les afficher |
| `git log --oneline` | Historique des modifications |
| `git bundle verify triade-history.bundle` | Vérifie l'intégrité du bundle de sauvegarde |
