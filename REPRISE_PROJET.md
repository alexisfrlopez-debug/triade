# REPRISE DU PROJET TRIADE — Fichier d'instruction

> Objet : reprendre le projet TRIADE là où il s'est arrêté, en moins de dix minutes, sans
> relire l'historique des conversations. Ce fichier est auto-suffisant : tout ce qu'il
> mentionne est présent dans la sauvegarde. Il s'adresse autant au développeur qu'à un
> agent IA chargé de continuer le travail.

- Dernière mise à jour : 25 octobre 2026
- Version de la spécification : v0.3 (figée pour le démarrage du jalon M0)
- État général : conception terminée (dont universalité par profils), infrastructure de sauvegarde opérationnelle, implémentation non commencée

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
| Spécification v0.3 | Terminée | `docs/PROTOCOLE_TRIADE.md` (source de travail faisant autorité pour la v0.3) ; le PDF v0.2 reste l'archive formelle de la version précédente |
| Journal des décisions | Terminé | D1 à D16 consignées dans `docs/DECISIONS.md` |
| Feuille de route | Terminée | Jalons M0 à M7 dans `docs/PLAN_MILESTONES.md`, critères de sortie mesurables |
| Format de la Carte | Spécifié | `docs/FORMAT_CARTE.md` — en-tête normalisé, quatre fragments, verrou croisé, export de continuité, re-cryptage |
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
│   ├── PROTOCOLE_TRIADE.md            Spécification v0.3 — source de travail
│   ├── Protocole_TRIADE_v0.2_Specification.pdf   Spécification v0.2 — archive formelle
│   ├── FORMAT_CARTE.md                Format détaillé de la Carte (couche C)
│   ├── DECISIONS.md                   Journal des décisions D1–D16
│   └── PLAN_MILESTONES.md             Feuille de route M0–M7
├── scripts/
│   ├── sync_backup.sh                 Sauvegarde complète : commit + Drive + GitHub
│   ├── drive_sync.py                  Synchronisation Google Drive (fichiers + bundle)
│   ├── check_auth.py                  Vérification des jetons d'accès
│   ├── triade_v02_spec.py             Générateur du PDF de spécification (ReportLab)
│   ├── triade_cover.html              Source HTML de la couverture du PDF
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

Ce script exécute, dans l'ordre : commit git (message passé en argument, sinon horodatage
automatique), synchro Google Drive (miroir des fichiers + régénération du bundle
d'historique + copie des fichiers d'instruction à la racine du Drive), puis push GitHub si
la remote `origin` est configurée. Le hook `post-commit` déclenche en outre une synchro Drive
à chaque commit, même manuel. Un agent IA travaillant sur ce projet DOIT exécuter cette
commande à chaque modification — c'est une exigence du protocole d'infrastructure,
consignée en D13 dans `docs/DECISIONS.md` et rappelée au § 11 du manuel agent.

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

## 7. Prochaine étape : le jalon M0

### 7.1 Objectif

Prouver la chaîne artefact de bout en bout sans compilateur : notation → octets → PE32+ →
exécution sur Windows 11. M0 est le jalon existentiel du projet — s'il échoue, le paradigme
entier est remis en question avant tout investissement supplémentaire.

### 7.2 Checklist de démarrage

1. Installer les dépendances de notation : `pip install keystone-engine capstone`.
2. Définir la couche I du « hello » : contrat du bloc principal, du bloc d'écriture, du bloc de sortie.
3. Écrire la notation des trois blocs initiaux (granularité D8).
4. Assembler via keystone ; vérifier le round-trip via capstone (fidélité exacte, R5).
5. Construire le PE32+ à la main : en-têtes DOS/COFF/PE32+, `.text` RX, `.rdata` imports +
   relocations, IAT kernel32 (WriteFile, GetStdHandle, ExitProcess), moins de 4 Kio.
6. Exécuter sur Windows 11 et observer la sortie console.
7. Créer la carte v0 : en-tête normalisé v0.3, trois blocs, quatre fragments, signature
   Ed25519 (R9).
8. Vérifier le verrou croisé bout en bout (R8) : empreintes des blocs dans frag-bld,
   re-vérification.
9. Après chaque avancée : `bash scripts/sync_backup.sh "M0 : <étape>"`.

### 7.3 Critères de sortie

Exécution constatée sur Windows 11 ; round-trip à 100 % ; carte signée et vérifiée ;
exécutable de moins de 4 Kio ; règles R1–R3 et R8–R9 respectées.

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
| `python3 scripts/drive_sync.py` | Synchronisation Drive seule (idempotente) |
| `python3 scripts/check_auth.py` | Vérifie les jetons Drive et GitHub sans les afficher |
| `git log --oneline` | Historique des modifications |
| `git bundle verify triade-history.bundle` | Vérifie l'intégrité du bundle de sauvegarde |
