# EXTENSION du Triade Kit — guide développeur

Architecture interne du kit, endpoints API utilisés et procédure pour l'étendre. Tout vit dans un fichier unique (`TriadeKit.py`), en Python stdlib uniquement — aucune dépendance à ajouter.

## 1. Architecture

```
TriadeKit.py
├── HTTP / ReponseHTTP      client HTTP minimal (urllib), timeout, statut 0 = réseau KO
├── Config                  chargement/sauvegarde atomique de config/triade.json
│                            (fusion avec CONFIG_DEFAUT = tolérant aux clés manquantes)
├── Journal                 lignes horodatées -> console ou GUI, fichiers journal/*.log,
│                            rapports JSON, historique.jsonl
├── Piliers (1 par plateforme)
│   ├── PilierGit           GitHub REST + git local (init/add/commit/push)
│   ├── PilierDrive         Drive API v3 (about, files, permissions, upload multipart)
│   ├── PilierZenodo        Zenodo REST (depositions, newversion, bucket, publish)
│   └── DemoPilier*         mêmes interfaces, comportements simulés (mode démo)
├── construire_piliers()    fabrique : piliers réels ou de démonstration
├── extraire_jetons()       parsing de fichiers de jetons (JSON / clé:valeur / brut)
├── construire_archive()    zip du projet, jetons et config exclus
├── Cérémonies (Ceremonie + 6 sous-classes)
│   └── FABRIQUE            registre identifiant -> classe
├── Interface (tkinter)     fenêtre 1-clic : boutons, voyants, journal, progression,
│                            thread de travail + file de messages (thread-safe)
└── mode_cli / auto_diagnostic / main
```

Principes :
- **Une cérémonie = une suite d'étapes journalisées** qui se termine par un rapport (`finaliser(succes)`). Les étapes sous-lèvent `ErreurPilier` pour un échec propre et lisible.
- **Le mode simulation (`dry=True`) traverse toute la pile** : chaque pilier journalise ce qu'il ferait sans rien écrire. Le mode démo remplace simplement les piliers par des doublons simulés.
- **La GUI ne touche jamais aux widgets depuis les threads** : le worker pousse des messages (`ligne`, `avancement`, `led`, `fin`) dans une file, consommée par la boucle `after(150, ...)`.

## 2. Endpoints utilisés

| Pilier | Endpoint | Usage |
|---|---|---|
| Git | `GET https://api.github.com/user` | validation du jeton |
| Git | `GET/PATCH /repos/{owner}/{repo}` | état du dépôt / passage public (`{"private": false}`) |
| Git | `git -C <dossier> init/add/commit/push` | synchronisation locale (jeton passé dans l'URL du push uniquement, jamais persisté) |
| Drive | `POST https://oauth2.googleapis.com/token` | rafraîchissement du jeton d'accès |
| Drive | `GET /drive/v3/about?fields=user` | validation du jeton |
| Drive | `POST /drive/v3/files` (mimeType folder) | création du dossier projet |
| Drive | `POST /upload/drive/v3/files?uploadType=multipart` | téléversement de l'archive |
| Drive | `POST /drive/v3/files/{id}/permissions` (`anyone/reader`) | partage en lecture |
| Drive | `GET drive.google.com/drive/folders/{id}` + `drive.usercontent.google.com/download` | lecture du dossier public des jetons (sans authentification) |
| Zenodo | `GET/POST {base}/deposit/depositions` | validation / création de dépôt |
| Zenodo | `POST /deposit/depositions/{id}/actions/newversion` puis `GET links.latest_draft` | préparation d'une nouvelle version |
| Zenodo | `PUT {bucket}/{fichier}` | téléversement des fichiers |
| Zenodo | `POST /deposit/depositions/{id}/actions/publish` | publication (DOI) |

`{base}` = `https://sandbox.zenodo.org/api` ou `https://zenodo.org/api` selon la configuration.

## 3. Ajouter une cérémonie

1. Créer une sous-classe de `Ceremonie` :

```python
class MaCeremonie(Ceremonie):
    nom = "Ma ceremonie"
    nom_id = "ma-ceremonie"
    description = "Ce qu'elle fait."

    def executer(self):
        self.j.titre("Ceremonie ... - %s" % datetime.now().strftime("%d/%m/%Y %H:%M"))
        self.total = 2
        self.etape(1, "Premiere etape")
        try:
            self.piliers["git"].synchroniser(dry=self.simulation or self.demo)
        except ErreurPilier as e:
            self._erreur("Git : %s" % e)
            return self.finaliser(False)
        self.etape(2, "Deuxieme etape")
        self.j.ok("termine")
        return self.finaliser(True)
```

2. L'enregistrer dans `FABRIQUE` (`"ma-ceremonie": MaCeremonie`) et dans `CEREMONIES` pour le bouton GUI.
3. Elle devient aussitôt disponible en CLI (`--cli ma-ceremonie`), dans le journal, les rapports et l'historique.

## 4. Ajouter un pilier (4e plateforme)

1. Sous-classer `Pilier` avec `nom`, `cle` (clé de section dans `triade.json`) et implémenter `verifier()` (retourne `(etat, detail)`, `etat` ∈ `ok / partiel / invalide / absent / erreur`) + `valider_jeton()`.
2. Ajouter les méthodes métier (elles reçoivent toujours `dry=` et journalisent via `self.j`).
3. Créer un `DemoPilierX` correspondant et l'ajouter aux deux tuples de `construire_piliers()`.
4. Ajouter la section dans `CONFIG_DEFAUT` et les champs dans `Interface.ouvrir_configuration()`.

## 5. Tests recommandés

```bash
python3 TriadeKit.py --selftest                 # auto-diagnostic complet (cycle démo inclus)
python3 TriadeKit.py --demo --cli cycle-complet # cycle complet simulé de bout en bout
python3 TriadeKit.py --cli verification         # attendu : échec propre si aucun jeton
python3 TriadeKit.py --cli rotation --dossier-jetons <dossier de test>
```

Convention : toute cérémonie doit réussir en mode `--demo` et ne rien écrire en mode `--simulation`.
