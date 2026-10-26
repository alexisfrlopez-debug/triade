# REPRISE DU PROJET TRIADE — Fichier d'instruction

> Objet : reprendre le projet TRIADE là où il s'est arrêté, en moins de dix minutes, sans
> relire l'historique des conversations. Ce fichier est auto-suffisant : tout ce qu'il
> mentionne est présent dans la sauvegarde. Il s'adresse autant au développeur qu'à un
> agent IA chargé de continuer le travail.

- Dernière mise à jour : 26 octobre 2026
- Version de la spécification : v0.4.0 (gouvernance vérifiée — figée pour le démarrage du jalon M0)
- État général : conception terminée (universalité par profils + gouvernance normalisée née de la démonstration RoomEq), infrastructure de sauvegarde opérationnelle, **méthode démontrée à échelle réelle** (recodage RoomEq v3), implémentation non commencée

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
| Spécification v0.4.0 | Terminée | `docs/PROTOCOLE_TRIADE.md` (source de travail) et `docs/Protocole_TRIADE_v0.4.0_Specification.pdf` (archive formelle, chaîne LaTeX/Tectonic — D25) ; révision de gouvernance née des pratiques du recodage RoomEq : couche I normalisée (gabarit), taxonomie T1–T6, R10 renforcée, R11 (optimisation mesurée), conformité par profil, traçabilité I↔C↔B↔tests, journal des décisions normalisé, tableau de bord ; vérification interne : `docs/VERIFICATION_v0.4.0.md` (64 contrôles PASS / 0 FAIL) ; les archives v0.3 (27 p.) et v0.2 sont conservées |
| Journal des décisions | Terminé | D1 à D25 consignées dans `docs/DECISIONS.md` (format normalisé depuis D24) |
| Feuille de route | Terminée | Jalons M0 à M7 dans `docs/PLAN_MILESTONES.md`, critères de sortie mesurables |
| Format de la Carte | Spécifié | `docs/FORMAT_CARTE.md` — en-tête normalisé, quatre fragments, verrou croisé, export de continuité, re-cryptage |
| Démonstration RoomEq | Livrée | `docs/Protocole_TRIADE_v0.3_Demonstration_RoomEq.pdf` (22 p.) — le protocole v0.3 démontré par le recodage complet de RoomEq (42 modules, 437 tests, parité v2.2.2), avec comparatifs de code avant/après ; dépôt `../roomeq` cristallisé depuis au tag `v3.0.2` (v3.0.0 → v3.0.2 : deux échecs de CI honorés puis corrigés, release GitHub publiée) |
| Article de recherche v0.4 | Livré | `docs/Protocole_TRIADE_v0.4_Article_Recherche.pdf` (12 p.) — édition académique du protocole (D18) : restructuration IMRAD, formalisation (verrou croisé κ, ordre lexicographique ≻_lex, règles en transitions), travaux connexes (dette technique, DbC, AISE), étude de cas avec RQ et design déclaré, menaces sur la validité (Wohlin) dont l'écart source/natif ; rapport de vérification interne : `docs/VERIFICATION_v0.4_Article.md` |
| Implémentation | Non commencée | La prochaine étape est le jalon M0 (voir section 7) |
| Infrastructure | Opérationnelle | Dépôt git local + sauvegarde Google Drive + miroir GitHub privé + synchro systématique |

Aucun bloc machine n'a encore été écrit : le projet entre dans sa phase de réalisation.

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
| Google Drive, dossier « Triade » | Sauvegarde | Sous-dossier `TRIADE/` (miroir des fichiers) + `TRIADE/triade-history.bundle` (historique git complet) + les deux fichiers d'instruction à la racine |
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
│   ├── DECISIONS.md                   Journal des décisions D1–D25
│   └── PLAN_MILESTONES.md             Feuille de route M0–M7 — à jour v0.4.0 (conditions transverses)
├── scripts/
│   ├── sync_backup.sh                 Sauvegarde complète : PDF à jour + commit + Drive + GitHub
│   ├── build_pdf.sh                   Régénération systématique du PDF formel (D17/D25 — chaîne LaTeX/Tectonic v0.4.0)
│   ├── drive_sync.py                  Synchronisation Google Drive (fichiers + bundle)
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

## 7. Prochaine étape : le jalon M0

### 7.1 Objectif

Prouver la chaîne artefact de bout en bout sans compilateur : notation → octets → PE32+ →
exécution sur Windows 11. M0 est le jalon existentiel du projet — s'il échoue, le paradigme
entier est remis en question avant tout investissement supplémentaire.

### 7.2 Checklist de démarrage

1. Installer les dépendances de notation : `pip install keystone-engine capstone`.
2. Définir la couche I du « hello » selon le gabarit v0.4.0 (§ 2 de la spécification) :
   contrat du bloc principal, du bloc d'écriture, du bloc de sortie.
3. Écrire la notation des trois blocs initiaux (granularité D8).
4. Assembler via keystone ; vérifier le round-trip via capstone (fidélité exacte, R5).
5. Construire le PE32+ à la main : en-têtes DOS/COFF/PE32+, `.text` RX, `.rdata` imports +
   relocations, IAT kernel32 (WriteFile, GetStdHandle, ExitProcess), moins de 4 Kio.
6. Exécuter sur Windows 11 et observer la sortie console.
7. Créer la carte v0 : en-tête normalisé v0.4.0, trois blocs avec champ `spec=` (traçabilité),
   quatre fragments, signature Ed25519 (R9).
8. Vérifier le verrou croisé bout en bout (R8) : empreintes des blocs dans frag-bld,
   re-vérification.
9. Après chaque avancée : `bash scripts/sync_backup.sh "M0 : <étape>"`.

### 7.3 Critères de sortie

Exécution constatée sur Windows 11 ; round-trip à 100 % ; carte signée et vérifiée ;
exécutable de moins de 4 Kio ; règles R1–R3 et R8–R9 respectées ; conditions transverses
v0.4.0 (§ 16) : oracle vert, journal à jour (décisions, optimisations, classification
T1–T6), tableau de bord conforme avec métriques cible explicitement annotées.

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
| `bash scripts/sync_backup.sh "msg"` | Sauvegarde complète (commit + Drive + GitHub) |
| `python3 scripts/triade_v03_demo_roomeq.py` | Régénère le PDF de démonstration RoomEq (couverture rendue au préalable via `html2poster.js` — voir en-tête du script) |
| `pdf.py convert.latex scripts/article_v04/main.tex --runs 3` puis `python3 scripts/article_v04/merge_cover.py` | Régénère le corps de l'article v0.4 puis fusionne couverture + corps (couverture : `html2poster.js` sur `cover.html` — voir l'en-tête de `merge_cover.py`) |
| `python3 scripts/article_v04/verify_article.py` | Contrôles pré-empaquetage de l'article (terminologie, IMRAD, références, flottants) |
| `python3 scripts/drive_sync.py` | Synchronisation Drive seule (idempotente) |
| `python3 scripts/check_auth.py` | Vérifie les jetons Drive et GitHub sans les afficher |
| `git log --oneline` | Historique des modifications |
| `git bundle verify triade-history.bundle` | Vérifie l'intégrité du bundle de sauvegarde |
