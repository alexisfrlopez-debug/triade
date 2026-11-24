# TriadeKit — le GUI 1-clic des cérémonies

Composant graphique du **Kit de Développement Triade** : une **interface
graphique 1-clic autonome** pour les cérémonies Git / Google Drive / Zenodo.
Conçu pour être le moins contraignant possible : un seul fichier à lancer,
zéro dépendance à installer, tout est paramétrable depuis la fenêtre.

> Ce dossier (`ceremonies/gui/`) peut aussi être copié seul et utilisé de
> manière autonome : le moteur complet vit dans l'unique fichier
> `TriadeKit.py` (Python stdlib uniquement, tkinter pour l'interface).

---

## Démarrage express (60 secondes, sans aucun jeton)

1. Ouvrez ce dossier (`ceremonies/gui/` du kit, ou sa copie autonome).
2. Double-cliquez sur le lanceur de votre système :
   - **Windows** : `LANCEUR-WINDOWS.bat`
   - **macOS** : `LANCEUR-MAC.command`
   - **Linux** : `LANCEUR-LINUX.sh`
3. À la question « Aucun jeton n'est encore configuré », répondez **Oui** pour
   la démonstration.
4. Cliquez sur le grand bouton vert **LANCER LE CYCLE COMPLET AUTONOME** et
   regardez la cérémonie se dérouler.

> Seul prérequis : **Python 3.8+** (préinstallé sur macOS et la plupart des
> Linux ; sur Windows, https://www.python.org/downloads/ en cochant
> « Add Python to PATH »). `git` doit aussi être installé
> (https://git-scm.com) pour les cérémonies Git. Sous Linux, le paquet
> `python3-tk` peut être nécessaire ; le mode `--cli` fonctionne sans.

---

## Le principe : trois piliers, six cérémonies, un clic

| Cérémonie | Ce qu'elle fait |
|---|---|
| **Initialisation** | Nouveau projet : `git init` + premier commit + push, dossier Drive créé, dépôt Zenodo en brouillon, première synchronisation. |
| **Vérification** | Contrôle les jetons et la connectivité de chaque pilier (voyants GIT / DRIVE / ZENODO en haut à droite). |
| **Rotation** | Renouvelle les jetons : récupération automatique depuis le **dossier Drive public des jetons** (validé en conditions réelles : fichiers reconnus par leurs noms et leurs contenus, environnement Zenodo sandbox/production détecté automatiquement), ou import d'un dossier local, ou saisie manuelle. Chaque jeton est **validé auprès de sa plateforme avant d'être appliqué** ; l'ancienne configuration est archivée dans `config/`. |
| **Synchronisation** | `git add + commit + push`, puis archive du projet téléversée sur Drive (jetons et configuration **exclus** des archives). |
| **Passage public** | Dépôt GitHub rendu public, dossier Drive partagé en lecture, nouvelle version Zenodo téléversée et **publiée (DOI)**. |
| **Cycle complet** | Tout l'enchaînement en un seul clic : vérification → rotation automatique si des jetons sont manquants ou périmés → synchronisation → passage public. |

Chaque cérémonie produit :
- un journal horodaté dans `journal/` ;
- un rapport JSON (`journal/*.rapport.json`) avec étapes, erreurs et liens ;
- une entrée dans `journal/historique.jsonl` (traçabilité complète des cérémonies passées).

## Les trois modes

| Mode | Comment l'activer | Effet |
|---|---|---|
| **Réel** | Par défaut | Actions effectives sur vos dépôts. |
| **Simulation** | Case « Mode simulation » dans la barre d'outils | Tout est journalisé, **rien n'est écrit** — idéal pour répéter une cérémonie avant de la jouer pour de vrai. |
| **Démonstration** | Bouton « Demo » ou `--demo` | Cérémonies entièrement simulées, aucun jeton requis, aucun réseau. |

Le passage public demande une **confirmation unique** (par défaut) car la
publication Zenodo est irréversible : un seul clic de confirmation pour tout
le cycle.

## Configurer les jetons (une seule fois, puis la rotation s'en charge)

Ouvrez **Configuration…** dans la barre d'outils :

- **Git** : URL du dépôt GitHub + Personal Access Token
  (https://github.com/settings/tokens, portée `repo`).
- **Drive** : jeton d'accès OAuth (+ optionnels : jeton d'actualisation,
  client ID, client secret — permettent au kit de rafraîchir le jeton
  automatiquement), et les **identifiants de VOS dossiers Drive** — ils
  partent **vides** : le kit n'embarque l'accès, le dossier ou le jeton
  **d'aucun utilisateur** :
  - dossier projet : l'identifiant de votre dossier Drive de travail (la
    partie de l'URL après `/folders/`) ;
  - dossier des jetons : l'identifiant de votre dossier Drive où vous
    déposez les jetons renouvelés (facultatif — utilisé par la rotation
    automatique).
- **Zenodo** : jeton (https://zenodo.org/account/settings/applications/) +
  ID du dépôt. L'environnement est sur **sandbox** par défaut ; lors de la
  rotation, le kit **détecte automatiquement l'environnement (sandbox ou
  production) qui accepte votre jeton** et le retient — basculez sur
  **production** pour un DOI définitif.

### Rotation : trois façons de fournir les nouveaux jetons

1. **Automatique** (bouton Rotation ou cycle complet) : le kit lit le
   dossier Drive public des jetons et télécharge les fichiers, sans même
   avoir besoin d'un jeton Drive valide.
2. **Dossier local** : « Rotation : importer un dossier… » et choisissez le
   dossier téléchargé.
3. **Manuel** : collez les jetons dans Configuration….

Astuce : nommez vos fichiers `jeton-git.txt`, `jeton-drive.txt`,
`jeton-zenodo.txt` pour que l'affectation automatique soit infaillible (le
kit reconnaît aussi les formats JSON, les lignes `clé: valeur`, les préfixes
`ghp_`/`ya29.`, et les jetons Zenodo hexadécimaux de 32 caractères).

## Ligne de commande (serveurs, automatisation)

```bash
python3 TriadeKit.py                          # interface graphique
python3 TriadeKit.py --demo                   # démonstration
python3 TriadeKit.py --cli verification       # une cérémonie sans interface
python3 TriadeKit.py --cli rotation --dossier-jetons ~/Téléchargements
python3 TriadeKit.py --cli cycle-complet --simulation
python3 TriadeKit.py --selftest               # auto-diagnostic complet
```

Codes retour : `0` = succès, `1` = échec, `2` = cérémonie inconnue.

## Sécurité

- Les jetons restent **en local** dans `config/triade.json` ; ils ne sont
  envoyés qu'aux API officielles (GitHub, Google, Zenodo).
- Ils ne sont **jamais journalisés** (affichés masqués `ghp_...x9`) ni
  inclus dans les archives téléversées sur Drive/Zenodo.
- Le jeton GitHub n'est jamais écrit dans `.git/config` : le push l'utilise
  uniquement en mémoire.
- Avant chaque rotation, la configuration courante est archivée
  (`config/triade.avant-rotation-*.json`).
- `config/`, `journal/`, `archives/`, `jetons-importes/` sont ignorés par
  git (`.gitignore` fourni dans ce dossier).

## Dépannage

| Symptôme | Solution |
|---|---|
| « Python est introuvable » (Windows) | Réinstallez Python en cochant *Add Python to PATH*, ou lancez via `py -3 TriadeKit.py`. |
| macOS bloque le lanceur (« développeur non identifié ») | Clic droit sur `LANCEUR-MAC.command` → *Ouvrir*, ou `bash LANCEUR-MAC.command` dans Terminal. |
| « tkinter indisponible » (Linux) | `sudo apt install python3-tk` (ou `python3-tkinter` selon la distribution) — le mode `--cli` fonctionne sans. |
| HTTP 401 sur un pilier | Jeton invalide ou périmé → lancez la cérémonie **Rotation**. |
| HTTP 403 sur un pilier | Portées du jeton insuffisantes (GitHub : `repo` ; Zenodo : deposits). |
| HTTP 404 | Mauvais identifiant de dépôt/dossier — vérifiez la Configuration. |
| La rotation automatique échoue | Le dossier Drive des jetons n'est pas public (« toute personne disposant du lien ») → téléchargez les fichiers et utilisez l'import de dossier. |

## Structure de ce dossier

```
ceremonies/gui/
├── TriadeKit.py             # tout le kit (moteur + GUI), stdlib uniquement
├── LANCEUR-WINDOWS.bat      # 1 double-clic sous Windows
├── LANCEUR-MAC.command      # 1 double-clic sous macOS
├── LANCEUR-LINUX.sh         # 1 double-clic sous Linux
├── LISEZMOI.md              # ce guide
├── docs/EXTENSION.md        # guide développeur (architecture, API, extension)
├── .gitignore               # exclut jetons, journaux, archives
├── config/triade.json       # créé à la configuration (jetons, identifiants, préférences)
├── journal/                 # créé automatiquement : journaux, rapports, historique
├── archives/                # créé automatiquement : archives du projet
└── jetons-importes/         # créé automatiquement : jetons récupérés depuis Drive
```

Pour étendre le kit (nouvelle cérémonie, nouveau pilier), voir
`docs/EXTENSION.md`.
