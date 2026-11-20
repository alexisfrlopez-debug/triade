# Guide des cérémonies — Protocole Triade v1.0

Ce guide contient le déroulé complet des six cérémonies du protocole Triade.
Chaque cérémonie possède : un objectif, des déclencheurs, des prérequis, des
étapes numérotées, des critères de sortie et des artefacts attendus. Une
cérémonie n'est terminée que lorsque sa **fiche** est écrite dans `journal/`
(modèle : `templates/FICHE_CEREMONIE.md`).

Exécution assistée : `python3 scripts/triade_ceremonie.py` (menu interactif,
mode non interactif avec `--c <code> --oui` pour les agents et l'automatisation).
Interface graphique 1-clic : lanceurs de `ceremonies/gui/` (TriadeKit —
vérification, rotation, synchronisation, passage public et cycle complet
en un clic, avec modes simulation et démonstration ; voir
`ceremonies/gui/LISEZMOI.md`).

## Synoptique général

| Code | Cérémonie | Déclencheur principal | Durée type | Sortie clé |
|---|---|---|---|---|
| C0 | Fondation | Démarrage du projet | 30–60 min | Triade instanciée et vérifiée |
| C1 | Rotation des jetons | Échéance ≈ 90 j, fuite, mouvement d'équipe | 20–40 min | Jetons neufs propagés, anciens révoqués |
| C2 | Synchronisation | Fin de séquence de travail | 10–20 min | Trois plateformes cohérentes |
| C3 | Gel & Pack | Jalon de contenu | 30–60 min | Pack versionné + manifeste + tag |
| C4 | Revue & Réception | Avant passage public | 30–45 min | GO / NO-GO consigné |
| C5 | Passage public | GO de C4 uniquement | 20–30 min | Publication Zenodo + DOI |

Ordre de propagation lors de toute écriture multi-plateformes : **Git → Drive →
Zenodo**, sans exception.

---

## C0 — Fondation

**Objectif.** Instancier une triade complète et opérationnelle : dépôt Git,
arborescence Drive, dépôt Zenodo réservé, coffre de jetons, état projet initial.

**Déclencheur.** Création d'un nouveau projet selon le protocole Triade.

**Prérequis.** Comptes Git hébergé / Drive / Zenodo ; kit copié à la racine du
futur dépôt ; droits de création de jetons sur les trois plateformes.

**Participants.** L'humain décide et crée les accès ; l'agent prépare les
structures, vérifie et documente.

**Étapes.**

1. Créer le dépôt Git (privé) et y committer le kit complet (README.md,
   AGENTS.md, SECURITE.md, ceremonies/, templates/, scripts/, docs/).
2. Activer le `.gitignore.triade` (copier dans `.gitignore`) : `.env`,
   `config.json`, `journal/`, `*.token`, `*.key`, `*.pem`, `credentials/`.
3. Créer l'arborescence Drive : `racine-projet/` avec les sous-dossiers
   `documents/`, `packs/` et `coffre-jetons/`.
4. Créer le dépôt Zenodo (statut **réservé**, privé) — ne rien y téléverser
   avant la première version figée.
5. Générer les jetons initiaux, un par plateforme, **privilège minimum**, et
   les déposer dans `coffre-jetons/rotation-AAAA-MM-JJ/`.
6. Remplir `.env` local à partir de `templates/.env.example` (valeurs uniquement
   ici) et `config.json` à partir de `templates/config.example.json`
   (identifiants non sensibles uniquement).
7. Définir la **phrase de contrôle** dans `CONTROLE.md`
   (`templates/CONTROLE.md`) : phrase secrète connue de l'humain seul.
8. Lancer `python3 scripts/triade_hygiene.py` : aucune alerte attendue.
9. Initialiser `ETAT_PROJET.md` et écrire la fiche C0 dans `journal/`.

**Critères de sortie.** Push Git fonctionnel ; accès Drive vérifié en lecture et
écriture ; dépôt Zenodo réservé ; scanner d'hygiène vert ; état projet initialisé.

**Artefacts.** Dépôt Git ; arborescence Drive ; dépôt Zenodo réservé ;
`.env` et `config.json` locaux ; `CONTROLE.md` ; `ETAT_PROJET.md` ;
`journal/C0_AAAA-MM-JJ.md`.

---

## C1 — Rotation des jetons

**Objectif.** Remplacer l'ensemble des jetons d'accès et propager le changement
aux trois plateformes, sans interruption de service.

**Déclencheurs.** Échéance de cadence (90 jours par défaut, configurable dans
`config.json` → `rotation_jetons.cadence_jours`) ; suspicion ou confirmation de
fuite ; arrivée ou départ d'un collaborateur ; changement de périmètre d'accès.

**Prérequis.** Accès au coffre ; droits de création et de révocation de jetons
sur les trois plateformes ; `.env` local accessible.

**Étapes.**

1. Ouvrir la fiche C1 : annoncer la date et le périmètre de la rotation.
2. Créer les **nouveaux** jetons (privilège minimum) **sans révoquer les
   anciens** — sauf fuite confirmée : dans ce cas, révoquer d'abord (cf.
   SECURITE.md, réponse aux incidents).
3. Déposer les nouveaux jetons dans `coffre-jetons/rotation-AAAA-MM-JJ/`.
4. Mettre à jour le `.env` local avec les nouvelles valeurs.
5. Propager et **vérifier par une opération réelle minimale**, dans l'ordre :
   Git (push de test), Drive (écriture de test), Zenodo (appel de test).
6. Révoquer les anciens jetons sur chaque plateforme.
7. Lancer `python3 scripts/triade_hygiene.py` pour vérifier qu'aucun ancien
   jeton ne traîne dans le projet.
8. Écrire la fiche C1 et mettre à jour `ETAT_PROJET.md` (date de rotation,
   prochaine échéance).

**Critères de sortie.** Trois plateformes vérifiées sur les nouveaux jetons ;
anciens jetons révoqués ; scanner vert ; échéance recalculée et consignée.

**Artefacts.** `coffre-jetons/rotation-AAAA-MM-JJ/` ; `.env` mis à jour ;
`journal/C1_AAAA-MM-JJ.md` ; `ETAT_PROJET.md` mis à jour.

---

## C2 — Synchronisation

**Objectif.** Ramener les trois plateformes à un état cohérent après une
séquence de travail.

**Déclencheur.** Fin d'une séquence de travail ; obligation avant toute
cérémonie C3.

**Étapes.**

1. Git : relecture du diff, commits atomiques et commentés, push.
2. Drive : téléverser ou mettre à jour les documents vivants modifiés.
3. Contrôle de cohérence : les versions annoncées correspondent aux fichiers
   réellement présents ; aucune divergence de nommage.
4. Fiche C2 dans `journal/` (une fiche légère suffit si aucune anomalie).

**Critères de sortie.** Trois plateformes cohérentes entre elles ; aucune
divergence non consignée.

**Artefacts.** `journal/C2_AAAA-MM-JJ.md` ; documents Drive à jour.

---

## C3 — Gel & Pack

**Objectif.** Figer un état cohérent du projet et régénérer le pack de
livrables versionné, prêt pour la revue puis la publication.

**Déclencheur.** Jalon de contenu : ensemble documentaire stabilisé, correction
importante intégrée, ou échéance de publication.

**Prérequis.** C2 préalable obligatoire (les trois plateformes sont cohérentes).

**Étapes.**

1. Choisir le numéro de version selon la sémantique du protocole :
   MAJEUR = rupture de structure du pack, MINEUR = contenu nouveau, PATCH =
   corrections sans ajout (exemple : v0.19.5 → v0.20.0 si un document s'ajoute).
2. Geler l'état : créer le tag Git du même numéro de version.
3. Régénérer **complètement** les documents du pack — composition définie dans
   `config.json` → `pack.documents` (exemple canonique de cinq documents :
   manuscrit, présentation, dossier de soumission, pack complet, rapport de
   vérification). Une version figée ne s'édite jamais à la main.
4. Calculer les empreintes SHA-256 de chaque fichier du pack et remplir
   `templates/PACK_MANIFEST.md`.
5. Téléverser le pack dans Drive `packs/vX.Y.Z/`.
6. Mettre à jour `CHANGELOG.md` (différences depuis la version précédente).
7. Écrire la fiche C3 et mettre à jour `ETAT_PROJET.md`.

**Critères de sortie.** Pack versionné complet ; manifeste rempli avec
empreintes ; tag Git ; dossier Drive horodaté ; changelog à jour.

**Artefacts.** `packs/vX.Y.Z/` ; manifeste de pack ; tag Git ; changelog ;
`journal/C3_AAAA-MM-JJ.md`.

---

## C4 — Revue & Réception

**Objectif.** Valider formellement, avant toute publication publique, la
qualité, l'exactitude et la salubrité (absence de fuite d'accès) du pack.

**Déclencheur.** Intention de passage public, ou jalon majeur du projet.

**Étapes.**

1. Revue du manifeste : chaque document, chaque empreinte SHA-256 vérifiée.
2. Revue de contenu : exactitude des faits, mentions, licences, autorisations
   de diffusion de chaque document du pack.
3. Lancer `python3 scripts/triade_hygiene.py` sur le pack exact qui sera
   publié, puis sur l'ensemble du projet.
4. Relecture humaine anti-fuite (le scanner ne voit pas les captures d'écran,
   les PDF embarqués, les métadonnées ni les noms de fichiers évocateurs).
5. Produire le résumé de session normalisé.
6. Décision humaine explicite **GO** ou **NO-GO**, consignée dans la fiche C4
   avec la date et le décideur.
7. Mettre à jour `ETAT_PROJET.md`.

**Critères de sortie.** Décision GO/NO-GO consignée ; en cas de NO-GO, liste
des points bloquants avec responsable et échéance.

**Artefacts.** `journal/C4_AAAA-MM-JJ.md` ; résumé de session ; `ETAT_PROJET.md`
mis à jour.

---

## C5 — Passage public

**Objectif.** Publier la version validée sur Zenodo en accès public et en
obtenir le DOI citable.

**Déclencheur.** Décision GO de la cérémonie C4, et elle seule.

**Étapes.**

1. Re-vérifier le GO de C4 et son horodatage dans `journal/`.
2. Dernier scan d'hygiène **sur le pack exact qui sera publié**.
3. Téléverser le pack sur le dépôt Zenodo avec des métadonnées complètes :
   titre, auteurs, version, licence, description, date.
4. Passer le dépôt en **public** et récupérer le DOI attribué.
5. Consigner le DOI dans `ETAT_PROJET.md` et dans le manifeste du pack.
6. Git : créer la release correspondant au tag, mentionnant le DOI.
7. Écrire la fiche C5, mettre à jour le changelog si besoin, et produire le
   résumé de session.

**Critères de sortie.** DOI actif et vérifiable ; dépôt Zenodo public ;
release Git ; DOI consigné.

**Artefacts.** DOI ; release Git ; `journal/C5_AAAA-MM-JJ.md` ; manifeste et
état projet mis à jour.

**Note d'irréversibilité.** Sur Zenodo, une version publiée ne peut pas être
modifiée en place : toute correction passe par une nouvelle version du pack
(nouvelle cérémonie C3 puis C4 puis C5). D'où l'exigence du GO formel.

---

## Journal des cérémonies

Toutes les fiches sont écrites dans `journal/` avec la nomenclature
`CX_AAAA-MM-JJ.md` (exemple : `journal/C3_2026-11-20.md`). Le journal peut
rester privé (il est ignoré par git par défaut) ou être publié selon la
politique du projet — dans ce dernier cas, retirer la ligne `journal/` du
`.gitignore` après vérification qu'il ne contient aucune donnée sensible.
